from Game import Game 
import tkinter as tk
from State import State
import random
from CandyCrush.CandyCrushTile import CandyCrushTile
from CandyCrush.CandyCrushGrid import CandyCrushGrid
class CandyCrushGame(Game):
    def __init__(self, playerList, parent, mainMenuFrame=None, showFrameFunc=None):
        super().__init__(playerList, parent, mainMenuFrame, showFrameFunc)
        self.gameGridType = CandyCrushGrid()
        self.tiles = []
        self.tile_frames = []
        self.selected_tile = None
    
    def gameSetUp(self):
        self.frame = super().gameSetUp()
        self.createGrid()
        return self.frame
    
    def createGrid(self):
        self.gameGridType.initializeGrid() # put the tile on the grid
        self.tiles = []
        self.tile_frames = []
        for i in range(self.gameGridType.height):
            tile_row = []
            frame_row = []
            for j in range(self.gameGridType.width):
                tile = self.gameGridType.getTileAt(i, j) 
                tile_row.append(tile)
                
                colored_frame = tk.Frame( # style of the tile
                    self.frame,
                    bg=tile.getColor(),
                    width=50,
                    height=30,
                    bd=3,
                    relief=tk.RAISED
                )
                colored_frame.grid(row=i, column=j, padx=2, pady=2)
                frame_row.append(colored_frame)
            
            self.tiles.append(tile_row)
            self.tile_frames.append(frame_row)
        
    def gamePlay(self):
        self.gameState = State.RUNNING
        return self.gameGridType

    def ruleChecking(self):
        pass

    def handleInput(self):
        pass