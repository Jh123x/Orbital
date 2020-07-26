import pygame
import random
from pygame.locals import *
from . import ClassicScreen
from .. import *

class PlayScreen(ClassicScreen):
    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, max_fps:int, difficulty: Difficulty, wave:int = 1, player_lives:int = 3, 
                powerup_chance:float = 0.1, debug:bool = False):
        """The Endless mode screen"""

        #Power ups group
        self.powerups = pygame.sprite.Group()

        #Store the powerup chance
        self.powerup_chance = powerup_chance

        #Call the superclass init
        super().__init__(screen_width, screen_height, screen, sensitivity, max_fps, difficulty, wave, player_lives, debug)

        #Set state to play state
        self.set_state(State.PLAY)

    def set_powerup_chance(self, chance:float) -> None:
        """Set the powerup chance"""
        self.powerup_chance = chance

    def draw_hitboxes(self, screen = None) -> None:
        """Draw hitboxes for the objects on screen"""
        #Check if screen is none
        if screen == None:

            #Set to self.surface if it is none
            screen = self.surface

        #Draw for powerups
        for p_up in self.powerups:
            pygame.draw.rect(screen, (255,255,10 * p_up.get_power_type()), p_up.rect, 0)

    def update_powerups(self) -> None:
        """Update and draw the powerups"""
        #Update powerups
        self.powerups.update()

        #Draw the powerups
        self.powerups.draw(self.screen)

    def get_random_boss(self) -> EnemyShip or None:
        """Get a random enemy"""

        #Generate list of enemies other than mothership
        lst = tuple(filter(lambda x: type(x) != MotherShip, self.other_enemies))

        #If the list is not empty
        if lst:

            #Return a random boss
            return lst[int(self.generate_random_no()* (len(lst)-1))]

    def spawn_enemy_bullets(self) -> None:
        """Endless mode spawn bullets
            To account for the brute and scout bullets
        """

        #Get a random boss
        boss = self.get_random_boss()

        #If there are other enemies
        if boss:

            #Scale random according to fps
            rand = self.generate_random_no()*self.fps*4

            #If rand <= 5
            if rand <= 3:

                #Let the boss shoot
                boss.shoot()

        return super().spawn_enemy_bullets()

    def spawn_enemies(self, number:int) -> None:
        """Spawn enemies if the conditions are met"""
        #Spawn the scout if condition is met
        self.spawn_scout()

        #Spawn brute if the conditions are met
        self.spawn_brute()

        #Spawn Crabs if the conditions are met
        self.spawn_crabs()

        #Call the superclass to spawn enemies
        super().spawn_enemies(number)

    def _spawn_crabs(self, x):
        #Add the scout to the other enemies grp
        self.other_enemies.add(Crabs(self.sensitivity, x, self.screen_height//10, 1,  self.screen_width, self.screen_height, self.mob_bullet, self.debug))

    def spawn_crabs(self):
        """Spawn crabs"""        
        if self.wave % 10 == 0:
            total = self.wave
            for i in range(1, total + 1):
                self._spawn_crabs(self.screen_width//(total/i))

    def spawn_brute(self) -> None:
        """Spawn a brute if the conditions are met"""

        #Spawn the brute every wave
        if self.wave % 15 == 0:

            #Add the brute to the other enemies group
            self.other_enemies.add(Brute(self.sensitivity, self.generate_random_no() * self.screen_width, self.screen_height//10, self.screen_width, self.screen_height, self.mob_bullet, self.debug))
            

    def spawn_scout(self) -> None:
        """Spawn the scout unit if the condition is met"""

        #Spawn the scout ever 5 waves
        if self.wave % 5 == 0:

            #Add the scout to the other enemies grp
            self.other_enemies.add(Scout(self.sensitivity, self.screen_width//4 + self.screen_width//10, self.screen_height//10, 1,  self.screen_width, self.screen_height, self.mob_bullet, self.debug))

    def spawn_powerups(self, x:int, y:int) -> None:
        """Spawn a powerup at specified x and y coordinate"""

        #Spawn the powerup
        self.powerups.add(PowerUp(x, y, 50, 50, random.choice(PowerUp.get_powerups()), self.fps * 3.5))

        #Increase the number of powerups
        self.powerup_numbers += 1

    def check_collisions(self):
        """Check collision of the various sprites"""

        #Check collisions of powerups
        self.check_powerup_collision()

        #Get destroyed ship
        ship = super().check_collisions()

        #If the ship exists and is destroyed
        if ship and ship.is_destroyed():

            #If powerups are not disabled
            if self.powerup_chance > 0:

                #Roll for chance of powerup spawning
                if self.generate_random_no() < self.powerup_chance:

                    #Spawn the powerup
                    self.spawn_powerups(ship.get_x(), ship.get_y())

                #If the power has not spawned during the wave
                elif self.powerup_numbers == 0 and len(self.enemies) == 0:

                    #Spawn the powerup
                    self.spawn_powerups(ship.get_x(), ship.get_y())

        #Return the destroyed ship
        return ship

    def check_powerup_collision(self) -> None:
        """Check the collisions of the powerups"""
        #If there are powerups
        if len(self.powerups):

            #Check if player hit the powerups
            hit = pygame.sprite.groupcollide(self.player1_bullet, self.powerups, True, True)

            #If player hit the powerups
            if len(hit):

                #For each list of powerups hit
                for l in hit.values():

                    #For each power up in powerup list
                    for p in l:

                        #Mutate player and current screen
                        p.get_ability()(self,self.player1)

                        #Spawn explosion in the place of the powerup
                        self.spawn_explosion(p.get_x(), p.get_y())

    def update(self) -> None:
        """Update for the play screen"""
        #Update powerups
        self.update_powerups()

        #Call superclass update method
        return super().update()

    def draw_sprites(self) -> None:
        """Draw sprites for the play screen"""

        #Draw the powerup on the screen
        self.powerups.draw(self.screen)

        #Draw the other sprites using the superclass
        return super().draw_sprites()

    def reset(self) -> None:
        """Reset for the play mode"""
        #Call the super class reset
        super().reset()

        #Reset the blocks from classic mode
        self.blocks.empty()

        #Reset the count for the Brute
        Brute.reset()

        #Reset powerup number
        self.powerup_numbers = 0

        #Empty powerup group
        self.powerups.empty()