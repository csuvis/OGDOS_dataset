import json

import json
import os

path  = '2-github-TUDataset'
dest_pos = 'res-TUDataset-1'

os.makedirs(dest_pos,exist_ok=True)
dir_lst = os.listdir(path)

for dir in dir_lst:
    # 初始化节点和链接集合
    nodes_set = set()  # 使用集合来去重
    links = []
    input_file = os.path.join(path,dir)
    # 读取文件并解析
    with open(input_file, 'r') as file:
        for line in file:
            # 处理逗号分隔的节点
            source, target = line.strip().split(',')

            # 去除可能存在的额外空格
            source = source.strip()
            target = target.strip()

            # 添加节点到集合中
            nodes_set.add(source)
            nodes_set.add(target)

            # 添加链接
            links.append({"source": source, "target": target})

    # 将节点集合转换为列表，并构造为需要的字典格式
    nodes = [{"id": node} for node in sorted(nodes_set)]

    # 构建 JSON 数据
    graph_data = {
        "source":path.split('-')[2],
        "name":dir.split('.')[0],
        "nodes": nodes,
        "links": links
    }

    output_file = os.path.join(dest_pos,dir.split('.')[0]+'.json')
    # 将数据写入 JSON 文件
    with open(output_file, 'w') as json_file:
        json.dump(graph_data, json_file, indent=4)

    print(f"数据已保存到 {output_file}")
