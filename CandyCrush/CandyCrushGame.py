from Game import Game 
from CandyCrush.CandyCrushGrid import CandyCrushGrid
import tkinter as tk


class CandyCrushGame(Game):
    def __init__(self, playerList, parent):
        super().__init__(playerList, parent)
        self.grid = CandyCrushGrid()

    def handleInput():
        pass