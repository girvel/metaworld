from lib.ecs.ecs import OwnedEntity


class Clock(OwnedEntity):
    def wait(self, delta):
        starting_time = self.current_time
        while (self.current_time - starting_time) < delta:
            yield