import pygame
import cv2
from .. import State
from . import Screen

class Cutscene(Screen):
    def __init__(self, screen_width:int, screen_height:int, state:State, screen, prev_state:State, video_path:str = None, next_scene = None):
        """Base constructor for the Cutscene class"""

        #Call the superclass (With top left corner at 0, 0)
        super().__init__(self, screen_width, screen_height, state, screen, 0, 0)

        #Store the video path
        self.video_path = video_path

        #Store the previous state
        self.prev_state = prev_state
        
        #Store the next screen
        self.next_scene = next_scene

    def play(self) -> None:
        """Load and play the video"""

        #Store the player
        self.player = cv2.VideoCapture(self.video_path)

        #Check the first frame
        frame,ret = self.player.read()

        #Ret
        if not ret:

            #Assert an error
            assert False, f"Problem with {self.video_path}"

        #Running loop
        while True:

            #Check if the user wants to quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            #Read from the video input
            ret, img = self.player.read()

            #Transpose the image
            img = cv2.transpose(img)
            
            #Blit directly on screen         
            pygame.surfarray.blit_array(self.screen, img)

        return


    def get_prev_state(self) -> State:
        """Get the previous state"""
        return self.prev_state

    def get_next_scene(self):
        """Return the next cutscene"""
        return self.next_scene

    def update(self) -> None:
        """Update the screen"""
        return super().update()


    

