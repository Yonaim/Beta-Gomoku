from concurrent.futures import ThreadPoolExecutor
import time

from src.game.gamestate import GameState
from src.game.mcts import MCTree
from src.game.node import Node
from .strategy_base import StrategyBase


class StrategyTree(StrategyBase):
    def __init__(self, n_workers: int, n_iteration: int, time_limit: float):
        self.n_workers = n_workers
        self.n_iteration = n_iteration
        self.time_limit = time_limit

    def run(self, state: GameState, tree: MCTree):
        tree.root = Node(state)
        start = time.time()

        def worker():
            while (
                tree.root.n_visit < self.n_iteration
                and time.time() - start < self.time_limit
            ):
                tree.do_iteration()

        with ThreadPoolExecutor(self.n_workers) as pool:
            list(pool.submit(worker) for _ in range(self.n_workers))

    def best_move(self, tree: MCTree) -> tuple[int, int]:
        move = tree.root.most_visited_child().move
        return move
