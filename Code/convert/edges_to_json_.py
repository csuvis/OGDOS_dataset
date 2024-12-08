import json

import json
import os

path  = '0-原始数据集/'
dest_pos = 'res-原始数据集/'

os.makedirs(dest_pos,exist_ok=True)
dir_lst = os.listdir(path)

for dir in dir_lst:


    # Initialize sets and lists for nodes and links
    nodes_set = set()
    links = []
    input_file_path = os.path.join(path,dir)
    with open(input_file_path, 'r') as file_content:

        for line in file_content:
            parts = line.split()
            if len(parts) >= 2:
                init_node = parts[0]
                term_node = parts[1]

                # Add nodes to the set (for uniqueness)
                nodes_set.add(init_node)
                nodes_set.add(term_node)

                # Add links
                links.append({"source": init_node, "target": term_node})

        # Convert nodes set to sorted list of dictionaries
        nodes = [{"id": node} for node in sorted(nodes_set, key=int)]

        # Construct the JSON structure
        graph_data = {
            "source":path.split('/')[1],
            "name":dir.split('.')[0],
            "nodes": nodes,
            "links": links
        }


        # Save the resulting data to a JSON file
        output_json_file = os.path.join(dest_pos,dir.split('.')[0]+'.json')
        with open(output_json_file, 'w') as json_file:
            json.dump(graph_data, json_file, indent=4)

        print(f"数据已保存到 {output_json_file}")

