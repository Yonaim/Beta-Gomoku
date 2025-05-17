from __future__ import annotations
import sys
import datetime

from typing import Callable

from settings import N_ITERATION, TIME_LIMIT
from constants import PLAYER_1, PLAYER_2
from ui.console_renderer import ConsoleRenderer
from game.agent import Agent
from game.gamestate import GameState

# ------------------------------------------------------------------ #
# 							Controller
# ------------------------------------------------------------------ #


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


def make_ai_controller(player_id: int) -> Callable[[GameState], tuple[int, int]]:
    """Agent 인스턴스를 감싸서 controller 형태로 반환"""
    ai = Agent(player_id=player_id, time_limit=TIME_LIMIT, n_iteration=N_ITERATION)

    def _ai_controller(state: GameState) -> tuple[int, int]:
        print("AI가 다음 수를 생각 중입니다...")
        return ai.select_move(state)

    return _ai_controller


# ------------------------------------------------------------------ #
# 					    	game loop
# ------------------------------------------------------------------ #


def play_game(
    controller_p1: Callable[[GameState], tuple[int, int]],
    controller_p2: Callable[[GameState], tuple[int, int]],
) -> None:
    state = GameState(current_player=PLAYER_1)
    renderer = ConsoleRenderer()

    controllers = {PLAYER_1: controller_p1, PLAYER_2: controller_p2}

    while not state.is_terminal:
        if state.current_player == PLAYER_1:
            print("플레이어 1의 차례입니다.")
        else:
            print("플레이어 2의 차례입니다.")
        renderer.draw(state.occupy_bitset, state.color_bitset)
        ctrl = controllers[state.current_player]

        move = ctrl(state)
        try:
            state.apply_move(move)
            print(f"놓은 위치: {int(move[1]), int(move[0])}")
        except ValueError:
            if ctrl is human_controller:  # human error
                print("\n잘못된 수입니다. 재입력해주세요\n")
                continue
            raise  # AI error
        state.current_player = (
            PLAYER_2 if state.current_player == PLAYER_1 else PLAYER_1
        )

    renderer.draw(state.occupy_bitset, state.color_bitset)
    winner = state.winner
    if winner == PLAYER_1:
        print("플레이어 1 승리!")
    elif winner == PLAYER_2:
        print("플레이어 2 승리!")
    else:
        print("무승부입니다.")


# ------------------------------------------------------------------ #
# 								mode
# ------------------------------------------------------------------ #


def play_human_vs_ai() -> None:
    play_game(human_controller, make_ai_controller(PLAYER_2))


def play_ai_vs_ai() -> None:
    play_game(make_ai_controller(PLAYER_1), make_ai_controller(PLAYER_2))


# ------------------------------------------------------------------ #
# 								main
# ------------------------------------------------------------------ #


def main() -> None:
    print("모드를 선택하세요:")
    print("1) 사람 vs AI")
    print("2) AI vs AI")
    while True:
        choice = input("모드 선택: ").strip()
        if choice == "1":
            play_human_vs_ai()
            break
        elif choice == "2":
            play_ai_vs_ai()
            break
        else:
            print("\n잘못된 입력입니다. 1 또는 2를 입력하세요.\n")


if __name__ == "__main__":
    if "--profile" in sys.argv:
        import cProfile, pstats

        now = datetime.datetime.now()
        path = f"./data/profile_{now.strftime('%Y%m%d_%H%M%S')}.txt"
        with open(path, "w") as f:
            prof = cProfile.Profile()
            prof.runcall(main)
            ps = pstats.Stats(prof, stream=f)
            ps.sort_stats("cumulative")
            ps.print_stats()
    else:
        main()
