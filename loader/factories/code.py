def code(source, kind):
    def freezed_script(self, player, world):
        return kind(source, {}, {
            'locations': world.locations,
            'npcs': world.npcs,
            'self': self,
            'player': player,
        })

    return freezed_script


def condition(x):
    return code(x, eval)


def script(x):
    return code(x, exec)
