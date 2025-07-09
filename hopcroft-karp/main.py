import time
import random
from graph import BipartiteGraph
from algorithms import HopcroftKarp, DFSMatching, BFSMatching

def print_results(name, matching_count, duration):
    print(f"{name:<20} | Emparelhamentos: {matching_count:<5} | Tempo: {duration:.4f} s")

def run_benchmark(U_size=1000, V_size=1000, min_edges=3, max_edges=10):
    print("Gerando grafo bipartido grande...")

    doctors = [f'D{i}' for i in range(U_size)]
    hospitals = [f'H{i}' for i in range(V_size)]

    graph = BipartiteGraph(doctors, hospitals)

    for doctor in doctors:
        k = random.randint(min_edges, max_edges)
        preferred = random.sample(hospitals, k)
        for hospital in preferred:
            graph.add_edge(doctor, hospital)

    print("Executando algoritmos de emparelhamento...\n")
    print(f"{'Algoritmo':<20} | {'Emparelhamentos':<15} | {'Tempo'}")
    print("-" * 60)

    results = {}

    # Hopcroft-Karp
    hk = HopcroftKarp(graph)
    start = time.time()
    hk_count, _ = hk.max_matching()
    duration = time.time() - start
    results['Hopcroft-Karp'] = hk_count
    print_results("Hopcroft-Karp", hk_count, duration)

    # DFS clássico
    dfs = DFSMatching(graph)
    start = time.time()
    dfs_count, _ = dfs.max_matching()
    duration = time.time() - start
    results['DFS'] = dfs_count
    print_results("DFS clássico", dfs_count, duration)

    # BFS clássico
    bfs = BFSMatching(graph)
    start = time.time()
    bfs_count, _ = bfs.max_matching()
    duration = time.time() - start
    results['BFS'] = bfs_count
    print_results("BFS clássico", bfs_count, duration)

    # Validação dos resultados
    print("\nValidação dos resultados:")
    unique_counts = set(results.values())
    if len(unique_counts) == 1:
        print("✓ Todos os algoritmos encontraram o mesmo número de emparelhamentos")
    else:
        print("✗ ERRO: Algoritmos produziram resultados diferentes!")
        for alg, count in results.items():
            print(f"  {alg}: {count}")

if __name__ == "__main__":
    run_benchmark()
