import json
import os

path  = 'Uniform-tnet'
dest_pos = 'res_Uniform-tnet'

os.makedirs(dest_pos,exist_ok=True)
dir_lst = os.listdir(path)

for dir in dir_lst:
    path_1 = os.path.join(path,dir)

    with open(path_1,'r') as file:
       dl_data = file.readlines()
       print(dl_data)
       num_nodes = int([line for line in dl_data if line.startswith('n=')][0].split('=')[1])

       nodes = [{"id": str(i+1)} for i in range(num_nodes)]
       links = []

       for line in dl_data[dl_data.index('data:\n')+1:]:
           node1, node2, weight = line.split()
           links.append({
               "source": node1,
               "target": node2
           })


       graph_data = {
            'source': 'Tore Opsahl',
            'name': dir.split('.')[0],
            "nodes":nodes,
            "links":links
        }

       json_output = json.dumps(graph_data,indent=4)
       output_path = os.path.join(dest_pos,dir.split('.')[0]+'.json')
       with open(output_path,'w') as outfile:
           outfile.write(json_output)


