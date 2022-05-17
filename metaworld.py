from common import Action, travel
from lib.ecs.ecs import Metasystem, Entity, create_system


# Concept:
# systems/ contains all the systems
# assets/ contains all the game's content
# toolkit/ contains all the additional code used outside the systems
# lib/ contains all the external libraries
# metaworld.py is the entrypoint

# TODO:
# - unify option mechanics
# - write illia pots's house
# - make house states a dict as a npc's dialogues
# - assert that names never match
# - a book in the pub


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
    def describe_interior(states):
        for _, state in states.items():
            if 'line' in state:
                print(state['line'])
                print()

    @staticmethod
    def finish_the_game():
        input("The end!")
        exit()


if __name__ == '__main__':
    ms = Metasystem()

    @ms.create_system
    def travel_system(traveler: 'does'):
        # TODO entity field update mechanics

        match traveler.does:
            case Action.stands_at(location):
                travel(traveler, location)

    @ms.create_system
    def action_system(world: 'npcs, locations', actor: 'is_player'):
        def load_script(expression, self, f=eval):
            return f(expression, {}, {
                'locations': world.locations,
                'npc': world.npcs,
                'Action': Action,
                'mc': actor,
                'self': self,
            })

        match actor.does:
            case Action.talks_to(npc, about):
                dialogue = npc.dialogue[about]

                Ui.play_lines(dialogue['lines'])
                actor.memory.add(f'{npc.name}.{about}')

                if not 'options' in dialogue:
                    actor.does = Action.stands_at(world.locations[actor.location])
                    return

                chosen_option = Ui.choose(dialogue['options'])
                if 'goto' in chosen_option:
                    actor.does = Action.talks_to(npc, chosen_option['goto'])
                else:
                    actor.does = load_script(chosen_option['does'], npc)

                if 'action' in chosen_option:
                    load_script(chosen_option['action'], npc, exec)

            case Action.stands_at(location):
                current_states = {
                    name: state for name, state in location['states'].items()
                    if 'if' not in state or load_script(state['if'], location)
                }

                Ui.describe_interior(current_states)

                for name in current_states:
                    actor.memory.add('.'.join([location.name, name]))

                options = [
                    option
                    for state in current_states.values()
                    for option in state.get('options', [])
                    if ('if' not in option or load_script(option['if'], location))
                ]

                actor.does = load_script(Ui.choose(options)['does'], location)

            case _:
                assert False

    try:
        while True:
            ms.update()
    except KeyboardInterrupt:
        if not __debug__:
            Ui.finish_the_game()
