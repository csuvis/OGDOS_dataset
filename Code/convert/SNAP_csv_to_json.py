import json

import json
import os

import pandas as pd

path  = '0-SNAP'
dest_pos = 'res-SNAP'

path_2 = '对等网络'

os.makedirs(os.path.join(dest_pos,path_2),exist_ok=True)
dir_lst = os.listdir(os.path.join(path,path_2))

for dir in dir_lst:

    file_path = os.path.join(os.path.join(path,path_2),dir)
    print(file_path)
    # Read the CSV into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Create a set for unique node IDs
    nodes_set = set()

    # Initialize links list
    links = []

    # Process each row to create nodes and links
    for index, row in df.iterrows():
        source = str(int(row[0]))  # Source node
        target = str(int(row[1]))  # Target node

        # Add source and target to the nodes set
        nodes_set.add(source)
        nodes_set.add(target)

        # print(source,target)

        # Add link to the links list
        links.append({"source": source, "target": target})

    # Create nodes list from the set of unique node IDs
    nodes = [{"id": node_id} for node_id in sorted(nodes_set, key=int)]

    # Create the final data structure
    graph_data = {
        "source":path.split('-')[1],
        "name":dir.split('.')[0],
        "nodes": nodes,
        "links": links
    }

    # Define the output file path
    output_file = os.path.join(os.path.join(dest_pos,path_2),dir.split('.')[0]+'.json')

    # Save the data as JSON
    with open(output_file, 'w') as json_file:
        json.dump(graph_data, json_file, indent=4)

    print(f"Data has been saved to {output_file}")
