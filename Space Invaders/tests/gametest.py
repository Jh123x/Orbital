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
        config = {'sensitivity' : 5,'maxfps' : 60,'game_width' : 600,'game_height' : 800,
                        'debug' : True, 'player_img_path' : 'images/player/player.png',
                        'enemy_img_path' : 'images/enemies/enemy.png','bullet_img_path' : 
                        'images/bullets/bullet.png','icon_img_path' : "images/icon/icon.png"}
        self.game = GameWindow(**config) 
        

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


class BulletClassTest(unittest.TestCase):
    """Unit test for the bullets"""

    def setUp(self) -> None:
        """To be called before every test case to simulate bullet movements"""
        super().setUp()
        config = {'sensitivity' : 5,'maxfps' : 60,'game_width' : 600,'game_height' : 800,
                        'debug' : True, 'player_img_path' : 'images/player/player.png',
                        'enemy_img_path' : 'images/enemies/enemy.png','bullet_img_path' : 
                        'images/bullets/bullet.png','icon_img_path' : "images/icon/icon.png"}
        self.bullet_img_path = config["bullet_img_path"]
        self.up_bullet = pygame.sprite.Group() #down bullet group
        self.down_bullet = pygame.sprite.Group() # up bullet group
        self.sensitivity = config["sensitivity"]
        self.game_width = config["game_width"]
        self.game_height = config["game_height"]
        self.delta = self.sensitivity*1.5#based on sensitivity, a tick implies movement of bullet by a constant delta
        self.screen = pygame.display.set_mode((self.game_height,self.game_width))

    def tearDown(self) -> None:
        """To be called after every test case"""
        pass
    
    def testSelfBulletDeletion(self) -> None:
        """
        Player Bullet Hits top bound of wall should disappear
        """
        bullet = Bullet(self.bullet_img_path,self.sensitivity*1.5,0,0,Direction.UP,self.game_width,self.game_height,True)
        self.down_bullet.add(bullet)
        bullet.update()
        bullet.update()#ticks 2 times at boundary to remove from sprite group
        #print(bullet in self.down_bullet)
        assert bullet not in self.down_bullet, "Enemy bullet not derendering properly"
    def testEnemyBulletDeletion(self) -> None:
        """
        Enemy Bullet hits bottom of Screen should disappear after calling update
        """
        bullet = Bullet(self.bullet_img_path,self.sensitivity*1.5,self.game_height,0,Direction.DOWN,self.game_width,self.game_height,True)
        self.down_bullet.add(bullet)
        bullet.update()
        bullet.update()#ticks 2 times at boundary to remove from sprite group
        #print(bullet in self.up_bullet)
        assert bullet not in self.up_bullet, "Player Bullet is not derendering at end of screen"
    def testMovementSelfBullet(self)-> None:
        """
        Own bullet should only move up, and bullet should also remain inside up bullet group
        """
        bullet = Bullet(self.bullet_img_path,self.sensitivity*1.5,300,200,Direction.UP,self.game_width,self.game_height,True)# coordinate initialised in middle so no collision 
        self.up_bullet.add(bullet)
        init_x = bullet.get_x()
        init_y = bullet.get_y()
        bullet.update() 
        print("\n self"+str(bullet.get_y()))
        print(init_y)
        assert bullet in self.up_bullet
        assert bullet.get_y() == init_y-self.delta and bullet.get_x()==init_x
    def testMovementEnemyBullet(self)-> None:
        """
        Enemy Bullet should only move down, Bullet should remain inside down_group
        """
        pygame.display.init()
        bullet = Bullet(self.bullet_img_path,self.sensitivity*1.5,300,
                200,Direction.DOWN,self.game_width,self.game_height,True)# coordinate initialised in middle so no collision
        self.down_bullet.add(bullet)
        init_x = bullet.get_x()
        init_y = bullet.get_y()
        bullet.update()
        print("\n enemy"+str(bullet.get_y()))
        print(init_y)
        assert bullet in self.down_bullet , "Bullet not added to sprite group correctly"
        assert bullet.get_y() == init_y+self.delta and bullet.get_x()==init_x, "Bullet Movement not moving as expected"
    def testC(self) -> None:
        """
        Player bullet Hits Enemy Alien
        TBC
        """
        assert 1==1

    def testD(self) -> None:
        """
        Player Hit by enemy bullet
        TBC
        """
        assert 1==1
#Main function
if __name__ == "__main__":
    #Runs all of the tests defined above
    unittest.main()
