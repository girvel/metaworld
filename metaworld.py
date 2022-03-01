from collections import namedtuple
from pathlib import Path

import yaml

from lib.ecs.ecs import Metasystem, Entity, create_system


class Action:
    stands_at = namedtuple("stands_at", "place")
    talks_to = namedtuple("talks_to", "person")


Memory = namedtuple("Memory", "places dialogues")


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
                travel(person, place)

    @ms.add
    @create_system
    def action_system(world: 'people, places', actor: 'is_player'):
        def evaluate_does(expression):
            return eval(expression, {}, {
                'places': world.places,
                'people': world.people,
                'Action': Action,
            })

        match actor.does:
            case Action.talks_to(person):
                if 'conversation' in person:
                    dialogue \
                        = person.dialogue['conversations'][person.conversation]
                else:
                    dialogue = next(
                        person.dialogue['conversations'][entrypoint]
                        for entrypoint in person.dialogue['entrypoints']
                    )

                Ui.play_lines(dialogue['lines'])

                if not 'options' in dialogue:
                    actor.does = Action.stands_at(world.places[actor.place])
                    return

                chosen_option = Ui.choose(dialogue['options'])
                if 'goto' in chosen_option:
                    person.conversation = chosen_option['goto']
                else:
                    actor.does = evaluate_does(chosen_option['does'])

            case Action.stands_at(place):
                Ui.describe_interior(place)

                options = [
                    option
                    for state in place['states']
                    for option in state.get('options', [])
                ]

                actor.does = evaluate_does(Ui.choose(options)['does'])

            case _:
                assert False


    # Concept:
    # systems/ contains all the systems
    # assets/ contains all the game's content
    # toolkit/ contains all the additional code used outside the systems
    # lib/ contains all the external libraries
    # metaworld.py is the entrypoint

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

    try:
        while True:
            ms.update()
    except KeyboardInterrupt:
        if not __debug__:
            Ui.finish_the_game()
