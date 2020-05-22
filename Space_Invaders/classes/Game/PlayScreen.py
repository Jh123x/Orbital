import pygame
import random
from pygame.locals import *

try: 
    from .Enums import State, Direction
    from .Player import Player
    from .EnemyGroup import EnemyShips
    from .EnemyShip import EnemyShip
    from .Colors import WHITE
    from .Screens import Screen
    from .Explosion import Explosion
    from .Bullet import Bullet
except ImportError:
    from Enums import State, Direction
    from Player import Player
    from EnemyGroup import EnemyShips
    from EnemyShip import EnemyShip
    from Colors import WHITE
    from Screens import Screen
    from Explosion import Explosion
    from Bullet import Bullet

class PlayScreen(Screen):
    def __init__(self, game_width:int, game_height:int, screen, sensitivity:int, max_fps:int, wave = 1, debug = False):
        """The Play screen"""

        #Call the superclass init
        super().__init__(game_width,game_height,State.PLAY,screen)

        #Store the variables
        self.debug = debug
        self.score = 0
        self.wave = wave - 1 
        self.sensitivity = sensitivity
        self.fps = max_fps

        #Create the groups
        #Bullets shot by player
        self.up_bullets = pygame.sprite.Group()

        #Bullet from Mobs
        self.down_bullets = pygame.sprite.Group()

        #Enemyships
        self.enemies = EnemyShips()

        #Explosions
        self.explosions = pygame.sprite.Group()

        #Create the player
        self.player = Player(sensitivity, game_width, game_height - 50, 3, max_fps, self.up_bullets, debug)

    def update_keypresses(self) -> None:
        """Update the map based on what the player has pressed"""
        #Check the keys the player has pressed
        keys = pygame.key.get_pressed()

        #If the player has click 'Left' or 'a' move the player to the left
        if keys[K_a] or keys[K_LEFT]: 
            self.player.move_left()

        #If the player has click 'right' or 'd' move the player to the right
        if keys[K_d] or keys[K_RIGHT]:
            self.player.move_right()

        #Move the player down
        if keys[K_s] or keys[K_DOWN]:
            self.player.move_down()
        
        #Move the player up
        if keys[K_w] or keys[K_UP]:
            self.player.move_up()

        #Check if the player pressed spacebar to spawn a bullet
        if keys[K_SPACE]:

            #Spawn a bullet
            self.player.shoot()

            #Set the bullet on cooldown
            self.bullet_cooldown = self.fps // (3 * 0.95 ** self.wave)

        #Check for debug keypresses
        if self.debug:

            #Deduct the life of the player
            if keys[K_q]:
                self.player.destroy()

    def spawn_enemy_bullets(self) -> None:
        """Spawns a bullet randomly for the enemy"""
        #Check if the enemy can shoot
        rand = random.randint(0,self.fps*50)
        if rand > self.fps:
            if self.debug:
                print(f"Random generated: {rand}")
            return

        #Get a random bullet for the entity to shoot
        if len(self.enemies):
            enemy = random.sample(set(self.enemies),1)
        else:
            enemy = None

        #If the set is non-empty
        if enemy:

            #Get the first element of the set
            enemy = enemy[0]

            #Create the bullet
            bullet2 = Bullet(self.sensitivity * 1.5, enemy.get_x() + enemy.get_width()//3, enemy.get_y(), Direction.DOWN, self.game_width, self.game_height, self.debug)

            #Rotate the bullet 180 degrees
            bullet2.rotate(180)

            #Add the bullet to the bullet group
            self.down_bullets.add(bullet2)

    def update_sprites(self) -> None:
        """Update the sprites"""

        #Update the player position
        self.player.update()

        #Update the enemy group
        self.enemies.update()

        #Update the explosions group
        self.explosions.update()

        #Spawn bullets for enemies
        self.spawn_enemy_bullets()

        #Update the bullets positions
        self.up_bullets.update()
        self.down_bullets.update()
        self.up_bullets.draw(self.screen)
        self.down_bullets.draw(self.screen)
        if self.debug:
            print(f"Number of player bullets: {len(self.up_bullets)}")

        #Draw the enemy
        self.enemies.draw(self.screen)
        if self.debug:
            print(f"Number of enemies: {len(self.enemies)}")

        #Draw the explosions
        self.explosions.draw(self.screen)

        #Draw player object
        self.screen.blit(self.player.image, self.player.rect)

    def get_score(self) -> int:
        """Gets the score of the player in the current state
            Arguments:
                No arguments
            Returns:
                Return an integer as a score
        """
        return self.score

    def reset(self) -> None:
        """Reset the play area"""
        #Zero the score and the wave
        self.score = 0
        self.wave = 0

        #Empty the sprite groups
        self.up_bullets.empty()
        self.down_bullets.empty()
        self.enemies.empty()
        self.explosions.empty()

        #Reset the player
        self.player.reset()

    def check_collisions(self) -> int:
        """Check the objects which collided"""
        #Check if player has collided with bullets
        bullet_collide = pygame.sprite.spritecollide(self.player, self.down_bullets, True)
        
        #If the set is not empty reduce player life
        if len(bullet_collide) > 0:

            #If it is in debug mode, print the event
            if self.debug:
                print("Player hit")

            #Destroy 1 of the player's life
            self.player.destroy()
            self.explosions.add(Explosion(self.player,self.fps//2,self.player.get_x(),self.player.get_y(),self.game_width,self.game_height))

        #Remove bullets that collide with one another
        pygame.sprite.groupcollide(self.up_bullets, self.down_bullets, True, True)

        #Get ships destroyed
        ships = list(pygame.sprite.groupcollide(self.up_bullets, self.enemies, True, False).values())

        if self.debug:
            print(ships)

        #If the list of collision is non-empty
        if ships:
            #Get the ship it collided with 
            ship = ships[0][0]

            #Destroy the first ship in the list
            ship.destroy()

            if self.debug:
                print(f"Ship destroyed")
        
            #Remove the ship from groupp if it has 0 lives
            if ship.is_destroyed():

                #Spawn an explosion in its place
                self.explosions.add(Explosion(0, self.fps//4, ship.get_x(), ship.get_y(), self.game_width, self.game_height, 0, self.debug))

                #Remove the ship from all groups
                ship.kill()

                #Remove sprites that collide with bullets and return the sum of all the scores
                return ship.get_points()

        #If nothing is destroyed return 0
        return 0


    def spawn_enemies(self, number:int) -> None:
        """Spawn enemies into the game"""
        #Adding sprites
        if number <= 6:
            self.enemies.add([EnemyShip(self.sensitivity, self.game_width//4 + i*self.game_width//10, self.game_height//10, random.randint(1,self.wave), self.game_width,  self.game_height, self.debug) for i in range(number)])
        else:
            for j in range(number//6 if number // 6 < 5 else 5):
                self.enemies.add([EnemyShip(self.sensitivity, self.game_width//4 + i*self.game_width//10, self.game_height//10 + EnemyShip.sprites[0].get_height() * j, random.randint(1,self.wave), self.game_width,  self.game_height, self.debug) for i in range(6)])

        
    def handle(self) -> State:
        #If player is destroyed, go to gameover state
        if self.player.is_destroyed():
            return State.GAMEOVER

        #Check if any of the enemies touched the bottom of the screen
        if [x for x in self.enemies if x.get_y() > self.game_height - self.player.get_height()]:

            #If it is debugging mode, print out what happened
            if self.debug:
                print("Alien hit the player")
                
            #If so it is gameover for the player
            return State.GAMEOVER

        #Spawn if there are no enemies 
        if not len(self.enemies):

            #Increase the wave number
            self.wave += 1

            #Spawn the aliens
            self.spawn_enemies(int(6 * self.wave))

        #Draw the score
        score = Screen.font.render(f"Score : {self.score}" , True, WHITE)
        self.screen.blit(score, (10, 10))

        #Draw the live count
        lives = Screen.font.render(f"Lives : {self.player.get_lives()}", True, WHITE)
        self.screen.blit(lives, (self.game_width - self.game_height//12,10))

        #Draw the wave number
        wave = Screen.font.render(f"Wave : {self.wave}", True, WHITE)
        self.screen.blit(wave, (self.game_width//2, 10))

        #Check object collisions
        self.score += self.check_collisions()

        #Check the player keypress
        self.update_keypresses()

        #Update the moving objs
        self.update_sprites()

        #Check if the player wants to pause
        if len(list(filter(lambda x: x.type == pygame.KEYDOWN and x.key == K_p, pygame.event.get()))):
            return State.PAUSE

        #Return play state
        return State.PLAY
