from tkinter import messagebox
from tkinter import * 
from Tetris.TetrisRules import TetrisRules
from Game import Game
from Tetris.TetrisGrid import TetrisGrid
from Tetris.shape import TetrisShapeFactory
from State import State
from Tetris.TetrisScore import TetrisScore
from Tetris.TetrisGameDisplay import TetrisGameDisplay



class TetrisGame(Game):
    def __init__(self, playerList, parent, mainMenuFrame, showFrameFunc):
        super().__init__(playerList, parent, mainMenuFrame, showFrameFunc)
        self.gameGridType = TetrisGrid()
        self.rules = TetrisRules(self.gameGridType.gameGrid)
        self.scores = {player.username: 0 for player in playerList}
        self.currentPlayer = self.playerList[0]

        self.current_shape = None
        self.current_position = [3, 0]
        self.last_position = [0, 0]

        self.fall_speed = 500
        self.gameState = State.RUNNING
        self.score_system = TetrisScore(self.scores.get(self.currentPlayer.username, 0), self.scores, self.currentPlayer)

        self.display = None
        self.score_label = None

        self.spawn_new_shape()

        
    def gameSetUp(self):
        self.generateGridFrame()
        if not self.frame:
            return  # Guard clause if frame generation failed

        self.display = TetrisGameDisplay(self.frame, self.gameGridType)
        super().gameSetUp()
        self.bind_keys(self.parent)

        self.score_label = self.display.create_labels(self.scores[self.currentPlayer.username], self.currentPlayer.username)

        self.display.update_grid_display()
        self.parent.after(self.fall_speed, self.auto_fall)
        return self.frame

      
    def gamePlay(self):
        self.handleInput()
        self.ruleChecking()
        if self.display:
            self.display.update_grid_display()

            
    def ruleChecking(self):
        self.rules.gameGrid = self.gameGridType.gameGrid
        filledRows = self.rules.checkRows()

        if self.checkIfShapeAtTop():
            self.gameOverPopUp()
            return  # Guard clause — exit early if game over

        if filledRows:
            if len(filledRows) == 18:
                self.gameOverPopUp()
            else:
                self.handle_filled_rows(filledRows)

                
    def handle_filled_rows(self, filledRows):
        self.gameGridType.updateGrid(filledRows)
        self.score_system.calculateGameScore(len(filledRows))
        self.score_system.updatePlayerScore()
        self.score_label.config(text=f"Score: {self.scores[self.currentPlayer.username]}")
        if self.display:
            self.display.update_grid_display()

            
    def checkIfShapeAtTop(self):
        for col_idx in range(len(self.current_shape.shape_matrix[0])):
            if self.gameGridType.gameGrid[0][self.current_position[0] + col_idx].tileType == 2:
                return True
        return False


    def handleInput(self, event=None):
        if not self.display:
            return  # Guard clause if display is not ready

        if event:
            key = event.char.lower()
            if key == 'a':
                self.move_shape(-1, 0)
            elif key == 'd':
                self.move_shape(1, 0)
            elif key == 's':
                self.move_shape(0, 1)
            elif key == 'w':
                self.rotate_shape()

        self.display.update_grid_display()


    def bind_keys(self, root):
        root.bind("<KeyPress>", self.handleInput)


    def spawn_new_shape(self):
        self.current_shape = TetrisShapeFactory.create_random_shape()
        self.current_position = [4, 0]
        self.place_shape_on_grid()


    def auto_fall(self):
        if self.gameState != State.RUNNING:
            return  # Guard clause for non-running state

        if self.can_move(self.current_position[0], self.current_position[1] + 1):
            self.move_shape(0, 1)
        else:
            self.lock_shape()
            self.ruleChecking()
            self.spawn_new_shape()

        if self.display:
            self.display.update_grid_display()

        self.parent.after(self.fall_speed, self.auto_fall)


    def move_shape(self, dx, dy):
        new_x = self.current_position[0] + dx
        new_y = self.current_position[1] + dy

        if self.can_move(new_x, new_y):
            self.last_position = [self.current_position[0], self.current_position[1]]
            self.clear_active_shape()
            self.current_position = [new_x, new_y]
            self.place_shape_on_grid()


    def rotate_shape(self):
        old_matrix = self.current_shape.shape_matrix
        self.current_shape.rotate()

        if not self.can_move(self.current_position[0], self.current_position[1]):
            self.current_shape.shape_matrix = old_matrix
        else:
            self.clear_active_shape()
            self.place_shape_on_grid()


    def can_move(self, x, y):
        for row_idx, row in enumerate(self.current_shape.shape_matrix):
            for col_idx, cell in enumerate(row):
                if not cell:
                    continue  # Guard clause for empty cells

                grid_x = x + col_idx
                grid_y = y + row_idx

                if grid_x < 0 or grid_x >= self.gameGridType.width:
                    return False
                if grid_y < 0 or grid_y >= self.gameGridType.height:
                    return False
                if self.gameGridType.gameGrid[grid_y][grid_x].tileType == 2:
                    return False
        return True


    def lock_shape(self):
        for row_idx, row in enumerate(self.current_shape.shape_matrix):
            for col_idx, cell in enumerate(row):
                if cell:
                    grid_x = self.current_position[0] + col_idx
                    grid_y = self.current_position[1] + row_idx
                    if 0 <= grid_x < self.gameGridType.width and 0 <= grid_y < self.gameGridType.height:
                        self.gameGridType.gameGrid[grid_y][grid_x].tileType = 2


    def clear_active_shape(self):
        for row in self.gameGridType.gameGrid:
            for tile in row:
                if tile.tileType == 1:
                    tile.tileType = 0


    def place_shape_on_grid(self):
        for row_idx, row in enumerate(self.current_shape.shape_matrix):
            for col_idx, cell in enumerate(row):
                if cell:
                    grid_x = self.current_position[0] + col_idx
                    grid_y = self.current_position[1] + row_idx
                    if 0 <= grid_x < self.gameGridType.width and 0 <= grid_y < self.gameGridType.height:
                        self.gameGridType.gameGrid[grid_y][grid_x].tileType = 1

                        
    def swapPlayer(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.gameGridType = TetrisGrid()
        self.rules = TetrisRules(self.gameGridType.gameGrid)
        self.score_system = TetrisScore(0, self.scores, self.playerList[1])
        self.currentPlayer = self.playerList[1]

        self.current_shape = None
        self.current_position = [3, 0]
        self.last_position = [0, 0]
        self.fall_speed = 500
        self.gameState = State.RUNNING

        self.gameSetUp()
        self.bind_keys(self.parent)
        self.frame.focus_set()
        self.spawn_new_shape()
        self.showFrameFunc(self.frame)


    def gameOverPopUp(self):
        if self.currentPlayer != self.playerList[1]:
            messagebox.showinfo("GameOver!", f"{self.currentPlayer.username}'s Score: {self.scores[self.currentPlayer.username]}\nNext game is {self.playerList[1].username}'s turn!")
            self.swapPlayer()
        else:
            winner = TetrisScore.decideWinner(self.playerList, self.scores)
            if winner:
                TetrisScore.updatePlayerWins(winner)
                messagebox.showinfo("GameOver!", f"{self.playerList[0].username}'s Score: {self.scores[self.playerList[0].username]}\n{self.currentPlayer.username}'s Score: {self.scores[self.currentPlayer.username]}\n{winner.username} Wins!")
            else:
                messagebox.showinfo("GameOver!", f"{self.playerList[0].username}'s Score: {self.scores[self.playerList[0].username]}\n{self.currentPlayer.username}'s Score: {self.scores[self.currentPlayer.username]}\nTie!")
            self.gameState = State.GAME_OVER
            self.parent.after(100, lambda: self.showFrameFunc(self.mainMenuFrame))
