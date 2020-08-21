#Import all the screens
from .Screens import Screen
from .MenuTemplate import MenuTemplate
from .ClassicScreen import ClassicScreen
from .PlayScreen import PlayScreen
from .GameoverScreen import GameoverScreen
from .HighscoreScreen import HighscoreScreen
from .LocalPVPScreen import LocalPVPScreen
from .MenuScreen import MenuScreen
from .NewhighscoreScreen import NewhighscoreScreen
from .PauseScreen import PauseScreen
from .PlayModesScreen import PlayModeScreen
from .TwoPlayerGameover import TwoPlayerGameoverScreen
from .TwoPlayerPauseScreen import TwoPlayerPauseScreen
from .TwoPlayerScreen import TwoPlayerScreen
from .SettingsScreen import SettingsScreen
from .CoopScreen import CoopScreen
from .OnlinePVPScreen import OnlinePVPScreen
from .StoryModeScreen import StoryModeScreen
from .OnePlayerModesScreen import OnePlayerModeScreen
from .TutorialScreen import TutorialScreen
from .VictoryScreen import VictoryScreen
from .ResetScreen import ResetScreen

{'sf': 0, 'en_k': 0, 'el_k': 0, 'sl': 0, 'pu': 0, 'mpu': 0, 'ek_c': 0, 'ek_e': 0}


def accumulate_powerups(self):
    '''Abstraction of the handling of powerups in order to allow overriding in downstream classes'''
    self.tracker.powerups_used(1)
    self._powerup += 1

    def set_threshold(self) -> None:
        '''Get current threshold for applicable screens via querying database'''

        # Accumulator for number of powerups in single session and number of mobs killed
        self._powerup = 0
        self._killed = 0
        self.max_powerup= self.tracker.get_stat('mpu')
        self.max_kill = self.tracker.get_stat('ek_e')