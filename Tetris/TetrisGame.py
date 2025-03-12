from Game import Game 
from Tetris.TetrisGrid import TetrisGrid
import tkinter as tk


class TetrisGame(Game):
    def __init__(self, playerList, parent):
        super().__init__(playerList)
        self.grid = TetrisGrid()
        self.frame = tk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew")

    def generateGrid(self):
        for i in range(self.grid.height):
            for j in range(self.grid.width):
                tk.Button(self.frame, text=" ", width=2).grid(row=i, column=j)
        return self.frame

    def handleInput():
        pass