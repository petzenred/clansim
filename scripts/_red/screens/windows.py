import os
import shutil
import subprocess
import threading
import time
from collections import namedtuple
from platform import system
from random import choice
from re import search as re_search
from re import sub

import i18n
import pygame
import pygame_gui
from pygame_gui.elements import UIWindow
from pygame_gui.windows import UIMessageWindow

from definitions import BoxShape, ButtonStyle, ScreenName, Rank, Icon, SwitchScreenButtonName
from scripts._red.config_manager import config

from scripts.game_structure import image_cache
from scripts.game_structure.game_essentials import game
from scripts.game_structure.localization import (
    get_lang_config,
    get_custom_pronouns,
    add_custom_pronouns,
)
from scripts._red.screens.screen_manager import screen_manager
from scripts.ui.ui_elements import (
    UIImageButton,
    UITextBoxTweaked,
    UISurfaceImageButton,
    UIDropDownContainer,
)
from scripts.housekeeping.datadir import (
    get_save_dir,
    get_cache_dir,
    get_saved_images_dir,
    get_data_dir,
)
from scripts.housekeeping.progress_bar_updater import UIUpdateProgressBar
from scripts.housekeeping.update import (
    self_update,
    UpdateChannel,
    get_latest_version_number,
)
from scripts.housekeeping.version import get_version_info
from scripts.ui.generate_box import get_box
from scripts.ui.generate_button import get_button_dict
from scripts._red.utils.ui_utils import (
    ui_scale,
    ui_scale_dimensions,
    ui_scale_offset,
)
from scripts.utility import ( # FIXME
    update_sprite,
    process_text,
)

import logging
logger = logging.getLogger(__name__)


class SymbolFilterWindow(UIWindow):
    def __init__(self):
        super().__init__(
            ui_scale(rect=pygame.Rect((250, 175), (300, 450)), scale=screen_manager.window_scale),
            window_display_title="windows.symbol_filters",
            object_id="#filter_window",
        )
        self.set_blocking(True)

        self.possible_tags = {
            "plant": ["flower", "tree", "leaf", "other plant", "fruit"],
            "animal": ["cat", "fish", "bird", "mammal", "bug", "other animal"],
            "element": ["water", "fire", "earth", "air", "light"],
            "location": [],
            "descriptor": [],
            "miscellaneous": [],
        }

        self.back_button = UIImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((270, 5), (22, 22)), scale=screen_manager.window_scale),
            text="",
            object_id="#exit_window_button",
            starting_height=10,
            container=self,
            screen_manager=screen_manager,
        )
        self.filter_title = pygame_gui.elements.UILabel(
            ui_scale(rect=pygame.Rect((5, 5), (-1, -1)), scale=screen_manager.window_scale),
            text="windows.symbol_filter_title",
            object_id="#text_box_40",
            container=self,
        )
        self.filter_container = pygame_gui.elements.UIScrollingContainer(
            ui_scale(rect=pygame.Rect((5, 45), (285, 310)), scale=screen_manager.window_scale),
            manager=screen_manager.uim,
            starting_height=1,
            object_id="#filter_container",
            allow_scroll_x=False,
            container=self,
        )
        self.checkbox = {}
        self.checkbox_text = {}
        x_pos = 15
        y_pos = 20
        for tag, subtags in self.possible_tags.items():
            self.checkbox[tag] = UIImageButton(
                ui_scale(rect=pygame.Rect((x_pos, y_pos), (34, 34)), scale=screen_manager.window_scale),
                "",
                object_id="@checked_checkbox",
                container=self.filter_container,
                starting_height=2,
                manager=screen_manager.uim,
            )
            if tag in game.switches["disallowed_symbol_tags"]:
                self.checkbox[tag].change_object_id("@unchecked_checkbox")

            self.checkbox_text[tag] = pygame_gui.elements.UILabel(
                ui_scale(rect=pygame.Rect((6, y_pos + 4), (-1, -1)), scale=screen_manager.window_scale),
                text=f"windows.{tag}",
                container=self.filter_container,
                object_id="#text_box_30_horizleft",
                manager=screen_manager.uim,
                anchors={"left_target": self.checkbox[tag]},
            )
            y_pos += 35
            if subtags:
                for s_tag in subtags:
                    self.checkbox[s_tag] = UIImageButton(
                        ui_scale(rect=pygame.Rect((x_pos + 35, y_pos), (34, 34)), scale=screen_manager.window_scale),
                        "",
                        object_id="@checked_checkbox",
                        container=self.filter_container,
                        starting_height=2,
                        manager=screen_manager.uim,
                        screen_manager=screen_manager,
                    )

                    if tag in game.switches["disallowed_symbol_tags"]:
                        self.checkbox[s_tag].disable()
                    if s_tag in game.switches["disallowed_symbol_tags"]:
                        self.checkbox[s_tag].change_object_id("@unchecked_checkbox")

                    self.checkbox_text[s_tag] = pygame_gui.elements.UILabel(
                        ui_scale(rect=pygame.Rect((6, y_pos + 4), (-1, -1)), scale=screen_manager.window_scale),
                        text=f"windows.{s_tag}",
                        container=self.filter_container,
                        object_id="#text_box_30_horizleft",
                        manager=screen_manager.uim,
                        screen_manager=screen_manager,
                        anchors={"left_target": self.checkbox[s_tag]},
                    )
                    y_pos += 30
                y_pos += 5

    def process_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.back_button:
                self.kill()

            elif event.ui_element in self.checkbox.values():
                for tag, element in self.checkbox.items():
                    if element == event.ui_element:
                        # find out what state the checkbox was in when clicked
                        object_ids = element.get_object_ids()
                        # handle checked checkboxes becoming unchecked
                        if "@checked_checkbox" in object_ids:
                            self.checkbox[tag].change_object_id("@unchecked_checkbox")
                            # add tag to disallowed list
                            if tag not in game.switches["disallowed_symbol_tags"]:
                                game.switches["disallowed_symbol_tags"].append(tag)
                            # if tag had subtags, also add those subtags
                            if tag in self.possible_tags:
                                for s_tag in self.possible_tags[tag]:
                                    self.checkbox[s_tag].change_object_id(
                                        "@unchecked_checkbox"
                                    )
                                    self.checkbox[s_tag].disable()
                                    if (
                                        s_tag
                                        not in game.switches["disallowed_symbol_tags"]
                                    ):
                                        game.switches["disallowed_symbol_tags"].append(
                                            s_tag
                                        )

                        # handle unchecked checkboxes becoming checked
                        elif "@unchecked_checkbox" in object_ids:
                            self.checkbox[tag].change_object_id("@checked_checkbox")
                            # remove tag from disallowed list
                            if tag in game.switches["disallowed_symbol_tags"]:
                                game.switches["disallowed_symbol_tags"].remove(tag)
                            # if tag had subtags, also add those subtags
                            if tag in self.possible_tags:
                                for s_tag in self.possible_tags[tag]:
                                    self.checkbox[s_tag].change_object_id(
                                        "@checked_checkbox"
                                    )
                                    self.checkbox[s_tag].enable()
                                    if s_tag in game.switches["disallowed_symbol_tags"]:
                                        game.switches["disallowed_symbol_tags"].remove(
                                            s_tag
                                        )
        return super().process_event(event)

# TODO
class SaveCheck(UIWindow):
    def __init__(self, is_main_menu):
        if game.is_close_menu_open:
            return
        game.is_close_menu_open = True
        super().__init__(
            ui_scale(rect=pygame.Rect((250, 200), (300, 200)), scale=screen_manager.window_scale),
            window_display_title="Save Check",
            object_id="#save_check_window",
            resizable=False,
            always_on_top=True,
        )
        self.set_blocking(True)

        self.clan_obj = game.cat_tracker.get_clan_object(clan_token=game.active_clan_token)
        if self.clan_obj:
            self.clan_name = f"{game.active_clan_token}Clan"
        else:
            self.clan_name = "Undefined"
        self.isMainMenu = is_main_menu
        self.mm_btn = screen_manager.menu_buttons[SwitchScreenButtonName.GoScreenMainMenu]
        # adding a variable for starting_height to make sure that this menu is always on top
        top_stack_menu_layer_height = 10000
        if self.isMainMenu:
            self.mm_btn.disable()
            self.main_menu_button = UISurfaceImageButton(
                ui_scale(rect=pygame.Rect((0, 155), (152, 30)), scale=screen_manager.window_scale),
                i18n.t("buttons.main_menu_lower"),
                get_button_dict(ButtonStyle.SquOval, (152, 30), scale=screen_manager.window_scale),
                manager=screen_manager.uim,
                object_id="@ButtonStyle_squoval",
                starting_height=top_stack_menu_layer_height,
                container=self,
                anchors={"centerx": "centerx"},
                screen_manager=screen_manager,
            )
        else:
            self.main_menu_button = UISurfaceImageButton(
                ui_scale(rect=pygame.Rect((0, 155), (152, 30)), scale=screen_manager.window_scale),
                "buttons.quit_game",
                get_button_dict(ButtonStyle.SquOval, (152, 30), scale=screen_manager.window_scale),
                manager=screen_manager.uim,
                object_id="@ButtonStyle_squoval",
                starting_height=top_stack_menu_layer_height,
                container=self,
                anchors={"centerx": "centerx"},
                screen_manager=screen_manager,
            )
        self.game_over_message = UITextBoxTweaked(
            html_text="windows.save_check_message",
            relative_rect=ui_scale(rect=pygame.Rect((20, 20), (260, -1)), scale=screen_manager.window_scale),
            line_spacing=1,
            object_id="#text_box_30_horizcenter",
            container=self,
            screen_manager=screen_manager,
        )
        save_buttons: dict[str, pygame.Surface] = get_button_dict(ButtonStyle.SquOval, (114, 30),
                                                                  scale=screen_manager.window_scale)
        save_buttons["normal"] = image_cache.load_image(
            "resources/images/buttons/save_clan.png"
        )
        self.save_button = UISurfaceImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((0, 115), (114, 30)), scale=screen_manager.window_scale),
            text="buttons.save_clan",
            image_dict=save_buttons,
            object_id="@ButtonStyle_squoval",
            sound_id="save",
            starting_height=top_stack_menu_layer_height,
            container=self,
            anchors={"centerx": "centerx"},
            screen_manager=screen_manager,
        )
        self.save_button_saved_state = UISurfaceImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((0, 115), (114, 30)), scale=screen_manager.window_scale),
            text="buttons.clan_saved",
            image_dict={
                "normal": pygame.transform.scale(
                    image_cache.load_image("resources/images/save_clan_saved.png"), # FIXME
                    ui_scale_dimensions((114, 30)),
                )
            },
            starting_height=top_stack_menu_layer_height + 2,
            container=self,
            object_id="@ButtonStyle_squoval",
            anchors={"centerx": "centerx"},
            screen_manager=screen_manager,
        )
        self.save_button_saved_state.hide()
        self.save_button_saving_state = UISurfaceImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((0, 115), (114, 30)), scale=screen_manager.window_scale),
            text="buttons.saving",
            image_dict={"normal": get_button_dict(ButtonStyle.SquOval, (114, 30),
                                                  scale=screen_manager.window_scale)["normal"]},
            object_id="@ButtonStyle_squoval",
            starting_height=top_stack_menu_layer_height + 1,
            container=self,
            anchors={"centerx": "centerx"},
            screen_manager=screen_manager,
        )
        self.save_button_saving_state.disable()
        self.save_button_saving_state.hide()

        self.back_button = UIImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((270, 5), (22, 22)), scale=screen_manager.window_scale),
            text="",
            object_id="#exit_window_button",
            starting_height=top_stack_menu_layer_height,
            container=self,
            screen_manager=screen_manager,
        )

        self.back_button.enable()
        self.main_menu_button.enable()
        self.set_blocking(True)

    def process_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.main_menu_button:
                if self.isMainMenu:
                    game.is_close_menu_open = False
                    self.mm_btn.enable()
                    # FIXME - use screen_manager instead of game.switches, game.switch_screens
                    game.last_screen_forupdate = game.switches["cur_screen"]
                    game.switches["cur_screen"] = ScreenName.MainMenu
                    game.switch_screens = True
                    self.kill()
                else:
                    game.is_close_menu_open = False
                    game.quit(savesettings=False, clearevents=False)
            elif event.ui_element == self.save_button:
                if self.clan_obj is not None:
                    self.save_button_saving_state.show()
                    self.save_button.disable()
                    game.save_cats()
                    self.clan_obj.save()
                    game.save_events()
                    self.save_button_saving_state.hide()
                    self.save_button_saved_state.show()
            elif event.ui_element == self.back_button:
                game.is_close_menu_open = False
                self.kill()
                if self.isMainMenu:
                    self.mm_btn.enable()

                # only allow one instance of this window
        return super().process_event(event)


class DeleteCheck(UIWindow):
    def __init__(self, reloadscreen, clan_name):
        super().__init__(
            ui_scale(rect=pygame.Rect((250, 200), (300, 180)), scale=screen_manager.window_scale),
            window_display_title="Delete Check",
            object_id="#delete_check_window",
            resizable=False,
        )
        self.set_blocking(True)
        self.active_clan_prefix = clan_name
        self.reloadscreen = reloadscreen

        self.delete_check_message = UITextBoxTweaked(
            html_text="windows.delete_check_message",
            relative_rect=ui_scale(rect=pygame.Rect((20, 20), (260, -1)), scale=screen_manager.window_scale),
            line_spacing=1,
            object_id="#text_box_30_horizcenter",
            container=self,
            text_kwargs={"clan": str(self.active_clan_prefix + "Clan")}, # FIXME use RedClan.clan_name instead
            screen_manager=screen_manager,
        )

        self.delete_it_button = UISurfaceImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((71, 100), (153, 30)), scale=screen_manager.window_scale),
            text="windows.delete_yes",
            image_dict=get_button_dict(ButtonStyle.SquOval, (153, 30),
                                       scale=screen_manager.window_scale),
            object_id="@ButtonStyle_squoval",
            container=self,
            screen_manager=screen_manager,
        )
        self.go_back_button = UISurfaceImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((71, 145), (153, 30)), scale=screen_manager.window_scale),
            text="windows.delete_no",
            image_dict=get_button_dict(ButtonStyle.SquOval, (153, 30),
                                       scale=screen_manager.window_scale),
            object_id="@ButtonStyle_squoval",
            container=self,
            screen_manager=screen_manager,
        )

        self.back_button = UIImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((270, 5), (22, 22)), scale=screen_manager.window_scale),
            text="",
            object_id="#exit_window_button",
            container=self,
            screen_manager=screen_manager,
        )

        self.back_button.enable()

        self.go_back_button.enable()
        self.delete_it_button.enable()

    def process_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.delete_it_button:
                rempath = get_save_dir() + "/" + self.active_clan_prefix # FIXME
                shutil.rmtree(rempath)
                # FIXME JSON bs
                if os.path.exists(rempath + "clan.json"):
                    os.remove(rempath + "clan.json")
                elif os.path.exists(rempath + "clan.txt"):
                    os.remove(rempath + "clan.txt")
                else:
                    print("No clan.json/txt???? Clan prolly wasnt initalized kekw")
                self.kill()
                self.reloadscreen(ScreenName.SwitchClan)

            elif event.ui_element == self.go_back_button:
                self.kill()
            elif event.ui_element == self.back_button:
                game.is_close_menu_open = False
                self.kill()
        return super().process_event(event)


class GameOver(UIWindow):
    def __init__(self, last_screen):
        super().__init__(
            ui_scale(rect=pygame.Rect((250, 200), (300, 180)), scale=screen_manager.window_scale),
            window_display_title="Game Over",
            object_id="#game_over_window",
            resizable=False,
        )
        self.set_blocking(True)
        self.clan_name = str(game.active_clan_token + "Clan")
        self.last_screen = last_screen
        self.game_over_message = UITextBoxTweaked(
            html_text="windows.game_over_message",
            relative_rect=ui_scale(rect=pygame.Rect((20, 20), (260, -1)), scale=screen_manager.window_scale),
            line_spacing=1,
            object_id="",
            container=self,
            text_kwargs={"clan": self.clan_name},
            screen_manager=screen_manager,
        )

        self.game_over_message = UITextBoxTweaked(
            screen_manager=screen_manager,
            html_text="windows.game_over_leave_message",
            relative_rect=ui_scale(rect=pygame.Rect((20, 155), (260, -1)), scale=screen_manager.window_scale),
            line_spacing=0.8,
            object_id="#text_box_22_horizcenter",
            container=self,
        )

        self.begin_anew_button = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((25, 115), (111, 30)), scale=screen_manager.window_scale),
            text="windows.begin_anew",
            image_dict=get_button_dict(ButtonStyle.SquOval, (111, 30),
                                       scale=screen_manager.window_scale),
            object_id="@ButtonStyle_squoval",
            container=self,
        )
        self.not_yet_button = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((159, 115), (111, 30)), scale=screen_manager.window_scale),
            text="windows.not_yet",
            image_dict=get_button_dict(ButtonStyle.SquOval, (111, 30),
                                       scale=screen_manager.window_scale),
            object_id="@ButtonStyle_squoval",
            container=self,
        )

        self.not_yet_button.enable()
        self.begin_anew_button.enable()

    def process_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.begin_anew_button:
                game.last_screen_forupdate = game.switches["cur_screen"] # FIXME
                game.switches["cur_screen"] = ScreenName.MainMenu
                game.switch_screens = True
                self.kill()
            elif event.ui_element == self.not_yet_button:
                self.kill()
        return super().process_event(event)


class ChangeCatName(UIWindow):
    """This window allows the user to change the cat's name"""

    def __init__(self, cat_obj):
        super().__init__(
            ui_scale(rect=pygame.Rect((300, 215), (400, 185)), scale=screen_manager.window_scale),
            window_display_title="Change Cat Name",
            object_id="#change_cat_name_window",
            resizable=False,
        )
        self.the_cat = cat_obj
        self.back_button = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((370, 5), (22, 22)), scale=screen_manager.window_scale),
            text="",
            object_id="#exit_window_button",
            container=self,
        )
        self.clan_obj = game.cat_tracker.get_clan_object(clan_token=game.active_clan_token)

        self.specsuffic_hidden = self.the_cat.name.special_suffix_hidden_f

        self.heading = pygame_gui.elements.UITextBox(
            html_text="windows.change_name_title",
            relative_rect=ui_scale(rect=pygame.Rect((0, 10), (400, 40)), scale=screen_manager.window_scale),
            object_id="#text_box_30_horizcenter",
            manager=screen_manager.uim,
            container=self,
            text_kwargs={"name": self.the_cat.name},
        )

        self.name_changed = pygame_gui.elements.UITextBox(
            html_text="windows.name_changed",
            relative_rect=ui_scale(rect=pygame.Rect((245, 130), (400, 40)), scale=screen_manager.window_scale),
            visible=False,
            object_id="#text_box_30_horizleft",
            manager=screen_manager.uim,
            container=self,
        )

        self.done_button = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((161, 145), (77, 30)), scale=screen_manager.window_scale),
            text="buttons.done_lower",
            image_dict=get_button_dict(ButtonStyle.SquOval, (77, 30),
                                       scale=screen_manager.window_scale),
            object_id="@ButtonStyle_squoval",
            manager=screen_manager.uim,
            container=self,
        )

        x_pos, y_pos = 37, 17

        self.prefix_entry_box = pygame_gui.elements.UITextEntryLine(
            ui_scale(rect=pygame.Rect((0 + x_pos, 50 + y_pos), (120, 30)), scale=screen_manager.window_scale),
            initial_text=self.the_cat.name.prefix,
            manager=screen_manager.uim,
            container=self,
        )

        self.randomize_prefix = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((122 + x_pos, 48 + y_pos), (34, 34)), scale=screen_manager.window_scale),
            text=Icon.DICE,
            image_dict=get_button_dict(ButtonStyle.Icon, (34, 34),
                                       scale=screen_manager.window_scale),
            object_id="@ButtonStyle_icon",
            manager=screen_manager.uim,
            container=self,
            tool_tip_text="Randomize the prefix",
            sound_id="dice_roll",
        )

        self.randomize_suffix = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((281 + x_pos, 48 + y_pos), (34, 34)), scale=screen_manager.window_scale),
            text=Icon.DICE,
            image_dict=get_button_dict(ButtonStyle.Icon, (34, 34),
                                       scale=screen_manager.window_scale),
            object_id="@ButtonStyle_icon",
            manager=screen_manager.uim,
            container=self,
            tool_tip_text="Randomize the suffix",
            sound_id="dice_roll",
        )

        self.toggle_spec_block_on = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((202 + x_pos, 80 + y_pos), (34, 34)), scale=screen_manager.window_scale),
            text="",
            object_id="@unchecked_checkbox",
            tool_tip_text="windows.remove_spec_block",
            manager=screen_manager.uim,
            container=self,
        )

        self.toggle_spec_block_off = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((202 + x_pos, 80 + y_pos), (34, 34)), scale=screen_manager.window_scale),
            text="",
            object_id="@checked_checkbox",
            tool_tip_text="windows.add_spec_block",
            manager=screen_manager.uim,
            container=self,
        )

        if self.the_cat.rank in list(self.the_cat.name.special_ranks.keys()):
            self.suffix_entry_box = pygame_gui.elements.UITextEntryLine(
                ui_scale( pygame.Rect((159 + x_pos, 50 + y_pos), (120, 30)), scale=screen_manager.window_scale ),
                placeholder_text=self.the_cat.name.special_ranks[self.the_cat.rank],
                manager=screen_manager.uim,
                container=self,
            )
            if not self.the_cat.name.special_suffix_hidden_f:
                self.toggle_spec_block_on.show()
                self.toggle_spec_block_on.enable()
                self.toggle_spec_block_off.hide()
                self.toggle_spec_block_off.disable()
                self.randomize_suffix.disable()
                self.suffix_entry_box.disable()
            else:
                self.toggle_spec_block_on.hide()
                self.toggle_spec_block_on.disable()
                self.toggle_spec_block_off.show()
                self.toggle_spec_block_off.enable()
                self.randomize_suffix.enable()
                self.suffix_entry_box.enable()
                self.suffix_entry_box.set_text(self.the_cat.name.suffix)

        else:
            self.toggle_spec_block_on.disable()
            self.toggle_spec_block_on.hide()
            self.toggle_spec_block_off.disable()
            self.toggle_spec_block_off.hide()
            self.suffix_entry_box = pygame_gui.elements.UITextEntryLine(
                ui_scale(rect=pygame.Rect((159 + x_pos, 50 + y_pos), (120, 30)), scale=screen_manager.window_scale),
                initial_text=self.the_cat.name.suffix,
                manager=screen_manager.uim,
                container=self,
            )
        self.set_blocking(True)

    def process_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            prefix_source = self.the_cat.name.prefix_source
            prefix: str = self.the_cat.name.prefix
            if event.ui_element == self.done_button:
                old_name = str(self.the_cat.name)
                self.the_cat.name.special_suffix_hidden_f = self.specsuffic_hidden

                # Note: Prefixes are not allowed be all spaces or empty, but they can have spaces in them.
                if sub(r"[^A-Za-z0-9 ]+", "", self.prefix_entry_box.get_text()) != "":
                    self.the_cat.name.prefix = sub(
                        r"[^A-Za-z0-9 ]+", "", self.prefix_entry_box.get_text()
                    )
                    if prefix == self.prefix_entry_box.get_text():
                        self.the_cat.name.prefix_source = prefix_source
                    else:
                        self.the_cat.name.prefix_source = None

                # Suffixes can be empty, if you want. However, don't change the suffix if it's currently being hidden
                # by a special suffix.
                if (
                    self.the_cat.rank in list(self.the_cat.name.special_ranks.keys())
                    or self.the_cat.name.special_suffix_hidden_f
                ):
                    self.the_cat.name.suffix = sub(
                        r"[^A-Za-z0-9 ]+", "", self.suffix_entry_box.get_text()
                    )
                    self.name_changed.show()

                if old_name != str(self.the_cat.name):
                    self.name_changed.show()
                    self.heading.set_text(f"-Change {self.the_cat.name}'s Name-")
                else:
                    self.name_changed.hide()

            elif event.ui_element == self.randomize_prefix:
                prefix_source, prefix = self.the_cat.name.get_random_prefix()
                self.prefix_entry_box.set_text(prefix)
            elif event.ui_element == self.randomize_suffix:
                self.suffix_entry_box.set_text(self.the_cat.name.get_random_suffix())
            elif event.ui_element == self.toggle_spec_block_on:
                self.specsuffic_hidden = True
                self.suffix_entry_box.enable()
                self.randomize_suffix.enable()
                self.toggle_spec_block_on.disable()
                self.toggle_spec_block_on.hide()
                self.toggle_spec_block_off.enable()
                self.toggle_spec_block_off.show()
                self.suffix_entry_box.set_text(self.the_cat.name.suffix)
            elif event.ui_element == self.toggle_spec_block_off:
                self.specsuffic_hidden = False
                self.randomize_suffix.disable()
                self.toggle_spec_block_off.disable()
                self.toggle_spec_block_off.hide()
                self.toggle_spec_block_on.enable()
                self.toggle_spec_block_on.show()
                self.suffix_entry_box.set_text("")
                self.suffix_entry_box.rebuild()
                self.suffix_entry_box.disable()
            elif event.ui_element == self.back_button:
                game.all_screens[ScreenName.Profile].exit_screen()
                game.all_screens[ScreenName.Profile].screen_switches()
                self.kill()
        return super().process_event(event)

# TODO update how the pronouns work for the new version
class PronounCreation(UIWindow):
    # This window allows the user to create a pronoun set
    PronounCat = namedtuple("PronounCat", ["name", "pronouns"])

    def __init__(self, cat):
        super().__init__(
            ui_scale(rect=pygame.Rect((80, 150), (650, 450)), scale=screen_manager.window_scale),
            window_display_title="Create Cat Pronouns",
            object_id="#change_cat_gender_window",
            resizable=False,
        )
        self.the_cat = cat
        self.pronoun_cat = self.PronounCat(
            str(self.the_cat.name), self.the_cat.pronouns
        )
        self.pronoun_template = self.the_cat.pronouns[0].copy()
        self.pronoun_template["ID"] = "custom" + str(len(get_custom_pronouns()))
        self.conju = self.pronoun_template.get("conju", 2)
        self.gender = self.pronoun_template.get("gender", 0)
        self.box_labels = {}
        self.elements = {}
        self.boxes = {}
        self.checkbox_label = {}
        self.back_button = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((615, 10), (22, 22)), scale=screen_manager.window_scale),
            text="",
            object_id="#exit_window_button",
            container=self,
        )

        self.elements["core_container"] = pygame_gui.core.UIContainer(
            ui_scale(rect=pygame.Rect((0, 3), (375, 448)), scale=screen_manager.window_scale),
            manager=screen_manager.uim,
            container=self,
        )
        self.elements["core_box"] = pygame_gui.elements.UIImage(
            ui_scale(rect=pygame.Rect((4, 0), (375, 448)), scale=screen_manager.window_scale),
            get_box(BoxShape.Frame, (375, 448), sides=(False, True, False, False)),
            container=self.elements["core_container"],
            manager=screen_manager.uim,
        )

        # Create a sub-container for the Demo frame and sample text
        demo_container_rect = ui_scale(rect=pygame.Rect((0, 0), (275, 450)), scale=screen_manager.window_scale)
        self.demo_container = pygame_gui.core.UIContainer(
            relative_rect=demo_container_rect,
            manager=screen_manager.uim,
            container=self,
            anchors={"left": "left", "left_target": self.elements["core_container"]},
        )

        # # Add the Demo frame to the sub-container
        self.elements["demo_frame"] = pygame_gui.elements.UIImage(
            ui_scale(rect=pygame.Rect((0, 4), (208, 288)), scale=screen_manager.window_scale),
            get_box(BoxShape.Frame, (208, 288), sides=(False, True, True, True)),
            manager=screen_manager.uim,
            container=self.demo_container,
            anchors={"center": "center"},
        )
        # Title of Demo Box
        self.elements["demo_title"] = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((0, -14), (208, 30)), scale=screen_manager.window_scale),
            text="windows.create_pronouns_demo_title",
            image_dict=get_button_dict(ButtonStyle.RoundedRect, (208, 30), static=True,
                                       scale=screen_manager.window_scale),
            object_id="@ButtonStyle_rounded_rect",
            manager=screen_manager.uim,
            container=self.demo_container,
            anchors={
                "centerx": "centerx",
                "bottom": "bottom",
                "bottom_target": self.elements["demo_frame"],
            },
        )
        self.elements["demo_title"].disable()

        # Add UITextBox for the sample text to the sub-container
        self.sample_text_box = pygame_gui.elements.UITextBox(
            html_text="screens.change_gender.demo",
            relative_rect=ui_scale(rect=pygame.Rect((0, 4), (195, 268)), scale=screen_manager.window_scale),
            object_id="#text_box_30_horizcenter_vertcenter",
            manager=screen_manager.uim,
            container=self.demo_container,
            anchors={"center": "center"},
            text_kwargs={"m_c": self.the_cat},
        )

        # Title
        self.elements["title"] = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((0, 15), (225, 40)), scale=screen_manager.window_scale),
            text="windows.pronoun_creation",
            image_dict=get_button_dict(ButtonStyle.RoundedRect, (225, 40), static=True,
                                       scale=screen_manager.window_scale),
            object_id="@ButtonStyle_icon",
            manager=screen_manager.uim,
            container=self.elements["core_container"],
            anchors={"centerx": "centerx"},
        )
        self.elements["title"].disable()

        self.heading = pygame_gui.elements.UITextBox(
            html_text="windows.create_pronouns_desc",
            relative_rect=ui_scale(rect=pygame.Rect((0, 60), (350, 75)), scale=screen_manager.window_scale),
            object_id="#text_box_30_horizcenter_spacing_95",
            manager=screen_manager.uim,
            container=self.elements["core_container"],
            anchors={"centerx": "centerx"},
        )

        self.dropdowns = {
            "conju_label": pygame_gui.elements.UILabel(
                ui_scale(rect=pygame.Rect((-50, 130), (100, 32)), scale=screen_manager.window_scale),
                "windows.conju",
                object_id="#text_box_30_horizcenter_spacing_95",
                container=self.elements["core_container"],
                anchors={"centerx": "centerx"},
            )
        }
        self.dropdowns["conju_button"] = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((0, 130), (100, 32)), scale=screen_manager.window_scale),
            text=f"windows.conju{self.conju}",
            image_dict=get_button_dict(ButtonStyle.DropDown, (100, 32),
                                       scale=screen_manager.window_scale),
            object_id="@ButtonStyle_dropdown",
            container=self.elements["core_container"],
            anchors={"left_target": self.dropdowns["conju_label"]},
        )

        self.dropdowns["conju_container"] = pygame_gui.elements.UIAutoResizingContainer(
            ui_scale(rect=pygame.Rect((0, -2), (0, 0)), scale=screen_manager.window_scale),
            object_id="#conju_dropdown_container",
            manager=screen_manager.uim,
            container=self.elements["core_container"],
            anchors={
                "top_target": self.dropdowns["conju_button"],
                "left_target": self.dropdowns["conju_label"],
            },
            starting_height=3,
            visible=False,
        )

        self.dropdowns["gender_label"] = pygame_gui.elements.UILabel(
            ui_scale(rect=pygame.Rect((-50, 5), (100, 32)), scale=screen_manager.window_scale),
            text="windows.gender",
            object_id="#text_box_30_horizcenter_spacing_95",
            container=self.elements["core_container"],
            anchors={"top_target": self.dropdowns["conju_label"], "centerx": "centerx"},
        )
        self.dropdowns["gender_button"] = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((0, 5), (100, 32)), scale=screen_manager.window_scale),
            text=f"windows.gender{self.gender}",
            image_dict=get_button_dict(ButtonStyle.DropDown, (100, 32),
                                       scale=screen_manager.window_scale),
            object_id="@ButtonStyle_dropdown",
            container=self.elements["core_container"],
            tool_tip_text="windows.gender_tooltip",
            tool_tip_text_kwargs={"m_c": self.the_cat},
            starting_height=2,
            anchors={
                "top_target": self.dropdowns["conju_label"],
                "left_target": self.dropdowns["gender_label"],
            },
        )
        self.dropdowns[
            "gender_container"
        ] = pygame_gui.elements.UIAutoResizingContainer(
            ui_scale(rect=pygame.Rect((0, -2), (0, 0)), scale=screen_manager.window_scale),
            object_id="#conju_dropdown_container",
            manager=screen_manager.uim,
            container=self.elements["core_container"],
            anchors={
                "top_target": self.dropdowns["gender_button"],
                "left_target": self.dropdowns["gender_label"],
            },
            visible=False,
        )

        config = get_lang_config()["pronouns"] # FIXME mirrors config from outer scope

        for i in range(1, config["conju_count"] + 1):
            self.dropdowns[f"conju{i}"] = UISurfaceImageButton(
                ui_scale(rect=pygame.Rect((0, -2 if i > 1 else 0), (100, 34)), scale=screen_manager.window_scale),
                f"windows.conju{i}",
                get_button_dict(ButtonStyle.DropDown, (100, 34),
                                scale=screen_manager.window_scale),
                container=self.dropdowns["conju_container"],
                object_id="@ButtonStyle_dropdown",
                screen_manager=screen_manager,
                anchors={"top_target": self.dropdowns[f"conju{i-1}"]}
                if i > 1
                else None,
            )

        for i in range(0, config["gender_count"]):
            self.dropdowns[f"gender{i}"] = UISurfaceImageButton(
                ui_scale(rect=pygame.Rect((0, -2 if i > 0 else 0), (100, 34)), scale=screen_manager.window_scale),
                f"windows.gender{i}",
                get_button_dict(ButtonStyle.DropDown, (100, 34),
                                scale=screen_manager.window_scale),
                container=self.dropdowns["gender_container"],
                object_id="@ButtonStyle_dropdown",
            screen_manager=screen_manager,
                anchors={"top_target": self.dropdowns[f"gender{i-1}"]}
                if i > 0
                else None,
            )

        self.dropdowns["conju_dropdown"] = UIDropDownContainer(
            ui_scale(rect=pygame.Rect((0, 125), (0, 0)), scale=screen_manager.window_scale),
            screen_manager=screen_manager,
            container=self,
            object_id="#conju_dropdown",
            starting_height=1,
            parent_button=self.dropdowns["conju_button"],
            child_button_container=self.dropdowns["conju_container"],
            visible=False,
            manager=screen_manager.uim,
        )
        self.dropdowns["gender_dropdown"] = UIDropDownContainer(
            ui_scale(rect=pygame.Rect((0, 125), (0, 0)), scale=screen_manager.window_scale),
            screen_manager=screen_manager,
            container=self,
            object_id="#gender_dropdown",
            starting_height=1,
            parent_button=self.dropdowns["gender_button"],
            child_button_container=self.dropdowns["gender_container"],
            visible=False,
            manager=screen_manager.uim,
        )

        text_inputs = list(self.pronoun_template.keys())
        try:
            text_inputs.remove("ID")
            text_inputs.remove("conju")
            text_inputs.remove("gender")
        except ValueError:
            pass

        for i, item in enumerate(text_inputs):
            self.box_labels[item] = pygame_gui.elements.UITextBox(
                f"windows.{item}",
                ui_scale(rect=pygame.Rect((0, 5), (200, 30)), scale=screen_manager.window_scale),
                object_id="#text_box_30_horizcenter_spacing_95",
                manager=screen_manager.uim,
                container=self.elements["core_container"],
                anchors={"top_target": self.box_labels[text_inputs[i - 1]]}
                if i > 0
                else {"top_target": self.dropdowns["gender_label"]},
            )
            self.boxes[item] = pygame_gui.elements.UITextEntryLine(
                ui_scale(rect=pygame.Rect((0, 5), (150, 30)), scale=screen_manager.window_scale),
                placeholder_text=self.the_cat.pronouns[0][item],
                manager=screen_manager.uim,
                container=self,
                anchors={
                    "top_target": self.boxes[text_inputs[i - 1]],
                    "left_target": self.box_labels[item],
                }
                if i > 0
                else {
                    "top_target": self.dropdowns["gender_label"],
                    "left_target": self.box_labels[item],
                },
            )
            self.boxes[item].set_allowed_characters("alpha_numeric")

        self.buttons = {
            "save_pronouns": UISurfaceImageButton(
                ui_scale(rect=pygame.Rect((0, 400), (73, 30)), scale=screen_manager.window_scale),
                "buttons.save",
                get_button_dict(ButtonStyle.SquOval, (73, 30),
                                scale=screen_manager.window_scale),
                object_id="@ButtonStyle_squoval",
                manager=screen_manager.uim,
                screen_manager=screen_manager,
                container=self.elements["core_container"],
                anchors={"centerx": "centerx"},
            )
        }

        self.pronoun_added = pygame_gui.elements.UITextBox(
            f"windows.pronoun_confirm",
            relative_rect=ui_scale(rect=pygame.Rect((0, 375), (300, 40)), scale=screen_manager.window_scale),
            visible=False,
            object_id="#text_box_30_horizleft",
            manager=screen_manager.uim,
            container=self.elements["core_container"],
            anchors={"centerx": "centerx"},
        )

        self.set_blocking(True)

    def update_display(self):
        for name, entry in self.boxes.items():
            self.pronoun_template[name] = (
                entry.get_text() if entry.get_text() != "" else entry.placeholder_text
            )
        self.sample_text_box.set_text(
            "screens.change_gender.demo",
            text_kwargs={"m_c": self.PronounCat(str(self.the_cat.name), [self.pronoun_template])},
        )

    def process_event(self, event):
        # TODO dropdowns shouldn't be hardcoded?
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.back_button:
                game.all_screens[ScreenName.SpecifyGender].exit_screen()
                game.all_screens[ScreenName.SpecifyGender].screen_switches()
                [item.kill() for item in self.dropdowns.values()]
                self.kill()
            elif event.ui_element == self.dropdowns["conju_button"]:
                if self.dropdowns["conju_dropdown"].is_open:
                    self.dropdowns["conju_dropdown"].close()
                    self.dropdowns["gender_button"].enable()
                else:
                    self.dropdowns["conju_dropdown"].open()
                    self.dropdowns["gender_button"].disable()
                    self.dropdowns["gender_dropdown"].close()
            elif event.ui_element in self.dropdowns["conju_container"]:
                self.pronoun_template["conju"] = int(
                    event.ui_element.text.replace("windows.conju", "")
                )
                self.dropdowns["conju_button"].set_text(event.ui_element.text)
                self.dropdowns["conju_dropdown"].close()
                self.dropdowns["gender_button"].enable()
                self.update_display()
            elif event.ui_element == self.dropdowns["gender_button"]:
                if self.dropdowns["gender_dropdown"].is_open:
                    self.dropdowns["gender_dropdown"].close()
                else:
                    self.dropdowns["gender_dropdown"].open()
                    self.dropdowns["conju_dropdown"].close()
            elif event.ui_element in self.dropdowns["gender_container"]:
                self.pronoun_template["gender"] = int(
                    event.ui_element.text.replace("windows.gender", "")
                )
                self.dropdowns["gender_button"].set_text(event.ui_element.text)
                self.dropdowns["gender_dropdown"].close()
                self.update_display()
            elif event.ui_element == self.buttons["save_pronouns"]:
                add_custom_pronouns(self.pronoun_template)
                self.pronoun_added.show()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                focused_box = [key for key, box in self.boxes.items() if box.is_focused]
                if not focused_box:
                    [box.unfocus() for box in self.boxes.values()]
                    return super().process_event(event)
                key = focused_box[0]
                boxlist = list(self.boxes)
                if event.mod & pygame.KMOD_SHIFT:
                    try:
                        idx = boxlist[boxlist.index(key) - 1]
                    except IndexError:
                        idx = boxlist[-1]
                else:
                    try:
                        idx = boxlist[boxlist.index(key) + 1]
                    except IndexError:
                        idx = boxlist[0]

                self.boxes[key].unfocus()
                self.boxes[idx].focus()
        elif event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            self.update_display()

        return super().process_event(event)

# RedHistory? RedCat.kill_cat()?
class KillCat(UIWindow):
    """This window allows the user to kill the selected cat"""

    def __init__(self, cat):
        super().__init__(
            rect=ui_scale(rect=pygame.Rect((300, 200), (450, 200)), scale=screen_manager.window_scale),
            window_display_title="Kill Cat",
            object_id="#kill_cat_window",
            resizable=False,
        )
        self.the_cat = cat
        self.take_all = False
        self.back_button = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((420, 5), (22, 22)), scale=screen_manager.window_scale),
            text="",
            object_id="#exit_window_button",
            container=self,
        )
        # TODO replace this with TextHandler
        cat_dict = {"m_c": (str(self.the_cat.name), choice(self.the_cat.pronouns))}
        self.heading = pygame_gui.elements.UITextBox(
            html_text="windows.kill_cat_method",
            relative_rect=ui_scale(rect=pygame.Rect((10, 10), (430, 75)), scale=screen_manager.window_scale),
            object_id="#text_box_30_horizcenter_spacing_95",
            manager=screen_manager.uim,
            container=self,
        )

        self.one_life_check = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((25, 150), (34, 34)), scale=screen_manager.window_scale),
            text="",
            object_id="@unchecked_checkbox",
            tool_tip_text=process_text(
                i18n.t("windows.all_lives_leader_tooltip"),
                cat_dict,
            ),
            manager=screen_manager.uim,
            container=self,
        )
        self.all_lives_check = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((25, 150), (34, 34)), scale=screen_manager.window_scale),
            text="",
            object_id="@checked_checkbox",
            tool_tip_text=process_text(
                i18n.t("windows.all_lives_leader_tooltip"),
                cat_dict,
            ),
            manager=screen_manager.uim,
            container=self,
        )

        if self.the_cat.rank is Rank.Leader:
            self.done_button = UISurfaceImageButton(
                ui_scale(rect=pygame.Rect((347, 152), (77, 30)), scale=screen_manager.window_scale),
                "buttons.done_lower",
                get_button_dict(ButtonStyle.SquOval, (77, 30),
                                scale=screen_manager.window_scale),
                object_id="@ButtonStyle_squoval",
                screen_manager=screen_manager,
                manager=screen_manager.uim,
                container=self,
            )

            self.prompt = process_text(i18n.t("windows.death_prompt"), cat_dict)
            self.initial = process_text(i18n.t("windows.default_death"), cat_dict)

            self.all_lives_check.hide()
            self.life_text = pygame_gui.elements.UITextBox(
                "windows.all_lives_leader",
                ui_scale(rect=pygame.Rect((60, 147), (450, 40)), scale=screen_manager.window_scale),
                object_id="#text_box_30_horizleft",
                manager=screen_manager.uim,
                container=self,
            )
            self.beginning_prompt = pygame_gui.elements.UITextBox(
                self.prompt,
                ui_scale(rect=pygame.Rect((25, 30), (450, 40)), scale=screen_manager.window_scale),
                object_id="#text_box_30_horizleft",
                manager=screen_manager.uim,
                container=self,
            )

            self.death_entry_box = pygame_gui.elements.UITextEntryBox(
                ui_scale(rect=pygame.Rect((25, 65), (400, 75)), scale=screen_manager.window_scale),
                initial_text=self.initial,
                object_id="text_entry_line",
                manager=screen_manager.uim,
                container=self,
            )

        elif self.the_cat.history.get_death_or_scars(deaths=True):
        # elif History.get_death_or_scars(self.the_cat, death=True):
            # This should only occur for retired leaders.

            self.prompt = process_text(i18n.t("windows.death_prompt"), cat_dict)
            self.initial = process_text(
                i18n.t("windows.default_leader_death"), cat_dict
            )
            self.all_lives_check.hide()
            self.one_life_check.hide()

            self.beginning_prompt = pygame_gui.elements.UITextBox(
                self.prompt,
                ui_scale(rect=pygame.Rect((25, 30), (450, 40)), scale=screen_manager.window_scale),
                object_id="#text_box_30_horizleft",
                manager=screen_manager.uim,
                container=self,
            )

            self.death_entry_box = pygame_gui.elements.UITextEntryBox(
                ui_scale(rect=pygame.Rect((25, 65), (400, 75)), scale=screen_manager.window_scale),
                initial_text=self.initial,
                object_id="text_entry_line",
                manager=screen_manager.uim,
                container=self,
            )

            self.done_button = UISurfaceImageButton(
                ui_scale(rect=pygame.Rect((186, 152), (77, 30)), scale=screen_manager.window_scale),
                "buttons.done_lower",
                get_button_dict(ButtonStyle.SquOval, (77, 30),
                                scale=screen_manager.window_scale),
                object_id="@ButtonStyle_squoval",
                screen_manager=screen_manager,
                manager=screen_manager.uim,
                container=self,
            )
        else:
            self.initial = i18n.t("windows.default_death_pronounless")
            self.prompt = None
            self.all_lives_check.hide()
            self.one_life_check.hide()

            self.death_entry_box = pygame_gui.elements.UITextEntryBox(
                ui_scale(rect=pygame.Rect((25, 55), (400, 75)), scale=screen_manager.window_scale),
                initial_text=self.initial,
                object_id="text_entry_line",
                manager=screen_manager.uim,
                container=self,
            )

            self.done_button = UISurfaceImageButton(
                ui_scale(rect=pygame.Rect((186, 152), (77, 30)), scale=screen_manager.window_scale),
                "buttons.done_lower",
                get_button_dict(ButtonStyle.SquOval, (77, 30),
                                scale=screen_manager.window_scale),
                object_id="@ButtonStyle_squoval",
                screen_manager=screen_manager,
                manager=screen_manager.uim,
                container=self,
            )
        self.set_blocking(True)

    def process_event(self, event):
        super().process_event(event)

        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.done_button:
                death_message = sub(
                    r"[^A-Za-z0-9<->/.()*'&#!?,| _]+",
                    "",
                    self.death_entry_box.get_text(),
                )
                if self.the_cat.rank is Rank.Leader:
                    # TODO use the TextHandler
                    if death_message.startswith("was"):
                        death_message = death_message.replace(
                            "was", "{VERB/m_c/were/was}", 1
                        )
                    elif death_message.startswith("were"):
                        death_message = death_message.replace(
                            "were", "{VERB/m_c/were/was}", 1
                        )

                    # TODO use cat_obj.kill_cat?
                    clan_obj = game.cat_tracker.get_clan_object(clan_token=game.active_clan_token)
                    if self.take_all:
                        clan_obj.kill_leader(remove_all_lives=True)
                    else:
                        clan_obj.kill_leader()

                self.the_cat.kill()  # TODO add the death message
                update_sprite(self.the_cat)
                game.all_screens[ScreenName.Profile].exit_screen()
                game.all_screens[ScreenName.Profile].screen_switches()
                self.kill()
            elif event.ui_element == self.all_lives_check:
                self.take_all = False
                self.all_lives_check.hide()
                self.one_life_check.show()
            elif event.ui_element == self.one_life_check:
                self.take_all = True
                self.all_lives_check.show()
                self.one_life_check.hide()
            elif event.ui_element == self.back_button:
                game.all_screens[ScreenName.Profile].exit_screen()
                game.all_screens[ScreenName.Profile].screen_switches()
                self.kill()

        return super().process_event(event)


class UpdateWindow(UIWindow):
    def __init__(self, last_screen, announce_restart_callback):
        super().__init__(
            ui_scale(rect=pygame.Rect((250, 200), (300, 160)), scale=screen_manager.window_scale),
            window_display_title="Game Over",
            object_id="#game_over_window",
            resizable=False,
        )
        self.set_blocking(True)
        self.last_screen = last_screen
        self.update_message = pygame_gui.elements.UITextBox(
            html_text="windows.update_message",
            relative_rect=ui_scale(rect=pygame.Rect((20, 10), (260, -1)), scale=screen_manager.window_scale),
            object_id="#text_box_30_horizcenter_spacing_95",
            starting_height=4,
            container=self,
        )
        self.announce_restart_callback = announce_restart_callback

        self.step_text = UITextBoxTweaked(
            html_text="windows.downloading_update",
            relative_rect=ui_scale(rect=pygame.Rect((20, 40), (260, -1)), scale=screen_manager.window_scale),
            line_spacing=1,
            object_id="#text_box_30_horizcenter",
            screen_manager=screen_manager,
            container=self,
        )

        self.progress_bar = UIUpdateProgressBar(
            ui_scale(rect=pygame.Rect((20, 65), (260, 45)), scale=screen_manager.window_scale),
            self.step_text,
            object_id="progress_bar",
            container=self,
        )

        self.update_thread = threading.Thread(
            target=self_update,
            daemon=True,
            args=(
                UpdateChannel(get_version_info().release_channel),
                self.progress_bar,
                announce_restart_callback,
            ),
        )
        self.update_thread.start()

        self.cancel_button = UIImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((200, 115), (78, 30)), scale=screen_manager.window_scale),
            text="",
            object_id="#cancel_button",
            screen_manager=screen_manager,
            container=self,
        )

        self.cancel_button.enable()

    def process_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.cancel_button:
                self.kill()

        return super().process_event(event)


class AnnounceRestart(UIWindow):
    def __init__(self, last_screen):
        super().__init__(
            ui_scale(rect=pygame.Rect((250, 200), (300, 90)), scale=screen_manager.window_scale),
            window_display_title="Game Over",
            object_id="#game_over_window",
            resizable=False,
        )
        self.last_screen = last_screen
        self.announce_message = UITextBoxTweaked(
            f"windows.restart_announce",
            relative_rect=ui_scale(rect=pygame.Rect((20, 20), (260, -1)), scale=screen_manager.window_scale),
            line_spacing=1,
            object_id="#text_box_30_horizcenter",
            screen_manager=screen_manager,
            container=self,
            text_kwargs={"count": "3"},
        )

        threading.Thread(target=self.update_text, daemon=True).start()

    def update_text(self):
        for i in range(2, 0, -1):
            time.sleep(1)
            self.announce_message.set_text(
                "windows.restart_announce", text_kwargs={"count": i}
            )


class UpdateAvailablePopup(UIWindow):
    def __init__(self, show_checkbox: bool = False):
        super().__init__(
            ui_scale(rect=pygame.Rect((200, 200), (400, 230)), scale=screen_manager.window_scale),
            window_display_title="Update available",
            object_id="#game_over_window",
            resizable=False,
        )
        self.set_blocking(True)

        self.begin_update_title = UIImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((97, 15), (200, 40)), scale=screen_manager.window_scale),
            text="",
            screen_manager=screen_manager,
            object_id="#new_update_button",
            container=self,
        )

        latest_version_number = "{:.16}".format(get_latest_version_number())
        current_version_number = "{:.16}".format(get_version_info().commit_id)

        self.game_over_message = UITextBoxTweaked(
            html_text="update_available",
            relative_rect=ui_scale(rect=pygame.Rect((10, 80), (400, -1)), scale=screen_manager.window_scale),
            line_spacing=0.8,
            object_id="#update_popup_title",
            screen_manager=screen_manager,
            container=self,
            text_kwargs={"latest_version_number": latest_version_number},
        )

        self.game_over_message = UITextBoxTweaked(
            html_text="windows.current_version",
            relative_rect=ui_scale(rect=pygame.Rect((11, 100), (400, -1)), scale=screen_manager.window_scale),
            line_spacing=0.8,
            object_id="#current_version",
            screen_manager=screen_manager,
            container=self,
            text_kwargs={"ver": current_version_number},
        )

        self.game_over_message = UITextBoxTweaked(
            html_text="windows.install_update",
            relative_rect=ui_scale(rect=pygame.Rect((10, 131), (200, -1)), scale=screen_manager.window_scale),
            line_spacing=0.8,
            object_id="#text_box_30",
            screen_manager=screen_manager,
            container=self,
        )

        self.box_unchecked = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((7, 183), (34, 34)), scale=screen_manager.window_scale),
            text="",
            object_id="@unchecked_checkbox",
            container=self,
        )
        self.box_checked = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((7, 183), (34, 34)), scale=screen_manager.window_scale),
            text="",
            object_id="@checked_checkbox",
            container=self,
        )
        self.box_text = UITextBoxTweaked(
            screen_manager=screen_manager,
            html_text="windows.dont_ask_again",
            relative_rect=ui_scale(rect=pygame.Rect((39, 190), (125, -1)), scale=screen_manager.window_scale),
            line_spacing=0.8,
            object_id="#text_box_30",
            container=self,
        )

        self.continue_button = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((278, 185), (102, 30)), scale=screen_manager.window_scale),
            text="buttons.continue",
            image_dict=get_button_dict(ButtonStyle.SquOval, (77, 30),
                                       scale=screen_manager.window_scale),
            object_id="@ButtonStyle_squoval",
            container=self,
        )

        self.cancel_button = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((187, 185), (78, 30)), scale=screen_manager.window_scale),
            text="buttons.cancel",
            image_dict=get_button_dict(ButtonStyle.SquOval, (77, 30),
                                       scale=screen_manager.window_scale),
            # (ButtonStyle.SquOval, (77, 30), scale=screen_manager.window_scale),
            object_id="@ButtonStyle_squoval",
            container=self,
        )

        self.close_button = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((740, 10), (44, 44)), scale=screen_manager.window_scale),
            text="",
            object_id="#exit_window_button",
            container=self,
        )

        if show_checkbox:
            self.box_unchecked.enable()
            self.box_checked.hide()
        else:
            self.box_checked.hide()
            self.box_unchecked.hide()
            self.box_text.hide()

        self.continue_button.enable()
        self.cancel_button.enable()
        self.close_button.enable()

    def process_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.continue_button:
                # TODO screen changes
                self.x = UpdateWindow(
                    game.switches["cur_screen"], self.announce_restart_callback
                )
                self.kill()
            elif (
                event.ui_element == self.close_button
                or event.ui_element == self.cancel_button
            ):
                self.kill()
            elif event.ui_element == self.box_unchecked:
                self.box_unchecked.disable()
                self.box_unchecked.hide()
                self.box_checked.enable()
                self.box_checked.show()
                # TODO hardcoded file location
                with open(
                    f"{get_cache_dir()}/suppress_update_popup", "w", encoding="utf-8"
                ) as write_file:
                    write_file.write(get_latest_version_number())
            elif event.ui_element == self.box_checked:
                self.box_checked.disable()
                self.box_checked.hide()
                self.box_unchecked.enable()
                self.box_unchecked.show()
                # TODO hardcoded file location
                if os.path.exists(f"{get_cache_dir()}/suppress_update_popup"):
                    os.remove(f"{get_cache_dir()}/suppress_update_popup")
        return super().process_event(event)

    def announce_restart_callback(self):
        self.x.kill()
        y = AnnounceRestart(game.switches["cur_screen"])
        y.update(1)

# TODO ClanSim vs ClanGen changelogs
class ChangelogPopup(UIWindow):
    def __init__(self):
        super().__init__(
            ui_scale(rect=pygame.Rect((150, 150), (500, 400)), scale=screen_manager.window_scale),
            window_display_title="Changelog",
            object_id="#game_over_window",
            resizable=False,
        )
        self.set_blocking(True)

        self.changelog_popup_title = UITextBoxTweaked(
            html_text="windows.whats_new",
            relative_rect=ui_scale(rect=pygame.Rect((0, 10), (500, -1)), scale=screen_manager.window_scale),
            screen_manager=screen_manager,
            line_spacing=1,
            object_id="#changelog_popup_title",
            container=self,
            anchors={"centerx": "centerx"},
        )

        # TODO version number
        current_version_number = "{:.16}".format(get_version_info().commit_id)

        self.changelog_popup_subtitle = UITextBoxTweaked(
            screen_manager=screen_manager,
            html_text="windows.version_title",
            relative_rect=ui_scale(rect=pygame.Rect((0, 35), (500, -1)), scale=screen_manager.window_scale),
            line_spacing=1,
            object_id="#changelog_popup_subtitle",
            container=self,
            anchors={"centerx": "centerx"},
            text_kwargs={"ver": current_version_number},
        )

        dynamic_changelog = False
        if (
            get_version_info().is_dev
            and get_version_info().is_source_build
            and get_version_info().git_installed
        ):
            file_cont = subprocess.check_output(
                [
                    "git",
                    "log",
                    r"--pretty=format:%H|||%cd|||%b|||%s",
                    "-15",
                    "--no-decorate",
                    "--merges",
                    "--grep=Merge pull request",
                    "--date=short",
                ]
            ).decode("utf-8")
            dynamic_changelog = True
        else:
            # TODO ClanGen changelog vs ClanSim changelog
            with open("changelog.clangen.txt", "r", encoding="utf-8") as read_file:
                file_cont = read_file.read()

        if get_version_info().is_dev and not get_version_info().is_source_build:
            dynamic_changelog = True

        if dynamic_changelog:
            commits = file_cont.splitlines()
            file_cont = ""
            for line in commits:
                info = line.split("|||")

                if len(info) < 4:
                    continue

                # Get PR number so we can link the PR
                pr_number = re_search(r"Merge pull request #([0-9]*?) ", info[3])
                if pr_number:
                    # For some reason, multi-line links on pygame_gui's text boxes don't work very well.
                    # So, to work around that, just add a little "link" at the end
                    info[
                        2
                    ] += f" <a href='https://github.com/ClanGenOfficial/clangen/pull/{pr_number.group(1)}'>(link)</a>"

                # Format: DATE- \n PR Title (link)
                file_cont += f"<b>{info[1]}</b>\n- {info[2]}\n"

        self.changelog_text = UITextBoxTweaked(
            screen_manager=screen_manager,
            html_text=file_cont,
            relative_rect=ui_scale(rect=pygame.Rect((10, 65), (480, 325)), scale=screen_manager.window_scale),
            object_id="#text_box_30",
            line_spacing=0.95,
            starting_height=2,
            container=self,
            manager=screen_manager.uim,
        )

        self.close_button = UIImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((470, 5), (22, 22)), scale=screen_manager.window_scale),
            text="",
            object_id="#exit_window_button",
            screen_manager=screen_manager,
            starting_height=2,
            container=self,
        )

    def process_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.close_button:
                self.kill()
        return super().process_event(event)


class RelationshipLog(UIWindow):
    """This window allows the user to see the relationship log of a certain relationship."""

    def __init__(self, relationship, disable_button_list, hide_button_list):
        super().__init__(
            ui_scale(rect=pygame.Rect((273, 122), (505, 550)), scale=screen_manager.window_scale),
            window_display_title="Relationship Log",
            object_id="#relationship_log_window",
            resizable=False,
        )
        self.hide_button_list = hide_button_list
        for button in self.hide_button_list:
            button.hide()

        self.exit_button = UIImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((470, 7), (22, 22)), scale=screen_manager.window_scale),
            text="",
            object_id="#exit_window_button",
            screen_manager=screen_manager,
            container=self,
        )
        self.back_button = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((25, 645), (105, 30)), scale=screen_manager.window_scale),
            text="buttons.back",
            image_dict=get_button_dict(ButtonStyle.SquOval, (105, 30),
                                       scale=screen_manager.window_scale),
            object_id="@ButtonStyle_squoval",
        )
        self.log_icon = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((222, 404), (34, 34)), scale=screen_manager.window_scale),
            text=Icon.NOTEPAD,
            image_dict=get_button_dict(ButtonStyle.Icon, (34, 34),
                                       scale=screen_manager.window_scale),
            object_id="@ButtonStyle_icon",
        )
        self.closing_buttons = [self.exit_button, self.back_button, self.log_icon]

        self.disable_button_list = []
        for button in disable_button_list:
            if button.is_enabled:
                self.disable_button_list.append(button)
                button.disable()

        opposite_log_string = None
        if not relationship.opposite_relationship:
            relationship.link_relationship()
        if (
            relationship.opposite_relationship
            and len(relationship.opposite_relationship.log) > 0
        ):
            opposite_log_string = f"{f'<br>-----------------------------<br>'.join(relationship.opposite_relationship.log)}<br>"

        log_string = (
            f"{f'<br>-----------------------------<br>'.join(relationship.log)}<br>"
            if len(relationship.log) > 0
            else i18n.t("windows.no_relation_logs")
        )

        if not opposite_log_string:
            self.log = pygame_gui.elements.UITextBox(
                log_string,
                ui_scale(rect=pygame.Rect((15, 45), (476, 425)), scale=screen_manager.window_scale),
                object_id="#text_box_30_horizleft",
                manager=screen_manager.uim,
                container=self,
            )
        else:
            self.log = pygame_gui.elements.UITextBox(
                log_string,
                ui_scale(rect=pygame.Rect((15, 45), (476, 250)), scale=screen_manager.window_scale),
                object_id="#text_box_30_horizleft",
                manager=screen_manager.uim,
                container=self,
            )
            self.opp_heading = pygame_gui.elements.UITextBox(
                "windows.other_perspective",
                ui_scale(rect=pygame.Rect((15, 275), (476, 280)), scale=screen_manager.window_scale),
                object_id="#text_box_30_horizleft",
                manager=screen_manager.uim,
                container=self,
            )
            self.opp_heading.disable()
            self.opp_log = pygame_gui.elements.UITextBox(
                opposite_log_string,
                ui_scale(rect=pygame.Rect((15, 305), (476, 232)), scale=screen_manager.window_scale),
                object_id="#text_box_30_horizleft",
                manager=screen_manager.uim,
                container=self,
            )

    def closing_process(self):
        """Handles to enable and kill all processes when an exit button is clicked."""
        for button in self.disable_button_list:
            button.enable()

        for button in self.hide_button_list:
            button.show()
            button.enable()
        self.log_icon.kill()
        self.exit_button.kill()
        self.back_button.kill()
        self.kill()

    def process_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element in self.closing_buttons:
                self.closing_process()
        return super().process_event(event)


class SaveError(UIWindow):
    def __init__(self, error_text):
        super().__init__(
            ui_scale(rect=pygame.Rect((150, 150), (500, 400)), scale=screen_manager.window_scale),
            window_display_title="Changelog",
            object_id="#game_over_window",
            resizable=False,
        )
        self.set_blocking(True)
        self.changelog_popup_title = pygame_gui.elements.UITextBox(
            html_text="windows.save_failed_title",
            relative_rect=ui_scale(rect=pygame.Rect((20, 10), (445, 375)), scale=screen_manager.window_scale),
            object_id="#text_box_30",
            container=self,
            text_kwargs={"error": error_text},
        )

        self.close_button = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((470, 5), (22, 22)), scale=screen_manager.window_scale),
            text="",
            object_id="#exit_window_button",
            starting_height=2,
            container=self,
        )

    def process_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.close_button:
                self.kill()
        return super().process_event(event)


class SaveAsImage(UIWindow):
    def __init__(self, image_to_save, file_name):
        super().__init__(
            ui_scale(rect=pygame.Rect((200, 175), (400, 250)), scale=screen_manager.window_scale),
            object_id="#game_over_window",
            resizable=False,
        )

        self.set_blocking(True)

        self.image_to_save = image_to_save
        self.file_name = file_name
        self.scale_factor = 1

        button_layout_rect = ui_scale(rect=pygame.Rect((0, 5), (22, 22)), scale=screen_manager.window_scale)
        button_layout_rect.topright = ui_scale_offset((-1, 5))

        self.close_button = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=button_layout_rect,
            text="",
            object_id="#exit_window_button",
            starting_height=2,
            container=self,
            anchors={"right": "right", "top": "top"},
        )

        self.save_as_image = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((0, 90), (135, 30)), scale=screen_manager.window_scale),
            text="screens.sprite_inspect.save_as_image",
            image_dict=get_button_dict(ButtonStyle.SquOval, (135, 30),
                                       scale=screen_manager.window_scale),
            object_id="@ButtonStyle_squoval",
            sound_id="save",
            container=self,
            anchors={"centerx": "centerx"},
        )

        self.open_data_directory_button = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((0, 175), (178, 30)), scale=screen_manager.window_scale),
            text="buttons.open_data_directory",
            image_dict=get_button_dict(ButtonStyle.SquOval, (178, 30),
                                       scale=screen_manager.window_scale),
            object_id="@ButtonStyle_squoval",
            container=self,
            starting_height=2,
            tool_tip_text="buttons.open_data_directory_tooltip",
            anchors={"centerx": "centerx"},
        )

        self.small_size_button = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((54, 50), (97, 30)), scale=screen_manager.window_scale),
            text="",
            object_id="#image_small_button",
            container=self,
            starting_height=2,
        )
        self.small_size_button.disable()

        self.medium_size_button = UIImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((151, 50), (97, 30)), scale=screen_manager.window_scale),
            text="",
            object_id="#image_medium_button",
            container=self,
            starting_height=2,
            screen_manager=screen_manager,
        )

        self.large_size_button = UIImageButton(
            relative_rect=ui_scale(rect=pygame.Rect((248, 50), (97, 30)), scale=screen_manager.window_scale),
            text="",
            object_id="#image_large_button",
            container=self,
            starting_height=2,
            screen_manager=screen_manager,
        )

        self.confirm_text = pygame_gui.elements.UITextBox(
            html_text="",
            relative_rect=ui_scale(rect=pygame.Rect((5, 125), (390, 45)), scale=screen_manager.window_scale),
            object_id="#text_box_26_horizcenter_vertcenter_spacing_95",
            container=self,
            starting_height=2,
        )

    def save_image(self):
        file_name = self.file_name
        file_number = ""
        i = 0
        while True:
            if os.path.isfile(
                f"{get_saved_images_dir()}/{file_name + file_number}.png"
            ):
                i += 1
                file_number = f"_{i}"
            else:
                break

        scaled_image = pygame.transform.scale_by(self.image_to_save, self.scale_factor)
        pygame.image.save(
            scaled_image, f"{get_saved_images_dir()}/{file_name + file_number}.png"
        )
        return f"{file_name + file_number}.png"

    def process_event(self, event) -> bool:
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.close_button:
                self.kill()
            elif event.ui_element == self.open_data_directory_button:
                if system() == "Darwin":
                    subprocess.Popen(["open", "-R", get_data_dir()])
                elif system() == "Windows":
                    os.startfile(get_data_dir())  # pylint: disable=no-member
                elif system() == "Linux":
                    try:
                        subprocess.Popen(["xdg-open", get_data_dir()])
                    except OSError:
                        logger.exception("Failed to call to xdg-open.")
                return True
            elif event.ui_element == self.save_as_image:
                file_name = self.save_image()
                self.confirm_text.set_text(
                    "windows.confirm_saved_image", text_kwargs={"file_name": file_name}
                )
            elif event.ui_element == self.small_size_button:
                self.scale_factor = 1
                self.small_size_button.disable()
                self.medium_size_button.enable()
                self.large_size_button.enable()
            elif event.ui_element == self.medium_size_button:
                self.scale_factor = 4
                self.small_size_button.enable()
                self.medium_size_button.disable()
                self.large_size_button.enable()
            elif event.ui_element == self.large_size_button:
                self.scale_factor = 6
                self.small_size_button.enable()
                self.medium_size_button.enable()
                self.large_size_button.disable()

        return super().process_event(event)


class EventLoading(UIWindow):
    """ Handles the event loading animation """

    def __init__(self, pos):
        if pos is None:
            pos = (350, 300)

        super().__init__(
            rect=ui_scale(rect=pygame.Rect(pos, (100, 100)), scale=screen_manager.window_scale),
            window_display_title="Game Over",
            object_id="#loading_window",
            resizable=False,
        )

        self.set_blocking(True)

        self.frames = self.load_images()
        self.end_animation = False

        self.animated_image = pygame_gui.elements.UIImage(
            ui_scale(rect=pygame.Rect(0, 0, 100, 100), scale=screen_manager.window_scale),
            self.frames[0],
            container=self,
        )

        self.animation_thread = threading.Thread(target=self.animate)
        self.animation_thread.start()

    @staticmethod
    def load_images() -> list[pygame.Surface]:
        frames = []
        for i in range(0, 16):
            frames.append(
                pygame.image.load(f"resources/images/loading_animate/timeskip/{i}.png") # FIXME hard reference
            )

        return frames

    def animate(self):
        """Loops over the event frames and displays the animation"""
        i = 0
        while not self.end_animation:
            i = (i + 1) % (len(self.frames))

            self.animated_image.set_image(self.frames[i])
            time.sleep(0.125)

    def kill(self):
        self.end_animation = True
        super().kill()


class ChangeCatToggles(UIWindow):
    """This window allows the user to edit various cat behavior toggles"""

    def __init__(self, cat):
        super().__init__(
            ui_scale(rect=pygame.Rect((300, 215), (400, 185)), scale=screen_manager.window_scale),
            window_display_title="Change Cat Name",
            object_id="#change_cat_name_window",
            resizable=False,
        )
        self.the_cat = cat
        self.set_blocking(True)
        self.back_button = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((370, 5), (22, 22)), scale=screen_manager.window_scale),
            text="",
            object_id="#exit_window_button",
            container=self,
        )

        self.checkboxes = {}
        self.refresh_checkboxes()

        # Text
        self.text_1 = pygame_gui.elements.UITextBox(
            html_text="windows.prevent_fading",
            relative_rect=ui_scale(rect=pygame.Rect(55, 25, -1, 32), scale=screen_manager.window_scale),
            object_id="#text_box_30_horizleft_pad_0_8",
            container=self,
        )

        self.text_2 = pygame_gui.elements.UITextBox(
            html_text="windows.prevent_kits",
            relative_rect=ui_scale(rect=pygame.Rect(55, 50, -1, 32), scale=screen_manager.window_scale),
            object_id="#text_box_30_horizleft_pad_0_8",
            container=self,
        )

        self.text_3 = pygame_gui.elements.UITextBox(
            html_text="windows.prevent_retirement",
            relative_rect=ui_scale(rect=pygame.Rect(55, 75, -1, 32), scale=screen_manager.window_scale),
            object_id="#text_box_30_horizleft_pad_0_8",
            container=self,
        )

        self.text_4 = pygame_gui.elements.UITextBox(
            html_text="windows.prevent_romance",
            relative_rect=ui_scale(rect=pygame.Rect(55, 100, -1, 32), scale=screen_manager.window_scale),
            object_id="#text_box_30_horizleft_pad_0_8",
            container=self,
        )

        # Text

    def refresh_checkboxes(self):

        for x in self.checkboxes.values():
            x.kill()
        self.checkboxes = {}

        # Prevent Fading
        if self.the_cat.cat_id in [game.cat_tracker.sc_guide_cat_id, game.cat_tracker.df_guide_cat_id]:
            box_type = "@checked_checkbox"
            tool_tip = "windows.prevent_fading_tooltip_guide"
        elif self.the_cat.prevent_fading:
            box_type = "@checked_checkbox"
            tool_tip = "windows.prevent_fading_tooltip"
        else:
            box_type = "@unchecked_checkbox"
            tool_tip = "windows.prevent_fading_tooltip"

        # Fading
        self.checkboxes["prevent_fading"] = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((22, 25), (34, 34)), scale=screen_manager.window_scale),
            text="",
            container=self,
            object_id=box_type,
            tool_tip_text=tool_tip,
        )

        if self.the_cat.cat_id in [game.cat_tracker.sc_guide_cat_id, game.cat_tracker.df_guide_cat_id]:
            self.checkboxes["prevent_fading"].disable()

        # No Kits
        self.checkboxes["prevent_kits"] = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((22, 50), (34, 34)), scale=screen_manager.window_scale),
            text="",
            container=self,
            object_id="@checked_checkbox"
            if self.the_cat.no_kits_f
            else "@unchecked_checkbox",
            tool_tip_text="windows.prevent_kits_tooltip",
        )

        # No Retire
        self.checkboxes["prevent_retire"] = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((22, 75), (34, 34)), scale=screen_manager.window_scale),
            text="",
            container=self,
            object_id="@checked_checkbox"
            if self.the_cat.no_retire_f
            else "@unchecked_checkbox",
            tool_tip_text="windows.prevent_retirement_tooltip_yes"
            if self.the_cat.no_retire_f
            else "windows.prevent_retirement_tooltip_no",
        )

        # No mates
        self.checkboxes["prevent_mates"] = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((22, 100), (34, 34)), scale=screen_manager.window_scale),
            text="",
            container=self,
            object_id="@checked_checkbox"
            if self.the_cat.no_romance_f
            else "@unchecked_checkbox",
            tool_tip_text="windows.prevent_romance_tooltip",
        )

    def process_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.back_button:
                game.all_screens[ScreenName.Profile].exit_screen()
                game.all_screens[ScreenName.Profile].screen_switches()
                self.kill()
            elif event.ui_element == self.checkboxes["prevent_fading"]:
                self.the_cat.prevent_fading = not self.the_cat.prevent_fading
                self.refresh_checkboxes()
            elif event.ui_element == self.checkboxes["prevent_kits"]:
                self.the_cat.no_kits_f = not self.the_cat.no_kits_f
                self.refresh_checkboxes()
            elif event.ui_element == self.checkboxes["prevent_retire"]:
                self.the_cat.no_retire_f = not self.the_cat.no_retire_f
                self.refresh_checkboxes()
            elif event.ui_element == self.checkboxes["prevent_mates"]:
                self.the_cat.no_romance_f = not self.the_cat.no_romance_f
                self.refresh_checkboxes()

        return super().process_event(event)


class SelectFocusClans(UIWindow):
    """ This window allows the user to select the Clans to be sabotaged, aided or raided in the focus setting. """

    def __init__(self):
        super().__init__(
            ui_scale(rect=pygame.Rect((250, 120), (300, 225)), scale=screen_manager.window_scale),
            window_display_title="Change Cat Name",
            object_id="#change_cat_name_window",
            resizable=False,
        )
        self.set_blocking(True)
        self.back_button = UIImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((270, 5), (22, 22)), scale=screen_manager.window_scale),
            text="",
            object_id="#exit_window_button",
            container=self,
        )
        self.save_button = UISurfaceImageButton(
            screen_manager=screen_manager,
            relative_rect=ui_scale(rect=pygame.Rect((80, 180), (139, 30)), scale=screen_manager.window_scale),
            text="windows.change_focus",
            image_dict=get_button_dict(ButtonStyle.SquOval, (139, 30),
                                       scale=screen_manager.window_scale),
            object_id="@ButtonStyle_squoval",
            container=self,
        )
        self.save_button.disable()

        self.checkboxes = {}
        self.refresh_checkboxes()

        # Text
        self.texts = {"prompt": pygame_gui.elements.UITextBox(
            html_text="windows.focus_prompt",
            relative_rect=ui_scale(rect=pygame.Rect((0, 5), (300, 30)), scale=screen_manager.window_scale),
            object_id="#text_box_30_horizcenter",
            container=self,
        )}
        n = 0
        for clan_prefix in game.cat_tracker.all_clans.keys():
            self.texts[clan_prefix] = pygame_gui.elements.UITextBox(
                html_text=clan_prefix + "Clan",
                relative_rect=ui_scale(rect=pygame.Rect(107, n * 27 + 38, -1, 25), scale=screen_manager.window_scale),
                object_id="#text_box_30_horizleft_pad_0_8",
                container=self,
            )
            n += 1

    def refresh_checkboxes(self):
        clan_obj = game.cat_tracker.get_clan_object(game.active_clan_token)

        for x in self.checkboxes.values():
            x.kill()
        self.checkboxes = {}

        n = 0
        for clan_prefix in game.cat_tracker.all_clans.keys():
            box_type = "@unchecked_checkbox"
            if clan_prefix in clan_obj.warrior_focus_arg:
                box_type = "@checked_checkbox"

            self.checkboxes[clan_prefix] = UIImageButton(
                ui_scale(rect=pygame.Rect((75, n * 27 + 35), (34, 34)), scale=screen_manager.window_scale),
                "",
                container=self,
                screen_manager=screen_manager,
                object_id=box_type,
            )
            n += 1

    def process_event(self, event):
        clan_obj = game.cat_tracker.get_clan_object(game.active_clan_token)
        
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.back_button:
                clan_obj.warrior_focus_arg = []
                game.all_screens[ScreenName.WarriorDen].exit_screen()
                game.all_screens[ScreenName.WarriorDen].screen_switches()
                self.kill()
            if event.ui_element == self.save_button:
                game.all_screens[ScreenName.WarriorDen].save_focus()
                game.all_screens[ScreenName.WarriorDen].exit_screen()
                game.all_screens[ScreenName.WarriorDen].screen_switches()
                self.kill()
            if event.ui_element in self.checkboxes.values():
                for clan_name, value in self.checkboxes.items():
                    if value == event.ui_element:
                        if value.object_ids[1] == "@unchecked_checkbox":
                            clan_obj.warrior_focus_arg.append(clan_name)
                        if value.object_ids[1] == "@checked_checkbox":
                            clan_obj.warrior_focus_arg.remove(clan_name)
                        self.refresh_checkboxes()
                if len(clan_obj.warrior_focus_arg) < 1 and self.save_button.is_enabled:
                    self.save_button.disable()
                if (
                    len(clan_obj.warrior_focus_arg) >= 1
                    and not self.save_button.is_enabled
                ):
                    self.save_button.enable()

        return super().process_event(event)

# TODO
class ConfirmDisplayChanges(UIMessageWindow):
    def __init__(self):
        super().__init__(
            rect=ui_scale(rect=pygame.Rect((275, 270), (250, 160)), scale=screen_manager.window_scale),
            html_message="This is a test!",
            manager=screen_manager.uim,
            object_id="#confirm_display_changes_window",
            always_on_top=True,
        )
        self.set_blocking(True)

        self.dismiss_button.kill()
        self.text_block.kill()

        button_size = (-1, 30)
        button_spacing = 10
        button_vertical_space = (button_spacing * 2) + button_size[1]

        dismiss_button_rect = ui_scale(rect=pygame.Rect((0, 0), (140, 30)), scale=screen_manager.window_scale)
        dismiss_button_rect.bottomright = ui_scale_offset(
            (-button_spacing, -button_spacing)
        )

        self.dismiss_button = UISurfaceImageButton(
            dismiss_button_rect,
            "windows.confirm_changes",
            image_dict=get_button_dict(ButtonStyle.SquOval, (140, 30),
                                       scale=screen_manager.window_scale),
            manager=screen_manager.uim,
            screen_manager=screen_manager,
            container=self,
            object_id="@ButtonStyle_squoval",
            anchors={
                "left": "right",
                "top": "bottom",
                "right": "right",
                "bottom": "bottom",
            },
        )

        revert_rect = ui_scale(rect=pygame.Rect((0, 0), (75, 30)), scale=screen_manager.window_scale)
        revert_rect.bottomleft = ui_scale_offset((button_spacing, -button_spacing))

        self.revert_button = UISurfaceImageButton(
            revert_rect,
            "windows.revert",
            image_dict=get_button_dict(ButtonStyle.SquOval, (75, 30),
                                       scale=screen_manager.window_scale),
            manager=screen_manager.uim,
            screen_manager=screen_manager,
            container=self,
            object_id="@ButtonStyle_squoval",
            anchors={
                "left": "left",
                "bottom": "bottom",
            },
        )

        rect = ui_scale(rect=pygame.Rect((0, 0), (22, 22)), scale=screen_manager.window_scale)
        rect.topright = ui_scale_offset((-5, 7))
        self.back_button = UIImageButton(
            rect,
            "",
            object_id="#exit_window_button",
            screen_manager=screen_manager,
            container=self,
            visible=True,
            anchors={"top": "top", "right": "right"},
        )

        text_block_rect = pygame.Rect(
            ui_scale_offset((0, 22)),
            (
                self.get_container().get_size()[0],
                self.get_container().get_size()[1] - button_vertical_space,
            ),
        )
        self.text_block = pygame_gui.elements.UITextBox(
            html_text="windows.display_change_confirm",
            relative_rect=text_block_rect,
            manager=screen_manager.uim,
            object_id="#text_box_30_horizcenter",
            container=self,
            anchors={
                "left": "left",
                "top": "top",
                "right": "right",
                "bottom": "bottom",
            },
            text_kwargs={"count": 10},
        )
        self.text_block.rebuild_from_changed_theme_data()

        # make a timeout that will call in 10 seconds - if this window isn't closed,
        # it'll be used to revert the change
        pygame.time.set_timer(pygame.USEREVENT + 10, 10000, loops=1)

    def revert_changes(self):
        """Revert the changes made to screen scaling"""
        from scripts._red.screens.screen_manager import screen_manager
        screen_manager.toggle_fullscreen()

    def process_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if (
                event.ui_element == self.back_button
                or event.ui_element == self.dismiss_button
            ):
                self.kill()
            elif event.ui_element == self.revert_button:
                self.revert_changes()
        elif event.type == pygame.USEREVENT + 10:
            self.revert_changes()
            self.kill()
        return super().process_event(event)
