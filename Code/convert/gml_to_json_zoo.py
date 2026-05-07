import json
import os

path  = '0-InterNet Topology Zoo'
dest_pos = 'res-Zoo'

os.makedirs(dest_pos,exist_ok=True)
dir_lst = os.listdir(path)

for dir in dir_lst:
    # 判断是否是 gml 格式的文件
    if not dir.endswith('.gml'):
        continue  # 如果不是 gml 文件，跳过

    path_1 = os.path.join(path,dir)

    # 初始化存储 nodes 和 links 的列表
    nodes = []
    links = []

    # 标志变量，用于跟踪我们是否在 node 或 edge 块中
    in_node_block = False
    in_edge_block = False

    # 打开并逐行读取 GML 文件
    with open(path_1, 'r') as file:
        gml_data = file.readlines()

    # 解析 GML 文件中的每一行
    for line in gml_data:
        line = line.strip()  # 去掉每行开头和结尾的空格

        # 检查 node 块的开始
        if line == "node [":
            in_node_block = True
            node_data = {}  # 临时存储当前节点的数据
            continue

        # 检查 edge 块的开始
        if line == "edge [":
            in_edge_block = True
            edge_data = {}  # 临时存储当前边的数据
            continue

        # 当前块的结束
        if line == "]":
            if in_node_block:
                nodes.append(node_data)  # 添加已解析的节点
                in_node_block = False
            elif in_edge_block:
                links.append(edge_data)  # 添加已解析的边
                in_edge_block = False
            continue

        # 解析节点信息
        if in_node_block:
            if line.startswith("id"):
                node_id = line.split()[1]
                node_data["id"] = node_id  # 存储节点 ID
            # elif line.startswith("label"):
            #     node_data["label"] = line.split(" ", 1)[1].strip('"')  # 存储节点标签

        # 解析边信息
        if in_edge_block:
            if line.startswith("source"):
                source = line.split()[1]
                edge_data["source"] = source  # 存储边的源节点
            elif line.startswith("target"):
                target = line.split()[1]
                edge_data["target"] = target  # 存储边的目标节点

    # 构建最终的 JSON 结构
    graph_data = {
        "source":path.split('-')[1],
        "name":dir.split('.')[0],
        "nodes": nodes,
        "links": links
    }

    # 将数据转换为 JSON 格式并保存到文件
    json_output = json.dumps(graph_data, indent=4)  # 格式化输出，缩进为 4
    output_path = os.path.join(dest_pos, dir.split('.')[0] + '.json')
    with open(output_path, 'w') as outfile:
        outfile.write(json_output)

    print(f"JSON 文件已保存到: {output_path}")
