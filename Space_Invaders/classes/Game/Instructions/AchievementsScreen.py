from . import PowerupInstructionsScreen
from .. import VictoryScreen, State, WHITE, ImageObject

class AchievementScreen(PowerupInstructionsScreen):
    
    description = {
        'A new low....': "Lose in a gamemode where it is almost impossible to lose",
        'Back from the Grave': "",
        'One small step for Man...': "Take back the Moon from the enemies",
        'Mars Colony': "Retake Mars for humanity",
        'Beat them Back': "",
        'Sk-...Cloud Net !!??': "Complete the Storyline to discover the truth",
        'The First taste of Victory': "Win a game",
        'Hero of Humanity': "Save humanity by killing aliens",
        'Are you a Monster??': "How did you even get this?",
        'Space Defender': "Defend space from the aliens",
        'Master of Space Invaders': "Did you just master the game?",
        'Coop King' : "King of Coop",
        "No, I'm the Space Defender!": "There can only be 1 true space defender",
        "I’ll Be Back": "",
        'Am I getting Replaced?': "Getting replaced 101",
    }

    def __init__(self, screen_width:int, screen_height:int, screen, fps, achievement_tracker, debug:bool = False):
        """Constructor for the powerup instructions screen"""

        #Store the achievement tracker
        self.tracker = achievement_tracker

        #Dict to see if the achievement is achieved
        self.refresh()

        #Render the image
        self.trophy = ImageObject(screen_width//2, screen_height//5 + screen_height // 15, 50, 50, VictoryScreen.sprites[1], debug)
        self.question_mark = ImageObject(screen_width//2, screen_height//5 + screen_height // 15, 50, 50, VictoryScreen.sprites[0], debug)

        #Call the superclass
        super().__init__(screen_width, screen_height, screen, fps, debug)

        #Set current state
        self.set_state(State.ACHIEVEMENTS)

    def preprocess(self):
        """Load other variables which will be used later"""
        
        #Load the achievements on the screen
        self.items = tuple(map(lambda x: (x, self.trophy if self.achieved[x] else self.question_mark), self.description.keys()))

        #Load the current page
        self.page = 1
        self.total_pages = len(self.items) - 1

    def refresh(self):
        """Refresh the stats"""
        self.achieved = self.tracker.get_all_achievements()

    def write_lines(self):
        """Write the header"""

        #Draw the header
        self.header = self.write(self.title_font, WHITE, "Achievements", self.screen_width//2, self.screen_height//5)

        #Draw the back button
        self.back = self.write(self.end_font, WHITE, "Back", self.screen_width//2, self.screen_height//1.2)

        #Write data onto the main screen
        self.main_write()

    def _back(self):
        """Override the superclass method"""
        super()._back()
        return State.MENU

    def main_write(self):
        """Writing the main information onto the screen"""

        #First pixel used for alignment
        first_px = self.screen_height//5 + self.screen_height // 15 + 50

        #Unpack powerup sprites
        name,img = self.items[self.page]

        #Draw the powerups name
        self.write_main(self.end_font, WHITE, f"{name}", self.screen_width // 2, first_px)

        #Draw the description
        self.insert_description(first_px, self.description[name])
        
        #Draw the icon
        img.draw(self.screen)

        #Draw page related items
        self.draw_pages()
