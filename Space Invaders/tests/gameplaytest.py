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
from classes.game import GameWindow, State, Direction, Bullet, Player, EnemyShip, EnemyShips
#Keyboard pip module

class BulletClassTest(unittest.TestCase):
    """Unit test for the bullets"""

    def setUp(self) -> None:
        """To be called before every test case to simulate bullet movements"""
        super().setUp()
        self.config = {'sensitivity': 5, 'maxfps': 60, 'game_width': 600, 'game_height': 800, 'debug': True, 'icon_img_path': 'images/icon/icon.png'}
        self.p_settings = {'ship': 1, 'bg': 1, 'difficulty': 4}
        self.background_img_paths = ('images/backgrounds/Space.png',)
        self.enemy_img_path = ('images/enemies/enemy.png', 'images/enemies/enemy2.png', 'images/enemies/enemy3.png', 'images/enemies/enemy4.png', 'images/enemies/mothership.png')
        self.bullet_img_path = ('images/bullets/bullet.png',)
        self.player_img_path = ('images/player/default.png', 'images/player/Spaceship.png', 'images/player/UFO.png')
        self.up_bullet = pygame.sprite.Group() #down bullet group
        self.down_bullet = pygame.sprite.Group() # up bullet group
        self.sensitivity = self.config["sensitivity"]
        self.game_width = self.config["game_width"]
        self.game_height = self.config["game_height"]
        self.delta = self.sensitivity*1.5#based on sensitivity, a tick implies movement of bullet by a constant delta
        self.screen = pygame.display.set_mode((self.game_height,self.game_width))
        Bullet.sprites.append(pygame.image.load(self.bullet_img_path[0]))
        for q in range(len(self.enemy_img_path)):
            EnemyShip.sprites.append(pygame.image.load(self.enemy_img_path[q]))
        for r in range(len(self.player_img_path)):
            Player.sprites.append(pygame.image.load(self.player_img_path[r]))

    def tearDown(self) -> None:
        """To be called after every test case"""
        pass
    def testSelfBulletDeletion(self) -> None:
        """
        Player Bullet Hits top bound of wall should disappear
        """
        bullet = Bullet(self.sensitivity*1.5,0,0,Direction.UP,self.game_width,self.game_height,True)
        self.down_bullet.add(bullet)
        bullet.update()
        bullet.update()#ticks 2 times at boundary to remove from sprite group
        #print(bullet in self.down_bullet)
        assert bullet not in self.down_bullet, "Enemy bullet not derendering properly"
    def testEnemyBulletDeletion(self) -> None:
        """
        Enemy Bullet hits bottom of Screen should disappear after calling update
        """
        bullet = Bullet(self.sensitivity*1.5,self.game_height,0,Direction.DOWN,self.game_width,self.game_height,True)
        self.down_bullet.add(bullet)
        bullet.update()
        bullet.update()#ticks 2 times at boundary to remove from sprite group
        #print(bullet in self.up_bullet)
        assert bullet not in self.up_bullet, "Player Bullet is not derendering at end of screen"
    def testMovementSelfBullet(self)-> None:
        """
        Own bullet should only move up, and bullet should also remain inside up bullet group
        """
        bullet = Bullet(self.sensitivity*1.5,300,200,Direction.UP,self.game_width,self.game_height,True)# coordinate initialised in middle so no collision 
        self.up_bullet.add(bullet)
        init_x = bullet.get_x()
        init_y = bullet.get_y()
        bullet.update()
        assert bullet in self.up_bullet
        assert bullet.get_y() == init_y-self.delta and bullet.get_x()==init_x
    def testMovementEnemyBullet(self)-> None:
        """
        Enemy Bullet should only move down, Bullet should remain inside down_group
        """
        bullet = Bullet(self.sensitivity*1.5,300,
                200,Direction.DOWN,self.game_width,self.game_height,True)# coordinate initialised in middle so no collision
        self.down_bullet.add(bullet)
        init_x = bullet.get_x()
        init_y = bullet.get_y()
        bullet.update()
        assert bullet in self.down_bullet , "Bullet not added to sprite group correctly"
        assert bullet.get_y() == init_y+self.delta and bullet.get_x()==init_x, "Bullet Movement not moving as expected"
    def testBulletOnBulletInteraction(self) -> None:
        """
        Player bullet Hits Enemy Bullet and should delete each other
        """
        bullet1 = Bullet(self.sensitivity*1.5,300,200-self.delta,Direction.DOWN,self.game_width,self.game_height,True)# coordinate initialised in middle so no collision
        bullet2 = Bullet(self.sensitivity*1.5,300,200+self.delta,Direction.UP,self.game_width,self.game_height,True)# coordinate initialised in middle so no collision
        self.down_bullet.add(bullet1)
        self.up_bullet.add(bullet2)
        bullet1.update()
        bullet2.update()
        pygame.sprite.groupcollide(self.up_bullet,self.down_bullet,True,True)
        assert len(self.down_bullet)==0 and len(self.up_bullet) == 0

    def testBulletOnPlayerInteraction(self) -> None:
        """
        Player Hit by enemy bullet should lose life or get destroyed
        """
        player = Player(self.p_settings['ship']-1,self.sensitivity,self.game_width,self.game_height,2,0,True)
        bullet1 = Bullet(self.sensitivity*1.5,300,
                800,Direction.DOWN,self.game_width,self.game_height,True)# coordinate initialised in middle so no collision
        bullet2 = Bullet(self.sensitivity*1.5,300,
                800-5*self.delta,Direction.DOWN,self.game_width,self.game_height,True)# coordinate initialised in middle so no collision
        self.down_bullet.add(bullet1)
        self.down_bullet.add(bullet2)
        detected = pygame.sprite.spritecollide(player, self.down_bullet, True)
        assert len(self.down_bullet) == 1, "Bullet Collision with Player does not remove Bullet"
        if detected:
            player.destroy() # Reduce Player Life by 1
        assert player.get_lives() == 1 , "Player life is not updated correctly"
        assert player.is_destroyed() == False , "Player is being destroyed before all lives are gone"
        bullet2.update()
        detected = pygame.sprite.spritecollide(player, self.down_bullet, True)
        if detected:
            player.destroy() # Reduce Player Life to 0 and cause player to be destroyed
        assert player.is_destroyed()==True, "Player is not being destroyed after all lives are gone"
    
    def testBulletOnEnemyInteraction(self) -> None:
        """
        Enemy Hit by Player Bullet should lose live or die.
        """
        bullet1 = Bullet(self.sensitivity*1.5,300,
                200,Direction.UP,self.game_width,self.game_height-50,True)# coordinate initialised in middle so no collision
        bullet2 = Bullet(self.sensitivity*1.5,300,
                200+4*self.delta,Direction.UP,self.game_width,self.game_height-50,True)# coordinate initialised in middle so no collision
        self.up_bullet.add(bullet1)
        self.up_bullet.add(bullet2)
        enemies = EnemyShips()
        enemy = EnemyShip(self.sensitivity,300,200,2,self.game_width,self.game_height,True)
        enemies.add(enemy)
        ships = list(pygame.sprite.groupcollide(self.up_bullet,enemies, True, False).values())
        if ships:
            ships[0][0].destroy()
        assert enemy.get_lives()==1, "Enemy Ship life is not being decreased"
        assert len(enemies) == 1, "Enemy is being removed from Sprite Group unexpectedly"
        bullet2.update()
        ships = list(pygame.sprite.groupcollide(self.up_bullet, enemies, True, False).values()) 
        if ships:
            ships[0][0].destroy()
        assert enemy.is_destroyed() == True, "Enemy Ship status is unexpectedly not 0"
if __name__ == "__main__":
    #Runs all of the tests defined above
    unittest.main()