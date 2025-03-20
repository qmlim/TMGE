from abc import ABC, abstractmethod
import tkinter as tk
from State import State


class Game(ABC):
    path: str

    def __init__(self, playerList, parent, mainMenuFrame=None, showFrameFunc=None):
        self.playerList = playerList
        self.parent = parent
        self.mainMenuFrame = mainMenuFrame
        self.showFrameFunc = showFrameFunc
        self.gameState = State.INITIALIZED
        self.frame = tk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.gameGridType = None

        
    def gameSetUp(self):
        self.generateGridFrame()
        self.handleInput()
        self.backButton()
        return self.frame
    
    def generateGridFrame(self):
        for i in range(self.gameGridType.height):
            for j in range(self.gameGridType.width):
                tk.Button(self.frame, text=" ", width=2).grid(row=i, column=j)
        return self.frame

    def backButton(self):
        backButton = tk.Button(self.frame, text="Back To Menu", command=self.backToMenu)
        backButton.grid(row=self.gameGridType.height + 1, column=0, columnspan=self.gameGridType.width, pady=10)

    def backToMenu(self):
        self.frame.destroy()
        self.showFrameFunc(self.mainMenuFrame)

    @abstractmethod
    def gamePlay(self):
        pass

    @abstractmethod
    def ruleChecking(self):
        pass

    @abstractmethod
    def handleInput(self):
        pass