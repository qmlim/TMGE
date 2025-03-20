from ScoreSystem import ScoreSystem

class TetrisScore(ScoreSystem):
    def __init__(self, points, scores, player):
        super().__init__(points)
        self.scores = scores
        self.player = player

    def calculateGameScore(self, rows_cleared):
        if rows_cleared == 1:
            self.points += 10
        elif rows_cleared == 2:
            self.points += 40
        elif rows_cleared == 3:
            self.points += 90
        elif rows_cleared == 4:
            self.points += 160

    def updateScore(self):
        self.scores[self.player.username] = self.points

    def updatePlayerScore(self):
        self.calculateGameScore(1)
        self.updateScore()

    def decideWinner(playersList, scores):
        if scores[playersList[0].username] > scores[playersList[1].username]:
            return playersList[0]
        elif scores[playersList[0].username] < scores[playersList[1].username]:
            return playersList[1]
        else:
            return None

    def updatePlayerWins(player):
        player.wins += 1