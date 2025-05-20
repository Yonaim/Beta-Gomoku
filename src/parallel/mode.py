from enum import Enum


class ParallelMode(str, Enum):
    NONE = "none"
    TREE = "tree"
    ROOT = "root"
