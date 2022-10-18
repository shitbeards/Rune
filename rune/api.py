import os
import shutil
import typing
import pathlib
import zipfile
import tempfile
import urllib.parse

import requests

from rune import const


NONE = object()


def search(query=NONE, slug=NONE):
    params = {
        "gameId": const.WOW_GAME_ID,
        "searchFilter": query,
        "slug": slug,
    }
    response = requests.get(
        url=urllib.parse.urljoin(const.BASE_URL, "mods/search"),
        headers={"x-api-key": const.API_TOKEN},
        params={k: v for k, v in params.items() if v is not NONE},
        allow_redirects=True,
    )
    response.raise_for_status()
    return response.json()


def download(file: dict, target: typing.Union[str, bytes, os.PathLike]):
    url = file["downloadUrl"]
    _, name = os.path.split(url)
    target = pathlib.Path(target)

    with (
        tempfile.NamedTemporaryFile(suffix=name) as fp,
        requests.get(url, stream=True) as r,
    ):
        r.raise_for_status()
        shutil.copyfileobj(r.raw, fp)

        # cleanup previous install
        # TODO: should get modules of previously installed version.
        for module in file["modules"]:
            shutil.rmtree(
                path=target / module["name"],
                ignore_errors=True,
            )

        # unzip download to addons dir
        with zipfile.ZipFile(fp, "r") as zp:
            zp.extractall(target)
