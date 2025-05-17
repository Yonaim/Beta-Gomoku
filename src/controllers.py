from typing import Callable
from src.game.agent import Agent
from src.game.gamestate import GameState
from src.settings import N_ITERATION, TIME_LIMIT


def human_controller(state: GameState) -> tuple[int, int]:
    """Receive user input and return a (y, x) coordinate tuple."""
    while True:
        raw = input("Enter coordinates (x y): ").strip()
        try:
            x_s, y_s = raw.split()
            x, y = int(x_s), int(y_s)
            return y, x  # board[row, col] = board[y, x]
        except Exception:
            print("Invalid format. Example: 2 3\n")


def make_ai_controller(
    player_id: int, parallel_mode: str = "none", n_workers: int = 1
) -> Callable[[GameState], tuple[int, int]]:
    """
    - Stateless: creates a new Agent instance every turn
    - Returns the coordinate tuple selected by the AI
    """

    def _ai_controller(state: GameState) -> tuple[int, int]:
        ai = Agent(
            player_id=player_id,
            time_limit=TIME_LIMIT,
            n_iteration=N_ITERATION,
            parallel_mode=parallel_mode,
            n_workers=n_workers,
        )
        print(
            f"AI is thinking about the next move... (time limit: {TIME_LIMIT} seconds)"
        )
        move = ai.select_move(state)
        print("AI has placed its move.")
        return move

    return _ai_controller
