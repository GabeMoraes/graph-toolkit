from collections import deque, defaultdict

class Graph:
    def __init__(self, representation=None, data_path=None):
        self.node_to_idx = {}
        self.idx_to_node = {}
        if data_path is not None:
            with open(data_path, 'r') as f:
                n = int(f.readline())
                nodes = []
                edges = []
                for line in f:
                    parts = line.split()
                    if len(parts) < 2:
                        continue
                    u, v = parts[:2]
                    nodes.extend([u, v])
                    edges.append((u, v))
                unique_nodes = sorted(set(nodes))
                self.n = len(unique_nodes)
                self.node_to_idx = {name: i+1 for i, name in enumerate(unique_nodes)}
                self.idx_to_node = {i+1: name for i, name in enumerate(unique_nodes)}
                self.representation = representation
                if representation == 'adj_list':
                    self.adj_list = {name: [] for name in unique_nodes}
                elif representation == 'adj_matrix':
                    self.adj_matrix = [[0]*(self.n+1) for _ in range(self.n+1)]
                else:
                    raise ValueError('Unsupported representation')
                for u, v in edges:
                    self._add_edge(u, v)
            return
        self.representation = representation
        raise ValueError('num_vertices must be read from data_path. Please provide data_path.')

    def _add_edge(self, u, v):
        if self.representation == 'adj_list':
            self.adj_list[u].append(v)
            self.adj_list[v].append(u)
        else:
            i, j = self.node_to_idx[u], self.node_to_idx[v]
            self.adj_matrix[i][j] = 1
            self.adj_matrix[j][i] = 1

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
        with open(out_filepath, 'w', encoding='utf-8') as f:
            f.write(f"Número de vértices: {self.n}\n")
            f.write(f"Número de arestas: {self.num_edges()}\n")
            f.write(f"Grau médio: {self.average_degree():.2f}\n")
            f.write("Distribuição empírica do grau dos vértices:\n")
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
        with open(out_filepath, 'w', encoding='utf-8') as f:
            f.write("Vértice / pai / nível:\n")
            for v in self.adj_list.keys() if self.representation == 'adj_list' else self.idx_to_node.values():
                p = parent.get(v, None)
                l = level.get(v, -1)
                f.write(f"{v} {p} {l}\n")

    def connected_components(self):
        visited = set()
        components = []
        nodes = list(self.adj_list.keys()) if self.representation == 'adj_list' else list(self.idx_to_node.values())
        for v in nodes:
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
        components.sort(key=lambda c: len(c), reverse=True)
        return components

    def write_components(self, out_filepath):
        comps = self.connected_components()
        with open(out_filepath, 'w', encoding='utf-8') as f:
            f.write(f"Número de componentes: {len(comps)}\n")
            for comp in comps:
                f.write(f"Tamanho: {len(comp)} [{' '.join(map(str, comp))}]\n")

    def _neighbors(self, u):
        if self.representation == 'adj_list':
            return self.adj_list[u]
        else:
            idx = self.node_to_idx[u]
            return [self.idx_to_node[i] for i, val in enumerate(self.adj_matrix[idx]) if val and i != 0]