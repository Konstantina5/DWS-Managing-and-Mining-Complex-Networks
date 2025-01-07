class NodeIterator:
    @staticmethod
    def run(graph):
        triangles = set()
        triangle_operations = 0

        for node1 in graph:
            neighbors = list(graph.neighbors(node1))  # get neighbors of node
            # neighbors = graph[node1]
            for node2 in neighbors:
                for node3 in neighbors:
                    triangle_operations += 1
                    # check if they two neighbors are connected by an edge
                    if graph.has_edge(node2, node3):
                        if node2 != node3 and node1 != node2 and node1 != node3:
                            triangles.add(tuple(sorted([node1, node2, node3])))

        return (triangles, triangle_operations)
