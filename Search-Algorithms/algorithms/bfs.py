from collections import deque
from typing import List, Tuple, Optional, Dict, Set, Generator
from utils.helpers import *

Pos = Tuple[int, int]

def bfs(start: Pos, goal: Pos, walls: Set[Pos]) -> Generator[dict, None, Optional[List[Pos]]]:
    if start == goal:
        yield {"frontier": [], "visited": [start], "current": start, "action": "done", "path": [start]}
        return [start]
    queue = deque([start])
    parent: Dict[Pos, Optional[Pos]] = {start: None}
    visited = set([start])

    while queue:
        current = queue.popleft()
        yield {"frontier": list(queue), "visited": list(visited), "current": current, "action": "pop"}
        if current == goal:
            break
        for n in neighbors(current):
            if n in walls or n in visited:
                continue
            visited.add(n)
            parent[n] = current
            queue.append(n)
            yield {"frontier": list(queue), "visited": list(visited), "current": current, "action": "push", "new": n}
    
    # reconstruct path
    if goal not in parent:
        yield {"frontier": list(queue), "visited": list(visited), "current": current, "action": "done", "path": None}
        return None
    
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
        
    path.reverse()
    yield {"frontier": list(queue), "visited": list(visited), "current": current, "action": "done", "path": path}
    return path
