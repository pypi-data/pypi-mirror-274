from __future__ import annotations

import re
import shlex

from dataclasses import dataclass
from typing import Optional
from collections.abc import Iterable, Iterator
from collections import deque
from copy import copy


@dataclass
class Root:
    name: str
    path: str
    version: str
    delimiter: str
    children: list[Node]
    stubs: list[str]
    begin: int
    end: int

    def __repr__(self) -> str:
        r = 'Root:\n'
        r += f'\tVersion: {self.version if self.version else "unset"}\n'
        r += f'\tDelimiter: {self.delimiter}\n'
        r += f'\tBegins at: {self.begin}\n'
        r += f'\tEnds at: {self.end}\n'
        r += f'\tNumber of children: {len(self.children)}\n'
        r += f'\tNumber of stubs: {len(self.stubs)}'
        return r


@dataclass
class Node:
    name: str
    path: str
    parent: Root | Node
    children: list[Node]
    stubs: list[str]
    is_closed: bool
    is_inactive: bool
    is_protect: bool
    begin: int
    end: int

    def __repr__(self) -> str:
        r = 'Node:\n'
        r += f'\tName: {self.name}\n'
        r += f'\tPath: {self.path}\n'
        r += f'\tBegins at: {self.begin}\n'
        r += f'\tEnds at: {self.end}\n'
        r += f'\tNumber of children: {len(self.children)}\n'
        r += f'\tNumber of stubs: {len(self.stubs)}\n'
        r += f'\tIs closed: {self.is_closed}\n'
        r += f'\tIs inactive: {self.is_inactive}\n'
        r += f'\tIs protect: {self.is_protect}'
        return r


def unstrict_compare(left: list[str], right: list[str]) -> bool:
    """Function compares the two lists and returns True whether they are equal.

    For every list element, an extra argument is accounted for to cover cases when these elements
        are inactive and/or protected.
    """
    if len(left) != len(right):
        return False

    dleft = deque(left)
    dright = deque(right)

    extra_pattern = r'^(?:inactive: |protect: ){0,2}'

    while True:
        lml = dleft.popleft()
        lmr = dright.popleft()
        if lml == lmr or re.match(extra_pattern + lml, lmr) or re.match(extra_pattern + lmr, lml):
            if dleft or dright:
                continue
            return True
        return False


def parser(data: Iterable[str], *, path: str, delimiter='^', greedy=False) -> tuple[list[str], list[str]]:
    if not isinstance(data, list) and greedy:
        return [], []

    bom_symbol = '\ufeff'
    sections: list[str] = []
    params: list[str] = []
    container: list[str] = []

    path_parts = path.split(delimiter) if path else []
    path_found = False if path else True

    start = 0

    for line_number, line in enumerate(data):
        if bom_symbol in line:
            # in case, when file is UTF-8 encoded with BOM
            # but opened with UTF-8 encoding and errors ignoring mode
            line = line.replace(bom_symbol, '')

        stripped = line.strip()

        if '{' in stripped and '}' not in stripped and ';' not in stripped:
            parts = stripped.split('{')
            section_name = parts[0]
            section_name = section_name.strip()

            if not section_name:
                return [], []

            sections.append(section_name)

            if not path_found:
                if len(sections) == len(path_parts) and unstrict_compare(sections, path_parts):
                    path_found = True
                    start = line_number
                    container.append(stripped)
            else:
                container.append(stripped)

        elif '}' in stripped and '{' not in stripped and ';' not in stripped:
            if path_found and len(sections) >= len(path_parts):
                container.append('}')

                if path_found and len(sections) == len(path_parts):
                    if greedy:
                        assert type(data) is list
                        del data[start : line_number + 1]

                    return container, params

            sections.pop()

        elif ';' in stripped and '{' not in stripped and '}' not in stripped:
            if path_found:
                if len(sections) == len(path_parts):
                    params.append(stripped)
                container.append(stripped)

    return container, params


def lazy_parser(data: Iterable[str], *, path: str, delimiter='^', top_level=True) -> Iterator[str]:
    bom_symbol = '\ufeff'
    sections: list[str] = []

    path_parts = path.split(delimiter) if path else []
    path_found = False if path else True

    for line in data:
        if bom_symbol in line:
            # in case, when file is UTF-8 encoded with BOM
            # but opened with UTF-8 encoding and errors ignoring mode
            line = line.replace(bom_symbol, '')

        stripped = line.strip()

        if '{' in stripped and '}' not in stripped and ';' not in stripped:
            parts = stripped.split('{')
            section_name = parts[0]
            section_name = section_name.strip()

            if not section_name:
                raise ValueError('Empty section name.')

            sections.append(section_name)

            if not path_found:
                if len(sections) == len(path_parts) and unstrict_compare(sections, path_parts):
                    path_found = True

                    if top_level:
                        yield stripped
            else:
                yield stripped

        elif '}' in stripped and '{' not in stripped and ';' not in stripped:
            if path_found:
                if len(sections) > len(path_parts):
                    yield stripped
                elif len(sections) == len(path_parts):
                    if top_level:
                        yield stripped

                    return

            sections.pop()

        elif ';' in stripped and '{' not in stripped and '}' not in stripped:
            if path_found:
                yield stripped


def wildcard_parser(
    data: Iterable[str], *, path: str, pattern: str, delimiter='^'
) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    if pattern.startswith('^'):
        pattern = pattern[1:]

    if not pattern:
        return {}, {}

    pattern = r'^(?:inactive: |protect: ){0,2}' + pattern
    bom_symbol = '\ufeff'

    sections = []
    container: dict[str, list[str]] = {}
    params: dict[str, list[str]] = {}

    path_parts = path.split(delimiter) if path else []
    path_found = False if path else True

    for line in data:
        if bom_symbol in line:
            # in case, when file is UTF-8 encoded with BOM
            # but opened with UTF-8 encoding and errors ignoring mode
            line = line.replace(bom_symbol, '')

        stripped = line.strip()

        if '{' in stripped and '}' not in stripped and ';' not in stripped:
            parts = stripped.split('{')
            section_name = parts[0]
            section_name = section_name.strip()

            if not section_name:
                return {}, {}

            sections.append(section_name)

            if path_found:
                key = sections[len(path_parts)]

                if re.match(pattern, key, re.IGNORECASE):
                    if key not in container:
                        container[key] = []
                        params[key] = []

                    container[key].append(stripped)

            else:
                if len(sections) == len(path_parts) and unstrict_compare(sections, path_parts):
                    path_found = True

        elif '}' in stripped and '{' not in stripped and ';' not in stripped:
            last = sections.pop()

            if path_found:
                if len(sections) < len(path_parts):
                    return container, params

                elif len(sections) > len(path_parts):
                    section_name = sections[len(path_parts)]
                else:
                    section_name = last

                if re.match(pattern, section_name, re.IGNORECASE):
                    container[section_name].append('}')

        elif ';' in stripped and '{' not in stripped and '}' not in stripped:
            if path_found:
                if len(sections) > len(path_parts):
                    section_name = sections[len(path_parts)]

                    if re.match(pattern, section_name, re.IGNORECASE):
                        container[section_name].append(stripped)

                        if len(sections) == len(path_parts) + 1:
                            params[section_name].append(stripped)

    return container, params


def lazy_wildcard_parser(data: Iterable[str], *, path: str, pattern: str, delimiter='^') -> Iterator[str]:
    if pattern.startswith('^'):
        pattern = pattern[1:]

    if not pattern:
        return {}, {}

    pattern = r'^(?:inactive: |protect: ){0,2}' + pattern
    bom_symbol = '\ufeff'

    sections = []

    path_parts = path.split(delimiter) if path else []
    path_found = False if path else True

    for line in data:
        if bom_symbol in line:
            # in case, when file is UTF-8 encoded with BOM
            # but opened with UTF-8 encoding and errors ignoring mode
            line = line.replace(bom_symbol, '')

        stripped = line.strip()

        if '{' in stripped and '}' not in stripped and ';' not in stripped:
            parts = stripped.split('{')
            section_name = parts[0]
            section_name = section_name.strip()

            if not section_name:
                return {}, {}

            sections.append(section_name)

            if path_found:
                key = sections[len(path_parts)]

                if re.match(pattern, key, re.IGNORECASE):
                    yield stripped

            else:
                if len(sections) == len(path_parts) and unstrict_compare(sections, path_parts):
                    path_found = True

        elif '}' in stripped and '{' not in stripped and ';' not in stripped:
            last = sections.pop()

            if path_found:
                if len(sections) < len(path_parts):
                    return

                elif len(sections) > len(path_parts):
                    section_name = sections[len(path_parts)]
                else:
                    section_name = last

                if re.match(pattern, section_name, re.IGNORECASE):
                    yield '}'

        elif ';' in stripped and '{' not in stripped and '}' not in stripped:
            if path_found:
                if len(sections) > len(path_parts):
                    section_name = sections[len(path_parts)]

                    if re.match(pattern, section_name, re.IGNORECASE):
                        yield stripped


def provide_config(data: Iterable[str], *, block=' ' * 2) -> str:
    accum_depth = 0
    flag = False
    result = ''

    for line in data:
        stripped = line.strip()

        if '{' in stripped and '}' not in stripped and ';' not in stripped:
            accum_depth += 1
            flag = True

        elif '}' in stripped and '{' not in stripped and ';' not in stripped:
            if accum_depth:
                accum_depth -= 1

        if flag:
            prepend = block * (accum_depth - 1)
            flag = False
        else:
            prepend = block * accum_depth

        result += prepend + stripped + '\n'

    return result


def lazy_provide_config(data: Iterable[str], *, block=' ' * 2, hide_secrets=True, end='') -> Iterator[str]:
    accum_depth = 0
    flag = False

    for line in data:
        stripped = line.strip()

        if '{' in stripped and '}' not in stripped and ';' not in stripped:
            accum_depth += 1
            flag = True

        elif '}' in stripped and '{' not in stripped and ';' not in stripped:
            if accum_depth:
                accum_depth -= 1

        elif hide_secrets and ';' in stripped and '{' not in stripped and '}' not in stripped:
            if stripped.endswith('## SECRET-DATA'):
                try:
                    parts = shlex.split(stripped)
                    if parts[-3] != '*/;':
                        parts[-3] = '/* SECRET-DATA */;'
                        stripped = ' '.join(parts)
                except Exception:
                    ...

        if flag:
            prepend = block * (accum_depth - 1)
            flag = False
        else:
            prepend = block * accum_depth

        yield prepend + stripped + end


def lazy_provide_inactives(tree: Root | Node, *, skip=True) -> Iterator[str]:
    if not skip:
        if type(tree) is Node and tree.is_inactive:
            yield f'inactive: {tree.name} {{'
        else:
            yield tree.name + ' {'

    for child in tree.children:
        yield from lazy_provide_inactives(child, skip=False)

    for stub in tree.stubs:
        yield stub

    if not skip:
        yield '}'


def lazy_provide_protect(tree: Root | Node, *, skip=True) -> Iterator[str]:
    if not skip:
        if type(tree) is Node and tree.is_protect:
            yield f'protect: {tree.name} {{'
        else:
            yield tree.name + ' {'

    for child in tree.children:
        yield from lazy_provide_protect(child, skip=False)

    for stub in tree.stubs:
        yield stub

    if not skip:
        yield '}'


def lazy_provide_compare(tree: Root | Node, *, skip=True) -> Iterator[str]:
    if not skip:
        yield tree.name + ' {'

    for child in tree.children:
        yield from lazy_provide_compare(child, skip=False)

    yield from tree.stubs

    if tree.name[0] in ('+', '-'):
        yield tree.name[0] + '}'
    else:
        if not skip:
            yield '}'


def search_inactives(tree: Root | Node) -> Optional[Root | Node]:
    copied_tree = copy(tree)
    copied_tree.children = []
    copied_tree.stubs = []

    for child in tree.children:
        if next_node := search_inactives(child):
            assert type(next_node) is Node
            copied_tree.children.append(next_node)
            next_node.parent = copied_tree

    inactives = list(filter(lambda x: x.startswith('inactive: '), tree.stubs))
    copied_tree.stubs = inactives

    if copied_tree.children or inactives or (type(copied_tree) is Node and copied_tree.is_inactive):
        return copied_tree

    return None


def search_protects(tree: Root | Node) -> Optional[Root | Node]:
    copied_tree = copy(tree)
    copied_tree.children = []
    copied_tree.stubs = []

    for child in tree.children:
        if next_node := search_protects(child):
            assert type(next_node) is Node
            copied_tree.children.append(next_node)
            next_node.parent = copied_tree

    protects = list(filter(lambda x: 'protect: ' in x, tree.stubs))
    copied_tree.stubs = protects

    if copied_tree.children or protects or (type(copied_tree) is Node and copied_tree.is_protect):
        return copied_tree

    return None


def compare_nodes(target: Root | Node, peer: Root | Node) -> Optional[Root | Node]:
    def copy_node(origin: Node, new_parent: Optional[Root | Node] = None, sign='') -> Node:
        copied_node = copy(origin)
        copied_node.name = sign + copied_node.name

        if new_parent:
            copied_node.parent = new_parent

        copied_node.children = []
        copied_node.stubs = []

        return copied_node

    if target.name != peer.name:
        return None

    copied_target = copy(target)
    copied_target.children = []
    copied_target.stubs = []

    peer_children = copy(peer.children)

    for child in target.children:
        for peer_child in peer.children:
            if child.name == peer_child.name:
                peer_children.remove(peer_child)

                if next_node := compare_nodes(child, peer_child):
                    assert type(next_node) is Node
                    next_node.parent = copied_target
                    copied_target.children.append(next_node)

                break
        else:
            copied_child = copy_node(child, copied_target, '+')
            copied_target.children.append(copied_child)

    for child in peer_children:
        copied_child = copy_node(child, copied_target, '-')
        copied_target.children.append(copied_child)

    if type(copied_target) is Node and type(peer) is Node:
        if copied_target.is_protect != peer.is_protect:
            if copied_target.is_protect:
                copied_target.name = 'protect(-): ' + copied_target.name
            else:
                copied_target.name = 'protect(+): ' + copied_target.name

        if copied_target.is_inactive != peer.is_protect:
            if copied_target.is_inactive:
                copied_target.name = 'inactive(+): ' + copied_target.name
            else:
                copied_target.name = 'inactive(-): ' + copied_target.name

    target_stubs = set(target.stubs)
    peer_stubs = set(peer.stubs)

    copied_target.stubs.extend(list('+' + x for x in target_stubs - peer_stubs))
    copied_target.stubs.extend(list('-' + x for x in peer_stubs - target_stubs))

    if copied_target.stubs or copied_target.children:
        return copied_target

    return None


def search_node(path: deque[str], node: Root | Node) -> Optional[Node]:
    if not path:
        return None

    step = path.popleft()
    step = step.lower()

    if '.' in step and node.name == 'interfaces':
        try:
            ifd, ifl = step.split('.')

        except ValueError:
            return None

        if not ifd or not ifl or not ifl.isdigit():
            return None

        step = ifd
        path.appendleft('unit ' + ifl)

    if not node.children:
        return None

    for child in node.children:
        if child.name.lower() == step:
            if not path:
                return child
            return search_node(path, child)

    if not path:
        return None

    extra = path.popleft()
    path.appendleft(step + ' ' + extra)
    return search_node(path, node)


def make_path(str_path: str, *, delimiter='^') -> deque[str]:
    return deque(str_path.split(delimiter))


def construct_path(node: Root | Node, *, delimiter='^') -> str:
    while True:
        if type(node) is Root:
            break
        assert type(node) is Node
        extra = construct_path(node.parent, delimiter=delimiter)
        return extra + delimiter + node.name
    return node.name


def construct_tree(data: Iterable[str], *, delimiter='^') -> Optional[Root]:
    root = Root(name='root', path='', version='', delimiter=delimiter, children=[], stubs=[], begin=0, end=0)
    current_node: Root | Node = root

    bom_symbol = '\ufeff'
    line_number = 0

    for line_number, line in enumerate(data):
        if bom_symbol in line:
            # in case, when file is UTF-8 encoded with BOM
            # but opened with UTF-8 encoding and errors ignoring mode
            line = line.replace(bom_symbol, '')

        stripped = line.strip()

        if '{' in stripped and '}' not in stripped and ';' not in stripped:
            parts = stripped.split('{')
            section_name = parts[0]
            section_name = section_name.strip()

            if not section_name:
                return None

            if 'inactive: ' in section_name:
                section_name = section_name.replace('inactive: ', '')

            if 'protect: ' in section_name:
                section_name = section_name.replace('protect: ', '')

            node = Node(
                name=section_name,
                path='',
                parent=current_node,
                children=[],
                stubs=[],
                is_closed=False,
                is_inactive='inactive: ' in parts[0],
                is_protect='protect: ' in parts[0],
                begin=line_number,
                end=0,
            )
            node.path = construct_path(node, delimiter=delimiter)
            node.path = node.path.replace('root' + delimiter, '')

            current_node.children.append(node)
            current_node = node

        elif '}' in stripped and '{' not in stripped and ';' not in stripped:
            if type(current_node) is Node:
                current_node.is_closed = True
                current_node.end = line_number
                current_node = current_node.parent
            else:
                print(line_number)

        elif ';' in stripped and '{' not in stripped and '}' not in stripped:
            parts = stripped.split(';')
            stub = parts[0] + ';'

            if not stub:
                continue

            current_node.stubs.append(stub)

            if type(current_node) is Root and stub.startswith('version '):
                if len(parts := stub.split()) == 2:
                    root.version = parts[1]

    root.end = line_number

    if root.begin == root.end == 0:
        return None

    if root.children and not root.children[-1].is_closed:
        return None

    return root
