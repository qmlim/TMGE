import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Player import Player
from Tetris.TetrisRules import TetrisRules
from Game import Game 
from Tetris.TetrisGrid import TetrisGrid
from tkinter import * 
from State import State


class TetrisGame(Game):
    def __init__(self, playerList, parent):
        super().__init__(playerList, parent)
        self.gameState = State.RUNNING
        self.gameGridType = TetrisGrid()
        self.rules = TetrisRules(self.gameGridType.gameGrid)


    def gamePlay(self):
        self.gameSetUp()

        while self.gameState == State.RUNNING:
            self.handleInput()
            self.ruleChecking()
            self.gameState = State.GAME_OVER    # Temporary so game doesn't running infinitely. Comment out later.


    def ruleChecking(self):
        self.rules.gameGrid = self.gameGridType.gameGrid
        checkResults = self.rules.executeRowsColumnsChecks()

        if checkResults[-1]:
            self.gameGridType.updateGrid(checkResults[-1])


    def gameSetUp(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

        tetrisFrame = Frame(self.parent)
        Label(tetrisFrame, 
              text="Tetris", 
              font=("Font", 30)).grid(row=0, column=0, padx=10, pady=(10, 0))
        tetrisFrame.grid(row=0, column=0, columnspan=2)

        self.playersFrame = Frame(self.parent)
        self.playersFrame.grid(row=1, column=0, columnspan=2)

        self.updatePlayer1Frame()
        self.updatePlayer2Frame()

        self.parent.tkraise()


    def handleInput(self):
        pass


    def updatePlayer1Frame(self):
        player1 = Frame(self.playersFrame)
        player1.grid(row=0, column=0, padx=40, pady=10)

        Label(
            player1, 
            text=f"{self.playerList[0].username}\nScore: {0}", 
            font=("Font", 16)).grid(row=0, column=0, columnspan=10, pady=(0,5))
        
        self.generatePlayerGridFrame(player1, start_row=1)


    def updatePlayer2Frame(self):
        player2 = Frame(self.playersFrame)
        player2.grid(row=0, column=1, padx=40, pady=10)

        Label(player2, 
              text=f"{self.playerList[1].username}\nScore: {0}", 
              font=("Font", 16)).grid(row=0, column=0, columnspan=10, pady=(0,5))
        
        self.generatePlayerGridFrame(player2, start_row=1)


    def generatePlayerGridFrame(self, frame, start_row=0):
        for i in range(self.gameGridType.height):
            for j in range(self.gameGridType.width):
                Button(frame, text="", width=1, height=1).grid(row=i + start_row, column=j)
