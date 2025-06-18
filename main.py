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