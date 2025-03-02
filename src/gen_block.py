from beet import DataPack, Function, BlockTag
import math
from mcdata import block


def index_char(n: int) -> str:
    return str(n) if n < 10 else chr(n - 10 + ord("a"))


def gen_block(
    pack: DataPack,
    version: str,
    divide=16,
    namespace="getblock",
    function_dir="zzz_internal",
    tag_dir="zzz_internal",
    root_name="_",
    storage_name="",
):
    block_ids = block.block_ids(version)

    if len(block_ids) == 0:
        return

    def create_files(index: str, blocks: list[str]):
        n = len(blocks)
        filename = root_name if index == "" else index

        if n == 1:
            # block check tag
            pack.block_tags[f"{namespace}:{tag_dir}/block/{filename}"] = BlockTag(
                {"values": [f"minecraft:{blocks[0]}"]}
            )
            # store id function
            pack.functions[f"{namespace}:{function_dir}/block/{filename}"] = Function(
                [
                    f'data modify storage {namespace}:{storage_name} output.id set value "minecraft:{blocks[0]}"',
                    f'data modify storage {namespace}:{storage_name} output.short_id set value "{blocks[0]}"',
                ]
            )
            return

        chunk_count = math.ceil(n / math.ceil(n / divide))
        chunk_size = math.ceil(n / divide)
        next_indexes: list[str] = []

        for i in range(chunk_count):
            chunk = blocks[i * chunk_size : (i + 1) * chunk_size]
            if len(chunk) == 0:
                continue
            next_index = f"{index}{index_char(i)}"
            next_indexes.append(next_index)
            create_files(next_index, chunk)

        pack.block_tags[f"{namespace}:{tag_dir}/block/{filename}"] = BlockTag(
            {
                "values": list(
                    map(
                        lambda next_index: {
                            "id": f"#{namespace}:{tag_dir}/block/{next_index}",
                            "required": False,
                        },
                        next_indexes,
                    )
                )
            }
        )

        pack.functions[f"{namespace}:{function_dir}/block/{filename}"] = Function(
            [
                f"execute if block ~ ~ ~ {f"#{namespace}:{tag_dir}/block/{next_index}"} run function {
                    namespace}:{function_dir}/block/{next_index}"
                for next_index in next_indexes
            ]
        )

    create_files("", block_ids)
