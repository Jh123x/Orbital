import pygame
from pygame.locals import *
from .. import CoopScreen, Player, AIPlayer, WHITE, Difficulty, Direction, State

class AICoopScreen(CoopScreen):
    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, fps:int, difficulty: Difficulty, player_lives:int = 3, debug:bool = False):
        """Main constructor the AICoopScreen"""
        
        #Call the superclass constructor
        super().__init__(screen_width, screen_height, screen, sensitivity, fps, difficulty, player_lives, debug)

        #Set the state
        self.set_state(State.AI_COOP)

    def spawn_players(self) -> None:
        """Spawn the players
            Overrides one of the players in CoopScreen with an AI
        """
        #Create the player
        self.player1 = Player(self.sensitivity, self.screen_width, self.screen_height, self.screen_width//(3/2), self.screen_height-50, self.player_lives, self.fps, self.player1_bullet, Direction.UP, self.debug)

        #Create the AI
        self.player2 = AIPlayer(self.sensitivity, self.screen_width, self.screen_height, self.screen_width//3, self.screen_height-50, self.player_lives, self.fps, self.player2_bullet, Direction.UP, 1, True, self.debug)

    def draw_letters(self) -> None:
        """Draw the words on the screen"""
        #Draw the wave number
        self.write_main(self.font, WHITE, f"Wave: {self.wave}", self.screen_width // 2, 20)

        #Draw the lives of player 1
        self.write_main(self.font, WHITE, f"P1 Lives: {self.player1.get_lives()}", self.screen_width - 10, 10, Direction.RIGHT)

        #Draw score of player 1
        self.write_main(self.font, WHITE, f"P1 Score: {self.p1_score}", 10, 10, Direction.LEFT)

        #Draw the lives of player 2
        self.write_main(self.font, WHITE, f"AI Lives: {self.player2.get_lives()}", self.screen_width - 10, 30, Direction.RIGHT)

        #Draw score of player 2
        self.write_main(self.font, WHITE, f"AI Score: {self.p2_score}", 10, 30, Direction.LEFT)

    def update_keypresses(self) -> bool:
        """Check the keys which are pressed"""
        #Get all the number of keys
        keys = pygame.key.get_pressed()

        #If the player wants to pause the game
        if keys[K_p]:

            #Return True
            return True

        #If player 1 is not destroyed
        if not self.player1.is_destroyed():

            #Check player 2 keys
            if keys[K_a]:
                self.player1.move_left()

            if keys[K_d]:
                self.player1.move_right()

            if keys[K_SPACE]:
                self.player1.shoot()

        return False

    def update(self) -> None:
        """Update method for the AICoopScreen"""

        #Update the action of the AI
        self.player2.action(self.get_entities())

        #Call the superclass update
        return super().update()
