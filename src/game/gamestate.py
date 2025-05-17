from __future__ import annotations

import copy
from typing import Optional

from constants import DIRS, BLACK, WIN_STONE_CNT
from settings import BOARD_LENGTH
from src.game.bitset import bit, idx, set_bit
from ui.console_renderer import ConsoleRenderer

BOARD_N_BITS = BOARD_LENGTH * BOARD_LENGTH


class GameState:
    occupy_bitset: int
    color_bitset: int
    current_player: int
    last_move: tuple[int, int] | None
    is_terminal: bool
    winner: int | None

    def __init__(self, current_player: int):
        self.color_bitset = 0
        self.occupy_bitset = 0
        self.current_player = current_player
        self.last_move = None
        self.is_terminal = False
        self.winner = None

    # --------------------------------------------------------------------- #
    #                   			interface                               #
    # --------------------------------------------------------------------- #

    def legal_moves(self) -> list[tuple[int, int]]:
        return [
            (i % BOARD_LENGTH, i // BOARD_LENGTH)
            for i in range(BOARD_N_BITS)
            if not (self.occupy_bitset >> i) & 1
        ]

    def apply_move(self, move: tuple[int, int]):
        x, y = move
        if not self._is_empty(x, y):
            raise ValueError("Already occupied")
        self.occupy_bitset = set_bit(self.occupy_bitset, x, y)
        if self.current_player == BLACK:
            self.color_bitset = set_bit(self.color_bitset, x, y)
        else:
            pass
        self.last_move = move
        self._check_terminal()

    def clone(self) -> GameState:
        return copy.deepcopy(self)

    # for debug
    def print_board(self) -> None:
        renderer = ConsoleRenderer(BOARD_LENGTH)
        renderer.draw(self.occupy_bitset, self.color_bitset)

    # --------------------------------------------------------------------- #
    #                   			internal                                #
    # --------------------------------------------------------------------- #

    def _count_one_dir(self, x: int, y: int, dx: int, dy: int) -> int:
        if self._is_empty(x, y) is True:
            return 0
        player = bit(self.color_bitset, x, y)
        nx, ny = x + dx, y + dy
        cnt = 0

        while (
            (0 <= nx < BOARD_LENGTH)
            and (0 <= ny < BOARD_LENGTH)
            and self._is_empty(nx, ny) is False
            and bit(self.color_bitset, nx, ny) == player
        ):
            cnt += 1
            nx += dx
            ny += dy
        return cnt

    # by last move
    def _check_terminal(self) -> Optional[int]:
        if self.last_move is None:
            return None
        y, x = self.last_move
        for dx, dy in DIRS:
            count = (
                self._count_one_dir(x, y, dx, dy)
                + 1
                + self._count_one_dir(x, y, -dx, -dy)
            )
            if count >= WIN_STONE_CNT:
                self.is_terminal = True
                self.winner = self.current_player
        if self.occupy_bitset.bit_count() == BOARD_N_BITS:
            self.is_terminal = True
            self.winner = None

    # occupy bit = 1이면 False, 0이면 True
    def _is_empty(self, x, y):
        return not (self.occupy_bitset >> idx(x, y)) & 1
