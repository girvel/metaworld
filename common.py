def travel(npc, location):
    if npc.location is not None:
        npc.location.npcs.remove(npc)

    npc.location = location
    location.npcs.add(npc)


def wait(clock, delta):
    starting_time = clock.current_time
    while (clock.current_time - starting_time) < delta:
        yield
