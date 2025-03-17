from TMGE.Game import Game 
from TMGE.State import State
from TMGE.CandyCrush.CandyCrushGrid import CandyCrushGrid
from TMGE.CandyCrush.CandyCrushRules import CandyCrushRules
import tkinter as tk
import random
class CandyCrushGame(Game):
    def __init__(self, playerList, parent, mainMenuFrame=None, showFrameFunc=None):
        super().__init__(playerList, parent, mainMenuFrame, showFrameFunc)
        self.gameGridType = CandyCrushGrid()
        self.ruleSystem = CandyCrushRules(self.gameGridType)
        self.tiles = [] # 2-d array
        self.selected_tile = None
        self.selected_position = None
    
    def gameSetUp(self):
        self.frame = super().gameSetUp()
        self.createGrid()
        self.checkForMatches()
        return self.frame
    
    def createGrid(self):
        self.gameGridType.initializeGrid() # put the tile on the grid
        self.tiles = []
        for i in range(self.gameGridType.height):
            tile_row = []
            for j in range(self.gameGridType.width):
                tile = self.gameGridType.getTileAt((i, j)) 
                
                colored_frame = tk.Frame( # frame(UI) of the tile
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

    def onTileClick(self, event, row, col):
        clicked_position = (row, col)
        clicked_tile = self.gameGridType.getTileAt(clicked_position)
        clicked_frame = clicked_tile.getFrame()
        
        if self.selected_tile is None:
            self.selected_tile = clicked_tile
            self.selected_position = clicked_position
            clicked_frame.config(relief=tk.SUNKEN, bd=5)
        else:
            if self.selected_position == clicked_position:
                self.selected_tile = None
                self.selected_position = None
                clicked_frame.config(relief=tk.RAISED, bd=3)
            else:
                if self.areAdjacent(self.selected_position, clicked_position):
                    self.selected_tile.getFrame().config(relief=tk.RAISED, bd=3)
                    self.swapTiles(self.selected_position, clicked_position)
                    self.selected_tile = None
                    self.selected_position = None
                else:
                    self.selected_tile.getFrame().config(relief=tk.RAISED, bd=3)
                    self.selected_tile = clicked_tile
                    self.selected_position = clicked_position
                    clicked_frame.config(relief=tk.SUNKEN, bd=5)

    def areAdjacent(self, p1, p2):
        row1, col1 = p1
        row2, col2 = p2
        return (row1 == row2 and abs(col1 - col2) == 1) or (col1 == col2 and abs(row1 - row2) == 1) # horizontal or vertical adjacent
    
    def swapTiles(self, p1, p2):
        tile1 = self.gameGridType.getTileAt(p1)
        tile2 = self.gameGridType.getTileAt(p2)
        
        temp_color_id = tile1.getColorId()
        tile1.color_id = tile2.getColorId()
        tile2.color_id = temp_color_id
        
        temp_color = tile1.color
        tile1.color = tile2.color
        tile2.color = temp_color
        
        # update the UI
        tile1.getFrame().config(bg=tile1.getColor())
        tile2.getFrame().config(bg=tile2.getColor())

    def gamePlay(self):
        self.gameState = State.RUNNING
        return self.gameGridType

    def ruleChecking(self):
        pass

    def handleInput(self):
        pass

    def checkForMatches(self):
        matches = self.ruleSystem.checkRows()
        if matches:
            print(matches)