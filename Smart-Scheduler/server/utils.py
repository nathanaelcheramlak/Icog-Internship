def has_cycle(current_graph, task_id, dependencies):
    """
    Detect if there is a cycle in the task dependency graph.
    Returns (has_cycle, cycle_path) where cycle_path is the list of nodes forming the cycle.
    """

    # Build adjacency list from DirectedEdge atoms
    edges = [str(atom) for atom in current_graph if str(atom).startswith("(DirectedEdge")]
    for dep in dependencies:
        edges.append(f"(DirectedEdge {dep} {task_id})")

    graph = {}
    for edge in edges:
        # Format: (DirectedEdge from to)
        parts = edge.strip("()").split()
        _, src, dst = parts
        src, dst = int(src), int(dst)
        graph.setdefault(src, []).append(dst)

    visited = set()
    stack = []
    cycle_path = []

    def dfs(node):
        nonlocal cycle_path
        if node in stack:
            # cycle detected → slice path from first occurrence to end
            idx = stack.index(node)
            cycle_path = stack[idx:] + [node]
            return True
        if node in visited:
            return False

        visited.add(node)
        stack.append(node)

        for neighbor in graph.get(node, []):
            if dfs(neighbor):
                return True

        stack.pop()
        return False

    # Check every node
    for node in graph:
        if dfs(node):
            return True, cycle_path
    return False, []

# --- Example usage ---
# ans, path = has_cycle(
#     ["(DirectedEdge 1 2)", "(DirectedEdge 2 3)", "(DirectedEdge 2 4)"],
#     1, [3]
# )
# print("Cycle?", ans)
# print("Cycle Path:", path)
