from beet import DataPack, Function, Predicate
from mcdata import block


def gen_state(
    pack: DataPack,
    version: str,
    namespace="getblock",
    function_dir="zzz_internal",
    predicate_dir="zzz_internal",
    root_name="_",
    storage_name="",
):
    block_states = block.state_entries(version)

    # root function
    pack.functions[f"{namespace}:{function_dir}/state/{root_name}"] = Function(
        list(
            map(
                lambda state: f"execute if predicate {namespace}:{predicate_dir}/state/{state[0]}/{root_name} run function {namespace}:{function_dir}/state/{state[0]}/{root_name}",
                block_states,
            )
        )
    )

    for state_name, state_values in block_states:
        for state_value in state_values:
            # value check predicate
            pack.predicates[
                f"{namespace}:{predicate_dir}/state/{state_name}/{state_value}"
            ] = Predicate(
                {
                    "condition": "minecraft:location_check",
                    "predicate": {
                        "block": {
                            "state": {
                                state_name: state_value,
                            },
                        },
                    },
                }
            )

            # store value function
            pack.functions[
                f"{namespace}:{function_dir}/state/{state_name}/{state_value}"
            ] = Function(
                f'data modify storage {namespace}:{storage_name} output.state.{state_name} set value "{state_value}"',
            )

        # state holder predicate
        pack.overlays.pack.predicates
        pack.predicates[
            f"{namespace}:{predicate_dir}/state/{state_name}/{root_name}"
        ] = Predicate(
            {
                "condition": "minecraft:location_check",
                "predicate": {
                    "block": {
                        "state": {
                            state_name: {},
                        },
                    },
                },
            }
        )

        # state parent function
        pack.functions[f"{namespace}:{function_dir}/state/{state_name}/{root_name}"] = (
            Function(
                list(
                    map(
                        lambda state_value: f"execute if predicate {namespace}:{predicate_dir}/state/{state_name}/{state_value} run function {namespace}:{predicate_dir}/state/{state_name}/{state_value}",
                        state_values,
                    )
                )
            )
        )
