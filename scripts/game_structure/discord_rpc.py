"""
This file is used to connect to Discord's Rich Presence API.
This allows the game to show up on your Discord profile.

Discord RPC is not required for the game to run.
If you do not have the pypresence module installed,
this file will not be used, and the game will run as normal.
"""

########################################################################################################################
# Imports
########################################################################################################################

import asyncio
import threading
from time import time

from definitions import ScreenName, CampKey
from scripts._red.config_manager import config
from scripts._red.screens.screen_manager import screen_manager
from scripts.game_structure.game_essentials import game

import logging
logger = logging.getLogger(__name__)


########################################################################################################################
# Constants
########################################################################################################################

status_dict = {
    ScreenName.MainMenu: "At the start screen",
    ScreenName.NewClan: "Making a Clan",
    ScreenName.Mediation: "Mediating a dispute",
    ScreenName.Patrol: "On a patrol",
    ScreenName.Profile: "Viewing a cat's profile",
    ScreenName.LeaderCeremony: "Remembering a ceremony",
    ScreenName.CatList: "Viewing the Clans",
    ScreenName.Allegiances: "Considering allegiances",
    # "starclan screen": "Viewing StarClan",
    # "dark forest screen": "Viewing the Dark Forest",
    ScreenName.HealerDen: "In the healer den",
    ScreenName.ScreenUnset: f"Leading {game.active_clan_token}Clan",
}


########################################################################################################################
# Classes
########################################################################################################################

class _DiscordRPC(threading.Thread):
    def __init__(self, client_id: str, daemon: bool):
        super().__init__(daemon=daemon)
        self._rpc = None
        self._client_id = client_id
        self._connected = False
        self._start_time = round(time() * 1000)
        self._rpc_supported = False
        self._event_loop = asyncio.new_event_loop()

        self.start_rpc = threading.Event()
        self.update_rpc = threading.Event()
        self.close_rpc = threading.Event()

    def run(self):
        self.start_rpc.wait()
        self.get_rpc()
        self.connect()
        while not self.close_rpc.is_set():
            self.update_rpc.wait()
            self.update()
        self.close()

    def get_rpc(self):
        # Check if pypresence is available.
        if not config.settings.Discord:
            return
        try:
            # raise ImportError # uncomment this line to disable rpc without uninstalling pypresence
            from pypresence import Presence, DiscordNotFound

            logger.debug("Discord RPC is supported")
        except ImportError:
            logger.warning("PyPresence not installed, Discord RPC isn't supported.")
            logger.warning("To enable RPC, run 'pip install pypresence' in your terminal.")
            return
        # Check if Discord is running.
        try:
            self._rpc = Presence(client_id=self._client_id, loop=self._event_loop)
            logger.debug("Discord found!")
        except DiscordNotFound:
            logger.debug("Discord not running.")
            return
        # Try to connect.
        try:
            self._rpc_supported = True
            self.connect()
            logger.info("Connected to discord!")
        except ConnectionError as e:
            logger.info(f"Failed to connect to Discord: {e}")

    def connect(self):
        if self._rpc_supported:
            try:
                self._rpc.connect()
            except BaseException as e:
                self._rpc_supported = False
                logger.info(f"Failed to connect to Discord: {e}")
                return
            self._connected = True
            self.update()

    def update(self):
        if self._connected:
            try:
                state_text = status_dict[screen_manager.curr_screen_name]
            except KeyError:
                state_text = "Leading the Clan"

            try:
                camp_key: CampKey = game.clan_obj.camp.camp_key
                img_str = camp_key.get_bg_path(season=game.current_season, theme=config.settings.Theme)
                img_text = game.clan_obj.biome
            except AttributeError:
                logger.warning("Failed to get image string, game may not be fully loaded yet. "
                      "Don't worry, it will fix itself. Hopefully.")
                img_str = "discord"  # fallback in case the game isn't loaded yet
                img_text = "ClanSim!!"

            # Example: beach_greenleaf_camp1_dark

            if game.clan_obj:
                clan_name = f"{game.active_clan_token}Clan"
                cats_amount = game.cat_tracker._last_id # FIXME do this in a way that doesn't access _last_id
                clan_age = game.current_moon
            else:
                clan_name = "Loading..."
                cats_amount = 0
                clan_age = 0
            try:
                self._rpc.update(
                    state=state_text,
                    details=f"Managing {clan_name} for {clan_age} moons",
                    large_image=img_str.lower(),
                    large_text=img_text,
                    small_image="discord",
                    small_text=f"{cats_amount} cats have lived in the Clans",
                    start=self._start_time,
                    buttons=[
                        {
                            "label": "Join The Server",
                            "url": "https://discord.gg/clangen",
                        }
                    ],
                )
            except BaseException:  # pylint: disable=broad-except
                logger.warning("Discord RPC had issue updating, disabling...")
                self._rpc_supported = False
                self._connected = False
                self._rpc = None
        self.update_rpc.clear()

    def close(self):
        if self._connected:
            self._rpc.close()
            self._connected = False
