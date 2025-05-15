from .mcts import MCTS
from .gamestate import GameState

class Agent:
	player_id: int
	mcts: MCTS

	def __init__(self, player_id: int, time_limit: float, n_iteration: int):
		self.player_id = player_id
		self.mcts = MCTS(time_limit, n_iteration)

	def select_move(self, state: GameState):
		return self.mcts.run(state)
