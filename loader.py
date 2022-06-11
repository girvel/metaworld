from functools import wraps
from pathlib import Path

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
    head, tail = path[0], path[1:]

    if len(tail) == 0:
        if head == '*':
            if isinstance(convertee, dict):
                for key, value in convertee.items():
                    convertee[key] = conversion(value)

            elif isinstance(convertee, list):
                for i, value in enumerate(convertee):
                    convertee[i] = conversion(value)

            else:
                raise TypeError("Can iterate only through dict or list, sorry.")
        else:
            convertee[head] = conversion(convertee[head])
    else:
        if head == '*':
            if isinstance(convertee, dict):
                for value in convertee.values():
                    _convert(value, tail, conversion)

            if isinstance(convertee, list):
                for value in convertee:
                    _convert(value, tail, conversion)
        else:
            _convert(convertee[head], tail, conversion)


class Location(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.npcs = set(self.npcs) if 'npcs' in self else set()

        for state in self.states.values():
            if isinstance(state.get('if', None), str):
                state['if'] = code(state['if'], eval)

            for option in state.get('options', []):
                if isinstance(option.get('does', None), str):
                    option['does'] = code(option['does'], exec)

                if isinstance(option.get('if', None), str):
                    option['if'] = code(option['if'], eval)


class Player(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.is_player = True
        self.does = False
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

        def dict_to_line(d):
            return (isinstance(d, dict)
                and ': '.join(tuple(d.items())[0])
                or d)

        convert(self, 'dialogue.*.lines.*', lambda x: ': '.join(tuple(x.items())[0]), dict)

        for piece in self.dialogue.values():
            # piece['lines'] = list(map(dict_to_line, piece['lines']))

            for option in piece.get('options', []):
                if isinstance(option.get('if', None), str):
                    option['if'] = code(option['if'], eval)

        if 'mind' in self:
            self.mind = (lambda mind:
                lambda self, world: mind(self, None, world)
            )(self.mind)


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


def load_from(path, ms):
    return (
        ms.create(**dict(yaml.safe_load(p.read_text(encoding='utf8'))))
        for p in Path(path).iterdir()
        if p.name.endswith(('.yaml', '.yml'))
    )


def load_assets(ms):
    world = ms.create(
        locations=Entity(**{
            location.name: location
            for location in load_from('assets/locations', ms)
        }),
        npcs=Entity(**{
            npc.name: npc for npc in load_from('assets/npc', ms)
        })
    )

    for _, location in world.locations:
        location.npcs = {world.npcs[name] for name in location.npcs}
        for npc in location.npcs:
            npc.location = location

    return world
