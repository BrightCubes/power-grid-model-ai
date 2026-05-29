from power_grid_model import CalculationMethod, ComponentType

from tests.data._generate_synthetic_pgm_data import (
    create_synthetic_input_data,
    create_synthetic_load_update_data,
    inject_invalid_sym_load_update,
    isolate_minimal_reproducible_sym_load_case,
    update_data_causes_error,
)


def test_isolate_minimal_reproducible_sym_load_case() -> None:
    _, input_data = create_synthetic_input_data(
        nr_nodes=50,
        nr_sources=1,
        nr_nops=0,
        seed=7,
        create_10_3_kv_net=False,
    )
    update_data = create_synthetic_load_update_data(
        input_data=input_data,
        n_steps=8,
        step_minutes=15,
        seed=11,
    )

    invalid_id = inject_invalid_sym_load_update(
        input_data=input_data,
        update_data=update_data,
        scenario_index=5,
        load_index=3,
    )

    assert update_data_causes_error(
        input_data=input_data,
        update_data=update_data,
        calculation_method=CalculationMethod.newton_raphson,
    )

    minimal_update_data = isolate_minimal_reproducible_sym_load_case(
        input_data=input_data,
        update_data=update_data,
        calculation_method=CalculationMethod.newton_raphson,
    )
    sym_load_key = next(
        key for key in minimal_update_data if getattr(key, "value", None) == ComponentType.sym_load.value
    )
    minimal_sym_load_update = minimal_update_data[sym_load_key]

    assert minimal_sym_load_update.shape == (1, 1)
    assert int(minimal_sym_load_update["id"][0, 0]) == invalid_id
    assert update_data_causes_error(
        input_data=input_data,
        update_data=minimal_update_data,
        calculation_method=CalculationMethod.newton_raphson,
    )
