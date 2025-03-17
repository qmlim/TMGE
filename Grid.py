from abc import ABC, abstractmethod

class Grid(ABC):
    def __init__(self, width, height):
        self. width = width
        self.height = height

    @abstractmethod
    def updateGrid(self):
        pass

    @abstractmethod
    def isEmpty(self):
        pass

    @abstractmethod
    def clearRows(self):
        pass

    @abstractmethod
    def clearColumns(self):
        pass

    @abstractmethod
    def updateTilePositions(self):
        pass