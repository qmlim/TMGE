import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Grid import Grid
from Tile import Tile


class TetrisGrid(Grid):
    def __init__(self):
        super().__init__(3, 3)
        self.gameGrid = [[Tile(0, (i, j)) for i in range(self.width)] for j in range (self.height)]

    def updateGrid(self, checkResults):
        self.clearRows(checkResults)
        self.updateTilePositions()

    def isEmpty(self, position):
        return self.gameGrid[position[1]][position[0]].tileType == 0

    def clearRows(self, checkResults):
        for index in checkResults:
            self.gameGrid.pop(index)
            self.gameGrid.insert(0, [Tile(0, (0,0)) for i in range(self.width)])
        
    def updateTilePositions(self):
        for j in range(self.height):
            for i in range(self.width):
                self.gameGrid[j][i].updatePosition((i, j))

    def clearColumns(self): # No need to implement
        return
