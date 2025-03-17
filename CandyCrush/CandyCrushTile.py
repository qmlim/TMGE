from Tile import Tile
import random

class CandyCrushTile(Tile):
    
    def __init__(self, color_id=None, position=None):
        if color_id is None:
            color_id = random.randint(1, 6)
        
        color = self.COLORS[color_id]
        
        super().__init__(color_id, position)
        self.color = color
        self.color_id = color_id
    
    def updatePosition(self, new_position):
        self.position = new_position
    
    def getColor(self):
        return self.color
    
    def getColorId(self):
        return self.color_id
    
    def getColorName(self):
        return self.COLOR_NAMES[self.color_id] 