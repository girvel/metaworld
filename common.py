from collections import namedtuple


class Action:
    stands_at = namedtuple("stands_at", "location")
    talks_to = namedtuple("talks_to", "npc about")


def travel(npc, location):
    npc.does = Action.stands_at(location)
    npc.location = location.name
    location.npcs.add(npc.name)
