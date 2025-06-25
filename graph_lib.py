from collections import deque, defaultdict
import heapq

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
                    w = float(parts[2]) if len(parts) > 2 else 1.0
                    nodes.extend([u, v])
                    edges.append((u, v, w))
                unique_nodes = sorted(set(nodes))
                self.n = len(unique_nodes)
                self.node_to_idx = {name: i+1 for i, name in enumerate(unique_nodes)}
                self.idx_to_node = {i+1: name for i, name in enumerate(unique_nodes)}
                self.representation = representation
                if representation == 'adj_list':
                    self.adj_list = {name: [] for name in unique_nodes}
                elif representation == 'adj_matrix':
                    self.adj_matrix = [[0.0]*(self.n+1) for _ in range(self.n+1)]
                else:
                    raise ValueError('Unsupported representation')
                for u, v, w in edges:
                    self._add_edge(u, v, w)
            return
        self.representation = representation
        raise ValueError('num_vertices must be read from data_path. Please provide data_path.')

    def _add_edge(self, u, v, w):
        if self.representation == 'adj_list':
            self.adj_list[u].append((v, w))
            self.adj_list[v].append((u, w))
        else:
            i, j = self.node_to_idx[u], self.node_to_idx[v]
            self.adj_matrix[i][j] = w
            self.adj_matrix[j][i] = w

    def num_edges(self):
        if self.representation == 'adj_list':
            return sum(len(neigh) for neigh in self.adj_list.values()) // 2
        else:
            count = 0
            for i in range(1, self.n+1):
                for j in range(i+1, self.n+1):
                    if self.adj_matrix[i][j] != 0.0:
                        count += 1
            return count

    def degree_distribution(self):
        dist = defaultdict(int)
        if self.representation == 'adj_list':
            for v in self.adj_list:
                d = len(self.adj_list[v])
                dist[d] += 1
        else:
            for i in range(1, self.n+1):
                d = sum(1 for x in self.adj_matrix[i][1:] if x != 0.0)
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
                f.write(f"Grau {degree}: {count} vértice(s)\n")

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
        else:
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
            return [v for v, w in self.adj_list[u]]
        else:
            idx = self.node_to_idx[u]
            return [self.idx_to_node[i] for i, val in enumerate(self.adj_matrix[idx]) if val != 0.0 and i != 0]

    def _neighbors_with_weights(self, u):
        if self.representation == 'adj_list':
            return self.adj_list[u]
        else:
            idx = self.node_to_idx[u]
            return [(self.idx_to_node[i], self.adj_matrix[idx][i]) for i in range(1, self.n+1) if self.adj_matrix[idx][i] != 0.0]

    def write_edges(self, out_filepath):
        with open(out_filepath, 'w', encoding='utf-8') as f:
            f.write("Arestas (u, v, peso):\n")
            if self.representation == 'adj_list':
                written = set()
                for u in self.adj_list:
                    for v, w in self.adj_list[u]:
                        if (v, u) not in written:
                            f.write(f"{u} {v} {w}\n")
                            written.add((u, v))
            else:
                for i in range(1, self.n+1):
                    for j in range(i+1, self.n+1):
                        w = self.adj_matrix[i][j]
                        if w != 0.0:
                            f.write(f"{self.idx_to_node[i]} {self.idx_to_node[j]} {w}\n")

    def _has_negative_weights(self):
        if self.representation == 'adj_list':
            for u in self.adj_list:
                for v, w in self.adj_list[u]:
                    if w < 0:
                        return True
        else:
            for i in range(1, self.n+1):
                for j in range(1, self.n+1):
                    if self.adj_matrix[i][j] < 0:
                        return True
        return False

    def _is_unweighted(self):
        if self.representation == 'adj_list':
            for u in self.adj_list:
                for v, w in self.adj_list[u]:
                    if w != 1.0:
                        return False
        else:
            for i in range(1, self.n+1):
                for j in range(1, self.n+1):
                    if i != j and self.adj_matrix[i][j] not in (0.0, 1.0):
                        return False
        return True

    def shortest_path(self, source, target):
        if self._is_unweighted():
            queue = deque([source])
            visited = {source}
            parent = {source: None}
            dist = {source: 0}
            while queue:
                u = queue.popleft()
                if u == target:
                    break
                for v in self._neighbors(u):
                    if v not in visited:
                        visited.add(v)
                        parent[v] = u
                        dist[v] = dist[u] + 1
                        queue.append(v)
            if target not in dist:
                return float('inf'), []
            
            path = []
            v = target
            while v is not None:
                path.append(v)
                v = parent[v]
            path.reverse()
            return round(dist[target], 6), path
        else:
            if self._has_negative_weights():
                raise ValueError('Grafo possui pesos negativos, Dijkstra não pode ser usado.')
            heap = [(0.0, source, None)]
            dist = {source: 0.0}
            parent = {source: None}
            visited = set()
            while heap:
                d, u, p = heapq.heappop(heap)
                if u in visited:
                    continue
                visited.add(u)
                parent[u] = p
                if u == target:
                    break
                for v, w in self._neighbors_with_weights(u):
                    if v not in dist or dist[v] > d + w:
                        dist[v] = d + w
                        heapq.heappush(heap, (dist[v], v, u))
            if target not in dist:
                return float('inf'), []
            path = []
            v = target
            while v is not None:
                path.append(v)
                v = parent[v]
            path.reverse()
            return round(dist[target], 6), path

    def all_shortest_paths(self, source):
        if self._is_unweighted():
            queue = deque([source])
            visited = {source}
            parent = {source: None}
            dist = {source: 0}
            while queue:
                u = queue.popleft()
                for v in self._neighbors(u):
                    if v not in visited:
                        visited.add(v)
                        parent[v] = u
                        dist[v] = dist[u] + 1
                        queue.append(v)
            paths = {}
            for v in dist:
                path = []
                x = v
                while x is not None:
                    path.append(x)
                    x = parent[x]
                path.reverse()
                paths[v] = (round(dist[v], 6), path)
            return paths
        else:
            if self._has_negative_weights():
                raise ValueError('Grafo possui pesos negativos, Dijkstra não pode ser usado.')
            heap = [(0.0, source, None)]
            dist = {source: 0.0}
            parent = {source: None}
            visited = set()
            while heap:
                d, u, p = heapq.heappop(heap)
                if u in visited:
                    continue
                visited.add(u)
                parent[u] = p
                for v, w in self._neighbors_with_weights(u):
                    if v not in dist or dist[v] > d + w:
                        dist[v] = d + w
                        heapq.heappush(heap, (dist[v], v, u))
            paths = {}
            for v in dist:
                path = []
                x = v
                while x is not None:
                    path.append(x)
                    x = parent[x]
                path.reverse()
                paths[v] = (round(dist[v], 6), path)
            return paths