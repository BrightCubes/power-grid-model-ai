#!/usr/bin/env python3
"""Generate synthetic PGM JSON input/update datasets for skill testing."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from power_grid_model import CalculationType, ComponentType, DatasetType, initialize_array
from power_grid_model.utils import json_serialize_to_file
from power_grid_model.validation import assert_valid_batch_data, assert_valid_input_data
from power_grid_model_ds import Grid, PowerGridModelInterface
from power_grid_model_ds.generators import RadialGridGenerator


def _find_component_key(dataset: dict, component: ComponentType):
    if component in dataset:
        return component
    for key in dataset:
        if getattr(key, "value", None) == component.value:
            return key
    raise KeyError(f"Component {component.value} not found in dataset")


def create_synthetic_input_data(nr_nodes: int, seed: int) -> dict:
    generator = RadialGridGenerator(
        grid_class=Grid,
        nr_nodes=nr_nodes,
        nr_sources=1,
        nr_nops=0,
    )
    grid = generator.run(seed=seed, create_10_3_kv_net=False)
    interface = PowerGridModelInterface(grid=grid)
    return interface.create_input_from_grid()


def create_synthetic_load_update_data(
    input_data: dict,
    n_steps: int,
    step_minutes: int,
    seed: int,
) -> dict:
    sym_load_key = _find_component_key(input_data, ComponentType.sym_load)
    base_loads = input_data[sym_load_key]
    n_loads = len(base_loads)
    if n_loads == 0:
        raise ValueError("Synthetic grid has no symmetric loads to update")

    update_loads = initialize_array(
        DatasetType.update,
        ComponentType.sym_load,
        shape=(n_steps, n_loads),
    )
    load_ids = base_loads["id"].astype(np.int32, copy=False)
    update_loads["id"] = load_ids[np.newaxis, :]
    update_loads["status"] = 1

    base_p = np.maximum(base_loads["p_specified"].astype(np.float64), 1.0)
    base_q = base_loads["q_specified"].astype(np.float64)
    q_over_p = np.divide(base_q, base_p, out=np.zeros_like(base_q), where=np.abs(base_p) > 1e-9)

    step_index = np.arange(n_steps, dtype=np.float64)
    hours = (step_index * step_minutes / 60.0) % 24.0
    days = (step_index * step_minutes) / (24.0 * 60.0)

    daily_shape = (
        0.75
        + 0.20 * np.sin(2.0 * np.pi * (hours - 6.0) / 24.0)
        + 0.10 * np.sin(4.0 * np.pi * (hours - 15.0) / 24.0)
    )
    weekday_index = days.astype(np.int64) % 7
    weekend_factor = np.where(weekday_index >= 5, 0.92, 1.00)
    seasonal_factor = 0.96 + 0.07 * np.sin(2.0 * np.pi * days / 60.0)
    global_multiplier = np.clip(daily_shape * weekend_factor * seasonal_factor, 0.35, 1.40)

    rng = np.random.default_rng(seed)
    load_scaler = np.clip(rng.normal(loc=1.0, scale=0.12, size=n_loads), 0.70, 1.35)
    random_noise = np.clip(rng.normal(loc=1.0, scale=0.03, size=(n_steps, n_loads)), 0.85, 1.15)

    multiplier = np.clip(
        global_multiplier[:, np.newaxis] * load_scaler[np.newaxis, :] * random_noise,
        0.20,
        2.00,
    )
    p_series = base_p[np.newaxis, :] * multiplier
    q_series = p_series * q_over_p[np.newaxis, :]

    update_loads["p_specified"] = p_series
    update_loads["q_specified"] = q_series
    return {sym_load_key: update_loads}


def validate_datasets(input_data: dict, update_data: dict) -> None:
    assert_valid_input_data(
        input_data,
        calculation_type=CalculationType.power_flow,
        symmetric=True,
    )
    assert_valid_batch_data(
        input_data,
        update_data,
        calculation_type=CalculationType.power_flow,
        symmetric=True,
    )


def main() -> None:
    nr_nodes = 100
    step_minutes = 15
    nr_days = 60
    n_steps = nr_days * 24 * (60 // step_minutes)
    grid_seed = 20260522
    profile_seed = 20260523

    out_dir = Path(__file__).resolve().parent
    input_path = out_dir / "synthetic_input_data.json"
    update_path = out_dir / "synthetic_update_data.json"

    input_data = create_synthetic_input_data(nr_nodes=nr_nodes, seed=grid_seed)
    update_data = create_synthetic_load_update_data(
        input_data=input_data,
        n_steps=n_steps,
        step_minutes=step_minutes,
        seed=profile_seed,
    )
    validate_datasets(input_data=input_data, update_data=update_data)

    json_serialize_to_file(
        input_path,
        input_data,
        dataset_type=DatasetType.input
    )
    json_serialize_to_file(
        update_path,
        update_data,
        dataset_type=DatasetType.update,
        use_compact_list=True,
    )

    sym_load_key = _find_component_key(input_data, ComponentType.sym_load)
    print(f"Wrote input_data to: {input_path}")
    print(f"Wrote update_data to: {update_path}")
    print(f"Grid nodes: {len(input_data[_find_component_key(input_data, ComponentType.node)])}")
    print(f"Symmetric loads: {len(input_data[sym_load_key])}")
    print(f"Time steps: {n_steps} ({nr_days} days at {step_minutes}-minute resolution)")


if __name__ == "__main__":
    main()