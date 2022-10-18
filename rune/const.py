import os
import sys
import pathlib


MACOS = "macOS"
WINDOWS = "Windows"

BASE_URL = "https://api.curseforge.com/v1/"
API_TOKEN = os.environ["RUNE_API_KEY"]
WOW_GAME_ID = "1"
RETAIL_VERSION_ID = "517"

RELEASE = 1
BETA = 2
ALPHA = 3

if sys.platform == "darwin":
    PLATFORM = MACOS
    ADDONS_DIR = (
        pathlib.Path("Applications")
        / "World of Warcraft"
        / "_retail_"
        / "Interface"
        / "AddOns"
    )
else:
    PLATFORM = WINDOWS
    ADDONS_DIR = (
        pathlib.Path("C:\\")
        / "World of Warcraft"
        / "_retail_"
        / "Interface"
        / "AddOns"
    )

ADDONS_DIR = os.environ.get("RUNE_ADDONS_DIR", ADDONS_DIR)
ADDONS_DIR = pathlib.Path(ADDONS_DIR).expanduser().absolute()

APP_DATA = os.environ.get("RUNE_ADDONS_DIR", "~/.rune")
APP_DATA = pathlib.Path(APP_DATA).expanduser().absolute()
APP_DATA.mkdir(exist_ok=True)
