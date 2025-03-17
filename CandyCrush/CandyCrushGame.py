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
        self.placeTilesOnGrid()
        return self.frame
    
    def placeTilesOnGrid(self):
        self.tiles = []
        self.tile_frames = []
        button_positions = []
        
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget('text') == " ":
                grid_info = widget.grid_info()
                row, col = int(grid_info['row']), int(grid_info['column'])
                button_positions.append((widget, row, col))
        
        for i in range(self.gameGridType.height):
            self.tiles.append([None] * self.gameGridType.width)
            self.tile_frames.append([None] * self.gameGridType.width)
        
        for widget, row, col in button_positions:
            button_width = widget.winfo_reqwidth()
            button_height = widget.winfo_reqheight()
            grid_info = widget.grid_info()
            
            widget.destroy()
            
            tile = CandyCrushTile(None, (row, col))
            self.tiles[row][col] = tile
            
            colored_frame = tk.Frame(
                self.frame,
                bg=tile.getColor(),
                width=button_width,
                height=button_height,
                bd=3,
                relief=tk.RAISED
            )

            colored_frame.grid(
                row=row, 
                column=col, 
                padx=2, 
                pady=2, 
                sticky=grid_info.get('sticky', '')
            )

            self.tile_frames[row][col] = colored_frame
            self.gameGridType.setTileAt(row, col, tile)
    
    def gamePlay(self):
        self.gameState = State.RUNNING
        return self.gameGridType

    def ruleChecking(self):
        pass

    def handleInput(self):
        pass