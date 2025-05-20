from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from game.gamestate import GameState
    from game.mctree import MCTree


class StrategyBase(ABC):
    time_limit: float
    n_iteration: int

    @abstractmethod
    def run(self, state: "GameState", tree: "MCTree") -> None:
        pass

    @abstractmethod
    def best_move(self, tree: "MCTree") -> Tuple[int, int]:
        pass
