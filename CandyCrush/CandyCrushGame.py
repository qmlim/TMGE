from Game import Game 
from CandyCrush.CandyCrushGrid import CandyCrushGrid
import tkinter as tk
from State import State

class CandyCrushGame(Game):
    def __init__(self, playerList, parent, mainMenuFrame=None, showFrameFunc=None):
        super().__init__(playerList, parent, mainMenuFrame, showFrameFunc)
        self.gameGridType = CandyCrushGrid()

    def gamePlay(self):
        while self.gameState == State.RUNNING:
            self.handleInput()
            self.ruleChecking()
            self.gameState = State.GAME_OVER
        return self.gameGridType

    def ruleChecking(self):
        pass

    def handleInput(self):
        pass