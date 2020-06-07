import pygame
import random
from . import LocalPVPScreen, Screen
from .. import State, Player, Direction, EnemyShip, WHITE, Explosion, Difficulty

class CoopScreen(LocalPVPScreen):
    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, fps:int, difficulty: Difficulty, player_lives:int = 3, debug:bool = False):
        """Main Coop screen"""

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

    def check_pvp_collision(self)->None:
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

    def bullet_direction(self) -> Direction:
        """Move the bullet down"""
        return Direction.DOWN

    def spawn_mobs(self) -> None:
        """Spawn enemies for the game"""
        #If there are still enemies left, Do nothing
        if len(self.enemies) > 0:
            return None

        #Increment wave
        self.wave += 1

        #Spawn the enemies
        for j in range(self.wave if self.wave < 5 else 5):
            self.enemies.add([EnemyShip(self.sensitivity, self.screen_width//4 + i*self.screen_width//10, 
                                self.screen_height//10 + EnemyShip.sprites[0].get_height() * j, random.randint(1,int(self.wave*self.difficulty.value()/4)), 
                                self.screen_width,  self.screen_height, None, self.mob_bullet, self.debug) for i in range(6)])

    def draw_words(self) -> None:
        """Draw the words on the screen"""
        #Draw the wave number
        self.write_main(Screen.font, WHITE, f"Wave: {self.wave}", self.screen_width // 2, 20)

        #Draw the lives of player 1
        self.write_main(Screen.font, WHITE, f"Lives: {self.player1.get_lives()}", self.screen_width - 10, 10, Direction.RIGHT)

        #Draw score of player 1
        self.write_main(Screen.font, WHITE, f"Score: {self.p1_score}", 10, 10, Direction.LEFT)

        #Draw the lives of player 2
        self.write_main(Screen.font, WHITE, f"Lives: {self.player2.get_lives()}", self.screen_width - 10, 20, Direction.RIGHT)

        #Draw score of player 2
        self.write_main(Screen.font, WHITE, f"Score: {self.p2_score}", 10, 20, Direction.LEFT)

