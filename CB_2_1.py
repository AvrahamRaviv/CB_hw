import itertools
import networkx as nx
from networkx.algorithms import isomorphism
import itertools
import networkx as nx
from networkx.algorithms import isomorphism


def generate_subgraphs(n):
    # Initialize the list of nodes
    nodes = list(range(1, n+1))
    # Generate all directed edges between the nodes
    all_edges = list(itertools.permutations(nodes, 2))
    # Set to store connected subgraphs
    connected_subgraphs = set()

    # Iterate over all possible edge combinations
    for edge_set in itertools.chain.from_iterable(itertools.combinations(all_edges, r) for r in range(1, len(all_edges) + 1)):
        # Create a directed graph from the edge set
        graph = nx.DiGraph(edge_set)
        # Check if the graph is weakly connected and has the required number of nodes
        if nx.is_weakly_connected(graph) and len(graph.nodes) == n:
            iso_match = False
            # Check if the graph is isomorphic to any of the existing connected subgraphs
            for existing_subgraph in connected_subgraphs:
                if isomorphism.DiGraphMatcher(graph, existing_subgraph).is_isomorphic():
                    iso_match = True
                    break
            # If not isomorphic, add the graph to the connected subgraphs set
            if not iso_match:
                connected_subgraphs.add(graph)

    return connected_subgraphs


def save_to_file(n, subgraphs, file_name):
    # Save the connected subgraphs to a file
    with open(file_name, 'w') as f:
        f.write(f"n={n}\n")
        f.write(f"count={len(subgraphs)}\n")
        for idx, graph in enumerate(subgraphs, 1):
            f.write(f"#{idx}\n")
            for edge in graph.edges:
                f.write(f"{edge[0]} {edge[1]}\n")


if __name__ == "__main__":
    for n in range(1, 5):
        connected_subgraphs = generate_subgraphs(n)
        save_to_file(n, connected_subgraphs, f"connected_subgraphs/CSG_{n}.txt")
