from datetime import timedelta


def travel(traveler: 'will_go_to', clock: 'current_time, wait'):
    traveler.business = 'traveling'
    yield from clock.wait(timedelta(seconds=30))

    traveler.business = None

    if traveler.location is not None:
        traveler.location.npcs.remove(traveler)

    traveler.location = traveler.will_go_to
    traveler.location.npcs.add(traveler)

    del traveler.will_go_to