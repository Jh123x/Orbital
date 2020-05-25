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
    SETTINGS = 8
    PLAYMODE = 9
    TWO_PLAYER_MENU = 10
    AI_COOP = 11
    AI_COOP_GAMEOVER  = 12
    AI_VS = 13
    AI_VS_GAMEOVER = 14
    PVP = 15
    PVP_GAMEOVER = 16
    QUIT = -1
    NONE = None

class Difficulty(enum.Enum):
    """Difficulty enum to hold the difficultly of the game"""
    CASUAL = 1
    EASY = 2
    MEDIUM = 3
    HARD = 4
    IMPOSSIBLE = 5