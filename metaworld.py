import loader
import ui
from lib.ecs.ecs import Metasystem, create_system
import systems


if __name__ == '__main__':
    ms = Metasystem()

    for system in systems.order:
        ms.add(create_system(system))

    loader.load_assets(ms)

    try:
        while True:
            ms.update()
    except KeyboardInterrupt:
        if not __debug__:
            ui.finish_the_game()
