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


class Action:
    stands_at = namedtuple("stands_at", "place")
    talks_to = namedtuple("talks_to", "person about")


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
    def describe_interior(interior):
        for state in interior['states']:
            if 'line' in state:
                print(state['line'])
                print()

    @staticmethod
    def finish_the_game():
        input("The end!")
        exit()


if __name__ == '__main__':
    ms = Metasystem()

    def travel(person, place):
        person.does = Action.stands_at(place)
        person.place = place.name
        place.people.add(person.name)

    @ms.add
    @create_system
    def travel_system(traveler: 'does'):
        # TODO entity field update mechanics

        match traveler.does:
            case Action.stands_at(place):
                travel(traveler, place)

    @ms.add
    @create_system
    def action_system(world: 'people, places', actor: 'is_player'):
        def load_script(expression, self, f=eval):
            return f(expression, {}, {
                'places': world.places,
                'people': world.people,
                'Action': Action,
                'mc': world.people['Officer Aernerh'],
                'self': self,
            })

        match actor.does:
            case Action.talks_to(person, about):
                dialogue = person.dialogue['conversations'][about]

                Ui.play_lines(dialogue['lines'])
                actor.memory['dialogues'].add(f'{person.name}.{about}')

                if not 'options' in dialogue:
                    actor.does = Action.stands_at(world.places[actor.place])
                    print(actor.does)
                    return

                chosen_option = Ui.choose(dialogue['options'])
                if 'goto' in chosen_option:
                    actor.does = Action.talks_to(person, chosen_option['goto'])
                else:
                    actor.does = load_script(chosen_option['does'], person)

                if 'action' in chosen_option:
                    load_script(chosen_option['action'], person, exec)

            case Action.stands_at(place):
                Ui.describe_interior(place)

                options = [
                    option
                    for state in place['states']
                    for option in state.get('options', [])
                    if ('if' not in option or load_script(option['if'], place))
                    and ('if' not in state or load_script(state['if'], place))
                ]

                actor.does = load_script(Ui.choose(options)['does'], place)

            case _:
                assert False

    def load_from(path):
        return (
            ms.add(Entity(**yaml.safe_load(p.read_text(encoding='utf8'))))
            for p in Path(path).iterdir()
            if p.name.endswith(('.yaml', '.yml'))
        )

    world = ms.add(Entity(
        places={
            place.name: place for place in load_from('assets/places')
        },
        people={
            person.name: person for person in load_from('assets/people')
        }
    ))

    for place in world.places.values():
        for person in place.people:
            travel(world.people[person], place)

    del person, place, world

    try:
        while True:
            ms.update()
    except KeyboardInterrupt:
        if not __debug__:
            Ui.finish_the_game()
