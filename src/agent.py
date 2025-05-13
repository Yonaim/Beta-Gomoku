from .mcts import MCTS
from .gamestate import GameState

class Agent:
	player_id: int
	mcts: MCTS

	def __init__(self, player_id: int, iterations: int):
		self.player_id = player_id
		self.mcts = MCTS(iterations)

	def select_move(self, state: GameState):
		return self.mcts.select_move(state)
