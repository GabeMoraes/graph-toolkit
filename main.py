import sys
from collections import deque, defaultdict

class Graph:
    def __init__(self, num_vertices, representation='adj_list'):
        self.n = num_vertices
        self.representation = representation
        if representation == 'adj_list':
            self.adj_list = {i: [] for i in range(1, num_vertices+1)}
        elif representation == 'adj_matrix':
            self.adj_matrix = [[0]*(num_vertices+1) for _ in range(num_vertices+1)]
        else:
            raise ValueError('Unsupported representation')

    def add_edge(self, u, v):
        if self.representation == 'adj_list':
            self.adj_list[u].append(v)
            self.adj_list[v].append(u)
        else:
            self.adj_matrix[u][v] = 1
            self.adj_matrix[v][u] = 1

    @classmethod
    def from_file(cls, filepath, representation='adj_list'):
        with open(filepath, 'r') as f:
            n = int(f.readline())
            graph = cls(n, representation)
            for line in f:
                parts = line.split()
                if len(parts) < 2:
                    continue
                u, v = map(int, parts[:2])
                graph.add_edge(u, v)
        return graph

    def num_edges(self):
        if self.representation == 'adj_list':
            return sum(len(neigh) for neigh in self.adj_list.values()) // 2
        else:
            count = 0
            for i in range(1, self.n+1):
                for j in range(i+1, self.n+1):
                    count += self.adj_matrix[i][j]
            return count

    def degree_distribution(self):
        dist = defaultdict(int)
        if self.representation == 'adj_list':
            for v in self.adj_list:
                d = len(self.adj_list[v])
                dist[d] += 1
        else:
            for i in range(1, self.n+1):
                d = sum(self.adj_matrix[i][1:])
                dist[d] += 1
        return dict(sorted(dist.items()))

    def average_degree(self):
        return 2 * self.num_edges() / self.n

    def write_summary(self, out_filepath):
        with open(out_filepath, 'w') as f:
            f.write(f"Number of vertices: {self.n}\n")
            f.write(f"Number of edges: {self.num_edges()}\n")
            f.write(f"Average degree: {self.average_degree():.2f}\n")
            f.write("Degree distribution:\n")
            for degree, count in self.degree_distribution().items():
                f.write(f"{degree}: {count}\n")

    def _search(self, start, method='bfs'):
        visited = set()
        parent = {start: None}
        level = {start: 0}
        if method == 'bfs':
            queue = deque([start])
            while queue:
                u = queue.popleft()
                for v in self._neighbors(u):
                    if v not in visited and v not in parent:
                        parent[v] = u
                        level[v] = level[u] + 1
                        queue.append(v)
                visited.add(u)
        else:  # dfs
            def dfs(u):
                visited.add(u)
                for v in self._neighbors(u):
                    if v not in visited:
                        parent[v] = u
                        level[v] = level[u] + 1
                        dfs(v)
            dfs(start)
        return parent, level

    def bfs(self, start):
        return self._search(start, 'bfs')

    def dfs(self, start):
        return self._search(start, 'dfs')

    def write_search_tree(self, start, method, out_filepath):
        parent, level = getattr(self, method)(start)
        with open(out_filepath, 'w') as f:
            f.write("Vertex Parent Level\n")
            for v in range(1, self.n+1):
                p = parent.get(v, None)
                l = level.get(v, -1)
                f.write(f"{v} {p} {l}\n")

    def connected_components(self):
        visited = set()
        components = []
        for v in range(1, self.n+1):
            if v not in visited:
                comp = []
                stack = [v]
                visited.add(v)
                while stack:
                    u = stack.pop()
                    comp.append(u)
                    for w in self._neighbors(u):
                        if w not in visited:
                            visited.add(w)
                            stack.append(w)
                components.append(comp)
        # sort by size desc
        components.sort(key=lambda c: len(c), reverse=True)
        return components

    def write_components(self, out_filepath):
        comps = self.connected_components()
        with open(out_filepath, 'w') as f:
            f.write(f"Number of components: {len(comps)}\n")
            for comp in comps:
                f.write(f"Size {len(comp)}: {' '.join(map(str, comp))}\n")

    def _neighbors(self, u):
        if self.representation == 'adj_list':
            return self.adj_list[u]
        else:
            return [i for i, val in enumerate(self.adj_matrix[u]) if val and i != 0]


# Example usage:
# python graph_lib.py input.txt
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python graph_lib.py <input_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    g = Graph.from_file(input_file, representation='adj_list')
    g.write_summary('graph_summary.txt')
    g.write_search_tree(start=1, method='bfs', out_filepath='bfs_tree.txt')
    g.write_search_tree(start=1, method='dfs', out_filepath='dfs_tree.txt')
    g.write_components('components.txt')
