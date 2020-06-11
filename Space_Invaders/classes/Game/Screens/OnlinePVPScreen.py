import pygame
from . import Screen, LocalPVPScreen
from .. import Network, Player, State, WHITE
from pygame.locals import *

class OnlinePVPScreen(LocalPVPScreen):
    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, fps:int, player_lives:int = 3, debug:bool = False):

        #Call the superclass
        super().__init__(screen_width, screen_height, screen, sensitivity, fps, player_lives, debug)

        #Initial network is none
        self.network = None
        self.waiting = True
        self.disconnected = False

        #Set the state to the correct state
        self.set_state(State.ONLINE)

    def create_network(self):
        """Create the network for the player to be hosted on"""
        #Create the network
        self.network = Network("192.168.1.215",5555)

    def pack_player_data(self, player:Player, shoot:bool):
        """Pack the data into the correct form to be sent"""
        return (self.network.get_id(), player.get_coord()[0], shoot)

    def generate_random_no(self):
        """Generate a random number from the server"""
        return self.random

    def get_random_direction(self) -> int:
        return int(self.br*10) < 5

    def check_keypresses(self) -> bool:
        """Check the keys which are pressed"""

        #Get all the number of keys
        keys = pygame.key.get_pressed()
        shot = False

        if not self.player2.is_destroyed():
            #Check player 1 keys
            if keys[K_a]:

                #Move player 1 to the left
                self.player2.move_left()

            if keys[K_d]:
                
                #Move player 1 to the right
                self.player2.move_right()

            if keys[K_SPACE]:

                #Let the player shoot
                self.shot = self.player2.shoot()

        #Send information on current player
        data = self.network.send(self.pack_player_data(self.player2, shot))
        if not data:
            self.disconnected = True
            return False
        else:
            _, player1_pos, shot, self.random, self.br = data

            #Update player 2 information
            self.player1.set_coord((int(player1_pos), 60))

            #If player 1 shot
            if shot:
                self.player1.shoot()
        return False


    def handle(self) -> State:
        """Handle the drawing of the screen"""

        #If it is not connected to the network
        if not self.network:

            #Create the network
            self.create_network()

        if self.waiting:
            data = self.network.send('waiting')
            print(f"Wait: {data}")

        #Draw the loading screen
        if self.waiting and data:
            #Draw loading screen
            self.write_main(Screen.end_font, WHITE, f"Loading", self.screen_width // 2, self.screen_height//2)
            self.back_rect = self.write_main(Screen.end_font, WHITE, f"Back", self.screen_width // 2, self.screen_height//2 + self.screen_height//15)

            if self.check_clicked(self.back_rect):
                return State.PLAYMODE

            return self.state

        elif self.disconnected:
            return State.TWO_PLAYER_GAMEOVER

        #Otherwise draw the game
        else:
            self.waiting = False
            state = super().handle()
            if state == State.TWO_PLAYER_GAMEOVER:
                self.network.close()
            return state

    def __del__(self):
        """Destructor for the object"""

        #If the network is connected
        if self.network:

            #Close the network
            self.network.close()

