# generate_box.py - Generate the shape, size, and spacing of UI elements.

########################################################################################################################
# Imports
########################################################################################################################

from dataclasses import dataclass
from functools import lru_cache
from math import ceil, floor
from typing import Optional

import pygame

import resources._red.red_filepaths as fp
from definitions import BoxShape
from scripts._red.utils.ui_utils import ui_scale_value, ui_scale_dimensions


########################################################################################################################
# Classes
########################################################################################################################

@dataclass(unsafe_hash=True)
class BoxData:
    name: str
    surface: pygame.Surface
    tilecount: tuple[int, int]


@dataclass
class Tileset:
    edge_length: int = 0
    ninetile: bool = True
    topleft: pygame.Surface = None
    top: pygame.Surface = None
    topright: pygame.Surface = None
    left: pygame.Surface = None
    middle: pygame.Surface = None
    right: pygame.Surface = None
    bottomleft: pygame.Surface = None
    bottom: pygame.Surface = None
    bottomright: pygame.Surface = None

    top_noborder: Optional[pygame.Surface] = None
    right_noborder: Optional[pygame.Surface] = None
    bottom_noborder: Optional[pygame.Surface] = None
    left_noborder: Optional[pygame.Surface] = None

    topleft_notop: Optional[pygame.Surface] = None
    topleft_noleft: Optional[pygame.Surface] = None
    topright_notop: Optional[pygame.Surface] = None
    topright_noright: Optional[pygame.Surface] = None
    bottomleft_nobottom: Optional[pygame.Surface] = None
    bottomleft_noleft: Optional[pygame.Surface] = None
    bottomright_nobottom: Optional[pygame.Surface] = None
    bottomright_noright: Optional[pygame.Surface] = None


########################################################################################################################
# Constants
########################################################################################################################

tilesets: dict[float, dict[BoxData, Tileset]] = {}


########################################################################################################################
# Functions
########################################################################################################################

def get_box(
    scale: float,
    style: BoxShape | BoxData,
    unscaled_dimensions: tuple[int, int],
    sides=True,
    use_extra_if_available: bool = True,
) -> pygame.Surface:
    """
    Generate a surface of arbitrary length and height from a given input surface

    :param float scale: current game window scale
    :param style: BoxShape style to create from, or BoxData to draw from
    :param tuple[int, int] unscaled_dimensions: SCALED dimensions of the final box # FIXME scaled or unscaled??
    :param bool sides: whether to render the sides of the box or just end it abruptly.
        tuple of booleans in order: Top, right, bottom, left. Also accepts a single boolean for all 4 values
    :param bool use_extra_if_available:whether to use the expanded tileset if the style has it. Default True.

    :return: A surface
    """

    if style is BoxShape.Frame:
        style = BoxData(
            "frame",
            pygame.image.load(fp.GENERATED_BOX_FRAME).convert_alpha(),
            (3, 3),
        )
    if style is BoxShape.RoundedBox:
        style = BoxData(
            "rounded_box",
            pygame.image.load(fp.GENERATED_BOX_ROUNDED_BOX).convert_alpha(),
            (7, 3),
        )

    return _get_box(
        style=style,
        scaled_dimensions=ui_scale_dimensions(dim=unscaled_dimensions, scale=scale),
        sides=sides,
        use_extra_if_available=use_extra_if_available,
        scale=scale,
    )


@lru_cache(maxsize=None)
def _get_box(
    style: BoxData,
    scaled_dimensions: tuple[int, int],
    sides: bool | tuple[bool, bool, bool, bool] = True,
    use_extra_if_available=True,
    *,
    scale: float
) -> pygame.Surface:
    """
    A wrapper for get_box that lets it be typehinted & still cache properly
    :param style:
    :param scaled_dimensions:
    :return:
    """

    # scale literally just exists for the sake of caching, just leave it be
    notouchytouchyeverpls = scale

    tileset = _build_needed_tileset(
        style=style, sides=sides, scale=scale, use_extra_if_available=use_extra_if_available
    )

    tiny_box = False  # a flag to determine whether the box is technically too small
    tiny_box_dimensions = {}

    if scaled_dimensions[0] < tileset.edge_length * 2:
        tiny_box = True
        new_x = scaled_dimensions[0] / 2
        x_left = floor(new_x)
        x_right = ceil(new_x)

        tileset.topleft = tileset.topleft.subsurface(
            pygame.Rect(0, 0, x_left, tileset.edge_length)
        )
        tileset.left = tileset.left.subsurface(
            pygame.Rect(0, 0, x_left, tileset.edge_length)
        )
        tileset.bottomleft = tileset.bottomleft.subsurface(
            pygame.Rect(0, 0, x_left, tileset.edge_length)
        )

        tileset.topright = tileset.topright.subsurface(
            pygame.Rect(tileset.edge_length - x_right, 0, x_right, tileset.edge_length)
        )
        tileset.right = tileset.right.subsurface(
            pygame.Rect(tileset.edge_length - x_right, 0, x_right, tileset.edge_length)
        )
        tileset.bottomright = tileset.bottomright.subsurface(
            pygame.Rect(tileset.edge_length - x_right, 0, x_right, tileset.edge_length)
        )

    if scaled_dimensions[1] < tileset.edge_length * 2:
        tiny_box = True
        new_y = scaled_dimensions[1] / 2
        y_top = floor(new_y)
        y_bottom = ceil(new_y)
        tileset.topleft = tileset.topleft.subsurface(
            pygame.Rect(0, 0, tileset.topleft.get_width(), y_top)
        )
        tileset.top = tileset.top.subsurface(
            pygame.Rect(0, 0, tileset.topleft.get_width(), y_top)
        )
        tileset.topright = tileset.topright.subsurface(
            pygame.Rect(0, 0, tileset.topleft.get_width(), y_top)
        )

        tileset.bottomleft = tileset.bottomleft.subsurface(
            pygame.Rect(
                0,
                tileset.edge_length - y_bottom,
                tileset.bottomleft.get_width(),
                y_bottom,
            )
        )
        tileset.bottom = tileset.bottom.subsurface(
            pygame.Rect(
                0,
                tileset.edge_length - y_bottom,
                tileset.bottomleft.get_width(),
                y_bottom,
            )
        )

        tileset.bottomright = tileset.bottomright.subsurface(
            pygame.Rect(
                0,
                tileset.edge_length - y_bottom,
                tileset.bottomleft.get_width(),
                y_bottom,
            )
        )

    # the number of tiles we need to make the desired size
    tilecount = (
        scaled_dimensions[0] // tileset.edge_length,
        scaled_dimensions[1] // tileset.edge_length,
    )

    # not all requests will be clean multiples of the tile size. this fixes that.
    # it's already handled in tinybox calculations so no need to redo it here if it's smol
    extra_width = (
        0
        if tileset.topleft.get_width() != tileset.edge_length
        else scaled_dimensions[0] % tileset.edge_length
    )
    extra_height = (
        0
        if tileset.topleft.get_height() != tileset.edge_length
        else scaled_dimensions[1] % tileset.edge_length
    )

    extra_width_tiles = (
        None
        if extra_width == 0
        else {
            "top": tileset.top.subsurface(
                (0, 0), (extra_width, tileset.top.get_height())
            ),
            "middle": tileset.middle.subsurface(
                (0, 0), (extra_width, tileset.middle.get_height())
            ),
            "bottom": tileset.bottom.subsurface(
                (0, 0), (extra_width, tileset.bottom.get_height())
            ),
        }
    )

    extra_height_tiles = (
        None
        if extra_height == 0
        else {
            "left": tileset.left.subsurface(
                (0, 0), (tileset.edge_length, extra_height)
            ),
            "middle": tileset.middle.subsurface(
                ((0, 0), (tileset.edge_length, extra_height))
            ),
            "right": tileset.right.subsurface(
                ((0, 0), (tileset.edge_length, extra_height))
            ),
        }
    )

    extra_corner_tile = (
        tileset.middle.subsurface(
            (0, 0),
            (extra_width, extra_height),
        )
        if extra_width != 0 and extra_height != 0
        else None
    )

    # okay, here's how the nine-tile system works. check the comments to see
    # which tile is being referred to in each part of this awful construction

    #      0     1     *     2
    #   |-----|-----|-----|-----|
    # 0 |  A  |  B  |  *  |  C  |
    #   |-----|-----|-----|-----|
    # 1 |  D  |  E  |  *  |  F  |
    #   |-----|-----|-----|-----|
    # * |  *  |  *  |  *  |  *  |
    #   |-----|-----|-----|-----|
    # 2 |  G  |  H  |  *  |  I  |
    #   |-----|-----|-----|-----|

    # asterisk = extra, cut-off tile to make up full desired size

    row_length = tilecount[0] + (1 if extra_width_tiles is not None else 0)
    row_x = [x * tileset.edge_length for x in range(row_length - 1)]
    if extra_width_tiles is not None:
        row_x.append(row_x[-1] + extra_width)
    else:
        row_x.append(row_x[-1] + tileset.edge_length)

    # AB*C
    top_row = (
        [tileset.topleft]
        + [tileset.top] * (tilecount[0] - 2)
        + (
            [extra_width_tiles["top"]] + [tileset.topright]
            if extra_width_tiles is not None
            else [tileset.topright]
        )
    )
    coords = [(x, 0) for x in row_x]
    top_row = tuple(zip(top_row, coords))

    # DE*F
    middle_row = (
        [tileset.left]
        + [tileset.middle] * (tilecount[0] - 2)
        + (
            [extra_width_tiles["middle"]] + [tileset.right]
            if extra_width_tiles is not None
            else [tileset.right]
        )
    )

    # ****
    extra_row = (
        (
            [extra_height_tiles["left"]]
            + [extra_height_tiles["middle"]] * (tilecount[0] - 2)
            + (
                [extra_corner_tile] + [extra_height_tiles["right"]]
                if extra_width_tiles is not None
                else [extra_height_tiles["right"]]
            )
        )
        if extra_height_tiles is not None
        else None
    )

    # GH*I
    bottom_row = (
        [tileset.bottomleft]
        + [tileset.bottom] * (tilecount[0] - 2)
        + (
            [extra_width_tiles["bottom"]] + [tileset.bottomright]
            if extra_width_tiles is not None
            else [tileset.bottomright]
        )
    )

    coords = [
        (x, scaled_dimensions[1] - tileset.bottomleft.get_height()) for x in row_x
    ]
    bottom_row = tuple(zip(bottom_row, coords))

    # ok time to build this ungodly contraption.
    surface = pygame.Surface(scaled_dimensions, flags=pygame.SRCALPHA)

    surface.fblits(top_row)

    if not tiny_box:
        for i in range(1, tilecount[1] - 1):
            coords = [(x, i * tileset.edge_length) for x in row_x]
            row = tuple(zip(middle_row, coords))
            surface.fblits(row)
    if extra_row is not None:
        coords = [
            (x, scaled_dimensions[1] - tileset.bottomleft.get_height() - extra_height)
            for x in row_x
        ]
        extra_row = tuple(zip(extra_row, coords))
        surface.fblits(extra_row)

    surface.fblits(bottom_row)

    return surface


def _build_needed_tileset(
    style: BoxData,
    sides: bool | tuple[bool, bool, bool, bool],
    scale: float,
    use_extra_if_available: bool = True,
):
    if isinstance(sides, bool):
        border_top = sides
        border_right = sides
        border_bottom = sides
        border_left = sides
    elif isinstance(sides, tuple):
        border_top, border_right, border_bottom, border_left = sides
    else:
        raise Exception("invalid sides argument supplied")

    tileset = _get_tileset(style=style, temp_scale=scale)

    output = Tileset(edge_length=tileset.edge_length, ninetile=tileset.ninetile)

    output.top = _handle_edges(
        {
            "border": tileset.top,
            "noborder": tileset.top_noborder,
            "middle": tileset.middle,
        },
        border_top,
        use_extra_if_available,
    )

    output.topleft = _handle_corners(
        {
            "all": tileset.topleft,
            "middle": tileset.middle,
            "side1": tileset.top,
            "side2": tileset.left,
            "noside1": tileset.topleft_notop,
            "noside2": tileset.topleft_noleft,
        },
        border_top,
        border_left,
        use_extra_if_available,
    )

    output.topright = _handle_corners(
        {
            "all": tileset.topright,
            "middle": tileset.middle,
            "side1": tileset.top,
            "side2": tileset.right,
            "noside1": tileset.topright_notop,
            "noside2": tileset.topright_noright,
        },
        border_top,
        border_right,
        use_extra_if_available,
    )

    if not tileset.ninetile:
        return output

    output.middle = tileset.middle
    output.left = _handle_edges(
        {
            "border": tileset.left,
            "noborder": tileset.left_noborder,
            "middle": tileset.middle,
        },
        border_left,
        use_extra_if_available,
    )
    output.right = _handle_edges(
        {
            "border": tileset.right,
            "noborder": tileset.right_noborder,
            "middle": tileset.middle,
        },
        border_right,
        use_extra_if_available,
    )

    output.bottom = _handle_edges(
        {
            "border": tileset.bottom,
            "noborder": tileset.bottom_noborder,
            "middle": tileset.middle,
        },
        border_bottom,
        use_extra_if_available,
    )
    output.bottomleft = _handle_corners(
        {
            "all": tileset.bottomleft,
            "middle": tileset.middle,
            "side1": tileset.bottom,
            "side2": tileset.left,
            "noside1": tileset.bottomleft_nobottom,
            "noside2": tileset.bottomleft_noleft,
        },
        border_bottom,
        border_left,
        use_extra_if_available,
    )

    output.bottomright = _handle_corners(
        {
            "all": tileset.bottomright,
            "middle": tileset.middle,
            "side1": tileset.bottom,
            "side2": tileset.right,
            "noside1": tileset.bottomright_nobottom,
            "noside2": tileset.bottomright_noright,
        },
        border_bottom,
        border_right,
        use_extra_if_available,
    )

    return output


def _get_tileset(style: BoxData, temp_scale: float) -> Tileset:
    if temp_scale in tilesets and style.name in tilesets[temp_scale]:
        return tilesets[temp_scale][style]

    surface = style.surface

    # ceiling to the nearest multiple of the tilecount
    width = (
        ceil(ui_scale_value(val=surface.get_width(), scale=temp_scale) / style.tilecount[0])
        * style.tilecount[0]
    )
    height = (
        ceil(ui_scale_value(val=surface.get_height(), scale=temp_scale) / style.tilecount[1])
        * style.tilecount[1]
    )

    scaled_base = pygame.transform.scale(surface, (width, height))

    tile_edge_length = round(height / style.tilecount[1])
    tile_size = (tile_edge_length, tile_edge_length)
    ninetile = True

    # make the tiles
    topleft = _get_tile_from_coords(scaled_base, (0, 0), tile_size)
    top = _get_tile_from_coords(scaled_base, (1, 0), tile_size)
    topright = _get_tile_from_coords(scaled_base, (2, 0), tile_size)

    if style.tilecount[1] > 1:
        left = _get_tile_from_coords(scaled_base, (0, 1), tile_size)
        middle = _get_tile_from_coords(scaled_base, (1, 1), tile_size)
        right = _get_tile_from_coords(scaled_base, (2, 1), tile_size)
        bottomleft = _get_tile_from_coords(scaled_base, (0, 2), tile_size)
        bottom = _get_tile_from_coords(scaled_base, (1, 2), tile_size)
        bottomright = _get_tile_from_coords(scaled_base, (2, 2), tile_size)
    else:
        left, middle, right, bottomleft, bottom, bottomright = [None] * 6
        ninetile = False

    try:
        topleft_notop = _get_tile_from_coords(scaled_base, (3, 0), tile_size)
        topleft_noleft = _get_tile_from_coords(scaled_base, (3, 1), tile_size)
        top_noborder = _get_tile_from_coords(scaled_base, (3, 2), tile_size)
        topright_notop = _get_tile_from_coords(scaled_base, (4, 0), tile_size)
        topright_noright = _get_tile_from_coords(scaled_base, (4, 1), tile_size)
        right_noborder = _get_tile_from_coords(scaled_base, (4, 2), tile_size)
        bottomleft_nobottom = _get_tile_from_coords(scaled_base, (5, 0), tile_size)
        bottomleft_noleft = _get_tile_from_coords(scaled_base, (5, 1), tile_size)
        bottom_noborder = _get_tile_from_coords(scaled_base, (5, 2), tile_size)
        bottomright_nobottom = _get_tile_from_coords(scaled_base, (6, 0), tile_size)
        bottomright_noright = _get_tile_from_coords(scaled_base, (6, 1), tile_size)
        left_noborder = _get_tile_from_coords(scaled_base, (6, 2), tile_size)

    except ValueError:
        (
            topleft_notop,
            topleft_noleft,
            topright_notop,
            topright_noright,
            bottomleft_nobottom,
            bottomleft_noleft,
            bottomright_nobottom,
            bottomright_noright,
            top_noborder,
            left_noborder,
            bottom_noborder,
            right_noborder,
        ) = [None] * 12

    if temp_scale not in tilesets:
        tilesets[temp_scale] = {}

    tilesets[temp_scale][style] = Tileset(
        edge_length=tile_edge_length,
        ninetile=ninetile,
        topleft=topleft,
        top=top,
        topright=topright,
        left=left,
        middle=middle,
        right=right,
        bottomleft=bottomleft,
        bottom=bottom,
        bottomright=bottomright,
        top_noborder=top_noborder,
        left_noborder=left_noborder,
        bottom_noborder=bottom_noborder,
        right_noborder=right_noborder,
        topleft_notop=topleft_notop,
        topleft_noleft=topleft_noleft,
        topright_notop=topright_notop,
        topright_noright=topright_noright,
        bottomleft_nobottom=bottomleft_nobottom,
        bottomleft_noleft=bottomleft_noleft,
        bottomright_nobottom=bottomright_nobottom,
        bottomright_noright=bottomright_noright,
    )
    return tilesets[temp_scale][style]


def _get_tile_from_coords(
    tilemap: pygame.Surface, tile_coords: tuple[int, int], tile_size: tuple[int, int]
):
    return tilemap.subsurface(
        (tile_coords[0] * tile_size[0], tile_coords[1] * tile_size[1]), tile_size
    )


def _handle_corners(tiles, border_side1, border_side2, use_extra_if_available):
    if not border_side1 and not border_side2:
        return tiles["middle"]
    elif border_side1 and border_side2:
        return tiles["all"]
    elif not border_side1:
        return (
            tiles["noside1"]
            if tiles["noside1"] is not None and use_extra_if_available
            else tiles["side2"]
        )
    elif not border_side2:
        return (
            tiles["noside2"]
            if tiles["noside2"] is not None and use_extra_if_available
            else tiles["side1"]
        )
    else:
        raise Exception("Something went wrong in _build_needed_tileset")


def _handle_edges(tiles, show_border, use_extra_if_available):
    if show_border:
        return tiles["border"]
    return (
        tiles["noborder"]
        if tiles["noborder"] is not None and use_extra_if_available
        else tiles["middle"]
    )
