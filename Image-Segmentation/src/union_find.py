class UnionFind:
    def __init__(self, n: int):
        self.n = int(n)
        self.parent = list(range(self.n))
        self.rank = [0] * self.n
        self.size = [1] * self.n

    def find(self, node: int) -> int:
        # Path compression (iterative)
        root = node
        while self.parent[root] != root:
            self.parent[root] = self.parent[self.parent[root]]
            root = self.parent[root]
        # compress path
        while node != root:
            parent = self.parent[node]
            self.parent[node] = root
            node = parent
        return root

    def union(self, a: int, b: int) -> int:
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return ra

        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra

        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.size[rb] = 0
        
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return ra

    def component_size(self, node: int) -> int:
        return self.size[self.find(node)]