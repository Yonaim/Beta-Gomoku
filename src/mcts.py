from .node import Node
from .gamestate import GameState
import time
import random

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
			expanded = self.expand(selected)
			value = self.simulate(expanded)
			self.backpropagate(expanded, value)
			i += 1

	def select(self, node: Node) -> Node:
		while (node.children.size != 0):
			if not node.is_fully_expanded():
				return node.expand()
			else:
				node = node.best_ucb1_child()

	# TODO: apply heuristic
	def simulate(self, state: GameState) -> float:
		cur = state

		while not (state.is_terminate()):
			move = random.choice(state.get_legal_moves()) # uniform random
			cur.apply_move(move)

	def backpropagate(self, node: Node, value: float):
		while (node != self.root):
			# TODO: 노드의 값에 반영하기
			node = node.parent
		# TODO: 루트에 반영

