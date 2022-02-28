from pathlib import Path

import yaml

from lib.ecs.ecs import Metasystem, Entity, create_system


if __name__ == '__main__':
    ms = Metasystem()

    @ms.add
    @create_system
    def input_system(talker: 'talks_to'):
        dialogue = talker.talks_to.lines[talker.talks_to.lines_state]

        for line in dialogue['lines']:
            print(line, end='')
            input()

        if not 'options' in dialogue:
            input("The end!")
            exit()

        for i, option in enumerate(dialogue['options']):
            print(f'{i + 1}. {option["line"]}')

        talker.talks_to.lines_state \
            = dialogue['options'][int(input("> ")) - 1]['goto']

    brian = ms.add(Entity(
        name='Brian',
        lines=yaml.safe_load(
            Path('assets/dialogues/brian.yaml').read_text(encoding='utf8')
        ),
        lines_state='initial',
    ))

    you = ms.add(Entity(
        name='Officer Aernerh',
        is_player='True',
        talks_to=brian,
    ))

    while True:
        ms.update()
