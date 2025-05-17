from typing import Callable
from src.game.agent import Agent
from src.game.gamestate import GameState
from src.settings import N_ITERATION, TIME_LIMIT


def human_controller(state: GameState) -> tuple[int, int]:
    """사용자 입력을 받아 (y, x) 좌표 튜플을 반환"""
    while True:
        raw = input("좌표 (x y)를 입력하세요: ").strip()
        try:
            x_s, y_s = raw.split()
            x, y = int(x_s), int(y_s)
            return y, x  # board[row, col] = board[y, x]
        except Exception:
            print("유효한 형식으로 입력하세요. 예: 2 3\n")


def make_ai_controller(
    player_id: int,
    parallel_mode: str = "none",
    n_workers: int = 1
) -> Callable[[GameState], tuple[int, int]]:
    """
    - stateless하게, 매 턴마다 Agent 인스턴스를 생성
    - AI가 select한 좌표 튜플을 반환
    """

    def _ai_controller(state: GameState) -> tuple[int, int]:
        ai = Agent(
            player_id=player_id,
            time_limit=TIME_LIMIT,
            n_iteration=N_ITERATION,
            parallel_mode=parallel_mode,
            n_workers=n_workers,
        )
        print(f"AI가 다음 수를 생각 중입니다... (제한시간: {TIME_LIMIT}초)")
        move = ai.select_move(state)
        print("AI가 자신의 수를 놓았습니다.")
        return move

    return _ai_controller
