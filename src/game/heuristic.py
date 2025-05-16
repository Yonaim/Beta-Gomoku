import numpy as np

from constants import BLACK, DIRS, EMPTY, WHITE, WIN_STONE_CNT
from game.gamestate import GameState
from settings import BOARD_LENGTH


class Heuristic:
    def evaluate(self, state: GameState, player: int) -> float:
        raise NotImplementedError

class ClassicHeuristic(Heuristic):
    """
    - 연속으로 놓인 돌의 수 N과 open, half-open, blocked 여부를 감안하여 점수 계산
    - Return value: [-1, 1]
    """

    # weight values of three cases: (open, half-open, blocked)
    WEIGHTS = {
        5: (1e6, 1e6, 1e6),
        4: (10000, 5000, 500),
        3: (1000, 500, 50),
        2: (100, 50, 5),
    }

    def evaluate(self, state, player: int) -> float:
        opp = BLACK if player == WHITE else WHITE
        my_score, opp_score = 0.0, 0.0
        visited = np.zeros_like(state.board, dtype=bool)

        for y in range(BOARD_LENGTH):
            for x in range(BOARD_LENGTH):
                stone = state.board[y, x]
                if stone == EMPTY:
                    continue

                for dx, dy in DIRS:
                    if visited[y, x]:
                        continue

                    length, left_open, right_open = self._line_info(
                        state, x, y, dx, dy, stone
                    )

                    nx, ny = x, y
                    for _ in range(length):
                        visited[ny, nx] = True
                        nx += dx
                        ny += dy

                    open_type = (left_open, right_open).count(
                        True
                    )  # 2=open, 1=half, 0=blocked
                    weights = self.WEIGHTS.get(length, (0, 0, 0))
                    score = weights[2 - open_type]

                    if length >= WIN_STONE_CNT:
                        return 1.0 if stone == player else -1.0

                    if stone == player:
                        my_score += score
                    else:
                        opp_score += score

        total = my_score + opp_score
        if total == 0:
            return 0.0
        return (my_score - opp_score) / (total + 1e-9)

    # --------------------------------------------------------------------- #
    #                   			internal                                #
    # --------------------------------------------------------------------- #

    @staticmethod
    def _line_info(state, x: int, y: int, dx: int, dy: int, stone: int):
        """
        (x, y)에서 (dx, dy) 방향으로 같은 돌이 연속된 길이와 양쪽 끝이 비어 있는지(open) 여부를 반환.
        """
        length = 0
        nx, ny = x, y
        while (
            0 <= nx < BOARD_LENGTH
            and 0 <= ny < BOARD_LENGTH
            and state.board[ny, nx] == stone
        ):
            length += 1
            nx += dx
            ny += dy

        lx, ly = x - dx, y - dy
        left_open = (
            0 <= lx < BOARD_LENGTH
            and 0 <= ly < BOARD_LENGTH
            and state.board[ly, lx] == EMPTY
        )

        right_open = (
            0 <= nx < BOARD_LENGTH
            and 0 <= ny < BOARD_LENGTH
            and state.board[ny, nx] == EMPTY
        )

        return length, left_open, right_open
