from abc import ABC, abstractmethod

class Tile(ABC):
    def __init__(self, tileType, position):
        self.tileType = tileType
        self.position = position

    @abstractmethod
    def updatePosition(self):
        pass