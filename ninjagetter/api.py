from typing import Literal, TypedDict

import requests

ENDPOINT = f"https://poe.ninja/api/data/0/getbuildoverview"

PARAMS = {"overview": "sanctum", "type": "exp", "language": "en"}


class Character(TypedDict):
    name: str
    level: int
    life: int
    es: int
    uniques: list[str]


def get_n_characters(n: int) -> list[Character] | Literal["No builds found."]:
    """
    Get the first n characters in the list storing their name, level, life, es, and worn unique items
    """
    builds = _try_get_builds()

    if builds:
        characters: list[Character] = []
        for i in range(n):
            c: Character = Character(name="", level=-1, life=-1, es=-1, uniques=[])
            c["name"] = builds["names"][i]
            c["level"] = builds["levels"][i]
            c["life"] = builds["life"][i]
            c["es"] = builds["energyShield"][i]
            c["uniques"] = []
            for idx, unique in enumerate(builds["uniqueItems"]):
                if _is_user_in_deltas(i, builds["uniqueItemUse"][str(idx)]):
                    c["uniques"].append(unique["name"])
            characters.append(c)
        return characters
    else:
        return "No builds found."


def _try_get_builds():
    r = requests.get(url=ENDPOINT, params=PARAMS)
    try:
        return r.json()
    except:
        return {}


def _is_user_in_deltas(
    user_idx: int, deltas: list, start_idx: int = 0, running_total: int = 0
):
    for i, delta in enumerate(deltas[start_idx:]):
        running_total += delta
        if user_idx == running_total:
            return i, running_total
