from collections import namedtuple
from pathlib import Path

import yaml

from lib.ecs.ecs import Metasystem, Entity, create_system


class Action:
    stands_at = namedtuple("stands", "place")
    talks_to = namedtuple("talks", "person")


if __name__ == '__main__':
    ms = Metasystem()

    @ms.add
    @create_system
    def action_system(actor: 'does'):
        match actor.does:
            case Action.talks_to(person):
                dialogue = person.lines[person.lines_state]

                for line in dialogue['lines']:
                    print(line, end='')
                    input()

                if not 'options' in dialogue:
                    input("The end!")
                    exit()

                for i, option in enumerate(dialogue['options']):
                    print(f'{i + 1}. {option["line"]}')

                person.lines_state \
                    = dialogue['options'][int(input("> ")) - 1]['goto']

            case Action.stands_at(place):
                for state in place.interior['states']:
                    print(state['line'])

                options = [
                    option
                    for state in place.interior['states']
                    for option in state.get('options', [])
                ]

                for i, option in enumerate(options):
                    print(f'{i + 1}. {option["line"]}')

                name, state = options[int(input("> ")) - 1]['goto'].split('.')
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
