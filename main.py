from graph_lib import Graph

path = "./data.txt"

# Entrada e representação
graph = Graph(data_path=path, representation="adj_list")

# Saída
graph.write_summary(out_filepath="graph_summary.txt")

# Busca em profundidade
graph.write_search_tree(start="5", method="dfs", out_filepath="dfs_tree.txt")

# Busca em largura
graph.write_search_tree(start="5", method="bfs", out_filepath="bfs_tree.txt")

# Componentes conexos
graph.write_components(out_filepath="connected_components.txt")

# Caminho mínimo entre dois vértices
source = "1"
target = "5"
dist, path = graph.shortest_path(source, target)
print(f"Distância mínima entre {source} e {target}: {dist}")
print(f"Caminho: {' -> '.join(path)}")

# Caminho mínimo de um vértice para todos os outros vértices
all_paths = graph.all_shortest_paths(source)
print(f"Caminhos mínimos a partir de {source}:")
for target, (dist, path) in all_paths.items():
    print(f"Para {target}: Distância = {dist}, Caminho = {' -> '.join(path)}")