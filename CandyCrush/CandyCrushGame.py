from Game import Game 
import tkinter as tk
from State import State
import random
from CandyCrush.CandyCrushGrid import CandyCrushGrid
from CandyCrush.CandyCrushTile import CandyCrushTile
class CandyCrushGame(Game):
    def __init__(self, playerList, parent, mainMenuFrame=None, showFrameFunc=None):
        super().__init__(playerList, parent, mainMenuFrame, showFrameFunc)
        self.gameGridType = CandyCrushGrid()
        self.tiles = []
        self.selected_tile = None
    
    def gameSetUp(self):
        self.frame = super().gameSetUp()
        self.placeTilesOnGrid()
        return self.frame
    
    def placeTilesOnGrid(self):
        self.tiles = []
        print("asdasdsa")

        grid_buttons = []
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget('text') == " ":
                grid_info = widget.grid_info()
                row, col = grid_info['row'], grid_info['column']
                
                if row < self.gameGridType.height and col < self.gameGridType.width:
                    while len(grid_buttons) <= row:
                        grid_buttons.append([])
                    
                    while len(grid_buttons[row]) <= col:
                        grid_buttons[row].append(None)
                    
                    grid_buttons[row][col] = widget
        
        for i in range(self.gameGridType.height):
            tile_row = []
            for j in range(self.gameGridType.width):
                if i < len(grid_buttons) and j < len(grid_buttons[i]) and grid_buttons[i][j] is not None:

                    tile = CandyCrushTile(None, (i, j))
                    tile_row.append(tile)
                    
                    button = grid_buttons[i][j]
                    button.config(
                        bg=tile.getColor(),
                        activebackground=tile.getColor(),
                        relief=tk.RAISED,
                        bd=4,
                        width=5,
                        height=2
                    )
                    
                    self.gameGridType.setTileAt(i, j, tile)
            
            if tile_row:
                self.tiles.append(tile_row)
    
    def gamePlay(self):
        self.gameState = State.RUNNING
        return self.gameGridType

    def ruleChecking(self):
        pass

    def handleInput(self):
        pass