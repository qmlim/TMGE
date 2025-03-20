# --- TetrisGameDisplay.py ---
from tkinter import Label

class TetrisGameDisplay:
    def __init__(self, frame, gameGridType):
        self.frame = frame
        self.gameGridType = gameGridType

    def update_grid_display(self):
        for i in range(self.gameGridType.height):
            for j in range(self.gameGridType.width):
                tile = self.gameGridType.gameGrid[i][j]
                btn = self.frame.grid_slaves(row=i, column=j)[0]

                if tile.tileType == 2:
                    btn.config(text="⬛", bg="darkblue")
                elif tile.tileType == 1:
                    btn.config(text="🟦", bg="blue")
                else:
                    btn.config(text=" ", bg="white")

    def create_labels(self, score, player_username):
        Label(self.frame, text="Tetris", font=("Font", 20), width=12).grid(row=0, column=20)
        Label(self.frame, text=f"Current Player: {player_username}", font=("Font", 15)).grid(row=2, column=20)
        Label(self.frame, text="Score:", font=("Font", 15)).grid(row=3, column=20)
        score_label = Label(self.frame, text=f"Score: {score}", font=("Font", 15))
        score_label.grid(row=4, column=20)
        return score_label
