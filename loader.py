from pathlib import Path

import yaml

from common import travel
from lib.ecs.ecs import Entity


class Location(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.npcs = set(self.npcs) if 'npcs' in self else set()


class Player(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.is_player = True
        self.does = False
        self.memory = set()


for tag in [Location, Player]:
    yaml.SafeLoader.add_constructor(
        '!' + tag.__name__.lower(),
        (lambda tag_:
            lambda loader, node:
                tag_(**loader.construct_mapping(node, True))
        )(tag)
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
            location.name: location for location in load_from('assets/locations')
        }),
        npcs=Entity(**{
            npc.name: npc for npc in load_from('assets/npc')
        })
    )

    for _, location in world.locations:
        for npc_name in location.npcs:
            travel(world.npcs[npc_name], location)

    return world
