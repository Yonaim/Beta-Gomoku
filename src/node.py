import numpy as np
from .gamestate import GameState
from __future__ import annotations
from typing import Optional
import math

class Node:
	state: GameState
	move: tuple[int, int]
	parent: Node
	children: np.ndarray
	total_reward: float
	n_visit: int
	heuristic: float

	def __init__(self, state: GameState, move: Optional[tuple[int,int]] = None, parent: Optional[Node] = None):
		self.state = state
		self.move = move
		self.parent = parent
		self.children = np.array([], dtype=object)
		self.total_reward: float = 0.0
		self.n_visit: int = 0
		self.heuristic

	def expand(self) -> Node:
		tried_moves = {child.move for child in self.children}
		for move in self.state.get_legal_moves():
			if move not in tried_moves:
				child_state = self.state.apply.move(move)
				child_node = Node(child_state, move, self)
				return child_node
		raise RuntimeError("expand() called on a fully-expanded node")

	# UCT = (mean of reward) + (c * sqrt(ln(parent.n_visit) / n_visit))
	# Usually, c = sqrt(2) = 1.414...
	def best_ucb1_child(self, c: float = 1.414) -> Node:
		assert self.children
		log_n = math.log(self.n_visit)

		def ucb1(child: Node) -> float:
			q = child.total_reward / child.n_visit
			u = c * math.sqrt(log_n / child.n_visit)
			return q + u
		return max(self.children, key = ucb1)		

	def is_fully_expanded(self) -> bool:
		if len(self.children == len(tuple(self.state.get_legal_moves()))):
			return True
		else:
			return False
