import json
import os

path  = 'Pajek-2'
dest_pos = 'res-Pajek'

os.makedirs(dest_pos,exist_ok=True)
dir_lst = os.listdir(path)

for dir in dir_lst:
    # 判断是否是 gml 格式的文件
    if not dir.endswith('.net'):
        continue  # 如果不是 net 文件，跳过

    path_1 = os.path.join(path, dir)

    # 读取 .net 文件内容，使用 'ISO-8859-1' 编码处理非 UTF-8 字符
    with open(path_1, 'r', encoding='ISO-8859-1') as file:
        net_data = file.readlines()

    # 初始化存储节点和边的列表
    nodes = []
    links = []

    # 标志变量，用于判断当前正在解析的部分是节点还是边
    in_vertex_section = False
    in_edge_section = False

    # 解析 .net 文件
    for line in net_data:
        line = line.strip()  # 去掉每行的开头和结尾空格

        # 判断是否进入节点部分
        if line.startswith("*vertices"):
            in_vertex_section = True
            in_edge_section = False
            continue

        # 判断是否进入边部分
        if line.startswith("*edges") or line.startswith("*arcs"):
            in_vertex_section = False
            in_edge_section = True
            continue

        # 解析节点信息
        if in_vertex_section:
            parts = line.split(" ", 1)
            if len(parts) == 2:
                node_id, label = parts
                nodes.append({"id": node_id})  # 节点ID和标签

        # 解析边信息
        if in_edge_section:
            parts = line.split()
            if len(parts) >= 2:
                source, target = parts[:2]
                links.append({"source": source, "target": target})  # 边的源节点和目标节点

    # 构建最终的 JSON 结构
    network_data = {
        "source": path.split('-')[1],
        "name": dir.split('.')[0],
        "nodes": nodes,
        "links": links
    }

    # 将数据转换为 JSON 格式并保存到文件
    json_output = json.dumps(network_data, indent=4)
    output_path = os.path.join(dest_pos, dir.split('.')[0] + '.json')
    with open(output_path, 'w') as outfile:
        outfile.write(json_output)

    print(f"JSON 文件已保存到: {output_path}")
