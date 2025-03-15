from abc import ABC, abstractmethod

class ScoreSystem(ABC):
    def __init__(self, points):
        self.points = points

    @abstractmethod
    def calculateGameScore(self):
        pass
    
    @abstractmethod
    def updateScore(self):
        pass

    @abstractmethod
    def updatePlayerScore(self):
        pass