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

    @ms.add
    @create_system
    def action_system(actor: 'does'):
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
                    actor.does = Action.stands_at(places[actor.place])
                    return

                chosen_option = Ui.choose(dialogue['options'])
                if 'goto' in chosen_option:
                    person.conversation = chosen_option['goto']
                else:
                    does_generator = chosen_option['does']

                    actor.does = eval(
                        does_generator,
                        {},
                        {'places': places, 'people': people, 'Action': Action}
                    )

            case Action.stands_at(place):
                Ui.describe_interior(place.interior)

                options = [
                    option
                    for state in place.interior['states']
                    for option in state.get('options', [])
                ]

                does_generator = Ui.choose(options)['does']

                actor.does = eval(
                    does_generator,
                    {},
                    {'places': places, 'people': people, 'Action': Action}
                )

            case _:
                assert False


    @ms.add
    @create_system
    def travel(traveler: 'does'):
        # TODO entity field update mechanics

        match traveler.does:
            case Action.stands_at(place):
                traveler.place = place.name
                place.people.add(traveler.name)


    # Concept:
    # systems/ contains all the systems
    # assets/ contains all the game's content
    # toolkit/ contains all the additional code used between the systems
    # lib/ contains all the external libraries
    # metaworld.py is the entrypoint

    places = ms.add(Entity())
    people = ms.add(Entity())

    people['Brian'] = ms.add(Entity(
        name='Brian',
        dialogue=yaml.safe_load(
            Path('assets/characters/brian.yaml').read_text(encoding='utf8')
        )['dialogue'],
        place='Pub',
    ))

    places['Pub'] = ms.add(Entity(
        name='The pub',
        interior=yaml.safe_load(
            Path('assets/places/pub.yaml').read_text(encoding='utf8'),
        ),
        people={'Brian', 'Officer Aernerh'},
    ))

    places['Central street'] = ms.add(Entity(
        name='Central street',
        interior=yaml.safe_load(
            Path('assets/places/central_street.yaml').read_text(encoding='utf8')
        ),
        people=set(),
    ))

    people['Officer Aernerh'] = ms.add(Entity(
        name='Officer Aernerh',
        is_player='True',
        does=Action.stands_at(places['Pub']),
        memory=Memory(set(), set()),
        place='Pub',
    ))

    while True:
        ms.update()
