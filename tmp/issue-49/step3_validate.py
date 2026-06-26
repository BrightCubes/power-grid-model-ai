from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np
from power_grid_model.utils import import_json_data
from power_grid_model.validation import validate_input_data


def load_input_data(path: Path) -> dict:
    """Load input data from JSON for comprehensive validation checks."""
    return import_json_data(path, data_type="input")


def run_structural_validation(input_data: dict) -> None:
    """Run built-in PGM structural validation and print all findings."""
    print("=== 3a. Built-in structural validation ===")
    errors = validate_input_data(input_data)
    if errors:
        for error in errors:
            print(f"  VALIDATION ERROR: {error}")
    else:
        print("  No structural validation errors.")


def run_cross_component_checks(input_data: dict) -> None:
    """Check consistency between connected component parameters."""
    print("\n=== 3b. Cross-component consistency checks ===")
    nodes = input_data["node"]
    node_voltage_by_id = {int(node["id"]): float(node["u_rated"]) for node in nodes}

    if "transformer" in input_data:
        for transformer in input_data["transformer"]:
            from_u = node_voltage_by_id[int(transformer["from_node"])]
            to_u = node_voltage_by_id[int(transformer["to_node"])]
            if not np.isclose(transformer["u1"], from_u, rtol=0.15):
                print(
                    "  MISMATCH: transformer "
                    f"{transformer['id']} u1={transformer['u1']} vs from_node u_rated={from_u}"
                )
            if not np.isclose(transformer["u2"], to_u, rtol=0.15):
                print(
                    "  MISMATCH: transformer "
                    f"{transformer['id']} u2={transformer['u2']} vs to_node u_rated={to_u}"
                )
            tap_min = min(int(transformer["tap_min"]), int(transformer["tap_max"]))
            tap_max = max(int(transformer["tap_min"]), int(transformer["tap_max"]))
            tap_pos = int(transformer["tap_pos"])
            if not (tap_min <= tap_pos <= tap_max):
                print(
                    f"  SUSPECT: transformer {transformer['id']} tap_pos={tap_pos} "
                    f"outside [{tap_min}, {tap_max}]"
                )

    if "source" in input_data:
        for source in input_data["source"]:
            node_u = node_voltage_by_id[int(source["node"])]
            effective_v = float(source["u_ref"]) * node_u
            if not (0.8 < float(source["u_ref"]) < 1.2):
                print(
                    f"  SUSPECT: source {source['id']} u_ref={source['u_ref']} "
                    f"far from 1.0 pu; effective voltage = {effective_v:.0f} V"
                )


def run_physical_plausibility_checks(input_data: dict) -> None:
    """Check common physical plausibility ranges for lines, loads, and transformers."""
    print("\n=== 3c. Physical plausibility checks ===")

    nodes = input_data["node"]
    print("  Voltage levels:", np.unique(nodes["u_rated"]))

    for component in ("line", "asym_line"):
        if component not in input_data:
            continue
        array = input_data[component]
        r_field = "r1" if component == "line" else "r_aa"
        x_field = "x1" if component == "line" else "x_aa"

        zero_r = array[array[r_field] <= 0]
        if len(zero_r):
            print(f"  SUSPECT: {len(zero_r)} {component}(s) with r <= 0: ids={zero_r['id'][:10]}")

        zero_x = array[array[x_field] <= 0]
        if len(zero_x):
            print(f"  SUSPECT: {len(zero_x)} {component}(s) with x <= 0: ids={zero_x['id'][:10]}")

    for component in ("sym_load", "asym_load"):
        if component not in input_data:
            continue
        array = input_data[component]
        p_field = "p_specified"
        p_total = array[p_field] if component == "sym_load" else array[p_field].sum(axis=1)
        large = array[np.abs(p_total) > 1e8]
        if len(large):
            print(f"  SUSPECT: {len(large)} {component}(s) with |P| > 100 MW")

    if "transformer" in input_data:
        for transformer in input_data["transformer"]:
            uk = float(transformer["uk"])
            if not (0.02 <= uk <= 0.25):
                print(
                    f"  SUSPECT: transformer {transformer['id']} uk={uk:.3f} "
                    "outside typical 2-25%"
                )


def run_topology_checks(input_data: dict) -> None:
    """Check source reachability and disabled components that may isolate islands."""
    print("\n=== 3d. Topology checks ===")
    nodes = input_data["node"]
    source_node_ids = set(map(int, input_data["source"]["node"]))
    adjacency: dict[int, set[int]] = {int(node_id): set() for node_id in nodes["id"]}

    for component in ("line", "asym_line"):
        if component in input_data:
            for row in input_data[component]:
                if int(row["from_status"]) and int(row["to_status"]):
                    from_node = int(row["from_node"])
                    to_node = int(row["to_node"])
                    adjacency[from_node].add(to_node)
                    adjacency[to_node].add(from_node)

    if "transformer" in input_data:
        for transformer in input_data["transformer"]:
            if int(transformer["from_status"]) and int(transformer["to_status"]):
                from_node = int(transformer["from_node"])
                to_node = int(transformer["to_node"])
                adjacency[from_node].add(to_node)
                adjacency[to_node].add(from_node)

    visited = set(source_node_ids)
    queue: deque[int] = deque(source_node_ids)
    while queue:
        node = queue.popleft()
        for neighbour in adjacency.get(node, set()):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

    unreachable = set(map(int, nodes["id"])) - visited
    if unreachable:
        print(f"  DISCONNECTED: {len(unreachable)} nodes not reachable: {sorted(unreachable)[:20]}")
    else:
        print("  Topology: all nodes reachable from source(s).")

    for component in ("line", "asym_line", "transformer"):
        if component not in input_data:
            continue
        array = input_data[component]
        disabled = array[(array["from_status"] == 0) | (array["to_status"] == 0)]
        if len(disabled):
            print(
                f"  INFO: {len(disabled)} {component}(s) disabled: "
                f"ids={disabled['id'][:10]}"
            )


def main() -> None:
    """Run all validation and plausibility checks relevant to this issue."""
    input_path = Path(__file__).with_name("out.json")
    input_data = load_input_data(input_path)
    run_structural_validation(input_data)
    run_cross_component_checks(input_data)
    run_physical_plausibility_checks(input_data)
    run_topology_checks(input_data)


if __name__ == "__main__":
    main()
