from abc import ABC, abstractmethod

class Game(ABC):
    path: str

    def __init__(self, playerList):
        self.playerList = playerList

    @abstractmethod
    def generateGrid():
        pass
    
    @abstractmethod
    def handleInput():
        pass