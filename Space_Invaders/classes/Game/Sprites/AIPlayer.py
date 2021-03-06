import os
import random

import numpy as np
import pygame

from . import Player, Bullet, StateMachine
from .. import Direction


class AIPlayer(Player):
    def __init__(self, sensitivity: int, game_width: int, game_height: int, initial_x: int,
                 initial_y: int, init_life: int, fps: int, bullet_grp: pygame.sprite.Group(),
                 bullet_direction: Direction, frames_per_action: int,
                 ai_avail=True, boss: bool = False, debug: bool = False):
        """Constructor for the AI Player class"""

        # Call the superclass
        super().__init__(sensitivity, game_width, game_height, initial_x, initial_y, init_life, fps,
                         bullet_grp, bullet_direction, debug, True)

        # Store the variables
        self.frames_per_action = frames_per_action
        self.state = None
        self.screen = None
        self.cd = self.frames_per_action
        self.boss = boss
        # If ai is available
        if ai_avail == True:
            self.ai = StateMachine(40)

    def get_space(self, screen):
        """
        Returns the pixel space of the screen
        Performs preliminary Preprocessing by making values
        """

        # Convert the surface to matrix of rgb
        img = pygame.surfarray.array3d(screen)

        # Return the matrix of rgb
        return img

    def get_points(self) -> int:
        """Points the AI player is worth"""
        return 0

    def action(self, gamestate) -> None:
        """Does the action taken by the AI every frames"""

        self.get_entities(*gamestate)

        # If the AI is still under cooldown
        if self.cd:

            # Reduce the cooldown time for the action
            self.cd -= 1

        # Otherwise
        else:

            # Perform the AI action
            self.get_action()()

            # Reset the cooldown
            self.cd = self.frames_per_action

    def no_ai(self):
        """No ai = random ai"""
        # Get current actions
        actions = self.get_action_space()

        # Generate a random action
        rng = random.randint(0, 100)

        # If the player is on cooldown
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

    def get_action(self, *args):
        """Get the next action taken by the AI"""
        # Add the AI to make the choice TODO

        # If an ai exists
        if self.ai == 'torch':
            # Get possible actions
            actions = self.get_action_space()
            return actions[self.ai.action(self.state)]
        elif self.ai:
            action = self.get_action_space()
            return action[self.ai.state_check(self.state)]

        # Otherwise
        else:

            # Default AI
            return self.no_ai()

    def move_shoot(self, left: bool):
        '''
        To encompass both move_left and shoot, and move_right and shoot action
        from Original Space Invaders Gym Environment
        '''

        # If left
        if left:

            # Move left
            self.move_left()

        # Otherwise
        else:

            # Move right
            self.move_right()

        # Return shoot function
        return self.shoot

    def get_action_space(self) -> tuple:
        """List of actions that the player can take (tuple of functions)"""
        return (self.shoot, self.move_left, self.move_right, lambda: 1, self.move_shoot(True),
                self.move_shoot(False))

    def draw(self, screen):
        """Draw the object
            Assign screen object if it is not done previously
        """

        # If there is no screen
        if not self.screen:
            # Set the screen
            self.screen = screen

        # Call the superclass draw
        super().draw(screen)

    def get_entities(self, enemies1, enemies2, enemy_bullets, enemy_player=[], player_bullets=[]):
        ''' Relevent Information for AI decision making'''
        curr_x = self.get_x()
        curr_y = self.get_y()
        enemy1 = list(
            map(lambda y: (y.get_x(), y.get_y()), filter(lambda x: (np.abs(x.get_x() - curr_x) <= 50), enemies1)))
        enemy2 = list(
            map(lambda y: (y.get_x(), y.get_y()), filter(lambda x: np.abs(x.get_x() - curr_x) <= 50, enemies2)))
        eb = list(
            map(lambda y: (y.get_x(), y.get_y()), filter(lambda x: np.abs(x.get_x() - curr_x) <= 50, enemy_bullets)))
        if self.boss:
            enemy1 = []
            enemy2 = []
            eb = []
        if enemy_player == []:
            ep = 'None'

        elif np.abs(enemy_player.get_x() - curr_x) > 50:
            ep = 'None'
            player_b = list(map(lambda y: (y.get_x(), y.get_y()),
                                filter(lambda x: np.abs(x.get_x() - curr_x) <= 50, player_bullets)))
            eb.extend(player_b)
        else:
            ep = (enemy_player.get_x(), enemy_player.get_y())
            player_b = list(map(lambda y: (y.get_x(), y.get_y()),
                                filter(lambda x: np.abs(x.get_x() - curr_x) <= 50, player_bullets)))
            eb.extend(player_b)

        environment_status = {'mobs': enemy1, 'bosses': enemy2, 'bullets': eb, 'enemy_player': ep,
                              'player': (curr_x, curr_y, self.life)}

        # Set state stored in AI for
        self.state = environment_status

    def has_screen(self) -> bool:
        """Detect if screen does not exist"""
        return self.screen != None
