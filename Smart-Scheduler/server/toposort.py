# edges = [
#     (0, 1),
#     (2, 0)
# ]

# def toposort(edges, num_nodes):
#     graph = [[] for _ in range(num_nodes)]
#     incoming = [0 for _ in range(num_nodes)]
#     order = []
#     for node, neighbor in edges:
#         graph[node].append(neighbor)
#         incoming[neighbor] += 1

#     queue = []
#     for i in range(num_nodes):
#         if incoming[i] == 0:
#             queue.append(i)

#     while queue:
#         node = queue.pop(0)
#         order.append(node)
#         for neighbor in graph[node]:
#             incoming[neighbor] -= 1
#             if incoming[neighbor] == 0:
#                 queue.append(neighbor)
#     if len(order) != num_nodes:
#         return []
#     return order

# print(toposort(edges, 3))

from datetime import datetime

# ----------------------------
# Example schema (your format)
# ----------------------------
tasks = {
    1: {"name": "Task-A", "description": "Write Proposal"},
    2: {"name": "Task-B", "description": "Research Topic"},
    3: {"name": "Task-C", "description": "Collect References"},
}

priorities = {
    1: "High",
    2: "Medium",
    3: "Low",
}

# Map priority labels to numeric ranks (lower = higher priority)
priority_rank = {"Critical": 1, "High": 2, "Medium": 3, "Low": 4}

deadlines = {
    1: 20231202,
    2: 20231201,
    3: 20231205,
}

dependencies = {
    1: [2, 3],  # Task 1 depends on 2 and 3
    2: [],
    3: [2],
}

# ----------------------------
# Helper functions
# ----------------------------
def days_until(date_int):
    """Convert YYYYMMDD int to days from today."""
    date_str = str(date_int)
    d = datetime.strptime(date_str, "%Y%m%d")
    delta = (d - datetime.now()).days
    return max(0, delta)

def task_score(task_id):
    """Lower score = higher priority in scheduling."""
    prio = priority_rank[priorities[task_id]]
    days = days_until(deadlines[task_id])
    return (prio, days, task_id)  
    # priority dominates, then deadline, then ID to keep deterministic

# ----------------------------
# DFS-based Topological Sort
# ----------------------------
def dfs_schedule():
    visited = set()
    visiting = set()
    result = []

    def dfs(task_id):
        if task_id in visited:
            return
        if task_id in visiting:
            raise ValueError(f"Cycle detected involving task {task_id}")
        visiting.add(task_id)

        # Visit dependencies first
        for dep in sorted(dependencies[task_id], key=task_score):
            dfs(dep)

        visiting.remove(task_id)
        visited.add(task_id)
        result.append(task_id)

    # Start DFS on all tasks, but order roots by priority/deadline
    for tid in sorted(tasks.keys(), key=task_score):
        if tid not in visited:
            dfs(tid)

    return result

# ----------------------------
# Run the scheduler
# ----------------------------
if __name__ == "__main__":
    schedule = dfs_schedule()
    print("Optimal Schedule (by DFS + Priority + Deadline):")
    print(schedule)
    for tid in schedule:
        print(f"- {tasks[tid]['name']} "
              f"(Priority: {priorities[tid]}, Deadline: {deadlines[tid]})")
        
from datetime import datetime
from collections import defaultdict

# ----------------------------
# Example schema (your format)
# ----------------------------
tasks = {
    1: {"name": "Task-A", "description": "Write Proposal"},
    2: {"name": "Task-B", "description": "Research Topic"},
    3: {"name": "Task-C", "description": "Collect References"},
    4: {"name": "Task-D", "description": "Make Slides"},
}

priorities = {
    1: "High",
    2: "Medium",
    3: "Low",
    4: "High",
}

priority_rank = {"Critical": 1, "High": 2, "Medium": 3, "Low": 4}

deadlines = {
    1: 20231202,
    2: 20231201,
    3: 20231205,
    4: 20231207,
}

dependencies = {
    1: [2, 3],  # Task A depends on B and C
    2: [],
    3: [],
    4: [2],     # Task D depends on B
}

# ----------------------------
# Helpers
# ----------------------------
def days_until(date_int):
    date_str = str(date_int)
    d = datetime.strptime(date_str, "%Y%m%d")
    delta = (d - datetime.now()).days
    return max(0, delta)

def task_score(task_id):
    prio = priority_rank[priorities[task_id]]
    days = days_until(deadlines[task_id])
    return (prio, days, task_id)

# ----------------------------
# Grouped Topological Sort
# ----------------------------
def group_schedule():
    indeg = {tid: 0 for tid in tasks}
    graph = defaultdict(list)

    # Build graph
    for tid, deps in dependencies.items():
        for dep in deps:
            graph[dep].append(tid)
            indeg[tid] += 1

    schedule = []
    ready = [tid for tid, deg in indeg.items() if deg == 0]

    while ready:
        # Sort ready tasks by score → but keep them as a group
        ready.sort(key=task_score)
        schedule.append(ready[:])  # add group

        next_ready = []
        for tid in ready:
            for nbr in graph[tid]:
                indeg[nbr] -= 1
                if indeg[nbr] == 0:
                    next_ready.append(nbr)

        ready = next_ready

    # Check if cycle exists
    if any(deg > 0 for deg in indeg.values()):
        raise ValueError("Cycle detected in tasks!")

    return schedule

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    groups = group_schedule()
    print("Grouped Schedule (parallel tasks):")
    print(groups)
    for i, group in enumerate(groups, 1):
        print(f"Step {i}:")
        for tid in group:
            print(f"  - {tasks[tid]['name']} "
                  f"(Priority: {priorities[tid]}, Deadline: {deadlines[tid]})")

