from TMGE.RuleSystem import RuleSystem

class CandyCrushRules(RuleSystem):
    def __init__(self, gameGrid):
        super().__init__(gameGrid)
        self.min_match = 3

    def checkRows(self):
        matches = [] # [[p1,p2,p3], [p5,p6,p7]]
        for row in range(self.gameGrid.height):
            current_match = [] # [p1,p2,p3] p1:(i,j)
            current_color = None
            for col in range(self.gameGrid.width):
                tile = self.gameGrid.getTileAt((row, col))
                if current_color is not None and tile.getColorId() == current_color: # p1 match p2 color
                    current_match.append((row, col))
                else:
                    if len(current_match) >= self.min_match:
                        matches.append(current_match)
                    current_color = tile.getColorId()
                    current_match = [(row, col)]

            if len(current_match) >= self.min_match: #extra check while end
                matches.append(current_match)
        return matches
    
    def checkColumns(self):
        matches = []
        for col in range(self.gameGrid.width):
            current_match = []
            current_color = None
            for row in range(self.gameGrid.height):
                tile = self.gameGrid.getTileAt((row, col))
                if current_color is not None and tile.getColorId() == current_color:
                    current_match.append((row, col))
                else:
                    if len(current_match) >= self.min_match:
                        matches.append(current_match)
                    current_color = tile.getColorId()
                    current_match = [(row, col)]
            
            if len(current_match) >= self.min_match:
                matches.append(current_match)
        return matches

    def findMatches(self):
        row_matches = self.checkRows()
        col_matches = self.checkColumns()
        return row_matches + col_matches
    
    def hasMatches(self):
        matches = self.findMatches()
        return len(matches) > 0