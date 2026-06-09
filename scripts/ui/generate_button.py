# generate_buttons.py - Functions to create the shape and spacing of buttons.

########################################################################################################################
# Imports
########################################################################################################################

from functools import lru_cache
from math import floor

import pygame

import resources._red.red_filepaths as fp
from definitions import ButtonStyle
from scripts._red.utils.ui_utils import ui_scale_dimensions
from scripts.ui.generate_box import BoxData, get_box


########################################################################################################################
# Constants
########################################################################################################################

buttonstyles = {
        ButtonStyle.MainMenu: {
            "normal": pygame.image.load(fp.BUTTON_MAINMENU_NORMAL).convert_alpha(),
            "hovered": pygame.image.load(fp.BUTTON_MAINMENU_HOVERED).convert_alpha(),
            "selected": pygame.image.load(fp.BUTTON_MAINMENU_NORMAL).convert_alpha(),
            "disabled": pygame.image.load(fp.BUTTON_MAINMENU_DISABLED).convert_alpha(),
            "ninetile": False,
            "scale_only": False,
        },
        ButtonStyle.SquOval: {
            "normal": pygame.image.load(fp.BUTTON_SQUOVAL_NORMAL).convert_alpha(),
            "hovered": pygame.image.load(fp.BUTTON_SQUOVAL_HOVERED).convert_alpha(),
            "selected": pygame.image.load(fp.BUTTON_SQUOVAL_NORMAL).convert_alpha(),
            "disabled": pygame.image.load(fp.BUTTON_SQUOVAL_DISABLED).convert_alpha(),
            "ninetile": False,
            "scale_only": False,
        },
        ButtonStyle.MenuLeft: {
            "normal": pygame.image.load(
                "resources/images/generated_buttons/menu_left_normal.png"
            ).convert_alpha(),
            "hovered": pygame.image.load(
                "resources/images/generated_buttons/menu_left_hovered.png"
            ).convert_alpha(),
            "selected": pygame.image.load(
                "resources/images/generated_buttons/menu_left_normal.png"
            ).convert_alpha(),
            "disabled": pygame.image.load(
                "resources/images/generated_buttons/menu_left_disabled.png"
            ).convert_alpha(),
            "ninetile": False,
            "scale_only": False,
        },
        ButtonStyle.MenuMiddle: {
            "normal": pygame.image.load(
                "resources/images/generated_buttons/menu_middle_normal.png"
            ).convert_alpha(),
            "hovered": pygame.image.load(
                "resources/images/generated_buttons/menu_middle_hovered.png"
            ).convert_alpha(),
            "selected": pygame.image.load(
                "resources/images/generated_buttons/menu_middle_normal.png"
            ).convert_alpha(),
            "disabled": pygame.image.load(
                "resources/images/generated_buttons/menu_middle_disabled.png"
            ).convert_alpha(),
            "ninetile": False,
            "scale_only": False,
        },
        ButtonStyle.MenuRight: {
            "normal": pygame.image.load(
                "resources/images/generated_buttons/menu_right_normal.png"
            ).convert_alpha(),
            "hovered": pygame.image.load(
                "resources/images/generated_buttons/menu_right_hovered.png"
            ).convert_alpha(),
            "selected": pygame.image.load(
                "resources/images/generated_buttons/menu_right_normal.png"
            ).convert_alpha(),
            "disabled": pygame.image.load(
                "resources/images/generated_buttons/menu_right_disabled.png"
            ).convert_alpha(),
            "ninetile": False,
            "scale_only": False,
        },
        ButtonStyle.ProfileLeft: {
            "normal": pygame.image.load(
                "resources/images/generated_buttons/profile_left_normal.png"
            ).convert_alpha(),
            "hovered": pygame.image.load(
                "resources/images/generated_buttons/profile_left_hovered.png"
            ).convert_alpha(),
            "selected": pygame.image.load(
                "resources/images/generated_buttons/profile_left_normal.png"
            ).convert_alpha(),
            "disabled": pygame.image.load(
                "resources/images/generated_buttons/profile_left_disabled.png"
            ).convert_alpha(),
            "ninetile": False,
            "scale_only": False,
        },
        ButtonStyle.ProfileMiddle: {
            "normal": pygame.image.load(
                "resources/images/generated_buttons/profile_middle_normal.png"
            ).convert_alpha(),
            "hovered": pygame.image.load(
                "resources/images/generated_buttons/profile_middle_hovered.png"
            ).convert_alpha(),
            "selected": pygame.image.load(
                "resources/images/generated_buttons/profile_middle_normal.png"
            ).convert_alpha(),
            "disabled": pygame.image.load(
                "resources/images/generated_buttons/profile_middle_disabled.png"
            ).convert_alpha(),
            "ninetile": False,
            "scale_only": False,
        },
        ButtonStyle.ProfileRight: {
            "normal": pygame.image.load(
                "resources/images/generated_buttons/profile_right_normal.png"
            ).convert_alpha(),
            "hovered": pygame.image.load(
                "resources/images/generated_buttons/profile_right_hovered.png"
            ).convert_alpha(),
            "selected": pygame.image.load(
                "resources/images/generated_buttons/profile_right_normal.png"
            ).convert_alpha(),
            "disabled": pygame.image.load(
                "resources/images/generated_buttons/profile_right_disabled.png"
            ).convert_alpha(),
            "ninetile": False,
            "scale_only": False,
        },
        ButtonStyle.RoundedRect: {
            "normal": pygame.image.load(
                "resources/images/generated_buttons/rounded_rect_normal.png"
            ).convert_alpha(),
            "hovered": pygame.image.load(
                "resources/images/generated_buttons/rounded_rect_hovered.png"
            ).convert_alpha(),
            "selected": pygame.image.load(
                "resources/images/generated_buttons/rounded_rect_normal.png"
            ).convert_alpha(),
            "disabled": pygame.image.load(
                "resources/images/generated_buttons/rounded_rect_disabled.png"
            ).convert_alpha(),
            "ninetile": False,
            "scale_only": False,
        },
        ButtonStyle.DropDown: {
            "normal": pygame.image.load(
                "resources/images/generated_buttons/dropdown_normal.png"
            ).convert_alpha(),
            "hovered": pygame.image.load(
                "resources/images/generated_buttons/dropdown_hovered.png"
            ).convert_alpha(),
            "selected": pygame.image.load(
                "resources/images/generated_buttons/dropdown_normal.png"
            ).convert_alpha(),
            "disabled": pygame.image.load(
                "resources/images/generated_buttons/dropdown_disabled.png"
            ).convert_alpha(),
            "ninetile": True,
            "scale_only": False,
        },
        ButtonStyle.HorizontalTab: {
            "normal": pygame.image.load(
                "resources/images/generated_buttons/horizontal_tab_normal.png"
            ).convert_alpha(),
            "hovered": pygame.image.load(
                "resources/images/generated_buttons/horizontal_tab_hovered.png"
            ).convert_alpha(),
            "selected": pygame.image.load(
                "resources/images/generated_buttons/horizontal_tab_normal.png"
            ).convert_alpha(),
            "disabled": pygame.image.load(
                "resources/images/generated_buttons/horizontal_tab_disabled.png"
            ).convert_alpha(),
            "ninetile": False,
            "scale_only": False,
            "tab_movement": {"hovered": False, "disabled": True, "amount": (0, -4)},
        },
        ButtonStyle.HorizontalTabMirrored: {
            "normal": pygame.transform.flip(
                pygame.image.load(
                    "resources/images/generated_buttons/horizontal_tab_normal.png"
                ).convert_alpha(),
                False,
                True,
            ),
            "hovered": pygame.transform.flip(
                pygame.image.load(
                    "resources/images/generated_buttons/horizontal_tab_hovered.png"
                ).convert_alpha(),
                False,
                True,
            ),
            "selected": pygame.transform.flip(
                pygame.image.load(
                    "resources/images/generated_buttons/horizontal_tab_normal.png"
                ).convert_alpha(),
                False,
                True,
            ),
            "disabled": pygame.transform.flip(
                pygame.image.load(
                    "resources/images/generated_buttons/horizontal_tab_disabled.png"
                ).convert_alpha(),
                False,
                True,
            ),
            "ninetile": False,
            "scale_only": False,
            "tab_movement": {"hovered": False, "disabled": True, "amount": (0, 4)},
        },
        ButtonStyle.VerticalTab: {
            "normal": pygame.image.load(
                "resources/images/generated_buttons/vertical_tab_normal.png"
            ).convert_alpha(),
            "hovered": pygame.image.load(
                "resources/images/generated_buttons/vertical_tab_hovered.png"
            ).convert_alpha(),
            "selected": pygame.image.load(
                "resources/images/generated_buttons/vertical_tab_normal.png"
            ).convert_alpha(),
            "disabled": pygame.image.load(
                "resources/images/generated_buttons/vertical_tab_disabled.png"
            ).convert_alpha(),
            "ninetile": False,
            "scale_only": False,
            "tab_movement": {"hovered": True, "disabled": False, "amount": (10, 0)},
        },
        ButtonStyle.LadderTop: {
            "normal": pygame.image.load(
                "resources/images/generated_buttons/ladder_top_normal.png"
            ).convert_alpha(),
            "hovered": pygame.image.load(
                "resources/images/generated_buttons/ladder_top_hovered.png"
            ).convert_alpha(),
            "selected": pygame.image.load(
                "resources/images/generated_buttons/ladder_top_normal.png"
            ).convert_alpha(),
            "disabled": pygame.image.load(
                "resources/images/generated_buttons/ladder_top_disabled.png"
            ).convert_alpha(),
            "ninetile": True,
            "scale_only": False,
        },
        ButtonStyle.LadderMiddle: {
            "normal": pygame.image.load(
                "resources/images/generated_buttons/ladder_middle_normal.png"
            ).convert_alpha(),
            "hovered": pygame.image.load(
                "resources/images/generated_buttons/ladder_middle_hovered.png"
            ).convert_alpha(),
            "selected": pygame.image.load(
                "resources/images/generated_buttons/ladder_middle_normal.png"
            ).convert_alpha(),
            "disabled": pygame.image.load(
                "resources/images/generated_buttons/ladder_middle_disabled.png"
            ).convert_alpha(),
            "ninetile": True,
            "scale_only": False,
        },
        ButtonStyle.LadderBottom: {
            "normal": pygame.image.load(
                "resources/images/generated_buttons/ladder_bottom_normal.png"
            ).convert_alpha(),
            "hovered": pygame.image.load(
                "resources/images/generated_buttons/ladder_bottom_hovered.png"
            ).convert_alpha(),
            "selected": pygame.image.load(
                "resources/images/generated_buttons/ladder_bottom_normal.png"
            ).convert_alpha(),
            "disabled": pygame.image.load(
                "resources/images/generated_buttons/ladder_bottom_disabled.png"
            ).convert_alpha(),
            "ninetile": True,
            "scale_only": False,
        },
        ButtonStyle.Icon: {
            "normal": pygame.image.load(
                "resources/images/generated_buttons/icon_normal.png"
            ).convert_alpha(),
            "hovered": pygame.image.load(
                "resources/images/generated_buttons/icon_hovered.png"
            ).convert_alpha(),
            "selected": pygame.image.load(
                "resources/images/generated_buttons/icon_normal.png"
            ).convert_alpha(),
            "disabled": pygame.image.load(
                "resources/images/generated_buttons/icon_disabled.png"
            ).convert_alpha(),
            "ninetile": False,
            "scale_only": True,
        },
        ButtonStyle.IconTabTop: {
            "ninetile": True,
            "scale_only": False,
            "tab_movement": {"hovered": True, "disabled": True, "amount": (0, -4)},
        },
        ButtonStyle.IconTabLeft: {
            "ninetile": True,
            "scale_only": False,
            "tab_movement": {"hovered": True, "disabled": True, "amount": (-4, 0)},
        },
        ButtonStyle.IconTabBottom: {
            "ninetile": True,
            "scale_only": False,
            "tab_movement": {"hovered": True, "disabled": True, "amount": (0, 4)},
        },
        ButtonStyle.IconTabRight: {
            "ninetile": True,
            "scale_only": False,
            "tab_movement": {"hovered": True, "disabled": True, "amount": (4, 0)},
        },
    }


########################################################################################################################
# Functions
########################################################################################################################

def __separate_icon_tabs() -> tuple[str, str, dict[str, dict[str, pygame.Surface]]]:
    """ A separate helper method to build the icon tabs since I shoved them all in one file. It just made sense, ok?

    :return: a generator for the tab, status and associated surface
    """
    source = pygame.image.load(fp.ICON_TAB).convert_alpha()
    tab_size = source.get_width() // 3
    for y, fun_tab in enumerate(
        [ButtonStyle.IconTabTop, ButtonStyle.IconTabLeft, ButtonStyle.IconTabBottom, ButtonStyle.IconTabRight], start=0
    ):
        for x, fun_status in enumerate(["normal", "hovered", "disabled"], start=0):
            yield fun_tab, fun_status, source.subsurface(
                (x * tab_size, y * tab_size, tab_size, tab_size)
            )


for tab, status, butt_surface in __separate_icon_tabs():
    if "normal" in buttonstyles[tab] and "selected" not in buttonstyles[tab]:
        buttonstyles[tab]["selected"] = buttonstyles[tab]["normal"]
    buttonstyles[tab][status] = butt_surface


def get_button_dict(style: ButtonStyle, 
                    unscaled_dimensions: tuple[int, int], 
                    *, 
                    static=False,
                    scale: float
) -> dict[str, pygame.Surface]:
    """ Return a dictionary of surfaces suitable for passing into a UISurfaceImageButton.

    :param ButtonStyle style: ButtonStyle style required for the button
    :param tuple[int, int] unscaled_dimensions: UNSCALED dimensions of the button
    :param bool static: whether to return only the normal surface, or the hovered & disabled surfaces as well | False
    :param float scale: current game window scale

    :return: A dictionary of surfaces
    """
    return _get_button_dict(
        style=style,
        unscaled_dimensions=unscaled_dimensions,
        static=static,
        scale=scale,
    )


@lru_cache(maxsize=None)
def _get_button_dict(
    style: ButtonStyle, unscaled_dimensions: tuple[int, int], static, scale
) -> dict[str, pygame.Surface]:
    """ This wrapper exists so that we can cache the values to make toggling quicker.

    :param ButtonStyle style: ButtonStyle style required for the button
    :param tuple[int, int] unscaled_dimensions: The UNSCALED dimensions of the button
    :param bool static: whether to return only the normal surface, default False
    :param float scale: current game window scale

    :return: A dictionary of surfaces
    """

    # scale exists pretty much only to ensure we have a different cached version of the function for different scales
    dontdeletethatpls = scale

    if buttonstyles[style.value]["scale_only"]:
        if static:
            return {
                "normal": pygame.transform.scale(
                    buttonstyles[style.value]["normal"],
                    ui_scale_dimensions(dim=unscaled_dimensions, scale=scale),
                )
            }
        return {
            "normal": pygame.transform.scale(
                buttonstyles[style.value]["normal"],
                ui_scale_dimensions(dim=unscaled_dimensions, scale=scale),
            ),
            "hovered": pygame.transform.scale(
                buttonstyles[style.value]["hovered"],
                ui_scale_dimensions(dim=unscaled_dimensions, scale=scale),
            ),
            "selected": pygame.transform.scale(
                buttonstyles[style.value]["selected"],
                ui_scale_dimensions(dim=unscaled_dimensions, scale=scale),
            ),
            "disabled": pygame.transform.scale(
                buttonstyles[style.value]["disabled"],
                ui_scale_dimensions(dim=unscaled_dimensions, scale=scale),
            ),
        }

    if buttonstyles[style.value]["ninetile"]:
        if static:
            return {
                "normal": get_box(
                    BoxData(
                        style.value + "_normal",
                        buttonstyles[style.value]["normal"],
                        (3, 3),
                    ),
                    unscaled_dimensions,
                )
            }
        return {
            "normal": get_box(
                BoxData(
                    style.value + "_normal", buttonstyles[style.value]["normal"], (3, 3)
                ),
                unscaled_dimensions,
            ),
            "hovered": get_box(
                BoxData(
                    style.value + "_hovered",
                    buttonstyles[style.value]["hovered"],
                    (3, 3),
                ),
                unscaled_dimensions,
            ),
            "selected": get_box(
                BoxData(
                    style.value + "_selected",
                    buttonstyles[style.value]["selected"],
                    (3, 3),
                ),
                unscaled_dimensions,
            ),
            "disabled": get_box(
                BoxData(
                    style.value + "_disabled",
                    buttonstyles[style.value]["disabled"],
                    (3, 3),
                ),
                unscaled_dimensions,
            ),
        }

    if static:
        return {
            "normal": _generate_button(buttonstyles[style.value]["normal"],
                                       ui_scale_dimensions(dim=unscaled_dimensions, scale=scale))
        }

    return {
        "normal": _generate_button(buttonstyles[style.value]["normal"],
                                   ui_scale_dimensions(dim=unscaled_dimensions, scale=scale)),
        "hovered": _generate_button(buttonstyles[style.value]["hovered"],
                                    ui_scale_dimensions(dim=unscaled_dimensions, scale=scale)),
        "selected": _generate_button(buttonstyles[style.value]["selected"],
                                     ui_scale_dimensions(dim=unscaled_dimensions, scale=scale)),
        "disabled": _generate_button(buttonstyles[style.value]["disabled"],
                                     ui_scale_dimensions(dim=unscaled_dimensions, scale=scale)),
    }


def _generate_button(base: pygame.Surface, scaled_dimensions: tuple[int, int]):
    """ Generate a surface of arbitrary length from a given input surface

    :param base: the Surface to generate from
    :param scaled_dimensions: the SCALED dimensions of the final button

    :return: A surface of the correct dimensions, scaled automatically
    """
    height = base.get_height()
    vertical_scale = scaled_dimensions[1] / height
    if vertical_scale < 0:
        vertical_scale = 1 / -vertical_scale

    left = base.subsurface((0, 0), (height, height))
    middle = base.subsurface((height, 0), (height, height))
    right = base.subsurface((height * 2, 0), (height, height))
    if vertical_scale == 0:
        pass
    else:
        scale = (scaled_dimensions[1], scaled_dimensions[1])
        left = pygame.transform.scale(left, scale)
        middle = pygame.transform.scale(middle, scale)
        right = pygame.transform.scale(right, scale)
        height = middle.get_height()
    del vertical_scale
    width_bookends = height * 2

    # if we need the middle segment
    if scaled_dimensions[0] - width_bookends > 0:
        middle = pygame.transform.scale(
            middle, (scaled_dimensions[0] - width_bookends, middle.get_height())
        )
        surface = pygame.Surface(scaled_dimensions, pygame.SRCALPHA)
        surface.convert_alpha()
        surface.fblits(
            (
                (left, (0, 0)),
                (middle, (left.get_width(), 0)),
                (right, (scaled_dimensions[0] - height, 0)),
            )
        )
    else:
        # if it's too small for us to put middle in there, just don't :)
        excess_width = left.get_width() * 2 - scaled_dimensions[0]
        surface = pygame.Surface(scaled_dimensions, pygame.SRCALPHA)
        surface.convert_alpha()
        excess = height - excess_width / 2
        if excess % 1 != 0:
            left_excess = floor(excess) + 1
            right_excess = floor(excess)
        else:
            left_excess = excess
            right_excess = excess
        surface.blits(
            (
                (
                    left,
                    (0, 0),
                    pygame.Rect((0, 0), (left_excess, height)),
                ),
                (
                    right,
                    (left_excess, 0),
                    pygame.Rect(
                        excess_width // 2,
                        0,
                        right_excess,
                        height,
                    ),
                ),
            )
        )

    return surface
