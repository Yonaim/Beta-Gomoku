from .gamestate import GameState
from .mcts import MCTree, run_root_parallel, run_tree_parallel


class Agent:
    player_id: int
    mct: MCTree

    def __init__(
        self,
        player_id: int,
        time_limit: float,
        n_iteration: int,
        parallel_mode: str = "none",
        n_workers: int = 1,
    ):
        self.player_id = player_id
        self.parallel_mode = parallel_mode
        self.n_iteration = n_iteration
        self.time_limit = time_limit
        self.n_workers = n_workers
        self.mct = MCTree(time_limit, n_iteration)

    def select_move(self, state: GameState) -> tuple[int, int]:
        if self.parallel_mode == "root":
            move = run_root_parallel(
                state, self.n_workers, self.n_iteration, self.time_limit
            )
        elif self.parallel_mode == "tree":
            move = run_tree_parallel(
                state, self.n_workers, self.n_iteration, self.time_limit
            )
        else:
            move = self.mct.run(state)
        return move
