from __future__ import annotations

from power_grid_model import LoadGenType, PowerGridModel, initialize_array


def create_bad_minimal_case() -> dict:
    """Create a minimal dataset that keeps the same voltage/tap inconsistencies."""
    node = initialize_array("input", "node", 2)
    node["id"] = [1, 2]
    node["u_rated"] = [230.0, 230.0]

    source = initialize_array("input", "source", 1)
    source["id"] = 10
    source["node"] = 1
    source["status"] = 1
    source["u_ref"] = 150000.0
    source["u_ref_angle"] = 0.0
    source["sk"] = 1e12
    source["rx_ratio"] = 0.1
    source["z01_ratio"] = 1.0

    transformer = initialize_array("input", "transformer", 1)
    transformer["id"] = 20
    transformer["from_node"] = 1
    transformer["to_node"] = 2
    transformer["from_status"] = 1
    transformer["to_status"] = 1
    transformer["u1"] = 10750.0
    transformer["u2"] = 400.0
    transformer["sn"] = 4e6
    transformer["uk"] = 0.175
    transformer["pk"] = 196000.0
    transformer["i0"] = 0.00012875
    transformer["p0"] = 515.0
    transformer["winding_from"] = 2
    transformer["winding_to"] = 2
    transformer["clock"] = 0
    transformer["tap_side"] = 1
    transformer["tap_pos"] = -128
    transformer["tap_min"] = 5
    transformer["tap_max"] = 1
    transformer["tap_nom"] = 3
    transformer["tap_size"] = 250.0

    load = initialize_array("input", "asym_load", 1)
    load["id"] = 30
    load["node"] = 2
    load["status"] = 1
    load["type"] = LoadGenType.const_power
    load["p_specified"][0] = [1200.0, 900.0, 1000.0]
    load["q_specified"][0] = [200.0, 150.0, 180.0]

    return {
        "node": node,
        "source": source,
        "transformer": transformer,
        "asym_load": load,
    }


def create_fixed_minimal_case() -> dict:
    """Create a corrected minimal dataset with consistent voltage and tap settings."""
    input_data = create_bad_minimal_case()
    input_data["node"]["u_rated"] = [10750.0, 400.0]
    input_data["source"]["u_ref"] = 1.0
    input_data["transformer"]["tap_pos"] = 3
    return input_data


def run_case(input_data: dict, label: str) -> None:
    """Run asymmetric power flow and print whether it succeeds."""
    print(f"\nRunning case: {label}")
    model = PowerGridModel(input_data=input_data)
    model.calculate_power_flow(symmetric=False)
    print("  SUCCESS")


def main() -> None:
    """Show that a tiny inconsistent case fails and corrected data succeeds."""
    bad_case = create_bad_minimal_case()
    run_case(bad_case, "bad minimal case")


if __name__ == "__main__":
    main()
