# _screen_core.py -

########################################################################################################################
# Imports
########################################################################################################################

import pygame
import pygame_gui
from typing import Optional, Tuple

from definitions import (
    CampKey, ScreenName, Season,
    AVAILABLE_SEASONS,
)
from resources.images.ui_directory import Background, Button, UIElement
from scripts._red.config_manager import config
import scripts.game_structure.screen_settings
from scripts.game_structure import image_cache
from scripts.game_structure.game_essentials import game
from scripts.game_structure.screen_settings import MANAGER
from scripts.ui.ui_elements import UISurfaceImageButton, UIImageButton
from scripts.housekeeping.version import get_version_info
from scripts.ui.generate_box import get_box, BoxStyles
from scripts.ui.generate_button import get_button_dict, ButtonStyles
from scripts.ui.icon import Icon
from scripts.utility import (
    ui_scale,
    ui_scale_offset,
    ui_scale_dimensions,
    ui_scale_blit,
    get_text_box_theme,
    ui_scale_value,
)


########################################################################################################################
# Constants and Paths
########################################################################################################################

game_frame: Optional[pygame.Surface] = None
core_vignette = pygame.image.load(UIElement.CoreVignette.png)
vignette: Optional[pygame.Surface] = None
dropshadow: Optional[pygame.Surface] = None
fade: Optional[pygame.Surface] = None

menu_buttons = dict()

default_game_bgs = None
default_fullscreen_bgs = None

version_number = None
dev_watermark = None

GAME_CONFIG_THEME = config.get_config_value("theme")


########################################################################################################################
# Functions
########################################################################################################################

def rebuild_core(*, should_rebuild_bgs=True):
    global menu_buttons
    global default_game_bgs
    global default_fullscreen_bgs
    global version_number
    global dev_watermark

    # menu buttons are used very often, so they are generated here.
    menu_buttons = dict()

    # they have to be added individually as some of them rely on others in anchors
    menu_buttons[Button.GoScreenEvents] = UISurfaceImageButton(
        ui_scale(pygame.Rect((246, 60), (82, 30))),
        "screens.core.events",
        get_button_dict(ButtonStyles.MENU_LEFT, (82, 30)),
        visible=False,
        manager=MANAGER,
        object_id=pygame_gui.core.ObjectID("#events_button", "@buttonstyles_menu_left"),
        starting_height=5,
    )
    menu_buttons[Button.GoScreenCamp] = UISurfaceImageButton(
        ui_scale(pygame.Rect((0, 60), (58, 30))),
        "screens.core.camp",
        get_button_dict(ButtonStyles.MENU_MIDDLE, (58, 30)),
        visible=False,
        manager=MANAGER,
        object_id="@buttonstyles_menu_middle",
        starting_height=5,
        anchors={"left": "left", "left_target": menu_buttons[ScreenName.Events]},
    )
    menu_buttons[Button.GoScreenCatList] = UISurfaceImageButton(
        ui_scale(pygame.Rect((0, 60), (88, 30))),
        "screens.core.cat_list",
        get_button_dict(ButtonStyles.MENU_MIDDLE, (88, 30)),
        visible=False,
        object_id="@buttonstyles_menu_middle",
        starting_height=5,
        anchors={"left": "left", "left_target": menu_buttons[ScreenName.Camp]},
    )
    menu_buttons[Button.GoScreenPatrol] = UISurfaceImageButton(
        ui_scale(pygame.Rect((0, 60), (80, 30))),
        "screens.core.patrol",
        get_button_dict(ButtonStyles.MENU_RIGHT, (80, 30)),
        visible=False,
        manager=MANAGER,
        object_id="#patrol_button",
        starting_height=5,
        anchors={"left": "left", "left_target": menu_buttons[ScreenName.CatList]},
    )
    menu_buttons[Button.GoScreenMainMenu] = UISurfaceImageButton(
        ui_scale(pygame.Rect((25, 25), (153, 30))),
        "buttons.main_menu",
        get_button_dict(ButtonStyles.SQUOVAL, (153, 30)),
        visible=False,
        manager=MANAGER,
        object_id="@buttonstyles_squoval",
        starting_height=5,
    )

    # used so we can anchor to the right with numbers that make sense
    scale_rect = ui_scale(pygame.Rect((0, 0), (118, 30)))
    scale_rect.topright = ui_scale_offset((-25, 25))
    menu_buttons[Button.GoScreenAllegiances] = UISurfaceImageButton(
        scale_rect,
        "screens.core.allegiances",
        get_button_dict(ButtonStyles.SQUOVAL, (118, 30)),
        visible=False,
        manager=MANAGER,
        object_id=pygame_gui.core.ObjectID(class_id="@image_button", object_id=None),
        starting_height=5,
        anchors={"top": "top", "right": "right"},
    )

    # used so we can anchor to the right with numbers that make sense
    scale_rect = ui_scale(pygame.Rect((0, 0), (85, 30)))
    scale_rect.topright = ui_scale_offset((-25, 5))
    menu_buttons[Button.GoScreenClanSettings] = UISurfaceImageButton(
        scale_rect,
        "screens.core.settings",
        get_button_dict(ButtonStyles.SQUOVAL, (85, 30)),
        visible=False,
        manager=MANAGER,
        object_id=pygame_gui.core.ObjectID(class_id="@image_button", object_id=None),
        starting_height=5,
        anchors={"top_target": menu_buttons[ScreenName.Allegiances], "right": "right"},
    )
    del scale_rect

    heading_rect = ui_scale(pygame.Rect((0, 0), (190, 35)))
    heading_rect.bottomleft = ui_scale_dimensions((0, 0))
    menu_buttons[UIElement.ClanNameHeading] = pygame_gui.elements.UIImage(
        heading_rect,
        pygame.transform.scale(
            image_cache.load_image(UIElement.ClanNameHeading.path).convert_alpha(),
            ui_scale_dimensions((190, 35)),
        ),
        visible=False,
        manager=MANAGER,
        starting_height=5,
        anchors={
            "bottom": "bottom",
            "bottom_target": menu_buttons[ScreenName.Camp],
            "centerx": "centerx",
        },
    )
    # it has to be at least 193 to make "cats outside the clan" fit
    heading_rect = ui_scale(pygame.Rect((0, 0), (193, 35)))
    heading_rect.bottomleft = ui_scale_offset((0, 1))  # yes, this is intentional.
    menu_buttons[Button.DropdownChooseGroup] = pygame_gui.elements.UITextBox(
        "",
        heading_rect,
        visible=False,
        manager=MANAGER,
        object_id=pygame_gui.core.ObjectID(
            "#text_box_34_horizcenter_vertcenter", "#dark"
        ),
        starting_height=5,
        anchors={
            "bottom": "bottom",
            "bottom_target": menu_buttons[ScreenName.Camp],
            "centerx": "centerx",
        },
    )
    del heading_rect

    menu_buttons[UIElement.WidgetMoonsSeasons] = pygame_gui.elements.UIScrollingContainer(
        ui_scale(pygame.Rect((25, 60), (153, 75))),
        visible=False,
        allow_scroll_x=False,
        manager=MANAGER,
        starting_height=5,
    )
    menu_buttons[UIElement.WidgetMoonsSeasonsArrow] = UIImageButton(
        ui_scale(pygame.Rect((174, 80), (22, 34))),
        "",
        visible=False,
        manager=MANAGER,
        object_id="#arrow_mns_button",
        starting_height=5,
    )
    menu_buttons[UIElement.DensBar] = pygame_gui.elements.UIImage(
        ui_scale(pygame.Rect((40, 5), (10, 160))),
        pygame.transform.scale(
            image_cache.load_image(UIElement.DensBar.path).convert_alpha(),
            ui_scale_dimensions((380, 70)),
        ),
        visible=False,
        starting_height=5,
        manager=MANAGER,
        anchors={"top_target": menu_buttons[ScreenName.MainMenu]},
    )
    menu_buttons[Button.DropdownDens] = UISurfaceImageButton(
        ui_scale(pygame.Rect((25, 5), (71, 30))),
        "screens.core.dens",
        get_button_dict(ButtonStyles.SQUOVAL, (71, 30)),
        visible=False,
        manager=MANAGER,
        object_id="@buttonstyles_squoval",
        starting_height=6,
        anchors={"top_target": menu_buttons[ScreenName.MainMenu]},
    )
    menu_buttons[Button.GoScreenLeaderDen] = UISurfaceImageButton(
        ui_scale(pygame.Rect((25, 100), (112, 28))),
        "screens.core.leader_den",
        get_button_dict(ButtonStyles.ROUNDED_RECT, (112, 28)),
        visible=False,
        manager=MANAGER,
        object_id="@buttonstyles_rounded_rect",
        starting_height=6,
    )
    menu_buttons[Button.GoScreenHealerDen] = UISurfaceImageButton(
        ui_scale(pygame.Rect((25, 140), (151, 28))),
        "screens.core.medicine_cat_den",
        get_button_dict(ButtonStyles.ROUNDED_RECT, (151, 28)),
        object_id="@buttonstyles_rounded_rect",
        visible=False,
        manager=MANAGER,
        starting_height=6,
    )
    menu_buttons[Button.GoScreenWarriorsDen] = UISurfaceImageButton(
        ui_scale(pygame.Rect((25, 180), (121, 28))),
        "screens.core.warriors_den",
        get_button_dict(ButtonStyles.ROUNDED_RECT, (121, 28)),
        object_id="@buttonstyles_rounded_rect",
        visible=False,
        manager=MANAGER,
        starting_height=6,
    )
    menu_buttons[Button.GoScreenClearing] = UISurfaceImageButton(
        ui_scale(pygame.Rect((25, 220), (81, 28))),
        "screens.core.clearing",
        get_button_dict(ButtonStyles.ROUNDED_RECT, (81, 28)),
        visible=False,
        manager=MANAGER,
        object_id="@buttonstyles_rounded_rect",
        starting_height=6,
    )

    rebuild_mute("default")

    version_number = pygame_gui.elements.UILabel(
        ui_scale(pygame.Rect((50, 50), (-1, -1))),
        get_version_info().version_number[0:8],
        object_id=get_text_box_theme(),
        anchors={"bottom": "bottom", "right": "right"},
    )
    # Adjust position
    version_number.set_relative_position(
        ui_scale_offset(
            (
                800 - version_number.get_relative_rect()[2],
                700 - version_number.get_relative_rect()[3],
            )
        )
    )

    if get_version_info().is_source_build or get_version_info().is_dev:
        dev_watermark = pygame_gui.elements.UILabel(
            ui_scale(pygame.Rect((525, 660), (300, 50))),
            "screens.core.dev_watermark",
            object_id="#dev_watermark",
            text_kwargs={"ver": version_number.text},
        )
        version_number.kill()
        version_number = None

    if should_rebuild_bgs:
        rebuild_bgs()


def rebuild_mute(location: str):
    if Button.Mute in menu_buttons:
        menu_buttons[Button.Mute].kill()
        menu_buttons[Button.Unmute].kill()

    mute_pos = ui_scale(pygame.Rect((0, 0), (34, 34)))

    if location in ["bottomright", "default"]:
        mute_pos.bottomright = ui_scale_offset((-25, -25))
        anchors = {"bottom": "bottom", "right": "right"}
    elif location == "topright":
        mute_pos.topright = ui_scale_offset((-25, 25))
        anchors = {"top": "top", "right": "right"}
    elif location == "bottomleft":
        mute_pos.bottomleft = ui_scale_offset((25, -25))
        anchors = {"bottom": "bottom", "left": "left"}
    elif location == "topleft":
        mute_pos.topleft = ui_scale_offset((25, 25))
        anchors = {"top": "top", "left": "left"}
    else:
        return

    menu_buttons[Button.Mute] = UISurfaceImageButton(
        mute_pos,
        Icon.SPEAKER,
        get_button_dict(ButtonStyles.ICON, (34, 34)),
        visible=False,
        manager=MANAGER,
        object_id="@buttonstyles_icon",
        starting_height=6,
        anchors=anchors,
    )

    menu_buttons[Button.Unmute] = UISurfaceImageButton(
        mute_pos,
        Icon.MUTE,
        get_button_dict(ButtonStyles.ICON, (34, 34)),
        visible=False,
        manager=MANAGER,
        object_id="@buttonstyles_icon",
        starting_height=6,
        anchors=anchors,
    )


def rebuild_bgs():
    global default_fullscreen_bgs
    global default_game_bgs
    global game_frame
    global vignette
    global dropshadow
    global fade

    if (
        vignette is None
        or scripts.game_structure.screen_settings.screen.get_size()
        != vignette.get_size()
    ):
        game_frame = get_box(
            BoxStyles.FRAME,
            (820, 720),
        )

        vignette = pygame.transform.scale(
            core_vignette, scripts.game_structure.screen_settings.screen.get_size()
        ).convert_alpha()

        dropshadow = pygame.Surface(
            scripts.game_structure.screen_settings.screen.get_size(),
            flags=pygame.SRCALPHA,
        )

        fade = pygame.Surface(scripts.game_structure.screen_settings.screen.get_size())
        fade.fill(pygame.Color(113, 113, 111))  # middle grey

        game_box = pygame.Surface(
            (
                scripts.game_structure.screen_settings.screen_x + ui_scale_value(30),
                scripts.game_structure.screen_settings.screen_y + ui_scale_value(30),
            ),
            pygame.SRCALPHA,
        )
        feather_surface(game_box, 15)
        dropshadow.blit(game_box, ui_scale_blit((-15, -15)))
        del game_box

    bg = pygame.Surface(scripts.game_structure.screen_settings.game_screen_size)
    bg.fill(GAME_CONFIG_THEME["light_mode_background"])
    bg_dark = pygame.Surface(scripts.game_structure.screen_settings.game_screen_size)
    bg_dark.fill(GAME_CONFIG_THEME["dark_mode_background"])

    default_game_bgs = {
        "light": {"default": bg},
        "dark": {"default": bg_dark},
    }

    temp_screen_size = scripts.game_structure.screen_settings.screen.get_size()

    default_fullscreen_bgs = {
        "light": {
            "default": pygame.transform.scale(bg, temp_screen_size),
            Background.MenuLogoless: pygame.transform.scale(
                pygame.image.load(Background.MenuLogoless.path).convert(),
                temp_screen_size,
            ),
            Background.StarClanCatsList: pygame.transform.scale(
                pygame.image.load(Background.StarClanCatsList.path).convert_alpha(),
                temp_screen_size,
            ),
            Background.DarkForestCatsList: pygame.transform.scale(
                pygame.image.load(Background.DarkForestCatsList.path).convert_alpha(),
                temp_screen_size,
            ),
            Background.UnknownResidenceCatsList: pygame.transform.scale(
                pygame.image.load(Background.UnknownResidenceCatsList.path).convert(),
                temp_screen_size,
            ),
        },
        "dark": {
            "default": pygame.transform.scale(bg_dark, temp_screen_size),
            Background.MenuLogoless: pygame.transform.scale(
                pygame.image.load(Background.MenuLogoless.path).convert(),
                temp_screen_size,
            ),
            Background.StarClanCatsList: pygame.transform.scale(
                pygame.image.load(Background.StarClanCatsList.path).convert_alpha(),
                temp_screen_size,
            ),
            Background.DarkForestCatsList: pygame.transform.scale(
                pygame.image.load(Background.DarkForestCatsList.path).convert_alpha(),
                temp_screen_size,
            ),
            Background.UnknownResidenceCatsList: pygame.transform.scale(
                pygame.image.load(Background.UnknownResidenceCatsList.path).convert(),
                temp_screen_size,
            ),
        },
    }

    # TODO Make this an enum
    for theme in ["light", "dark"]:
        for name, bg in default_fullscreen_bgs[theme].items():
            if name not in [
                "default",
                Background.MenuLogoless,
                Background.DarkForestCatsList,
                Background.UnknownResidenceCatsList,
                Background.StarClanCatsList,
            ]:
                default_fullscreen_bgs[theme][name] = process_blur_bg(
                    default_fullscreen_bgs[theme][name], theme=theme
                )
            elif name == "default":
                default_fullscreen_bgs[theme][name] = process_blur_bg(
                    default_fullscreen_bgs[theme][name],
                    theme=theme,
                    vignette_strength=0,
                    fade_color=None,
                )
            elif name in [Background.MenuLogoless, Background.DarkForestCatsList, Background.UnknownResidenceCatsList]:
                default_fullscreen_bgs[theme][name] = process_blur_bg(
                    default_fullscreen_bgs[theme][name], theme=theme, blur_radius=10
                )
            elif name == Background.StarClanCatsList:
                default_fullscreen_bgs[theme][name] = process_blur_bg(
                    default_fullscreen_bgs[theme][name], theme=theme, blur_radius=2
                )

    camp_bgs = get_camp_bgs()

    for theme in ["light", "dark"]:
        for name, camp_bg in camp_bgs[theme].items():
            default_fullscreen_bgs[theme][name] = process_blur_bg(camp_bg, theme=theme)


def get_camp_bgs():

    try:
        camp_key: CampKey = game.clan_obj.camp.camp_key
    except AttributeError:
        camp_key = CampKey.ForestClearing

    all_backgrounds = {}
    for light_dark in ["light", "dark"]:
        for season in AVAILABLE_SEASONS:
            all_backgrounds.update({season: camp_key.get_bg_path(season=season, theme=light_dark)})

    return {
        "light": {
            Season.Spring: pygame.transform.scale(
                pygame.image.load(all_backgrounds[Season.Spring]).convert(),
                scripts.game_structure.screen_settings.screen.get_size(),
            ),
            Season.Summer: pygame.transform.scale(
                pygame.image.load(all_backgrounds[Season.Summer]).convert(),
                scripts.game_structure.screen_settings.screen.get_size(),
            ),
            Season.Autumn: pygame.transform.scale(
                pygame.image.load(all_backgrounds[Season.Autumn]).convert(),
                scripts.game_structure.screen_settings.screen.get_size(),
            ),
            Season.Winter: pygame.transform.scale(
                pygame.image.load(all_backgrounds[Season.Winter]).convert(),
                scripts.game_structure.screen_settings.screen.get_size(),
            ),
        },
        "dark": {
            Season.Spring: pygame.transform.scale(
                pygame.image.load(all_backgrounds[Season.Spring]).convert(),
                scripts.game_structure.screen_settings.screen.get_size(),
            ),
            Season.Summer: pygame.transform.scale(
                pygame.image.load(all_backgrounds[Season.Summer]).convert(),
                scripts.game_structure.screen_settings.screen.get_size(),
            ),
            Season.Autumn: pygame.transform.scale(
                pygame.image.load(all_backgrounds[Season.Autumn]).convert(),
                scripts.game_structure.screen_settings.screen.get_size(),
            ),
            Season.Winter: pygame.transform.scale(
                pygame.image.load(all_backgrounds[Season.Winter]).convert(),
                scripts.game_structure.screen_settings.screen.get_size(),
            ),
        },
    }


def process_blur_bg(
    bg,
    theme: str = None,
    blur_radius: Optional[int] = 5,
    vignette_strength: Optional[int] = None,
    fade_color: Optional[Tuple[int, int, int]] = None,
) -> pygame.Surface:
    global vignette
    global fade
    global dropshadow
    if theme is None:
        theme = "dark" if game.settings["dark mode"] else "light"

    fade.fill(GAME_CONFIG_THEME["fullscreen_background"][theme]["fade_color"])
    vignette.set_alpha(
        GAME_CONFIG_THEME["fullscreen_background"][theme]["vignette_alpha"]
    )
    dropshadow.set_alpha(
        GAME_CONFIG_THEME["fullscreen_background"][theme]["dropshadow_alpha"]
    )

    if vignette_strength is not None:
        vignette.set_alpha(vignette_strength)

    bg = pygame.transform.scale(
        bg, scripts.game_structure.screen_settings.screen.get_size()
    ).convert_alpha()

    if blur_radius is not None:
        bg = pygame.transform.box_blur(bg, blur_radius)

    bg.blits(
        (
            (fade, (0, 0), None, pygame.BLEND_MULT),
            (vignette, (0, 0), None),
            (dropshadow, (0, 0), None),
            (game_frame, ui_scale_blit((-10, -10))),
        )
    )

    return bg


def feather_surface(surface, feather_width):
    """
    Run a per-pixel effect to make a fun fade-to-transparent border
    :param surface: The surface to add a feathered edge to
    :param feather_width: How fat to make the edge
    :return: None
    """
    width, height = surface.get_size()
    for x in range(width):
        for y in range(height):
            distance = min(x, y, width - x - 1, height - y - 1)
            if distance < feather_width:
                alpha = int(255 * (distance / feather_width))
                surface.set_at((x, y), (0, 0, 0, alpha))


rebuild_core()
