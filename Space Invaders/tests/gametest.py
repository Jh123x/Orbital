#Unit tests
import pygame
from time import sleep
from pygame.locals import *
import pygame.freetype
import unittest
import os, sys
#Import the main file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import read_settings
from classes.game import GameWindow, State,Direction,Bullet
#Keyboard pip module
#Relavant functions to be tested

#Test Classes
class MenuTest(unittest.TestCase):
    """
    Unit Test for the Game Class
    To test the user interface menu and ensure proper render of the UI
    """
    def setUp(self) -> None:
        """To be called before the testing for all the testcases"""
        super().setUp()
        config = {'sensitivity': 5, 'maxfps': 60, 'game_width': 600, 'game_height': 800, 'debug': True, 'icon_img_path': 'images/icon/icon.png'}
        settings = {'ship': 1, 'bg': 1, 'difficulty': 4}
        background_img_paths = ('images/backgrounds/Space.png',)
        enemy_img_paths = ('images/enemies/enemy.png', 'images/enemies/enemy2.png', 'images/enemies/enemy3.png', 'images/enemies/enemy4.png', 'images/enemies/mothership.png')
        bullet_img_paths = ('images/bullets/bullet.png',)
        player_img_paths = ('images/player/default.png', 'images/player/Spaceship.png', 'images/player/UFO.png')
        self.game = GameWindow(player_img_paths = player_img_paths, bullet_img_paths = bullet_img_paths, enemy_img_paths = enemy_img_paths, background_img_paths = background_img_paths, p_settings = settings, **config)
        

    def tearDown(self) -> None:
        """To be called after testing all the testcases"""
        self.game.__del__()

    def testMouseA(self) -> None:
        """
        Test mouse click on nothing
        """
        sleep(1)
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN,{"pos": (0,0),"button": 1})
        pygame.event.post(event)
        assert self.game.get_state()== State.MENU, "Mouse Click is activating a event when it should not be activating event at this coord"
    def testMouseB(self) -> None:
        """
        Test mouse click on exit
        """
        sleep(1)
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN,{"pos": (312,447),"button": 1})
        pygame.event.post(event)
        print(self.game.state)
        assert self.game.get_state()==State.QUIT, "Mouse Click is not activating a exit event it should be activating"
    def testMouseC(self)->None:
        """
        Test mouse click on play
        """
        sleep(1)
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN,{"pos": (288,400),"button": 1})
        pygame.event.post(event)
        print(self.game.state)
        assert self.game.get_state()==State.PLAY, "Mouse Click is activating a event it should not"
    def testKeyboard(self)-> None:
        """
        Test keyboard activation on main menu -> Not Implemented
        """
        assert 1==1
#Main function
if __name__ == "__main__":
    #Runs all of the tests defined above
    unittest.main()
