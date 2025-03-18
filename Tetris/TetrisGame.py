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
        """Sets up the game UI."""
        super().gameSetUp()
        self.bind_keys(self.parent)
        self.updateGridDisplay()

        self.parent.after(self.fall_speed, self.auto_fall)
        return self.frame

    def gamePlay(self):
        """Main game logic loop, called by the framework."""
        self.handleInput()
        self.ruleChecking()
        self.updateGridDisplay()

    def ruleChecking(self):
        """Checks and clears fully filled rows (non-zero)."""
        self.rules.gameGrid = self.gameGridType.gameGrid
        checkResults = self.rules.checkRows()
        if checkResults:
            self.gameGridType.updateGrid(checkResults)
            self.updateGridDisplay()

    def handleInput(self, event=None):
        """Handles user key presses."""
        if event:
            if event.keysym == "Left":
                self.move_shape(-1, 0)
            elif event.keysym == "Right":
                self.move_shape(1, 0)
            elif event.keysym == "Down":
                self.move_shape(0, 1)
            elif event.keysym == "Up":
                self.rotate_shape()

        self.updateGridDisplay()

    def bind_keys(self, root):
        """Binds keyboard presses to shape movement/rotation."""
        root.bind("<KeyPress>", self.handleInput)

    def spawn_new_shape(self):
        """Create a random Tetris shape at the top of the grid."""
        self.current_shape = TetrisShapeFactory.create_random_shape()
        self.current_position = [4, 0]
        self.place_shape_on_grid()

    def auto_fall(self):
        """
        Moves the active shape down automatically every self.fall_speed ms.
        If it can’t move down any further, lock the shape in place and spawn a new one.
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

    def lock_shape(self):
        """
        Convert all tiles from tileType=1 (the falling shape)
        into tileType=2 (locked) in the grid.
        """
        for row_idx, row in enumerate(self.current_shape.shape_matrix):
            for col_idx, cell in enumerate(row):
                if cell:
                    grid_x = self.current_position[0] + col_idx
                    grid_y = self.current_position[1] + row_idx
                    if 0 <= grid_x < self.gameGridType.width and 0 <= grid_y < self.gameGridType.height:
                        self.gameGridType.gameGrid[grid_y][grid_x].tileType = 2

    def move_shape(self, dx, dy):
        """Move the active shape by (dx, dy) if it is a valid move."""
        new_x = self.current_position[0] + dx
        new_y = self.current_position[1] + dy

        if self.can_move(new_x, new_y):
            self.clear_active_shape()
            self.current_position = [new_x, new_y]
            self.place_shape_on_grid()

    def rotate_shape(self):
        """Rotate the shape 90° clockwise if valid."""
        original_matrix = self.current_shape.shape_matrix[:]
        self.current_shape.rotate()
        if not self.can_move(self.current_position[0], self.current_position[1]):
            self.current_shape.shape_matrix = original_matrix
        else:
            self.clear_active_shape()
            self.place_shape_on_grid()

    def can_move(self, x, y):
        """
        Returns True if the shape’s top-left corner can be placed at (x, y)
        without colliding with existing locked tiles or going out-of-bounds.
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

    def clear_active_shape(self):
        """Remove any cell with tileType=1 from the grid."""
        for row in self.gameGridType.gameGrid:
            for tile in row:
                if tile.tileType == 1:
                    tile.tileType = 0

    def place_shape_on_grid(self):
        """Put the current shape (tileType=1) into the grid."""
        for row_idx, row in enumerate(self.current_shape.shape_matrix):
            for col_idx, cell in enumerate(row):
                if cell:
                    grid_x = self.current_position[0] + col_idx
                    grid_y = self.current_position[1] + row_idx
                    if 0 <= grid_x < self.gameGridType.width and 0 <= grid_y < self.gameGridType.height:
                        self.gameGridType.gameGrid[grid_y][grid_x].tileType = 1

    def updateGridDisplay(self):
        """Update the tkinter grid to show locked (2) and active (1) tiles."""
        for i in range(self.gameGridType.height):
            for j in range(self.gameGridType.width):
                tile = self.gameGridType.gameGrid[i][j]
                btn = self.frame.grid_slaves(row=i, column=j)[0]

                if tile.tileType == 2:
                    btn.config(text="■", bg="darkblue")
                elif tile.tileType == 1:
                    btn.config(text="■", bg="blue")
                else:
                    btn.config(text=" ", bg="white")


if __name__ == "__main__":
    TetrisGame([], None)
