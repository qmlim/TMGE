import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Tetris.TetrisRules import TetrisRules
from Game import Game 
from Tetris.TetrisGrid import TetrisGrid
import tkinter as tk
from State import State


class TetrisGame(Game):
    def __init__(self, playerList, parent):
        super().__init__(playerList, parent)
        self.gameGridType = TetrisGrid()
        self.rules = TetrisRules(self.gameGridType.gameGrid)

    def gamePlay(self):
        while self.gameState == State.RUNNING:
            self.handleInput()
            self.ruleChecking()
            self.gameState = State.GAME_OVER    # Temporary so game doesn't running infinitely. Comment out later.
        return self.gameGridType.gameGrid

    def ruleChecking(self):
        self.rules.gameGrid = self.gameGridType.gameGrid
        checkResults = self.rules.executeRowsColumnsChecks()

        if checkResults[-1]:
            self.gameGridType.updateGrid(checkResults[-1])

    def handleInput(self):
        pass
