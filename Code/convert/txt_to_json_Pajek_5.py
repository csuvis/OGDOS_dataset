import json

# File paths
input_file = 'Pajek-5/SciMet.txt'
output_file = 'res-Pajek/SciMet.json'

# Initialize storage for nodes and links
nodes = []
links = []

# Read the file
with open(input_file, 'r') as file:
    lines = file.readlines()

# Parse the file
in_node_section = True
num_nodes = 0

for line in lines:
    line = line.strip()

    if line.startswith("*vertices"):
        # 提取 Vertices 后面的数字，表示节点数量
        num_nodes = int(line.split()[1])
        # 根据节点数量生成节点列表
        nodes = [{"id": str(i + 1)} for i in range(num_nodes)]  # 节点 ID 从 1 开始
        continue

    if line.startswith("*arcslist") or line.startswith("*edgeslist"):
        in_node_section = False  # Switch to links section
        continue

    if not in_node_section:
        # Add links (edges/arcs)
        parts = line.split()
        source = parts[0]
        targets = parts[1:]
        for target in targets:
            links.append({"source": source, "target": target})

# Create the final data structure
graph_data = {
    "nodes": nodes,
    "links": links
}

# Save the data as JSON
with open(output_file, 'w') as json_file:
    json.dump(graph_data, json_file, indent=4)

print(f"Data has been saved to {output_file}")
