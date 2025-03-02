from beet import DataPack, Function, FunctionTag
import datetime


def gen_core(
    pack: DataPack,
    namespace="getblock",
    function_dir="zzz_internal",
    root_name="_",
    storage_name="",
):
    pack[f"{namespace}:block"] = Function(
        [
            f"data modify storage {namespace}:{storage_name} output set value {{}}",
            f"function {namespace}:{function_dir}/block/{root_name}",
            f"function {namespace}:{function_dir}/state/{root_name}",
            f"execute if data block ~ ~ ~ {{}} run data modify storage {namespace}:{storage_name} output.data set from block ~ ~ ~ {{}}",
            f"function {namespace}:{function_dir}/coords",
        ]
    )
    pack[f"{namespace}:id"] = Function(
        [
            f"data remove storage {namespace}:{storage_name} output",
            f"function {namespace}:{function_dir}/block/{root_name}",
        ]
    )
    pack[f"{namespace}:state"] = Function(
        [
            f"data remove storage {namespace}:{storage_name} output",
            f"function {namespace}:{function_dir}/state/{root_name}",
        ]
    )


def gen_debug(pack: DataPack):
    print("*debug build*")
    pack["minecraft:load"] = FunctionTag()

    quick_check(pack)
    performance_check(pack)


def quick_check(pack: DataPack):
    pack.function_tags["minecraft:load"].add("getblock:debug/quick")
    pack["getblock:debug/quick"] = Function(
        [
            f'tellraw @a "[getblock@{datetime.datetime.now().strftime("%H:%M:%S")}] loaded"',
            "setblock ~ ~ ~ minecraft:dispenser",
            "function getblock:id",
            'execute unless data storage getblock: output.id run tellraw @a "Error at ID"',
            "function getblock:state",
            'execute unless data storage getblock: output.state run tellraw @a "Error at State"',
            "function getblock:block",
            'execute unless data storage getblock: output.data run tellraw @a "Error at Block.data"',
            'execute unless data storage getblock: output.x run tellraw @a "Error at Block.coords"',
        ]
    )


def performance_check(pack: DataPack):
    pack["getblock:debug/perf"] = Function(
        [
            "execute positioned ~ ~-0.5 ~ run function getblock:block"
            for _ in range(10000)
        ]
    )


# def all_block_check(pack: DataPack, version: str):
#     data = fetch_data.block_data(version)

#     setblock_cmds = []
#     check_cmds = []
#     for i, [block, [_, defo]] in enumerate(data.items()):
#         id = f"minecraft:{block}"
#         coords = f"{math.floor(i/100)*2} 0 {(i%100)*2}"
#         setblock_cmds.append(f"setblock {coords} {id} strict")
#         check_cmds.append(f"execute positioned {coords} run function getblock:block")
#         check_cmds.append(
#             f'execute unless data storage getblock:block output{{id:"{id}"}} run tellraw @a "Search failed: {id}"'
#         )

#     pack["getblock:debug/all_block_prepare"] = Function(setblock_cmds)
#     pack["getblock:debug/all_block_check"] = Function(check_cmds)
#     pack["getblock:debug/all_block"] = Function(
#         [
#             "function getblock:debug/all_block_prepare",
#             "function getblock:debug/all_block_check",
#         ]
#     )

# pack.function_tags["getblock:debug"].add("getblock:debug/all_block")
