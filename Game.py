from abc import ABC, abstractmethod
import tkinter as tk


class Game(ABC):
    path: str

    def __init__(self, playerList, parent):
        self.playerList = playerList
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.grid = None

    def gameSetUp(self):
        self.generateGridFrame()
        self.handleInput()
        return self.frame

    def generateGridFrame(self):
        for i in range(self.grid.height):
            for j in range(self.grid.width):
                tk.Button(self.frame, text=" ", width=2).grid(row=i, column=j)
        return self.frame
    
    @abstractmethod
    def handleInput():
        pass