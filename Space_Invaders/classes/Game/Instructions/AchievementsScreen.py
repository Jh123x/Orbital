from . import PowerupInstructionsScreen
from .. import VictoryScreen, State, WHITE, ImageObject


class AchievementScreen(PowerupInstructionsScreen):
    description = {
        'A new low....': "Lose in a gamemode where it is almost impossible to lose",
        'Back from the Grave': "The hero is back in the making",
        'One small step for Man...': "Take back the Moon from the enemies",
        'Mars Colony': "Retake Mars for humanity",
        'Beat them Back': "Beat them past the belt",
        'Sk-...Cloud Net !!??': "Complete the Storyline to discover the truth",
        'The First taste of Victory': "Kill some aliens. Cant be too hard",
        'Hero of Humanity': "Holy smokes thats alot of aliens you killed",
        'Are you a Monster??': "How did you even get this?",
        'Space Defender': "Aren't you a master of the game",
        'Master of Space Invaders': "Are you one of them OG players?",
        'Coop King': "What can I say at least try to make friends through the game.",
        "No, I'm the Space Defender!": "There can only be 1 true space defender",
        "I’ll Be Back": "Guess who will be coming back for revenge",
        'Am I getting Replaced?': "Are you getting replaced??"
    }

    def __init__(self, screen_width: int, screen_height: int, screen, fps, achievement_tracker, debug: bool = False):
        """Constructor for the powerup instructions screen"""

        # Render the image
        self.trophy = ImageObject(screen_width // 2, screen_height // 5 + screen_height // 15, 50, 50,
                                  VictoryScreen.sprites[1], debug)
        self.question_mark = ImageObject(screen_width // 2, screen_height // 5 + screen_height // 15, 50, 50,
                                         VictoryScreen.sprites[0], debug)

        # Store the achievement tracker
        self.tracker = achievement_tracker

        #Check if it is refreshed
        self.refreshed = False

        # Dict to see if the achievement is achieved
        self.refresh()

        # Call the superclass
        super().__init__(screen_width, screen_height, screen, fps, debug)

        # Set current state
        self.set_state(State.ACHIEVEMENTS)

    def preprocess(self):
        """Load other variables which will be used later"""

        # Load the achievements on the screen
        self.items = tuple(
            map(lambda x: (x, self.trophy if self.achieved[x] else self.question_mark), self.description.keys()))

        # Load the current page
        self.page = 1
        self.total_pages = len(self.items)

    def refresh(self):
        """Refresh the stats"""
        if not self.refreshed:
            self.achieved = self.tracker.get_all_achievements()
            self.preprocess()
            self.refreshed = True

    def write_lines(self):
        """Write the header"""

        # Draw the header
        self.header = self.write(self.title_font, WHITE, "Achievements", self.screen_width // 2,
                                 self.screen_height // 5)

        # Draw the back button
        self.back = self.write(self.end_font, WHITE, "Back", self.screen_width // 2, self.screen_height // 1.2)

        # Write data onto the main screen
        self.main_write()

    def _back(self):
        """Override the superclass method"""
        super()._back()
        self.refreshed = False
        return State.MENU

    def main_write(self):
        """Writing the main information onto the screen"""

        #Refresh stats
        self.refresh()

        # First pixel used for alignment
        first_px = self.screen_height // 5 + self.screen_height // 15 + 50

        # Unpack powerup sprites
        name, img = self.items[self.page - 1]

        # Draw the powerups name
        self.write_main(self.end_font, WHITE, f"{name}", self.screen_width // 2, first_px)

        # Draw the description
        self.insert_description(first_px, self.description[name])

        # Draw the icon
        img.draw(self.screen)

        # Draw page related items
        self.draw_pages()
