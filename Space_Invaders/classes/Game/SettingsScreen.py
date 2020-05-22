try:
    from .Screens import Screen
    from .Enums import State
except ImportError:
    from Screens import Screen
    from Enums import State

class SettingsScreen(Screen):
    def __init__(self, game_width:int, game_height:int, screen):
        """Constructor for the settings menu class"""
        super().__init__(game_width, game_height, State.SETTINGS, screen)

        #Getting the current settings
        # self.load_current() #TODO