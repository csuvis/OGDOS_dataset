import json

import json
import os

path  = '0-SNAP'
dest_pos = 'res-SNAP'

path_2 = '通信网络'

os.makedirs(os.path.join(dest_pos,path_2),exist_ok=True)
dir_lst = os.listdir(os.path.join(path,path_2))

for dir in dir_lst:

    path_1 = os.path.join(os.path.join(path,path_2),dir)
    print(path_1)

    # 初始化节点和边的列表
    nodes = []
    links = []
    num_nodes = 0

    # 读取文件
    with open(path_1, 'r') as file:
        lines = file.readlines()

    # 解析文件中的节点和边数量，并生成对应数量的节点
    for line in lines:
        line = line.strip()

        # 检查文件中的节点和边信息
        if line.startswith("# Nodes:"):
            num_nodes = int(line.split()[2])  # 获取节点数量
            # 根据节点数量生成节点
            nodes = [{"id": str(i)} for i in range(num_nodes)]
            continue
        if line.startswith("# Edges:"):
            continue  # 跳过边数行

        if line.startswith("#") or line.startswith("*"):
            continue  # 跳过其他注释行

    # 解析文件中的边信息
    for line in lines:
        line = line.strip()

        if line.startswith("#") or line.startswith("*"):
            continue  # 跳过注释行

        parts = line.split()
        if len(parts) >= 3:  # 只处理至少有三个元素的行
            source, target, _ = parts[0], parts[1], parts[2]  # 忽略第三个值
            # 添加边（有向边）
            links.append({"source": source, "target": target})

    # 创建最终的 JSON 数据结构
    graph_data = {
        "source":path.split('-')[1],
        "name":dir.split('.')[0],
        "nodes": nodes,
        "links": links
    }

    output_path = os.path.join(os.path.join(dest_pos,path_2), dir.split('.')[0] + '.json')
    # 将数据保存为 JSON 文件
    with open(output_path, 'w') as json_file:
        json.dump(graph_data, json_file, indent=4)

    print(f"数据已保存到 {output_path}")
