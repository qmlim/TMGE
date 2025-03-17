from abc import ABC, abstractmethod
import tkinter as tk
from State import State


class Game(ABC):
    path: str

    def __init__(self, playerList, parent):
        self.playerList = playerList
        self.parent = parent
        self.gameState = State.RUNNING
        self.gameGridType = None

    @abstractmethod
    def gameSetUp(self):
        pass

    @abstractmethod
    def gamePlay(self):
        pass

    @abstractmethod
    def ruleChecking(self):
        pass

    @abstractmethod
    def handleInput(self):
        pass