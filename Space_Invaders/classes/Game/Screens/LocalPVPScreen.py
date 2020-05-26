import pygame
import random
from pygame.locals import *
from . import Screen
from .. import State, EnemyShips, Player, Direction, EnemyShip, WHITE, Explosion, Bullet

class LocalPVPScreen(Screen):
    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, fps:int, player_lives:int = 3, debug:bool = False):
        """Constructor for local PVP class"""

        #Call the super class Screen object
        super().__init__(screen_width, screen_height, State.PVP, screen, 0, 0, debug)

        #Store other variables
        self.sensitivity = sensitivity
        self.fps = fps
        self.player_lives = player_lives
        self.resetted = False

        #Bullet groups
        self.player1_bullet = pygame.sprite.Group()
        self.player2_bullet = pygame.sprite.Group()
        self.mob_bullet = pygame.sprite.Group()

        #Create explosions grp
        self.explosions = pygame.sprite.Group()

        #Enemyships
        self.enemies = EnemyShips(self.state)

        #Get wave
        self.wave = 0

        #Init scores
        self.p1_score = 0
        self.p2_score = 0
    
        #Call the players
        self.player1 = Player(sensitivity, screen_width, screen_height, screen_width//2, 50, player_lives, fps, self.player1_bullet, Direction.DOWN, debug)
        self.player2 = Player(sensitivity, screen_width, screen_height, screen_width//2, screen_height-50, player_lives, fps, self.player2_bullet, Direction.UP, debug)
        
    def reset(self) -> None:
        """Reset the environment"""
        if self.resetted:
            return

        #Reset score
        self.p1_score = 0
        self.p2_score = 0

        #Reset player model
        self.player1.reset()
        self.player2.reset()

        #Empty groups
        self.explosions.empty()
        self.player1_bullet.empty()
        self.player2_bullet.empty()

        self.resetted = True

    def check_keypresses(self) -> bool:
        """Check the keys which are pressed"""
        #Get all the number of keys
        keys = pygame.key.get_pressed()

        #Check if they want to pause game
        if keys[K_p]:
            return True

        if not self.player1.is_destroyed():
            #Check player 1 keys
            if keys[K_a]:

                #Move player 1 to the left
                self.player1.move_left()

            if keys[K_d]:
                
                #Move player 1 to the right
                self.player1.move_right()

            if keys[K_SPACE]:

                #Let the player shoot
                self.player1.shoot()

        #If player 2 is not destroyed
        if not self.player2.is_destroyed():

            #Check player 2 keys
            if keys[K_LEFT]:
                self.player2.move_left()

            if keys[K_RIGHT]:
                self.player2.move_right()

            if keys[K_0]:
                self.player2.shoot()

        return False

    def spawn_enemy_bullets(self) -> None:
        """Spawn bullets for mobs"""
        #Check if the enemy can shoot randomly
        rand = random.randint(0,self.fps*50)

        #If it does not hits the probability allow the mob to shoot
        if rand > self.fps:

            #Print debug statements
            if self.debug:
                print(f"Random generated: {rand}")

            #Return and no need to shoot
            return

        #Get a random bullet for the entity to shoot
        if len(self.enemies):
            enemy = random.sample(set(self.enemies),1)
        else:
            enemy = None

        #If the set is non-empty
        if enemy:

            #Get the first enemy of the set
            enemy = enemy[0]

            #Randomly get a direction
            if self.player1.is_destroyed():
                direction = Direction.DOWN
            elif self.player2.is_destroyed():
                direction = Direction.UP
            elif random.randint(0,1):
                direction = Direction.UP
            else:
                direction = Direction.DOWN

            #Create the bullet
            bullet2 = Bullet(self.sensitivity * 1.5, enemy.get_x() + enemy.get_width()//3, enemy.get_y(), direction, self.screen_width, self.screen_height, self.debug)

            #Rotate the bullet 180 degrees to face it down
            if direction == Direction.DOWN:
                bullet2.rotate(180)

            #Add the bullet to the bullet group
            self.mob_bullet.add(bullet2)

    def spawn_mobs(self) -> None:
        """Spawn enemies for the game"""
        #If there are still enemies left, Do nothing
        if len(self.enemies) > 0:
            return None

        #Increment wave
        self.wave += 1

        #Spawn the enemies
        for j in range(2):
            self.enemies.add([EnemyShip(self.sensitivity, self.screen_width//4 + i*self.screen_width//10, self.screen_height//2 - 50 + 50 * j, random.randint(1,self.wave), self.screen_width,  self.screen_height, None, self.debug) for i in range(6)])


    def get_scores(self) -> tuple:
        """Get the scores of the players"""
        return (self.p1_score, self.p2_score)

    def update(self) -> None:
        """Update the movement of the sprites"""

        #Set reset to false
        if self.resetted:
            self.resetted = not self.resetted

        #Spawn the mobs
        self.spawn_mobs()

        #Update the player
        self.player1.update()
        
        self.player2.update()

        #Update the enemies
        self.enemies.update()

        #Update explosions 
        self.explosions.update()

        #Spawn bullets for enemies
        self.spawn_enemy_bullets()

        #Update the position of the bullets
        self.player1_bullet.update()
        self.player2_bullet.update()
        self.mob_bullet.update()

        #Draw the bullets
        self.player1_bullet.draw(self.screen)
        self.player2_bullet.draw(self.screen)
        self.mob_bullet.draw(self.screen)

        #Draw the enemies
        self.enemies.draw(self.screen)

        #Draw the explosions
        self.explosions.draw(self.screen)

        #Draw the players
        if not self.player1.is_destroyed():
            self.player1.draw(self.screen)
        if not self.player2.is_destroyed():
            self.player2.draw(self.screen)

        #Call the superclass update
        super().update()

    def check_player_mob_collision(self, player_bullet):
        #Check collision of mobs with player 1 bullet
        ships = list(pygame.sprite.groupcollide(player_bullet, self.enemies, True, False).values())
        pts = 0
        #If the list is non-empty
        if ships:

            #Iterate through the ship
            for ship in ships[0]:

                #Destroy the ship
                ship.destroy()

                #If the ship is destroyed
                if ship.is_destroyed():
                    #Spawn an explosion in its place
                    self.explosions.add(Explosion(self.fps//4, ship.get_x(), ship.get_y(), self.screen_width, self.screen_height, 0, self.debug))

                    #Remove the ship from all groups
                    ship.kill()

                    #Remove sprites that collide with bullets and return the sum of all the scores
                    pts += ship.get_points()
        return pts
        

    def check_collision(self) -> None:
        """Check the collisions between all of the sprites"""
        #Check collisions of bullets
        pygame.sprite.groupcollide(self.player1_bullet, self.player2_bullet, True, True)
        pygame.sprite.groupcollide(self.player1_bullet, self.mob_bullet, True, True)
        pygame.sprite.groupcollide(self.player2_bullet, self.mob_bullet, True, True)

        #Check Collision of player 1
        bullet_hit_p = len(pygame.sprite.spritecollide(self.player1, self.player2_bullet, True)) 
        bullet_hit_m = len(pygame.sprite.spritecollide(self.player1, self.mob_bullet, True))

        #Check if it player bullet hit the other player
        if bullet_hit_p and not self.player1.isInvincible():
            self.p2_score += 500

        if bullet_hit_p + bullet_hit_m > 0 and not self.player1.is_destroyed():
            self.player1.destroy()
            self.explosions.add(Explosion(self.fps//4, self.player1.get_x(), self.player1.get_y(), self.screen_width, self.screen_height, 0, self.debug))
        
            

        #Check Collision of player 2
        bullet_hit_p = len(pygame.sprite.spritecollide(self.player2, self.player1_bullet, True))
        bullet_hit_m = len(pygame.sprite.spritecollide(self.player2, self.mob_bullet, True))
        if bullet_hit_p and not self.player2.isInvincible():
            self.p1_score += 500


        if bullet_hit_p + bullet_hit_m > 0 and not self.player2.is_destroyed():
            self.player2.destroy()
            self.explosions.add(Explosion(self.fps//4, self.player2.get_x(), self.player2.get_y(), self.screen_width, self.screen_height, 0, self.debug))
        

        #Check collision of mobs with player 1 bullet
        self.p1_score += self.check_player_mob_collision(self.player1_bullet)

        #Check collision of mobs with player 2 bullet
        self.p2_score += self.check_player_mob_collision(self.player2_bullet)


    def handle(self) -> State:
        """Handle the drawing of the screen"""

        #Check keypresses
        if self.check_keypresses():
            return State.PVP_PAUSE

        #Check collisions
        self.check_collision()

        #Update position of sprites
        self.update()

        #Draw the wave number
        self.write_main(Screen.font, WHITE, f"Wave: {self.wave}", self.screen_width // 2, 20)

        #Draw the lives of player 1
        self.write_main(Screen.font, WHITE, f"Lives: {self.player1.get_lives()}", self.screen_width - 10, 10, Direction.RIGHT)

        #Draw score of player 1
        self.write_main(Screen.font, WHITE, f"Score: {self.p1_score}", 10, 10, Direction.LEFT)

        #Draw the lives of player 2
        self.write_main(Screen.font, WHITE, f"Lives: {self.player2.get_lives()}", self.screen_width - 10, self.screen_height - 20, Direction.RIGHT)

        #Draw score of player 2
        self.write_main(Screen.font, WHITE, f"Score: {self.p2_score}", 10, self.screen_height - 20, Direction.LEFT)

        #Check if both players are destroyed
        if self.player1.is_destroyed() or self.player2.is_destroyed():
            return State.PVP_GAMEOVER

        return State.PVP