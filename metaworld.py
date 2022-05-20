import loader
import ui
from lib.ecs.ecs import Metasystem
import systems


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


if __name__ == '__main__':
    ms = Metasystem()

    for system in systems.list:
        ms.create_system(system)

    loader.load_assets(ms)

    try:
        while True:
            ms.update()
    except KeyboardInterrupt:
        if not __debug__:
            ui.finish_the_game()
