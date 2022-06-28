from datetime import timedelta

import common
import ui


def travel(traveler: 'will_go_to'):
    common.travel(traveler, traveler.will_go_to)
    del traveler.will_go_to


def speech(talker: 'will_talk_to', world: 'npcs, locations'):
    npc = talker.will_talk_to
    del talker.will_talk_to

    # assert talker.location == npc.location, "Distant speech is forbidden"
    # TODO fix on continuity milestone

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


def decision_making(sapient: 'mind', world: 'npcs, locations'):
    sapient.mind(sapient, world)


def time(clock: 'current_time'):
    clock.current_time += timedelta(seconds=1)


list = [travel, speech, decision_making, time]
