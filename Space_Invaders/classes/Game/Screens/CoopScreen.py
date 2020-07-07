#!/usr/bin/env python
import pygame
import random
from . import LocalPVPScreen, Screen, PlayScreen
from .. import State, Player, Direction, EnemyShip, WHITE, Explosion, Difficulty

class CoopScreen(LocalPVPScreen):
    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, fps:int, difficulty: Difficulty, player_lives:int = 3, debug:bool = False):
        """Main Coop screen for local cooperative mode"""

        #Call the super class
        super().__init__(screen_width, screen_height, screen, sensitivity, fps, player_lives, debug)

        #Store variables
        self.difficulty = difficulty

        #Set to the correct state
        self.set_state(State.COOP)
    
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
        return sum(super().get_scores())

    def get_gameover_state(self):
        return State.GAMEOVER

    def bullet_direction(self) -> Direction:
        """Set the bullet direction to always go down"""
        return Direction.DOWN

    def spawn_enemies(self, number:int) -> None:
        """Spawn enemies into the game
            Arguments: 
                number: Number of enemies to spawn (int)
            Returns: 
                No returns
        """

        #Make the enemies into rows of 6
        for j in range(number//6 if number // 6 < 5 else 5):
            self.enemies.add([EnemyShip(self.sensitivity, self.screen_width//4 + i*self.screen_width//10, self.screen_height//10 + EnemyShip.sprites[0].get_height() * j, self.wave_random(), self.screen_width,  self.screen_height, Direction.DOWN, self.mob_bullet, self.debug) for i in range(6)])

    def draw_letters(self) -> None:
        """Draw the words on the screen"""
        #Draw the wave number
        self.write_main(Screen.font, WHITE, f"Wave: {self.wave}", self.screen_width // 2, 20)

        #Draw the lives of player 1
        self.write_main(Screen.font, WHITE, f"P1 Lives: {self.player1.get_lives()}", self.screen_width - 10, 10, Direction.RIGHT)

        #Draw score of player 1
        self.write_main(Screen.font, WHITE, f"P1 Score: {self.p1_score}", 10, 10, Direction.LEFT)

        #Draw the lives of player 2
        self.write_main(Screen.font, WHITE, f"P2 Lives: {self.player2.get_lives()}", self.screen_width - 10, 30, Direction.RIGHT)

        #Draw score of player 2
        self.write_main(Screen.font, WHITE, f"P2 Score: {self.p2_score}", 10, 30, Direction.LEFT)

