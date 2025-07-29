
from constants import DIRS, WIN_STONE_CNT
from game.gamestate import BOARD_N_BITS, GameState
from settings import BOARD_LENGTH
from src.game.bitset import bit, idx

CENTER_WEIGHT = 5  # bonus weight for central positions

# weight values of three cases: (open, half-open, blocked)
CLASSIC_HEURISTIC_WEIGHTS = {
    5: (10_000_000, 10_000_000, 10_000_000),
    4: (100_000, 10_000, 1_000),
    3: (5_000, 500, 50),
    2: (300, 30, 5),
    1: (1, 1, 1),
}


def heuristic_evaluate(state: GameState, player: int) -> float:
    my_score, opp_score = 0.0, 0.0
    center = BOARD_LENGTH // 2
    visited: list[int] = [0] * len(DIRS)

    occ = state.occupy_bitset
    for i in range(BOARD_N_BITS):
        if not (occ >> i) & 1:
            continue

        x, y = i % BOARD_LENGTH, i // BOARD_LENGTH
        stone_color = bit(state.color_bitset, x, y)

        dist = abs(x - center) + abs(y - center)
        center_bonus = CENTER_WEIGHT * (BOARD_LENGTH - dist)
        if stone_color == player:
            my_score += center_bonus
        else:
            opp_score += center_bonus

        for dir_idx, (dx, dy) in enumerate(DIRS):
            if (visited[dir_idx] >> i) & 1:
                continue

            length, left_open, right_open, line_bits = line_info(
                state, x, y, dx, dy, stone_color
            )

            visited[dir_idx] |= line_bits

            # early return: 즉시승/즉시패
            if length >= WIN_STONE_CNT:
                return 1e9 if stone_color == player else -1e9

            weight_tuple = CLASSIC_HEURISTIC_WEIGHTS.get(length, (0, 0, 0))
            open_cnt = int(left_open) + int(right_open)
            score = weight_tuple[2 - open_cnt]

            if stone_color == player:
                my_score += score
            else:
                # open 3
                if length == 3 and open_cnt == 2:
                    opp_score += score * 10
                # half-open 4
                elif length == 4 and open_cnt == 1:
                    opp_score += score * 3
                else:
                    opp_score += score

    return my_score - opp_score


def line_info(
    state: GameState, x: int, y: int, dx: int, dy: int, stone_color: int
) -> tuple[int, bool, bool, int]:
    """
    (x, y)에서 (dx, dy) 방향으로 같은 색 돌의 정보를 구한다.

    - length      : 연속된 돌 개수
    - left_open   : 시작점 반대쪽이 비어 있으면 True
    - right_open  : 끝점 우측이 비어있으면 True
    - line_bits   : 연속 구간을 나타내는 bitmask
    """
    length = 0
    line_bits = 0
    nx, ny = x, y

    while (
        0 <= nx < BOARD_LENGTH
        and 0 <= ny < BOARD_LENGTH
        and not state._is_empty(nx, ny)
        and (bit(state.color_bitset, nx, ny)) == stone_color
    ):
        length += 1
        line_bits |= 1 << idx(nx, ny)
        nx += dx
        ny += dy

    lx, ly = x - dx, y - dy
    left_open = (
        0 <= lx < BOARD_LENGTH and 0 <= ly < BOARD_LENGTH and state._is_empty(lx, ly)
    )
    right_open = (
        0 <= nx < BOARD_LENGTH and 0 <= ny < BOARD_LENGTH and state._is_empty(nx, ny)
    )

    return length, left_open, right_open, line_bits
