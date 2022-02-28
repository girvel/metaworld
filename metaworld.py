from collections import namedtuple
from pathlib import Path

import yaml

from lib.ecs.ecs import Metasystem, Entity, create_system


class Action:
    stands_at = namedtuple("stands", "place")
    talks_to = namedtuple("talks", "person")


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

    @staticmethod
    def play_lines(lines):
        for line in lines:
            print(line, end='')
            input()

    @staticmethod
    def describe_interior(interior):
        for state in interior['states']:
            print(state['line'])

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
                dialogue = person.lines[person.lines_state]

                Ui.play_lines(dialogue['lines'])

                if not 'options' in dialogue:
                    Ui.finish_the_game()

                person.lines_state = Ui.choose(dialogue['options'])['goto']

            case Action.stands_at(place):
                Ui.describe_interior(place.interior)

                options = [
                    option
                    for state in place.interior['states']
                    for option in state.get('options', [])
                ]

                name, state = Ui.choose(options)['goto'].split('.')
                person = next(
                    p for p in place.persons if p.name.lower() == name.lower()
                )

                actor.does = Action.talks_to(person)
                person.state = state


    brian = ms.add(Entity(
        name='Brian',
        lines=yaml.safe_load(
            Path('assets/characters/brian.yaml').read_text(encoding='utf8')
        ),
        lines_state='initial',
    ))

    pub = ms.add(Entity(
        name='The pub',
        interior=yaml.safe_load(
            Path('assets/places/pub.yaml').read_text(encoding='utf8')
        ),
        persons=[brian],
    ))

    you = ms.add(Entity(
        name='Officer Aernerh',
        is_player='True',
        does=Action.stands_at(pub),
        talks_to=brian,
    ))

    while True:
        ms.update()
