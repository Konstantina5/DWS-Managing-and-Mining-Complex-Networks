class CompactForward:
    @staticmethod
    def run(graph):

        sorted_degree = sorted(graph.degree, key=lambda x: x[1], reverse=True)
        eta = {node: i + 1 for i, (node, _) in enumerate(sorted_degree)}
        degree_per_node = dict(eta)

        triangles = set()
        triangle_operations = 0

        # for every node in the sorted_nodes list
        for v in sorted(eta, key=eta.get):
            neighbors = iter(sorted(graph.neighbors(v), key=lambda x: eta[x]))

            for u in neighbors:

                if degree_per_node[u] > degree_per_node[v]:
                    u_neighbors = iter(sorted(graph.neighbors(u), key=lambda x: eta[x]))
                    v_neighbors = iter(sorted(graph.neighbors(v), key=lambda x: eta[x]))

                    u_neighbor = next(u_neighbors, None)
                    v_neighbor = next(v_neighbors, None)
                    while (u_neighbor and v_neighbor) and degree_per_node[u_neighbor] < degree_per_node[v] and degree_per_node[v_neighbor] < degree_per_node[v]:
                        triangle_operations += 1
                        if degree_per_node[u_neighbor] < degree_per_node[v_neighbor]:
                            u_neighbor = next(u_neighbors, None)
                        elif degree_per_node[u_neighbor] > degree_per_node[v_neighbor]:
                            v_neighbor = next(v_neighbors, None)
                        else:
                            triangles.add(tuple(sorted([v, u, u_neighbor])))
                            u_neighbor = next(u_neighbors, None)
                            v_neighbor = next(v_neighbors, None)

        return (triangles, triangle_operations)