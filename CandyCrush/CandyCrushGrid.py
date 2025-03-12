from Grid import Grid

class CandyCrushGrid(Grid):
    def __init__(self):
        self.width = 9
        self.height = 9
        self.gameGrid = [["_" for i in range(self.width)] for j in range(self.height)]

    def updateGrid(self):
        pass

    def isEmpty(self):
        pass