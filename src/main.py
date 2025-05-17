from __future__ import annotations
import argparse
import multiprocessing
import sys
import datetime

from typing import Callable

from settings import DEBUG_MODE
from constants import PLAYER_1, PLAYER_2
from ui.console_renderer import BLACK_CHAR, WHITE_CHAR, ConsoleRenderer
from game.gamestate import GameState

from controllers import (
    human_controller,
    make_ai_controller,
)

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
            print(f"\n플레이어 1({BLACK_CHAR})의 차례입니다.")
        else:
            print(f"\n플레이어 2({WHITE_CHAR})의 차례입니다.")
        renderer.draw(state.occupy_bitset, state.color_bitset)
        ctrl = controllers[state.current_player]

        move = ctrl(state)
        try:
            state.apply_move(move)
            if DEBUG_MODE:
                print(f"놓은 위치: {int(move[0]), int(move[1])}")
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


def play_human_vs_ai(parallel_mode: str, n_workers: int) -> None:
    play_game(human_controller, make_ai_controller(PLAYER_2, parallel_mode, n_workers))


def play_ai_vs_ai(parallel_mode: str, n_workers: int) -> None:
    play_game(
        make_ai_controller(PLAYER_1, parallel_mode, n_workers),
        make_ai_controller(PLAYER_2, parallel_mode, n_workers),
    )


# ------------------------------------------------------------------ #
#                           argument parser
# ------------------------------------------------------------------ #


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Quarto 게임 병렬 모드 설정")
    parser.add_argument(
        "--parallel",
        choices=["none", "tree", "root"],
        default="none",
        help="none (default), tree (tree parallel), root (root parallel)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        help="The number of worker (core)",
    )
    args = parser.parse_args()
    if args.parallel not in ("none", "tree", "root"):
        parser.error("Wrong parallel mode")
    return args


# ------------------------------------------------------------------ #
# 								main
# ------------------------------------------------------------------ #


def main() -> None:
    args = parse_args()
    if args.workers is None:
        args.workers = multiprocessing.cpu_count()

    print("모드를 선택하세요:")
    print("1) 사람 vs AI")
    print("2) AI vs AI")
    while True:
        choice = input("모드 선택: ").strip()
        if choice == "1":
            play_human_vs_ai(parallel_mode=args.parallel, n_workers=args.workers)
            break
        elif choice == "2":
            play_ai_vs_ai(parallel_mode=args.parallel, n_workers=args.workers)
            break
        else:
            print("\n잘못된 입력입니다. 1 또는 2를 입력하세요.\n")


if __name__ == "__main__":
    if "--profile" in sys.argv:
        import cProfile, pstats
        sys.argv.remove("--profile")

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
