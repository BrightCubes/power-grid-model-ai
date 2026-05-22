# PGM-DS Mutations, Serialization, and Visualizer

## Topology Mutation APIs
Use these instead of manual array edits to keep graph consistency.

- `grid.append(array)`
- `grid.add_node(node)`
- `grid.delete_node(node)`
- `grid.add_branch(branch)`
- `grid.delete_branch(branch)`
- `grid.delete_branch3(branch3)`
- `grid.make_active(branch)`
- `grid.make_inactive(branch, at_to_side=True)`

## Merge Grids
```python
offset = grid.merge(other_grid, mode="recalculate_ids")
```

Modes:
- `keep_ids`: fail on collisions
- `recalculate_ids`: offset IDs in incoming grid to avoid collisions

## Grid Serialization
### Preferred portable format (JSON)
```python
grid.serialize(path_json, mode="json", indent=2)
loaded = Grid.deserialize(path_json)
```

### In-memory JSON string
```python
json_text = grid.serialize(mode="json_string")
loaded = Grid.from_json_string(json_text)
```

### Cache format (pickle-based)
```python
grid.cache(cache_dir, cache_name="baseline", compress=True)
loaded = Grid.from_cache(cache_path)
```

Warning:
- `from_cache` uses pickle; only use trusted files.

## Visualizer Quickstart
```python
from power_grid_model_ds.visualizer import visualize

visualize(grid)
```

This starts a local dashboard (default localhost).

Optional dependency install:
```bash
pip install 'power-grid-model-ds[visualizer]'
```

## Visualizer Use Cases
- Quick structural inspection before/after topology mutations
- Highlight problematic nodes/branches during debugging
- Compare feeder structures under switching scenarios

## Recommended Mutation Loop
1. Apply topology changes via grid methods.
2. Recompute feeder IDs / branch orientation if needed.
3. Run calculation through interface.
4. Update grid output fields.
5. Visualize and inspect.
