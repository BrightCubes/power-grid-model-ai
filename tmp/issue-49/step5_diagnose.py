from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from power_grid_model import PowerGridModel
from power_grid_model.utils import import_json_data


def load_input_data(path: Path) -> dict:
    """Load the original user dataset for diagnosis experiments."""
    return import_json_data(path, data_type="input")


def run_power_flow(input_data: dict, label: str) -> None:
    """Run asymmetric power flow and report success or failure class."""
    print(f"\nCase: {label}")
    try:
        PowerGridModel(input_data=input_data).calculate_power_flow(symmetric=False)
        print("  Result: SUCCESS")
    except Exception as error:  # noqa: BLE001
        print(f"  Result: {type(error).__name__}")
        print(f"  Message: {str(error).splitlines()[0]}")


def apply_corrections(input_data: dict) -> dict:
    """Apply key data corrections inferred from validation findings."""
    corrected = deepcopy(input_data)
    corrected["source"]["u_ref"] = 1.0

    for transformer in corrected["transformer"]:
        tap_min = min(int(transformer["tap_min"]), int(transformer["tap_max"]))
        tap_max = max(int(transformer["tap_min"]), int(transformer["tap_max"]))
        transformer["tap_pos"] = tap_min

    return corrected


def main() -> None:
    """Test hypotheses to classify root cause as data bug or PGM bug."""
    input_path = Path(__file__).with_name("out.json")
    input_data = load_input_data(input_path)

    run_power_flow(input_data, "original data")

    corrected = apply_corrections(input_data)
    run_power_flow(corrected, "source u_ref and tap_pos corrected")


if __name__ == "__main__":
    main()
