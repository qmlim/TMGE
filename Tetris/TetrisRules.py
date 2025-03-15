import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from RuleSystem import RuleSystem


class TetrisRules(RuleSystem):
    def __init__(self, gameGrid):
        self.gameGrid = gameGrid

    def checkColumns(self):
        return

    def checkRows(self):
        filledRows = []
        for index, row in enumerate(self.gameGrid):
            if "" not in row:
                filledRows.append(index)
        return filledRows
