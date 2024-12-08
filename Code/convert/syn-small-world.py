import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import json
import os

# 设置点规模范围
node_scales = range(100, 1000, 100)

# 输出文件夹
dest_pos = './output'
os.makedirs(dest_pos, exist_ok=True)

# 生成小世界网络并保存为JSON
for n in node_scales:
    k_min = max(1, int(np.log(n)))  # k >= ln(n) 并且 k >= 1
    k_max = n  # k <= n

    for k in range(k_min, k_max + 1):
        # 生成小世界网络
        G = nx.watts_strogatz_graph(n, k, 0.025)  # 0.1 是重连概率

        # 提取节点和边
        nodes_set = G.nodes()
        links = [{"source": source, "target": target} for source, target in G.edges()]

        # Convert nodes set to sorted list of dictionaries
        nodes = [{"id": node} for node in sorted(nodes_set, key=int)]

        # Construct the JSON structure
        graph_data = {
            "source": "Small-World Network",
            "name": f"Nodes_{n}_k_{k}",
            "nodes": nodes,
            "links": links
        }

        # Save the resulting data to a JSON file
        output_json_file = os.path.join(dest_pos, f'Nodes_{n}_k_{k}.json')
        with open(output_json_file, 'w') as json_file:
            json.dump(graph_data, json_file, indent=4)

        print(f"数据已保存到 {output_json_file}")
