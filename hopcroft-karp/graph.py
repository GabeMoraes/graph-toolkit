from collections import defaultdict
from typing import List, Dict, Set

class BipartiteGraph:
    def __init__(self, U: List[str], V: List[str]):
        """
        Inicializa o grafo bipartido com dois conjuntos disjuntos de vértices:
        U: lado esquerdo (ex: médicos)
        V: lado direito (ex: hospitais)
        """
        self.U: List[str] = U
        self.V: List[str] = V
        self.adj: Dict[str, List[str]] = defaultdict(list)

    def add_edge(self, u: str, v: str):
        """
        Adiciona uma aresta entre um vértice u de U e um vértice v de V.
        """
        if u not in self.U:
            raise ValueError(f"Vértice {u} não está no conjunto U.")
        if v not in self.V:
            raise ValueError(f"Vértice {v} não está no conjunto V.")
        self.adj[u].append(v)

    def neighbors(self, u: str) -> List[str]:
        """
        Retorna a lista de vizinhos (vértices de V) conectados a u (vértice de U).
        """
        return self.adj[u]

    def get_U(self) -> List[str]:
        return self.U

    def get_V(self) -> List[str]:
        return self.V
