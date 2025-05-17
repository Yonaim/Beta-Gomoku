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
                if occ is 1:
                    continue
                color = bit(color_bitset, x, y)
                row.append(
                    BLACK_CHAR
                    if color == BLACK
                    else WHITE_CHAR if color == WHITE else EMPTY_CHAR
                )
            print(" ".join(row))
        print()  # blank line
