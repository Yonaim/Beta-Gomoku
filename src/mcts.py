from __future__ import annotations
import time
import random
import math
from .node import Node
from .gamestate import GameState

C_DEFAULT = math.sqrt(2)	# exploration constant (tune if necessary)
K_DEFAULT = 50				# bias-decay constant
MAX_DEPTH_DEFAULT = 20
N_ROLLOUT = 5

class MCTS:
	time_limit: float
	n_iteration: int
	
	def __init__(self, time_limit: float, n_iteration: int):
		self.time_limit = time_limit
		self.n_iteration = n_iteration

	def run(self, state: GameState) -> tuple[int, int]:
		root = Node(state) # root is the current game state
		start_time = time.time()
		i = 0

		while (i < self.n_iteration) and (time.time() - start_time < self.time_limit):
			selected = self.select(root)
			expanded = selected.expand()
			reward = self.average_rollout(expanded.state, N_ROLLOUT)
			self.backpropagate(expanded, reward)
			i += 1

		best_move = root.most_visited_child().move
		assert best_move != None
		return best_move

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
			while True:
				try:
					move = random.choice(state.get_legal_moves())
					state.apply_move(move)
					break
				except ValueError:
					print("illegal move")
					continue
		return self.heuristic_eval(state)

	def heuristic_eval(self, state: GameState) -> float:
		# TODO: 구현하기
		return random.uniform(-1, 1)

	# progressive bias
	# TODO: select에 적용
	def pb_ucb1(self, node: Node, k: float = K_DEFAULT, c: float = C_DEFAULT):
		parent_n = node.parent.n_visit if node.parent else 1
		q = node.total_reward / node.n_visit
		h = node.heuristic
		
		alpha = k / (k + node.n_visit)
		exploitation = (1 - alpha) * q + alpha * h
		exploration = c * math.sqrt(math.log(parent_n) / (1 + node.n_visit))		
		return exploitation + exploration
