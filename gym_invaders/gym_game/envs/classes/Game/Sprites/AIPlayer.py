import pygame
import random
import torch
from . import Player, Bullet
from .. import Direction
# from gym_invaders.ai_invader.agent import DQNAgent
# from gym_invaders.ai_invader.model import DQNCNN
# from gym_invaders.ai_invader.util import preprocess_frame,stack_frame

def stack_frames(frames, state, is_new=False):
    '''
    Function combine of utility functions to preprocess frames
    '''
    frame = preprocess_frame(state, 84)
    frames = stack_frame(frames,frame, is_new)
    return frames

class AIPlayer(Player):
    def __init__(self, sensitivity:int, game_width:int, game_height:int, initial_x:int, 
                    initial_y:int, init_life:int, fps:int, bullet_grp:pygame.sprite.Group(), 
                    bullet_direction:Direction, frames_per_action:int, ai = None, debug:bool = False):
        """Constructor for the AI Player class
        """

        #Call the superclass
        super().__init__(sensitivity, game_width, game_height, initial_x, initial_y, init_life, fps,
                        bullet_grp, bullet_direction, debug, True)

        #Store the variables
        self.frames_per_action = frames_per_action
        self.cd = self.frames_per_action
        if ai == None:
            self.ai = False
        else:
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.ai = DQNAgent()
            #self.ai.load_model(torch.load('<file path here>'))
        self.screen = None
        self.state = None
    def action(self) -> None:
        """Does the action taken by the AI every frames"""

        #If the AI is still under cooldown
        if self.cd:

            #Reduce the cooldown time for the action
            self.cd -= 1

        #Otherwise
        else:

            #Perform the AI action
            self.get_action()()

    def get_space(self):
        """
        Returns the pixel space of the screen
        Performs preliminary Preprocessing by making values positive
        """
        space = pygame.surfarray.array2d(self.screen.surface)
        return space *-1

    def draw(self, screen) -> None:
        """Draw the player onto the screen and stores it if not stored before."""

        #If there is no screen
        if not self.screen:

            #stores the screen
            self.screen = screen

        #Draw hitboxes
        self.screen.draw_hitboxes()

        #Draw model on the screen
        super().draw(screen)

    def get_action(self):
        """Get the next action taken by the AI"""
        #Add the AI to make the choice TODO

        #Get current actions
        actions = self.get_action_space()
        state = self.get_space()

        #If an ai exists
        if self.ai and self.state:
            # Stacks frames
            self.state = stack_frames(state, self.state, False)
            # Gets Maximum Value action
            a = self.ai.action(self.state)
            # Performs Action with greatest expected reward
            return actions[a]

        elif not self.state:
            # for the first timestep where there is no stackedframes yet
            self.state = stack_frames(None, state, False)
            return actions[0]
        #Otherwise Default AI
        else:
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

    def move_shoot(self, shoot:bool) -> bool:
        '''
        To encompass both move_left and shoot, and move_right and shoot action
        from Original Space Invaders Gym Environment
        '''
        if shoot:
            self.move_left()
            return self.shoot
        self.move_right()
        return self.shoot

    def get_action_space(self) -> tuple:
        """Returns a list of actions the AI player can take"""
        return (self.shoot, self.move_left, self.move_right, lambda : 1,self.move_shoot(True),
                self.move_shoot(False))


    


        