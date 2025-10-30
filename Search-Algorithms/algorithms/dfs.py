from typing import List, Optional, Dict, Set, Generator
from utils.helpers import *

def dfs(start: Pos, goal: Pos, walls: Set[Pos]) -> Generator[dict, None, Optional[List[Pos]]]:
    if start == goal:
        yield {"frontier": [], "visited": [start], "current": start, "action": "done", "path": [start]}
        return [start]
    stack = [start]
    parent: Dict[Pos, Optional[Pos]] = {start: None}
    visited: Set[Pos] = set()
    frontier_set: Set[Pos] = {start}

    while stack:
        current = stack.pop()
        frontier_set.discard(current)
        if current in visited:
            # skip stale entries
            continue
        visited.add(current)
        yield {"frontier": list(frontier_set), "visited": list(visited), "current": current, "action": "pop"}
        if current == goal:
            break
        for n in neighbors(current):
            if n in walls or n in visited:
                continue
            if n not in parent:
                parent[n] = current
            stack.append(n)
            frontier_set.add(n)
            yield {"frontier": list(frontier_set), "visited": list(visited), "current": current, "action": "push", "new": n}
    
    if goal not in parent:
        yield {"frontier": list(stack), "visited": list(visited), "current": current, "action": "done", "path": None}
        return None
    
    # Path reconstruction
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    
    path.reverse()
    yield {"frontier": list(frontier_set), "visited": list(visited), "current": current, "action": "done", "path": path}
    return path
