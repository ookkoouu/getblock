# Get Block

This library allows to get block placed at current execution context.

## Usage

All functions return result to storage `getblock:`.

### `getblock:block`

**Input**: None  
**Output**:

- `id`: ID of the block
- `short_id`: Un-namespaced ID of the block
- `state`: State of the block
- `data`: Data obtained by command `data get block ~ ~ ~`
- `x`, `y`, `z`: Coordinates of the block

```mcfunction
function getblock:block
data get storage getblock: output
```

```json
{
  "id": "minecraft:dispenser",
  "short_id": "dispenser",
  "state": {
    "triggered": "false",
    "facing": "north"
  },
  "data": {
    "Items": [],
    "x": 0,
    "y": 56,
    "z": 0,
    "id": "minecraft:dispenser"
  },
  "x": 0,
  "y": 56,
  "z": 0
}
```

### `getblock:id`

Get only id  
**Input**: None  
**Output**:

- `id`: ID of the block

```json
{
  "id": "minecraft:dispenser"
}
```

### `getblock:state`

Get only state  
**Input**: None  
**Output**:

- `state`: State of the block

```json
{
  "state": {
    "triggered": "false",
    "facing": "north"
  }
}
```
