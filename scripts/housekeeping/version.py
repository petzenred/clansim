import os
import subprocess
import sys
from configparser import ConfigParser
from dataclasses import dataclass
from importlib.util import find_spec

from definitions import (
    # This is saved in the Clan save-file, and is used for save-file conversion.
    VERSION_CLANSIM_NUMBER, SAVE_CLANSIM_VERSION_NUMBER,
    VERSION_CLANGEN_NUMBER, SAVE_CLANGEN_VERSION_NUMBER
)
from platformdirs import user_data_dir

import logging
logger = logging.getLogger(__name__)


def get_version_info():
    if get_version_info.instance is None:
        is_source_build = False
        commit_id = VERSION_CLANSIM_NUMBER
        release_channel = False
        upstream = ""
        is_itch = False
        is_sandboxed = False
        is_thonny = False
        git_installed = False
        game_version = VERSION_CLANSIM_NUMBER
        save_version = SAVE_CLANSIM_VERSION_NUMBER

        # is this a source build
        if not getattr(sys, "frozen", False):
            is_source_build = True

        # TODO what is this indicating
        if find_spec("thonny") is not None:
            is_thonny = True

        # get the git commit ID, release channel, and TODO upstream?
        if os.path.exists("version.ini"):
            # check for version.ini and parse if present
            version_ini = ConfigParser()
            version_ini.read("version.ini", encoding="utf-8")
            commit_id = version_ini.get("DEFAULT", "version_number") # TODO change version_number to commit_id
            release_channel = version_ini.get("DEFAULT", "release_channel")
            upstream = version_ini.get("DEFAULT", "upstream")
        else:
            # if there's no version.ini, manually get the git commit ID instead
            try:
                commit_id = (
                    subprocess.check_output(["git", "rev-parse", "HEAD"])
                    .decode("ascii")
                    .strip()
                )
                git_installed = True
            except:
                logger.exception("Git CLI invocation failed")

        if (
            "--launched-through-itch" in sys.argv
            or "LAUNCHED_THROUGH_ITCH" in os.environ
        ):
            is_itch = True

        if "itch-player" in user_data_dir().lower():
            is_sandboxed = True

        get_version_info.instance = VersionInfo(
            is_source_build,
            release_channel,
            commit_id,
            upstream,
            is_itch,
            is_sandboxed,
            git_installed,
            is_thonny,
            game_version,
            save_version
        )
    return get_version_info.instance


get_version_info.instance = None


@dataclass
class VersionInfo:

    is_source_build: bool
    release_channel: str
    commit_id: str
    upstream: str
    is_itch: bool
    is_sandboxed: bool
    git_installed: bool
    is_thonny: bool
    game_version: tuple[int]
    save_version: int

    @property
    def is_dev(self) -> bool:
        if self.release_channel != "stable":
            return True
        else:
            return False
