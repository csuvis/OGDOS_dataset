import os
import json
import shutil  # Used for file copying

# Path settings
path = 'dataset/data'  # Original dataset directory
dest_pos = 'res_simple_graph'  # Target directory for simple graphs
special_folder = 'res_complex_graph'  # Folder for graphs with multiple edges or self-loops


# Ensure the folder for special cases exists
os.makedirs(special_folder, exist_ok=True)
os.makedirs(dest_pos, exist_ok=True)

# Get the list of directories
dir_lst = os.listdir(path)

for dir in dir_lst:
    path_1 = os.path.join(path, dir)
    sub_dir_lst = os.listdir(path_1)

    # Check if the target subdirectory exists, create if not
    target_dir = os.path.join(dest_pos, dir)
    os.makedirs(target_dir, exist_ok=True)

    # Create a folder to save complex graphs, if it doesn't exist
    target_dir_CG = os.path.join(special_folder, dir)
    os.makedirs(target_dir_CG, exist_ok=True)

    for sub_file in sub_dir_lst:  # Read each JSON file individually
        path_2 = os.path.join(path_1, sub_file)

        # Check if it's a file and not a directory
        if not os.path.isfile(path_2):
            print(f"Skipping directory: {path_2}")
            continue

        edges = set()
        removed_edges = False  # Flag to track if self-loops or multiple edges were removed
        has_self_loop = False  # Flag to check if a self-loop exists

        with open(path_2, 'r', encoding='utf-8') as f:
            graph_data = json.load(f)  # Parse the JSON data
            # Iterate through all links (edges) in the graph
            for link in graph_data['links']:
                source, target = link['source'], link['target']
                # Check for self-loops
                if source == target:
                    has_self_loop = True
                    break
                # Ensure the edge is an unordered pair to guarantee uniqueness
                edge = tuple(sorted((link['source'], link['target'])))

                # Check for multiple edges
                if edge in edges:
                    removed_edges = True
                    break
                else:
                    edges.add(edge)

        # Calculate the number of nodes and edges, and the node-to-link ratio
        nodes_len = len(graph_data['nodes'])
        links_len = len(graph_data['links'])
        node_link_ratio = round(links_len / nodes_len, 5)

        # Construct the new file name
        original_name = os.path.splitext(sub_file)[0]  # Extract the original filename (without extension)
        new_name = f"{nodes_len}-{links_len}-1-{node_link_ratio}-{original_name}.json"

        # If there are self-loops or multiple edges, move the file to the special folder
        if removed_edges or has_self_loop:
            # special_dest_path = os.path.join(special_folder, new_name)
            special_dest_path = os.path.join(target_dir_CG, new_name)
            shutil.copy(path_2, special_dest_path)
            print(f"Moved complex graph: {special_dest_path}")
        else:
            # Save normal graphs to their respective folders
            dest_path = os.path.join(target_dir, new_name)
            with open(dest_path, 'w') as outfile:
                json.dump(graph_data, outfile, indent=4)
            print(f"Saved simple graph: {dest_path}")
