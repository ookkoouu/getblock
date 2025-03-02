import requests


def packformat(version: str) -> int:
    url = f"https://raw.githubusercontent.com/misode/mcmeta/refs/tags/{version}-summary/version.json"
    return requests.get(url).json()["data_pack_version"]
