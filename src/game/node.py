from __future__ import annotations

from contextlib import nullcontext
import random
import threading
from typing import Optional


from constants import EPSILON
from game.gamestate import GameState
from src.game.heuristic import heuristic_evaluate
from src.settings import BOARD_LENGTH


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
        self._lock = threading.Lock() if thread_safe else nullcontext()
        self.heuristic = heuristic_evaluate(state, state.current_player)

    def update(self, reward: float):
        with self._lock:
            self.n_visit += 1
            self.total_reward += reward

    def expand(self, top_k: int = 3) -> "Node":
        """
        Create child node for untried move that has high heuristic score
        (Select random in Top k nodes)
        """
        tried = {c.move for c in self.children}
        untried = [
            m for m in self.state.legal_moves(radius=BOARD_LENGTH) if m not in tried
        ]
        if not untried:
            raise RuntimeError("expand on fully-expanded node")

        # (1) Calculate heuristic score of each move
        scored: list[tuple[float, tuple[int, int]]] = []
        player = self.state.current_player
        for mv in untried:
            s = self.state.clone()
            s.apply_move(mv)
            score = heuristic_evaluate(s, player)
            scored.append((score, mv))

        # (2) Select random node in top k nodes (if k=1, best)
        scored.sort(key=lambda x: x[0], reverse=True)
        k = min(top_k, len(scored))
        _, move = random.choice(scored[:k])

        # (3) Create child node
        child_state = self.state.clone()
        child_state.apply_move(move)
        child = Node(child_state, move, self, thread_safe=bool(self._lock))
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
        return len(self.children) == len(self.state.legal_moves(radius=BOARD_LENGTH))

    def most_visited_child(self) -> Node:
        return max(self.children, key=lambda ch: ch.n_visit)
