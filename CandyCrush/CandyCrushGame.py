from Game import Game 
import tkinter as tk
from State import State
import random
from CandyCrush.CandyCrushGrid import CandyCrushGrid
class CandyCrushGame(Game):
    def __init__(self, playerList, parent, mainMenuFrame=None, showFrameFunc=None):
        super().__init__(playerList, parent, mainMenuFrame, showFrameFunc)
        self.gameGridType = CandyCrushGrid()
        self.tiles = []
        self.selected_tile = None
        self.selected_position = None
    
    def gameSetUp(self):
        self.frame = super().gameSetUp()
        self.createGrid()
        return self.frame
    
    def createGrid(self):
        self.gameGridType.initializeGrid() # put the tile on the grid
        self.tiles = []
        for i in range(self.gameGridType.height):
            tile_row = []
            for j in range(self.gameGridType.width):
                tile = self.gameGridType.getTileAt(i, j) 
                
                colored_frame = tk.Frame( # style of the tile
                    self.frame,
                    bg=tile.getColor(),
                    width=50,
                    height=30,
                    bd=3,
                    relief=tk.RAISED
                )
                colored_frame.grid(row=i, column=j, padx=2, pady=2)
                colored_frame.bind("<Button-1>", lambda event, row=i, col=j: self.onTileClick(event, row, col))
                tile.setFrame(colored_frame)
                tile_row.append(tile)
            
            self.tiles.append(tile_row)

    def areAdjacent(self, p1, p2):
        row1, col1 = p1
        row2, col2 = p2
        return (row1 == row2 and abs(col1 - col2) == 1) or (col1 == col2 and abs(row1 - row2) == 1) # horizontal or vertical adjacent
    
    def gamePlay(self):
        self.gameState = State.RUNNING
        return self.gameGridType

    def ruleChecking(self):
        pass

    def handleInput(self):
        pass