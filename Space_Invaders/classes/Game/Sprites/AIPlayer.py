import os
import random
import pygame
import numpy as np
from . import Player, Bullet
from .. import Direction, DQNAgent, DQNCNN, stack_frame, preprocess_frame

class AIPlayer(Player):
    def __init__(self, sensitivity:int, game_width:int, game_height:int, initial_x:int, 
                    initial_y:int, init_life:int, fps:int, bullet_grp:pygame.sprite.Group(), 
                    bullet_direction:Direction, frames_per_action:int, 
                    ai_avail = True, debug:bool = False):
        """Constructor for the AI Player class"""

        #Call the superclass
        super().__init__(sensitivity, game_width, game_height, initial_x, initial_y, init_life, fps,
                        bullet_grp, bullet_direction, debug, True)

        #Store the variables
        self.frames_per_action = frames_per_action
        self.state = None
        self.screen = None
        self.cd = self.frames_per_action
        
        #If ai is available
        if ai_avail:

            #AI variables
            ACTION_SIZE = 6
            SEED = 0
            GAMMA = 0.99  # discount factor
            BUFFER_SIZE = 10000  # replay buffer size
            BATCH_SIZE = 64  # Update batch size
            LR = 0.0001  # learning rate
            TAU = 1e-3  # for soft update of target parameters
            UPDATE_EVERY = 7  # how often to update the network
            UPDATE_TARGET = 6 * BATCH_SIZE  # After which thershold replay to be started

            #Load the Deep Q learning Agent
            self.ai = DQNAgent(AIPlayer.input_shape, ACTION_SIZE, SEED,  AIPlayer.device, BUFFER_SIZE, BATCH_SIZE, GAMMA, LR, TAU, UPDATE_EVERY, UPDATE_TARGET, DQNCNN)

            #Load the model
            self.ai.load_model(AIPlayer.ai_dic)

    def get_space(self, screen):
        """
        Returns the pixel space of the screen
        Performs preliminary Preprocessing by making values
        """

        #Convert the surface to matrix of rgb
        img = pygame.surfarray.array3d(screen)

        #Return the matrix of rgb
        return img

    def stack_frames(self, screen):
        '''
        Function combine of utility functions to preprocess the frames
        '''
        #Preprocess the frame (Input shape needs to be processed to 1x2 tuple from 1x3)
        frame = preprocess_frame(self.get_space(screen), AIPlayer.input_shape[1:])

        #Stack the frame
        frames = stack_frame(self.state, frame, self.state is None)

        #Return stacked frames
        return frames

    def action(self, screen) -> None:
        """Does the action taken by the AI every frames"""

        #If there is no screen do nothing
        if not self.has_screen():
            return 

        # Updates the state of the game for the model
        self.state = self.stack_frames(screen)

        #If the AI is still under cooldown
        if self.cd:

            #Reduce the cooldown time for the action
            self.cd -= 1

        #Otherwise
        else:

            #Perform the AI action
            self.get_action()()

            #Reset the cooldown
            self.cd = self.frames_per_action

    def no_ai(self):
        """No ai = random ai"""
        #Get current actions
        actions = self.get_action_space()

        #Generate a random action
        rng = random.randint(0,100)

        #If the player is on cooldown
        if not self.on_cooldown():
            if rng < 20:
                return actions[2]
            elif rng < 60:
                return actions[1]
            else:
                return actions[0]
        else:
            if rng < 50:
                return actions[1]
            else:
                return actions[0]

    def get_action(self,*args):
        """Get the next action taken by the AI"""
        #Add the AI to make the choice TODO

        #If an ai exists
        if self.ai:
            # Get possible actions
            actions = self.get_action_space()
            return actions[self.ai.action(self.state)]

        #Otherwise
        else:
            #Default AI
            return self.no_ai()
            

    def move_shoot(self, left:bool):
        '''
        To encompass both move_left and shoot, and move_right and shoot action
        from Original Space Invaders Gym Environment
        '''

        #If left 
        if left:

            #Move left
            self.move_left()

        #Otherwise
        else:

            #Move right
            self.move_right()

        #Return shoot function
        return self.shoot

    def get_action_space(self) -> tuple:
        """List of actions that the player can take (tuple of functions)"""
        return (self.shoot, self.move_left, self.move_right, lambda: 1, self.move_shoot(True),
                self.move_shoot(False))

    def draw(self, screen):
        """Draw the object
            Assign screen object if it is not done previously
        """

        #If there is no screen
        if not self.screen:

            #Set the screen
            self.screen = screen

        #Call the superclass draw
        super().draw(screen)
    
    def has_screen(self):
        ''' Detect if screen does not exist'''
        return self.screen != None