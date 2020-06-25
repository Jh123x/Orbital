import pygame
import random
from pygame.locals import *
from . import PlayScreen
from .. import BlockGroup, State, Difficulty, MotherShip

class ClassicScreen(PlayScreen):
    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, max_fps:int, difficulty:Difficulty, wave:int = 1, player_lives:int = 3,debug:bool = False):
        """Classic screen for the game
            Main class to draw the classic screen for the game
        """
        #Call the superclass
        super().__init__(screen_width, screen_height, screen, sensitivity, max_fps, difficulty, wave, player_lives, 0, debug)

        #Change the state to classic
        self.state = State.CLASSIC

    def reset(self) -> None:
        """Reset the classic screen"""
        #Reset the 5 blocks
        self.blocks = BlockGroup(self.screen_width, self.screen_height//1.2, self.screen, 5, self.player.get_height() + 10)

        #Init no mothership
        self.mothership = None

        #Store mothership cooldown
        self.ms_cooldown = 0

        #Call superclass reset
        return super().reset()

    def randomly_spawn_mothership(self) -> bool:
        """Spawns a mothership randomly, returns if mothership is spawned"""

        #If the mothership does not exist and the random roll hits
        if not self.ms_cooldown and self.generate_random_no() < 1/900:
            
            #Create the mothership
            self.mothership = MotherShip(0, 50, self.screen_width, self.screen_height, 500)

            #Set the cooldown for the mothership
            self.ms_cooldown = self.fps * 3

            #Return True to signify that mothership spawned
            return True

        #If mothership is still under cooldown
        elif self.ms_cooldown:

            #Reduce cooldown by 1
            self.ms_cooldown -= 1

        #If it is not on cooldown and mothership still exists
        elif not self.ms_cooldown and self.mothership:

            #Set mothership to None
            self.mothership = None

        #return False if a mothership does not spawn
        return False

    def update(self) -> None:
        """Update class for classic"""
        
        #Attempts to spawn the mothership
        self.randomly_spawn_mothership()

        #If mothership exists
        if self.mothership:

            #Update the mothership
            self.mothership.update()

        #Call the superclass update
        return super().update()

    def draw_sprites(self) -> None:
        """Draw the sprites for the screen"""

        #If the mothership exists
        if self.mothership:

            #Draw the mothership
            self.mothership.draw(self.surface)

        #Draw the rest of the sprites
        return super().draw_sprites()

    def draw_hitboxes(self) -> None:
        """Draw hitboxes for the sprites"""

        #If mothership exists
        if self.mothership:
            
            #Draw the hitbox for the mothership
            pygame.draw.rect(self.surface, (5, 50, 5), self.mothership.rect, 0)

        #Call the superclass to draw the hitbox
        return super().draw_hitboxes()

    def check_collisions(self) -> None:
        """Check the collisions for the mothership"""

        #Initialise the score to 0
        score = 0

        #Check if ship has collided with bullets
        if self.mothership and len(pygame.sprite.spritecollide(self.mothership, self.up_bullets, True)) > 0:

            #Get points of mothership and add it to score
            score += self.mothership.get_points()

            #If so delete the mothership
            self.mothership = None

        #Return the superclass check collisions and add the score to it
        return score + super().check_collisions()