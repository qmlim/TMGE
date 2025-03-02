from abc import ABC, abstractmethod

class Grid(ABC):
    def __init__(self, gameGrid):
        self.gameGrid = gameGrid

    @abstractmethod
    def updateGrid(self):
        pass

    @abstractmethod
    def isEmpty(self):
        pass