from collections import namedtuple
from pathlib import Path

import yaml

from lib.ecs.ecs import Metasystem, Entity, create_system


# Concept:
# systems/ contains all the systems
# assets/ contains all the game's content
# toolkit/ contains all the additional code used outside the systems
# lib/ contains all the external libraries
# metaworld.py is the entrypoint

# TODO:
# - unify option mechanics
# - write illia pots's house
# - make house states a dict as a npc's dialogues
# - assert that names never match
# - unify memory for npc and locations?
# pro: unification
# con: the locations' description are more temporal and normally repetitive
# - a book in the pub

class Action:
    stands_at = namedtuple("stands_at", "location")
    talks_to = namedtuple("talks_to", "npc about")


class Ui:
    @staticmethod
    def choose(options):
        for i, option in enumerate(options):
            print(f'{i + 1}. {option["line"]}')

        while True:
            try:
                return options[int(input("> ")) - 1]
            except ValueError:
                pass
            except IndexError:
                pass

    @staticmethod
    def play_lines(lines):
        for line in lines:
            print(line, end='')
            if not __debug__:
                input()
            else:
                print()

    @staticmethod
    def describe_interior(states):
        for _, state in states.items():
            if 'line' in state:
                print(state['line'])
                print()

    @staticmethod
    def finish_the_game():
        input("The end!")
        exit()


if __name__ == '__main__':
    ms = Metasystem()

    def travel(npc, location):
        npc.does = Action.stands_at(location)
        npc.location = location.name
        location.npcs.add(npc.name)

    @ms.create_system
    def travel_system(traveler: 'does'):
        # TODO entity field update mechanics

        match traveler.does:
            case Action.stands_at(location):
                travel(traveler, location)

    @ms.create_system
    def action_system(world: 'npcs, locations', actor: 'is_player'):
        def load_script(expression, self, f=eval):
            return f(expression, {}, {
                'locations': world.locations,
                'npc': world.npcs,
                'Action': Action,
                'mc': actor,
                'self': self,
            })

        match actor.does:
            case Action.talks_to(npc, about):
                dialogue = npc.dialogue['conversations'][about]

                Ui.play_lines(dialogue['lines'])
                actor.memory.add(f'{npc.name}.{about}')

                if not 'options' in dialogue:
                    actor.does = Action.stands_at(world.locations[actor.location])
                    return

                chosen_option = Ui.choose(dialogue['options'])
                if 'goto' in chosen_option:
                    actor.does = Action.talks_to(npc, chosen_option['goto'])
                else:
                    actor.does = load_script(chosen_option['does'], npc)

                if 'action' in chosen_option:
                    load_script(chosen_option['action'], npc, exec)

            case Action.stands_at(location):
                current_states = {
                    name: state for name, state in location['states'].items()
                    if 'if' not in state or load_script(state['if'], location)
                }

                Ui.describe_interior(current_states)

                for name in current_states:
                    actor.memory.add('.'.join([location.name, name]))

                options = [
                    option
                    for state in current_states.values()
                    for option in state.get('options', [])
                    if ('if' not in option or load_script(option['if'], location))
                ]

                actor.does = load_script(Ui.choose(options)['does'], location)

            case _:
                assert False

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

    def load_from(path):
        return (
            ms.create(**dict(yaml.safe_load(p.read_text(encoding='utf8'))))
            for p in Path(path).iterdir()
            if p.name.endswith(('.yaml', '.yml'))
        )

    world = ms.create(
        locations=Entity(**{
            location.name: location for location in load_from('assets/locations')
        }),
        npcs=Entity(**{
            npc.name: npc for npc in load_from('assets/npc')
        })
    )

    npc_name = None
    location = None
    for _, location in world.locations:
        for npc_name in location.npcs:
            travel(world.npcs[npc_name], location)

    del npc_name, location, world

    try:
        while True:
            ms.update()
    except KeyboardInterrupt:
        if not __debug__:
            Ui.finish_the_game()
