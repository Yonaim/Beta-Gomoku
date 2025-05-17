import numpy as np

from constants import BLACK, WHITE
from settings import BOARD_LENGTH
from src.game.bitset import bit

EMPTY_CHAR = "·"
BLACK_CHAR = "●"
WHITE_CHAR = "○"


class ConsoleRenderer:

    def __init__(self, size: int = BOARD_LENGTH):
        self.size = size

    def draw(self, occupy_bitset: int, color_bitset: int):
        for y in range(self.size):
            row = []
            for x in range(self.size):
                occ = bit(occupy_bitset, x, y)
                if occ is 0:
                    row.append(EMPTY_CHAR)
                    continue
                row.append(BLACK_CHAR if bit(color_bitset, x, y) else WHITE_CHAR)
            print(" ".join(row))
        print()  # blank line
