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

# ------------------------------- DOWNLOAD UPDATES ------------------------------- #

# FIXME make sure this info gets saved in the logger too
if os.path.exists("auto-updated"):
    print("ClanSim starting, deleting auto-updated file")
    os.remove("auto-updated")
    shutil.rmtree("Downloads", ignore_errors=True)
    print("Update Complete!")
    print(f"New version: {get_version_info().commit_id}")

setup_data_dir()
timestr = time.strftime(definitions.TIMESTR_FORMAT)

# ----------------------------- SET ENVIRONMENT INFO ----------------------------- #

# if user is developing in a Github codespace
environment: definitions.Environment
version_msg: str = (f"\nClanSim Version: {get_version_info().game_version}\n"
                    f"Running on commit {get_version_info().commit_id}\n")
if os.environ.get("CODESPACES"):
    environment = definitions.Environment.Codespace
    web_vnc: str = (f"https://{os.environ.get('CODESPACE_NAME')}-6080"
                    f".{os.environ.get('GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN')}"
                    f"/?autoconnect=true&reconnect=true&password=clangen&resize=scale")
    version_msg += (
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
    version_msg += "Running on source code\n"
    if get_version_info().commit_id == "unknown":
        version_msg += (f"\n"
                        f"Failed to get git commit hash, using hardcoded version number instead.\n"
                        f"Hey testers! We recommend you use git to clone the repository, as it makes things easier "
                        f"for everyone.\n"
                        f"There are instructions at "
                        f"https://discord.com/channels/1003759225522110524/1054942461178421289/1078170877117616169\n")
else:
    environment = definitions.Environment.Executable
    version_msg += "Running on PyInstaller build\n"

# -------------------------------- LOGGING SETUP --------------------------------- #

import logging
from scripts._red.utils.logger_utils import logger_setup, LOGGER_LEVEL_DEFAULT

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

from scripts._red.game_structure.monkeypatch import translate

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

# from scripts.debug_console import debug_mode
debug_f: bool = False

########################################################################################################################
# pygame Setup
########################################################################################################################

# -------------------------------- PYGAME OBJECT --------------------------------- #

import pygame

# --------------------------------- GAME IMPORTS --------------------------------- #

# configuration manager setup
#   config needs to be initialized before the screen manager
from scripts._red.config_manager import config

# import/initialization of all screens is now handled by the screen manager initialization
from scripts._red.screens.screen_manager import screen_manager

# game object setup
from scripts.game_structure.game_essentials import game
from scripts._red.save_manager import SaveManager
save_manager: SaveManager = SaveManager()
game.initialize(save_manager=save_manager, screen_manager=screen_manager)

clock = pygame.time.Clock()
pygame.display.set_caption(definitions.APP_NAME_LONG)
pygame.display.set_icon(pygame.image.load("resources/images/icons/_icon_.png")) # FIXME hardcoded filepath

from scripts._red.sprite_manager import sprite_manager
from scripts.game_structure.audio import sound_manager, music_manager
from scripts._red.screens.windows import SaveCheck
# pylint: disable=redefined-builtin
# Add your imports here!

# ------------------------------- DISCORD PRESENCE ------------------------------- #

from scripts.game_structure.discord_rpc import _DiscordRPC
game.rpc = _DiscordRPC("1076277970060185701", daemon=True)
game.rpc.start()
game.rpc.start_rpc.set()

# TODO can I move the imports here?


########################################################################################################################
# Loading
########################################################################################################################

finished_loading_f = False

# -------------------------------- LOAD SAVE DATA -------------------------------- #

def load_data():
    global finished_loading_f

    from scripts._red.red_exceptions import InitializationError

    try:
        # TODO new loading
        # load in the spritesheets
        logger.debug(f"Loading all sprites...")
        sprite_manager.load_all_sprites()
        logger.debug(f"Finished loading sprites")

        # load the save file referred to by 'currentclan.txt', which is set when the game object's save_manager is set
        #   loads Clans, cats, relationships, events, and history
        logger.debug(f"Loading save data...")
        from scripts._red.io_manager import io_manager
        current_clan_prefix = io_manager.get_last_played_clan_token()
        game.switch_to_new_save(new_active_clan_prefix=current_clan_prefix)
        # game._load_active_clan_save_file()
        logger.debug(f"Finished loading save data")

        # rebuild screens and buttons
        logger.debug(f"Building UI...")
        screen_manager.rebuild_core()
        screen_manager.build_all_screens()
        logger.debug(f"Finished building UI")
    except Exception as err:
        logger.exception("Something went wrong while loading data", exc_info=err)
        game.quit(savesettings=False)

    # FIXME old loading
    # clan_list = game.read_clans()
    # if clan_list:
    #     game.switches["clan_list"] = clan_list
    #     try:
    #         load_cats()
    #         version_info = clan_class.load_clan()
    #         clangen_version_convert(version_info)
    #         game.load_events()
    #         scripts.screens.screens_core.screens_core.rebuild_core()
    #     except Exception as e:
    #         if not game.switches["error_message"]:
    #             game.switches[
    #                 "error_message"
    #             ] = "There was an error loading the cats file!"
    #             game.switches["traceback"] = e
    #         logging.exception("File failed to load", e)

    finished_loading_f = True

# ------------------------------- LOAD ANIMATIONS -------------------------------- #

def loading_animation(scale: float = 1):
    # global finished_loading_f

    # Load images, adjust color
    color = pygame.Surface((200 * scale, 210 * scale))
    color.fill(color=config.screen_config.themes[config.settings.Theme]["bg_colour"])

    images = []
    for i in range(1, 11):
        im = pygame.transform.scale_by(
            pygame.image.load(f"resources/images/loading_animate/startup/{i}.png"), # TODO hardcoded filepath
            screen_manager.window_scale,
        )
        im.blit(color, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        images.append(im)

    # Cleanup
    del im
    del color

    x = screen_manager.curr_surface_obj.get_width() / 2
    y = screen_manager.curr_surface_obj.get_height() / 2

    i = 0
    total_frames = len(images)

    # run the loading screen while the game data is loading
    while not finished_loading_f: # wait until the game data is finished loading
        clock.tick(8)  # Loading screen is 8FPS

        screen_manager.curr_surface_obj.fill(color=config.screen_config.themes[config.settings.Theme]["bg_colour"])

        screen_manager.curr_surface_obj.blit(
            images[i], (x - images[i].get_width() / 2, y - images[i].get_height() / 2)
        )

        i += 1
        if i >= total_frames:
            i = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit(savesettings=False)

        pygame.display.update()

# load the game data in another thread
loading_thread = threading.Thread(target=load_data)
loading_thread.start()

loading_animation(screen_manager.window_scale)

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
    logger.warning("Failed to initialize sound. Sound will be disabled.")
    music_manager.audio_disabled_f = True
    music_manager.muted_f = True

screen_manager.queue_screen_switch(new_screen_name=definitions.ScreenName.MainMenu)
screen_manager.run_screen_switch()

# screen_manager.all_screen_objs[definitions.ScreenName.MainMenu].screen_switches()
# screen_manager.curr_surface_obj # TODO can we get rid of this

# start main menu screen music here
# music_manager.check_music(screen_manager.curr_screen_name) # TODO this shouldn't be needed anymore

# TODO move cursor stuff to screen_manager.rebuild_core()? (1/2)
cursor_img = pygame.image.load("resources/images/paw_cursor.png").convert_alpha()
cursor = pygame.cursors.Cursor((9, 0), cursor_img)
disabled_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)


########################################################################################################################
# Run the game
########################################################################################################################

try:
    while True:
        time_delta_ms = clock.tick(game.fps) / 1000.0

        # TODO move cursor stuff to screen_manager.rebuild_core()? (2/2)
        if config.settings.UsePawCursor:
            if pygame.mouse.get_cursor() == disabled_cursor:
                pygame.mouse.set_cursor(cursor)
        elif pygame.mouse.get_cursor() == cursor:
            pygame.mouse.set_cursor(disabled_cursor)

        # Draw screens
        # This occurs before events are handled to stop pygame_gui buttons from blinking.
        # game.all_screens[game.current_screen_obj].on_use() # FIXME
        screen_manager.all_screen_objs[screen_manager.curr_screen_name].on_use()

        # EVENTS
        for event in pygame.event.get():
            # TODO fix debug mode
            #   logger_utils.logger_change_level(_logging_level)
            # if (
            #     event.type == pygame.KEYDOWN
            #     and config.settings.UseKeybinds
            #     and debug_mode.debug_menu.visible
            # ):
            #     pass
            # else:
            #     game.all_screens[game.current_screen_obj].handle_event(event)
            #     if event.type in (pygame_gui.UI_BUTTON_START_PRESS, pygame_gui.UI_BUTTON_ON_HOVERED):
            #         sound_manager.handle_sound_events(event)

            # RedBaseScreen object handles the event
            screen_manager.all_screen_objs[screen_manager.curr_screen_name].handle_event(event)
            # game.all_screens[game.current_screen_obj].handle_event(event) # FIXME

            # sound happens
            if event.type in (pygame_gui.UI_BUTTON_START_PRESS, pygame_gui.UI_BUTTON_ON_HOVERED):
                sound_manager.handle_sound_events(event)

            # if the player is trying to quit the game, check the player has saved first unless
            #   they're on the start screen or there's no active Clan to save
            if event.type == pygame.QUIT:
                if (
                        screen_manager.curr_screen_name.category in (
                        definitions.ScreenCategory.MainMenu, definitions.ScreenCategory.Creation
                        )
                ):
                    game.quit(savesettings=False)
                else:
                    SaveCheck(is_main_menu=False, mm_btn=None)

            # MOUSE CLICK
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.clicked = True

                # TODO fix debug mode
                # if ui_manager.visual_debug_active: # TODO 'visual debug' should be 'console debug'
                #     _ = pygame.mouse.get_pos()
                #     if config.settings.Fullscreen:
                #         logger.info(f"(x: {_[0]}, y: {_[1]})")
                #     else:
                #         logger.info(f"(x: {_[0] * screen_manager.window_scale}, y: {_[1] * screen_manager.window_scale})")
                #     del _

            # F2 toggles visual debug mode for pygame_gui, allowed for easier bug fixes.
            # F3 opens the debugging console
            # F11 toggles fullscreen mode
            # TODO fix debug mode - logger level DEBUG
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    screen_manager.toggle_fullscreen()
                elif event.key == pygame.K_F2:
                    # ui_manager.logger.info_layer_debug() # TODO logger level DEBUG
                    if debug_f:
                        debug_f = False
                    else:
                        debug_f = True
                    logger_setup(debug_mode_f=debug_f)
                elif event.key == pygame.K_F3:
                    # debug_mode.toggle_debug_mode() # TODO logger level DEBUG
                    # debugmode.toggle_console()
                    raise NotImplementedError(f"debugging console not yet implemented")

            screen_manager.uim.process_events(event)

        screen_manager.uim.update(time_delta_ms)

        # update FIXME
        game.update_game()
        # FIXME - make sure game.switch_screens is replaced with screen_manager.switch_screens_f everywhere
        if screen_manager.switch_screens_f:
            screen_manager.run_screen_switch()
        if (
            not music_manager.audio_disabled_f
            and not pygame.mixer.music.get_busy()
            and not music_manager.muted_f
        ):
            music_manager.external_music_start()

        # debug_mode.pre_update(clock)
        # END FRAME

        screen_manager.uim.draw_ui(screen_manager.curr_surface_obj)

        # debug_mode.post_update(screen)

        pygame.display.update()
except Exception as err:
    logger.exception(f"There was an error running ClanSim.", exc_info=err)
    logger.error(f"The game will now close to prevent the game hanging")
