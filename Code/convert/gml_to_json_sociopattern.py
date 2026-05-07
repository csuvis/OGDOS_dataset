import json
import os
import re

import networkx as nx

path  = '1-github-sociopattern/INFECTIOUS_cumulative_daily_networks'
dest_pos = 'res-sociopattern'

os.makedirs(dest_pos,exist_ok=True)
dir_lst = os.listdir(path)

for dir in dir_lst:
    print(dir)
    # # 判断是否是 gml 格式的文件
    # if not dir.endswith('.gml'):
    #     continue  # 如果不是 gml 文件，跳过

    path_1 = os.path.join(path,dir)

    nodes = []
    links = []
    node_ids = set()
    current_node = None
    current_edge = None
    is_directed = False

    with open(path_1, 'r') as file:
        for line in file:
            line = line.strip()

            # Check if the graph is directed
            if line.startswith('directed'):
                is_directed = int(line.split()[1])

            # Parse nodes
            if line.startswith('node'):
                current_node = {}
            if line.startswith('id') and current_node is not None:
                node_id = line.split()[1]
                current_node['id'] = node_id
                node_ids.add(node_id)
            if line.startswith(']') and current_node is not None:
                nodes.append(current_node)
                current_node = None

            # Parse edges
            if line.startswith('edge'):
                current_edge = {}
            if line.startswith('source') and current_edge is not None:
                current_edge['source'] = line.split()[1]
            if line.startswith('target') and current_edge is not None:
                current_edge['target'] = line.split()[1]
            if line.startswith(']') and current_edge is not None:
                links.append(current_edge)
                current_edge = None

        # Create final JSON structure
        graph_data = {
            "source":path.split('/')[0].split('-')[2],
            "name":dir.split('.')[0],
            "nodes":  [{"id": node_id} for node_id in sorted(node_ids, key=int)],
            "links": links
        }

        # Save the data to a JSON file
        os.makedirs(os.path.join(dest_pos,'INFECTIOUS_cumulative_daily_networks'), exist_ok=True)
        output_file = os.path.join(os.path.join(dest_pos,'INFECTIOUS_cumulative_daily_networks'),dir.split('.')[0]+'.json')
        with open(output_file, 'w') as json_file:
            json.dump(graph_data, json_file, indent=4)

        print(f"Data has been saved to {output_file}")

