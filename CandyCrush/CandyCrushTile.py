class CandyCrushTile:
    COLOR_MAP = {
        0: "#FFFFFF", 
        1: "#FF0000",
        2: "#00FF00",
        3: "#0000FF",
        4: "#FFFF00",
        5: "#FF00FF",
        6: "#00FFFF",
    }
    
    def __init__(self, color_id, position):
        self.color_id = color_id
        self.position = position
        self.color = self.COLOR_MAP.get(color_id, "#FFFFFF") # default white
        self.frame = None
    
    def getColorId(self):
        return self.color_id
    
    def getColor(self):
        return self.color
    
    def getPosition(self):
        return self.position
    
    def setPosition(self, position):
        self.position = position
    
    def getFrame(self):
        return self.frame
    
    def setFrame(self, frame):
        self.frame = frame