import random

import pygame
from pygame.locals import *

from . import PlayScreen
from .. import *


class TutorialScreen(PlayScreen):
    # Store the information for the tutorial screen
    information = [("a", "move left"), ("d", "move right"), ("spacebar", "shoot"), ("p", "to pause")]

    def __init__(self, screen_width: int, screen_height: int, screen, sensitivity: int, max_fps: int
                 , tracker, debug: bool = False):
        """Main class for the tutorial screen"""

        # Call the superclass
        super().__init__(screen_width, screen_height, screen, sensitivity, max_fps, Difficulty(1), tracker, 1, 1, 1,
                         debug)

        # Set the state to tutorial
        self.set_state(State.TUTORIAL)

        # Set powerups to 100% spawn
        self.set_powerup_chance(1)

        # Reset the game
        self.reset()

    def handle_threshold(self) -> None:
        pass

    def spawn_powerups(self, x: int, y: int) -> None:
        """Spawn a powerup at specified x and y coordinate"""

        # Spawn the powerups
        self.powerups.add(PowerUp(x, y, 50, 50, random.choice(PowerUp.get_powerups()), -1))

        # Increase the number of powerups
        self.powerup_numbers += 1

    def randomly_spawn_mothership(self) -> bool:
        """Spawns a mothership randomly, returns if mothership is spawned"""
        return False

    def reset(self) -> None:
        """Reset the game"""
        self.pressed = [False, False, False, False]

        # Enemyshot variable
        self.enemy_shot = False

        # Track the mob cooldown
        self.cooldown_mob = self.fps
        self.spawn_cooldown = -1

        # Check if any powerups spawned before
        self.pu_show = False

        # Check if mobs spawned
        self.spawned_mobs = False

        # Call the superclass reset
        return super().reset()

    def get_stage_name(self) -> str:
        """Returns the stage name"""
        return "Tutorial"

    def spawn_enemies(self):
        """Spawn the enemies"""

        # If not on spawn cooldown
        if self.spawn_cooldown == 0 and len(self.powerups) == 0:
            # Add 1 enemy ship to the board
            self.enemies.add(
                EnemyShip(self.sensitivity, self.screen_width // 4 + self.screen_width // 10, self.screen_height // 10,
                          self.wave_random(), self.screen_width, self.screen_height, Direction.DOWN, self.mob_bullet,
                          self.debug))

    def spawn_enemy_bullets(self):
        """Spawn bullets for the enemy"""

        # Let the first enemy shoot if there are any enemies
        if len(self.enemies.sprites()) > 0 and self.cooldown_mob == 0:
            # Let the enemy shoot
            self.enemies.sprites()[0].shoot()

            # Set the cooldown for the mob
            self.cooldown_mob = self.fps

        # Get the lower cooldown for the mob
        if self.cooldown_mob > 0:
            # Reduce the cooldown
            self.cooldown_mob -= 1

    def update_keypresses(self) -> None:
        """Check the keypresses of the player"""

        # Get the keys the player pressed
        keys = pygame.key.get_pressed()

        # If the player has click 'Left' or 'a' move the player to the left
        if keys[K_a] or keys[K_LEFT]:
            self.player1.move_left()
            if not self.pressed[0]:
                self.pressed[0] = self.fps // 2

        # If the player has click 'right' or 'd' move the player to the right
        if keys[K_d] or keys[K_RIGHT]:
            self.player1.move_right()
            if not self.pressed[1]:
                self.pressed[1] = self.fps // 2

        # Check if the player pressed spacebar to spawn a bullet
        if keys[K_SPACE]:

            # Make the player shoot
            self.player1.shoot()
            if not self.pressed[2]:
                self.pressed[2] = self.fps // 2

        # If player wants to pause the game
        if keys[K_p]:

            if not self.pressed[3]:
                # Prompt the player to press the pause button
                self.pressed[3] = self.fps // 2

            # Bring player to pause screen
            return True

        # Return False to not pause the game
        return False

    def end_game(self) -> None:
        """Ends the game"""
        # Set the game to be over
        self.over = True

        # Reset the game
        self.reset()

    def update_trackers(self, loss: bool = False):
        super(TutorialScreen, self).update_trackers()
        if loss:
            self.tracker.add_value('tut_n_clr', 1)

    def handle(self) -> State:
        """Handle the drawing of the sprites"""

        # If player is destroyed or enemies hit the bottom, go to gameover state
        if self.player1.is_destroyed() or self.enemy_touched_bottom():

            # Update trackers
            self.update_trackers(True)
            self.tracker.update_achievement()

            # Cause the game to end
            self.end_game()

            # Return the gameover state
            return State.GAMEOVER

        # Otherwise if player wins
        elif self.wave == 3:
            # update internal stats
            self.update_trackers()
            # Cause the game to end
            self.end_game()

            # Go to victory screen
            return State.VICTORY

        # Spawn if there are no enemies
        if all(self.pressed) and not len(self.enemies) and self.spawn_cooldown == 0 and not self.spawned_mobs:
            # Increase the wave number
            self.wave += 1

            # Spawn the aliens
            self.spawn_enemies()

        # Spawn the bullet
        self.spawn_enemy_bullets()

        # Check object collisions
        self.check_collisions()

        # Draw the tutorial label number
        self.write_main(self.font, WHITE, "Tutorial", self.screen_width // 2, 40)

        # Instructions for the player
        for i in range(len(self.pressed)):
            if not self.pressed[i]:
                self.write_main(self.end_font, WHITE, f"Press {self.information[i][0]} to {self.information[i][1]}",
                                self.screen_width // 2, self.screen_height // 2)
                break
            elif self.pressed[i] > 1:
                self.write_main(self.end_font, WHITE, f"Press {self.information[i][0]} to {self.information[i][1]}",
                                self.screen_width // 2, self.screen_height // 2)
                self.pressed[i] -= 1
                break

        # If there are no breaks in the loop
        else:
            if self.spawn_cooldown == -1:
                self.spawn_cooldown = self.fps // 2
            elif self.spawn_cooldown > 0:
                self.spawn_cooldown -= 1

            if self.pu_show or len(self.powerups) > 0:
                if not self.pu_show:
                    self.pu_show = True
                    self.spawn_cooldown = self.fps * 5
                self.write_main(self.end_font, WHITE, f"Collect powerups from aliens", self.screen_width // 2,
                                self.screen_height // 2 + self.screen_height // 15)
                self.write_main(self.end_font, WHITE, f"Shoot the powerups to get it", self.screen_width // 2,
                                self.screen_height // 2)
            else:
                self.write_main(self.end_font, WHITE, f"Avoid the bullets from the alien", self.screen_width // 2,
                                self.screen_height // 2)
                self.write_main(self.end_font, WHITE, f"Kill the alien to win", self.screen_width // 2,
                                self.screen_height // 2 + self.screen_height // 15)

        # Draw the wave number
        self.write_main(self.font, WHITE, f"Wave : {self.wave}", self.screen_width // 2, 15)

        # Draw the score
        self.write_main(self.font, WHITE, f"Score : {self.p1_score}", 10, 10, Direction.LEFT)

        # Draw the live count
        self.write_main(self.font, WHITE, f"Lives : {self.player1.get_lives()}", self.screen_width - 10, 10,
                        Direction.RIGHT)

        # Check the player keypress
        if self.update_keypresses():
            return State.PAUSE

        # Update the moving objs
        self.update()

        # Call superclass handle
        return self.state
