from __future__ import annotations

from pathlib import Path

import numpy as np
from power_grid_model.utils import import_json_data


def load_input_data(path: Path) -> dict:
    """Load input data from JSON for structural analysis."""
    return import_json_data(path, data_type="input")


def print_component_counts(input_data: dict) -> None:
    """Print all component types and their instance counts."""
    for component, array in input_data.items():
        print(f"{component}: {len(array)}")


def print_voltage_levels(nodes: np.ndarray) -> None:
    """Print unique node rated-voltage levels present in the network."""
    print("Unique node u_rated values:", np.unique(nodes["u_rated"]))


def print_transformer_connections(input_data: dict, nodes: np.ndarray) -> None:
    """Print transformer terminal voltage consistency information."""
    if "transformer" not in input_data:
        return
    node_voltage_by_id = {int(node["id"]): float(node["u_rated"]) for node in nodes}
    for transformer in input_data["transformer"]:
        from_u = node_voltage_by_id[int(transformer["from_node"])]
        to_u = node_voltage_by_id[int(transformer["to_node"])]
        print(
            f"  Transformer {transformer['id']}: u1={transformer['u1']}  "
            f"u2={transformer['u2']}  from_node u_rated={from_u}  to_node u_rated={to_u}"
        )


def print_source_references(input_data: dict, nodes: np.ndarray) -> None:
    """Print source voltage references against connected node ratings."""
    if "source" not in input_data:
        return
    node_voltage_by_id = {int(node["id"]): float(node["u_rated"]) for node in nodes}
    for source in input_data["source"]:
        node_u = node_voltage_by_id[int(source["node"])]
        print(
            f"Source {source['id']}: node={source['node']}  "
            f"u_ref={source['u_ref']}  node u_rated={node_u}"
        )


def print_transformer_downstream_without_connections(input_data: dict) -> None:
    """Identify transformer LV/MV sides that have no downstream elements."""
    if "transformer" not in input_data:
        return

    all_connected: set[int] = set()
    for component in ("line", "asym_line"):
        if component in input_data:
            all_connected |= set(map(int, input_data[component]["from_node"]))
            all_connected |= set(map(int, input_data[component]["to_node"]))

    for component in ("sym_load", "asym_load", "sym_gen", "asym_gen", "shunt"):
        if component in input_data:
            all_connected |= set(map(int, input_data[component]["node"]))

    tr_to_nodes = set(map(int, input_data["transformer"]["to_node"]))
    empty = tr_to_nodes - all_connected
    print("Transformer to_nodes with nothing else connected:", sorted(empty))


def main() -> None:
    """Build a structural picture of the reported network model."""
    input_path = Path(__file__).with_name("out.json")
    input_data = load_input_data(input_path)
    nodes = input_data["node"]

    print_component_counts(input_data)
    print_voltage_levels(nodes)
    print_transformer_connections(input_data, nodes)
    print_source_references(input_data, nodes)
    print_transformer_downstream_without_connections(input_data)


if __name__ == "__main__":
    main()
