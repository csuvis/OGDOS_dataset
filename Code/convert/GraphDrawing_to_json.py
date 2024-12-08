import json
import os
import re

import networkx as nx

path  = '0-GraphDrawing'
dest_pos = 'res-GraphDrawing'

os.makedirs(dest_pos,exist_ok=True)
dir_lst = os.listdir(path)

for dir in dir_lst:

    path_1 = os.path.join(path,dir)


    for dir_1 in os.listdir(path_1):
        path_2 = os.path.join(path_1,dir_1)

        # Load the provided JSON file
        with open(path_2, 'r') as file:
            data = json.load(file)

        # Create a mapping of original ids to new sequential ids
        id_mapping = {node['id']: index for index, node in enumerate(data['nodes'])}
        Error = False

        # Update source and target in links based on the new id mapping
        for link in data['links']:
            if link['source'] in id_mapping and link['target'] in id_mapping:
                link['source'] = id_mapping[link['source']]
                link['target'] = id_mapping[link['target']]
            else:
                Error = True
                print(f"Error: {dir_1}")
                break

        if Error:
            continue


        # Remove all attributes except 'source' and 'target'
        for link in data['links']:
            link.pop('timestamp', None)

        # Remove all node attributes except 'id'
        data['nodes'] = [{'id': id_mapping[node['id']]} for node in data['nodes']]

        # Save the modified data to a new JSON file
        output_path_1 = os.path.join(dest_pos,dir)
        os.makedirs(output_path_1, exist_ok=True)
        output_path = os.path.join(output_path_1,dir_1)
        with open(output_path, 'w') as output_file:
            json.dump(data, output_file, indent=4)

        print(f"Data has been saved to {output_file}")