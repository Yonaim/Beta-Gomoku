from __future__ import annotations
import numpy as np
from .gamestate import GameState
from typing import Optional
from numpy.typing import NDArray
import random
from .constants import EPSILON
from .heuristic import ClassicHeuristic

class Node:
	state: GameState
	move: tuple[int, int] | None
	parent: Node | None
	children: NDArray[np.object_]
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
		self.heuristic = ClassicHeuristic().evaluate(state, state.current_player)

	def expand(self) -> "Node":
		tried = {c.move for c in self.children}
		untried = [m for m in self.state.get_legal_moves() if m not in tried]
		if not untried:
			raise RuntimeError("expand on fully-expanded node")

		move = random.choice(untried)
		child_state = self.state.clone()
		child_state.apply_move(move)

		child = Node(child_state, move, self)
		self.children = np.append(self.children, np.array([child], dtype=object))
		return child

	def best_child(self, score_fn):
		best_score = -float("inf")
		best_nodes = []
		for child in self.children:
			score = score_fn(child)
			if score > best_score + EPSILON:
				best_score = score
				best_nodes = [child]
			elif abs(score - best_score) < EPSILON:
				best_nodes.append(child)
		return random.choice(best_nodes)

	def is_fully_expanded(self) -> bool:
		return len(self.children) == len(self.state.get_legal_moves())

	def most_visited_child(self) -> Node:
		return max(self.children, key=lambda ch: ch.n_visit)
