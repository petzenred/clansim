# screen_manager.py - ScreenManager class, which handles building and changing between screens.

# ---------------------------------------------------------------------------- #
#                                  UI RULES                                    #
# ---------------------------------------------------------------------------- #
"""
SCREEN: 700 height x 800 width

MARGINS: 25px on all sides
    ~Any new buttons or text MUST be within these margins.
    ~Buttons on the edge of the screen should butt up right against the margin.
    (i.e. the <<Main Menu button is placed 25px x 25px on most screens)

BUTTONS:
    ~Buttons are 30px in height. Width can be anything, though generally try to keep to even numbers.
    ~Square icons are 34px x 34px.
    ~Generally keep text at least 5px away from the right and left /straight/ (do not count the rounded ends) edge
    of the button (this rule is sometimes broken. the goal is to be consistent across the entire screen or button type)
    ~Generally, the vertical gap between buttons should be 5px
"""

########################################################################################################################
# Imports
########################################################################################################################

# determines what can be imported from this module
# __all__ = ['screen_manager']

import os
from math import floor
from typing import Optional

import pygame
import pygame_gui

from definitions import (
    ScreenBackground, SwitchScreenButtonName, ButtonStyle, BoxShape, Icon, UIElementPath,
    CampKey, ScreenName, Season,
    AVAILABLE_SEASONS,
    DEFAULT_WINDOW_POS,
    DEFAULT_WINDOW_SIZE_X, DEFAULT_WINDOW_SIZE_Y, DEFAULT_SCREEN_SCALE,
    FULLSCREEN_SCALE_MULT_X, FULLSCREEN_SCALE_MULT_Y, FULLSCREEN_SCALE_ADJ, FULLSCREEN_SCALE_FACTOR,
    WINDOWED_SCALE_MULT_X, WINDOWED_SCALE_MULT_Y, WINDOWED_SCALE_FACTOR, cast_to_camp_key, ThemeName, ClanSymbolTag,
    STAR_CLAN_TOKEN, DF_CLAN_TOKEN, UR_CLAN_TOKEN, UniversalButtonName
)
import resources._red.red_filepaths as fp

from scripts._red.config_manager import config
from scripts._red.red_exceptions import InitializationError
from scripts.game_structure import image_cache
from scripts.housekeeping.version import get_version_info
from scripts.ui.generate_screen_scale_json import generate_screen_scale
from scripts.ui.ui_elements import UISurfaceImageButton, UIImageButton
from scripts.ui.ui_manager import UIManager
from scripts._red.utils.ui_utils import (
    get_text_box_theme,
    ui_scale,
    ui_scale_blit,
    ui_scale_dimensions,
    ui_scale_offset,
    ui_scale_value,
)

import logging
logger = logging.getLogger(__name__)


########################################################################################################################
# Classes
########################################################################################################################

""" 
from scripts.game_structure.screen_settings import screen_scale, ui_manager, screen, toggle_fullscreen
toggle_fullscreen(
    fullscreen=config.Fullscreen,
    show_confirm_dialog=False,
    ingame_switch=False,
)
from scripts.screens.all_screens import AllScreens
import scripts.game_structure.screen_settings
clock = pygame.time.Clock()
pygame.display.set_icon(pygame.image.load("resources/images/icons/_icon_.png"))
"""

# -------------------------------------------------------------------------------- #
# ----------------------------------------
# ----------------------------------------
# ----------------------------------------
# ----------------------------------------

class ScreenManager:
    """ This class manages a lot of things related to the UI.
    - calculates game window size, position, and screen scaling
    - handles toggling fullscreen mode
    - creates and tracks all RedBaseScreen objects
    - creates and tracks all pygame.Surface objects

    TODO
     - set self.active_clan_camp_key when game sets active_clan_token
    """

    uim: UIManager = None # Optional[pygame_gui.UIManager]

    active_clan_token: str = None
    active_clan_camp_key: CampKey = CampKey.NoCamp
    _time_manager = None # type = TimeManager # FIXME set this

    # flags
    display_change_in_progress_f: bool = False # this acts as a lock to ensure we don't end up
                                               # in a loop of fullscreen changes
    switch_screens_f: bool = False
    mns_widget_open_f: bool = False # whether the Moons and Season widget should be open or closed

    # changed from screen size to make the difference between monitor and window sizes clearer
    _monitor_size_x: int = 0 # screen_settings.game_screen_size[0]
    _monitor_size_y: int = 0 # screen_settings.game_screen_size[1]
    window_size_x: int = DEFAULT_WINDOW_SIZE_X # screen_settings.screen_x
    window_size_y: int = DEFAULT_WINDOW_SIZE_Y # screen_settings.screen_y
    window_pos: tuple[int, int] = DEFAULT_WINDOW_POS # where the window is located on the screen
    window_scale: float = DEFAULT_SCREEN_SCALE # screen_settings.screen_scale

    # information about the current screen
    curr_surface_obj: Optional[pygame.Surface] = None # screen_settings.screen, BaseScreen.game_screen
    curr_screen_name: ScreenName = ScreenName.ScreenUnset
    curr_screen_info: Optional[dict] = None
    viewing_clan_token: str = None
    viewing_living_cats: bool = True
    viewing_list_page: int = 1

    # used when changing screens
    switch_to_screen_name: ScreenName = ScreenName.ScreenUnset
    last_screen_name: ScreenName = ScreenName.ScreenUnset
    last_non_profile_screen_name: ScreenName = ScreenName.ScreenUnset

    # TODO what are these?
    game_frame_surface_obj: pygame.Surface = None
    # core_vignette_surface_obj = pygame.image.load(fp.CORE_VIGNETTE)
    # core_vignette_surface_obj = pygame.image.load(fp.CORE_VIGNETTE).convert() ?
    vignette_surface_obj: pygame.Surface = None
    drop_shadow_surface_obj: pygame.Surface = None
    fade_surface_obj: pygame.Surface = None
    version_number_label: pygame_gui.elements.UILabel
    dev_watermark: pygame_gui.elements.UILabel

    # TODO what are these?
    #  I think I should combine game_bgs and all_screen_objs
    #  Actually, I think the difference is that backgrounds either one of three things:
    #  A camp, a solid colour, or the main menu
    # global default_fullscreen_bgs
    # global default_game_bgs
    all_screen_objs: dict = {} # dict[ScreenName, RedBaseScreen]
    menu_buttons: dict[str | UIElementPath, pygame_gui.core.UIElement] = {}
    non_camp_bgs: dict[ScreenBackground, pygame.Surface] = {}
    # only the active Clan's camp is created and saved
    camp_bgs: dict[Season, pygame.Surface] = {}
    default_fullscreen_bgs: dict[ScreenBackground | Season, pygame.Surface] = {}

    def _ready_to_go(self) -> bool:
        ready_f: bool = True
        if not self._monitor_size_x: # is the screen size known?
            ready_f = False
        if not self.uim: # has the PyGame UI manager been created?
            ready_f = False
        if self.curr_screen_name is ScreenName.ScreenUnset: # has the current screen been set?
            ready_f = False
        if not self.active_clan_token: # is the current Clan known? FIXME what if no Clan exists yet?
            ready_f = False
        # TODO make sure all backgrounds have been created
        if not ready_f:
            raise InitializationError(f"Screen manager hasn't been fully initialized yet")
        return ready_f

    # ------------------------------------- INIT ------------------------------------- #

    def __init__(self):
        # create the UIManager
        self._load_ui_manager()

        # create the buttons and RedBaseScreen objects
        self._set_display_mode()
        self.rebuild_core()
        return

    def _load_ui_manager(self):
        """ Creates a UIManager object and readies it for use.

        :return UIManager: the created object
        """
        # if there's already a self.uim, safely delete it before proceeding
        if self.uim is not None:
            del self.uim
            self.uim = None

        # make sure the window and monitor size values have been set
        if not self._monitor_size_x:
            self._set_screen_sizes()

        # load translation dictionaries
        translation_paths = []
        for root, dirs, files in os.walk(fp.TRANSLATION_DICTS_FILEPATH):
            for directory in dirs:
                translation_paths.append(os.path.join(root, directory))
            break

        # don't need to update old settings data from pre-localization
        #   since unlike ClanGen, ClanSim never didn't have localizations

        # initialize pygame_gui manager
        manager = UIManager(
            window_resolution=(self.window_size_x, self.window_size_y),
            offset=self.window_pos,
            screen_scale=self.window_scale,
            theme_path=None,
            enable_live_theme_updates=False,
            starting_language=config.settings.Language.value,
            translation_directory_paths=translation_paths
        )

        # load fonts
        manager.add_font_paths(
            font_name=fp.NOTOSANS_FONT.Name,
            regular_path=str(fp.NOTOSANS_FONT.Regular),
            bold_path=str(fp.NOTOSANS_FONT.Bold),
            italic_path=str(fp.NOTOSANS_FONT.Italic),
            bold_italic_path=str(fp.NOTOSANS_FONT.BoldItalic))
        manager.add_font_paths(
            font_name=fp.CLANGEN_FONT.Name,
            regular_path=str(fp.CLANGEN_FONT.Regular))

        self.uim = manager

        self._generate_and_load_theme()

        return

# ------------------------------------ PUBLIC ------------------------------------ #

    def set_active_clan_camp(self, camp_key: CampKey):
        """ Update the ScreenManager on the active Clan's camp location. """
        logger.debug(f"Setting ScreenManager.active_camp_key to {camp_key}")
        self.active_clan_camp_key = cast_to_camp_key(camp_key)
        self._build_camp_bgs()
        return

    def update_active_clan_token(self, new_active_clan_token: str):
        logger.debug(f"Setting ScreenManager.active_clan_token to {new_active_clan_token}")
        self.active_clan_token = new_active_clan_token
        self.active_clan_camp_key = CampKey.NoCamp
        return

    def toggle_fullscreen(self):
        """ Swap between fullscreen modes. """
        # if the display is already being changed, wait until it's done changing, then proceed
        # FIXME this risks an infinite loop

        while self.display_change_in_progress_f:
            logger.debug(f"Waiting to toggle fullscreen mode until previous display change finishes...")
            continue

        # if this isn't being called by the user, it's being called when the game is booting, so don't
        #   actually toggle the fullscreen setting
        if not self.curr_screen_name is ScreenName.ScreenUnset:
            config.settings.Fullscreen = not config.settings.Fullscreen
            config.save_game_settings()
            # config.update_setting("Fullscreen", fullscreen_f)

        self._set_display_mode()
        return

    def rebuild_core(self, *, should_rebuild_buttons=True, should_rebuild_bgs=True):
        """ Builds screens and buttons.

        Menu buttons are used very often, so they are generated here.
        """
        logger.debug(f"Rebuilding screens core...")
        if should_rebuild_buttons:
            self.rebuild_buttons()
        if should_rebuild_bgs:
            self.build_bg_surfaces()
        logger.debug(f"Finished rebuilding screens core")
        return

    def rebuild_buttons(self):
        """ Builds menu buttons, which are used very often, so they are generated here. """
        from scripts.ui.generate_button import get_button_dict

        # the buttons have to be added individually as some of them rely on others in anchors
        self.menu_buttons[SwitchScreenButtonName.GoScreenEvents] = UISurfaceImageButton(
            ui_scale(rect=pygame.Rect((246, 60), (82, 30)), scale=self.window_scale),
            "screens.core.events",
            get_button_dict(ButtonStyle.MenuLeft, (82, 30), scale=self.window_scale),
            visible=False,
            manager=self.uim,
            object_id=pygame_gui.core.ObjectID("#events_button", "@ButtonStyle_menu_left"),
            starting_height=5,
            screen_manager=self,
        )
        self.menu_buttons[SwitchScreenButtonName.GoScreenCamp] = UISurfaceImageButton(
            ui_scale(rect=pygame.Rect((0, 60), (58, 30)), scale=self.window_scale),
            "screens.core.camp",
            get_button_dict(ButtonStyle.MenuMiddle, (58, 30), scale=self.window_scale),
            visible=False,
            manager=self.uim,
            object_id="@ButtonStyle_menu_middle",
            starting_height=5,
            anchors={"left": "left", "left_target": self.menu_buttons[SwitchScreenButtonName.GoScreenEvents]},
            screen_manager=self,
        )
        self.menu_buttons[SwitchScreenButtonName.GoScreenCatList] = UISurfaceImageButton(
            ui_scale(rect=pygame.Rect((0, 60), (88, 30)), scale=self.window_scale),
            "screens.core.cat_list",
            get_button_dict(ButtonStyle.MenuMiddle, (88, 30), scale=self.window_scale),
            visible=False,
            manager=self.uim, # TODO this was missing originally, make sure it should be here
            object_id="@ButtonStyle_menu_middle",
            starting_height=5,
            anchors={"left": "left", "left_target": self.menu_buttons[SwitchScreenButtonName.GoScreenCamp]},
            screen_manager=self,
        )
        self.menu_buttons[SwitchScreenButtonName.GoScreenPatrol] = UISurfaceImageButton(
            ui_scale(rect=pygame.Rect((0, 60), (80, 30)), scale=self.window_scale),
            "screens.core.patrol",
            get_button_dict(ButtonStyle.MenuRight, (80, 30), scale=self.window_scale),
            visible=False,
            manager=self.uim,
            object_id="#patrol_button",
            starting_height=5,
            anchors={"left": "left", "left_target": self.menu_buttons[SwitchScreenButtonName.GoScreenCatList]},
            screen_manager=self,
        )
        self.menu_buttons[SwitchScreenButtonName.GoScreenMainMenu] = UISurfaceImageButton(
            ui_scale(rect=pygame.Rect((25, 25), (153, 30)), scale=self.window_scale),
            "buttons.main_menu",
            get_button_dict(ButtonStyle.SquOval, (153, 30), scale=self.window_scale),
            visible=False,
            manager=self.uim,
            object_id="@ButtonStyle_squoval",
            starting_height=5,
            screen_manager=self,
        )

        # used so we can anchor to the right with numbers that make sense
        scale_rect = ui_scale(rect=pygame.Rect((0, 0), (118, 30)), scale=self.window_scale)
        scale_rect.topright = ui_scale_offset(coords=(-25, 25), scale=self.window_scale)
        self.menu_buttons[SwitchScreenButtonName.GoScreenAllegiances] = UISurfaceImageButton(
            scale_rect,
            "screens.core.allegiances",
            get_button_dict(ButtonStyle.SquOval, (118, 30), scale=self.window_scale),
            visible=False,
            manager=self.uim,
            object_id=pygame_gui.core.ObjectID(class_id="@image_button", object_id=None),
            starting_height=5,
            anchors={"top": "top", "right": "right"},
            screen_manager=self,
        )

        # used so we can anchor to the right with numbers that make sense
        scale_rect = ui_scale(rect=pygame.Rect((0, 0), (85, 30)), scale=self.window_scale)
        scale_rect.topright = ui_scale_offset(coords=(-25, 5), scale=self.window_scale)
        self.menu_buttons[SwitchScreenButtonName.GoScreenClanSettings] = UISurfaceImageButton(
            scale_rect,
            "screens.core.settings",
            get_button_dict(ButtonStyle.SquOval, (85, 30), scale=self.window_scale),
            visible=False,
            manager=self.uim,
            object_id=pygame_gui.core.ObjectID(class_id="@image_button", object_id=None),
            starting_height=5,
            anchors={"top_target": self.menu_buttons[SwitchScreenButtonName.GoScreenAllegiances], "right": "right"},
            screen_manager=self,
        )
        del scale_rect

        heading_rect = ui_scale(rect=pygame.Rect((0, 0), (190, 35)), scale=self.window_scale)
        heading_rect.bottomleft = ui_scale_dimensions(dim=(0, 0), scale=self.window_scale)
        self.menu_buttons[UIElementPath.ClanNameHeader] = pygame_gui.elements.UIImage(
            heading_rect,
            pygame.transform.scale(
                image_cache.load_image(fp.CLAN_NAME_HEADER).convert_alpha(), # fp.CLAN_NAME_HEADER
                ui_scale_dimensions((190, 35)),
            ),
            visible=False,
            manager=self.uim,
            starting_height=5,
            anchors={
                "bottom": "bottom",
                "bottom_target": self.menu_buttons[SwitchScreenButtonName.GoScreenCamp],
                "centerx": "centerx",},
        )
        # it has to be at least 193 to make "cats outside the clan" fit
        heading_rect = ui_scale(rect=pygame.Rect((0, 0), (193, 35)), scale=self.window_scale)
        heading_rect.bottomleft = ui_scale_offset(coords=(0, 1), scale=self.window_scale)  # yes, this is intentional.
        self.menu_buttons[UniversalButtonName.DropdownChooseClan] = pygame_gui.elements.UITextBox(
            "",
            heading_rect,
            visible=False,
            manager=self.uim,
            object_id=pygame_gui.core.ObjectID(
                "#text_box_34_horizcenter_vertcenter", "#dark"
            ),
            starting_height=5,
            anchors={
                "bottom": "bottom",
                "bottom_target": self.menu_buttons[SwitchScreenButtonName.GoScreenCamp],
                "centerx": "centerx",
            },
        )
        del heading_rect

        self.menu_buttons[UIElementPath.MoonsSeasonsWidget] = pygame_gui.elements.UIScrollingContainer(
            ui_scale(rect=pygame.Rect((25, 60), (153, 75)), scale=self.window_scale),
            visible=False,
            allow_scroll_x=False,
            manager=self.uim,
            starting_height=5,
        )
        self.menu_buttons[UniversalButtonName.MoonsSeasonsArrow] = UIImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((174, 80), (22, 34)), scale=self.window_scale),
            text="",
            visible=False,
            manager=self.uim,
            object_id="#arrow_mns_button",
            starting_height=5,
            screen_manager=self,
        )
        self.menu_buttons[UIElementPath.DropdownDensBar] = pygame_gui.elements.UIImage(
            ui_scale(rect=pygame.Rect((40, 5), (10, 160)), scale=self.window_scale),
            pygame.transform.scale(
                image_cache.load_image(fp.BAR_VERTICAL).convert_alpha(),
                ui_scale_dimensions((380, 70), scale=self.window_scale),
            ),
            visible=False,
            starting_height=5,
            manager=self.uim,
            anchors={"top_target": self.menu_buttons[SwitchScreenButtonName.GoScreenMainMenu]},
        )
        self.menu_buttons[UniversalButtonName.DropdownDens] = UISurfaceImageButton(
            ui_scale(rect=pygame.Rect((25, 5), (71, 30)), scale=self.window_scale),
            "screens.core.dens",
            get_button_dict(ButtonStyle.SquOval, (71, 30), scale=self.window_scale),
            visible=False,
            manager=self.uim,
            object_id="@ButtonStyle_squoval",
            starting_height=6,
            anchors={"top_target": self.menu_buttons[SwitchScreenButtonName.GoScreenMainMenu]},
            screen_manager=self,
        )
        self.menu_buttons[SwitchScreenButtonName.GoScreenLeaderDen] = UISurfaceImageButton(
            ui_scale(rect=pygame.Rect((25, 100), (112, 28))),
            "screens.core.leader_den",
            get_button_dict(ButtonStyle.RoundedRect, (112, 28), scale=self.window_scale),
            visible=False,
            manager=self.uim,
            object_id="@ButtonStyle_rounded_rect",
            starting_height=6,
            screen_manager=self,
        )
        self.menu_buttons[SwitchScreenButtonName.GoScreenHealerDen] = UISurfaceImageButton(
            ui_scale(rect=pygame.Rect((25, 140), (151, 28)), scale=self.window_scale),
            "screens.core.medicine_cat_den",
            get_button_dict(ButtonStyle.RoundedRect, (151, 28), scale=self.window_scale),
            object_id="@ButtonStyle_rounded_rect",
            visible=False,
            manager=self.uim,
            starting_height=6,
            screen_manager=self,
        )
        self.menu_buttons[SwitchScreenButtonName.GoScreenWarriorDen] = UISurfaceImageButton(
            ui_scale(rect=pygame.Rect((25, 180), (121, 28)), scale=self.window_scale),
            "screens.core.warriors_den",
            get_button_dict(ButtonStyle.RoundedRect, (121, 28), scale=self.window_scale),
            object_id="@ButtonStyle_rounded_rect",
            visible=False,
            manager=self.uim,
            starting_height=6,
            screen_manager=self,
        )
        self.menu_buttons[SwitchScreenButtonName.GoScreenFreshkillPile] = UISurfaceImageButton(
            ui_scale(rect=pygame.Rect((25, 220), (81, 28)), scale=self.window_scale),
            "screens.core.clearing",
            get_button_dict(ButtonStyle.RoundedRect, (81, 28), scale=self.window_scale),
            visible=False,
            manager=self.uim,
            object_id="@ButtonStyle_rounded_rect",
            starting_height=6,
            screen_manager=self,
        )

        # build and position the buttons to mute and unmute sounds and music
        #   this section used to be screen_core.rebuild_mute()
        # TODO for the NewClan screen, this is moved to the top right; I need to deal with that since I removed the
        #   location parameter
        logger.debug(f"Running the section of ScreenManager.rebuild_core() which used to be screen_core.rebuild_mute()")
        if UniversalButtonName.Mute in self.menu_buttons:
            self.menu_buttons[UniversalButtonName.Mute].kill()
            self.menu_buttons[UniversalButtonName.Unmute].kill()

        # place the mute button at the bottom right of the screen
        mute_pos = ui_scale(rect=pygame.Rect((0, 0), (34, 34)), scale=self.window_scale)
        mute_pos.bottomright = ui_scale_offset(coords=(-25, -25), scale=self.window_scale)
        self.menu_buttons[UniversalButtonName.Mute] = UISurfaceImageButton(
            mute_pos,
            Icon.Speaker,
            get_button_dict(ButtonStyle.Icon, (34, 34), scale=self.window_scale),
            visible=False,
            manager=self.uim,
            object_id="@ButtonStyle_icon",
            starting_height=6,
            anchors={"bottom": "bottom", "right": "right"},
            screen_manager=self,
        )
        self.menu_buttons[UniversalButtonName.Unmute] = UISurfaceImageButton(
            mute_pos,
            Icon.MUTE,
            get_button_dict(ButtonStyle.Icon, (34, 34), scale=self.window_scale),
            visible=False,
            manager=self.uim,
            object_id="@ButtonStyle_icon",
            starting_height=6,
            anchors={"bottom": "bottom", "right": "right"},
            screen_manager=self,
        )

        # build the version number label
        self.version_number_label = pygame_gui.elements.UILabel(
            ui_scale(rect=pygame.Rect((50, 50), (-1, -1)), scale=self.window_scale),
            get_version_info().commit_id[0:8],
            object_id=get_text_box_theme(),
            anchors={"bottom": "bottom", "right": "right"},
        )
        # Adjust position
        self.version_number_label.set_relative_position(
            ui_scale_offset(
                (
                    DEFAULT_WINDOW_SIZE_X - self.version_number_label.get_relative_rect()[2],
                    DEFAULT_WINDOW_SIZE_Y - self.version_number_label.get_relative_rect()[3],
                ),
                scale=self.window_scale
            )
        )

        # build the dev watermark label
        if get_version_info().is_source_build or get_version_info().is_dev:
            self.dev_watermark = pygame_gui.elements.UILabel(
                ui_scale(rect=pygame.Rect((525, 660), (300, 50)), scale=self.window_scale),
                "screens.core.dev_watermark",
                object_id="#dev_watermark",
                text_kwargs={"ver": self.version_number_label.text},
            )
            self.version_number_label.kill()
            self.version_number_label = None
        return

    # FIXME this should be called when switching between themes
    def build_bg_surfaces(self):
        """ Rebuilds the menu, cat list, and camp backgrounds. """
        self._build_menu_bgs()
        self._build_camp_bgs()
        return

    # TODO discord status update
    def queue_screen_switch(self, new_screen_name: ScreenName):
        """ Switch to a new screen.

        This replaces the old BaseScreen.screen_switches / change_screen TODO

        :param ScreenName new_screen_name: the screen to switch to
        """
        # if self.curr_screen_name == new_screen_name:
        #     logger.debug(f"Skipping queued screen switch from {self.curr_screen_name} to {new_screen_name}")
        #     return
        if self.curr_screen_name is new_screen_name:
            logger.warning(f"Skipping requested screen switch from {self.curr_screen_name} "
                           f"to {new_screen_name}")
            return
        else:
            logger.debug(f"Queue screen switch: {self.curr_screen_name} -> {new_screen_name}")
        self.switch_to_screen_name = new_screen_name

        # music_manager.check_music(new_screen_name) moved to RedBaseScreen

        # When using the 'Back' button from the Profile screen, the player could want to see the Camp, Events, or
        #   CatList screen. If it's the CatList screen, then going into a cat's profile shouldn't change which page
        #   of the CatLit screen the player was looking at.
        if new_screen_name is ScreenName.Profile:
            self.last_non_profile_screen_name = self.curr_screen_name
            if self.last_non_profile_screen_name is not ScreenName.CatList:
                self.viewing_living_cats = True
                self.viewing_clan_token = self.active_clan_token
                self.viewing_list_page = 1

        # TODO update game.rpc.update_rpc.set()

        if (
                self.active_clan_token is not None
                and config.settings.ShowMoonSeasonWidget
                and new_screen_name is not ScreenName.Events
        ):
            x_shift = 1358
            y_shift = 70
        else:
            x_shift = 0
            y_shift = 0

        self.all_screen_objs[self.switch_to_screen_name].mns_ui_offset(x_shift, y_shift)

        # main.py will check this to actually switch the screens
        self.switch_screens_f = True
        return

    # TODO
    def run_screen_switch(self):
        """ Completes a screen switch queued by ScreenManager.queue_screen_switch().

        Used to be BaseScreen.screen_switches().
        """
        if self.switch_to_screen_name is ScreenName.ScreenUnset:
            raise ValueError(f"Can't switch to screen ScreenUnset!")

        logger.debug(f"Running screen switch: {self.curr_screen_name} -> {self.switch_to_screen_name}")

        if self.curr_screen_name is not ScreenName.ScreenUnset:
            # old_screen_obj = self.all_screen_objs[self.curr_screen_name]
            # old_screen_obj.exit_screen()
            self.all_screen_objs[self.curr_screen_name].exit_screen()
        # new_screen_obj = self.all_screen_objs[self.switch_to_screen_name]
        # new_screen_obj.enter_screen()
        self.all_screen_objs[self.switch_to_screen_name].enter_screen()

        self.last_screen_name = self.curr_screen_name
        self.curr_screen_name = self.switch_to_screen_name
        self.switch_to_screen_name = ScreenName.ScreenUnset

        self.switch_screens_f = False
        return

    def show_screen_background(self, screen_name: ScreenName):
        """ Set the currently active background for a screen.

        This is called by ScreenManager.run_screen_switch().

        The options are a solid colour (a shade of brown which depends on the current theme), the main menu background,
        or one of several special backgrounds for the 'Clan members' lists for StarClan, the Dark Forest, and the
        Unknown Residence where non-Clan cats go when they die.

        :param ScreenName screen_name: the screen whose background should be loaded
        """
        # TODO when should the screen use a transition?
        do_transition_f: bool = False

        # find the correct background
        bg_name = ScreenBackground.SolidColour
        if screen_name is ScreenName.MainMenu:
            bg_name = ScreenBackground.MainMenuLogoless
        elif screen_name is ScreenName.Camp and config.settings.ShowCampBackground:
            bg_name = ScreenBackground.ClanCamp
        elif screen_name is ScreenName.CatList and not self.viewing_living_cats:
            if self.viewing_clan_token is STAR_CLAN_TOKEN:
                bg_name = ScreenBackground.StarClanCatsList
            elif self.viewing_clan_token is DF_CLAN_TOKEN:
                bg_name = ScreenBackground.DarkForestCatsList
            elif self.viewing_clan_token is UR_CLAN_TOKEN:
                bg_name = ScreenBackground.UnknownResidenceCatsList

        # actually run the blit
        # if do_transition_f:
        #     # enable the transition if required
        #     if self.bg_transition:
        #         # this determines how many frames the fade can show for
        #         # in order to remove visual artifacts
        #         self.bg_transition_time = 5
        #         self.bg_transition = False
        #
        #     # actually run the transition
        #     if self.bg_transition_time > 0:
        #         temp = blur_bg.copy()
        #         temp.set_alpha(
        #             255 // self.bg_transition_time
        #         )  # this determines the actual fade rate
        #         scripts.game_structure.screen_settings.screen.blit(temp, (0, 0))
        #         self.bg_transition_time -= 1
        #     else:
        #         # if we've done the transition, just blit the full-alpha version on top to remove artifacts.
        #         scripts.game_structure.screen_settings.screen.blit(blur_bg, (0, 0))

        # now blit the foreground
        if bg_name is ScreenBackground.ClanCamp:
            self.curr_surface_obj.blit(self.camp_bgs[self._time_manager.curr_season], ui_scale_blit((0, 0)))
        else:
            self.curr_surface_obj.blit(self.non_camp_bgs[bg_name], ui_scale_blit((0, 0)))

        return

    # ----------------------------------- PRIVATE ------------------------------------ #

    def _generate_and_load_theme(self):
        """ Generates a new file with scaled theme elements and loads in to the PyGame UI manager. """
        logger.debug(f"Creating and loading new theme...")
        try:
            generate_screen_scale(
                input_file=fp.THEME_FILEPATHS[config.settings.Theme],
                output_file=fp.SCREEN_SCALE_OUTPUT_FILEPATH,
                multiplier=self.window_scale)

            # TODO catch warnings.warn() UserWarning (try/except doesn't work)
            # self.uim.get_theme().load_theme(fp.SCREEN_SCALE_OUTPUT_FILEPATH)
            theme: pygame_gui.core.UIAppearanceTheme = \
                self.uim.create_new_theme(theme_path=fp.SCREEN_SCALE_OUTPUT_FILEPATH)
            self.uim.set_ui_theme(theme=theme, update_all_sprites=True)
        except Exception as err:
            msg: str = f"Something went wrong while loading the UI theme!"
            logger.warning(msg=msg, exc_info=err)
            raise InitializationError(msg)
        else:
            logger.debug(f"Successfully loaded theme")
            return

    def _set_screen_sizes(self):
        """ Calculates values for window size, scaling factor, and position.

        This method ONLY CALCULATES the values; it does not update the game window.
        """
        # the size of the player's primary display, e.g. (3840, 2160)
        self._monitor_size_x, self._monitor_size_y = pygame.display.get_desktop_sizes()[0]

        # SCREEN SIZE
        if config.settings.Fullscreen:
            # if ClanSim is in fullscreen mode, then the window size and screen size are the same
            window_size_x = self._monitor_size_x
            window_size_y = self._monitor_size_y
        else:
            window_size_x = DEFAULT_WINDOW_SIZE_X
            window_size_y = DEFAULT_WINDOW_SIZE_Y

        # WINDOW SCALING FACTOR
        if config.settings.FullscreenScaling:  # TODO should this only be active when the game is in fullscreen mode?
            scale_x: int = (window_size_x - FULLSCREEN_SCALE_ADJ) // FULLSCREEN_SCALE_MULT_X
            scale_y: int = (window_size_y - FULLSCREEN_SCALE_ADJ) // FULLSCREEN_SCALE_MULT_Y

            self.window_scale = min(scale_x, scale_y) / FULLSCREEN_SCALE_FACTOR
        else:
            # this means screen scales in multiples of 200 x 175 which has a reasonable tradeoff for crunch
            scale_x: int = window_size_x // WINDOWED_SCALE_MULT_X
            scale_y: int = window_size_y // WINDOWED_SCALE_MULT_Y

            self.window_scale = min(scale_x, scale_y) / WINDOWED_SCALE_FACTOR

        self.window_size_x = floor(window_size_x * self.window_scale) # floor(DEFAULT_WINDOW_SIZE_X * self.window_scale)
        self.window_size_y = floor(window_size_y * self.window_scale) # floor(DEFAULT_WINDOW_SIZE_Y * self.window_scale)
        self.window_pos = (
            floor((self._monitor_size_x - self.window_size_x) / 2),
            floor((self._monitor_size_y - self.window_size_y) / 2)
        )

        return

    def _set_display_mode(self):
        """ This essentially sets up the display Surface object.

        Switching in and out of fullscreen mode is handled in toggle_fullscreen, which then calls this method.
        """
        # make sure the game isn't already in the middle of a display change
        if self.display_change_in_progress_f:
            return
        self.display_change_in_progress_f = True

        # get the information about the current screen in order to rebuild accurately it later (in _set_display_mode)
        if self.curr_screen_name is not ScreenName.ScreenUnset:
            curr_screen_obj = self.all_screen_objs[self.curr_screen_name]
            self.curr_screen_info = curr_screen_obj.get_screen_info()

        old_window_pos: tuple[int, int] = self.window_pos
        old_scale: float = self.window_scale
        mouse_pos: tuple[int, int] = pygame.mouse.get_pos()

        self._set_screen_sizes()

        # TODO "# generate new theme" used to be below "# set the screen mode"; was moving it correct?


        # set the screen mode
        # THIS MUST BE RUN BEFORE ANY IMAGES ARE LOADED
        if config.settings.Fullscreen:
            # set_mode(size=00, flags=0, depth=0, display=0, vsync=0)
            #   initializes a window or screen for display
            self.curr_surface_obj = pygame.display.set_mode(
                size=(self.window_size_x, self.window_size_y),
                flags=pygame.FULLSCREEN,
                display=config.settings.FullScreen # TODO is this required with the flag?
            )
        else:
            self.curr_surface_obj = pygame.display.set_mode(
                size=(self.window_size_x, self.window_size_y)
            )

        # TODO "# generate new theme" used to be here; was moving it correct?
        # generate new theme
        self._generate_and_load_theme()

        # FIXME - add the loading animation here

        # <------------------- DEBUG -------------------> #
        # this reloads the current screen if this method has been called because of a screen change, not the game loading
        if self.curr_screen_name is not ScreenName.ScreenUnset:

            self.uim.set_window_resolution((self.window_size_x, self.window_size_y))
            self.uim.set_offset(self.window_pos)
            self.build_bg_surfaces()

            if old_scale != self.window_scale:
                self._reload_curr_screen(old_window_pos=old_window_pos,
                                         old_scale=old_scale,
                                         mouse_pos=mouse_pos)

        # <------------------- DEBUG -------------------> #

        # preloading the associated fonts
        # FIXME doesn't this happen in _load_ui_manager?
        if not self.uim.ui_theme.get_font_dictionary().check_font_preloaded(
            f"notosans_bold_aa_{floor(11 * self.window_scale)}"
        ):
            self.uim.preload_fonts(
                [
                    {
                        "name": "notosans",
                        "point_size": floor(11 * self.window_scale),
                        "style": "bold",
                    },
                    {
                        "name": "notosans",
                        "point_size": floor(13 * self.window_scale),
                        "style": "bold",
                    },
                    {
                        "name": "notosans",
                        "point_size": floor(15 * self.window_scale),
                        "style": "bold",
                    },
                    {
                        "name": "notosans",
                        "point_size": floor(13 * self.window_scale),
                        "style": "italic",
                    },
                    {
                        "name": "notosans",
                        "point_size": floor(15 * self.window_scale),
                        "style": "italic",
                    },
                    {
                        "name": "notosans",
                        "point_size": floor(17 * self.window_scale),
                        "style": "bold",
                    },  # this is only used on the allegiances screen?
                    {
                        "name": "clangen",
                        "point_size": floor(18 * self.window_scale),
                        "style": "regular",
                    },
                ]
            )

        # always show the 'confirm dialogue' popup
        if self.curr_screen_name is not ScreenName.ScreenUnset:
            from scripts._red.screens.windows import ConfirmDisplayChanges
            ConfirmDisplayChanges()

        self.display_change_in_progress_f = False
        return

    def _reload_curr_screen(self, old_window_pos: tuple[int, int], old_scale: float, mouse_pos: tuple[int, int]):
        """ This reloads the current screen if this method has been called because the display mode has changed,
        not the game loading.
        """
        if self.curr_screen_name is not ScreenName.ScreenUnset:

            self.uim.set_window_resolution((self.window_size_x, self.window_size_y))
            self.uim.set_offset(self.window_pos)
            self.build_bg_surfaces()

            if old_scale != self.window_scale:
                self.all_screen_objs[self.curr_screen_name].exit_screen()

                if config.settings.Fullscreen:
                    mouse_pos = (int(mouse_pos[0] * self.window_scale) + self.window_pos[0],
                                 int(mouse_pos[1] * self.window_scale) + self.window_pos[1])
                else:
                    mouse_pos = (int((mouse_pos[0] - old_window_pos[0]) / old_scale),
                                 int((mouse_pos[1] - old_window_pos[1]) / old_scale))

                self.uim.clear_and_reset()
                self.uim.set_window_resolution(window_resolution=(self.window_size_x, self.window_size_y))
                self.uim.set_offset(self.window_pos)
                pygame.mouse.set_pos(mouse_pos)

                if self._ready_to_go():
                    self.build_all_screens()
                    self.rebuild_core()
                    # scripts.debug_console.debug_mode.rebuild_console() # TODO fix debug mode

                    # switch to the correctly scaled version of the same screen
                    new_screen_obj = self.all_screen_objs[self.curr_screen_name]
                    new_screen_obj.screen_switches()

                    if self.curr_screen_obj:
                        new_screen_obj.set_screen_info(self.curr_screen_info)

                    if self.curr_screen_info is not None:
                        new_screen_obj.set_screen_info(self.curr_screen_info)
                        self.curr_screen_info = None

        else:
            logger.warning(f"Can't reload the current screen because no screen has been loaded yet!")

    # FIXME
    def build_all_screens(self):
        """ Import all screens for initialization (must be done after pygame_gui manager is created). """
        logger.debug(f"ScreenManager is building all screens...")
        from scripts._red.screens.red_main_menu_screen import MainMenuScreen
        self.all_screen_objs[ScreenName.MainMenu] = MainMenuScreen()
        # from scripts._red.screens.NewClanScreen import NewClanScreen
        # cls.new_clan_screen = NewClanScreen()
        # from scripts._red.screens.SwitchClanScreen import SwitchClanScreen
        # cls.switch_clan_screen = SwitchClanScreen()
        # from scripts._red.screens.MainSettingsScreen import MainSettingsScreen
        # cls.main_settings_screen = MainSettingsScreen()
        #
        # from scripts._red.screens.ClanEventsScreen import ClanEventsScreen
        # cls.clan_events_screen = ClanEventsScreen()
        # from scripts._red.screens.ClanCampScreen import ClanCampScreen
        # cls.clan_camp_screen = ClanCampScreen()
        # from scripts._red.screens.ClanMembersScreen import ClanMembersScreen
        # cls.clan_members_screen = ClanMembersScreen()
        # from scripts._red.screens.ClanPatrolScreen import ClanPatrolScreen
        # cls.clan_patrol_screen = ClanPatrolScreen()
        #
        # from scripts._red.screens.ClanAllegiancesScreen import ClanAllegiancesScreen
        # cls.clan_allegiances_screen = ClanAllegiancesScreen()
        # from scripts._red.screens.ClanSettingsScreen import ClanSettingsScreen
        # cls.clan_settings_screen = ClanSettingsScreen()
        #
        # from scripts._red.screens.DenLeaderScreen import LeaderDenScreen
        # cls.leader_den_screen = LeaderDenScreen()
        # from scripts._red.screens.DenHealerScreen import MedDenScreen
        # cls.med_den_screen = MedDenScreen()
        # from scripts._red.screens.DenWarriorScreen import WarriorDenScreen
        # cls.warrior_den_screen = WarriorDenScreen()
        # from scripts._red.screens.DenFreshkillScreen import ClanFreshkillScreen
        # cls.clan_freshkill_screen = ClanFreshkillScreen()
        #
        # from scripts._red.screens.ProfileScreen import ProfileScreen
        # cls.profile_screen = ProfileScreen()
        # from scripts._red.screens.ProfileAdoptScreen import ProfileAdoptScreen
        # cls.profile_adopt_screen = ProfileAdoptScreen()
        # from scripts._red.screens.ProfileCeremonyScreen import ProfileCeremonyScreen
        # cls.profile_ceremony_screen = ProfileCeremonyScreen()
        # from scripts._red.screens.ProfileFamilyScreen import ProfileFamilyScreen
        # cls.profile_family_screen = ProfileFamilyScreen()
        # from scripts._red.screens.ProfileGenderScreen import ProfileGenderScreen
        # cls.profile_gender_screen = ProfileGenderScreen()
        # from scripts._red.screens.ProfileInspectScreen import ProfileInspectSpriteScreen
        # cls.profile_sprite_inspect_screen = ProfileInspectSpriteScreen()
        # from scripts._red.screens.ProfileMateScreen import ProfileMateScreen
        # cls.profile_mate_screen = ProfileMateScreen()
        # from scripts._red.screens.ProfileMediationScreen import ProfileMediationScreen
        # cls.profile_mediation_screen = ProfileMediationScreen()
        # from scripts._red.screens.ProfileMentorScreen import ProfileMentorScreen
        # cls.profile_mentor_screen = ProfileMentorScreen()
        # from scripts._red.screens.ProfileRelationshipsScreen import ProfileRelationshipsScreen
        # cls.profile_relationship_screen = ProfileRelationshipsScreen()
        # from scripts._red.screens.ProfileRoleScreen import ProfileRoleScreen
        # cls.profile_role_screen = ProfileRoleScreen()

        logger.debug(f"ScreenManager is finished building all screens")
        return

    def _build_menu_bgs(self):
        """ Build pygame.Surface objects for all non-camp backgrounds.

        Used to be screen_core.rebuild_bgs().
        """
        if (
                self.vignette_surface_obj is None
                    or
                self.curr_surface_obj.get_size() != self.vignette_surface_obj.get_size()
        ):
            from scripts.ui.generate_box import get_box
            self.game_frame_surface_obj = get_box(style=BoxShape.Frame,
                                                  unscaled_dimensions=(820, 720), # FIXME hardcoded numbers
                                                  scale=self.window_scale)

            #core_vignette = pygame.image.load(file=fp.CORE_VIGNETTE)
            core_vignette = pygame.image.load(file=fp.CORE_VIGNETTE).convert()
            self.vignette_surface_obj = pygame.transform.scale(
                surface=core_vignette, size=self.curr_surface_obj.get_size())

            self.fade_surface_obj = pygame.Surface(size=self.curr_surface_obj.get_size())
            self.fade_surface_obj.fill(color=config.screen_config.FADE_SURFACE_COLOUR)  # middle grey

            self.drop_shadow_surface_obj = pygame.Surface(
                size=self.curr_surface_obj.get_size(),
                flags=pygame.SRCALPHA,
            )
            game_box: pygame.Surface = pygame.Surface(
                size=(self.window_size_x + ui_scale_value(30, scale=self.window_scale), # FIXME hardcoded numbers
                      self.window_size_y + ui_scale_value(30, scale=self.window_scale)), # FIXME hardcoded numbers
                flags=pygame.SRCALPHA,
            )
            self._feather_surface(surface=game_box, feather_width=15) # FIXME hardcoded numbers
            self.drop_shadow_surface_obj.blit(game_box, ui_scale_blit(coords=(-15, -15), # FIXME hardcoded numbers
                                                                      scale=self.window_scale,
                                                                      window_pos=self.window_pos))
            del game_box

        # build fullscreen pygame.Surface objects (only for the currently active theme)
        logger.debug(f"Building Surface object for the solid colour background")
        solid_colour_bg_obj: pygame.Surface = pygame.Surface(size=self.curr_surface_obj.get_size())
        solid_colour_bg_obj.fill(config.screen_config.themes[config.settings.Theme]["bg_colour"])
        self.non_camp_bgs[ScreenBackground.SolidColour] = self._process_surface_blur(
            surface=solid_colour_bg_obj,
            **ScreenBackground.SolidColour.blur_properties
        )

        # create the backgrounds that are photos (e.g. the main menu)
        logger.debug(f"Building Surface objects for backgrounds which are photos")
        for bg_name in (ScreenBackground.MainMenuLogoless, ScreenBackground.StarClanCatsList,
                        ScreenBackground.DarkForestCatsList, ScreenBackground.UnknownResidenceCatsList):
            bg: pygame.Surface = pygame.transform.scale(
                surface=pygame.image.load(bg_name.path).convert(),
                size=self.curr_surface_obj.get_size()
            )
            # the main menu has a tint in dark mode
            if bg_name is ScreenBackground.MainMenuLogoless and config.settings.Theme is ThemeName.Dark:
                bg.fill(
                    color=config.screen_config.themes[ThemeName.Dark]["mainmenu_tint"],
                    rect=bg.get_rect(),
                    special_flags=pygame.BLEND_MULT,
                )
            # self.non_camp_bgs[bg_name] = bg
            # FIXME apply blur effect to non-camp background screens
            self.non_camp_bgs[bg_name] = self._process_surface_blur(
                surface=bg, **bg_name.blur_properties
            )

        return

    def _build_camp_bgs(self):
        """ Builds surface objects for every season for the active Clan, based on camp and theme.

        Called when loading a Clan, when changing the theme, or when toggling fullscreen mode.

        Used to be screen_core.get_camp_bgs().

        :return dict: key-value pairs are Season objects-pygame.Surface objects
        """
        if self.active_clan_camp_key is not CampKey.NoCamp:
            for season in AVAILABLE_SEASONS:
                bg_path: str = self.active_clan_camp_key.get_bg_path( # FIXME this should be a PathLike
                    season=season, theme=config.settings.Theme)
                surface_obj = pygame.transform.scale(
                    surface=pygame.image.load(bg_path).convert(),
                    size=self.curr_surface_obj.get_size()
                )
                # apply blur effect to camp background
                self.camp_bgs[season] = self._process_surface_blur(surface=surface_obj)
        else:
            logger.warning(f"Couldn't build camp backgrounds because no camp is set in screen_manager! "
                           f"If the game is initializing, this is expected and this message can be ignored.")

        return

    def _process_surface_blur(
            self,
            surface: pygame.Surface,
            blur_radius: Optional[int] = None, # default was 5
            vignette_strength: Optional[int] = None,
            fade_color: Optional[tuple[int, int, int]] = None
    ) -> pygame.Surface:
        """ Add a blur effect to a pygame.Surface.

        Used to be screen_core.process_blur_bg().

        Used by self.rebuild_bgs().

        :param pygame.Surface surface: the background to blur
        :param Optional[int] blur_radius: TODO
        :param Optional[int] vignette_strength: TODO
        :param Optional[tuple[int, int, int]] fade_color: TODO
        """
        # the theme details are grabbed this way to avoid using a hardcoded string
        #   that might not change if the config dictionary does
        theme_details = config.screen_config.themes[config.settings.Theme]

        if fade_color is not None:
            self.fade_surface_obj.fill(color=fade_color)
        else:
            self.fade_surface_obj.fill(color=theme_details["fade_color"])
        if vignette_strength is not None:
            self.vignette_surface_obj.set_alpha(vignette_strength)
        else:
            self.vignette_surface_obj.set_alpha(theme_details["vignette_alpha"])
        self.drop_shadow_surface_obj.set_alpha(theme_details["dropshadow_alpha"])

        # resize the background and adjust alpha
        surface = pygame.transform.scale(
            surface=surface,
            size=self.curr_surface_obj.get_size(),
        ).convert_alpha()

        # if the background should be blurred, blur it
        if blur_radius is not None:
            surface = pygame.transform.box_blur(surface=surface, radius=blur_radius)

        surface.blits(
            (
                (self.fade_surface_obj, (0, 0), None, pygame.BLEND_MULT),
                (self.vignette_surface_obj, (0, 0), None),
                (self.drop_shadow_surface_obj, (0, 0), None),
                (self.game_frame_surface_obj, ui_scale_blit(coords=(-10, -10),
                                                            scale=self.window_scale,
                                                            window_pos=self.window_pos)),
            )
        )

        return surface

    def _feather_surface(self, surface: pygame.Surface, feather_width: int):
        """ Run a per-pixel effect to make a fun fade-to-transparent border.

        Called by self.rebuild_bgs().

        Used to be screen_core.feather_surface().

        :param pygame.Surface surface: The surface to add a feathered edge to
        :param int feather_width: How fat to make the edge
        """
        width, height = surface.get_size()
        for x in range(width):
            for y in range(height):
                distance = min(x, y, width - x - 1, height - y - 1)
                if distance < feather_width:
                    alpha = int(255 * (distance / feather_width))
                    surface.set_at((x, y), (0, 0, 0, alpha))

        return


########################################################################################################################
# Instances
########################################################################################################################

screen_manager = ScreenManager()
