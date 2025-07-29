from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from constants import DIRS, BLACK, WIN_STONE_CNT
from settings import BOARD_LENGTH
from src.game.bitset import bit, idx, set_bit
from ui.console_renderer import ConsoleRenderer

BOARD_N_BITS = BOARD_LENGTH * BOARD_LENGTH


@dataclass(slots=True)
class GameState:
    current_player: int
    color_bitset: int = 0
    occupy_bitset: int = 0
    last_move: tuple[int, int] = (-1, -1)
    is_terminal: bool = False
    winner: int = -1

    # --------------------------------------------------------------------- #
    #                   			interface                               #
    # --------------------------------------------------------------------- #

    # only around of last move (optimization)
    def legal_moves(self, radius: int = 1) -> list[tuple[int, int]]:
        if self.last_move == (-1, -1) or radius == BOARD_LENGTH:
            return [
                (i % BOARD_LENGTH, i // BOARD_LENGTH)
                for i in range(BOARD_N_BITS)
                if not (self.occupy_bitset >> i) & 1
            ]

        lx, ly = self.last_move
        moves = []
        for dx in range(-radius, radius + 1):
            nx = lx + dx
            if nx < 0 or nx >= BOARD_LENGTH:
                continue
            for dy in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue
                ny = ly + dy
                if 0 <= ny < BOARD_LENGTH and self._is_empty(nx, ny):
                    moves.append((nx, ny))
        if moves:
            return moves
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
        return GameState(
            current_player=self.current_player,
            color_bitset=self.color_bitset,
            occupy_bitset=self.occupy_bitset,
            last_move=self.last_move,
            is_terminal=self.is_terminal,
            winner=self.winner,
        )

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
        x, y = self.last_move
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

    # occupy bit = 1이면 False, 0이면 True
    def _is_empty(self, x, y):
        return not (self.occupy_bitset >> idx(x, y)) & 1
