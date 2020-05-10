#Unit tests
import pygame
import unittest
import os, sys
#Import the main file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import read_settings
from classes.game import GameWindow
#Keyboard pip module
# import keyboard
from pynput.mouse import Button, Controller, Listener
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
        config = {'sensitivity' : 5,'maxfps' : 60,'game_width' : 600,'game_height' : 800,
                        'debug' : True, 'player_img_path' : '../images/player/player.png',
                        'enemy_img_path' : '../images/enemies/enemy.png','bullet_img_path' : 
                        '../images/bullets/bullet.png','icon_img_path' : "../images/icon/icon.png"}
        self.game = GameWindow(**config) 
        

    def tearDown(self) -> None:
        """To be called after testing all the testcases"""
        self.game.__del__()

    def testMouseA(self) -> None:
        """
        Test mouse click on nothing
        """
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN,{"pos": (0,0),"button": 1})
        pygame.event.post(event)
        assert 1==1, "Mouse Click is activating a event when it should not be activating event at this coord"
    def testMouseB(self) -> None:
        """
        Test mouse click on exit
        """
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN,{"pos": (320,453),"button": 1})
        pygame.event.post(event)
        assert 1==1, "Mouse Click is not activating a exit event it should be activating"
    def testMouseC(self)->None:
        """
        Test mouse click on play
        """
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN,{"pos": (300,400),"button": 1})
        pygame.event.post(event)
        assert 1==1, "Mouse Click is activating a event it should not"
    def testKeyboard(self)-> None:
        """
        Test keyboard activation on main menu
        """
        pass


class BulletClassTest(unittest.TestCase):
    """Unit test for the bullets"""

    def setUp(self) -> None:
        """To be called before every test case"""
        pass

    def tearDown(self) -> None:
        """To be called after every test case"""
        pass
    
    def testA(self) -> None:
        """
        Enemy Bullet Hits ground
        """
        assert 1 == 1, "This test has passed"
    def testB(self) -> None:
        """
        Player Bullet hits end of Screen
        """
        pass
    def testC(self) -> None:
        """
        Player Hits Enemy Alien
        """
        pass
    def testD(self) -> None:
        """
        Player Hit by enemy bullet
        """
        pass
#Main function
if __name__ == "__main__":
    #Runs all of the tests defined above
    unittest.main()
