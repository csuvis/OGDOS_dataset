import json
import os

path = 'E:\\20241017-论文数据集和相关代码\\20241017-论文数据集和相关代码\\0-处理原始数据集代码_tojson\\py-处理数据代码集-toJson-2\\new'
dest_pos = 'E:\\20241017-论文数据集和相关代码\\20241017-论文数据集和相关代码\\0-处理原始数据集代码_tojson\\py-处理数据代码集-toJson-2\\new'

os.makedirs(dest_pos, exist_ok=True)
dir_lst = os.listdir(path)

for dir in dir_lst:

    print(dir)

    path_1 = os.path.join(path, dir)

    # 用于存储唯一节点的集合
    nodes_set = set()
    links = []

    with open(path_1, 'r') as file:
        for line in file:
            # 以空格为分隔符提取 i 和 j
            i, j = line.split()[:2]  # Get the first two elements
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
        "source": path.split('/')[0],
        "name": dir.split('.')[0],
        "nodes": nodes,
        "links": links_json
    }

    # Save the data to a JSON file
    os.makedirs(os.path.join(dest_pos, 'sg_infectious_contact_list'), exist_ok=True)
    output_file = os.path.join(os.path.join(dest_pos), dir.split('.')[0] + '.json')
    with open(output_file, 'w') as json_file:
        json.dump(graph_data, json_file, indent=4)

    print(f"Data has been saved to {output_file}")
