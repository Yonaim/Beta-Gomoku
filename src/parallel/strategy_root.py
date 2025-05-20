import multiprocessing as mp

from src.game.gamestate import GameState
from src.game.mcts import MCTree
from .strategy_base import StrategyBase


class StrategyRoot(StrategyBase):
    def __init__(self, n_workers: int, n_iteration: int, time_limit: float):
        self.n_workers = n_workers
        self.n_iteration = n_iteration
        self.time_limit = time_limit
        self._cum: dict[tuple[int, int], tuple[int, float]] = {}

    @staticmethod
    def _worker(state: GameState, n_iter: int, t_lim: float):
        tree = MCTree(t_lim, n_iter)
        tree.run_single_thread(state)
        return {
            child.move: (child.n_visit, child.total_reward)
            for child in tree.root.children
            if child.move is not None
        }

    def run(self, state: GameState, tree: MCTree):  # tree 인자를 쓰지 않음
        args = [
            (state.clone(), self.n_iteration, self.time_limit)
            for _ in range(self.n_workers)
        ]
        with mp.Pool(self.n_workers) as pool:
            results = pool.starmap(self._worker, args)

        for result in results:
            for move, (v, r) in result.items():
                prev_v, prev_r = self._cum.get(move, (0, 0.0))
                self._cum[move] = (prev_v + v, prev_r + r)

    def best_move(self, _: MCTree) -> tuple[int, int]:
        return max(self._cum.items(), key=lambda item: item[1][0])[0]
