from __future__ import annotations
import numpy as np
import copy

from ui import console_renderer
from .constants import WIN_STONE_CNT, EMPTY, DIRS, WHITE
from .settings import BOARD_LENGTH
from typing import Optional

class GameState:
    board: np.ndarray
    current_player: int
    last_move: tuple[int, int] | None
    is_terminal: bool
    terminal_winner: int | None

    def __init__(self, current_player: int):
        self.board = np.zeros((BOARD_LENGTH, BOARD_LENGTH), dtype=np.uint8)
        self.current_player = current_player
        self.last_move = None
        self.is_terminal = False
        self.terminal_winner = None

    def get_legal_moves(self) -> list[tuple[int, int]]:
        arr = np.argwhere(self.board == EMPTY)
        return [tuple(pos) for pos in arr]

    def apply_move(self, move: tuple[int, int]):
        if self.board[move] != EMPTY:
            raise ValueError
        self.board[move] = self.current_player
        self.last_move = move
        winner = self.winner_by_last_move()
        if winner != None or len(self.get_legal_moves()) == 0:
            self.is_terminal = True
            self.terminal_winner = winner

	# internal -----------------------------------------------------------------

	# for debug
    def print_board(self) -> None:
        renderer = console_renderer.ConsoleRenderer(BOARD_LENGTH)
        renderer.draw(self.board)
