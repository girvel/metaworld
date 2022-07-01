def decision_making(
    sapient: 'mind',
    world: 'npcs, locations',
    clock: 'current_time',
):
    while sapient.business is not None: yield
    yield from clock.wait(sapient.reaction_time)

    sapient.mind(sapient, world)