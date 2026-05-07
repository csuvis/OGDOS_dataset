import json

import json
import os
import re

import networkx as nx

path_1  = '0-knownCR'
dest_pos = 'res/res-knownCR'

os.makedirs(dest_pos,exist_ok=True)

for dir_1 in os.listdir(path_1):
    path_2 = os.path.join(path_1, dir_1)

    # Load the JSON data
    with open(path_2, 'r') as file:
        data = json.load(file)

    data['source'] = path_1.split('-')[1]
    data['name'] = dir_1.split('.')[0]

    # Create a mapping from old ids to new sequential ids
    id_mapping = {node['id']: idx for idx, node in enumerate(data['nodes'])}

    # Update the ids in the nodes
    for node in data['nodes']:
        node['id'] = id_mapping[node['id']]

    # Update the source and target ids in the links
    for link in data['links']:
        link['source'] = id_mapping[link['source']]
        link['target'] = id_mapping[link['target']]

    # Save the modified data to a new JSON file
    output_path = os.path.join(dest_pos, dir_1)

    with open(output_path, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    print(f"Data has been saved to {output_path}")
