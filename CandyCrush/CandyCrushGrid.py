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
    
    def swapTiles(self, p1, p2):
        tile1 = self.getTileAt(p1)
        tile2 = self.getTileAt(p2)
            
        temp_color_id = tile1.getColorId()
        tile1.color_id = tile2.getColorId()
        tile2.color_id = temp_color_id
        
        temp_color = tile1.color
        tile1.color = tile2.color
        tile2.color = temp_color
        
        # Update the UI
        tile1.getFrame().config(bg=tile1.getColor())
        tile2.getFrame().config(bg=tile2.getColor())

    def swapTilesBack(self, p1, p2):
        tile1 = self.getTileAt(p1)
        tile2 = self.getTileAt(p2)
        
        temp_color_id = tile1.getColorId()
        tile1.color_id = tile2.getColorId()
        tile2.color_id = temp_color_id
        
        temp_color = tile1.color
        tile1.color = tile2.color
        tile2.color = temp_color
        
        tile1.getFrame().config(bg=tile1.getColor())
        tile2.getFrame().config(bg=tile2.getColor())
        
        self.is_animating = False
    
    def moveTile(self, p1, p2): # from p1 to p2
        t1 = self.getTileAt(p1)
        t2 = self.getTileAt(p2)
        
        t2.color_id = t1.getColorId()
        t2.color = t1.getColor()
        t1.color_id = 0
        t1.color = "#FFFFFF"
        
        t2.getFrame().config(bg=t2.getColor())
        t1.getFrame().config(bg=t1.getColor())
    
    def updateGrid(self): #Fills Empty Spaces
        empty_positions = []
        # find all empty positions
        for row in range(self.height):
            for col in range(self.width):
                if self.getTileAt((row, col)).getColorId() == 0:
                    empty_positions.append((row, col))
        
        if not empty_positions:
            self.is_animating = False
            return
        
        for position in empty_positions:
            row, col = position
            color_id = random.choice(range(1, 7))
            tile = self.getTileAt(position)
            tile.color_id = color_id
            tile.color = tile.COLOR_MAP.get(color_id, "#FFFFFF")
            tile.getFrame().config(bg=tile.getColor())
    
    def isEmpty(self): #Not Necessary
        return

    def clearRows(self): #Not Necessary
        return

    def clearColumns(self): #Not Necessary
        return

    def updateTilePositions(self):
        columns_affected = set()
        # columns that need drop tiles
        for row in range(self.height):
            for col in range(self.width):
                if self.getTileAt((row, col)).getColorId() == 0:
                    columns_affected.add(col)
        
        has_dropped = False
        for col in columns_affected:
            # bottom to top
            for row in range(self.height - 1, -1, -1):
                current_tile = self.getTileAt((row, col))
                if current_tile.getColorId() == 0:
                    row_above = row - 1
                    while row_above >= 0:
                        tile_above = self.getTileAt((row_above, col))
                        if tile_above.getColorId() != 0:
                            # found a non-empty tile, drop it to the current position
                            self.moveTile((row_above, col), (row, col))
                            has_dropped = True
                            break
                        row_above -= 1
        return has_dropped