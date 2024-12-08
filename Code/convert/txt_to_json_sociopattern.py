import csv
import json
import os
import re

import networkx as nx

path  = '0-原始数据集/小世界_引文网络'
dest_pos = 'res-原始数据集/小世界_引文网络'

os.makedirs(dest_pos,exist_ok=True)
dir_lst = os.listdir(path)

for dir in dir_lst:
    print(dir)
    # # 判断是否是 gml 格式的文件
    # if not dir.endswith('.gml'):
    #     continue  # 如果不是 gml 文件，跳过

    path_1 = os.path.join(path,dir)

    # 用于存储唯一节点的集合
    nodes_set = set()
    links = []

    # 读取 CSV 文件
    with open(path_1, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            # 提取 i 和 j 列
            i, j = row[0], row[1]
            nodes_set.add(i)
            nodes_set.add(j)
            links.append((i, j))

    # 为每个唯一节点分配序号
    nodes_list = sorted(nodes_set)
    node_index = {node: idx for idx, node in enumerate(nodes_list)}

    # 生成 JSON 格式的节点和链接
    nodes = [{"id": idx} for node, idx in node_index.items()]
    links_json = [{"source": node_index[i], "target": node_index[j]} for i, j in links]

    # Create final JSON structure
    print(path)
    graph_data = {
        "source":path.split('/')[1],
        "name":dir.split('.')[0],
        "nodes": nodes,
        "links": links_json
    }

    # Save the data to a JSON file
    os.makedirs(os.path.join(dest_pos,'sg_infectious_contact_list'), exist_ok=True)
    output_file = os.path.join(os.path.join(dest_pos,'sg_infectious_contact_list'),dir.split('.')[0]+'.json')
    with open(output_file, 'w') as json_file:
        json.dump(graph_data, json_file, indent=4)

    print(f"Data has been saved to {output_file}")

