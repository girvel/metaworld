import common
import ui


def travel(traveler: 'will_go_to'):
    common.travel(traveler, traveler.will_go_to)
    del traveler.will_go_to


def speech(talker: 'will_talk_to', world: 'npcs, locations'):
    npc = talker.will_talk_to
    del talker.will_talk_to

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


def decision_making(player: 'is_player', world: 'npcs, locations'):
    if 'will_talk_to' in player:
        return

    current_states = {
        name: state for name, state in player.location.states.items()
        if 'if' not in state or state['if'](player.location, player, world)
    }

    ui.describe_interior(current_states)

    for state_name in current_states:
        player.memory.add(f'{player.location.name}.{state_name}')

    options = [
        option
        for state in current_states.values()
        for option in state.get('options', [])
        if ('if' not in option or option['if'](player.location, player, world))
    ]

    ui.choose(options)['does'](player.location, player, world)


list = [travel, speech, decision_making]
