# PGM-DS Overview and Core Objects

## Purpose of PGM-DS
`power-grid-model-ds` provides an application-facing grid model on top of PGM.
Use it when you need:
- Safer grid mutations
- Graph-aware analysis
- Easier array handling with typed abstractions
- Tight integration with PGM calculations

## Core Types
- `Grid`: full network object with arrays and graph container
- `FancyArray`: typed structured-array wrapper
- `GraphContainer`: maintains active and complete graph views
- `PowerGridModelInterface`: bridge between `Grid` and `PowerGridModel`

## Building a Grid
```python
from power_grid_model_ds import Grid

grid = Grid.empty()
```

Other constructors:
- `Grid.from_txt(...)` and `Grid.from_txt_file(...)`
- `Grid.from_cache(...)` (pickle-based; trusted sources only)
- `Grid.deserialize(path)` and `Grid.from_json_string(...)`
- `RadialGridGenerator(...).run(seed=...)`

## FancyArray Essentials
Common capabilities:
- `zeros(num)` and `empty(num)`
- `filter(...)`, `exclude(...)`, `get(...)`
- `update_by_id(...)`
- `as_df()`
- `check_ids()`

Design notes:
- Define custom arrays by subclassing `FancyArray`.
- Use `_defaults` for fill values.
- Prefer enums over string fields when possible for memory efficiency.

## Grid Container Behaviors
`Grid` tracks:
- Typed component arrays (`node`, `line`, `transformer`, sensors, etc.)
- `graphs` with active and complete topology views
- ID integrity across arrays

Useful properties/methods:
- `branch_arrays`, `branches`
- `append(array)`
- `rebuild_ids()`, `check_ids()`
- `rebuild_graphs()`
- `diff(other_grid)` for debugging

## Extending Grid with Custom Output Columns
PGM-DS supports extending arrays so output fields can be pushed back from calculation results.

Pattern:
1. Extend `NodeArray` / `LineArray` with extra columns.
2. Extend `Grid` dataclass using those array types.
3. Use `PowerGridModelInterface.update_grid()` after calculations.

## Safety Notes
- `Grid.from_cache(...)` uses pickle and can execute arbitrary code.
- Only load cache files from trusted sources.
- Prefer JSON `serialize`/`deserialize` for portable and safer interchange.
