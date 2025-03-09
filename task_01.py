import networkx as nx
from typing import Dict, Tuple, List

def build_graph() -> nx.DiGraph:
    """
    Створює орієнтований граф логістичної мережі.
    """
    G = nx.DiGraph()
    
    edges = [
        ("Термінал 1", "Склад 1", 25),
        ("Термінал 1", "Склад 2", 20),
        ("Термінал 1", "Склад 3", 15),
        ("Термінал 2", "Склад 3", 15),
        ("Термінал 2", "Склад 4", 30),
        ("Термінал 2", "Склад 2", 10),
        ("Склад 1", "Магазин 1", 15),
        ("Склад 1", "Магазин 2", 10),
        ("Склад 1", "Магазин 3", 20),
        ("Склад 2", "Магазин 4", 15),
        ("Склад 2", "Магазин 5", 10),
        ("Склад 2", "Магазин 6", 25),
        ("Склад 3", "Магазин 7", 20),
        ("Склад 3", "Магазин 8", 15),
        ("Склад 3", "Магазин 9", 10),
        ("Склад 4", "Магазин 10", 20),
        ("Склад 4", "Магазин 11", 10),
        ("Склад 4", "Магазин 12", 15),
        ("Склад 4", "Магазин 13", 5),
        ("Склад 4", "Магазин 14", 10),
    ]

    for u, v, capacity in edges:
        G.add_edge(u, v, capacity=capacity)
    
    return G

def compute_max_flow(G: nx.DiGraph, sources: List[str], sinks: List[str]) -> Tuple[int, Dict[str, Dict[str, int]]]:
    """
    Обчислює максимальний потік у логістичній мережі.
    """
    super_source, super_sink = "Джерело", "Стік"
    
    for source in sources:
        G.add_edge(super_source, source, capacity=float('inf'))
    for sink in sinks:
        G.add_edge(sink, super_sink, capacity=float('inf'))
    
    flow_value, flow_dict = nx.maximum_flow(G, super_source, super_sink, flow_func=nx.algorithms.flow.edmonds_karp)
    
    G.remove_node(super_source)
    G.remove_node(super_sink)
    
    return flow_value, flow_dict

def calculate_terminal_to_store_flows(flow_dict: Dict[str, Dict[str, int]], sources: List[str], intermediate_nodes: List[str], sinks: List[str]) -> Dict[Tuple[str, str], int]:
    """
    Обчислює фактичні потоки між терміналами та магазинами.
    """
    terminal_to_store_flows = {}
    for source in sources:
        for sink in sinks:
            total_flow = 0
            for intermediate in intermediate_nodes:
                flow_to_intermediate = flow_dict.get(source, {}).get(intermediate, 0)
                flow_from_intermediate = flow_dict.get(intermediate, {}).get(sink, 0)
                total_flow += min(flow_to_intermediate, flow_from_intermediate)
            terminal_to_store_flows[(source, sink)] = total_flow
    return terminal_to_store_flows

def main() -> None:
    """Основна функція додатку."""
    G = build_graph()
    sources = ["Термінал 1", "Термінал 2"]
    intermediate_nodes = ["Склад 1", "Склад 2", "Склад 3", "Склад 4"]
    sinks = [
        "Магазин 1", "Магазин 2", "Магазин 3", "Магазин 4", "Магазин 5", "Магазин 6",
        "Магазин 7", "Магазин 8", "Магазин 9", "Магазин 10", "Магазин 11", "Магазин 12",
        "Магазин 13", "Магазин 14"
    ]
    
    max_flow, flow_distribution = compute_max_flow(G, sources, sinks)
    print(f"Максимальний потік через всю мережу: {max_flow}")
    
    terminal_to_store_flows = calculate_terminal_to_store_flows(flow_distribution, sources, intermediate_nodes, sinks)
    print("Таблиця потоків між терміналами та магазинами:")
    for (source, sink), flow in terminal_to_store_flows.items():
        print(f"{source} -> {sink}: {flow}")

if __name__ == "__main__":
    main()

