from enum import Enum

class State(Enum):
    INITIALIZED = "INITIALIZED",
    RUNNING = "RUNNING",
    PAUSED = "PAUSED",
    GAME_OVER = "GAME_OVER"