from datetime import timedelta

import common
import ui


list = []


@list.append
def travel(traveler: 'will_go_to', clock: 'current_time'):
    traveler.business = 'traveling'
    yield from common.wait(clock, timedelta(seconds=30))

    traveler.business = None
    common.travel(traveler, traveler.will_go_to)
    del traveler.will_go_to


@list.append
def speech(
    talker: 'will_talk_to',
    world: 'npcs, locations',
    clock: 'current_time',
):
    while talker.business is not None: yield
    yield from common.wait(clock, timedelta(seconds=5))

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

    yield from common.wait(clock, timedelta(seconds=30 * amount_of_lines))


@list.append
def decision_making(
    sapient: 'mind',
    world: 'npcs, locations',
    clock: 'current_time',
):
    while sapient.business is not None: yield
    yield from common.wait(clock, timedelta(seconds=5))

    sapient.mind(sapient, world)


@list.append
def time(clock: 'current_time'):
    clock.current_time += timedelta(seconds=1)
