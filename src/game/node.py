from __future__ import annotations

from contextlib import nullcontext
import random
import threading
from typing import Optional


from constants import EPSILON
from game.gamestate import GameState
from game.heuristic import ClassicHeuristic


class Node:
    state: GameState
    move: tuple[int, int]
    parent: Node | None
    children: list[Node]
    total_reward: float
    n_visit: int
    heuristic: float
    thread_safe: bool

    def __init__(
        self,
        state: GameState,
        move=(-1, -1),
        parent: Optional[Node] = None,
        *,
        thread_safe: bool = False,
    ):
        if parent:
            self.move = move
        self.state = state
        self.parent = parent
        self.children: list[Node] = []
        self.total_reward: float = 0.0
        self.n_visit: int = 0
        self.heuristic = ClassicHeuristic().evaluate(state, state.current_player)
        self._lock = threading.Lock() if thread_safe else nullcontext()

    def update(self, reward: float):
        with self._lock:
            self.n_visit += 1
            self.total_reward += reward

    def expand(self) -> "Node":
        tried = {c.move for c in self.children}
        untried = [m for m in self.state.legal_moves() if m not in tried]
        if not untried:
            raise RuntimeError("expand on fully-expanded node")

        move = random.choice(untried)
        child_state = self.state.clone()
        child_state.apply_move(move)

        child = Node(child_state, move, self)
        with self._lock:
            self.children.append(child)
        return child

    def best_child(self, score_fn):
        best_score = -float("inf")
        best_nodes = []
        for child in self.children:
            score = score_fn(child)
            if score > best_score + EPSILON:
                best_score = score
                best_nodes = [child]
            elif abs(score - best_score) < EPSILON:
                best_nodes.append(child)
        return random.choice(best_nodes)

    def is_fully_expanded(self) -> bool:
        return len(self.children) == len(self.state.legal_moves())

    def most_visited_child(self) -> Node:
        return max(self.children, key=lambda ch: ch.n_visit)
