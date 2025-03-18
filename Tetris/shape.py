import random

class TetrisShape:
    def __init__(self, shape_matrix):
        self.shape_matrix = shape_matrix  # A 2D list representing the shape
    
    def rotate(self):
        """Rotates the shape 90 degrees clockwise."""
        self.shape_matrix = [list(row) for row in zip(*self.shape_matrix[::-1])]
    
    def display(self):
        """Prints the shape to the console for debugging."""
        for row in self.shape_matrix:
            print(" ".join(["■" if cell else " " for cell in row]))
        print()


class TetrisShapeFactory:
    SHAPES = {
        "I": [[1, 1, 1, 1]],  # 4x1
        "O": [[1, 1], [1, 1]],  # 2x2
        "L": [[1, 0], [1, 0], [1, 1]],  # L shape
        "S": [[0, 1, 1], [1, 1, 0]],  # S shape
        "T": [[1, 1, 1], [0, 1, 0]],  # T shape
    }

    @staticmethod
    def create_random_shape():
        """Creates a random Tetris shape."""
        shape_type = random.choice(list(TetrisShapeFactory.SHAPES.keys()))
        return TetrisShape(TetrisShapeFactory.SHAPES[shape_type])

# Example Usage:
if __name__ == "__main__":
    factory = TetrisShapeFactory()
   
