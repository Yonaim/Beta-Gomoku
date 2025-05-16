from __future__ import annotations

import copy
from typing import Optional

import numpy as np

from constants import DIRS, EMPTY, WIN_STONE_CNT
from settings import BOARD_LENGTH
from ui.console_renderer import ConsoleRenderer


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

    def winner_by_last_move(self) -> Optional[int]:
        if self.last_move == None:
            return None
        y, x = self.last_move
        player = self.board[y, x]
        for dx, dy in DIRS:
            count = (
                self._count_one_dir(x, y, dx, dy)
                + 1
                + self._count_one_dir(x, y, -dx, -dy)
            )
            if count >= WIN_STONE_CNT:
                return player
        return None

    # internal -----------------------------------------------------------------

    def _count_one_dir(self, x: int, y: int, dx: int, dy: int) -> int:
        cnt = 0
        nx, ny = x + dx, y + dy
        player = self.board[y, x]
        
        if (player == EMPTY):
            return 0
        
        while (
            (0 <= nx < BOARD_LENGTH)
            and (0 <= ny < BOARD_LENGTH)
            and self.board[ny, nx] == player
        ):
            cnt += 1
            nx += dx
            ny += dy
        return cnt

    def clone(self) -> GameState:
        return copy.deepcopy(self)
	
	# for debug
    def print_board(self) -> None:
        renderer = ConsoleRenderer(BOARD_LENGTH)
        renderer.draw(self.board)
