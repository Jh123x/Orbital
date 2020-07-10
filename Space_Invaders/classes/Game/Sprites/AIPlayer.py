import os
import random
import pygame
import numpy as np
import matplotlib.pyplot as plt
import torch
from . import Player, Bullet
from .. import Direction
from gym_invaders.ai_invader.agent import DQNAgent
from gym_invaders.ai_invader.model import DQNCNN
from gym_invaders.ai_invader.util import stack_frame,preprocess_frame

def stack_frames(frames, state, is_new=False):
    '''
    Function combine of utility functions to preprocess the frames
    '''
    # print()
    #Preprocess the frame
    frame = preprocess_frame(state, (84,84))

    #Stack the frame
    frames = stack_frame(frames, frame, is_new)

    #Return stacked frames
    return frames

class AIPlayer(Player):
    def __init__(self, sensitivity:int, game_width:int, game_height:int, initial_x:int, 
                    initial_y:int, init_life:int, fps:int, bullet_grp:pygame.sprite.Group(), 
                    bullet_direction:Direction, frames_per_action:int, ai = True, debug:bool = False):
        """Constructor for the AI Player class"""

        #Call the superclass
        super().__init__(sensitivity, game_width, game_height, initial_x, initial_y, init_life, fps,
                        bullet_grp, bullet_direction, debug, True)

        #Store the variables
        self.frames_per_action = frames_per_action
        self.state = None
        self.screen = None
        self.cd = self.frames_per_action
        self.ai = ai
        INPUT_SHAPE = (4,84,84)
        ACTION_SIZE = 6
        SEED = 0
        GAMMA = 0.99  # discount factor
        BUFFER_SIZE = 10000  # replay buffer size
        BATCH_SIZE = 64  # Update batch size
        LR = 0.0001  # learning rate
        TAU = 1e-3  # for soft update of target parameters
        UPDATE_EVERY = 7  # how often to update the network
        UPDATE_TARGET = 6 * BATCH_SIZE  # After which thershold replay to be started

        if ai:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            PATH = os.getcwd() + '/classes/Game/Sprites/model'
            # print(PATH)
            os.makedirs('obj', exist_ok=True)
            dict = torch.load(os.path.join(PATH,'sample.pth'),map_location=device)
            # print(dict.keys())
            self.ai = DQNAgent(INPUT_SHAPE, ACTION_SIZE, SEED, device, BUFFER_SIZE, BATCH_SIZE, GAMMA, LR, TAU, UPDATE_EVERY, UPDATE_TARGET, DQNCNN)
            self.ai.load_model(dict)

    def get_space(self):
        """
        Returns the pixel space of the screen
        Performs preliminary Preprocessing by making values
        """
        self.screen.draw_hitboxes()
        img = pygame.surfarray.array3d(self.screen.screen)
        # plt.imshow(img, interpolation='none')
        # plt.show()
        self.screen.screen.fill((0,0,0))
        return img

    def show_space(self):
        """Show the space in a matplotlib diagram"""
        image_transp = self.get_space()
        print(image_transp.shape)
        plt.imshow(image_transp, interpolation='none')
        plt.show()


    def action(self) -> None:
        """Does the action taken by the AI every frames"""
        # first pass
        if self.state is  None:
            self.state = stack_frames(None,self.get_space(), True)
            self.show_space()
        # updates the state of the game for the model

        self.state = stack_frames(self.state,self.get_space(), False)
        #If the AI is still under cooldown
        if self.cd:

            #Reduce the cooldown time for the action
            self.cd -= 1

        #Otherwise
        else:

            #Perform the AI action
            self.get_action()()

    def get_action(self,*args):
        """Get the next action taken by the AI"""
        #Add the AI to make the choice TODO
        # print(self.ai is None)
        #If an ai exists
        if self.ai:
            # Get possible actions
            actions = self.get_action_space()

            return actions[self.ai.action(self.state)]


        #Otherwise
        else:
            #Default AI
            
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

    def move_shoot(self, bool):
        '''
        To encompass both move_left and shoot, and move_right and shoot action
        from Original Space Invaders Gym Environment
        '''
        if bool:
            self.move_left()
            return self.shoot
        self.move_right()
        return self.shoot

    def get_action_space(self) -> tuple:
        """List of actions that the player can take (tuple of functions)"""
        return (self.shoot, self.move_left, self.move_right, lambda: 1, self.move_shoot(True),
                self.move_shoot(False))
    
    def no_screen(self):
        ''' Detect if screen does not exist'''
        return self.screen is None

    def set_screen(self, screen):
        self.screen = screen

        