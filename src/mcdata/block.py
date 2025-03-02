import json
from pathlib import Path
import requests

type BlockID = str
type BlockStates = list[tuple[str, list[str]]]
type BlockData = dict[str, tuple[dict[str, list[str]], dict[str, str]]]


def get_cache(version: str, dir=".mcmeta") -> tuple[bool, BlockData]:
    cache_file = Path(dir, f"blocks-{version}.json")
    if not cache_file.is_file():
        return (False, {})
    data: BlockData = json.loads(cache_file.read_text())
    return (True, data)


def set_cache(version: str, data: BlockData, dir=".mcmeta"):
    cache_file = Path(dir, f"blocks-{version}.json")

    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps(data, indent=2), "utf-8")


def block_data(version: str) -> BlockData:
    ok, data = get_cache(version)
    if not ok:
        url = f"https://github.com/misode/mcmeta/raw/refs/tags/{version}-summary/blocks/data.json"
        r = requests.get(url)
        if not r.ok:
            return ([], [])
        data: BlockData = r.json()
        set_cache(version, data)

    return data


def block_ids(version: str) -> list[BlockID]:
    data = block_data(version)
    return sorted(data)


def state_entries(version: str) -> BlockStates:
    data = block_data(version)
    state_map: dict[str, list[str]] = {}
    for _, state in data.items():
        for state_name, state_values in state[0].items():
            old = state_map.get(state_name) or []
            state_map[state_name] = sorted(list(set([*old, *state_values])))
    block_states = sorted([*state_map.items()])
    return block_states
