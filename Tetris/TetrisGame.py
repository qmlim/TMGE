import sys
import os
import tkinter as tk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Tetris.TetrisRules import TetrisRules
from Game import Game
from Tetris.TetrisGrid import TetrisGrid
from Tetris.shape import TetrisShapeFactory
from State import State

class TetrisGame(Game):
    def __init__(self, playerList, parent):
        super().__init__(playerList, parent)
        self.gameGridType = TetrisGrid()
        self.rules = TetrisRules(self.gameGridType.gameGrid)


        self.current_shape = None
        self.current_position = [4, 0]

        self.running = True
        self.fall_speed = 500

        self.spawn_new_shape()

    def gameSetUp(self):
        """Sets up the game’s UI (buttons, etc.)."""
        super().gameSetUp()
        self.bind_keys(self.parent)
        self.updateGridDisplay()

        self.parent.after(self.fall_speed, self.auto_fall)
        return self.frame

    def gamePlay(self):
        """Main game loop called from the framework (if applicable)."""
        self.handleInput()
        self.ruleChecking()
        self.updateGridDisplay()

    def ruleChecking(self):
        """Check if any rows are fully filled, then clear them."""
        self.rules.gameGrid = self.gameGridType.gameGrid
        filled_rows = self.rules.checkRows()
        if filled_rows:
            self.gameGridType.updateGrid(filled_rows)
            self.updateGridDisplay()

    def handleInput(self, event=None):
        """Handles keyboard input. Using WASD for movement/rotation."""
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

        self.updateGridDisplay()

    def bind_keys(self, root):
        """
        Binds keyboard controls to the window.
        Instead of arrow keys, we use WASD.
        """
        root.bind("<KeyPress>", self.handleInput)

    def spawn_new_shape(self):
        """Spawns a brand-new random Tetris shape at the top."""
        self.current_shape = TetrisShapeFactory.create_random_shape()
        self.current_position = [4, 0]
        self.place_shape_on_grid()

    def auto_fall(self):
        """
        Automatically called every self.fall_speed ms.
        Tries to move shape down by 1. If it fails, the piece is “locked”
        and a new piece spawns.
        """
        if not self.running:
            return

        if self.can_move(self.current_position[0], self.current_position[1] + 1):
            self.move_shape(0, 1)
        else:
            self.lock_shape()
            self.ruleChecking()
            self.spawn_new_shape()

        self.updateGridDisplay()
        self.parent.after(self.fall_speed, self.auto_fall)

    def move_shape(self, dx, dy):
        """Moves the current shape (tileType=1) by (dx, dy) if valid."""
        new_x = self.current_position[0] + dx
        new_y = self.current_position[1] + dy

        if self.can_move(new_x, new_y):
            self.clear_active_shape()
            self.current_position = [new_x, new_y]
            self.place_shape_on_grid()

    def rotate_shape(self):
        """Rotate the shape 90 degrees clockwise if it fits."""
        old_matrix = self.current_shape.shape_matrix
        self.current_shape.rotate()

        if not self.can_move(self.current_position[0], self.current_position[1]):
            self.current_shape.shape_matrix = old_matrix
        else:
            self.clear_active_shape()
            self.place_shape_on_grid()

    def can_move(self, x, y):
        """
        Checks if placing the shape’s top-left corner at grid (x, y)
        would go out-of-bounds or collide with locked tiles.
        """
        for row_idx, row in enumerate(self.current_shape.shape_matrix):
            for col_idx, cell in enumerate(row):
                if cell:
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
        """
        Convert the current shape’s tileType=1 squares to tileType=2,
        thus “locking” it in place on the board.
        """
        for row_idx, row in enumerate(self.current_shape.shape_matrix):
            for col_idx, cell in enumerate(row):
                if cell:
                    grid_x = self.current_position[0] + col_idx
                    grid_y = self.current_position[1] + row_idx
                    if 0 <= grid_x < self.gameGridType.width and 0 <= grid_y < self.gameGridType.height:
                        self.gameGridType.gameGrid[grid_y][grid_x].tileType = 2

    def clear_active_shape(self):
        """Erase any tileType=1 squares (the “active” piece) from the board."""
        for row in self.gameGridType.gameGrid:
            for tile in row:
                if tile.tileType == 1:
                    tile.tileType = 0

    def place_shape_on_grid(self):
        """Draw the current shape in the grid with tileType=1."""
        for row_idx, row in enumerate(self.current_shape.shape_matrix):
            for col_idx, cell in enumerate(row):
                if cell:
                    grid_x = self.current_position[0] + col_idx
                    grid_y = self.current_position[1] + row_idx
                    if 0 <= grid_x < self.gameGridType.width and 0 <= grid_y < self.gameGridType.height:
                        self.gameGridType.gameGrid[grid_y][grid_x].tileType = 1

    def updateGridDisplay(self):
        """
        Update the on-screen buttons to reflect:
          - 0 => empty
          - 1 => active shape
          - 2 => locked tile
        """
        for i in range(self.gameGridType.height):
            for j in range(self.gameGridType.width):
                tile = self.gameGridType.gameGrid[i][j]
                btn = self.frame.grid_slaves(row=i, column=j)[0]

                if tile.tileType == 2:
                    btn.config(text="", bg="darkblue")
                elif tile.tileType == 1:
                    btn.config(text="", bg="blue")
                else:
                    btn.config(text=" ", bg="white")


if __name__ == "__main__":
    TetrisGame([], None)
