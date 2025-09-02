edges = [
    (0, 1),
    (2, 0)
]

def toposort(edges, num_nodes):
    graph = [[] for _ in range(num_nodes)]
    incoming = [0 for _ in range(num_nodes)]
    order = []
    for node, neighbor in edges:
        graph[node].append(neighbor)
        incoming[neighbor] += 1

    queue = []
    for i in range(num_nodes):
        if incoming[i] == 0:
            queue.append(i)

    while queue:
        node = queue.pop(0)
        order.append(node)
        for neighbor in graph[node]:
            incoming[neighbor] -= 1
            if incoming[neighbor] == 0:
                queue.append(neighbor)
    if len(order) != num_nodes:
        return []
    return order

print(toposort(edges, 3))