from Game import Game 
from State import State
from CandyCrush.CandyCrushGrid import CandyCrushGrid
from CandyCrush.CandyCrushRules import CandyCrushRules
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
        self.previousScore = 0
        self.currentPlayer = self.playerList[0]
    
    def gameSetUp(self):
        self.score = 0
        self.moves = 10 # Adjust this for number of moves per game
        self.frame = super().gameSetUp()
        self.createGrid()
        
        self.current = tk.Label(self.frame, text=f"Current Player: {self.currentPlayer.getUsername()}", font=("Arial", 14))
        self.current.grid(row=0, column=self.gameGridType.width)
        self.score_label = tk.Label(self.frame, text=f"Score: {self.score}", font=("Arial", 14))
        self.score_label.grid(row=1, column=self.gameGridType.width)
        self.movesLeft = tk.Label(self.frame, text=f"Moves Left: {self.moves}", font=("Arial", 14))
        self.movesLeft.grid(row=2, column=self.gameGridType.width)
        
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
        if self.is_animating or self.moves == 0:
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
                    
                    self.gameGridType.swapTiles(pos1, pos2)
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

    def checkAfterSwap(self, p1, p2):
        matches = self.ruleChecking()
        if matches:
            self.moves -= 1
            self.movesLeft.config(text=f"Moves Left: {self.moves}")
            self.clearMatches(matches)
        else:
            self.frame.after(200, lambda: self.gameGridType.swapTilesBack(p1, p2))

    def checkForMatches(self):
        matches = self.ruleChecking()
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
    
    def dropTiles(self):
        dropped = self.gameGridType.updateTilePositions()
        if dropped:
            self.frame.after(300, self.fillEmptySpaces)
        else:
            self.fillEmptySpaces()

    def removeMatches(self, positions):
        for position in positions:
            tile = self.gameGridType.getTileAt(position)
            tile.color_id = 0
            tile.color = "#FFFFFF"
            tile.getFrame().config(bg=tile.getColor())
        self.frame.after(300, self.dropTiles)
    
    def fillEmptySpaces(self):
        self.gameGridType.updateGrid()
        # check if there are new matches
        self.frame.after(300, self.checkAfterFilling)
    
    def checkAfterFilling(self):
        matches = self.ruleChecking()
        if matches:
            self.clearMatches(matches)
        else:
            self.is_animating = False
            if self.moves == 0:
                if self.currentPlayer != self.playerList[1]:
                    self.previousScore = self.score
                    next = tk.Button(self.frame, text="Next Player", command=self.swapPlayer)
                    next.grid(row=self.gameGridType.height, columnspan=self.gameGridType.width)
                else:
                    if self.score > self.previousScore:
                        result = self.playerList[1].getUsername() + " Wins!"
                        self.playerList[1].addWin()
                    elif self.score < self.previousScore:
                        result = self.playerList[0].getUsername() + " Wins!"
                        self.playerList[0].addWin()
                    else:
                        result = "Tie"
                        self.playerList[0].addWin()
                        self.playerList[1].addWin()
                    matchResult = tk.Label(self.frame, text = f"Result: {result}")
                    matchResult.grid(row=self.gameGridType.height, columnspan=self.gameGridType.width)
    
    def updateScoreDisplay(self):
        if hasattr(self, 'score_label'):
            self.score_label.config(text=f"Score: {self.score}")

    def swapPlayer(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        self.currentPlayer = self.playerList[1]
        self.gameSetUp()


    def gamePlay(self):
        return self.gameSetUp()

    def ruleChecking(self):
        return self.ruleSystem.findMatches()

    def handleInput(self):
        pass #No need for real time input handling, player could select a tile and leave for 10 years and come back to select the next.