from pathlib import Path
from beet import DataPack
import click
from mcdata import datapack, manifest
import gen_core
import gen_block
import gen_state
import gen_coords


@click.command()
@click.option("--version", "-v", help="minecraft version for generation (e.g. 1.21.4)")
@click.option("--channel", "-c", help="release channel to generate")
@click.option("--debug", is_flag=True, help="Whether to build in debug mode")
def main(
    version: str | None,
    channel: manifest.ReleaseChannel | None,
    debug: bool,
):
    if channel == None or channel != "release" or channel != "snapshot":
        channel = "release"

    if version == None or version == "latest":
        version = manifest.latest_version(channel)

    pack_format = datapack.packformat(version)
    if pack_format < 7:
        print("Versions less than 1.17 are not supported")
        return
    if pack_format < 45:
        # 1.17 ~ 1.20.6
        # version_range = "1.17-1.20.6"
        supported_versions = manifest.range_version("1.17", "1.20.6")
        min_format = 7
        max_format = 44
    if 45 <= pack_format:
        # 1.21 ~
        # version_range = f"1.21-{mcversion}"
        supported_versions = manifest.range_version("1.21")
        min_format = 45
        max_format = 999

    print(f"Generating for {version}({pack_format})")

    code_version = Path("version.txt").read_text("utf8").strip()
    pack = DataPack(
        f"getblock-{code_version}+mc{version}",
        description="Adds getblock function to get id, State and Data of the block",
        pack_format=min_format,
        supported_formats={"min_inclusive": min_format, "max_inclusive": max_format},
    )

    if debug:
        gen_core.gen_debug(pack)
    gen_core.gen_core(pack)
    gen_block.gen_block(pack, version)
    gen_state.gen_state(pack, version)
    gen_coords.gen_coords(pack)

    pack.save(directory="build", overwrite=True, zipped=True)
    if debug:
        pack.save(directory="build", overwrite=True, zipped=False)

    f = Path("build/supported-versions.txt")
    f.write_text("\n".join(supported_versions))


if __name__ == "__main__":
    main()
