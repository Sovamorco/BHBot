from enum import Enum, auto
from typing import Optional, Callable

from direct_input import VirtualInput


# noinspection PyArgumentList
class Direction(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()


class MenuItem:
    def __init__(self, name: str):
        self.name = name
        self.position: Optional[int] = None  # assigned by parent
        self.parent: Optional['Layout'] = None  # assigned by parent

    def move_to_parent(self, vi: VirtualInput) -> list[Callable]:
        return []

    def _move_to(self, target: 'MenuItem', vi: VirtualInput) -> list[Callable]:
        if self.parent is None:
            raise Exception('Trying to move from orphan')
        if isinstance(target, ThirdColumn):
            # noinspection PyUnresolvedReferences
            if find_element('first_column').current_position > 6:
                target.current_position = 2
            else:
                target.current_position = 1
        if target == self.parent:
            return self.move_to_parent(vi)
        if target in self.parent.contents:
            if self.parent.direction == Direction.HORIZONTAL:
                return (target.position - self.position) * [vi.right] + (self.position - target.position) * [vi.left]
            return (target.position - self.position) * [vi.down] + (self.position - target.position) * [vi.up]
        raise Exception('Trying to move to non-adjacent node')

    def move_to(self, target: 'MenuItem', vi: VirtualInput) -> list[Callable]:
        path = path_between(self, target)
        steps = []
        for i in range(len(path) - 1):
            steps += path[i]._move_to(path[i + 1], vi)
        return steps


class Layout(MenuItem):
    def __init__(self, name: str, contents: list[MenuItem], base_position: int,
                 direction: Direction):
        super().__init__(name)
        for pos, item in enumerate(contents):
            item.parent = self
            item.position = pos
        self.contents = contents
        self.current_position = base_position
        self.direction = direction

    @property
    def current_element(self):
        return self.contents[self.current_position]

    def _move_to(self, target: 'MenuItem', vi: VirtualInput) -> list[Callable]:
        if target in self.contents:
            steps = self.current_element._move_to(target, vi)
            self.current_position = target.position
            return steps
        return super()._move_to(target, vi)


class MiniMenu(Layout):
    def move_to_parent(self, vi: VirtualInput) -> list[Callable]:
        self.parent.current_position = 1
        return [vi.dodge]


class ThirdColumn(Layout):
    pass


def find_element(name: str, layout: Layout = None) -> Optional[MenuItem]:
    if layout is None:
        layout = main_layout
    for item in layout.contents:
        if item.name == name:
            return item
        if isinstance(item, Layout):
            res = find_element(name, item)
            if res is not None:
                return res
    return None


def distance_to_root(node: MenuItem) -> int:
    distance = 0
    while node.parent is not None:
        distance += 1
        node = node.parent
    return distance


def path_between(source: MenuItem, target: MenuItem) -> list[MenuItem]:
    steps = [source]
    reverse_steps = [target]

    # find distance to root
    source_d = distance_to_root(source)
    target_d = distance_to_root(target)

    while source_d > target_d:
        steps.append(source.parent)
        source = source.parent
        source_d -= 1
    while target_d > source_d:
        reverse_steps.append(target.parent)
        target = target.parent
        target_d -= 1

    while source.parent != target.parent:
        steps.append(source.parent)
        source = source.parent
        reverse_steps.append(target.parent)
        target = target.parent

    return steps + list(reversed(reverse_steps))


def generate_layout():
    options_items = [
        MenuItem(name) for name in [
            'system_settings',
            'controls',
            'change_region',
            'report_bug',
            'image_render_tool',
            'legal',
            'exit_game',
        ]
    ]
    options = Layout('options', options_items, 0, Direction.VERTICAL)

    mini_menu_items = [
        MenuItem(name) for name in [
            'inventory',
            'store',
            'battle_pass',
            'notifications',
            'friends',
            'clans',
            'replays',
        ]
    ]
    mini_menu_items.append(options)
    mini_menu = MiniMenu('mini_menu', mini_menu_items, 0, Direction.HORIZONTAL)

    third_column_items = [
        mini_menu,
        MenuItem('smol_ad'),
        MenuItem('smoller_ad'),
    ]

    second_column_items = [
        MenuItem('big_ad'),
    ]

    first_column_items = [
        MenuItem(name) for name in [
            'play',
            'ranked',
            'battle_pass',
            'custom_game_room',
            'brawl',
            'offline',
            'meet_the_legends',
            'store',
        ]
    ]
    first_column = Layout('first_column', first_column_items, 0, Direction.VERTICAL)

    main_layout_items = [
        first_column,
        Layout('second_column', second_column_items, 0, Direction.VERTICAL),
        ThirdColumn('third_column', third_column_items, 1, Direction.VERTICAL),
    ]
    main = Layout('main', main_layout_items, 0, Direction.HORIZONTAL)
    return main


main_layout = generate_layout()


def regenerate_layout():
    global main_layout
    main_layout = generate_layout()
