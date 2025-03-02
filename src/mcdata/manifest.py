from dataclasses import dataclass
from typing import Literal

import requests

type ReleaseChannel = Literal["snapshot", "release"]


@dataclass
class Latest:
    release: str
    snapshot: str


@dataclass
class Version:
    id: str
    type: ReleaseChannel
    url: str
    time: str
    releaseTime: str
    sha1: str
    complianceLevel: int


@dataclass
class VersionManifest:
    latest: Latest
    versions: list[Version]
    ids: list[str]

    def releases(self):
        return list(
            map(lambda v: v.id, filter(lambda v: v.type == "release", self.versions))
        )

    def snapshots(self):
        return list(
            map(lambda v: v.id, filter(lambda v: v.type == "snapshot", self.versions))
        )


def manifest():
    url = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
    data = requests.get(url).json()
    return VersionManifest(
        latest=Latest(**data["latest"]),
        versions=list(
            map(
                lambda v: Version(**v),
                filter(
                    lambda v: v["type"] == "release" or v["type"] == "snapshot",
                    data["versions"],
                ),
            )
        ),
        ids=list(
            map(
                lambda v: v["id"],
                filter(
                    lambda v: v["type"] == "release" or v["type"] == "snapshot",
                    data["versions"],
                ),
            )
        ),
    )


def latest_version(channel: ReleaseChannel = "release"):
    if channel == "release":
        return manifest().latest.release
    else:
        return manifest().latest.snapshot


def range_version(
    min="",
    max="",
    filter: ReleaseChannel = "release",
    min_inclusive=True,
    max_inclusice=True,
):
    if filter == "release":
        versions = manifest().releases()  # [new, ..., old]
    else:
        versions = manifest().snapshots()  # [new, ..., old]

    try:
        start = versions.index(max)
        if not max_inclusice:
            start = start + 1
    except:
        start = 0

    try:
        end = versions.index(min)
        if min_inclusive:
            end = end + 1
    except:
        end = len(versions)

    return versions[start:end]
