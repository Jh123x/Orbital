from .. import PlayScreen, State, Difficulty, Direction, WHITE, AchievmentTracker


class StoryTemplate(PlayScreen):
    # Store the sprites to be used for stories
    sprites_dict = {}

    def __init__(self, screen_width: int, screen_height: int, screen, state: State, sensitivity: int, max_fps: int,
                 powerup_chance: float, tracker: AchievmentTracker, debug: bool):
        """The template for the stage to be built on"""
        self.something = state

        # Call the superclass
        super().__init__(screen_width, screen_height, screen, sensitivity, max_fps, Difficulty(3), tracker, 1, 1,
                         powerup_chance, debug)

        # Set the state
        self.set_state(state)

        # Reset the game
        self.reset()

    def fetch_stats(self, keys: tuple = None):
        if not keys:
            keys = ('ek_e', 'en_k', 'el_k', 'pu', 'sf', f'st_{self.get_stage()}_clr')

        return super().fetch_stats(keys)

    def handle_threshold(self) -> None:
        pass

    def draw_letters(self) -> None:
        """Draw the letters on the screen"""
        # Draw the score
        self.write_main(self.font, WHITE, self.get_stage_name(), 10, 10, Direction.LEFT)

        # Draw the live count
        self.write_main(self.font, WHITE, f"Lives : {self.player1.get_lives()}", self.screen_width - 10, 10,
                        Direction.RIGHT)

        # Draw the wave number
        self.write_main(self.font, WHITE, f"Wave : {self.wave}", self.screen_width // 2, 15)

    def reset(self) -> None:
        """Reset the state of the game"""
        # Set the state
        self.set_state(self.something)

        # Set the number of clicks to 0
        self.clicks = 0

        # Set the cooldown to max
        self.click_cd = self.fps // 5

        # Reset the flag to play the cutscenes
        self.curr = 0

        # Call the superclass reset
        return super().reset()

    def render_speech(self, first_px: int, left_px: int, speech: tuple) -> None:
        """Render the speech onto the screen"""

        # Loop through the speech
        for index, text in enumerate(speech):

            # Break if the speech is more than 6 lines
            if index == 6:
                break

            # Render the speech in 15 spaces
            self.write_main(self.font, WHITE, text, left_px, first_px + index * 15, Direction.LEFT)

    def next_scene(self):
        """Increment the scene counter to the next scene"""
        self.curr += 1

    def win_condition(self) -> bool:
        """Check if the player has won"""
        raise NotImplementedError("Please override this method")

    def get_stage(self) -> int:
        """Return the stage number"""
        return self.state.value - 99

    def get_stage_name(self):
        """Get the name of the stage"""
        return f"Stage {self.get_stage()}"

    def pre_cutscene(self):
        """Plays the precutscene for the story"""
        raise NotImplementedError("Please override the pre_cutscene method")

    def post_cutscene(self):
        """Plays the postcutscene for the story"""
        raise NotImplementedError("Please override the post_cutscene method")

    def play(self):
        """Stage where the player plays the game"""
        return super().handle()

    def get_victory_state(self):
        """Get the state of the game when the player wins"""
        return State.VICTORY

    def get_pause_state(self):
        """Get the pause state of the stages"""
        return State.STAGE_PAUSE

    def get_gameover_state(self):
        """Get the state of the game when the player loses"""
        return State.STAGE_GAMEOVER

    def comparator(self):
        """Variable used for comparison"""
        return self.get_stage()

    def update_trackers(self, win=False):
        '''
        If there is a win, add one to the clear state and continue normally with tracked stats
        '''
        if win:
            self.accumulate(f'st_{self.get_stage()}_clr', 1)

        return super().update_trackers()

    def handle(self):
        """Handles the playing out of the screen"""

        # If player is destroyed or enemies hit the bottom, go to gameover state
        if self.player1.is_destroyed() or self.enemy_touched_bottom():

            # Cause the game to end
            self.reset()

            # update the statistic values
            self.update_trackers()

            # Return the gameover state
            return self.get_gameover_state()

        # Otherwise if player wins
        elif self.win_condition():
            self.update_trackers(True)
            # Go to next state
            self.next_scene()

            self.wave = 0

        # If it is the pre_cutscene stage
        if self.curr == 0:
            return self.pre_cutscene()

        # If it is the play state
        elif self.curr == 1:
            return self.play()

        # If it is the post_cutscene state
        else:
            return self.post_cutscene()
