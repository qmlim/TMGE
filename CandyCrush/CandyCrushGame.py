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
        self.tile_frames = []
        self.selected_tile = None
        self.selected_position = None
    
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
                colored_frame.bind("<Button-1>", lambda event, row=i, col=j: self.onTileClick(event, row, col))
                frame_row.append(colored_frame)
            
            self.tiles.append(tile_row)
            self.tile_frames.append(frame_row)

    def onTileClick(self, event, row, col):
        clicked_tile = self.gameGridType.getTileAt(row, col)
        clicked_frame = self.tile_frames[row][col]
        
        if self.selected_tile is None: # if no tile is selected
            self.selected_tile = clicked_tile
            self.selected_position = (row, col)
            clicked_frame.config(relief=tk.SUNKEN, bd=5) # select the tile
       
    
    
    def gamePlay(self):
        self.gameState = State.RUNNING
        return self.gameGridType

    def ruleChecking(self):
        pass

    def handleInput(self):
        pass