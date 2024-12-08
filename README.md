# OGDOS

Graph-related technologies, including social networks, transportation systems, and bioinformatics, are continually evolving in various application domains. The  advancement of these technologies often relies on high-quality graph datasets for validating scalability, complexity, and performance. However, existing datasets are typically categorized by domain or type and lack explicit organization at the scale level. Moreover, existing datasets may not fully cover a wide range of graph scale levels. These absences may limit comprehensive evaluations of the complex relationships between graph scales and performance. 

To address these gaps, we introduce an open graph dataset organized by scales named OGDOS. Our OGDOS is an open graph dataset organized by scales, encompassing 470 preset scale levels, with node counts ranging from 100 to 200,000 and edge-to-node ratios from 1 to 10. The dataset combines real-world graphs, aligned by scale, with synthetic graphs, providing a versatile resource for evaluating various graph-related applications. 

All real-world graphs in OGDOS are sourced from well-known graph datasets listed in Table 1 and have undergone careful selection and refinement. The process of selecting and refining these graphs is documented in the '.py' files in the Code folder. All synthetic graphs in OGDOS are generated using the barabasi_albert_graph or watts_strogatz_graph functions from Python NetworkX library (version 2.8.8), which offers flexible functions and parameters (such as target node scale and edge-to-node ratio) to generate the desired graph datasets. The source types of the graphs in OGDOS are provided in Table 2.

# Files in the repository

All graphs in OGDOS are provided in 'OGDOS' folder. The code for processing real-world graphs is provided in 'Code' folder.

## 'OGDOS' folder

In this folder, each graph in OGDOS is stored as a “.json” file in a specific directory path, which reflects its corresponding scale levels. For example, a “.json” file located at the “…\OGDOS \ 100 \ 1 \” folder represents a graph with a node scale of 100 and an edge-to-node ratio of 1. The source types of these graphs in OGDOS are provided in Table 2.

## 'Code' folder

In this folder, the codes for processing real-world graphs are provided in the form of '.py' files. The folder includes instructions on how to convert the format of source files (**'conver' folder**), how to judge complex graphs (**'judge_complex_graphs.py'**), how to process complex graphs (**'process_complex_graphs.py'**), how to identify the target scale levels (**'identify_the_target_scale_levels.py'**), and how to filter and refine real-world graphs (**'filter_and_refine_graphs.py'**).

## 'Table' folder

In this folder, the Table 1 (**List of well-known graph datasets and the categorization perspectives they provide.**) and Table 2 (**The source types of graphs in OGDOS.**) are provided.

