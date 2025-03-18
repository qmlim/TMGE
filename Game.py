from abc import ABC, abstractmethod
import tkinter as tk
from State import State


class Game(ABC):
    path: str

    def __init__(self, playerList, parent, mainMenuFrame, showFrame):
        self.playerList = playerList
        self.parent = parent
        self.mainMenuFrame = mainMenuFrame
        self.showFrame = showFrame
        self.gameState = State.INITIALIZED
        self.frame = tk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.gameGridType = None

    # @abstractmethod
    # def gameSetUp(self):
    #     pass
        
    def gameSetUp(self):
        self.generateGridFrame()
        self.handleInput()
        return self.frame
    
    def generateGridFrame(self):
        for i in range(self.gameGridType.height):
            for j in range(self.gameGridType.width):
                tk.Button(self.frame, text=" ", width=2).grid(row=i, column=j)
        return self.frame

    @abstractmethod
    def gamePlay(self):
        pass

    @abstractmethod
    def ruleChecking(self):
        pass

    @abstractmethod
    def handleInput(self):
        pass