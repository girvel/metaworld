from datetime import timedelta

import ui


def speech(
    talker: 'will_talk_to',
    world: 'npcs, locations',
    clock: 'current_time, wait',
):
    while talker.business is not None: yield
    yield from clock.wait(timedelta(seconds=5))

    npc = talker.will_talk_to
    del talker.will_talk_to

    assert talker.location == npc.location, "Distant speech is forbidden"

    if 'will_talk_about' in talker:
        about = talker.will_talk_about
        del talker.will_talk_about
    else:
        about = 'initial'

    amount_of_lines = 0
    while True:
        dialogue = npc.dialogue[about]
        context = {
            'player': talker,
            'self': npc,
            'world': world,
        }
        ui.play_lines(dialogue['lines'], context)
        amount_of_lines += len(dialogue['lines'])

        talker.memory.add(f'{npc.name}.{about}')

        if 'options' not in dialogue:
            break

        about = ui.choose([
            o for o in dialogue['options']
            if 'if' not in o or o['if'](**context)
        ])['goto']

    yield from clock.wait(timedelta(seconds=30 * amount_of_lines))
