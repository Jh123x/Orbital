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

    #Quitting states
    QUIT = -1
    NONE = None

    #Menu States
    MENU = 1
    PLAYMODE = 2
    SETTINGS = 3
    TUTORIAL = 4
    VICTORY = 5
    ONE_PLAYER_MENU = 6

    #Highscore states
    HIGHSCORE = 8
    NEWHIGHSCORE = 9
    
    #Instruction states
    INSTRUCTIONS_MENU = 40
    INSTRUCTIONS = 41
    PVP_INSTRUCTIONS = 42
    AI_VS_INSTRUCTIONS = 43
    AI_COOP_INSTRUCTIONS = 44
    
    #Two player states
    TWO_PLAYER_MENU = 10

    AI_COOP = 11
    AI_COOP_GAMEOVER  = 12

    AI_VS = 14
    AI_VS_GAMEOVER = 15

    PVP = 16
    COOP = 17

    TWO_PLAYER_GAMEOVER = 18
    TWO_PLAYER_PAUSE = 19

    #Single player states
    PLAY = 30
    GAMEOVER = 31
    PAUSE = 32
    STORY_MENU = 33
    CLASSIC = 34
    ONLINE = 35

class Difficulty_enum(enum.Enum):
    """Difficulty enum to hold the difficultly of the game"""
    CASUAL = 1
    EASY = 2
    MEDIUM = 3
    HARD = 4
    IMPOSSIBLE = 5
    OUTRAGEOUS = 6