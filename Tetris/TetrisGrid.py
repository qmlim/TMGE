import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Grid import Grid

class TetrisGrid(Grid):
    def __init__(self):
        super().__init__(10, 20)

    def updateGrid(self, checkResults):
        self.clearRows(checkResults)

    def isEmpty(self):
        pass

    def clearRows(self, checkResults):
        for index in checkResults:
            self.gameGrid.pop(index)
            self.gameGrid.insert(0, [""] * self.width)    

    def clearColumns(self):
        return
