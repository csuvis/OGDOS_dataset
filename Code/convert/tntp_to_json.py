import json

import json
import os

path  = '1-github-transportation'
dest_pos = 'res-transportation'

os.makedirs(dest_pos,exist_ok=True)
dir_lst = os.listdir(path)

for dir in dir_lst:
    # 初始化节点和链接集合
    nodes_set = set()
    links = []
    input_file_path = os.path.join(path,dir)
    # 读取文件并解析
    with open(input_file_path, 'r') as file:
        start_parsing = False
        for line in file:
            # 找到包含 init_node 和 term_node 的标头
            if "init_node" in line and "term_node" in line:
                start_parsing = True
                continue

            # 开始处理实际数据
            if start_parsing and line.strip():
                # 按空格或制表符分割字段
                parts = line.split()
                if len(parts) >= 2:
                    init_node = parts[0]
                    term_node = parts[1]

                    # 添加到节点集合
                    nodes_set.add(init_node)
                    nodes_set.add(term_node)

                    # 添加到链接列表
                    links.append({"source": init_node, "target": term_node})

    # 将节点集合转换为列表，并按顺序排序
    nodes = [{"id": node} for node in sorted(nodes_set)]

    # 构建 JSON 数据
    graph_data = {
        "nodes": nodes,
        "links": links
    }
    output_file_path = os.path.join(dest_pos,dir.split('.')[0])
    # 将数据写入 JSON 文件
    with open(output_file_path, 'w') as json_file:
        json.dump(graph_data, json_file, indent=4)

    print(f"数据已保存到 {output_file_path}")