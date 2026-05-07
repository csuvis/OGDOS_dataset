import os
import shutil
import re

# Define the node scale intervals array
scale_intervals = list(range(100, 1000, 100)) + list(range(1000, 10000, 1000)) + list(
    range(10000, 100000, 5000)) + list(range(100000, 200001, 10000))

# Target edge-to-node ratios
target_edge_ratios = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Set custom tolerance ranges
# node_scale_tolerance = 50  # This value can be adjusted
edge_node_ratio_tolerance = 0.1  # This value can be adjusted

# Set directories for JSON files and output
json_dir = 'dataset'  # Directory containing the JSON files
output_dir = 'res'  # Directory for extracted files
# Make sure to adjust the filename parsing

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Traverse through the JSON files
for dir in os.listdir(json_dir):
    path_1 = json_dir + '/' + dir
    sub_dir_lst = os.listdir(path_1)
    print(path_1)
    for filename in sub_dir_lst:
        # print(filename)
        if filename.endswith('.json'):
            # Extract node scale and edge-to-node ratio from the filename
            match = re.match(r'(\d+)-(\d+)-1-([\d\.]+)-.*\.json', filename)
            if match:
                node_scale = int(match.group(1))  # Node scale
                edge_node_ratio = float(match.group(3))  # Edge-to-node ratio

                # Find the closest scale interval
                closest_scale = min(scale_intervals, key=lambda x: abs(x - node_scale))

                # Check if the node scale difference is within the tolerance range
                if abs(node_scale - closest_scale) <= closest_scale * 0.05:

                    # Loop through the target edge-to-node ratios and check for matching ratios
                    for target_ratio in target_edge_ratios:
                        if abs(edge_node_ratio - target_ratio) <= edge_node_ratio_tolerance:
                            # If conditions are met, process the file

                            # Construct the output directory path
                            dir_path = os.path.join(output_dir, dir)  # Target subdirectory path
                            if not os.path.exists(dir_path):
                                os.makedirs(dir_path)  # Create the subdirectory if it doesn't exist
                                print(f"Created directory: {dir_path}")

                            # Construct the file paths
                            src_path = os.path.join(json_dir + '/' + dir, filename)
                            dst_path = os.path.join(output_dir + '/' + dir, filename)

                            # Check if the file exists and copy it
                            if os.path.exists(src_path):
                                shutil.copy(src_path, dst_path)
                                print(f"Extracted: {filename}")
                            else:
                                print(f"File not found: {src_path}")

                            # Break out of the loop for target edge-to-node ratios once a match is found
                            break
                    else:
                        print(f"No matching target edge ratio for: {filename}")
                else:
                    print(f"Condition not met for node scale: {filename}")
