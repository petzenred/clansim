# ui_utils.py - Utility functions for the user interface.

########################################################################################################################
# Imports
########################################################################################################################

from math import floor

import pygame
from pygame_gui.core import ObjectID

import resources._red.red_filepaths as fp
from definitions import (
    ThemeName,
    AVAILABLE_SEASONS,
    DEFAULT_WINDOW_SIZE_X, DEFAULT_WINDOW_SIZE_Y, DEFAULT_SCREEN_SCALE,
    FULLSCREEN_SCALE_MULT_X, FULLSCREEN_SCALE_MULT_Y, FULLSCREEN_SCALE_ADJ, FULLSCREEN_SCALE_FACTOR,
    WINDOWED_SCALE_MULT_X, WINDOWED_SCALE_MULT_Y, WINDOWED_SCALE_FACTOR, DEFAULT_WINDOW_POS
)
from scripts._red.config_manager import config
# must be done like this to get updates when we change screen size etc
#from scripts._red.screens.screen_manager import screen_manager

import logging
logger = logging.getLogger(__name__)


########################################################################################################################
# Functions
########################################################################################################################

def get_text_box_theme(theme_name=None):
    """ Updates the name of the theme based on dark or light mode """
    if config.settings.Theme is ThemeName.Dark:
        return ObjectID("#dark", theme_name)
    else:
        return theme_name

def ui_scale(rect: pygame.Rect, scale: float = DEFAULT_SCREEN_SCALE):
    """
    Scales a pygame.Rect appropriately for the UI scaling currently in use.
    :param rect: a pygame.Rect
    :param scale: The size of the game window
    :return: the same pygame.Rect, scaled for the current UI.
    """
    # offset can be negative to allow for correct anchoring
    rect[0] = floor(rect[0] * scale)
    rect[1] = floor(rect[1] * scale)
    # if the dimensions are negative, it's dynamically scaled, ignore
    rect[2] = (
        floor(rect[2] * scale)
        if rect[2] > 0
        else rect[2]
    )
    rect[3] = (
        floor(rect[3] * scale)
        if rect[3] > 0
        else rect[3]
    )

    return rect


def ui_scale_blit(coords: tuple[int, int],
                  scale: float = DEFAULT_SCREEN_SCALE,
                  window_pos: tuple[int, int] = DEFAULT_WINDOW_POS):
    """
    Use to scale WHERE to blit an item, not the SIZE of it. (0, 0) is the top left corner of the pygame_gui managed window,
    this adds the offset from fullscreen etc. to make it blit in the right place. Not to be confused with ui_scale_offset.
    :param coords: The coordinates to blit to
    :param scale: The size of the game window
    :param window_pos: The placement of the game window on the computer screen
    :return: The scaled, correctly offset coordinates to blit to.
    """
    return floor(
        coords[0] * scale + window_pos[0]
    ), floor(
        coords[1] * scale + window_pos[1]
    )


def ui_scale_dimensions(dim: tuple[int, int], scale: float = DEFAULT_SCREEN_SCALE):
    """
    Use to scale the dimensions of an item - WILL IGNORE NEGATIVE VALUES
    :param dim: The dimensions to scale
    :param scale: The size of the game window
    :return: The scaled dimensions
    """
    return (
        floor(dim[0] * scale)
        if dim[0] > 0
        else dim[0],
        floor(dim[1] * scale)
        if dim[1] > 0
        else dim[1],
    )


def ui_scale_offset(coords: tuple[int, int], scale: float = DEFAULT_SCREEN_SCALE):
    """
    Use to scale the offset of an item (i.e. the first 2 values of a pygame.Rect).
    Not to be confused with ui_scale_blit.
    :param coords: The coordinates to scale
    :param scale: The size of the game window
    :return: The scaled coordinates
    """
    return (
        floor(coords[0] * scale),
        floor(coords[1] * scale),
    )


def ui_scale_value(val: int, scale: float = DEFAULT_SCREEN_SCALE):
    """
    Use to scale a single value according to the UI scale. If you need this one,
    you're probably doing something unusual. Try to avoid where possible.
    :param val: The value to scale
    :param scale: The size of the game window
    :return: The scaled value
    """
    return floor(val * scale)


def shorten_text_to_fit(
        name,
        length_limit,
        font_size=None,
        font_type=fp.NOTOSANS_FONT.Regular, # FIXME
        scale: float = DEFAULT_SCREEN_SCALE
):
    length_limit = length_limit * scale
    if font_size is None:
        font_size = 15
    font_size = floor(font_size * scale)

    if font_type == fp.CLANGEN_FONT.Name:
        font_type = fp.CLANGEN_FONT.Regular # FIXME
    # Create the font object
    font = pygame.font.Font(font_type, font_size)

    # Add dynamic name lengths by checking the actual width of the text
    total_width = 0
    short_name = ""
    ellipsis_width = font.size("...")[0]
    for index, character in enumerate(name):
        char_width = font.size(character)[0]

        # Check if the current character is the last one and its width is less than or equal to ellipsis_width
        if index == len(name) - 1 and char_width <= ellipsis_width:
            short_name += character
        else:
            total_width += char_width
            if total_width + ellipsis_width > length_limit:
                break
            short_name += character

    # If the name was truncated, add "..."
    if len(short_name) < len(name):
        short_name += "..."

    return short_name
