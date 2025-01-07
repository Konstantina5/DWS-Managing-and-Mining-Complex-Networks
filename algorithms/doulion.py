import networkx as nx
from networkx import Graph
from numpy.random import choice


class Doulion:
    @staticmethod
    def sparsify(G: Graph, p):
        G_sparcified = nx.Graph()
        for e in G.edges:
            if choice([True, False], p=[p, 1 - p]):
                G_sparcified.add_edge(e[0], e[1])
            else:
                G.remove_edge(*e)
        return G_sparcified

    @staticmethod
    def run(G, p, algorithm_function):
        return algorithm_function(Doulion.sparsify(G, p))
