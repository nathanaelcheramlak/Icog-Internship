from typing import List, Tuple

DIRS_4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]
GRID_W, GRID_H = 28, 20  # columns, rows
Pos = Tuple[int, int]

def in_bounds(pos: Pos) -> bool:
    x, y = pos
    return 0 <= x < GRID_W and 0 <= y < GRID_H

def neighbors(pos: Pos) -> List[Pos]:
    x, y = pos
    res = [(x + dx, y + dy) for dx, dy in DIRS_4]
    return [p for p in res if in_bounds(p)]

def manhattan(a: Pos, b: Pos) -> int:
    return abs(a[0]-b[0]) + abs(a[1]-b[1])