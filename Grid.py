from abc import ABC, abstractmethod

class Grid(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def updateGrid(self):
        pass

    @abstractmethod
    def isEmpty(self):
        pass