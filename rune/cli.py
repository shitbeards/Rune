import os
import typing
import shutil
import operator

import requests

from docopt import docopt

from rune import api, const


def error(msg: str):
    print(msg)
    exit(1)


def _latest_file(addon: dict):
    files = [
        file
        for file in addon["latestFiles"]
        if file["releaseType"] == const.RELEASE
        and file["isAvailable"] is True
    ]

    if len(files) == 0:
        error(f"No addon release found for '{addon['slug']}'.")

    latest = sorted(files, key=operator.itemgetter("fileDate"))[0]

    return latest


def search(query: str):
    try:
        payload = api.search(query=query)
    except requests.HTTPError as e:
        error(f"{e.status_code}: {e.reason}")

    slugs = (item["slug"] for item in payload["data"])
    print(os.linesep.join(f"- {s}" for s in slugs))


def install(name: str):
    try:
        payload = api.search(slug=name)
    except requests.HTTPError as e:
        error(f"{e.status_code}: {e.reason}")

    if len(payload["data"]) == 0:
        error(f"Addon '{name}' not found.")
    elif len(payload["data"]) > 1:
        error(f"Found multiple addons with the name '{name}'.")

    addon = payload["data"][0]
    latest = _latest_file(addon)
    api.download(latest, target=const.ADDONS_DIR)

    print(f"Installed {name} [{latest['displayName']}]")


def uninstall(name: str):
    try:
        payload = api.search(slug=name)
    except requests.HTTPError as e:
        error(f"{e.status_code}: {e.reason}")

    if len(payload["data"]) == 0:
        error(f"Addon '{name}' not found.")
    elif len(payload["data"]) > 1:
        error(f"Found multiple addons with the name '{name}'.")

    addon = payload["data"][0]
    latest = _latest_file(addon)

    for module in latest["modules"]:
        shutil.rmtree(const.ADDONS_DIR / module["name"], ignore_errors=False)

    print(f"Uninstalled {name}")


def update(name: typing.Optional[str]):
    print("update", name)


def run():
    """\
    Rune.

    Usage:
        rune search <query>...
        rune install <name>
        rune uninstall <name>
        rune update [<name>]
        rune (-h | --help)
        rune --version

    Options:
        -h --help     Show this screen.
        --version     Show version.
    """
    arguments = docopt(run.__doc__, version="0.0.1")

    match arguments:
        case {"search": True}:
            search(arguments["<query>"])
        case {"install": True}:
            install(arguments["<name>"])
        case {"uninstall": True}:
            uninstall(arguments["<name>"])
        case {"update": True}:
            update(arguments["<name>"])
