import enum

class Direction(enum.Enum):
    """Direction enum to store where objects are moving"""
    UP = 1
    DOWN = -1
    LEFT = -2
    RIGHT = 2
    CENTER = 0

class State(enum.Enum):
    """State enum to keep track of the state of the game"""
    MENU = 1
    PLAY = 2
    GAMEOVER = 3
    PAUSE = 4
    HIGHSCORE = 5
    NEWHIGHSCORE = 6
    INSTRUCTIONS = 7
    QUIT = -1

class Difficulty(enum.Enum):
    """Difficulty enum to hold the difficultly of the game"""
    CASUAL = 1
    EASY = 2
    MEDIUM = 3
    HARD = 4
    IMPOSSIBLE = 5