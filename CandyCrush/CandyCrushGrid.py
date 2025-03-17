from Grid import Grid
from CandyCrush.CandyCrushTile import CandyCrushTile
import random
class CandyCrushGrid(Grid):
    def __init__(self):
        self.height = 9
        self.width = 9
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)] # create a 9x9 grid

    def initializeGrid(self):
        for i in range(self.height):
            for j in range(self.width):
                color_id = self.getValidColorId(i, j)
                tile = CandyCrushTile(color_id, (i, j))
                self.setTileAt((i, j), tile)
        return self.grid
            
    def getValidColorId(self, row, col):
        available_colors = list(range(1, 7))
        if col >= 2:
            left1 = self.getTileAt((row, col-1))
            left2 = self.getTileAt((row, col-2))
            if left1.getColorId() == left2.getColorId():
                if left1.getColorId() in available_colors:
                    available_colors.remove(left1.getColorId())
        
        if row >= 2:
            up1 = self.getTileAt((row-1, col))
            up2 = self.getTileAt((row-2, col))
            if up1.getColorId() == up2.getColorId():
                if up1.getColorId() in available_colors:
                    available_colors.remove(up1.getColorId())
        
        return random.choice(available_colors)
        
    def setTileAt(self, position, tile):
        row, col = position
        self.grid[row][col] = tile
    
    def getTileAt(self, position):
        row, col = position
        return self.grid[row][col]
    
    def updateGrid(self, new_grid=None):
        pass
    
    def isEmpty(self):
        pass
    
    def clearRows(self):
        pass
    
    def clearColumns(self):
        pass