import pygame
from pygame.locals import *
import matplotlib.pyplot as plt
from . import LocalPVPScreen
from .. import AIPlayer, State, Player, Direction

class AIPVPScreen(LocalPVPScreen):
    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, fps:int,
                 player_lives:int = 3, debug:bool = False):
        """The AI PVP screen"""
        
        #Call the superclass
        super().__init__(screen_width, screen_height, screen, sensitivity, fps, player_lives, debug)

        #Set the state to the correct state
        self.set_state(State.AI_VS)

    def show_space(self):
        """Show the space in a matplotlib diagram"""
        screen = self.get_hitboxes_copy()
        image_transp = pygame.surfarray.array3d(screen)
        print(image_transp.shape)
        plt.imshow(image_transp, interpolation='none')
        plt.show()

    def spawn_players(self) -> None:
        """Spawn the players for the game"""
        #Spawn the first player
        self.player1 = Player(self.sensitivity, self.screen_width, self.screen_height, self.screen_width//2, self.screen_height-50, self.player_lives, self.fps, self.player1_bullet, Direction.UP, self.debug, False)

        #Override the 2nd player with the AI player
        self.player2 = AIPlayer(self.sensitivity, self.screen_width, self.screen_height, self.screen_width//2, 50,
                        self.player_lives, self.fps, self.player2_bullet, Direction.DOWN, 1, True, self.debug)

        #Rotate the AI
        self.player2.rotate(180)

    def check_keypresses(self) -> bool:
        """Check the keys which are pressed
            Only player 1 keys are valid
        """
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
        
        #Return False if they do not want to pause the game
        return False

    def handle(self) -> State:
        """Handles the drawing of the screen"""

        #Let the AI do a move
        self.player2.action(self.get_hitboxes_copy())

        #Call the superclass handle
        return super().handle()