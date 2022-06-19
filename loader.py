from pathlib import Path
from typing import Union

import yaml

import common
import ui
from lib.ecs.ecs import Entity


def convert(convertee, path, conversion, expected_type=None):
    return _convert(
        convertee,
        path.split('.'),
        lambda x:
            conversion(x)
            if expected_type is None or isinstance(x, expected_type)
            else x
    )


def _convert(convertee, path, conversion):
    match path:
        case ['*']:
            assert isinstance(convertee, Union[dict, list]), \
                "Can iterate only through dict or list, sorry."

            for key, value in (
                convertee.items()
                if isinstance(convertee, dict)
                else enumerate(convertee)
            ):
                convertee[key] = conversion(value)

        case [head]:
            assert not isinstance(head, list)
            if head in convertee:
                convertee[head] = conversion(convertee[head])

        case ['*', *tail]:
            assert isinstance(convertee, Union[dict, list]), \
                "Can iterate only through dict or list, sorry."

            for value in (
                convertee.values()
                if isinstance(convertee, dict)
                else convertee
            ):
                _convert(value, tail, conversion)

        case [head, *tail]:
            assert not isinstance(head, list)
            if head in convertee:
                _convert(convertee[head], tail, conversion)


class Location(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.npcs = set()

        convert(self, 'states.*.if', condition, str)
        convert(self, 'states.*.options.*.does', script, str)
        convert(self, 'states.*.options.*.if', condition, str)


class Player(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.is_player = True
        self.memory = set()

    @staticmethod
    def mind(self, world):
        if 'will_talk_to' in self:
            return

        current_states = {
            name: state for name, state in self.location.states.items()
            if 'if' not in state or state['if'](self.location, self, world)
        }

        ui.describe_interior(current_states)

        for state_name in current_states:
            self.memory.add(f'{self.location.name}.{state_name}')

        options = [
            option
            for state in current_states.values()
            for option in state.get('options', [])
            if 'if' not in option or option['if'](self.location, self, world)
        ]

        ui.choose(options, skip=(True, {'does': lambda *_: None}))['does'](self.location, self, world)


class Npc(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)

        unpack_dict = lambda d: tuple(d.items())[0]
        convert(self, 'dialogue.*.lines.*', lambda x: ': '.join(unpack_dict(x)), dict)
        convert(self, 'dialogue.*.options.*.if', condition, str)
        convert(self, 'mind', script, str)
        convert(self, 'mind', lambda m: lambda self, world: m(self, None, world))


def code(source, kind):
    def freezed_script(self, player, world):
        return kind(source, {}, {
            'locations': world.locations,
            'npcs': world.npcs,
            'self': self,
            'player': player,
            'common': common,
        })

    return freezed_script


condition = lambda x: code(x, eval)
script = lambda x: code(x, exec)


for tag in [Location, Player, Npc]:
    yaml.SafeLoader.add_constructor(
        '!' + tag.__name__.lower(),
        (lambda tag_:
            lambda loader, node:
                tag_(**loader.construct_mapping(node, True))
        )(tag)
    )

yaml.SafeLoader.add_constructor(
    '!script',
    lambda loader, node: code(loader.construct_scalar(node), exec)
)

yaml.SafeLoader.add_constructor(
    '!condition',
    lambda loader, node: code(loader.construct_scalar(node), eval)
)


def load(path, ms):
    path = Path(path)
    assert path.exists()

    if path.is_dir():
        result = Entity(**{
            entity.name: entity
            for entity in (
                load(p, ms)
                for p in path.iterdir()
                if p.suffix in ('.yaml', '.yml') or p.is_dir()
            )
        })
    elif path.suffix in ('.yaml', '.yml'):
        result = ms.create(
            **dict(yaml.safe_load(path.read_text(encoding='utf8'))),
        )
    else:
        result = Entity(content=path.read_text(encoding='utf8'))

    result.name = path.stem
    return result


def load_assets(ms):
    world = load('assets', ms)

    for _, npc in world.npcs:
        location = world.locations[npc.location]
        location.npcs.add(npc)
        npc.location = location

    return world
