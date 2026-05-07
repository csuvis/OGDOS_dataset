import csv
import json

import json
import os

path  = '2-github-transportation'
dest_pos = 'res-transportation'

os.makedirs(dest_pos,exist_ok=True)
dir_lst = os.listdir(path)

for dir in dir_lst:


    # Initialize sets and lists for nodes and links
    nodes_set = set()
    links = []
    input_file_path = os.path.join(path,dir)
    with open(input_file_path, 'r') as file:
        csv_reader = csv.DictReader(file)

        # 遍历每一行，提取 origin 和 dest
        for row in csv_reader:
            origin = row['fBus']
            dest = row['tBus']

            # 添加到节点集合
            nodes_set.add(origin)
            nodes_set.add(dest)

            # 添加链接
            links.append({"source": origin, "target": dest})

        # 将节点集合转换为列表
    nodes = [{"id": node} for node in sorted(nodes_set)]

    # 构建 JSON 数据
    graph_data = {
        "source":path.split('-')[2],
        "name":dir.split('.')[0],
        "nodes": nodes,
        "links": links
    }

    output_file_path = os.path.join(dest_pos,dir)
    # 将数据写入 JSON 文件
    with open(output_file_path, 'w') as json_file:
        json.dump(graph_data, json_file, indent=4)

    print(f"数据已保存到 {output_file_path}")