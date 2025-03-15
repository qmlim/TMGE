from abc import ABC, abstractmethod

class RuleSystem(ABC):
    def __init__(self, gameGrid):
        self.gameGrid = gameGrid

    def executeRowsColumnsChecks(self):
        return [self.checkColumns(), self.checkRows()]
    
    @abstractmethod
    def checkColumns():
        pass

    @abstractmethod
    def checkRows():
        pass

