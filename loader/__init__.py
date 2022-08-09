from datetime import timedelta
from pathlib import Path
from typing import Union

import yaml
import re

import ui
from lib.ecs.ecs import OwnedEntity, Entity
from loader import factories


for factory in factories.__all__:
    tag = f"!{factory.__name__}"
    loader = (lambda factory_:
        lambda loader, node: (factory_.__name__.islower()
            and factory_(loader.construct_scalar(node))
            or factory_(**loader.construct_mapping(node, True))
        )
    )(factory)

    yaml.SafeLoader.add_constructor(tag, loader)

    if hasattr(factory, 'implicit_resolver'):
        yaml.SafeLoader.add_implicit_resolver(
            tag, re.compile(factory.implicit_resolver), None,
        )

def load(path, ms):
    path = Path(path)
    assert path.exists()

    if path.is_dir():
        return Entity(**{
            entity['name', file_name]: entity
            for file_name, entity in (
                (p.stem, load(p, ms))
                for p in path.iterdir()
                if p.suffix in ('.yaml', '.yml') or p.is_dir()
            )
        })
    elif path.suffix in ('.yaml', '.yml'):
        result = ms.add(
            yaml.safe_load(path.read_text(encoding='utf8')),
        )
    else:
    
        result = ms.create(content=path.read_text(encoding='utf8'))

    result.name = path.stem
    return result


def load_assets(ms):
    world = ms.add(load('assets', ms))

    for _, npc in world.npcs:
        location = world.locations[npc.location]
        location.npcs.add(npc)
        npc.location = location

    return world
