import numpy as np
from .gamestate import GameState
from __future__ import annotations
from typing import Optional

class Node:
	state: GameState
	parent: Node
	children: np.ndarray
	value: int
	visits: int

	def __init__(self):
		pass

	def select(self):
		pass

	def expand(self) -> Node:
		pass
	
	def update(self):
		pass

	def best_ucb1_child(self) -> Node:
		pass
