import pygame
from . import PowerupInstructionsScreen
from .. import State, WHITE, ImageObject, Scout, EnemyShip, Crabs, Brute, MotherShip

class MobInstructionsScreen(PowerupInstructionsScreen):

    #Store the sprites
    sprites_dict = {}

    #Store the description
    description = {
        'enemyship': ("Normal Enemy", "The typical foot soldier, the color of the enemy represents its health, randomly shoots bullets"),
        'brute' : ("Brute","Moves straight down, shoots downwards too. They plough through everything in their path"), 
        'scout' : ("Scout", "Moves diagonally from left to right, shoot bullets that moves straight down. Known to juke bullets like a badass"),
        'mothership': ("Mother Ship", "Moves rapidly from left to right at the top of the screen, does not shoot. Sometimes we are not sure what they are doing here"),
        'crabs': ("Crabs", "Moves diagonally and fires bullets diagonally as well. Warning diagonal bullets bounces off the wall"),
        's-net': ("???", "Unknown information about the ship. All we know is that it is controlling all the chaos here")
    }

    def __init__(self, screen_width:int, screen_height:int, screen, fps, debug:bool = False):
        """Main constructor for Mob instruction screen"""

        #Call the superclass constructor
        super().__init__(screen_width, screen_height, screen, fps, debug)

        #Set the current state
        self.set_state(State.MOBS_INSTRUCTIONS)

    def preprocess(self):
        """Load other variables"""

        #Init the sprites
        self.items = (('enemyship', EnemyShip(0, self.screen_width//2, self.screen_height//5 + self.screen_height // 15, 1,  self.screen_width, self.screen_height, None, None, self.debug)), 
                        ('mothership',MotherShip(self.screen_width//2, self.screen_height//5 + self.screen_height // 15, self.screen_width, self.screen_height, 0, self.debug)), 
                        ('brute', Brute(0, self.screen_width//2, self.screen_height//5 + self.screen_height // 15, self.screen_width, self.screen_height, None, self.debug)), 
                        ('scout', Scout(0, self.screen_width//2, self.screen_height//5 + self.screen_height // 15, 1, self.screen_width, self.screen_height, None, self.debug)), 
                        ('crabs', Crabs(0, self.screen_width//2, self.screen_height//5 + self.screen_height // 15, 1,  self.screen_width, self.screen_height, None, self.debug)), 
                        ('s-net', ImageObject(self.screen_width//2, self.screen_height//5 + self.screen_height // 15, 50, 50, self.sprites_dict['unknown'], self.debug)))

        #Load the current page
        self.page = 1
        self.total_pages = len(self.items)
    
    def write_header(self):
        """Write the header"""
        #Draw the header
        self.header = self.write(self.title_font, WHITE, "Enemies", self.screen_width//2, self.screen_height//5)