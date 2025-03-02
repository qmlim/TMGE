from abc import ABC, abstractmethod

class RuleSystem(ABC):
    def __init__(self, currentGrid):
        self.currentGrid = currentGrid

    @abstractmethod
    def checkColumns():
        pass

    @abstractmethod
    def clearColumns():
        pass

    @abstractmethod
    def checkRows():
        pass

    @abstractmethod
    def clearRows():
        pass

    @abstractmethod
    def calculateScore():
        pass