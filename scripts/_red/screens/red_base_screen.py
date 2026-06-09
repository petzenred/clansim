# RedBaseScreen.py - Base class for all screens.
from abc import abstractmethod
from threading import current_thread

########################################################################################################################
# Imports
########################################################################################################################

from typing import Callable, Optional

import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.core.ui_element import UIElement

from definitions import ScreenName, Season, ThemeName, UIElementPath, SwitchScreenButtonName, GameMode, \
    ScreenBackground, \
    LOADING_SCREEN_DELAY_SEC, UniversalButtonName

from scripts._red.config_manager import config
from scripts._red.screens.screen_manager import screen_manager
from scripts._red.utils.ui_utils import ui_scale, ui_scale_dimensions
from scripts.game_structure import image_cache
from scripts.game_structure.audio import music_manager
from scripts.game_structure.game_essentials import game
from scripts.ui.ui_elements import UIImageButton

import resources._red.red_filepaths as fp
from scripts.game_structure.propagating_thread import PropagatingThread
from scripts._red.screens.windows import EventLoading, SaveCheck

import logging

logger = logging.getLogger(__name__)


########################################################################################################################
# Constants
########################################################################################################################

BACKGROUND_TRANSITION_TIME_S: int = 5 # FIXME move this to definitions.py


########################################################################################################################
# Classes
########################################################################################################################

class RedBaseScreen:
    """ The base class for all screens. """

    name: ScreenName = ScreenName.ScreenUnset
    screen_buttons: dict[str, pygame_gui.elements.UIButton] # don't use = {} here or all classes that inherit from this
                                                            # one will share their screen_buttons dictionary

    bg_transition_effect_f: bool = False
    bg_transition_time_s: int = BACKGROUND_TRANSITION_TIME_S

    mns_widget_parts: dict[str, Optional[UIElement]] = {
        "bg": None,
        "moon_icon": None,
        "moon_text": None,
        "season_icon": None,
        "season_text": None
    }
    previous_season: Season = Season.NoSeason

    # used in managing threads
    loading_window: dict = {} # place to store the loading window(s)
    work_done: dict = {} # dictionary of work done, keyed by the target function name

    # only the relevant screens (ProfileScreen, ProfileGenderScreen, ProfileRoleScreen, and ProfileSpriteInspectScreen)
    # implement the method update_previous_next_cat_buttons()

    # only the relevant screens (ProfileScreen, ProfileGenderScreen, ProfileMateScreen, and ProfileFamilyScreen)
    # implement the method set_cat_location_bg()

    # TODO cat_profiles

    # ------------------------------------- INIT ------------------------------------- #

    def __init__(self, name: ScreenName):
        self.name = name
        # screen_manager.curr_screen_name = self.name # TODO should
        game.current_screen_obj = self

        # TODO what are these doing?
        # light_surface_obj = pygame.Surface((screen_manager.window_size_x, screen_manager.window_size_y))
        # light_surface_obj.fill(config.screen_config.windowed_themes[ThemeName.Light])
        # dark_surface_obj = pygame.Surface((screen_manager.window_size_x, screen_manager.window_size_y))
        # dark_surface_obj.fill(config.screen_config.windowed_themes[ThemeName.Dark])

    # ------------------------------------ PUBLIC ------------------------------------ #

    # TODO enter_screen()
    def enter_screen(self):
        """ Called by the screen manager when the game switches TO this screen.

        This used to be BaseScreen.screen_switches().
        """
        logger.debug(f"RedBaseScreen.enter_screen")

        # change the music playing if necessary
        music_manager.check_music(self.name)

        # background
        screen_manager.show_screen_background(screen_name=self.name)

        # buttons
        self.show_mute_buttons()
        self._create_screen_buttons()
        for btn in self.screen_buttons:
            self.screen_buttons[btn].show()

        # BaseScreen.hide_mute_buttons()
        # BaseScreen.hide_menu_buttons()
        # BaseScreen.menu_buttons = scripts.screens.screens_core.screens_core.menu_buttons
        # BaseScreen.game_frame = scripts.screens.screens_core.screens_core.game_frame

        # try:
        #     BaseScreen.update_heading_text(game.clan_obj.name + "Clan")
        # except AttributeError:
        #     BaseScreen.update_heading_text("DebugClan")

        # if self.active_bg is None or "default" in self.active_bg:
        #     self.set_bg(None)

        # self.bg_transition = True
        return

    # TODO exit_screen()
    def exit_screen(self):
        """ Called by the screen manager when the game switches AWAY FROM this screen."""
        logger.debug(f"RedBaseScreen.exit_screen")
        self.hide_menu_buttons()
        self.hide_mute_buttons()
        return

    def on_use(self):
        """ Runs every frame this screen is used. """
        screen_manager.show_screen_background(screen_name=self.name)
        # self.show_bg()
        for btn in self.screen_buttons:
            self.screen_buttons[btn].show()
        return

    def handle_event(self, event):
        """ This is where events that occur on this screen are handled.
        For the pygame_gui rewrite, button presses are also handled here.
        """
        logger.debug(f"RedBaseScreen.handle_event")
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            success: bool = self.mute_button_pressed(event)
            # FIXME this returns None either way
            if success:
                return

    # -------------------------------- LOADING METHODS ------------------------------- #

    def loading_screen_start_work(
            self, target: Callable, thread_name: str = "work_thread", args: tuple = tuple()
    ) -> PropagatingThread:
        """ Creates and starts the work_thread.

        :return PropagatingThread: the started thread
        """
        logger.debug(f"RedBaseScreen.loading_screen_start_work")
        work_thread = PropagatingThread(
            target=self._work_target, args=(target, args), name=thread_name, daemon=True
        )

        work_thread.start()

        return work_thread

    def loading_screen_on_use(
        self,
        work_thread: PropagatingThread,
        final_actions: Callable,
        loading_screen_pos: tuple = None,
        delay: float = LOADING_SCREEN_DELAY_SEC,
    ) -> None:
        """
        Handles all actions that must be run every frame for the loading window to work.
        Also handles creating and killing the loading window.
        """
        logger.debug(f"RedBaseScreen.loading_screen_on_use")
        if not isinstance(work_thread, PropagatingThread):
            return

        # Handled the loading animation, both creating and killing it.
        if (
            not self.loading_window.get(work_thread.name)
            and work_thread.is_alive()
            and work_thread.get_time_from_start() > delay
        ):
            self.loading_window[work_thread.name] = EventLoading(loading_screen_pos)
        elif self.loading_window.get(work_thread.name) and not work_thread.is_alive():
            self.loading_window[work_thread.name].kill()
            self.loading_window.pop(work_thread.name)

        # Handles displaying the events once timeskip is done.
        if self.work_done.get(work_thread.name, False):
            # By this time, the thread should have already finished.
            # This line allows exceptions in the work thread to be
            # passed to the main thread, so issues in the work thread are not
            # silent failures.
            work_thread.join()

            self.work_done.pop(work_thread.name)

            final_actions()

        return

    def _work_target(self, target, args):
        logger.debug(f"RedBaseScreen._work_target")
        exp = None
        try:
            target(*args)
        except Exception as e:
            raise e
        finally:
            self.work_done[current_thread().name] = True

    # ------------------------------ BACKGROUNDS METHODS ----------------------------- #

    # TODO add_bgs
    #  used in two screens: the ClanCamp and the ClanMembers screens
    # FIXME this should be deleted
    # RedBaseScreen.add_bgs() is now ScreenManager.build_bg_surfaces()
    def add_custom_bgs(
        self,
        bgs: dict[ScreenBackground, pygame.Surface],
        blur_bgs: dict[ScreenBackground, Optional[pygame.Surface]] = None,
        radius: int = 5,
        vignette_alpha: int = None,
    ):
        """
        Add custom backgrounds to the Screen.

        Used to be add_bgs.

        :param dict bgs: A dictionary of ScreenNames and Surfaces representing the game window background
        :param dict blur_bgs: A dictionary of ScreenNames and Surfaces/None representing the fullscreen backdrop.
            If a key is supplied with a None value, the default clan season background will be used.
            If no matching key is supplied, the input bg will be appropriately scaled and blurred to fit. Optional.
        :param int radius: If a bg is missing a corresponding blur_bg value, this value determines how much
            to blur the bg to make the background. Default 10.
        :param int vignette_alpha: Change the strength of the vignette. Value must be between 0 and 255.
            Default 0 (disabled/none).
        :return: None
        """
        logger.debug(f"RedBaseScreen.add_custom_bgs")
        # initialise the vignette strength
        # vignette = screen_manager.vignette_surface_obj
        if vignette_alpha is None:
            vignette_alpha = config.screen_config.themes[config.settings.Theme]["vignette_alpha"]
        if not (0 <= vignette_alpha <= 255):
            raise ValueError(f"Vignette alpha out of range for theme {config.settings.Theme}. Permitted value range "
                                 f"is 0-255, but the given value was {vignette_alpha}.")
        screen_manager.vignette_surface_obj.set_alpha(vignette_alpha)

        # # add the bg to the game bgs # TODO
        # for name, bg in bgs.items():
        #     screen_manager.game_bgs = pygame.transform.scale((DEFAULT_WINDOW_SIZE_X, DEFAULT_WINDOW_SIZE_Y))
        #
        #     # if blur_bgs exists
        #     if blur_bgs is not None and name in blur_bgs:
        #         if blur_bgs[name] is None:
        #             self.fullscreen_bgs[name] = "default"
        #             continue
        #
        #         # there's an input blur_bg here, so scale it
        #         self.fullscreen_bgs[
        #             name
        #         ] = scripts.screens.screens_core.screens_core.process_blur_bg(
        #             blur_bgs[name], blur_radius=0, vignette_strength=vignette_alpha
        #         )
        #         continue

        #     # no blur_bg, so blur the input bg to become the fullscreen backing
        #     # also blit the vignette & game frame over the top of that for performance
        #     screen_manager.default_fullscreen_bgs[name]
        #     self.fullscreen_bgs[
        #         name
        #     ] = scripts.screens.screens_core.screens_core.process_blur_bg(
        #         bg, blur_radius=radius, vignette_strength=vignette_alpha
        #     )

        raise NotImplementedError("RedBaseScreen.add_bgs")

    # TODO show_bg - this is now screen_manager.set_screen_background()
    #  only used in RedBaseScreen.on_use()
    def show_bg(self, theme: ThemeName = config.settings.Theme):
        """ Blit the currently selected blur_bg and bg. Must be called somewhere in on_use.

        :param theme: Allows overriding the displayed theme (dark/light mode).
        """
        logger.debug(f"RedBaseScreen.show_bg")
        try:
            season = game.current_season
        except AttributeError as e:
            # took this out to prevent log spam because show_bg is called every frame
            # logger.warning(f"Couldn't access game.current_season in RedBaseScreen.show_bg()! Defaulting to spring")
            season = Season.Spring
        season_bg_obj = screen_manager.default_fullscreen_bgs[season] # season_bg

        # handle non-default backgrounds
        # if self.active_bg in self.game_bgs:
        #     bg = self.game_bgs[self.active_bg]
        # # handle default screen backgrounds
        # elif (
        #     self.active_bg
        #     in scripts.screens.screens_core.screens_core.default_game_bgs[theme]
        # ):
        #     bg = scripts.screens.screens_core.screens_core.default_game_bgs[theme][
        #         self.active_bg
        #     ]
        # else:
        #     raise Exception(
        #         f"Selected game background not recognised! '{self.active_bg}' not in default or custom bgs"
        #     )
        #
        # if self.active_blur_bg == "default" or self.active_blur_bg == season:
        #     blur_bg = season_bg
        # elif self.name in [
        #     "start screen",
        #     "settings screen",
        #     "switch clan screen",
        # ]:
        #     # if we're in the main menu levels, display the main menu bg
        #     blur_bg = scripts.screens.screens_core.screens_core.default_fullscreen_bgs[theme]["mainmenu_bg"]
        # elif self.active_blur_bg in self.fullscreen_bgs:
        #     blur_bg = self.fullscreen_bgs[self.active_blur_bg]
        # elif (
        #     self.active_blur_bg
        #     in scripts.screens.screens_core.screens_core.default_fullscreen_bgs[theme]
        # ):
        #     blur_bg = scripts.screens.screens_core.screens_core.default_fullscreen_bgs[theme][self.active_blur_bg]
        # else:
        #     raise Exception(
        #         f"Selected fullscreen background not recognised! '{self.active_blur_bg}' not in default or custom bgs"
        #     )
        #
        # if (
        #     self.previous_season != season
        #     and self.active_blur_bg == "default"
        #     or self.active_blur_bg == season
        # ):
        #     self.bg_transition_time = 10  # doubled transition time for the Vibes
        #     self.previous_season = season
        # # onto the actual blitting
        # # handle the blur bg
        # if (
        #     scripts.game_structure.screen_settings.game_screen_size
        #     != scripts.game_structure.screen_settings.screen.get_size()
        # ):
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
        # # now blit the foreground.
        # scripts.game_structure.screen_settings.screen.blit(bg, ui_scale_blit((0, 0)))

        raise NotImplementedError("RedBaseScreen.show_bg")

    # only the relevant screens (ProfileScreen, ProfileGenderScreen, ProfileMateScreen, and ProfileFamilyScreen)
    # implement the method set_cat_location_bg()
    # FIXME
    # def set_cat_location_bg(self, cat_obj, bg_name: ScreenBackground):
    #     """ """
    #     logger.debug(f"RedBaseScreen.set_cat_location_bg")
    #     if not cat_obj.alive and not cat_obj.faded:
    #         self.set_bg(bg_name=bg_name, blur_bg=cat_obj.location.afterlife_screen_background)
    #     else:
    #         self.set_bg(bg_name=bg_name)
    #     return


    # -------------------------- SCREEN INFORMATION METHODS -------------------------- #

    # display_change_save
    def get_screen_info(self) -> dict:
        """ Get a dictionary of data to help rebuild the screen the way it was when we return.

        :return dict: a dictionary of data to be used later to rebuild the screen
        """
        logger.debug(f"RedBaseScreen.get_screen_info")
        # the HTML text reads "*Clan*"
        return {UIElementPath.ClanNameHeader: screen_manager.menu_buttons[UIElementPath.ClanNameHeader].html_text}

    # display_change_load
    def set_screen_info(self, info: dict):
        """ Load a screen back to how it was following a display (e.g. fullscreen mode) change. """
        logger.debug(f"RedBaseScreen.set_screen_info")
        try:
            # this is "*Clan*"
            screen_manager.menu_buttons[UIElementPath.ClanNameHeader].set_text(info.pop(UIElementPath.ClanNameHeader))
        except KeyError:
            pass

    def update_heading_text(self, text, text_kwargs=None):
        """ Updates the menu heading text. """
        logger.debug(f"RedBaseScreen.update_heading_text")
        screen_manager.menu_buttons[UIElementPath.ClanNameHeader].set_text(text, text_kwargs=text_kwargs)

    # -------------------------------- BUTTON METHODS -------------------------------- #

    # Functions to deal with the menu and mute button.
    #   The menu is used very often, so I don't want to keep
    #   recreating and killing it. Lots of chances for bugs there.

    def hide_mute_buttons(self):
        """This hides the mute buttons, so they are no longer visible
        or interact-able. It does not delete the buttons from memory."""
        logger.debug(f"RedBaseScreen.hide_mute_buttons")
        screen_manager.menu_buttons[UniversalButtonName.Mute].hide()
        screen_manager.menu_buttons[UniversalButtonName.Unmute].hide()

    def show_mute_buttons(self):
        """ This shows all mute buttons, and makes them interact-able. """
        logger.debug(f"RedBaseScreen.show_mute_buttons")
        if music_manager.muted_f or music_manager.audio_disabled_f:
            screen_manager.menu_buttons[UniversalButtonName.Unmute].show()
            screen_manager.menu_buttons[UniversalButtonName.Mute].hide()
        else:
            screen_manager.menu_buttons[UniversalButtonName.Unmute].hide()
            screen_manager.menu_buttons[UniversalButtonName.Mute].show()

    # TODO raise an error if this hasn't been overwritten
    @abstractmethod
    def _create_screen_buttons(self):
        """ Every class which inherits from RedBaseScreen needs to implement this method. """

    # FIXME this will also hide mute buttons, etc.
    def hide_menu_buttons(self):
        """ This hides all menu buttons, so they are no longer visible
        or interactable. It does not delete the buttons from memory. """
        logger.debug(f"RedBaseScreen.hide_menu_buttons")
        for button in screen_manager.menu_buttons.values():
            button.hide()

    def show_menu_buttons(self, buttons: list[SwitchScreenButtonName]):
        """ This shows menu buttons, and makes them interact-able. """
        logger.debug(f"RedBaseScreen.show_menu_buttons")
        # Check if the setting for moons and seasons UI is on so stats button can be moved # TODO stats button?
        self.update_mns_widget()

        for button_name in buttons:
            if button_name in screen_manager.menu_buttons:
                screen_manager.menu_buttons[button_name].show()

        # for name, button in screen_manager.menu_buttons.items():
        #     if name is UniversalButtonName.DropdownDens:
        #         pass # TODO do I want to keep the dens dropdown?
        #         if config.settings.ShowMoonSeasonWidget and screen_manager.curr_screen_name is ScreenName.Events:
        #             button.show()
        #         elif not config.settings.ShowMoonSeasonWidget \
        #             and screen_manager.curr_screen_name is not ScreenName.Events:
        #             button.show()
        #         button.hide() # FIXME should this be behind an else: ?
        #     if name in [
        #         UniversalButtonName.MoonsSeasonsArrow,
        #         UIElementPath.MoonsSeasonsWidget,
        #         UniversalButtonName.DropdownDens,
        #         SwitchScreenButtonName.GoScreenLeaderDen,
        #         SwitchScreenButtonName.GoScreenHealerDen,
        #         SwitchScreenButtonName.GoScreenWarriorDen,
        #         SwitchScreenButtonName.GoScreenFreshkillPile,
        #         UIElementPath.DropdownDensBar,
        #         UniversalButtonName.Mute,
        #         UniversalButtonName.Unmute
        #     ]:
        #         continue
        #     else:
        #         button.show()

        return

    # TODO use this to disable "Switch Clan" if there's no other save files, for example
    def disable_menu_buttons(self, disabled_button_names=()):
        """ This sets all menu buttons as interact-able, except buttons listed in disabled_buttons.

        This used to be BaseScreen.set_disabled_menu_buttons().

        :param set[SwitchScreenButtonName] disabled_button_names: names of buttons to disabled
        """
        logger.debug(f"RedBaseScreen.disable_menu_buttons")
        for name, button in screen_manager.menu_buttons.items():
            button.disable() if name in disabled_button_names else button.enable()

    def menu_button_pressed(self, event):
        """ This is a short-up to deal with menu button presses.

        This will fail if event.type != pygame_gui.UI_BUTTON_START_PRESS.
        """
        logger.debug(f"RedBaseScreen.menu_button_pressed")
        # if the player is trying to quit to the main menu, ask if they want to save first
        if event.ui_element is screen_manager.menu_buttons[SwitchScreenButtonName.GoScreenMainMenu]:
            SaveCheck(is_main_menu=True)

        # update the Moon & Seasons widget
        elif event.ui_element is screen_manager.menu_buttons[UniversalButtonName.MoonsSeasonsArrow]:
            screen_manager.mns_widget_open_f = not screen_manager.mns_widget_open_f
            self.update_mns_widget()

        elif event.ui_element is screen_manager.menu_buttons[UniversalButtonName.DropdownDens]:
            self.toggle_dens_dropdown()

        else:
            screen_manager.queue_screen_switch(event.ui_element.go_to_screen_name)

        return

    def mute_button_pressed(self, event) -> bool:
        """ This is a short-up to deal with mute button presses.
        This will fail if event.type != pygame_gui.UI_BUTTON_START_PRESS
        """
        logger.debug(f"RedBaseScreen.mute_button_pressed")
        if event.ui_element is screen_manager.menu_buttons[UniversalButtonName.Mute]:
            music_manager.mute_music()
            self.show_mute_buttons()
            return True
        elif event.ui_element is screen_manager.menu_buttons[UniversalButtonName.Unmute]:
            success = music_manager.unmute_music(self.name)
            self.show_mute_buttons()
            return success
        else:
            return False

    # TODO set_mute_button_position
    #   I got rid of this because it's only used once - for the NewClan screen (which is the only screen where
    #   the mute button is in a unique position). I'll figure that out, maybe by relocating the button in NewClan's
    #   enter_screen() method and moving it back in exit_screen()?

    def toggle_dens_dropdown(self):
        """ Toggle whether the dens dropdown menu is open or closed.

        Used to be BaseScreen.update_dens().
        """
        logger.debug(f"RedBaseScreen.toggle_dens_dropdown")
        den_bar_components: list = [
            UIElementPath.DropdownDensBar,
            SwitchScreenButtonName.GoScreenLeaderDen,
            SwitchScreenButtonName.GoScreenHealerDen,
            SwitchScreenButtonName.GoScreenWarriorDen,
            SwitchScreenButtonName.GoScreenFreshkillPile
        ]
        for comp in den_bar_components:
            # if dropdown is visible, hide
            if screen_manager.menu_buttons[comp].visible:
                screen_manager.menu_buttons[comp].hide()
            else:
                if config.settings.GameMode is not GameMode.Classic:
                    screen_manager.menu_buttons[comp].show()
                elif comp is SwitchScreenButtonName.GoScreenFreshkillPile:
                    if screen_manager.menu_buttons[UIElementPath.DropdownDensBar].get_relative_rect()[2:] != [10, 125]:
                        # redraw this to be shorter
                        screen_manager.menu_buttons[UIElementPath.DropdownDensBar].kill()
                        screen_manager.menu_buttons[UIElementPath.DropdownDensBar] = pygame_gui.elements.UIImage(
                            relative_rect=ui_scale( rect=pygame.Rect((40, 60), (10, 125)),
                                                    scale=screen_manager.window_scale ),
                            image_surface=pygame.transform.scale(
                                surface=image_cache.load_image(fp.BAR_VERTICAL).convert_alpha(),
                                size=ui_scale_dimensions(dim=(10, 125), scale=screen_manager.window_scale),
                            ),
                            visible=True, # TODO change this if I want to get rid of the dens dropdown
                            starting_height=1,
                            manager=screen_manager.uim,
                        )
                    else:
                        screen_manager.menu_buttons[comp].show()
        return

    def mns_ui_offset(self, x_shift, y_shift):
        """ Shifts the dens UI by the given amount - needed for positioning around the Moons and Seasons widget. """
        logger.debug(f"RedBaseScreen.mns_ui_offset")
        # close the UI components before moving them
        try:
            screen_manager.menu_buttons[UniversalButtonName.DropdownDens].kill()
            screen_manager.menu_buttons[UIElementPath.DropdownDensBar].kill()
            screen_manager.menu_buttons[SwitchScreenButtonName.GoScreenLeaderDen].kill()
            screen_manager.menu_buttons[SwitchScreenButtonName.GoScreenWarriorDen].kill()
            screen_manager.menu_buttons[SwitchScreenButtonName.GoScreenFreshkillPile].kill()
            screen_manager.menu_buttons[SwitchScreenButtonName.GoScreenFreshkillPile].kill()
        except:
            logger.warning(f"Something went wrong trying to shift the Moons & Seasons widget - "
                           f"couldn't kill the old objects")

        if y_shift != 0:
            screen_manager.menu_buttons[UIElementPath.DropdownDensBar] = pygame_gui.elements.UIImage(
                relative_rect=ui_scale(rect=pygame.Rect((142 + x_shift, 120 + y_shift), (20, 320)),
                                       scale=screen_manager.window_scale),
                image_surface=pygame.transform.scale(
                    image_cache.load_image(
                        "resources/images/bar_vertical.png").convert_alpha(),
                    (380, 70)),
                visible=False,
                starting_height=5,
                manager=screen_manager.uim)
            screen_manager.menu_buttons[SwitchScreenButtonName.GoScreenLeaderDen] = UIImageButton(
                relative_rect=ui_scale(rect=pygame.Rect((-12 + x_shift, 200 + y_shift), (224, 56)),
                                       scale=screen_manager.window_scale),
                screen_manager=screen_manager,
                text="",
                visible=False,
                manager=screen_manager.uim,
                object_id="#lead_den_button",
                starting_height=6)
            screen_manager.menu_buttons[SwitchScreenButtonName.GoScreenHealerDen] = UIImageButton(
                relative_rect=ui_scale(rect=pygame.Rect((-90 + x_shift, 280 + y_shift), (302, 56)),
                                       scale=screen_manager.window_scale),
                screen_manager=screen_manager,
                text="",
                visible=False,
                manager=screen_manager.uim,
                object_id="#med_den_button",
                starting_height=6)
            screen_manager.menu_buttons[SwitchScreenButtonName.GoScreenWarriorDen] = UIImageButton(
                relative_rect=ui_scale(rect=pygame.Rect((-30 + x_shift, 360 + y_shift), (242, 56)),
                                       scale=screen_manager.window_scale),
                screen_manager=screen_manager,
                text="",
                visible=False,
                manager=screen_manager.uim,
                object_id="#warrior_den_button",
                starting_height=6)
            screen_manager.menu_buttons[SwitchScreenButtonName.GoScreenFreshkillPile] = UIImageButton(
                relative_rect=ui_scale(rect=pygame.Rect((50 + x_shift, 440 + y_shift), (162, 56)),
                                       scale=screen_manager.window_scale),
                screen_manager=screen_manager,
                text="",
                visible=False,
                manager=screen_manager.uim,
                object_id="#clearing_button",
                starting_height=6)
        else:
            screen_manager.menu_buttons[UIElementPath.DropdownDensBar] = pygame_gui.elements.UIImage(
                relative_rect=ui_scale(rect=pygame.Rect((80 + x_shift, 120 + y_shift), (20, 320)), scale=screen_manager.window_scale),
                image_surface=pygame.transform.scale(
                    surface=image_cache.load_image(fp.BAR_VERTICAL).convert_alpha(),
                    size=(380, 70)
                ),
                visible=False,
                starting_height=5,
                manager=screen_manager.uim)
            screen_manager.menu_buttons[SwitchScreenButtonName.GoScreenLeaderDen] = UIImageButton(
                relative_rect=ui_scale(rect=pygame.Rect((50 + x_shift, 200 + y_shift), (224, 56)), scale=screen_manager.window_scale),
                screen_manager=screen_manager,
                text="",
                visible=False,
                manager=screen_manager.uim,
                object_id="#lead_den_button",
                starting_height=6)
            screen_manager.menu_buttons[SwitchScreenButtonName.GoScreenHealerDen] = UIImageButton(
                relative_rect=ui_scale(rect=pygame.Rect((50 + x_shift, 280 + y_shift), (302, 56)), scale=screen_manager.window_scale),
                screen_manager=screen_manager,
                text="",
                visible=False,
                manager=screen_manager.uim,
                object_id="#med_den_button",
                starting_height=6)
            screen_manager.menu_buttons[SwitchScreenButtonName.GoScreenWarriorDen] = UIImageButton(
                relative_rect=ui_scale(rect=pygame.Rect((50 + x_shift, 360 + y_shift), (242, 56)), scale=screen_manager.window_scale),
                screen_manager=screen_manager,
                text="",
                visible=False,
                manager=screen_manager.uim,
                object_id="#warrior_den_button",
                starting_height=6)
            screen_manager.menu_buttons[SwitchScreenButtonName.GoScreenFreshkillPile] = UIImageButton(
                relative_rect=ui_scale(rect=pygame.Rect((50 + x_shift, 440 + y_shift), (162, 56)), scale=screen_manager.window_scale),
                screen_manager=screen_manager,
                text="",
                visible=False,
                manager=screen_manager.uim,
                object_id="#clearing_button",
                starting_height=6)

        if screen_manager.curr_screen_name is not ScreenName.Camp:
            screen_manager.menu_buttons[UniversalButtonName.DropdownDens] = UIImageButton(
                relative_rect=ui_scale(rect=pygame.Rect((50 + x_shift, 120 + y_shift), (142, 60)), scale=screen_manager.window_scale),
                screen_manager=screen_manager,
                text="",
                visible=False,
                manager=screen_manager.uim,
                object_id="#dens_button",
                starting_height=6)

        return

    def update_mns_widget(self):
        """ Toggles the Moons & Season widget.

        Used to be BaseScreen.update_moon_and_season().
        """
        logger.debug(f"RedBaseScreen.update_mns_widget")
        if config.settings.ShowMoonSeasonWidget and screen_manager.curr_screen_name is not ScreenName.Events:
            screen_manager.menu_buttons[UniversalButtonName.MoonsSeasonsArrow].kill()
            screen_manager.menu_buttons[UIElementPath.MoonsSeasonsWidget].kill()
            if config.settings.ShowMoonSeasonWidget or self.name is ScreenName.Events:
                self.close_mns_widget()
            else:
                self.open_mns_widget()

        else:
            screen_manager.menu_buttons[UniversalButtonName.MoonsSeasonsArrow].hide()
            screen_manager.menu_buttons[UIElementPath.MoonsSeasonsWidget].hide()

    def open_mns_widget(self):
        """ Open the Moons & Seasons widget.

        Used to be BaseScreen.open_moon_and_season().
        """
        logger.debug(f"RedBaseScreen.open_mns_widget")
        screen_manager.menu_buttons[UniversalButtonName.MoonsSeasonsArrow] = UIImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((174, 80), (22, 34)), scale=screen_manager.window_scale),
            screen_manager=screen_manager,
            text="",
            manager=screen_manager.uim,
            object_id="#arrow_mns_button")
        screen_manager.menu_buttons[UIElementPath.MoonsSeasonsWidget] = pygame_gui.elements.UIScrollingContainer(
            relative_rect=ui_scale(rect=pygame.Rect((25, 60), (153, 75)), scale=screen_manager.window_scale),
            allow_scroll_x=False,
            manager=screen_manager.uim)
        self.mns_widget_parts["bg"] = UIImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((0, 0), (153, 75)), scale=screen_manager.window_scale),
            screen_manager=screen_manager,
            text="",
            manager=screen_manager.uim,
            object_id="#mns_bg",
            container=screen_manager.menu_buttons[UIElementPath.MoonsSeasonsWidget])
        self.mns_widget_parts["moon_icon"] = UIImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((14, 10), (24, 24)), scale=screen_manager.window_scale),
            screen_manager=screen_manager,
            text="",
            manager=screen_manager.uim,
            object_id="#mns_image_moon",
            container=screen_manager.menu_buttons[UIElementPath.MoonsSeasonsWidget])
        self.mns_widget_parts["moon_text"] = pygame_gui.elements.UITextBox(
            html_text="general.moons_age",
            relative_rect=ui_scale(rect=pygame.Rect((42, 6), (100, 30)), scale=screen_manager.window_scale),
            container=screen_manager.menu_buttons[UIElementPath.MoonsSeasonsWidget],
            manager=screen_manager.uim,
            object_id="#text_box_30_horizleft_light",
            text_kwargs={"count": str(game.current_moon)},)

        if game.current_season.season_image_id is not None:
            season_image_id = game.current_season.season_image_id
        else:
            season_image_id = screen_manager.uim.get_universal_empty_surface()

        self.mns_widget_parts["season_icon"] = UIImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((14, 41), (24, 24)), scale=screen_manager.window_scale),
            screen_manager=screen_manager,
            text="",
            manager=screen_manager.uim,
            object_id=season_image_id,
            container=screen_manager.menu_buttons[UIElementPath.MoonsSeasonsWidget],
        )
        self.mns_widget_parts["season_text"] = pygame_gui.elements.UITextBox(
            html_text=f"general.{game.current_season.lower()}".capitalize(),
            relative_rect=ui_scale(rect=pygame.Rect((42, 36), (100, 30)), scale=screen_manager.window_scale),
            container=screen_manager.menu_buttons[UIElementPath.MoonsSeasonsWidget],
            manager=screen_manager.uim,
            object_id=ObjectID("#text_box_30_horizleft", "#dark"),
        )
        return

    def close_mns_widget(self):
        """ Close the Moons & Seasons widget.

        Used to be BaseScreen.close_moon_and_season().
        """
        logger.debug(f"RedBaseScreen.close_mns_widget")
        screen_manager.menu_buttons[UniversalButtonName.MoonsSeasonsArrow] = UIImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((71, 80), (22, 34)), scale=screen_manager.window_scale),
            screen_manager=screen_manager,
            text="",
            object_id="#arrow_mns_closed_button",
        )
        if self.name is ScreenName.Events:
            screen_manager.menu_buttons[UniversalButtonName.MoonsSeasonsArrow].kill()

        screen_manager.menu_buttons[UIElementPath.MoonsSeasonsWidget] = pygame_gui.elements.UIScrollingContainer(
            relative_rect=ui_scale(rect=pygame.Rect((25, 60), (50, 75)), scale=screen_manager.window_scale),
            allow_scroll_x=False,
            manager=screen_manager.uim)
        self.mns_widget_parts["bg"] = UIImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((0, 0), (50, 75)), scale=screen_manager.window_scale),
            screen_manager=screen_manager,
            text="",
            manager=screen_manager.uim,
            object_id="#mns_bg_closed",
            container=screen_manager.menu_buttons[UIElementPath.MoonsSeasonsWidget])

        self.mns_widget_parts["moon_icon"] = UIImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((14, 10), (24, 24)), scale=screen_manager.window_scale),
            screen_manager=screen_manager,
            text="",
            manager=screen_manager.uim,
            object_id="#mns_image_moon",
            container=screen_manager.menu_buttons[UIElementPath.MoonsSeasonsWidget],
            starting_height=2,
            tool_tip_text=f"general.moons_age",
            tool_tip_text_kwargs={"count": str(game.current_moon)})
        self.mns_widget_parts["moon_text"] = None

        if game.current_season.season_image_id is not None:
            season_image_id = game.current_season.season_image_id
        else:
            season_image_id = screen_manager.uim.get_universal_empty_surface()

        self.mns_widget_parts["season_icon"] = UIImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((14, 41), (24, 24)), scale=screen_manager.window_scale),
            text="",
            manager=screen_manager.uim,
            object_id=season_image_id,
            container=screen_manager.menu_buttons[UIElementPath.MoonsSeasonsWidget],
            starting_height=2,
            tool_tip_text=f"{game.current_season}", # FIXME refer to game.time_manager.curr_season?
            screen_manager=screen_manager
        )
        self.mns_widget_parts["season_text"] = None

        return

