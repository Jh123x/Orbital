import pygame
import queue
from . import Screen, LocalPVPScreen
from .. import Network, Player, State, WHITE, Bullet
from pygame.locals import *

class OnlinePVPScreen(LocalPVPScreen):
    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, fps:int, player_lives:int = 3, debug:bool = False):
        """The main class for the online PVP screen"""

        #Call the superclass
        super().__init__(screen_width, screen_height, screen, sensitivity, fps, player_lives, debug)

        #Initial network is none
        self.network = None
        self.waiting = True
        self.disconnected = False
        self.shot = False

        #Create queue for player action
        self.queue = queue.Queue()

        #Set the state to the correct state
        self.set_state(State.ONLINE)

    def create_network(self):
        """Create the network for the player to be hosted on"""
        #Create the network
        self.network = Network("192.168.1.215", 9999)

    def pack_player_data(self, player:Player, shoot:bool, score:int):
        """Pack the data into the correct form to be sent"""
        return (player.get_coord()[0], shoot, score)

    def generate_random_no(self):
        """Generate a random number from the server"""
        return self.random

    def shoot_bullet(self, enemy):
        """Modified shoot bullet for online"""
        #If the set is non-empty
        if enemy:

            #Get the x_coord of the enmy
            x_coord = enemy.get_x()

            #Get direction of bullet
            direction = self.bullet_direction()

            #Add bullet to the mob_bullets
            self.mob_bullet.add(
                #Create the bullet object
                Bullet(self.sensitivity, x_coord, self.screen_height//2, direction, self.screen_width, self.screen_height, self.debug)
                )
            
    def get_random_direction(self) -> int:
        """Get the random direction"""

        #Generate random number
        chksum = int(self.generate_random_no()*10)

        #Get the boolean value
        res = chksum < 5

        #If it is player 2
        if self.br:

            #Invert it
            res = not res

        #Return the boolean
        return res

    def check_keypresses(self) -> bool:
        """Check the keys which are pressed"""

        #Get all the number of keys
        keys = pygame.key.get_pressed()

        #Flag to check if online player shot
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
            else:
                self.shot = False

        #Return to false screen 
        return False


    def communicate(self):
        """Communicate with the server"""
        #Send information on current player
        data = self.network.send(self.pack_player_data(self.player2, self.shot, self.p1_score))

        #If player is waiting
        if not self.waiting:
            
            #Check if player should continue to wait
            self.waiting = data['waiting']

        #If the data is empty
        if not self.waiting:

            #Unpack the data
            player1_pos, shot, self.p2_score= data['data']
            self.random = data['random']

            #Update player 2 information
            self.player1.set_coord((int(player1_pos), 60))

            #If player 1 shot
            if shot:

                #Shoot for the player
                self.player1.shoot()

    def handle(self) -> State:
        """Handle the drawing of the screen"""
        #If it is not connected to the network
        if not self.network:

            #Create the network
            self.create_network()

        #Communicate with network
        try:
            self.communicate()
        except Exception as exp:
            print(f"Error communicating: {exp}")

        #Draw the loading screen
        if self.waiting:

            #Draw loading screen
            self.write_main(Screen.end_font, WHITE, f"Loading", self.screen_width // 2, self.screen_height//2)
            self.back_rect = self.write_main(Screen.end_font, WHITE, f"Back", self.screen_width // 2, self.screen_height//2 + self.screen_height//15)

            #Check if player clicked the back button
            if self.check_clicked(self.back_rect):
                
                #Close the network
                self.close_network()

                #Return to the playmode screen
                return State.PLAYMODE

            #Otherwise return current state 
            return self.state

        #IF player disconnected go to gameover screen
        elif self.disconnected:

            #Close the network
            self.close_network()

            #Return next state
            return State.TWO_PLAYER_GAMEOVER

        #Otherwise draw the game
        else:
            #Set waiting to false
            if self.waiting:
                self.waiting = False

            #Call the superclass handle
            state = super().handle()

            #Set if the next state is gameoveer
            if state == State.TWO_PLAYER_GAMEOVER:

                #Close the network
                self.close_network()

            #Return next state
            return state

    def close_network(self):
        """Close the network and reset variable"""
        #If there is a socket previously
        if self.network:
            self.network.close()

        self.network = None
        self.waiting = True
        self.reset()

    def __del__(self):
        """Destructor for the object"""

        #If the network is connected
        if self.network:

            #Close the network
            self.network.close()

