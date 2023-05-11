import itertools
import networkx as nx
from networkx.algorithms import isomorphism

def read_input_graph():
    edges = []
    print("Enter the graph edges, one per line (press Enter twice or use Ctrl+D/Ctrl+Z to finish):")
    while True:
        try:
            edge = input().split()
            if not edge:
                break
            edge_tuple = tuple(map(int, edge))
            edges.append(edge_tuple)
            print(f"Edge added: {edge_tuple}")
        except EOFError:
            break
    return nx.DiGraph(edges)


def all_directed_edges(nodes):
    return list(itertools.permutations(nodes, 2))


def generate_subgraphs(n, nodes):
    all_edges = all_directed_edges(nodes)
    connected_subgraphs = set()

    for edge_set in itertools.chain.from_iterable(itertools.combinations(all_edges, r) for r in range(1, len(all_edges) + 1)):
        graph = nx.DiGraph(edge_set)
        if nx.is_weakly_connected(graph) and len(graph.nodes) == n:
            iso_match = False
            for existing_subgraph in connected_subgraphs:
                if isomorphism.DiGraphMatcher(graph, existing_subgraph).is_isomorphic():
                    iso_match = True
                    break
            if not iso_match:
                connected_subgraphs.add(graph)

    return connected_subgraphs


def count_motifs(input_graph, subgraphs):
    counts = []
    for subgraph in subgraphs:
        count = 0
        for sub_nodes in itertools.combinations(input_graph.nodes, len(subgraph.nodes)):
            induced_subgraph = input_graph.subgraph(sub_nodes).copy()
            if isomorphism.DiGraphMatcher(induced_subgraph, subgraph).is_isomorphic():
                count += 1
        counts.append(count)
    return counts


def print_output(subgraphs, counts):
    print(f"count={len(subgraphs)}")
    counter = 0
    for idx, (graph, count) in enumerate(zip(subgraphs, counts), 1):
        print(f"#{idx} contains={bool(count)}")
        counter += count
        for edge in graph.edges:
            print(f"{edge[0]} {edge[1]}")
    print(f"count={counter}")


if __name__ == "__main__":
    n = int(input("Enter a positive integer n: "))
    input_graph = read_input_graph()
    connected_subgraphs = generate_subgraphs(n, input_graph.nodes)
    motif_counts = count_motifs(input_graph, connected_subgraphs)
    print_output(connected_subgraphs, motif_counts)
