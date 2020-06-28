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
    QUIT = -1
    NONE = None

    MENU = 1
    PLAYMODE = 2
    SETTINGS = 3

    PLAY = 20
    GAMEOVER = 21
    PAUSE = 22
    NEWHIGHSCORE = 23

    HIGHSCORE = 30
    
    INSTRUCTIONS_MENU = 40
    INSTRUCTIONS = 41
    PVP_INSTRUCTIONS = 42
    AI_VS_INSTRUCTIONS = 43
    AI_COOP_INSTRUCTIONS = 44
    
    TWO_PLAYER_MENU = 10
    AI_COOP = 11
    AI_COOP_GAMEOVER  = 12

    AI_VS = 14
    AI_VS_GAMEOVER = 15

    PVP = 16
    TWO_PLAYER_GAMEOVER = 17
    TWO_PLAYER_PAUSE = 18

    COOP = 19

    CLASSIC = 60
    STORY_MENU = 70
    ONLINE = 90

class Difficulty_enum(enum.Enum):
    """Difficulty enum to hold the difficultly of the game"""
    CASUAL = 1
    EASY = 2
    MEDIUM = 3
    HARD = 4
    IMPOSSIBLE = 5