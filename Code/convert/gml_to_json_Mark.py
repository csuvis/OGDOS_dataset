import json
import os
import re

import networkx as nx

path  = '0-MarkNewman Dataset'
dest_pos = 'res-Mark'

os.makedirs(dest_pos,exist_ok=True)
dir_lst = os.listdir(path)

for dir in dir_lst:
    # # 判断是否是 gml 格式的文件
    # if not dir.endswith('.gml'):
    #     continue  # 如果不是 gml 文件，跳过

    path_1 = os.path.join(path,dir)

    for dir_1 in os.listdir(path_1):
        path_2 = os.path.join(path_1,dir_1)

        with open(path_2, 'r') as file:
            file_content = file.read()


        # Function to extract numeric part of node id
        def extract_numeric_id(node_id):
            return re.sub(r'\D', '', node_id)


        # Extract nodes
        nodes = re.findall(r'<node id="(n\d+)">', file_content)
        nodes = [{"id": extract_numeric_id(node)} for node in nodes]

        # Extract links (edges)
        links = re.findall(r'<edge source="(n\d+)" target="(n\d+)" />', file_content)
        links = [{"source": extract_numeric_id(source), "target": extract_numeric_id(target)} for source, target in links]

        # Create final JSON structure
        graph_data = {
            "source":path.split('-')[1],
            "name":dir_1.split('.')[0],
            "nodes": nodes,
            "links": links
        }

        # Save the data to a JSON file
        os.makedirs(os.path.join(dest_pos,dir), exist_ok=True)
        output_file = os.path.join(os.path.join(dest_pos,dir),dir_1.split('.')[0]+'.json')
        with open(output_file, 'w') as json_file:
            json.dump(graph_data, json_file, indent=4)

        print(f"Data has been saved to {output_file}")

