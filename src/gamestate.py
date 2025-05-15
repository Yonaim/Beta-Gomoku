from __future__ import annotations
import numpy as np

BOARD_LEGNTH = 15
WIN_STONE_CNT = 5
EMPTY = 0
BLACK = 1
WHITE = 2

class GameState:
	board: np.darray
	current_player: int
	DIRS = [(1,0), (0,1), (1,1), (1,-1)]

	def __init__(self, current_player: int):
		self.board = np.zeros((15,15), dtype=np.uint8)
		self.current_player = current_player
	
	def get_legal_moves(self) -> list[tuple[int, int]]:
		return np.argwhere(self.board == 0).tolist()
 
	def apply_move(self, move: tuple[int, int]):
		self.board[move] = self.current_player

	def get_winner(self) -> int:
		for y in range(BOARD_LEGNTH):
			for x in range(BOARD_LEGNTH):
				player = self.board[y][x]
				if (player == EMPTY):
					continue
				for dx, dy in self.DIRS:
					if self._count_stone_in_dir(x, y, dx, dy) >= WIN_STONE_CNT:
						return player
		return EMPTY

	def is_terminated(self) -> bool:
		return self.get_winner() != 0 or len(self.get_legal_moves()) == 0

	# internal -----------------------------------------------------------------

	def _count_stone_in_dir(self, x: int, y: int, dx: int, dy: int):
		player = self.board[y, x]
		nx, ny =  x, y
		cnt = 0
		i = 0

		while ((0 <= nx < BOARD_LEGNTH) and (0 <= ny < BOARD_LEGNTH) and self.board[ny, nx] == player):
			cnt += 1
			nx = x + i * dx
			ny = y + i * dy
			i += 1
		return cnt
