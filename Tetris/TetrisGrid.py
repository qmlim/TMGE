from Grid import Grid

class TetrisGrid(Grid):
    def __init__(self):
        self.width = 10
        self.height = 20
        self.gameGrid = [["_" for i in range(self.width)] for j in range(self.height)]

    def updateGrid(self):
        pass

    def isEmpty(self):
        pass