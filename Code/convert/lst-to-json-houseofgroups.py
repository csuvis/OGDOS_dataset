import json
import os

path = 'House of Groups'
dest_pos = 'res-House of Groups'

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
            parts = line.strip().split(':')
            if len(parts) != 2:
                continue  # Skip malformed lines

            # Extract the node and its connections
            node = parts[0].strip()
            connections = parts[1].strip().split()

            # Add the node to the set
            nodes_set.add(node)

            # Create links for each connection
            for target in connections:
                links.append((node, target))
                nodes_set.add(target)

    # 为每个唯一节点分配序号
    nodes_list = sorted(nodes_set)
    node_index = {node: idx for idx, node in enumerate(nodes_list)}

    # 生成 JSON 格式的节点和链接
    nodes = [{"id": idx} for node, idx in node_index.items()]
    links_json = [{"source": node_index[i], "target": node_index[j]} for i, j in links]

    # Create final JSON structure
    graph_data = {
        "source": path.split('/')[-1],  # Use the last part of the path for source
        "name": dir.split('.')[0],
        "nodes": nodes,
        "links": links_json
    }

    # Save the data to a JSON file
    os.makedirs(os.path.join(dest_pos), exist_ok=True)
    output_file = os.path.join(os.path.join(dest_pos), dir.split('.')[0] + '.json')
    with open(output_file, 'w') as json_file:
        json.dump(graph_data, json_file, indent=4)

    print(f"Data has been saved to {output_file}")
