import heapq
from typing import List, Tuple, Optional, Dict, Set, Generator
from utils.helpers import *

Pos = Tuple[int, int]
def astar(start: Pos, goal: Pos, walls: Set[Pos], weights: Optional[Dict[Pos, float]] = None) -> Generator[dict, None, Optional[List[Pos]]]:
    if start == goal:
        yield {"frontier": [], "visited": [start], "current": start, "action": "done", "path": [start]}
        return [start]
    pq = []  # heap of (priority, cost_so_far, pos)
    min_w = 1.0
    if weights:
        # ensure admissibility by scaling heuristic by min edge weight
        positives = [w for w in weights.values() if w > 0]
        if positives:
            min_w = max(1e-6, min(positives))
    heapq.heappush(pq, (min_w * manhattan(start, goal), 0.0, start))
    parent: Dict[Pos, Optional[Pos]] = {start: None}
    cost_so_far: Dict[Pos, float] = {start: 0.0}
    visited = set()
    frontier_set = {start}

    while pq:
        _, cost, current = heapq.heappop(pq)
        frontier_set.discard(current)
        if current in visited:
            continue
        visited.add(current)
        yield {"frontier": list(frontier_set), "visited": list(visited), "current": current, "action": "pop"}
        if current == goal:
            break
        for n in neighbors(current):
            if n in walls:
                continue
            step_cost = 1.0
            if weights:
                step_cost = float(max(1e-6, weights.get(n, 1.0)))
            new_cost = cost_so_far[current] + step_cost
            if n not in cost_so_far or new_cost < cost_so_far[n]:
                cost_so_far[n] = new_cost
                priority = new_cost + min_w * manhattan(n, goal)
                heapq.heappush(pq, (priority, new_cost, n))
                frontier_set.add(n)
                parent[n] = current
                yield {"frontier": list(frontier_set), "visited": list(visited), "current": current, "action": "push", "new": n}
    if goal not in parent:
        yield {"frontier": list(frontier_set), "visited": list(visited), "current": current, "action": "done", "path": None}
        return None
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    yield {"frontier": list(frontier_set), "visited": list(visited), "current": current, "action": "done", "path": path}
    return path
