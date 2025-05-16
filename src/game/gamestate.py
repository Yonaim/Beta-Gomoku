from __future__ import annotations
import numpy as np
import copy
from .constants import WIN_STONE_CNT, EMPTY, DIRS
from .settings import BOARD_LENGTH

class GameState:
	board: np.ndarray
	current_player: int

	def __init__(self, current_player: int):
		self.board = np.zeros((BOARD_LENGTH,BOARD_LENGTH), dtype=np.uint8)
		self.current_player = current_player
	
	def get_legal_moves(self) -> list[tuple[int, int]]:
		arr = np.argwhere(self.board == EMPTY)
		return [tuple(pos) for pos in arr]
 
	def apply_move(self, move: tuple[int, int]):
		if self.board[move] != EMPTY:
			raise ValueError
		self.board[move] = self.current_player

	def get_winner(self) -> int:
		for y in range(BOARD_LENGTH):
			for x in range(BOARD_LENGTH):
				player = self.board[y][x]
				if (player == EMPTY):
					continue
				for dx, dy in DIRS:
					if self._count_stone_in_dir(x, y, dx, dy) >= WIN_STONE_CNT:
						return player
		return EMPTY

	def is_terminated(self) -> bool:
		return self.get_winner() != 0 or len(self.get_legal_moves()) == 0

	# internal -----------------------------------------------------------------

	# for debug
    def print_board(self) -> None:
        renderer = console_renderer.ConsoleRenderer(BOARD_LENGTH)
        renderer.draw(self.board)
