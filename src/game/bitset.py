from settings import BOARD_LENGTH

"""최하위 비트(우측 끝)이 0번 인덱스"""


def idx(x: int, y: int) -> int:
    return y * BOARD_LENGTH + x


def bit(mask: int, x: int, y: int) -> int:
    return (mask >> idx(x, y)) & 1


def set_bit(mask: int, x: int, y: int) -> int:
    return (1 << idx(x, y)) | mask


def unset_bit(mask: int, x: int, y: int) -> int:
    return ~(1 << idx(x, y)) & mask
