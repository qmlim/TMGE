from abc import ABC, abstractmethod
from InputHandler import InputHandler

class Game(ABC):
    def __init__(self, playerList):
        self.playerList = playerList

    @abstractmethod
    def generateGrid():
        pass
    
    @abstractmethod
    def handleInput():
        pass