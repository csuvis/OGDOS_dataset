import json

# Path to the input txt file
input_file = '0-SNAP/通信网络/Email-Enron.txt'

# Initialize empty sets for nodes and list for links
nodes_set = set()
links = []

# Read the file and process it
with open(input_file, 'r') as file:
    lines = file.readlines()

    # Process each line in the file
    for line in lines:
        # Skip lines starting with '#', which are comments
        if line.startswith('#'):
            continue

        # Split the line to get source and target
        source, target = line.split()

        # Add source and target to nodes set
        nodes_set.add(source)
        nodes_set.add(target)

        # Add a link (directed edge) from source to target
        links.append({"source": source, "target": target})

# Convert the nodes set into a list of dictionaries with "id"
nodes = [{"id": node_id} for node_id in sorted(nodes_set, key=int)]

# Create the final JSON structure
graph_data = {
    "source":"SNAP",
    "name":"Email-Enron",
    "nodes": nodes,
    "links": links
}

# Path to output the JSON file
output_file = 'res-SNAP/对等网络/Email-Enron.json'

# Write the JSON data to the output file
with open(output_file, 'w') as json_file:
    json.dump(graph_data, json_file, indent=4)

print(f"JSON data has been saved to {output_file}")
