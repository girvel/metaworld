def travel(npc, location):
    if npc.location is not None:
        npc.location.npcs.remove(npc)

    npc.location = location
    location.npcs.add(npc)
