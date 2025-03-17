from TMGE.RuleSystem import RuleSystem

class CandyCrushRules(RuleSystem):
    def __init__(self, gameGrid):
        super().__init__(gameGrid)
        self.min_match = 3

    def checkRows(self):
        matches = []
        for i in range(self.gameGrid.height):
            current_match = [] # 3 in horizontal
            current_color = None
            for j in range(self.gameGrid.width):
                tile = self.gameGrid.getTileAt((i, j))
                if current_color is not None and tile.getColorId() == current_color:
                    current_match.append((i, j))
                else:
                    if len(current_match) >= self.min_match:
                        matches.append(current_match)
                    current_color = tile.getColorId()
                    current_match = [(i, j)]

      
    
    def checkColumns(self):
        pass