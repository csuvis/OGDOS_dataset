import json

import json
import os

path  = '1-github-HIN'
dest_pos = 'res-HIN'

os.makedirs(dest_pos,exist_ok=True)
dir_lst = os.listdir(path)

for dir_0 in dir_lst:
    path_1 = os.path.join(path,dir_0)

    for dir in os.listdir(path_1):
        # 初始化节点和链接集合
        nodes_set = set()  # 使用集合来去重
        links = []
        input_file = os.path.join(path_1,dir)
        # 读取文件并解析
        with open(input_file, 'r') as file:
            for line in file:
                line = line.strip()

                # 判断文件中使用的分隔符（逗号、制表符或空格）
                if ',' in line:
                    source, target = line.split(',')[:2]  # 只取前两个字段
                elif '\t' in line:
                    source, target = line.split('\t')[:2]  # 只取前两个字段
                else:
                    source, target = line.split()[:2]  # 处理空格分隔并取前两个字段

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
        os.makedirs(os.path.join(dest_pos,dir_0), exist_ok=True)

        output_file = os.path.join(os.path.join(dest_pos,dir_0),dir.split('.')[0]+'.json')
        # 将数据写入 JSON 文件
        with open(output_file, 'w') as json_file:
            json.dump(graph_data, json_file, indent=4)

        print(f"数据已保存到 {output_file}")
