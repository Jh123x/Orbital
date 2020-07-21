from . import PlayScreen
from .. import State, Difficulty

class StoryTemplate(PlayScreen):

    #Store the sprites to be used for stories
    sprites = []

    def __init__(self, screen_width:int, screen_height:int, screen, state:State, sensitivity:int, max_fps:int, debug:bool):
        """The template for the stage to be built on"""

        #Call the superclass
        super().__init__(screen_width, screen_height, screen, sensitivity, max_fps, Difficulty(3), 1, 1, 1, debug)

        #Set the state
        self.set_state(state)

        #Reset the game
        self.reset()

    def reset(self):
        """Reset the state of the game"""

        #Reset the flag to play the cutscenes
        self.curr = 0

        #Call the superclass reset
        return super().reset()
    
    def next_scene(self):
        """Increment the scene counter to the next scene"""
        self.curr += 1

    def win_condition(self) -> bool:
        """Check if the player has won"""
        raise NotImplementedError("Please override this method")

    def get_stage_name(self):
        """Get the name of the stage"""
        return f"Stage {self.state.value - 100}"

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

    def handle(self):
        """Handles the playing out of the screen"""

        #If player is destroyed or enemies hit the bottom, go to gameover state
        if self.player1.is_destroyed() or self.enemy_touched_bottom():

            #Cause the game to end
            self.reset()

            #Return the gameover state
            return self.get_gameover_state()

        #Otherwise if player wins
        elif self.win_condition():

            #Go to victory screen
            return self.get_victory_state()

        #If it is the pre_cutscene stage
        if self.curr == 0:
            return self.pre_cutscene()

        #If it is the play state
        elif self.curr == 1:
            return self.play()

        #If it is the post_cutscene state
        else:
            return self.post_cutscene()


    

