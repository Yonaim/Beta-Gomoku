import numpy as np

from constants import BLACK, DIRS, EMPTY, WHITE, WIN_STONE_CNT
from game.gamestate import BOARD_N_BITS, GameState
from settings import BOARD_LENGTH
from src.game.bitset import bit, idx


class Heuristic:
    def evaluate(self, state: GameState, player: int) -> float:
        raise NotImplementedError


class ClassicHeuristic(Heuristic):
    """
    - 점수 책정 기준
        - 연속으로 놓인 stone의 개수
        - 연속된 stone line의 개폐 여부: (open, half-open, blocked)
    - 방향 별로 visited bitset 존재하며, 같은 방향에서 같은 stone은 다시 세지 않음
    - Return value: [-1, 1]
    """
    
    # weight values of three cases: (open, half-open, blocked)
    WEIGHTS = {
        5: (1e6, 1e6, 1e6),
        4: (10000, 5000, 500),
        3: (5000, 100, 50),
        2: (100, 50, 5),
    }

    def evaluate(self, state: GameState, player: int) -> float:
        my_score, opp_score = 0.0, 0.0
        visited: list[int] = [0] * len(DIRS)

        occ = state.occupy_bitset
        for i in range(BOARD_N_BITS):
            if not (occ >> i) & 1:
                continue

            x, y = i % BOARD_LENGTH, i // BOARD_LENGTH
            stone_color = bit(state.color_bitset, x, y)

            for dir_idx, (dx, dy) in enumerate(DIRS):
                if (visited[dir_idx] >> i) & 1:
                    continue

                length, left_open, right_open, line_bits = self._line_info(
                    state, x, y, dx, dy, stone_color
                )

                visited[dir_idx] |= line_bits
                if length >= WIN_STONE_CNT:
                    return 1.0 if stone_color == player else -1.0
                weight_tuple = self.WEIGHTS.get(length, (0, 0, 0))
                open_cnt = (left_open, right_open).count(True)
                score = weight_tuple[2 - open_cnt]

                if stone_color == player:
                    my_score += score
                else:
                    opp_score += score

        total = my_score + opp_score
        if total == 0:
            return 0.0
        return (my_score - opp_score) / total

    # --------------------------------------------------------------------- #
    #                   			internal                                #
    # --------------------------------------------------------------------- #

    @staticmethod
    def _line_info(
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
            0 <= lx < BOARD_LENGTH
            and 0 <= ly < BOARD_LENGTH
            and state._is_empty(lx, ly)
        )
        right_open = (
            0 <= nx < BOARD_LENGTH
            and 0 <= ny < BOARD_LENGTH
            and state._is_empty(nx, ny)
        )

        return length, left_open, right_open, line_bits
