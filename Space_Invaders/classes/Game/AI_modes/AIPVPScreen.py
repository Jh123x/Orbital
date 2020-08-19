import pygame
from pygame.locals import *
from .. import AIPlayer, State, Player, Direction, WHITE, LocalPVPScreen, AchievmentTracker

class AIPVPScreen(LocalPVPScreen):
    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, fps:int,
                 tracker:AchievmentTracker, player_lives:int = 3, debug:bool = False):
        """The constructor for the AI PVP screen"""
        
        #Call the superclass
        super().__init__(screen_width, screen_height, screen, sensitivity, fps,tracker ,player_lives, debug)

        #Set the state to the correct state
        self.set_state(State.AI_VS)

    def fetch_stats(self, keys:tuple = None):
        """Fetch stats for AI PVP screen"""
        if not key:
            key = ("aivs",)

        return super().fetch_stats(keys)

    def spawn_players(self) -> None:
        """Spawn the players for the game"""
        #Spawn the first player
        self.player1 = Player(self.sensitivity, self.screen_width, self.screen_height, self.screen_width//2, self.screen_height-50, self.player_lives, self.fps, self.player1_bullet, Direction.UP, self.debug, False)

        #Override the 2nd player with the AI player
        self.player2 = AIPlayer(self.sensitivity, self.screen_width, self.screen_height, self.screen_width//2, 50,
                        self.player_lives, self.fps, self.player2_bullet, Direction.DOWN, 1, True, self.debug)

        #Rotate the AI
        self.player2.rotate(180)

    def update(self) -> None:
        """Update the AI before calling superclass update"""

        #Let the AI do a move
        self.player2.action(self.get_entities())

        #Call the superclass update
        return super().update()

    def draw_letters(self) -> None:
        """Draw the words on the screen"""
        #Draw the wave number
        self.write_main(self.font, WHITE, f"Wave: {self.wave}", self.screen_width // 2, 20)

        #Draw the lives of player 1
        self.write_main(self.font, WHITE, f"AI Lives: {self.player2.get_lives()}", self.screen_width - 10, 10, Direction.RIGHT)

        #Draw score of player 1
        self.write_main(self.font, WHITE, f"AI Score: {self.p2_score}", 10, 10, Direction.LEFT)

        #Draw the lives of player 2
        self.write_main(self.font, WHITE, f"Lives: {self.player1.get_lives()}", self.screen_width - 10, self.screen_height - 20, Direction.RIGHT)

        #Draw score of player 2
        self.write_main(self.font, WHITE, f"Score: {self.p1_score}", 10, self.screen_height - 20, Direction.LEFT)

    def check_keypresses(self) -> bool:
        """Check the keys which are pressed
            Only player 1 keys are valid
        """
        #Get all the number of keys
        keys = pygame.key.get_pressed()

        #Check if they want to pause game
        if keys[K_p]:
            return True

        #If player 1 is not destroyed
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
        
        #Return False if they do not want to pause the game
        return False