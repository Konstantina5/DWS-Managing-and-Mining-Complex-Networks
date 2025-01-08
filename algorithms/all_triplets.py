class AllTriplets:
    @staticmethod
    def run(graph):
        triangles = set()
        triangle_operations = 0

        for node1 in graph:
            for node2 in graph:
                if node1 != node2:  # check that node1 is not equal to node2
                    for node3 in graph:
                        triangle_operations += 1
                        if node1 != node3 and node2 != node3:  # check that all three nodes are different
                            # if all nodes are connected to each other
                            if node1 in graph[node2] and node1 in graph[node3] and node2 in graph[node3]:
                                # check if the triangle has already been detected
                                triangles.add(tuple(sorted([node1, node2, node3])))

        return (triangles, triangle_operations)