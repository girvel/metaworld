from datetime import timedelta

import common
import ui


list = []


@list.append
def travel(traveler: 'will_go_to', clock: 'current_time'):
    traveler.business = 'traveling'
    destination = traveler.will_go_to
    yield from common.wait(clock, timedelta(seconds=30))

    traveler.business = None
    common.travel(traveler, destination)
    del traveler.will_go_to


@list.append
def speech(
    talker: 'will_talk_to',
    world: 'npcs, locations',
    clock: 'current_time'
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

    while True:
        dialogue = npc.dialogue[about]
        context = {
            'player': talker,
            'self': npc,
            'world': world,
        }
        ui.play_lines(dialogue['lines'], context)

        talker.memory.add(f'{npc.name}.{about}')

        if 'options' not in dialogue:
            break

        about = ui.choose([
            o for o in dialogue['options']
            if 'if' not in o or o['if'](**context)
        ])['goto']


@list.append
def decision_making(sapient: 'mind', world: 'npcs, locations'):
    while sapient.business is not None: yield

    sapient.mind(sapient, world)
    pass


@list.append
def time(clock: 'current_time'):
    clock.current_time += timedelta(seconds=1)
