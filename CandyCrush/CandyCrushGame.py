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
        self.animation_speed = 100
        self.is_animating = False
        self.score = 0
    
    def gameSetUp(self):
        self.frame = super().gameSetUp()
        self.createGrid()
        
        self.score_label = tk.Label(self.frame, text=f"Score: {self.score}", font=("Arial", 14))
        self.score_label.grid(row=self.gameGridType.height + 1, columnspan=self.gameGridType.width, pady=10)
        
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
        if self.is_animating:
            return
        
        clicked_position = (row, col)
        clicked_tile = self.gameGridType.getTileAt(clicked_position)
        
        if clicked_tile is None or clicked_tile.getColorId() == 0:
            return
            
        clicked_frame = clicked_tile.getFrame()
        
        if self.selected_tile is None:
            # First selection
            self.selected_tile = clicked_tile
            self.selected_position = clicked_position
            clicked_frame.config(relief=tk.SUNKEN, bd=5)
        else:
            # Second selection
            if self.selected_position == clicked_position:
                # Deselect if clicking the same tile
                self.selected_tile = None
                self.selected_position = None
                clicked_frame.config(relief=tk.RAISED, bd=3)
            else:
                if self.areAdjacent(self.selected_position, clicked_position):
                    # If adjacent, swap tiles
                    self.selected_tile.getFrame().config(relief=tk.RAISED, bd=3)
                    pos1 = self.selected_position
                    pos2 = clicked_position

                    self.selected_tile = None
                    self.selected_position = None
                    self.is_animating = True
                    
                    self.swapTiles(pos1, pos2)
                    self.frame.after(300, lambda p1=pos1, p2=pos2: self.checkAfterSwap(p1, p2))
                else:
                    # Not adjacent, update selection to new tile
                    self.selected_tile.getFrame().config(relief=tk.RAISED, bd=3)
                    self.selected_tile = clicked_tile
                    self.selected_position = clicked_position
                    clicked_frame.config(relief=tk.SUNKEN, bd=5)
                    print(f"Changed selection to tile at {clicked_position}")

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
        
        # Update the UI
        tile1.getFrame().config(bg=tile1.getColor())
        tile2.getFrame().config(bg=tile2.getColor())

    def checkAfterSwap(self, p1, p2):
        matches = self.ruleSystem.findMatches()
        if matches:
            self.clearMatches(matches)
        else:
            self.frame.after(200, lambda: self.swapTilesBack(p1, p2))
        
    def swapTilesBack(self, p1, p2):
        tile1 = self.gameGridType.getTileAt(p1)
        tile2 = self.gameGridType.getTileAt(p2)
        
        temp_color_id = tile1.getColorId()
        tile1.color_id = tile2.getColorId()
        tile2.color_id = temp_color_id
        
        temp_color = tile1.color
        tile1.color = tile2.color
        tile2.color = temp_color
        
        tile1.getFrame().config(bg=tile1.getColor())
        tile2.getFrame().config(bg=tile2.getColor())
        
        self.is_animating = False

    def checkForMatches(self):
        matches = self.ruleSystem.findMatches()
        if matches:
            self.clearMatches(matches)
        else:
            self.is_animating = False
        
    def clearMatches(self, matches):
        if not matches:
            self.is_animating = False
            return
        
        total_matched = 0
        positions_to_remove = []
        
        for match in matches:
            total_matched += len(match)
            for position in match:
                positions_to_remove.append(position)
        
        self.score += total_matched * 10
        self.updateScoreDisplay()
        self.removeMatches(positions_to_remove)
    
    def removeMatches(self, positions):
        for position in positions:
            tile = self.gameGridType.getTileAt(position)
            tile.color_id = 0
            tile.color = "#FFFFFF"
            tile.getFrame().config(bg=tile.getColor())
            tile.getFrame().config(bg=tile.getColor())
        self.is_animating = False
    
    def updateScoreDisplay(self):
        if hasattr(self, 'score_label'):
            self.score_label.config(text=f"Score: {self.score}")

    def gamePlay(self):
        self.gameState = State.RUNNING
        return self.gameGridType

    def ruleChecking(self):
        return self.ruleSystem.hasMatches()

    def handleInput(self):
        pass