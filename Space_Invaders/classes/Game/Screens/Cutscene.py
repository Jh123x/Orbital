import pygame
import cv2
from .. import State
from . import Screen

class VideoCutscene(Screen):
    def __init__(self, screen_width:int, screen_height:int, screen, prev_state:State, video_path:str, next_scene = None):
        """Base constructor for the Cutscene class"""

        #Call the superclass (With top left corner at 0, 0)
        super().__init__(screen_width, screen_height, State.VID_CUTSCENE, screen, 0, 0)

        #Store the video path
        self.video_path = video_path

        #Store the previous state
        self.prev_state = prev_state
        
        #Store the next screen
        self.next_scene = next_scene

    def play(self) -> None:
        """Load and play the video"""

        #Store the player
        self.player = cv2.VideoCapture(f"{self.video_path}")

        #Running loop
        while self.player.isOpened():

            #Check if the user wants to quit
            if self.check_quit():
                running = False
            
            #Read from the video input
            ret, img = self.player.read()

            #If there is no image break out of the loop
            if type(img) == type(None):
                break

            #Resize image to fit frame
            height, width = img.shape[:2]
            res = cv2.resize(img, (self.screen_width, self.screen_height), interpolation = cv2.INTER_AREA)

            #Transpose the image
            img = cv2.transpose(res)
            
            #Blit directly on screen         
            pygame.surfarray.blit_array(self.screen, img)
            pygame.display.update()

        #Close the player
        self.player.release()

        #Close all cv2 windows
        cv2.destroyAllWindows()

        #Return the prev state
        return self.get_prev_state()

    def get_prev_state(self) -> State:
        """Get the previous state"""
        return self.prev_state

    def get_next_scene(self):
        """Return the next cutscene"""
        return self.next_scene

    def update(self) -> None:
        """Update the screen"""
        return super().update()


    

