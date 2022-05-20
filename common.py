from collections import namedtuple


class Action:
    stands_at = namedtuple("stands_at", "location")
    talks_to = namedtuple("talks_to", "npc about")


def travel(npc, location):
    if npc.location is not None:
        npc.location.npcs.remove(npc)

    npc.location = location
    location.npcs.add(npc)
