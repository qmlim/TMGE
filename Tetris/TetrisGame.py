from Game import Game 
from Tetris.TetrisGrid import TetrisGrid
import tkinter as tk


class TetrisGame(Game):
    def __init__(self, playerList, parent):
        super().__init__(playerList, parent)
        self.grid = TetrisGrid()

    def handleInput():
        pass