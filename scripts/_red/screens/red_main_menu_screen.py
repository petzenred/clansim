# pylint: disable=line-too-long
"""

This file contains:
  The start screen,
  The switch clan screen,
  The settings screen,
  And the statistics screen.



"""  # pylint: enable=line-too-long

# -------------------------------------------------------------------------------- #
# ----------------------------------------

########################################################################################################################
# Imports
########################################################################################################################

import os
import platform
import subprocess
import traceback
from html import escape

import pygame
import pygame_gui
from pygame.surface import Surface
from pygame_gui.core import ObjectID
from requests.exceptions import RequestException, Timeout

from definitions import (
    ButtonStyle,
    ScreenName, ScreenBackground, ThemeName, SwitchScreenButtonName
)
from scripts._red.config_manager import config
from scripts.game_structure import image_cache
from scripts.game_structure.game_essentials import game

import resources._red.red_filepaths as fp
from scripts._red.io_manager import io_manager
# from scripts.cat.cats import Cat
#from scripts._red.cats.red_cat import RedCat
# from scripts.utility import ui_scale, quit, ui_scale_dimensions
from scripts._red.utils.ui_utils import ui_scale, ui_scale_dimensions
from scripts._red.screens.screen_manager import screen_manager
# from scripts.screens.BaseScreen import BaseScreen
from scripts._red.screens.red_base_screen import RedBaseScreen

from scripts.ui.ui_elements import UIImageButton, UISurfaceImageButton
from scripts._red.screens.windows import UpdateAvailablePopup, ChangelogPopup
from scripts.housekeeping.datadir import get_data_dir, get_cache_dir
from scripts.housekeeping.update import has_update, UpdateChannel, get_latest_version_number
from scripts.housekeeping.version import get_version_info
from scripts.ui.generate_button import get_button_dict


########################################################################################################################
# Constants and Paths
########################################################################################################################

VERSION_UPSTREAM: str = "petzenred/clansim" # "ClanGenOfficial/clangen"

has_checked_for_update = False
update_available = False

import logging
logger = logging.getLogger(__name__)


class MainMenuScreen(RedBaseScreen):
    """ The class for the main screen that shows when the game is started. """

    name = ScreenName.MainMenu

    warning_label: pygame_gui.elements.UITextBox = None
    screen_buttons: dict[str, pygame_gui.elements.UIButton] = {}
    error_popup: dict = {} # error_text_box, error_label, closebtn, open_data_directory_button, error_gethelp
    update_popup: dict = {}

    error_open_f: bool = False
    checked_for_update_f: bool = False
    update_available_f: bool = False

    discord_target: str = "https://discord.gg/clangen" # FIXME don't have people ask ClanGen about ClanSim problems
    tumblr_target: str = "https://officialclangen.tumblr.com/"
    twitter_target: str = "https://twitter.com/OfficialClangen"

    def __init__(self):
        super().__init__(self.name)

    def handle_event(self, event):
        """ This is where events that occur on this page are handled.

        For the pygame_gui rewrite, button presses are also handled here.
        """
        platform_system: str = platform.system()

        if event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
            io_manager.open_external_link(link_target=event.link_target)
            return

        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            self.mute_button_pressed(event)

            # connections are screens the current screen can go to, and the buttons that send the user to those screens
            connections = {
                self.screen_buttons[SwitchScreenButtonName.GoScreenContinue]: \
                    screen_manager.menu_buttons[SwitchScreenButtonName.GoScreenCamp],
                self.screen_buttons[SwitchScreenButtonName.GoScreenSwitchClan]: \
                    screen_manager.menu_buttons[SwitchScreenButtonName.GoScreenSwitchClan],
                self.screen_buttons[SwitchScreenButtonName.GoScreenNewClan]: \
                    screen_manager.menu_buttons[SwitchScreenButtonName.GoScreenNewClan],
                self.screen_buttons[SwitchScreenButtonName.GoScreenGameSettings]: \
                    screen_manager.menu_buttons[SwitchScreenButtonName.GoScreenGameSettings],
                # TODO add a 'convert save' button
            }

            # handle being sent to a different screen
            if event.ui_element in connections and not self.error_open_f:
                # self.change_screen(connections[event.ui_element])
                screen_manager.queue_screen_switch(new_screen_name=event.ui_element.go_to_screen_name)

            # handle the data directory being opened
            elif event.ui_element == self.error_popup["open_data_directory_button"]:
                io_manager.open_system_link(system_link=get_data_dir())
                return

            # handle the game being closed
            elif event.ui_element == self.error_popup["closebtn"]:
                for btn in self.error_popup:
                    self.error_popup[btn].kill()
                self.error_open_f = False
                # game.switches['error_message'] = ''
                # game.switches['traceback'] = ''
            elif event.ui_element == self.screen_buttons["quit"]:
                game.quit(savesettings=False, clearevents=False)

            # handle the game being updated
            elif event.ui_element == self.update_popup["update_button"]:
                UpdateAvailablePopup() # FIXME make the UpdateAvailablePopup() works

            # handle social buttons being pressed
            elif event.ui_element == self.screen_buttons["discord_button"]:
                io_manager.open_external_link(link_target=self.discord_target)
            elif event.ui_element == self.screen_buttons["tumblr_button"]:
                io_manager.open_external_link(link_target=self.tumblr_target)
            elif event.ui_element == self.screen_buttons["twitter_button"]:
                io_manager.open_external_link(link_target=self.twitter_target)

        # handle keyboard navigation (instead of mouse navigation)
        elif event.type == pygame.KEYDOWN and config.settings.UseKeybinds:
            if (
                event.key == pygame.K_RETURN or event.key == pygame.K_SPACE
            ) and self.screen_buttons[SwitchScreenButtonName.GoScreenContinue].is_enabled:
                screen_manager.queue_screen_change(ScreenName.Camp)

        return

    def on_use(self):
        """ This is called on every frame of the game. """
        super().on_use()

    def _create_screen_buttons(self):
        """ Create buttons used by the main menu screen (and no other screens). """
        logger.debug("MainMenuScreen._create_screen_buttons")
        self.screen_buttons[SwitchScreenButtonName.GoScreenContinue] = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(pygame.Rect((70, 310), (200, 30)), scale=screen_manager.window_scale),
            text="buttons.continue",
            image_dict=get_button_dict(
                style=ButtonStyle.MainMenu,
                unscaled_dimensions=(200, 30),
                scale=screen_manager.window_scale),
            object_id="@ButtonStyle_mainmenu",
            manager=screen_manager.uim)
        self.screen_buttons[SwitchScreenButtonName.GoScreenSwitchClan] = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(pygame.Rect((70, 15), (200, 30)), scale=screen_manager.window_scale),
            text="buttons.switch_clan",
            image_dict=get_button_dict(
                style=ButtonStyle.MainMenu,
                unscaled_dimensions=(200, 30),
                scale=screen_manager.window_scale),
            object_id="@ButtonStyle_mainmenu",
            manager=screen_manager.uim,
            anchors={"top_target": self.screen_buttons[SwitchScreenButtonName.GoScreenContinue]})
        self.screen_buttons[SwitchScreenButtonName.GoScreenNewClan] = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(pygame.Rect((70, 15), (200, 30)), scale=screen_manager.window_scale),
            text="buttons.new_clan",
            image_dict=get_button_dict(
                style=ButtonStyle.MainMenu,
                unscaled_dimensions=(200, 30),
                scale=screen_manager.window_scale),
            object_id="@ButtonStyle_mainmenu",
            manager=screen_manager.uim,
            anchors={"top_target": self.screen_buttons[SwitchScreenButtonName.GoScreenSwitchClan]})
        self.screen_buttons[SwitchScreenButtonName.GoScreenGameSettings] = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(pygame.Rect((70, 15), (200, 30)), scale=screen_manager.window_scale),
            text="buttons.settings_info",
            image_dict=get_button_dict(
                style=ButtonStyle.MainMenu,
                unscaled_dimensions=(200, 30),
                scale=screen_manager.window_scale),
            object_id="@ButtonStyle_mainmenu",
            manager=screen_manager.uim,
            anchors={"top_target": self.screen_buttons[SwitchScreenButtonName.GoScreenNewClan]})
        self.screen_buttons["quit"] = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(pygame.Rect((70, 15), (200, 30)), scale=screen_manager.window_scale),
            text="buttons.quit",
            image_dict=get_button_dict(
                style=ButtonStyle.MainMenu,
                unscaled_dimensions=(200, 30),
                scale=screen_manager.window_scale),
            object_id="@ButtonStyle_mainmenu",
            manager=screen_manager.uim,
            anchors={"top_target": self.screen_buttons[SwitchScreenButtonName.GoScreenGameSettings]})

        # buttons to go to ClanGen's social media
        self.screen_buttons["twitter_button"] = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(pygame.Rect((12, 647), (40, 40)), scale=screen_manager.window_scale),
            text="",
            object_id="#twitter_button",
            manager=screen_manager.uim,
            tool_tip_text="screens.main_menu.tooltip_twitter")
        self.screen_buttons["tumblr_button"] = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(pygame.Rect((5, 647), (40, 40)), scale=screen_manager.window_scale),
            text="",
            object_id="#tumblr_button",
            manager=screen_manager.uim,
            tool_tip_text="screens.main_menu.tooltip_tumblr",
            anchors={"left_target": self.screen_buttons["twitter_button"]})
        self.screen_buttons["discord_button"] = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(pygame.Rect((7, 647), (40, 40)), scale=screen_manager.window_scale),
            text="",
            object_id="#discord_button",
            manager=screen_manager.uim,
            tool_tip_text="screens.main_menu.tooltip_discord",
            anchors={"left_target": self.screen_buttons["tumblr_button"]})

        return

    def _error_interrupt(self):
        error_img: Surface = image_cache.load_image(fp.ERROR_MSG).convert_alpha()

        self.error_popup["error_text_box"] = pygame_gui.elements.UIImage(
            relative_rect=ui_scale(pygame.Rect((130, 150), (590, 400)), scale=screen_manager.window_scale),
            image_surface=pygame.transform.scale(error_img, ui_scale_dimensions((590, 400))),
            manager=screen_manager.uim)
        self.error_popup["error_text_box"].disable()

        self.error_popup["error_label"] = pygame_gui.elements.UITextBox(
            html_text="",
            relative_rect=ui_scale(pygame.Rect((137, 185), (385, 360)), scale=screen_manager.window_scale),
            object_id="#text_box_22_horizleft",
            starting_height=1,
            manager=screen_manager.uim)

        # FIXME don't have people ask for help on the ClanGen discord for ClanSim
        self.error_popup["error_gethelp"] = pygame_gui.elements.UITextBox(
            "screens.main_menu.error_gethelp",  # pylint: disable=line-too-long
            relative_rect=ui_scale(pygame.Rect((527, 215), (175, 300)), scale=screen_manager.window_scale),
            object_id="#text_box_22_horizleft",
            starting_height=3,
            manager=screen_manager.uim)

        self.error_popup["open_data_directory_button"] = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(pygame.Rect((527, 511), (178, 30)), scale=screen_manager.window_scale),
            text="buttons.open_data_directory",
            image_dict=get_button_dict(ButtonStyle.SquOval, (178, 30), scale=screen_manager.window_scale),
            object_id="@ButtonStyle_squoval",
            manager=screen_manager.uim,
            starting_height=2,  # Layer 2 and repositioned so hover affect works.
            tool_tip_text="Opens the data directory.\nThis is where save files \nand logs are stored.")

        self.error_popup["closebtn"] = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(pygame.Rect((693, 215), (22, 22)), scale=screen_manager.window_scale),
            text="",
            starting_height=2,  # Hover affect works, and now allows it to be clicked more easily.
            object_id="#exit_window_button",
            manager=screen_manager.uim)

        for btn in self.error_popup:
            self.error_popup[btn].show()

        return

    def enter_screen(self):
        """ Called by the screen manager when the game switches TO this screen. """
        super().enter_screen()
        logger.debug(f"MainMenuScreen.enter_screen") # this is meant to be below super().enter_screen()

        # FIXME detect error from game
        error_FIXME: bool = False
        if error_FIXME:
            self._error_interrupt()

        # check for updates
        self.update_popup["update_button"] = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(pygame.Rect((577, 25), (153, 30)), scale=screen_manager.window_scale),
            text="buttons.update_available",
            image_dict=get_button_dict(
                style=ButtonStyle.SquOval,
                unscaled_dimensions=(153, 30),
                scale=screen_manager.window_scale),
            object_id="@ButtonStyle_squoval",
            manager=screen_manager.uim)
        self.update_popup["update_button"].visible = False

        self._check_for_updates()
        self._show_changelog()

        # create the content warning at the bottom of the screen
        self.warning_label = pygame_gui.elements.UITextBox(
            html_text="screens.main_menu.content_warning",
            relative_rect=ui_scale(pygame.Rect((0, 600), (800, 40)), scale=screen_manager.window_scale),
            object_id=ObjectID("#text_box_30_horizcenter", "#dark"),
            manager=screen_manager.uim,
            anchors={"left": "left", "right": "right"})
        self.warning_label.text_horiz_alignment = "center"
        self.warning_label.rebuild()

        # enable and disable the continue and switch buttons
        if game.active_clan_token is not None and not game.error_msg:
            self.screen_buttons[SwitchScreenButtonName.GoScreenContinue].enable()
        else:
            self.screen_buttons[SwitchScreenButtonName.GoScreenContinue].disable()

        valid_saves, invalid_saves = game.get_valid_invalid_saves()
        if (len(valid_saves) + len(invalid_saves)) > 1:
            self.screen_buttons[SwitchScreenButtonName.GoScreenSwitchClan].enable()
        else:
            self.screen_buttons[SwitchScreenButtonName.GoScreenSwitchClan].disable()

        # check for error and show the error popup if there are any
        # FIXME detect error from game again
        if error_FIXME:
            self._error_interrupt()
        # the old stuff \/
        if game.error_msg:
            error_text = "screens.main_menu.error_text"
            traceback_text = ""
            if game.error_trace:
                logger.error(game.error_trace)
                traceback_text = "<br><br>" + escape(
                    "".join(
                        traceback.format_exception(
                            game.error_trace,
                            game.error_trace,
                            game.error_trace.__traceback__,
                        )
                    )
                )  # pylint: disable=line-too-long
            self.error_popup["error_label"].set_text(
                error_text,
                text_kwargs={
                    "error": str(game.error_msg),
                    "traceback": traceback_text,
                },
            )
            self.error_popup["error_text_box"].show()
            self.error_popup["error_label"].show()
            self.error_popup["error_gethelp"].show()
            self.error_popup["open_data_directory_button"].show()

            if get_version_info().is_sandboxed:
                self.error_popup["open_data_directory_button"].hide()

            self.error_popup["closebtn"].show()

            self.error_open_f = True

        return

    def exit_screen(self):
        """ Called by the screen manager when the game switches AWAY FROM this screen."""
        super().exit_screen()
        logger.debug(f"MainMenuScreen.exit_screen") # this is meant to be below the call to super()
        # Button murder time.
        for btn in self.screen_buttons:
            self.screen_buttons[btn].kill()
        for btn in self.error_popup:
            self.error_popup[btn].kill()
        for btn in self.update_popup:
            self.update_popup[btn].kill()
        return

    def _check_for_updates(self):
        """ Checks if there are any updates available. """
        logger.debug(f"MainMenuScreen._check_for_updates")
        try:
            if (
                not get_version_info().is_source_build
                and not get_version_info().is_itch
                and get_version_info().upstream.lower() == VERSION_UPSTREAM.lower()
                and config.settings.AutoUpdate
                and not self.checked_for_update_f
            ):
                if has_update(UpdateChannel(get_version_info().release_channel)):
                    self.update_available_f = True
                    show_popup = True
                    if os.path.exists(fp.SUPRESS_UPDATE_POPUP):
                        # FIXME use io_manager here
                        with open(
                            file=fp.SUPRESS_UPDATE_POPUP,
                            mode="r",
                            encoding="utf-8",
                        ) as read_file:
                            if read_file.readline() == get_latest_version_number():
                                show_popup = False

                    if show_popup:
                        UpdateAvailablePopup(show_checkbox=True)

                self.checked_for_update_f = True

            if self.update_available_f:
                self.update_popup["update_button"].visible = True
        except (RequestException, Timeout):
            logger.exception("Failed to check for update")
            self.checked_for_update_f = True

        return

    def _show_changelog(self):
        """ Show the changelog popup window if the game has been updated. """
        logger.debug(f"MainMenuScreen._show_changelog")
        if config.settings.ShowChangelogOnUpdate:
            show_changelog = True
            last_commit: str = "0000000000000000000000000000000000000000"
            if os.path.exists(fp.CHANGELOG_POPUP_SHOWN):
                # FIXME use io_manager here
                with open(
                    fp.CHANGELOG_POPUP_SHOWN, encoding="utf-8"
                ) as read_file:
                    last_commit = read_file.readline()
                    if last_commit == get_version_info().commit_id:
                        show_changelog = False

            if show_changelog:
                ChangelogPopup()
                # FIXME use io_manager here
                with open(fp.CHANGELOG_POPUP_SHOWN, 'w', encoding="utf-8") as write_file:
                    write_file.write(get_version_info().commit_id)

        return