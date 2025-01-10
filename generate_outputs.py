import time
from pathlib import Path

import networkx as nx
import pandas as pd
from networkx import NetworkXError

from algorithms.compact_forward import CompactForward
from algorithms.doulion import Doulion
from algorithms.node_iterator import NodeIterator
from algorithms.triest import Triest

directory = 'input/'


def store_dataset_properties():
    result_df = pd.DataFrame(columns=['dataset', 'nodes', 'edges', 'density', 'diameter', 'triangles'])

    for filepath in sorted(Path(directory).iterdir()):
        if filepath.is_file():
            file_name = filepath.name

            df = pd.read_csv(filepath, delimiter=',')
            graph = nx.from_pandas_edgelist(df, 'node_1', 'node_2')

            triangles = sum(nx.triangles(graph).values()) / 3
            nodes = graph.number_of_nodes()
            edges = graph.number_of_edges()
            try:
                diameter = nx.diameter(graph)
            except NetworkXError:
                diameter = '-'

            try:
                density = nx.density(graph)
            except NetworkXError:
                density = '-'

            result_df.loc[len(result_df.index)] = [file_name, nodes, edges, density, diameter, triangles]

    result_df.to_csv('output/datasets_stats.csv', sep=',', index=False)


def run_algorithm(run_func, algorithm_name, result):

    for filepath in sorted(Path(directory).iterdir()):
        if filepath.is_file():
            file_name = filepath.name

            df = pd.read_csv(filepath, delimiter=',')
            graph = nx.from_pandas_edgelist(df, 'node_1', 'node_2')

            start_time = time.time()
            (triangles, triangle_operations) = run_func(graph)
            end_time = time.time()

            result.loc[len(result.index)] = [algorithm_name, (end_time - start_time), file_name,
                                             triangle_operations, len(triangles)]


def run_algorithms():
    result = pd.DataFrame(columns=['algorithm', 'execution_time', 'dataset', 'triangle_operations', 'triangles'])

    run_algorithm(NodeIterator.run, 'Node Iterator', result)
    run_algorithm(CompactForward.run, 'Compact Forward', result)

    result.to_csv('output/node_iterator_compact_forward_results.csv', sep=',', index=False)


def run_doulion():
    doulion_results = pd.DataFrame(
        columns=['algorithm', 'execution_time', 'dataset', 'triangle_operations', 'triangles',
                 'initial_graph_triangles', 'p'])

    p_values = [0.1, 0.3, 0.5, 0.7]

    for filepath in sorted(Path(directory).iterdir()):
        if filepath.is_file():
            for p in p_values:
                file_name = filepath.name

                df = pd.read_csv(filepath, delimiter=',')
                graph = nx.from_pandas_edgelist(df, 'node_1', 'node_2')

                sparsified_graph = Doulion.sparsify(graph, p)

                start_time = time.time()
                (triangles, triangle_operations) = NodeIterator.run(sparsified_graph)
                end_time = time.time()

                doulion_results.loc[len(doulion_results.index)] = ['Node Iterator', (end_time - start_time),
                                                                   file_name, triangle_operations, len(triangles),
                                                                   (len(triangles) * (1 / (p ** 3))), p]

                start_time = time.time()
                (triangles, triangle_operations) = CompactForward.run(sparsified_graph)
                end_time = time.time()

                doulion_results.loc[len(doulion_results.index)] = ['Compact Forward', (end_time - start_time),
                                                                   file_name, triangle_operations, len(triangles),
                                                                   (len(triangles) * (1 / (p ** 3))), p]

    doulion_results.to_csv('output/doulion_results.csv', sep=',', index=False)


def run_triest():
    triest_results = pd.DataFrame(columns=['algorithm', 'execution_time', 'dataset', 'Global Triangle Estimation','Local Triangle Estimation', 'initial_graph_triangles'])
    
    for filepath in sorted(Path(directory).iterdir()):
        if filepath.is_file():
            file_name = filepath.name

            try:
              print(file_name)
              df = pd.read_csv(filepath, delimiter=',')

              tr = Triest(1000000)
              start_time = time.time()
              estimation = tr.run(tr,df)
              end_time = time.time()

              global_est = estimation['global']
              local_est = estimation['local']

              triest_results.loc[len(triest_results.index)] = ['Triest', (end_time - start_time), file_name, global_est, local_est, 0]
            except KeyError as e:
                print(f"Skipping dataset {file_name} due to KeyError: {e}")
                continue  # Move to the next dataset

    triest_results.to_csv('output/triest_results.csv', sep=',', index=False)




store_dataset_properties()
run_algorithms()
run_doulion()
run_triest()
