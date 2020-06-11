import pygame
from .. import Network, Player, State
from . import LocalPVPScreen
from pygame.locals import *

class OnlinePVPScreen(LocalPVPScreen):
    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, fps:int, player_lives:int = 3, debug:bool = False):

        #Call the superclass
        super().__init__(screen_width, screen_height, screen, sensitivity, fps, player_lives, debug)
        self.network = None
        self.set_state(State.ONLINE)

    def create_network(self):
        #Create the network
        self.network = Network("192.168.1.215",5555)

    def pack_data(self, player:Player, shoot:bool):
        return (self.network.get_id(), player.get_coord(), shoot)

    def unpack_data(self, data):
        return data[1], data[2]

    def generate_random_no(self):
        return self.network.send(('rand',))

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
                shot = self.player2.shoot()


        #Send information on current player
        _, player1_pos, shot = self.network.send(self.pack_data(self.player2, shot))

        #Update player 2 information
        self.player1.set_coord(player1_pos)

        #If player 2 shot
        if shot:
            self.player1.shoot()


    def handle(self):
        """Handle the drawing of the screen"""
        if not self.network:
            #Create the network
            self.create_network()

        #Check keypresses
        self.check_keypresses()

        #Check collisions
        self.check_collision()

        #Update position of sprites
        self.update()

        #Draw the words
        self.draw_words()

        #Check if both players are destroyed
        if self.player1.is_destroyed() or self.player2.is_destroyed():
            return State.TWO_PLAYER_GAMEOVER

        return self.state

