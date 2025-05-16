from __future__ import annotations
import time
import random
import math

from .constants import EMPTY
from .settings import MAX_DEPTH, N_ROLLOUT
from .node import Node
from .gamestate import GameState
from .heuristic import ClassicHeuristic, Heuristic

C = math.sqrt(2)  # exploration constant (tune if necessary)
K_PB = 50  # bias-decay constant
K_BLEND = 3

class MCTS:
    time_limit: float
    n_iteration: int
    heuristic: Heuristic

    def __init__(self, time_limit: float, n_iteration: int):
        self.time_limit = time_limit
        self.n_iteration = n_iteration
        self.heuristic = ClassicHeuristic()

    def run(self, state: GameState) -> tuple[int, int]:
        root = Node(state)  # root is the current game state
        start_time = time.time()
        i = 0

        while (i < self.n_iteration) and (time.time() - start_time < self.time_limit):
            selected, is_terminal = self.select(root)
            
            if (is_terminal):
                 reward = self.terminal_value(selected.state)
                 self.backpropagate(selected, reward)
            else:
                 expanded = selected.expand()
                 reward = self.blended_evaluation(expanded.state, N_ROLLOUT, MAX_DEPTH, K_BLEND)
                 self.backpropagate(expanded, reward)
            i += 1

        print(f"iteration 횟수: {i}")
        best_move = root.most_visited_child().move
        assert best_move != None
        return best_move

    def select(self, node: Node) -> tuple[Node, bool]:
        while True:
            if node.state.is_terminated():
                return node, True
            elif not node.is_fully_expanded():
                return node, False
            node = node.best_child(self.pb_ucb1)

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
            node.n_visit += 1
            node.total_reward += cur_reward
            cur_reward = -cur_reward
            node = node.parent

    # internal -----------------------------------------------------------------

    def rollout_average(
        self, state: GameState, n_rollout: int, max_depth: int) -> float:
        total = 0.0
        for _ in range(n_rollout):
            total += self.rollout(state, max_depth)
        return total / n_rollout

    def rollout(self, start: GameState, max_depth: int) -> float:
        state = start.clone()
        for _ in range(max_depth):
            if state.is_terminal:
                break
            move = random.choice(state.get_legal_moves())
            state.apply_move(move)
            state.current_player = (
                PLAYER_2 if state.current_player == PLAYER_1 else PLAYER_1
            )
            state.print_board()
        return self.heuristic.evaluate(state, state.current_player)

    # progressive bias UCB1 (PB-UCB1)
    def pb_ucb1(self, node: Node, k: float = K_PB, c: float = C):
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

    def ucb1(self, node: Node, c=math.sqrt(2)):
        if node.n_visit == 0:
            return float("inf")
        q = node.total_reward / node.n_visit
        parent_n = node.parent.n_visit if node.parent else 1
        exploration = c * math.sqrt(math.log(parent_n) / node.n_visit)
        return q + exploration

    def terminal_value(self, state: GameState) -> float:
        winner = state.get_winner()
        if winner == EMPTY:
            return 0.0
        return 1.0 if winner == state.current_player else -1.0
