try:
    from .Screens import Screen
    from .Enums import State, Direction
    from .Colors import WHITE
except ImportError:
    from Screens import Screen
    from Enums import State, Direction
    from Colors import WHITE
    

class HighscoreScreen(Screen):
    def __init__(self, game_width:int, game_height:int, screen:int, scores:tuple, debug:bool = False):
        """Constructor for the Highscore screen"""
        #Keep track of the scores
        self.scores = sorted(scores, key = lambda x: x[-1], reverse = True)
        self.removed = []

        #Call the superclass
        super().__init__(game_width, game_height, State.HIGHSCORE, screen)

        #Draw the sprite
        self.draw()

    def update_score(self, name, score):
        """Update the new player into the score board"""

        #Add the score to the score board
        self.scores.append((None, name,score))

        #Sort the scores
        self.sort_scores()

        #Remove the other scores while there are more than 5 of them
        if len(self.scores) > 5:
            self.removed.append(self.scores.pop())

        #Redraw the sprites
        self.draw()
        
    def sort_scores(self):
        """Sort the scores"""
        self.scores.sort(key = lambda x: x[-1], reverse = True)

    def beat_highscore(self, score):
        """Check if the highscore was beaten"""
        return len(self.scores) < 5 or score > self.scores[4][-1]

    def get_scores(self) -> list:
        """Get the high score list"""
        return self.scores

    def get_removed(self) -> list:
        """Get a list of people removed from the database"""
        return self.removed

    def draw(self) -> None:

        #Reset the screen
        super().reset()

        #Start pixel to print the score
        start_px = 200

        #Draw the button for back
        self.end_rect = self.write(Screen.end_font, WHITE, "Back", self.game_width//2, self.game_height//2 + self.game_height//3)

        #Draw the highscore header
        self.write(Screen.title_font, WHITE, f"HIGH SCORES", self.game_width//2, 100)

        #Draw the scores of the players
        for index, item in enumerate(self.scores[:5]):

            #Draw the first half of the scoreboard
            self.write(Screen.end_font, WHITE, f"{index+1}. {item[1]}".ljust(15, ' '), self.game_width//4, start_px + self.game_height//(15/(index+1)),Direction.LEFT)

            #Draw the 2nd half of the scoreboard
            self.write(Screen.end_font, WHITE, f"{item[2]:<5}",self.game_width//1.6, start_px + self.game_height//(15/(index+1)),Direction.LEFT)

    def handle(self) -> State:
        """Handles the drawing of the highscore screen"""

        #Update itself
        self.update()

        #Check for click
        if self.check_clicked(self.end_rect):
            return State.MENU
        else:
            return State.HIGHSCORE