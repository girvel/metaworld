import ui
from lib.ecs.ecs import OwnedEntity


class Player(OwnedEntity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.is_player = True
        self.memory = set()
        self.business = None

    @staticmethod
    def mind(self, world):
        if 'will_talk_to' in self:
            return

        current_states = {
            name: state for name, state in self.location.states.items()
            if 'if' not in state or state['if'](self.location, self, world)
        }

        ui.describe_interior(current_states)

        for state_name in current_states:
            self.memory.add(f'{self.location.name}.{state_name}')

        options = [
            option
            for state in current_states.values()
            for option in state.get('options', [])
            if 'if' not in option or option['if'](self.location, self, world)
        ]

        ui.choose(options, skip=(True, {'does': lambda *_: None}))['does'](self.location, self, world)

    def talk_to(self, target, about):
        self.will_talk_to = target
        self.will_talk_about = about