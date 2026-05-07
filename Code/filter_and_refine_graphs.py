import json
import os
import random
import networkx as nx
from networkx.readwrite import json_graph

# Target node scale and edge-to-node ratio distributions
target_scales = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
                 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
                 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000,
                 55000, 60000, 65000, 70000, 75000, 80000, 85000, 90000,
                 95000, 100000, 110000, 120000, 130000, 140000, 150000,
                 160000, 170000, 180000, 190000, 200000]

target_edge_ratios = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# Load graph dataset from a JSON file
def load_graph(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return json_graph.node_link_graph(data)


# Save the graph to a new JSON file after adjustments
def save_graph(G, original_name, output_directory):
    node_count = G.number_of_nodes()
    edge_count = G.number_of_edges()
    edge_ratio = edge_count / node_count

    # Create a new filename based on the adjusted node count, edge count, and edge ratio
    new_filename = f"{node_count}-{edge_count}-1-{round(edge_ratio, 5)}-{original_name}.json"
    output_path = os.path.join(output_directory, new_filename)

    data = json_graph.node_link_data(G)
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Graph adjusted and saved to {output_path}")


# Find the closest node scale and edge-to-node ratio, and return them
def find_closest_scale_and_ratio(node_count, edge_count):
    closest_scale = None
    closest_ratio = None

    current_edge_ratio = edge_count / node_count
    any_scale_within_limit = False

    # First step: find the closest node scale, regardless of whether it's larger or smaller
    min_scale_diff = float('inf')
    for target_scale in target_scales:
        any_scale_within_limit = True
        scale_diff = abs(target_scale - node_count)
        if scale_diff < min_scale_diff:
            min_scale_diff = scale_diff
            closest_scale = target_scale

    # Second step: find the closest edge-to-node ratio among the closest node scales
    min_ratio_diff = float('inf')
    for target_ratio in target_edge_ratios:
        ratio_diff = abs(target_ratio - current_edge_ratio)

        # Only select the target ratio where the difference is less than or equal to 1
        if ratio_diff < min_ratio_diff and abs(target_ratio - current_edge_ratio) <= 1:
            min_ratio_diff = ratio_diff
            closest_ratio = target_ratio

    # If no suitable edge ratio is found, return None
    if closest_ratio is None:
        print(f"No suitable edge-to-node ratio found, current ratio: {current_edge_ratio}")
        return None, None

    return closest_scale, closest_ratio


# Adjust the number of edges by removing edges while ensuring the number of connected components doesn't increase
def adjust_edges(G, target_scale, target_ratio):
    node_count = G.number_of_nodes()
    target_edges = int(target_scale * target_ratio)
    current_edges = G.number_of_edges()

    if current_edges > target_edges:
        # If the number of edges is greater than the target, remove some edges
        edges_to_remove = current_edges - target_edges
        edges = list(G.edges)

        # Get all triangles in the graph
        triangles = list(nx.triangles(G).values())

        # Randomly select edges_to_remove edges to delete
        for _ in range(edges_to_remove):
            edge = random.choice(edges)
            u, v = edge

            # Check if this edge is part of any triangle
            common_neighbors = list(nx.common_neighbors(G, u, v))
            if common_neighbors:  # If common neighbors exist, the edge is part of at least one triangle
                # Skip deleting this edge if it is part of a triangle
                continue

            # Before removing the edge, check if it would increase the number of connected components
            original_components = list(nx.connected_components(G))
            G.remove_edge(*edge)
            new_components = list(nx.connected_components(G))

            # If removing the edge increases the number of connected components, restore it
            if len(new_components) > len(original_components):
                G.add_edge(*edge)
            else:
                edges.remove(edge)  # Remove the deleted edge from the list

    return G


# Remove nodes with lower degrees to ensure the node count matches the target and avoid adding new connected components
def adjust_nodes(G, target_scale):
    current_nodes = G.number_of_nodes()

    if current_nodes > target_scale:
        nodes_to_remove = current_nodes - target_scale
        # Sort nodes by degree and remove nodes with the lowest degrees
        sorted_nodes = sorted(G.degree, key=lambda x: x[1])  # Sort nodes by degree
        nodes = [n for n, d in sorted_nodes[:nodes_to_remove]]  # Select nodes to remove
        for node in nodes:
            # Check if removing this node would increase the number of connected components
            original_components = list(nx.connected_components(G))
            G.remove_node(node)
            new_components = list(nx.connected_components(G))

            # If removing the node increases the number of connected components, restore the node
            if len(new_components) > len(original_components):
                G.add_node(node)
                for neighbor in G.neighbors(node):
                    G.add_edge(node, neighbor)
                print(f"Skipped removing node {node}, it caused a new connected component")
    elif current_nodes < target_scale:
        # If there are fewer nodes than the target, additional logic can be added (if adding nodes is allowed)
        print(f"Cannot increase node count, current {current_nodes} < target {target_scale}")
    return G


# Main function to process and adjust the graph
def process_graph(json_file, output_directory):
    G = load_graph(json_file)

    node_count = G.number_of_nodes()
    edge_count = G.number_of_edges()

    # Find the closest node scale and edge ratio
    closest_scale, closest_ratio = find_closest_scale_and_ratio(node_count, edge_count)

    # Skip if no suitable edge-to-node ratio is found
    if closest_scale is None or closest_ratio is None:
        print(f"Skipping dataset: {json_file}")
        return

    # Adjust node count and edge count
    G = adjust_nodes(G, closest_scale)
    G = adjust_edges(G, closest_scale, closest_ratio)

    # Calculate the adjusted node count and edge ratio
    adjusted_node_count = G.number_of_nodes()
    adjusted_edge_count = G.number_of_edges()
    adjusted_edge_ratio = adjusted_edge_count / adjusted_node_count

    # Error control: Check if the adjusted node count and edge ratio are within acceptable limits
    scale_diff = abs(adjusted_node_count - closest_scale) / closest_scale
    ratio_diff = abs(adjusted_edge_ratio - closest_ratio)

    if scale_diff < 0.05 and ratio_diff < 0.05:
        # If the error is within the allowed range, save the adjusted graph
        original_name = json_file.split('\\')[-1].replace('.json', '')  # Remove file path and extension
        save_graph(G, original_name, output_directory)
    else:
        print(f"Error too large, skipping. Scale diff: {scale_diff}, Ratio diff: {ratio_diff}")


# Traverse the folder and process the graphs
path = 'dataset_simple_graph_refine'
dest_path = 'res_20241017_simple_graph_refine'

for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".json"):  # Process only JSON files
            file_path = os.path.join(root, file)

            # Determine the output directory structure (preserve original subfolder structure)
            relative_path = os.path.relpath(root, path)
            output_directory = os.path.join(dest_path, relative_path)

            os.makedirs(output_directory, exist_ok=True)

            # Call the processing function
            process_graph(file_path, output_directory)
