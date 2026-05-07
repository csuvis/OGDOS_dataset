import json
import os
import networkx as nx
from networkx.readwrite import json_graph

path = 'dataset'
dest_path = 'res'

for file_map in os.listdir(path):
    # Traverse the directories and process the graphs
    for root, dirs, files in os.walk(os.path.join(path, file_map)):
        for file in files:
            if file.endswith(".json"):  # Only process JSON files
                file_path = os.path.join(root, file)
                print(file_path)
                with open(file_path, 'r') as f:
                    data = json.load(f)

                # Convert the JSON data into a NetworkX graph
                G = json_graph.node_link_graph(data)

                # First, collect all self-loop edges
                self_loops = list(nx.selfloop_edges(G))
                # Then, remove these edges
                G.remove_edges_from(self_loops)

                # Convert to a simple graph to remove multiple edges
                G = nx.Graph(G)

                # Recalculate the number of nodes, edges, and the node-to-edge ratio
                node_count = G.number_of_nodes()
                edge_count = G.number_of_edges()
                edge_ratio = edge_count / node_count if node_count != 0 else 0

                # Create a new filename based on the recalculated values
                original_name = os.path.basename(file_path).replace('.json', '')
                new_filename = f"{node_count}-{edge_count}-1-{round(edge_ratio, 5)}-{original_name}.json"
                res_file_path = os.path.join(dest_path, file_map)
                os.makedirs(res_file_path, exist_ok=True)
                new_filepath = os.path.join(res_file_path, new_filename)

                # Save the cleaned graph back to a new JSON file
                new_data = json_graph.node_link_data(G)
                with open(new_filepath, 'w') as f:
                    json.dump(new_data, f, indent=2)
