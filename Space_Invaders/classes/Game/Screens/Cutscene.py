from .. import State
from . import Screen


class Cutscene(Screen):
    def __init__(self, screen_width:int, screen_height:int, state:State, screen, prev_state:State, next_scene:Cutscene = None):
        """Base constructor for the cutscene class"""

        #Call the superclass (With top left corner at 0, 0)
        super().__init__(self, screen_width, screen_height, state, screen, 0, 0)

        #Store the previous state
        self.prev_state = prev_state
        
        #Store the next screen
        self.next_scene = next_scene

    def get_prev_state(self) -> State:
        """Get the previous state"""
        return self.prev_state

    def get_next_scene(self) -> Cutscene:
        """Return the next cutscene"""
        return self.next_scene

    def update(self) -> None:
        """Update the screen"""
        return super().update()


    

