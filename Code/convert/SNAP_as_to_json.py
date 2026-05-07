import json

import json
import os

import pandas as pd

path  = '0-SNAP/自治系统图'
dest_pos = 'res-SNAP/自治系统图'

path_2 = 'as-733'

os.makedirs(os.path.join(dest_pos,path_2),exist_ok=True)
# dir_lst = os.listdir(os.path.join(path,path_2))
path_0 = os.path.join(path,path_2)


for dir in os.listdir(path_0):

    nodes_set = set()  # 用于收集所有的唯一节点
    links_set = set()  # 用于去除重复的边
    links = []
    file_path  = os.path.join(path_0,dir)
    print(dir)
    with open(file_path, 'r') as file:
        for line in file:
            if not line.startswith('#') and line.strip():
                from_node, to_node = line.strip().split()

                if from_node==to_node:
                    print("有自环",from_node)

                # 添加节点到集合
                nodes_set.add(from_node)
                nodes_set.add(to_node)

                # 使用排序的方式避免无向图中重复边
                sorted_edge = tuple(sorted((from_node, to_node)))
                if sorted_edge not in links_set:
                    links_set.add(sorted_edge)
                    links.append({"source": from_node, "target": to_node})

    # 为每个唯一节点分配一个从0开始的序号
    node_mapping = {node: idx for idx, node in enumerate(sorted(nodes_set))}

    # 创建 JSON 格式的节点和链接
    nodes = [{"id": node_mapping[node]} for node in sorted(nodes_set)]
    links_json = [{"source": node_mapping[link["source"]], "target": node_mapping[link["target"]]} for link in links]

    graph_data = {
        "source":"SNAP",
        "name":dir.split('.')[0],
        "nodes": nodes,
        "links": links_json
    }

    # Define the output file path
    output_file = os.path.join(os.path.join(dest_pos, path_2), dir.split('.')[0] + '.json')

    # Save the data as JSON
    with open(output_file, 'w') as json_file:
        json.dump(graph_data, json_file, indent=4)

    print(f"Data has been saved to {output_file}")