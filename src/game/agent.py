# agent.py
from __future__ import annotations

from game.gamestate import GameState
from parallel.runner import parallel_mcts
from src.game.mctree import MCTree
from src.parallel.strategy_root import StrategyRoot
from src.parallel.strategy_tree import StrategyTree
from src.parallel.mode import ParallelMode

# strategy class map
PARALLEL_MODE_MAP = {
    ParallelMode.ROOT: StrategyRoot,
    ParallelMode.TREE: StrategyTree,
    ParallelMode.NONE: None,
}


class Agent:
    def __init__(
        self,
        player_id: int,
        time_limit: float,
        n_iteration: int,
        parallel_mode: ParallelMode = ParallelMode.NONE,
        n_workers: int = 1,
    ):
        self.player_id = player_id
        self.time_limit = time_limit
        self.n_iteration = n_iteration
        self.n_workers = n_workers
        self.parallel_mode = parallel_mode
        if self.parallel_mode not in PARALLEL_MODE_MAP:
            raise ValueError(f"unknown parallel_mode: {parallel_mode}")

    def select_move(self, state: GameState) -> tuple[int, int]:
        StrategyCls = PARALLEL_MODE_MAP[self.parallel_mode]

        if StrategyCls is None:
            tree = MCTree(self.time_limit, self.n_iteration, thread_safe=False)
            return tree.run_single_thread(state)

        strategy = StrategyCls(
            n_workers=self.n_workers,
            n_iteration=self.n_iteration,
            time_limit=self.time_limit,
            thread_safe = True
        )
        return parallel_mcts(state, strategy)
