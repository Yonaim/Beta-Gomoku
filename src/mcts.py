from __future__ import annotations
import time
import random
import math
from .node import Node
from .gamestate import GameState

MAX_DEPTH_DEFAULT = 20
N_ROLLOUT = 5

class MCTS:
	time_limit: float
	max_iterations: int
	
	def __init__(self, time_limit: float, max_iterations: int):
		self.time_limit = time_limit
		self.max_iterations = max_iterations

	def run(self, state: GameState):
		root = Node(state) # root is the current game state
		start_time = time.time()
		i = 0

		while (i < self.max_iterations) and (time.time() - start_time < self.time_limit):
			selected = self.select(root)
			expanded = selected.expand()
			value = self.average_rollout(expanded.state, N_ROLLOUT)
			self.backpropagate(expanded, value)
			i += 1

	def select(self, node: Node) -> Node:
		while True:
			if node.state.is_terminated():
				return node
			elif not node.is_fully_expanded():
				return node.expand()
			node = node.best_ucb1_child()

	# TODO: Blending with heuristic
	def average_rollout(self, state: GameState, n_rollout: int, max_depth : int = MAX_DEPTH_DEFAULT) -> float:
		total = 0.0
		for _ in range(n_rollout):
			total += self.rollout(state, max_depth)
		return total / n_rollout
	
	# To reduce stack frame, use iterative update and do not call a function
	def backpropagate(self, node: Node | None, reward: float):
		cur_reward = reward
		while node is not None:
			node.n_visit += 1
			node.total_reward += cur_reward
			cur_reward = -cur_reward
			node = node.parent
	
	# internal -----------------------------------------------------------------

	def rollout(self, start: GameState, max_depth : int = MAX_DEPTH_DEFAULT) -> float:
		state = start.clone()
		for _ in range(max_depth):
			if state.is_terminated():
				break
			move = random.choice(state.get_legal_moves())
			state.apply_move(move)
		return self.heuristic_eval(state)

	def heuristic_eval(self, state: GameState) -> float:
		# TODO: 구현하기
		return random.uniform(-1, 1)

