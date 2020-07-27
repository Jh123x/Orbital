import pygame
import random
import time
from pygame.locals import *
from . import ClassicScreen
from .. import *

class LocalPVPScreen(ClassicScreen):
    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, fps:int, player_lives:int = 3, debug:bool = False):
        """Constructor for local PVP class"""

        #Bullet groups
        self.player2_bullet = pygame.sprite.Group()

        #Call the super class classic screen object
        super().__init__(screen_width, screen_height, screen, sensitivity, fps, Difficulty(3), 1, player_lives, debug)

        #Set current state
        self.set_state(State.PVP)

        #Set PVP enemyships
        self.enemies = EnemyShips(self.state)

        #Create score for player2
        self.p2_score = 0

        #Spawn Players
        self.spawn_players()

    def randomly_spawn_mothership(self) -> None:
        """Do not spawn any motherships for 2 players"""
        return

    def spawn_players(self) -> None:
        """Create the players variables"""
        #Initialise the players
        self.player1 = Player(self.sensitivity, self.screen_width, self.screen_height, self.screen_width//2, 50, self.player_lives, self.fps, self.player1_bullet, Direction.DOWN, self.debug)
        self.player2 = Player(self.sensitivity, self.screen_width, self.screen_height, self.screen_width//2, self.screen_height-50, self.player_lives, self.fps, self.player2_bullet, Direction.UP, self.debug)

        #Rotate the image of the player at the top
        self.player1.rotate(180)

    def get_entities(self):
        """Get entities in pvp"""
        return super().get_entities() + (self.player1,)
        
    def reset(self) -> None:
        """Reset the environment"""
        #If the environment is already resetted
        if self.resetted:

            #Do nothing
            return

        #Reset player 2 score
        self.p2_score = 0

        #Reset player model
        self.player2.reset()

        #Empty groups
        self.player2_bullet.empty()

        #Call the superclass
        super().reset()

        #Empty block grp
        self.blocks.empty()

    def spawn_enemies(self, number:int = None) -> None:
        """Spawn enemies into the game, Ignore numbers"""

        #Make the enemies into rows of 6
        for j in range(2):
            self.enemies.add([EnemyShip(self.sensitivity, self.screen_width//4 + i*self.screen_width//10, self.screen_height//2 - EnemyShip.sprites[0].get_height() * j, self.wave_random(), self.screen_width,  self.screen_height, self.get_random_direction(), self.mob_bullet, self.debug) for i in range(6)])

    def get_pause_state(self) -> State:
        """Return the pause state"""
        return State.TWO_PLAYER_PAUSE

    def get_gameover_state(self) -> State:
        """Return the gameover state"""
        return State.TWO_PLAYER_GAMEOVER

    def update_keypresses(self) -> bool:
        """Check the keys which are pressed"""
        #Get all the number of keys
        keys = pygame.key.get_pressed()

        #If player 2 is not destroyed
        if not self.player2.is_destroyed():

            #Check player 2 keys
            if keys[K_LEFT]:
                self.player2.move_left()

            if keys[K_RIGHT]:
                self.player2.move_right()

            if keys[K_0]:
                self.player2.shoot()

        #Call the superclass update keypress
        return super().update_keypresses()

    def draw_hitboxes(self, screen = None) -> None:
        """Draw hitboxes for players and objects"""
        #Check if screen is none
        if screen == None:

            #Set to self.surface if it is none
            screen = self.surface

        #Draw player 2 bullets
        for sprite in self.player2_bullet:
            pygame.draw.rect(screen, (100,255,0), sprite.rect, 0)

        #Draw the player 2
        pygame.draw.rect(screen, (55,255,10*self.player2.get_lives()), self.player2.rect, 0)

        #Call the superclass draw
        super().draw_hitboxes(screen)

    def get_random_direction(self) -> int:
        """Get a random direction (0 or 1)"""
        return int(self.generate_random_no()*10 < 5)

    def bullet_direction(self) -> Direction:
        """Generate the bullet direction for the bullets"""
        #Randomly get a direction
        if self.get_random_direction():
            direction = Direction.UP

        else:
            direction = Direction.DOWN

        return direction

    def get_scores(self) -> tuple:
        """Get the scores of the players"""
        return (self.p1_score, self.p2_score)

    def update(self) -> None:
        """Update the movement of the sprites"""

        #Update player 2 information
        self.player2.update()
        self.player2_bullet.update()
        self.player2_bullet.draw(self.screen)
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

        #Return with the points the player got
        return pts

    def check_collisions(self) -> None:
        """Check the collisions between all of the sprites"""
        #Check collisions of bullets
        pygame.sprite.groupcollide(self.player1_bullet, self.player2_bullet, True, True)
        pygame.sprite.groupcollide(self.player1_bullet, self.mob_bullet, True, True)
        pygame.sprite.groupcollide(self.player2_bullet, self.mob_bullet, True, True)

        #Check player vs player collisions
        self.check_players_collision()
        
        #Check collision of mobs with player 1 bullet
        self.p1_score += self.check_player_mob_collision(self.player1_bullet)

        #Check collision of mobs with player 2 bullet
        self.p2_score += self.check_player_mob_collision(self.player2_bullet)

    def check_players_collision(self):
        """Check collisions between the players"""
        #Check if bullet hit the player 1
        bullet_hit_p = len(pygame.sprite.spritecollide(self.player1, self.player2_bullet, True)) 
        bullet_hit_m = len(pygame.sprite.spritecollide(self.player1, self.mob_bullet, True))
        if bullet_hit_p and not self.player1.isInvincible():
            self.p2_score += 500
        if bullet_hit_p + bullet_hit_m > 0 and not self.player1.is_destroyed():
            self.player1.destroy()
            self.explosions.add(Explosion(self.fps//4, self.player1.get_x(), self.player1.get_y(), self.screen_width, self.screen_height, 0, self.debug))
        
        #Check if Player 2 bullet hit the player 1
        bullet_hit_p = len(pygame.sprite.spritecollide(self.player2, self.player1_bullet, True))
        bullet_hit_m = len(pygame.sprite.spritecollide(self.player2, self.mob_bullet, True))
        if bullet_hit_p and not self.player2.isInvincible():
            self.p1_score += 500
        if bullet_hit_p + bullet_hit_m > 0 and not self.player2.is_destroyed():
            self.player2.destroy()
            self.explosions.add(Explosion(self.fps//4, self.player2.get_x(), self.player2.get_y(), self.screen_width, self.screen_height, 0, self.debug))

    def draw_letters(self) -> None:
        """Draw the words on the screen"""
        #Draw the wave number
        self.write_main(self.font, WHITE, f"Wave: {self.wave}", self.screen_width // 2, 20)

        #Draw the lives of player 1
        self.write_main(self.font, WHITE, f"Lives: {self.player2.get_lives()}", self.screen_width - 10, 10, Direction.RIGHT)

        #Draw score of player 1
        self.write_main(self.font, WHITE, f"Score: {self.p2_score}", 10, 10, Direction.LEFT)

        #Draw the lives of player 2
        self.write_main(self.font, WHITE, f"Lives: {self.player1.get_lives()}", self.screen_width - 10, self.screen_height - 20, Direction.RIGHT)

        #Draw score of player 2
        self.write_main(self.font, WHITE, f"Score: {self.p1_score}", 10, self.screen_height - 20, Direction.LEFT)

    def handle(self) -> State:
        """Handle the drawing of the screen"""
        #Check if both players are destroyed
        if self.player2.is_destroyed():

            #Mark the game as over
            self.over = True

            #Return the gameover state
            return self.get_gameover_state()

        #Otherwise return the current state
        return super().handle()