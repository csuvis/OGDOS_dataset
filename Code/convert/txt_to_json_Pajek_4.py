import json

# File paths
input_file = 'Pajek-5/NDyeast.txt'
output_file = 'res-Pajek/NDyeast.json'

# Initialize storage for nodes and links
nodes = []
links = []

# Read the file
with open(input_file, 'r') as file:
    lines = file.readlines()

# Parse the nodes
node_section = True
for line in lines:
    line = line.strip()

    if "*vertices" in line:
        continue  # Skip the vertices header

    if "*arcslist" in line:
        node_section = False  # Switch to arcs (links) section
        continue

    if node_section:
        # Add node (ID and label)
        parts = line.split(maxsplit=1)
        node_id = parts[0]
        label = parts[1].strip('"')
        nodes.append({"id": node_id})

    else:
        # Add links (arcs)
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
