import pygame
import random
from pygame.locals import *
from . import PlayScreen
from .. import BlockGroup, State, Difficulty


class ClassicScreen(PlayScreen):
    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, max_fps:int, difficulty:Difficulty, wave:int = 1, player_lives:int = 3,debug:bool = False):

        #Call the superclass
        super().__init__(screen_width, screen_height, screen, sensitivity, max_fps, difficulty, wave, player_lives, debug)

        #Change the state to classic
        self.state = State.CLASSIC

        #Create a block group
        self.blocks = BlockGroup(screen_width, screen_height//1.2, screen, 5, self.player.get_height() + 10)

    def reset(self) -> None:
        """Reset the classic screen"""
        #Reset the 5 blocks
        self.blocks = BlockGroup(self.screen_width, self.screen_height//1.2, self.screen, 5, self.player.get_height() + 10)

        #Call superclass reset
        super().reset()
    def draw_hitboxes(self):
        for sprite in self.blocks:
            pygame.draw.rect(self.surface, (0, 255, 0), sprite.rect, 0)
        super().draw_hitboxes()

    def enemy_touched_bottom(self):
        """Check if enemy touched the bottom of the screen"""
        return len(tuple(filter(lambda x: x.get_y() + x.get_height()//2 > self.screen_height - (self.player.get_height() + 10), self.enemies ))) > 0

    def check_collisions(self) -> int:
        """Check collisions between the sprites"""
        #Check if the player or the enemies shot the blocks
        pygame.sprite.groupcollide(self.up_bullets, self.blocks, True, True)
        pygame.sprite.groupcollide(self.blocks, self.down_bullets, True, True)

        #Call the superclass check collision
        return super().check_collisions()

    def update(self) -> None:
        """Update location of the sprites"""

        #Call superclass update
        super().update()

        #Draw the block
        self.blocks.draw(self.screen)

