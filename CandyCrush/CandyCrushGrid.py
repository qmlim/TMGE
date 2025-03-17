from Grid import Grid
from CandyCrush.CandyCrushTile import CandyCrushTile
import random
class CandyCrushGrid:
    def __init__(self):
        self.height = 9
        self.width = 9
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
    
    def setTileAt(self, row, col, tile):
        if 0 <= row < self.height and 0 <= col < self.width:
            self.grid[row][col] = tile
    
    def getTileAt(self, row, col):
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.grid[row][col]
        return None
    
    def updateGrid(self, new_grid=None):
        pass
    
    def isEmpty(self):
        pass
    
    def clearRows(self):
        pass
    
    def clearColumns(self):
        pass