import time
import random
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from graph import BipartiteGraph
from algorithms import HopcroftKarp, DFSMatching, BFSMatching

def generate_graph(U_size, V_size, min_edges=3, max_edges=10, seed=None):
    """Gera um grafo bipartido com tamanho e densidade especificados"""
    if seed is not None:
        random.seed(seed)
    
    doctors = [f'D{i}' for i in range(U_size)]
    hospitals = [f'H{i}' for i in range(V_size)]
    
    graph = BipartiteGraph(doctors, hospitals)
    
    for doctor in doctors:
        k = random.randint(min_edges, max_edges)
        preferred = random.sample(hospitals, min(k, len(hospitals)))
        for hospital in preferred:
            graph.add_edge(doctor, hospital)
    
    return graph

def run_single_test(graph):
    """Executa todos os algoritmos em um grafo e retorna os tempos e resultados"""
    results = {}
    times = {}
    
    # Hopcroft-Karp
    hk = HopcroftKarp(graph)
    start = time.time()
    hk_count, _ = hk.max_matching()
    times['Hopcroft-Karp'] = time.time() - start
    results['Hopcroft-Karp'] = hk_count
    
    # DFS clássico
    dfs = DFSMatching(graph)
    start = time.time()
    dfs_count, _ = dfs.max_matching()
    times['DFS'] = time.time() - start
    results['DFS'] = dfs_count
    
    # BFS clássico
    bfs = BFSMatching(graph)
    start = time.time()
    bfs_count, _ = bfs.max_matching()
    times['BFS'] = time.time() - start
    results['BFS'] = bfs_count
    
    return results, times

def benchmark_by_size(sizes=[100, 200, 500, 1000, 1500, 2000], runs_per_size=5):
    """Executa benchmark variando o tamanho do grafo"""
    print("Executando benchmark por tamanho de grafo...")
    
    size_results = defaultdict(list)
    
    for size in sizes:
        print(f"Testando tamanho {size}x{size}...")
        
        for run in range(runs_per_size):
            # Usar seed diferente para cada execução
            graph = generate_graph(size, size, seed=run * 1000 + size)
            results, times = run_single_test(graph)
            
            # Verificar se todos os algoritmos encontraram o mesmo resultado
            unique_counts = set(results.values())
            if len(unique_counts) > 1:
                print(f"  AVISO: Resultados diferentes no tamanho {size}, run {run}: {results}")
            
            for alg, time_taken in times.items():
                size_results[alg].append((size, time_taken))
    
    return size_results

def benchmark_multiple_runs(graph_size=1000, num_runs=20):
    """Executa múltiplas rodadas no mesmo tamanho de grafo"""
    print(f"Executando {num_runs} rodadas com grafo {graph_size}x{graph_size}...")
    
    run_results = defaultdict(list)
    
    for run in range(num_runs):
        graph = generate_graph(graph_size, graph_size, seed=run * 42)
        results, times = run_single_test(graph)
        
        # Verificar consistência
        unique_counts = set(results.values())
        if len(unique_counts) > 1:
            print(f"  AVISO: Resultados diferentes na rodada {run}: {results}")
        
        for alg, time_taken in times.items():
            run_results[alg].append(time_taken)
        
        if (run + 1) % 5 == 0:
            print(f"  Completadas {run + 1}/{num_runs} rodadas")
    
    return run_results

def plot_size_comparison(size_results):
    """Gera gráfico comparando algoritmos por tamanho"""
    plt.figure(figsize=(12, 8))
    
    algorithms = ['Hopcroft-Karp', 'DFS', 'BFS']
    colors = ['blue', 'red', 'green']
    
    for i, alg in enumerate(algorithms):
        if alg in size_results:
            sizes = [x[0] for x in size_results[alg]]
            times = [x[1] for x in size_results[alg]]
            
            # Agrupar por tamanho e calcular média
            size_groups = defaultdict(list)
            for size, time_val in zip(sizes, times):
                size_groups[size].append(time_val)
            
            avg_sizes = sorted(size_groups.keys())
            avg_times = [np.mean(size_groups[size]) for size in avg_sizes]
            std_times = [np.std(size_groups[size]) for size in avg_sizes]
            
            plt.errorbar(avg_sizes, avg_times, yerr=std_times, 
                        label=alg, color=colors[i], marker='o', linewidth=2)
    
    plt.xlabel('Tamanho do Grafo (n×n)')
    plt.ylabel('Tempo de Execução (segundos)')
    plt.title('Comparação de Performance por Tamanho do Grafo')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.yscale('log')  # Escala logarítmica para melhor visualização
    plt.tight_layout()
    plt.savefig('benchmark_por_tamanho.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_run_variation(run_results):
    """Gera gráfico mostrando variação entre execuções"""
    plt.figure(figsize=(14, 10))
    
    # Subplot 1: Tempos por execução
    plt.subplot(2, 2, 1)
    algorithms = ['Hopcroft-Karp', 'DFS', 'BFS']
    colors = ['blue', 'red', 'green']
    
    for i, alg in enumerate(algorithms):
        if alg in run_results:
            runs = range(1, len(run_results[alg]) + 1)
            plt.plot(runs, run_results[alg], 
                    label=alg, color=colors[i], marker='o', alpha=0.7)
    
    plt.xlabel('Número da Execução')
    plt.ylabel('Tempo (segundos)')
    plt.title('Variação de Tempo por Execução')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Subplot 2: Box plot
    plt.subplot(2, 2, 2)
    data_for_box = []
    labels_for_box = []
    
    for alg in algorithms:
        if alg in run_results:
            data_for_box.append(run_results[alg])
            labels_for_box.append(alg)
    
    plt.boxplot(data_for_box, labels=labels_for_box)
    plt.ylabel('Tempo (segundos)')
    plt.title('Distribuição dos Tempos')
    plt.grid(True, alpha=0.3)
    
    # Subplot 3: Estatísticas
    plt.subplot(2, 2, 3)
    stats_text = "Estatísticas:\n\n"
    
    for alg in algorithms:
        if alg in run_results:
            times = run_results[alg]
            stats_text += f"{alg}:\n"
            stats_text += f"  Média: {np.mean(times):.4f}s\n"
            stats_text += f"  Desvio: {np.std(times):.4f}s\n"
            stats_text += f"  Min: {np.min(times):.4f}s\n"
            stats_text += f"  Max: {np.max(times):.4f}s\n\n"
    
    plt.text(0.1, 0.9, stats_text, transform=plt.gca().transAxes, 
             fontfamily='monospace', fontsize=10, verticalalignment='top')
    plt.axis('off')
    plt.title('Estatísticas Detalhadas')
    
    # Subplot 4: Speedup relativo
    plt.subplot(2, 2, 4)
    if 'Hopcroft-Karp' in run_results and 'DFS' in run_results and 'BFS' in run_results:
        hk_times = np.array(run_results['Hopcroft-Karp'])
        dfs_times = np.array(run_results['DFS'])
        bfs_times = np.array(run_results['BFS'])
        
        runs = range(1, len(hk_times) + 1)
        speedup_dfs = dfs_times / hk_times
        speedup_bfs = bfs_times / hk_times
        
        plt.plot(runs, speedup_dfs, label='DFS vs HK', color='red', marker='s')
        plt.plot(runs, speedup_bfs, label='BFS vs HK', color='green', marker='^')
        plt.axhline(y=1, color='blue', linestyle='--', alpha=0.5, label='Hopcroft-Karp baseline')
        
        plt.xlabel('Número da Execução')
        plt.ylabel('Razão de Tempo (algoritmo/HK)')
        plt.title('Speedup Relativo ao Hopcroft-Karp')
        plt.legend()
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('benchmark_variacao.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    print("=== Análise Comparativa de Algoritmos de Emparelhamento ===\n")
    
    # Benchmark 1: Variação por tamanho
    print("1. Executando benchmark por tamanho...")
    size_results = benchmark_by_size(sizes=[100, 200, 500, 800, 1000], runs_per_size=3)
    plot_size_comparison(size_results)
    
    print("\n" + "="*60 + "\n")
    
    # Benchmark 2: Múltiplas execuções no mesmo tamanho
    print("2. Executando múltiplas rodadas...")
    run_results = benchmark_multiple_runs(graph_size=1000, num_runs=15)
    plot_run_variation(run_results)
    
    print("\n=== Análise Finalizada ===")
    print("Gráficos salvos:")
    print("- benchmark_por_tamanho.png")
    print("- benchmark_variacao.png")

if __name__ == "__main__":
    main()
