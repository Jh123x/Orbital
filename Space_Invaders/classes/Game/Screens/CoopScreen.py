#!/usr/bin/env python
import pygame
import random
from pygame.locals import *
from . import PlayScreen
from .. import State, Player, Direction, WHITE, Explosion, Difficulty, AchievmentTracker

class CoopScreen(PlayScreen):
    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, fps:int,
                 difficulty: Difficulty, tracker:AchievmentTracker, player_lives:int = 3, debug:bool = False):
        """Main Coop screen for local cooperative mode"""

        #Bullet groups for player 2
        self.player2_bullet = pygame.sprite.Group()

        #Call the super class
        super().__init__(screen_width, screen_height, screen, sensitivity, fps, difficulty,tracker, 1, player_lives, 0.1, debug)

        #Set to the correct state
        self.set_state(State.COOP)

        #Set the state of the enemy ship
        self.enemies.set_state(self.state)

    def comparator(self):
        """Return variable used for comparison"""
        return self.get_score()

    def handle_threshold(self) -> None:
        pass

    def update_trackers(self):
        self.tracker.add_value('coop', 1)


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

    def update(self) -> None:
        """Update the movement of the sprites"""

        #Update player 2 information
        self.player2.update()
        self.player2_bullet.update()
        self.player2_bullet.draw(self.screen)
        self.player2.draw(self.screen)

        #Call the superclass update
        super().update()

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
    
    def spawn_players(self) -> None:
        """Spawn the players"""
        #Recreate the players
        self.player1 = Player(self.sensitivity, self.screen_width, self.screen_height, self.screen_width//(3/2), self.screen_height-50, self.player_lives, self.fps, self.player1_bullet, Direction.UP, self.debug)
        self.player2 = Player(self.sensitivity, self.screen_width, self.screen_height, self.screen_width//3, self.screen_height-50, self.player_lives, self.fps, self.player2_bullet, Direction.UP, self.debug)

    def check_players_collision(self)->None:
        """Check collisions for players"""
        #Check if bullet hit player 2
        bullet_hit_m = len(pygame.sprite.spritecollide(self.player1, self.mob_bullet, True))
        if bullet_hit_m > 0 and not self.player1.is_destroyed():
            self.player1.destroy()
            self.explosions.add(Explosion(self.fps//4, self.player1.get_x(), self.player1.get_y(), self.screen_width, self.screen_height, 0, self.debug))
        
        #Check if bullet hit the player 1
        bullet_hit_m = len(pygame.sprite.spritecollide(self.player2, self.mob_bullet, True))
        if bullet_hit_m > 0 and not self.player2.is_destroyed():
            self.player2.destroy()
            self.explosions.add(Explosion(self.fps//4, self.player2.get_x(), self.player2.get_y(), self.screen_width, self.screen_height, 0, self.debug))

    def get_score(self) -> int:
        """Return the combined score of the players"""
        return super().get_score() + self.p2_score

    def get_gameover_state(self) -> State:
        """Returns the gameover mode for this state"""
        return State.GAMEOVER

    def bullet_direction(self) -> Direction:
        """Set the bullet direction to always go down"""
        return Direction.DOWN

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

    def check_powerups(self, ship) -> None:
        """Check if the powerups should be spawned"""
        #If powerups are not disabled
        if self.powerup_chance > 0:

            #Roll for chance of powerup spawning
            if self.generate_random_no() < self.powerup_chance:

                #Spawn the powerup
                super().spawn_powerups(ship.get_x(), ship.get_y())

            #If the power has not spawned during the wave
            elif self.powerup_numbers == 0 and len(self.enemies) == 0:

                #Spawn the powerup
                super().spawn_powerups(ship.get_x(), ship.get_y())

    def check_player_mob_collision(self, player_bullet):
        """Check the collision between the enemies and the players"""

        #Check collision of mobs with player 1 bullet
        ships = list(pygame.sprite.groupcollide(player_bullet, self.enemies, True, False).values()) + list(pygame.sprite.groupcollide(player_bullet, self.other_enemies, True, False).values())

        #Initialise the points the player got so far
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

                    #Check if powerups can spawn
                    self.check_powerups(ship)
                    

        #Return with the points the player got
        return pts
    
    def check_block_collision(self) -> None:
        """Check collisions with blocks"""
        #Check if the players or the enemies shot the blocks
        pygame.sprite.groupcollide(self.player1_bullet, self.blocks, True, True)
        pygame.sprite.groupcollide(self.blocks, self.mob_bullet, True, True)
        pygame.sprite.groupcollide(self.player2_bullet, self.blocks, True, True)

    def check_collisions(self) -> None:
        """Check collisions method for Coop"""

        #Check collisions of bullets
        pygame.sprite.groupcollide(self.player1_bullet, self.player2_bullet, True, True)
        pygame.sprite.groupcollide(self.player1_bullet, self.mob_bullet, True, True)
        pygame.sprite.groupcollide(self.player2_bullet, self.mob_bullet, True, True)

        #Check collisions of players
        self.check_players_collision()

        #Check powerup collisions
        self.check_powerup_collision()
        
        #Check collision of mobs with player 1 bullet
        self.p1_score += self.check_player_mob_collision(self.player1_bullet)

        #Check collision of mobs with player 2 bullet
        self.p2_score += self.check_player_mob_collision(self.player2_bullet)

        #Check block collisions
        self.check_block_collision()

    def check_powerup_collision(self):
        """Check the collisions of the powerups"""

        #Call superclass check powerup collisions
        super().check_powerup_collision()

        #Check the same for player 2
        if len(self.powerups):

            #Check if player hit the powerups
            hit = pygame.sprite.groupcollide(self.player2_bullet, self.powerups, True, True)

            #If player hit the powerups
            if len(hit):

                #For each list of powerups hit
                for l in hit.values():

                    #For each power up in powerup list
                    for p in l:

                        #Mutate player and current screen
                        p.get_ability()(self,self.player2)

    def draw_letters(self) -> None:
        """Draw the words on the screen"""
        #Draw the wave number
        self.write_main(self.font, WHITE, f"Wave: {self.wave}", self.screen_width // 2, 20)

        #Draw the lives of player 1
        self.write_main(self.font, WHITE, f"P1 Lives: {self.player1.get_lives()}", self.screen_width - 10, 10, Direction.RIGHT)

        #Draw score of player 1
        self.write_main(self.font, WHITE, f"P1 Score: {self.p1_score}", 10, 10, Direction.LEFT)

        #Draw the lives of player 2
        self.write_main(self.font, WHITE, f"P2 Lives: {self.player2.get_lives()}", self.screen_width - 10, 30, Direction.RIGHT)

        #Draw score of player 2
        self.write_main(self.font, WHITE, f"P2 Score: {self.p2_score}", 10, 30, Direction.LEFT)


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

