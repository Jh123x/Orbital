import pygame
import random
from . import Player, Bullet
from .. import Direction

class AIPlayer(Player):
    def __init__(self, sensitivity:int, game_width:int, game_height:int, initial_x:int, 
                    initial_y:int, init_life:int, fps:int, bullet_grp:pygame.sprite.Group(), 
                    bullet_direction:Direction, frames_per_action:int, ai = None, debug:bool = False):
        """Constructor for the AI Player class"""

        #Call the superclass
        super().__init__(sensitivity, game_width, game_height, initial_x, initial_y, init_life, fps,
                        bullet_grp, bullet_direction, debug, True)

        #Store the variables
        self.frames_per_action = frames_per_action
        self.cd = self.frames_per_action
        self.ai = ai

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

    def get_action(self,*args):
        """Get the next action taken by the AI"""

        #Add the AI to make the choice TODO

        #If an ai exists
        if self.ai:
            self.ai.apply()

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

    def get_action_space(self) -> tuple:
        """Returns a list of actions the AI player can take"""
        return self.move_left, self.move_right, self.shoot


    


        