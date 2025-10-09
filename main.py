#!/usr/bin/env python3


# pylint: disable=line-too-long
"""



This file is the main file for the game.
It also contains the main pygame loop.
It first sets up logging, then loads the version hash from version.ini (if it exists), then loads the cats and clan.
It then loads the settings, and then loads the start screen.




"""  # pylint: enable=line-too-long
# DO NOT ADD YOUR IMPORTS HERE.
# Scroll down to the "Add your imports here!" comment and add them there.
# Side effects of imports WILL BREAK crucial setup logic for logging and init
import os
import shutil
import sys
import threading
import time
from importlib import reload
from importlib.util import find_spec



########################################################################################################################
# Pre-game setup
########################################################################################################################

# ---------------------------- CHECK REQUIRED MODULES ---------------------------- #

if not getattr(sys, "frozen", False):
    requiredModules = [
        "ujson",
        "pygame",
        "pygame_gui",
        "platformdirs",
        "pgpy",
        "requests",
        "strenum",
    ]

    isMissing = False

    for module in requiredModules:
        if find_spec(module) is None:
            isMissing = True
            break

    if isMissing:
        print("""
        You are missing some requirements to run ClanSim!
                
        Please look at the "README.md" file for instructions on how to install them.
        """)

        sys.exit(1)

    del requiredModules
    del isMissing
del find_spec

import definitions
from scripts.housekeeping.datadir import setup_data_dir
from scripts.housekeeping.version import get_version_info

try:
    directory = os.path.dirname(__file__)
except NameError:
    directory = os.getcwd()
if directory:
    os.chdir(directory)

# ------------------------------------ UPDATE ------------------------------------ #
# check for downloaded updates

# FIXME make sure this info gets saved in the logger too
if os.path.exists("auto-updated"):
    print("ClanSim starting, deleting auto-updated file")
    os.remove("auto-updated")
    shutil.rmtree("Downloads", ignore_errors=True)
    print("Update Complete!")
    print(f"New version: {get_version_info().version_number}")

setup_data_dir()
timestr = time.strftime(definitions.TIMESTR_FORMAT)

# ------------------------------- SET VERSION INFO ------------------------------- #

# if user is developing in a Github codespace
# TODO potentially replace Environment with a debug flag
environment: definitions.Environment
version_msg: str
if os.environ.get("CODESPACES"):
    environment = definitions.Environment.Codespace
    web_vnc: str = (f"https://{os.environ.get('CODESPACE_NAME')}-6080"
                    f".{os.environ.get('GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN')}"
                    f"/?autoconnect=true&reconnect=true&password=clangen&resize=scale")
    version_msg = (
        f"\n"
        f"Running in Github codespace\n"
        f"Sorry, but sound *may* not work :(\n"
        f"SDL_AUDIODRIVER is dsl. This is to avoid ALSA errors, but it may disable sound.\n"
        f"Web VNC:\n"
        f"{web_vnc}\n"
        f"(use ClanSim in fullscreen mode for best results)\n"
    )
# FIXME can you be running the source code from Github Codespaces? If not, change to elif
if get_version_info().is_source_build:
    environment = definitions.Environment.SourceCode
    version_msg = "Running on source code\n"
    if get_version_info().version_number == definitions.VERSION_CLANSIM_NUMBER:
        version_msg += (f"\n"
                        f"Failed to get git commit hash, using hardcoded version number instead.\n"
                        f"Hey testers! We recommend you use git to clone the repository, as it makes things easier "
                        f"for everyone.\n"
                        f"There are instructions at "
                        f"https://discord.com/channels/1003759225522110524/1054942461178421289/1078170877117616169\n")
else:
    environment = definitions.Environment.Executable
    version_msg = "Running on PyInstaller build\n"

version_msg += (f"\nVersion Name: {definitions.VERSION_CLANSIM_NUMBER}\n"
                f"Running on commit {get_version_info().version_number}\n")

# -------------------------------- LOGGING SETUP --------------------------------- #

import logging
from utils.logger_utils import logger_setup

# use the version info to establish what level of message the log should show -
#   to include debugging messages or not to include debugging messages?
logger_setup(environment.log_level)
logger = logging.getLogger(__name__)

# print the version message
logger.info(version_msg)

########################################################################################################################
# Game setup
########################################################################################################################

# ------------------------------ PYGAME GUI MANAGER ------------------------------ #
# this needs to happen before screens are initialized

import pygame_gui

# ------------------------ LANGUAGE AND TRANSLATION SETUP ------------------------ #
# replace pygame's translate module with a custom one

from scripts.game_structure.monkeypatch import translate

# MONKEYPATCH

pygame_gui.core.utility.translate = translate
for module_name, module in list(sys.modules.items()):
    if module and hasattr(module, "translate"):  # Check for the attribute
        if module.translate is pygame_gui.core.utility.translate:  # Ensure it's the original reference
            setattr(module, "translate", translate)
            break

# ----------------------------- LOAD PYGAME MODULES ------------------------------ #

for module_name, module in list(sys.modules.items()):
    if module_name.startswith(f"pygame_gui."):
        if (
            not module_name.endswith("utility")
            and not module_name.endswith("container_interface")
            and not module_name.endswith("_constants")
            and not module_name.endswith("layered_gui_group")
            and not module_name.endswith("object_id")
        ):
            # Reload the module
            reload(module)

# --------------------------- CHECK AND SET DEBUG MODE --------------------------- #

# from scripts.debug_menu import debugmode
# FIXME turn this into debug for logger
from scripts.debug_console import debug_mode

########################################################################################################################
# pygame Setup
########################################################################################################################

# -------------------------------- PYGAME OBJECT --------------------------------- #

import pygame

from scripts._red.config_manager import config
from scripts.game_structure.game_essentials import game
from scripts._red.save_manager import SaveManager
save_manager: SaveManager = SaveManager()

# configuration manager setup
config.assign_save_manager(save_manager=save_manager, currentclan=)
config.read_game_settings_file()

# game object setup
game.assign_save_manager(save_manager=save_manager, currentclan=True)  # TODO when will autoload not be true?
pygame.display.set_caption(definitions.APP_NAME_LONG)

# --------------------------------- GAME IMPORTS --------------------------------- #

from scripts.cat.sprites import sprites
from scripts.clan import clan_class

from conversion.conversion_manager import update_clansim_save
from scripts._red.save_manager import load_cats, clangen_version_convert
from scripts.game_structure.audio import sound_manager, music_manager
from scripts.game_structure.windows import SaveCheck
from scripts.utility import (
    quit,
)  # pylint: disable=redefined-builtin
# Add your imports here!

# import all screens for initialization (must be done after pygame_gui manager is created)
from scripts.game_structure.screen_settings import screen_scale, MANAGER, screen, toggle_fullscreen
toggle_fullscreen(
    fullscreen=config.Fullscreen,
    show_confirm_dialog=False,
    ingame_switch=False,
)
from scripts.screens.all_screens import AllScreens
import scripts.game_structure.screen_settings
clock = pygame.time.Clock()
pygame.display.set_icon(pygame.image.load("resources/images/icons/_icon_.png"))

# ------------------------------- DISCORD PRESENCE ------------------------------- #

from scripts.game_structure.discord_rpc import _DiscordRPC
game.rpc = _DiscordRPC("1076277970060185701", daemon=True)
game.rpc.start()
game.rpc.start_rpc.set()

# TODO can I move the imports here?

# --------------------------- LOAD SAVE AND ANIMATIONS --------------------------- #

finished_loading_f = False

def load_data():
    global finished_loading_f

    # TODO new loading

    # TODO handle what happens if any of the save files are malformed
    # TODO create a custom MalformedSaveError to catch here to make that easier

    # load in the spritesheets
    sprites.load_all()

    # if possible, load the save referred to in "currentclan.txt"
    # loads Clans, cats, relationships, events, and history
    game.load_active_clan_save_file()

    # TODO update ClanSim saves from older versions
    # ClanGen save files can be converted to ClanSim files from the game's main menu
    update_clansim_save(old_version)

    # TODO rebuild screens core

    # TODO old loading
    clan_list = game.read_clans()
    if clan_list:
        game.switches["clan_list"] = clan_list
        try:
            load_cats()
            version_info = clan_class.load_clan()
            clangen_version_convert(version_info)
            game.load_events()
            scripts.screens.screens_core.screens_core.rebuild_core()
        except Exception as e:
            if not game.switches["error_message"]:
                game.switches[
                    "error_message"
                ] = "There was an error loading the cats file!"
                game.switches["traceback"] = e
            logging.exception("File failed to load", e)

    finished_loading_f = True


def loading_animation(scale: float = 1):
    global finished_loading_f

    # Load images, adjust color
    color = pygame.Surface((200 * scale, 210 * scale))
    if config.settings.DarkMode:
        color.fill(config.get_config_value("theme")["dark_mode_background"])
    else:
        color.fill(config.get_config_value("theme")["light_mode_background"])

    images = []
    for i in range(1, 11):
        im = pygame.transform.scale_by(
            pygame.image.load(f"resources/images/loading_animate/startup/{i}.png"),
            screen_scale,
        )
        im.blit(color, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        images.append(im)

    # Cleanup
    del im
    del color

    x = screen.get_width() / 2
    y = screen.get_height() / 2

    i = 0
    total_frames = len(images)
    while not finished_loading_f: # wait until the game data is finished loading
        clock.tick(8)  # Loading screen is 8FPS

        if config.settings.DarkMode:
            screen.fill(config.get_config_value("theme")["dark_mode_background"])
        else:
            screen.fill(config.get_config_value("theme")["light_mode_background"])

        screen.blit(
            images[i], (x - images[i].get_width() / 2, y - images[i].get_height() / 2)
        )

        i += 1
        if i >= total_frames:
            i = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit(savesettings=False)

        pygame.display.update()

# load the game data in another thread
loading_thread = threading.Thread(target=load_data)
loading_thread.start()

loading_animation(screen_scale)

# The loading thread should be done by now. This line
# is just for safety. Plus some cleanup.
loading_thread.join()
del loading_thread
del finished_loading_f
del loading_animation
del load_data

# ----------------------------- LOAD SOUND AND MUSIC ----------------------------- #

pygame.mixer.pre_init(buffer=44100)
try:
    pygame.mixer.init()
except pygame.error:
    logger.info("Failed to initialize sound. Sound will be disabled.")
    music_manager.audio_disabled_f = True
    music_manager.muted_f = True
AllScreens.main_menu_screen.screen_switches()
# start main menu screen music here
music_manager.check_music(definitions.ScreenName.MainMenu)

# dev screen info now lives in scripts/screens/screens_core

cursor_img = pygame.image.load("resources/images/paw_cursor.png").convert_alpha()
cursor = pygame.cursors.Cursor((9, 0), cursor_img)
disabled_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)

while True:
    time_delta = clock.tick(game.switches["fps"]) / 1000.0

    if config.settings.UsePawCursor:
        if pygame.mouse.get_cursor() == disabled_cursor:
            pygame.mouse.set_cursor(cursor)
    elif pygame.mouse.get_cursor() == cursor:
        pygame.mouse.set_cursor(disabled_cursor)
    # Draw screens
    # This occurs before events are handled to stop pygame_gui buttons from blinking.
    game.all_screens[game.current_screen].on_use()
    # EVENTS
    for event in pygame.event.get():
        if (
            event.type == pygame.KEYDOWN
            and config.settings.UseKeybinds
            and debug_mode.debug_menu.visible
        ):
            pass
        else:
            game.all_screens[game.current_screen].handle_event(event)
            if event.type in (pygame_gui.UI_BUTTON_START_PRESS, pygame_gui.UI_BUTTON_ON_HOVERED):
                sound_manager.handle_sound_events(event)

        if event.type == pygame.QUIT:
            # Don't display if on the start screen or there is no clan.
            if (
                game.switches["cur_screen"]
                in [
                    definitions.MAIN_MENU_SCREEN_NAME,
                    definitions.SWITCH_CLAN_SCREEN_NAME,
                    definitions.MAIN_SETTINGS_SCREEN_NAME,
                    definitions.NEW_CLAN_SCREEN_NAME,
                ]
                or not game.clan_obj
            ):
                quit(savesettings=False)
            else:
                SaveCheck(game.switches["cur_screen"], False, None)

        # MOUSE CLICK
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.clicked = True

            if MANAGER.visual_debug_active: # TODO 'visual debug' should be 'console debug'
                _ = pygame.mouse.get_pos()
                if config.settings.Fullscreen:
                    logger.info(f"(x: {_[0]}, y: {_[1]})")
                else:
                    logger.info(f"(x: {_[0] * screen_scale}, y: {_[1] * screen_scale})")
                del _

        # F2 toggles visual debug mode for pygame_gui, allowed for easier bug fixes.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F2:
                MANAGER.logger.info_layer_debug()
            elif event.key == pygame.K_F3:
                debug_mode.toggle_debug_mode()
                # debugmode.toggle_console()
            elif event.key == pygame.K_F11:
                scripts.game_structure.screen_settings.toggle_fullscreen(
                    source_screen=getattr(
                        AllScreens, game.switches["cur_screen"].replace(" ", "_")
                    ),
                    show_confirm_dialog=False,
                )

        MANAGER.process_events(event)

    MANAGER.update(time_delta)

    # update
    game.update_game()
    if game.switch_screens:
        game.all_screens[game.last_screen_forupdate].exit_screen()
        game.all_screens[game.current_screen].screen_switches()
        game.switch_screens = False
    if (
        not music_manager.audio_disabled_f
        and not pygame.mixer.music.get_busy()
        and not music_manager.muted_f
    ):
        music_manager.external_music_start()

    debug_mode.pre_update(clock)
    # END FRAME

    MANAGER.draw_ui(screen)

    debug_mode.post_update(screen)

    pygame.display.update()
