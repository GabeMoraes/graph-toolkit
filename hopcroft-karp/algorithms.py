from collections import deque
from graph import BipartiteGraph

class HopcroftKarp:
    def __init__(self, graph: BipartiteGraph):
        self.graph = graph
        self.U = graph.get_U()
        self.V = graph.get_V()
        self.adj = graph.adj
        self.pair_U = {u: None for u in self.U}
        self.pair_V = {v: None for v in self.V}
        self.dist = {}

    def bfs(self):
        queue = deque()
        for u in self.U:
            if self.pair_U[u] is None:
                self.dist[u] = 0
                queue.append(u)
            else:
                self.dist[u] = float('inf')
        found = False
        while queue:
            u = queue.popleft()
            for v in self.adj[u]:
                match_u = self.pair_V[v]
                if match_u is None:
                    found = True
                elif self.dist[match_u] == float('inf'):
                    self.dist[match_u] = self.dist[u] + 1
                    queue.append(match_u)
        return found

    def dfs(self, u):
        for v in self.adj[u]:
            match_u = self.pair_V[v]
            if match_u is None or (self.dist[match_u] == self.dist[u] + 1 and self.dfs(match_u)):
                self.pair_U[u] = v
                self.pair_V[v] = u
                return True
        self.dist[u] = float('inf')
        return False

    def max_matching(self):
        matching = 0
        while self.bfs():
            for u in self.U:
                if self.pair_U[u] is None and self.dfs(u):
                    matching += 1
        return matching, self.pair_U


class DFSMatching:
    def __init__(self, graph: BipartiteGraph):
        self.graph = graph
        self.U = graph.get_U()
        self.V = graph.get_V()
        self.adj = graph.adj
        self.pair_U = {u: None for u in self.U}
        self.pair_V = {v: None for v in self.V}

    def dfs(self, u, visited):
        for v in self.adj[u]:
            if v not in visited:
                visited.add(v)
                if self.pair_V[v] is None or self.dfs(self.pair_V[v], visited):
                    self.pair_U[u] = v
                    self.pair_V[v] = u
                    return True
        return False

    def max_matching(self):
        matching = 0
        for u in self.U:
            if self.pair_U[u] is None:
                visited = set()
                if self.dfs(u, visited):
                    matching += 1
        return matching, self.pair_U


class BFSMatching:
    def __init__(self, graph: BipartiteGraph):
        self.graph = graph
        self.U = graph.get_U()
        self.V = graph.get_V()
        self.adj = graph.adj
        self.pair_U = {u: None for u in self.U}
        self.pair_V = {v: None for v in self.V}

    def find_augmenting_path(self):
        """Encontra um caminho aumentante usando BFS (algoritmo Edmonds-Karp)"""
        from collections import deque
        
        queue = deque()
        parent = {}
        
        # Adicionar todos os vértices não emparelhados de U à fila
        for u in self.U:
            if self.pair_U[u] is None:
                queue.append(u)
                parent[u] = None
        
        while queue:
            u = queue.popleft()
            
            # Para cada vizinho v de u
            for v in self.adj[u]:
                if v not in parent:  # Se v ainda não foi visitado
                    parent[v] = u
                    matched_u = self.pair_V[v]
                    
                    if matched_u is None:
                        # Encontrou vértice não emparelhado em V - caminho aumentante encontrado
                        return self.reconstruct_path(parent, v)
                    else:
                        # v está emparelhado, adiciona seu par à busca
                        if matched_u not in parent:
                            parent[matched_u] = v
                            queue.append(matched_u)
        
        return None

    def reconstruct_path(self, parent, end_v):
        """Reconstrói o caminho aumentante a partir dos parents"""
        path = []
        current = end_v
        
        while current is not None and parent[current] is not None:
            u = parent[current]
            path.append((u, current))
            # Navegar para o próximo par no caminho
            current = parent.get(u)
            
        return list(reversed(path))

    def max_matching(self):
        matching = 0
        
        while True:
            path = self.find_augmenting_path()
            if path is None:
                break
            
            # Aplicar o caminho aumentante (inverter arestas)
            for u, v in path:
                self.pair_U[u] = v
                self.pair_V[v] = u
            matching += 1
            
        return matching, self.pair_U
