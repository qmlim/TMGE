from Game import Game 
from CandyCrush.CandyCrushGrid import CandyCrushGrid
from CandyCrush.CandyCrushTile import CandyCrushTile
import tkinter as tk
from State import State

class CandyCrushGame(Game):
    def __init__(self, playerList, parent, mainMenuFrame=None, showFrameFunc=None):
        super().__init__(playerList, parent, mainMenuFrame, showFrameFunc)
        self.gameGridType = CandyCrushGrid()
        self.buttons = []
        self.tiles = []
    
    def gameSetUp(self):
        self.frame = super().gameSetUp()
        self.placeTilesOnGrid()
        return self.frame
    
    def placeTilesOnGrid(self):
        self.tiles = []
        for i in range(self.gameGridType.height):
            tile_row = []
            for j in range(self.gameGridType.width):
                tile = CandyCrushTile(None, (i, j))
                
                for widget in self.frame.winfo_children():
                        widget.config(
                            bg="#3366FF",
                            text="■",
                            font=("Arial", 12, "bold"),
                            fg="white"
                        )
                        break
                
                self.gameGridType.setTileAt(i, j, tile)
                tile_row.append(tile)
            self.tiles.append(tile_row)
    
    
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