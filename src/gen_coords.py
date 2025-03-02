from beet import DataPack, Function


def gen_coords(
    pack: DataPack,
    namespace="getblock",
    function_dir="zzz_internal",
    storage_name="",
):
    pack[f"{namespace}:{function_dir}/coords"] = Function(
        [
            f'execute align xyz run summon minecraft:marker ~ ~ ~ {{Tags:["{namespace}.coords"]}}',
            f"execute align xyz store result storage {namespace}:{storage_name} output.x int 1 run data get entity @e[type=minecraft:marker,tag={namespace}.coords,sort=nearest,limit=1] Pos[0]",
            f"execute align xyz store result storage {namespace}:{storage_name} output.y int 1 run data get entity @e[type=minecraft:marker,tag={namespace}.coords,sort=nearest,limit=1] Pos[1]",
            f"execute align xyz store result storage {namespace}:{storage_name} output.z int 1 run data get entity @e[type=minecraft:marker,tag={namespace}.coords,sort=nearest,limit=1] Pos[2]",
            f"execute align xyz run kill @e[type=minecraft:marker,tag={namespace}.coords]",
        ]
    )
