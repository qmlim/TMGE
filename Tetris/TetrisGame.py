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
        self.spawn_new_shape()

        self.running = True
        self.fall_speed = 500

    def gameSetUp(self):
        """Sets up the game UI."""
        super().gameSetUp()
        self.bind_keys(self.parent)
        self.updateGridDisplay()  # Show initial grid
        return self.frame

    def gamePlay(self):
        """Implements game logic loop."""
        self.handleInput()
        self.ruleChecking()
        self.updateGridDisplay()  # Ensure UI updates with changes

    def ruleChecking(self):
        """Checks and clears rows."""
        self.rules.gameGrid = self.gameGridType.gameGrid
        checkResults = self.rules.checkRows()
        if checkResults:
            self.gameGridType.updateGrid(checkResults)
            self.updateGridDisplay()

    def handleInput(self, event=None):
        """Handles user input for moving the shape."""
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
        """Binds keyboard controls to game actions."""
        root.bind("<KeyPress>", self.handleInput)

    def spawn_new_shape(self):
        """Spawns a new random Tetris shape at the top of the grid."""
        self.current_shape = TetrisShapeFactory.create_random_shape()
        self.current_position = [4, 0]
        self.place_shape_on_grid()

    def move_shape(self, dx, dy):
        """Moves the shape if the new position is valid."""
        new_x = self.current_position[0] + dx
        new_y = self.current_position[1] + dy

        if self.can_move(new_x, new_y):
            self.current_position = [new_x, new_y]
            self.place_shape_on_grid()

    def rotate_shape(self):
        """Rotates the shape if possible."""
        original_matrix = self.current_shape.shape_matrix
        self.current_shape.rotate()

        if not self.can_move(self.current_position[0], self.current_position[1]):
            self.current_shape.shape_matrix = original_matrix
        else:
            self.place_shape_on_grid()

    def can_move(self, x, y):
        """Checks if the shape can move to the new position."""
        for row_idx, row in enumerate(self.current_shape.shape_matrix):
            for col_idx, cell in enumerate(row):
                if cell:
                    grid_x = x + col_idx
                    grid_y = y + row_idx

                    if grid_x < 0 or grid_x >= self.gameGridType.width or grid_y >= self.gameGridType.height:
                        return False
                    
                    if not self.gameGridType.isEmpty((grid_x, grid_y)):
                        return False
        
        return True

    def place_shape_on_grid(self):
        for row in self.gameGridType.gameGrid:
            for tile in row:
                tile.tileType = 0

        for row_idx, row in enumerate(self.current_shape.shape_matrix):
            for col_idx, cell in enumerate(row):
                if cell:
                    grid_x = self.current_position[0] + col_idx
                    grid_y = self.current_position[1] + row_idx
                    if 0 <= grid_x < self.gameGridType.width and 0 <= grid_y < self.gameGridType.height:
                        self.gameGridType.gameGrid[grid_y][grid_x].tileType = 1

    def updateGridDisplay(self):
        for i in range(self.gameGridType.height):
            for j in range(self.gameGridType.width):
                tile = self.gameGridType.gameGrid[i][j]
                btn = self.frame.grid_slaves(row=i, column=j)[0]
                if tile.tileType == 1:
                    btn.config(text="■", bg="blue")
                else:
                    btn.config(text=" ", bg="white")


if __name__ == "__main__":
    TetrisGame([], None)
