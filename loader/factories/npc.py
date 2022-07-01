from lib.ecs.ecs import OwnedEntity
from loader.converter import convert
from loader.factories.code import condition, script


class Npc(OwnedEntity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.business = None

        unpack_dict = lambda d: tuple(d.items())[0]
        convert(self, 'dialogue.*.lines.*', lambda x: ': '.join(unpack_dict(x)), dict)
        convert(self, 'dialogue.*.options.*.if', condition, str)
        convert(self, 'mind', script, str)
        convert(self, 'mind', lambda m: lambda self, world: m(self, None, world))