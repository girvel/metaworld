from lib.ecs.ecs import OwnedEntity
from loader.converter import convert
from loader.factories.code import condition, script


class Location(OwnedEntity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.npcs = set()

        convert(self, 'states.*.if', condition, str)
        convert(self, 'states.*.options.*.does', script, str)
        convert(self, 'states.*.options.*.if', condition, str)