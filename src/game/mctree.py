from __future__ import annotations

import math
import random
import time

from constants import PLAYER_1, PLAYER_2
from game.gamestate import GameState
from game.heuristic import ClassicHeuristic, Heuristic
from game.node import Node
from settings import DEBUG_MODE, MAX_DEPTH, N_ROLLOUT

C = math.sqrt(2)  # exploration constant (tune if necessary)
K_PB = 50  # bias-decay constant
K_BLEND = 3


class MCTree:
    root: Node
    time_limit: float
    n_iteration: int
    heuristic: Heuristic
    thread_safe: bool

    def __init__(
        self, time_limit: float, n_iteration: int, *, thread_safe: bool = False
    ):
        self.time_limit = time_limit
        self.n_iteration = n_iteration
        self.heuristic = ClassicHeuristic()
        self.thread_safe = thread_safe

    def run_single_thread(self, state: GameState) -> tuple[int, int]:
        self.root = Node(state, thread_safe=self.thread_safe)
        start = time.time()
        i = 0

        while i < self.n_iteration and time.time() - start < self.time_limit:
            self.do_iteration()
            i += 1

        if DEBUG_MODE:
            print(f"iteration 횟수: {i}")

        best_child = self.root.most_visited_child()
        assert best_child is not None
        return best_child.move

    def do_iteration(self):
        selected, is_terminal = self.select(self.root)
        if is_terminal:
            reward = self._terminal_value(selected.state)
            self.backpropagate(selected, reward)
        else:
            expanded = selected.expand()
            reward = self.blended_evaluation(
                expanded.state, N_ROLLOUT, MAX_DEPTH, K_BLEND
            )
            self.backpropagate(expanded, reward)

    def select(self, node: Node) -> tuple[Node, bool]:  # [selected Node, is_terminal]
        while True:
            if node.state.is_terminal:
                return node, True
            elif not node.is_fully_expanded():
                return node, False
            node = node.best_child(self._pb_ucb1)

    # average of rollout + heuristic
    def blended_evaluation(
        self, state: GameState, n_rollout: int, max_depth: int, k: float
    ) -> float:
        rollout_val = self.rollout_average(state, n_rollout, max_depth)
        heuristic_val = self.heuristic.evaluate(state, state.current_player)

        alpha = k / (k + n_rollout)
        return (1 - alpha) * rollout_val + alpha * heuristic_val

    # To reduce stack frame, use iterative update and do not call a function
    def backpropagate(self, node: Node | None, reward: float):
        cur_reward = reward
        while node is not None:
            node.update(cur_reward)
            cur_reward = -cur_reward
            node = node.parent

    # internal -----------------------------------------------------------------

    def rollout_average(
        self, state: GameState, n_rollout: int, max_depth: int
    ) -> float:
        total = 0.0
        for _ in range(n_rollout):
            total += self.rollout(state, max_depth)
        return total / n_rollout

    def rollout(self, start: GameState, max_depth: int) -> float:
        state = start.clone()
        for _ in range(max_depth):
            if state.is_terminal:
                break
            move = random.choice(state.legal_moves())
            state.apply_move(move)
            state.current_player = (
                PLAYER_2 if state.current_player == PLAYER_1 else PLAYER_1
            )
            # if DEBUG_MODE:
            #     state.print_board()
        return self.heuristic.evaluate(state, state.current_player)

    @staticmethod
    def _pb_ucb1(node: Node, k: float = K_PB, c: float = C):
        """progressive bias UCB1 (PB-UCB1)"""
        if node.n_visit == 0:
            return float("inf")

        parent_n = node.parent.n_visit if node.parent else 1
        q = node.total_reward / node.n_visit  # average reward
        h = node.heuristic  # heuristic

        alpha = k / (k + node.n_visit)
        exploitation = (
            1 - alpha
        ) * q + alpha * h  # 방문 횟수가 많아질 수록 heuristic의 영향은 줄어든다
        exploration = c * math.sqrt(math.log(parent_n) / node.n_visit)
        return exploitation + exploration

    @staticmethod
    def _ucb1(node: Node, c=math.sqrt(2)):
        if node.n_visit == 0:
            return float("inf")
        q = node.total_reward / node.n_visit
        parent_n = node.parent.n_visit if node.parent else 1
        exploration = c * math.sqrt(math.log(parent_n) / node.n_visit)
        return q + exploration

    @staticmethod
    def _terminal_value(state: GameState) -> float:
        assert state.is_terminal == True
        winner = state.winner
        if winner == -1:
            return 0.0
        return 1.0 if winner == state.current_player else -1.0
