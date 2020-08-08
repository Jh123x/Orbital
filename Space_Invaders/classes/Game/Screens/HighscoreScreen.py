from . import MenuTemplate
from .. import State, WHITE, Direction

class HighscoreScreen(MenuTemplate):
    def __init__(self, screen_width:int, screen_height:int, screen, scores:tuple, debug:bool = False):
        """Constructor for the Highscore screen"""

        #Keep track of the scores added
        self.scores = sorted(scores, key = lambda x: x[-1], reverse = True)

        #Keep track of the scores removed
        self.removed = []

        #Call the superclass
        super().__init__(screen_width, screen_height, State.HIGHSCORE, screen, debug)

    def update_score(self, name:str, score:int) -> None:
        """Update the new player's name and score into the score board"""

        #Add the score to the score board
        self.scores.append((None, name, score))

        #Sort the scores
        self.sort_scores()

        #Redraw the sprites
        self.draw()
        
    def sort_scores(self) -> None:
        """Sort the scores stored internally"""

        #Sort the score
        self.scores.sort(key = lambda x: x[-1], reverse = True)

        #Remove the other scores while there are more than 5 of them
        while len(self.scores) > 5:
            self.removed.append(self.scores.pop())

    def beat_highscore(self, score:int) -> bool:
        """Check if the highscore was beaten"""
        return len(self.scores) < 5 or score > self.scores[-1][-1]

    def get_scores(self) -> tuple:
        """Get the high score list"""
        return tuple(self.scores)

    def get_removed(self) -> tuple:
        """Get a list of people removed from the database"""
        return tuple(self.removed)

    def write_lines(self) -> None:
        """Draws the highscore screen onto the predefined surface"""
        #Reset the screen
        super().reset_surface()

        #Start pixel to print the score
        start_px = 200

        #Draw the button for back
        self.end_rect = self.write(self.end_font, WHITE, "Back", self.screen_width//2, self.screen_height//2 + self.screen_height//3)

        #Draw the highscore header
        self.write(self.title_font, WHITE, f"High Scores", self.screen_width//2, 100)

        #Draw the scores of the players
        for index, item in enumerate(self.scores[:5]):

            #Draw the first half of the scoreboard
            self.write(self.end_font, WHITE, f"{index+1}. {item[1]}".ljust(15, ' '), self.screen_width//4, start_px + self.screen_height//(15/(index+1)),Direction.LEFT)

            #Draw the 2nd half of the scoreboard
            self.write(self.end_font, WHITE, f"{item[2]:<5}",self.screen_width//1.6, start_px + self.screen_height//(15/(index+1)),Direction.LEFT)


    def get_rects(self):
        """Get the rects in the highscore screen"""
        return (self.end_rect,)

    def get_effects(self):
        """Get the effects of the rect in the highscore screen"""
        return (State.MENU,)