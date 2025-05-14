import numpy as np

EMPTY = "·"
BLACK = "●"
WHITE = "○"

class ConsoleRenderer:
    def __init__(self, size: int = 15):
        self.size = size

    def draw(self, board: np.ndarray):
        for y in range(self.size):
                    row = []
                    for x in range(self.size):
                        p = board[y, x]
                        row.append(
                            BLACK if p == 1
                            else WHITE if p == 2
                            else EMPTY
                        )
                    print(" ".join(row))
        print()  # blank line
