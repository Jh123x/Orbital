try:
    from .Screens import Screen
    from .Enums import State, Direction
    from .Colors import WHITE
except ImportError:
    from Screens import Screen
    from Enums import State, Direction
    from Colors import WHITE
    

class HighscoreScreen(Screen):
    def __init__(self, game_width:int, game_height:int, screen, scores:tuple, debug:bool = False):
        """Constructor for the Highscore screen
            Arguments:
                game_width: Width of the game window (int)
                game_height: Height of the game window (int)
                screen: Surface for the screen to blit to (pygame.Surface)
                scores: List of 5 top scores recorded (tuple of tuple)
                debug: Toggle whether the screen is in debug mode (bool): default = False

            Methods:
                update_score: Update the player and the score into the highscore screen
                sort_scores: Sort the scores recorded
                beat_highscore: Check if the score has made it into the highscore
                get_scores: Get a list of the highscore
                get_removed: Get a list of entries that dropped out of the highscore screen
                draw: Draw the highscore screen onto a surface
                handle: Handles the drawing and processes of the highscore screen
        """
        #Keep track of the scores added
        self.scores = sorted(scores, key = lambda x: x[-1], reverse = True)

        #Keep track of the scores removed
        self.removed = []

        #Call the superclass
        super().__init__(game_width, game_height, State.HIGHSCORE, screen, debug)

        #Draw the sprite
        self.draw()

    def update_score(self, name:str, score:int) -> None:
        """Update the new player's name and score into the score board
            Arguments:
                name: Name of the player (str)
                score: Score of the player (int)
            Returns:
                No return
        """

        #Add the score to the score board
        self.scores.append((None, name,score))

        #Sort the scores
        self.sort_scores()

        #Remove the other scores while there are more than 5 of them
        while len(self.scores) > 5:
            self.removed.append(self.scores.pop())

        #Redraw the sprites
        self.draw()
        
    def sort_scores(self) -> None:
        """Sort the scores stored internally
            Arguments:
                No arguments
            Returns:
                No returns
        """
        self.scores.sort(key = lambda x: x[-1], reverse = True)

    def beat_highscore(self, score:int) -> bool:
        """Check if the highscore was beaten
            Arguments:
                Score: Score to compare (int)
            Returns:
                A boolean indicating if it is a new highscore (bool)
        """
        return len(self.scores) < 5 or score > self.scores[-1][-1]

    def get_scores(self) -> list:
        """Get the high score list
            Arguments:
                No arguments
            Returns: 
                Returns a list of the highscore (list)
        """
        return self.scores

    def get_removed(self) -> list:
        """Get a list of people removed from the database
            Arguments:
                No arguments
            Returns:
                Returns a list of players removed from the highscore (list)
        """
        return self.removed

    def draw(self) -> None:
        """Draws the highscore screen onto the predefined surface
            Arguments:
                No arguments
            Returns:
                No returns
        """
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
        """Handles the drawing of the highscore screen
            Arguments:
                No arguments
            Returns: 
                The next state the game is suppose to be in (State)
        """

        #Update itself
        self.update()

        #Check if the back button is clicked
        if self.check_clicked(self.end_rect):

            #Return the menu state
            return State.MENU

        #Otherwise
        else:
            
            #Return the current state
            return State.HIGHSCORE