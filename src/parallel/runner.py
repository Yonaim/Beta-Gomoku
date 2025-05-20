from src.parallel.strategy_base import StrategyBase
from src.game.gamestate import GameState
from src.game.mctree import MCTree


def parallel_mcts(
    state: GameState,
    strategy: StrategyBase,
) -> tuple[int, int]:
    """
    Common pipeline:
        1. Prepare the tree
        2. Perform parallel search using strategy.run()
        3. Determine the final move with strategy.best_move()
    """
    tree = MCTree(strategy.time_limit, strategy.n_iteration)
    strategy.run(state, tree)
    move = strategy.best_move(tree)
    assert move is not None, "parallel_mcts: best_move returned None"
    return move
