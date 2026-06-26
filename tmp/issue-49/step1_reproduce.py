from __future__ import annotations

import argparse
from pathlib import Path

from power_grid_model import PowerGridModel
from power_grid_model.utils import import_json_data


def parse_args() -> argparse.Namespace:
    """Parse command-line options for reproduction mode."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--symmetric", action="store_true", help="Run symmetric power flow")
    parser.add_argument("--input", type=Path, default=Path(__file__).with_name("out.json"))
    return parser.parse_args()


def load_input_data(path: Path) -> dict:
    """Load PGM input dataset from a JSON file."""
    return import_json_data(path, data_type="input")


def run_power_flow(input_data: dict, symmetric: bool) -> None:
    """Run one-time power flow with the requested symmetric mode."""
    model = PowerGridModel(input_data=input_data)
    model.calculate_power_flow(symmetric=symmetric)


def main() -> None:
    """Load the user dataset and reproduce the reported calculation failure."""
    args = parse_args()
    input_data = load_input_data(args.input)
    print(f"Running one-time power flow with symmetric={args.symmetric}")
    run_power_flow(input_data=input_data, symmetric=args.symmetric)


if __name__ == "__main__":
    main()
