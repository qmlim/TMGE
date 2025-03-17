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
        self.score = 0  # Initialize the score
    
    def gameSetUp(self):
        self.frame = super().gameSetUp()
        self.createGrid()
        
        # Add score display
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
                    
                    # Store positions for later use
                    pos1 = self.selected_position
                    pos2 = clicked_position
                    
                    # Reset selection before animation
                    self.selected_tile = None
                    self.selected_position = None
                    
                    # Set animating flag to prevent additional clicks
                    self.is_animating = True
                    
                    # Perform the swap
                    self.swapTiles(pos1, pos2)
                    
                    # Check for matches after the swap
                    self.frame.after(300, lambda: self.checkAfterSwap(pos1, pos2))
                else:
                    # Not adjacent, update selection to new tile
                    self.selected_tile.getFrame().config(relief=tk.RAISED, bd=3)
                    self.selected_tile = clicked_tile
                    self.selected_position = clicked_position
                    clicked_frame.config(relief=tk.SUNKEN, bd=5)

    def areAdjacent(self, p1, p2):
        if p1 is None or p2 is None:
            return False
            
        row1, col1 = p1
        row2, col2 = p2
        return (row1 == row2 and abs(col1 - col2) == 1) or (col1 == col2 and abs(row1 - row2) == 1) # horizontal or vertical adjacent
    
    def swapTiles(self, p1, p2):
        if p1 is None or p2 is None:
            self.is_animating = False
            return
            
        tile1 = self.gameGridType.getTileAt(p1)
        tile2 = self.gameGridType.getTileAt(p2)
        
        if tile1 is None or tile2 is None:
            self.is_animating = False
            return
            
        # Swap color IDs
        temp_color_id = tile1.getColorId()
        tile1.color_id = tile2.getColorId()
        tile2.color_id = temp_color_id
        
        # Swap colors
        temp_color = tile1.color
        tile1.color = tile2.color
        tile2.color = temp_color
        
        # Update the UI
        tile1.getFrame().config(bg=tile1.getColor())
        tile2.getFrame().config(bg=tile2.getColor())

    def checkAfterSwap(self, p1, p2):
        """Check for matches after swapping tiles"""
        if p1 is None or p2 is None:
            self.is_animating = False
            return
            
        matches = self.ruleSystem.findMatches()
        if matches:
            # If there are matches, clear them
            self.clearMatches(matches)
        else:
            # If no matches, swap back
            self.swapTilesBack(p1, p2)
        
    def swapTilesBack(self, p1, p2):
        """Swap tiles back if no matches were found"""
        if p1 is None or p2 is None:
            self.is_animating = False
            return
            
        self.swapTiles(p1, p2)
        self.is_animating = False

    def checkForMatches(self):
        """Check for matches and process them"""
        matches = self.ruleSystem.findMatches()
        if matches:
            self.clearMatches(matches)
        else:
            self.is_animating = False
        
    def clearMatches(self, matches):
        """Clear matched tiles and update score"""
        if not matches:
            self.is_animating = False
            return
        
        # Count total matched tiles for scoring
        total_matched = 0
        
        # Store match positions for delayed removal
        positions_to_remove = []
        
        for match in matches:
            total_matched += len(match)
            
            # Visual indication of matches with a flash effect
            for position in match:
                tile = self.gameGridType.getTileAt(position)
                if tile:
                    frame = tile.getFrame()
                    # Flash effect - using lambda with default arguments to capture current values
                    self.frame.after(0, lambda f=frame: f.config(bg="#FFFFFF"))
                    self.frame.after(200, lambda f=frame, t=tile: f.config(bg=t.getColor()))
                    positions_to_remove.append(position)
        
        # Update score - basic scoring: 10 points per matched tile
        self.score += total_matched * 10
        
        # Update score display
        self.frame.after(300, self.updateScoreDisplay)
        
        # Clear tiles after the flash effect
        self.frame.after(400, lambda: self.actuallyRemoveMatches(positions_to_remove))
    
    def actuallyRemoveMatches(self, positions):
        """Actually remove the matched tiles after the visual effect"""
        for position in positions:
            tile = self.gameGridType.getTileAt(position)
            if tile:
                # Change the color to white (empty)
                tile.color_id = 0
                tile.color = "#FFFFFF"
                tile.getFrame().config(bg=tile.getColor())
        
        # Set this to false to allow interaction again
        self.is_animating = False
    
    def updateScoreDisplay(self):
        """Update the score display"""
        if hasattr(self, 'score_label'):
            self.score_label.config(text=f"Score: {self.score}")

    def gamePlay(self):
        self.gameState = State.RUNNING
        return self.gameGridType

    def ruleChecking(self):
        return self.ruleSystem.hasMatches()

    def handleInput(self):
        pass