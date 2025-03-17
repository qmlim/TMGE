import random

class CandyCrushTile:
    COLORS = {
        1: "#FF3333", 
        2: "#33CC33",  
        3: "#3366FF",  
        4: "#FFCC00",  
        5: "#CC33FF",  
        6: "#00CCCC"  
    }
    
    COLOR_NAMES = {
        1: "red",
        2: "green",
        3: "blue",
        4: "yellow",
        5: "purple",
        6: "teal"
    }
    
    def __init__(self, color_id=None, position=None, frame=None):
        if color_id is None:
            color_id = random.randint(1, 6)
        self.color = self.COLORS[color_id]
        self.color_id = color_id
        self.position = position
        self.frame = frame
    
    def updatePosition(self, new_position):
        self.position = new_position
    
    def getColor(self):
        return self.color
    
    def getColorId(self):
        return self.color_id
    
    def getColorName(self):
        return self.COLOR_NAMES[self.color_id]
    
    def setFrame(self, frame):
        self.frame = frame
    
    def getFrame(self):
        return self.frame