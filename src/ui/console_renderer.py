import numpy as np
from game.constants import BLACK, WHITE

EMPTY_CHAR = "·"
BLACK_CHAR = "●"
WHITE_CHAR = "○"

class ConsoleRenderer:
    def __init__(self, size: int = 15):
        self.size = size

    def draw(self, board: np.ndarray):
        for y in range(self.size):
                    row = []
                    for x in range(self.size):
                        p = board[y, x]
                        row.append(
                            BLACK_CHAR if p == BLACK
                            else WHITE_CHAR if p == WHITE
                            else EMPTY_CHAR
                        )
                    print(" ".join(row))
        print()  # blank line
