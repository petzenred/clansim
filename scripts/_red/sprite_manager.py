# sprite_manager.py - Class to manage all sprites in the game.

########################################################################################################################
# Imports
########################################################################################################################

import os
from copy import copy
from enum import EnumType, StrEnum
from typing import Optional

import pygame

import resources._red.red_filepaths as fp
from definitions import (
    ThemeName, Biome, Season,
    AccessoryName, SpritePose, EyeColour, ScarName, SkinColour, WhitePatches, TortiePatches, PeltPattern,
    STAR_CLAN_TOKEN, DF_CLAN_TOKEN, UR_CLAN_TOKEN,
    AVAILABLE_BIOMES, AVAILABLE_SEASONS, PeltColour,
    DEFAULT_SPRITES_PER_SPRITESHEET_X,
    DEFAULT_SPRITES_PER_SPRITESHEET_Y, DEFAULT_SPRITE_SIZE,
    PLATFORM_HEIGHT, PLATFORM_WIDTH, DEFAULT_CLAN_SYMBOL_NAME,
    EFFECT_MASK, EFFECT_LIGHTING  # TODO use AVAILABLE_BIOMES when loading platforms?
)
from scripts._red.config_manager import config
from scripts._red.io_manager import io_manager
from scripts._red.screens.screen_manager import screen_manager

from scripts._red.utils.ui_utils import ui_scale_dimensions
from scripts.game_structure import image_cache # TODO make sure this is the same as in the future version
from scripts.special_dates import SpecialDate, is_today

import logging
logger = logging.getLogger(__name__)


########################################################################################################################
# Constants
########################################################################################################################

PALETTE_BASE_SPRITE_NAME: str = "base"


########################################################################################################################
# Enum Classes
########################################################################################################################

class EffectType(StrEnum):

    Lineart = "lineart"
    Overlay = "overlay"
    Underlay = "underlay"
    Gradient = "gradient"
    Shader = "shader"
    FadeFog = "fog"


class SpriteGroup(StrEnum):
    """ Used by SpriteManager to group similar sprites. """

    Accessory = "acc" # AccessoryName
    EyeBoth = "eyes_both" # EyeColour
    EyeRight = "eyes_right" # EyeColour
    Scar = "scars" # ScarName
    Skin = "skin" # SkinColour
    Tortie = "tortie" # TortiePatches
    White = "white" # WhitePatches

    Effect = "effect"
    Pelt = "pelt"

    Platform = "platforms"
    ClanSymbol = "clan_symbol"
    PeltError = "error_placeholder"

    Faded = "faded"

    @property
    def to_cast_class(self) -> Optional[EnumType]:
        if self is self.Accessory:
            return AccessoryName
        elif self is self.Effect:
            return EffectType
        elif self is self.EyeRight or self is self.EyeBoth:
            return EyeColour
        elif self is self.Pelt:
            return PeltColour
        elif self is self.Scar:
            return ScarName
        elif self is self.Skin:
            return SkinColour
        elif self is self.Tortie:
            return TortiePatches
        elif self is self.White:
            return WhitePatches
        return None


########################################################################################################################
# Classes
########################################################################################################################

# TODO April Fool's lineart

class SpriteManager:

    cat_tints = {}
    white_patches_tints = {}
    clan_symbols = []

    symbol_dict: dict = None
    spritesheets: dict = {}
    images: dict = {}
    sprites: dict = {}

    blank_sprite: pygame.Surface = None # Shared empty sprite for placeholders

    size: int
    # FIXME these should be sprites per block, not sprites per sheet
    sprites_per_sheet_x: int = DEFAULT_SPRITES_PER_SPRITESHEET_X
    sprites_per_sheet_y: int = DEFAULT_SPRITES_PER_SPRITESHEET_Y

    # ------------------------------------- INIT ------------------------------------- #

    def __init__(self):
        """ Class that handles and hold all spritesheets.

        Size is normally automatically determined by the size of the
        lineart. If lineart sprites are not square, a default value
        is used.
        """
        self._load_data_dictionaries()
        self._set_sprite_size()

        self.sprites: dict = {
            SpriteGroup.Accessory: {},
            SpriteGroup.EyeBoth: {},
            SpriteGroup.EyeRight: {},
            SpriteGroup.Scar: {},
            SpriteGroup.Skin: {},
            SpriteGroup.Tortie: {},
            SpriteGroup.White: {},

            SpriteGroup.Effect: {},
            SpriteGroup.Pelt: {},

            SpriteGroup.Platform: {},
            SpriteGroup.ClanSymbol: {},
            SpriteGroup.PeltError: None,

            SpriteGroup.Faded: {},
        }
        return

    def _load_data_dictionaries(self):
        for attr, filepath in fp.SPRITE_DATA_DICTS.items():
            self.__setattr__(attr, io_manager.read_file(filepath=filepath))
        self.symbol_dict = io_manager.read_file(filepath=fp.CLAN_SYMBOL_NAMES)
        return

    def _set_sprite_size(self):
        # get the width and height of the spritesheet
        lineart = pygame.image.load(fp.LINEART)
        width, height = lineart.get_size()
        del lineart  # unneeded

        # if anyone changes lineart for whatever reason update this
        # if isinstance(self.size, int):
        #     pass
        if width // self.sprites_per_sheet_x == height // self.sprites_per_sheet_y \
                and isinstance(width // self.sprites_per_sheet_x, int):
            self.size = width // self.sprites_per_sheet_x
        else:
            self.size = DEFAULT_SPRITE_SIZE  # default, what base ClanGen uses
            logger.warning(f"The sprites in lineart.png are not square. Falling back to "
                           f"DEFAULT_SPRITE_SIZE={self.size}x{self.size}.\nIf you are a "
                           f"modder, please update `definitions.DEFAULT_SPRITES_PER_SHEET_X`"
                           f" and `definitions.DEFAULT_SPRITES_PER_SHEET_Y`.")

        # set the blank sprite used when a sprite doesn't load properly
        if not self.blank_sprite:
            self.blank_sprite = pygame.Surface(size=(self.size, self.size), flags=pygame.HWSURFACE | pygame.SRCALPHA)

        del width, height  # unneeded
        return

    # ------------------------------ LOAD DATA FROM MAIN ----------------------------- #

    def load_all_sprites(self):
        self._load_cat_sprites()
        self._load_effects()
        self._load_clan_symbol_sprites()
        self._load_platform_sprites()
        return

    def _load_cat_sprites(self):
        """ Load sprite layers for cat sprites. """
        # pelt error sprite
        self.sprites[SpriteGroup.PeltError] = self._load_spritesheet(filepath=fp.ERROR_PLACEHOLDER)

        # faded cat sprites
        for dead_clan_name in (STAR_CLAN_TOKEN, DF_CLAN_TOKEN, UR_CLAN_TOKEN):
            clan_dict: dict[str, pygame.Surface] = {}
            for age in ("newborn", "kitten", "adolescent", "adult", "senior"): # FIXME make this an enum
                clan_dict[age] = self._load_spritesheet(filepath=f"sprites/faded/faded{dead_clan_name}{age}.png") # FIXME hardcoded filepath
            self.sprites[SpriteGroup.Faded][dead_clan_name] = clan_dict
        del age, dead_clan_name

        # pelt base
        for spritesheet in self.PELT_DATA["spritesheets"]:
            # each spritesheet here is a pattern with all the colours
            self._save_spritesheet(spritesheet=spritesheet)
            self._separate_spritesheet(sprite_group=SpriteGroup.Pelt,
                                       spritesheet=spritesheet,
                                       sprite_list=self.PELT_DATA["sprite_list"])

        # collars
        self._save_spritesheet(spritesheet=self.COLLAR_DATA["spritesheet"])
        for col, collar_style_group in enumerate(self.COLLAR_DATA["sprite_dict"].keys()):
            # collar_style_group = ["bows", "leather", "nylon"]
            collar_styles: dict = self.COLLAR_DATA["sprite_dict"][collar_style_group]
            # collar_styles = {bow: [], bow_foil: [], bow_gradient: []}
            for row, collar_style in enumerate(collar_styles.keys()):
                # collar_style = [bow, bow_foil, bow_gradient]
                colours: list = collar_styles[collar_style]
                self.make_group(spritesheet=self.COLLAR_DATA["spritesheet"], sprite_group=SpriteGroup.Accessory,
                                name_to_cast=collar_style, palette_colours=colours, pos=(row, col))

        # all other sprites
        for data_set in (self.EYE_BOTH_DATA, self.EYE_RIGHT_DATA,
                         self.PLANT_DATA, self.WILD_DATA,
                         self.SKIN_DATA, self.TORTIE_DATA, self.WHITE_DATA,
                         self.SCAR_PELT_DATA, self.SCAR_MISSING_DATA,
                         ):
            self._save_spritesheet(spritesheet=data_set["spritesheet"])
            self._separate_spritesheet(sprite_group=SpriteGroup(data_set["sprite_group"]),
                                       spritesheet=data_set["spritesheet"],
                                       sprite_list=data_set["sprite_list"])

        return

    def _load_effects(self):
        """ Load effects for cat sprites. """
        effects: dict = {
            EffectType.Overlay: [STAR_CLAN_TOKEN, UR_CLAN_TOKEN],
            EffectType.Underlay: [UR_CLAN_TOKEN],
            EffectType.Gradient: [UR_CLAN_TOKEN],
            EffectType.Lineart: ["", STAR_CLAN_TOKEN, DF_CLAN_TOKEN, UR_CLAN_TOKEN],
            EffectType.Shader: [EFFECT_MASK, EFFECT_LIGHTING],
        }
        for effect_type in effects:
            if effect_type is EffectType.Gradient:
                self.sprites[SpriteGroup.Effect][EffectType.Gradient] = {}
            for loc in effects[effect_type]:
                spritesheet = effect_type.value + loc
                self._save_spritesheet(spritesheet=spritesheet, subfolder=fp.SPRITE_EFFECTS_DIRNAME)
                if effect_type is not EffectType.Gradient:
                    self.make_group(spritesheet=spritesheet, sprite_group=SpriteGroup.Effect, name_to_cast=effect_type,
                                    loc=loc)
                else:
                    self.sprites[SpriteGroup.Effect][EffectType.Gradient][loc] = self.spritesheets[spritesheet]

        # fade fog
        fogs: list[str] = [DF_CLAN_TOKEN, STAR_CLAN_TOKEN, UR_CLAN_TOKEN, EFFECT_MASK]
        for loc in fogs:
            spritesheet: str = EffectType.FadeFog + loc
            self._save_spritesheet(spritesheet=spritesheet, subfolder=fp.SPRITE_FADE_FOG_DIRNAME)
            for fade_level in range(3): # FIXME hardcoded, replace with MAX_FADE_LEVEL
                self.make_group(spritesheet=spritesheet, sprite_group=SpriteGroup.Effect,
                                name_to_cast=EffectType.FadeFog, pos=(fade_level, 0), loc=loc)

        return

    # TODO reconfigure this to work off of the names in the dictionary of Clan symbols, not a list of letters
    def _load_clan_symbol_sprites(self):
        """ Loads Clan symbols. """
        self._save_spritesheet(spritesheet=fp.CLAN_SYMBOL_SPRITES)

        # save the default Clan symbol, which is just the cat head outline without any symbol on it
        self.make_group(spritesheet=fp.CLAN_SYMBOL_SPRITES,
                        sprite_group=SpriteGroup.ClanSymbol,
                        name_to_cast=DEFAULT_CLAN_SYMBOL_NAME)

        # U and X omitted from letter list due to having no prefixes
        letters = [
            "_skip_",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "V",
            "W",
            "Y",
            "Z",
        ]

        # sprite names will format as "symbol{PREFIX}{INDEX}", ex. "symbolSPRING0"
        for y_pos, letter in enumerate(letters):
            if letter == "_skip_":
                continue
            x_mod = 0
            for i, symbol_name in enumerate(
                [
                    symbol
                    for symbol in self.symbol_dict
                    if letter in symbol and self.symbol_dict[symbol]["variants"]
                ]
            ):
                if self.symbol_dict[symbol_name]["variants"] > 1 and x_mod > 0:
                    x_mod += -1
                for variant_index in range(self.symbol_dict[symbol_name]["variants"]):
                    x_pos = i + x_mod

                    if self.symbol_dict[symbol_name]["variants"] > 1:
                        x_mod += 1
                    elif x_mod > 0:
                        x_pos += -1

                    self.clan_symbols.append(f"symbol{symbol_name.upper()}{variant_index}")
                    self.make_group(spritesheet=fp.CLAN_SYMBOL_SPRITES, sprite_group=SpriteGroup.ClanSymbol,
                                    name_to_cast=f"symbol{symbol_name.upper()}{variant_index}", pos=(x_pos, y_pos))

        return

    def _load_platform_sprites(self):
        """ Load cat platforms, used on the profile screen. """
        self._save_spritesheet(spritesheet=fp.PLATFORM_SPRITES)
        self.sprites[SpriteGroup.Platform] = {}

        season_offsets: dict = {
            Season.Summer: 0,
            Season.Winter: 160,
            Season.Autumn: 320,
            Season.Spring: 480
        }
        order: list = [Biome.Beach, Biome.Forest, Biome.Mountain, "nest", Biome.Plains, "dead"]

        for biome in order:
            row = order.index(biome)
            biome_platforms = self.spritesheets[fp.PLATFORM_SPRITES].subsurface(
                pygame.Rect(0, row * PLATFORM_HEIGHT, 8 * PLATFORM_WIDTH, PLATFORM_HEIGHT)
            )
            biome_dict = {}
            for _ in [(ThemeName.Dark, 0), (ThemeName.Light, 80)]:
                theme = _[0]
                theme_offset = _[1]
                biome_dict[theme] = {}

                if biome == "dead":
                    biome_dict[theme] = {
                        DF_CLAN_TOKEN: biome_platforms.subsurface(
                            pygame.Rect(0 + theme_offset, 0, PLATFORM_WIDTH, PLATFORM_HEIGHT)),
                        STAR_CLAN_TOKEN: biome_platforms.subsurface(
                            pygame.Rect(2 * PLATFORM_WIDTH + theme_offset, 0, PLATFORM_WIDTH, PLATFORM_HEIGHT)),
                        UR_CLAN_TOKEN: biome_platforms.subsurface(
                            pygame.Rect(4 * PLATFORM_WIDTH + theme_offset, 0, PLATFORM_WIDTH, PLATFORM_HEIGHT)),
                    }
                else:
                    for col, season in enumerate(AVAILABLE_SEASONS):
                        biome_dict[theme][season] = biome_platforms.subsurface(
                            pygame.Rect(season_offsets[season] + theme_offset, 0, PLATFORM_WIDTH, PLATFORM_HEIGHT))

                self.sprites[SpriteGroup.Platform][biome] = biome_dict
        return

    def _separate_spritesheet(self, sprite_group: SpriteGroup, spritesheet: str, sprite_list: list[list[str]]):
        for col, sprite_sets in enumerate(sprite_list):
            for row, sprite_set in enumerate(sprite_sets):
                # make sure that sprite_group and sprite_set are compatible, and that a dictionary has been created
                #   for the new sprites in self.sprites
                try:
                    if sprite_group.to_cast_class(sprite_set) not in self.sprites[sprite_group]:
                        self.sprites[sprite_group][sprite_group.to_cast_class(sprite_set)] = {}
                except TypeError:
                    raise TypeError(f"SpriteGroup.{sprite_group.name} does not have a to_cast_class property, so "
                                    f"can't be used with the functions _seperate_spritesheet() and make_group() in "
                                    f"the SpriteManager class.")
                except ValueError:
                    raise ValueError(f"Tried to cast \"{sprite_set}\" as a {sprite_group.to_cast_class} while "
                                     f"separating spritesheet \"{spritesheet}\" in the SpriteManager")
                self.make_group(spritesheet=spritesheet, sprite_group=sprite_group, name_to_cast=sprite_set,
                                palette_colours=[], pos=(row, col))

    def _save_spritesheet(self, spritesheet: str, subfolder: str = ""):
        """ Save a spritesheet to SpriteManager.spritesheets.

        :param str spritesheet: name of the file in the "sprites/" directory
        :param str subfolder: optional name of the subfolder in the "sprites/" directory; should include "/"
        """
        filepath: str = f"sprites/{subfolder}{spritesheet}.png"
        self.spritesheets[spritesheet] = self._load_spritesheet(filepath=filepath)

    # TODO consider moving this to io_manager
    def _load_spritesheet(self, filepath: str) -> pygame.Surface:
        """ Get spritesheet from filepath. """
        return pygame.image.load(filepath).convert_alpha()

    # TODO docstring
    def make_group(self,
                   spritesheet: str,
                   sprite_group: SpriteGroup,
                   name_to_cast: str,
                   palette_colours: list[str] = [],
                   pos: tuple[int, int] = (0, 0),
                   loc: str = "",
    ):
        """ Divide sprites on a spritesheet into groups of sprites that are easily accessible

        :param spritesheet: name of spritesheet file
        :param SpriteGroup sprite_group: which sprite group the sprite should be saved under
        :param name_to_cast: the sprites will be saved under sprite_group.to_cast_class(name_to_cast)
        :param pos: (col,row) tuple of offsets. NOT pixel offset, but offset of other sprites
        """
        # error_sprite_name is here to save time when catching errors in this function, it happens a lot
        # TODO get rid of error_sprite_name during testing if it's not needed
        error_sprite_base: str = f"sprites[SpriteGroup.{sprite_group.name}]"
        if sprite_group is SpriteGroup.Pelt:
            error_sprite_base += f"[PeltPattern.{spritesheet[8:].title()}]"
        if not sprite_group is SpriteGroup.ClanSymbol:
            error_sprite_base += f"[{sprite_group.to_cast_class.__name__}.{name_to_cast.title()}]"
        if loc:
            error_sprite_base += f"[{loc}]"

        if sprite_group is SpriteGroup.ClanSymbol:
            sprites_x, sprites_y = 1, 1
        else:
            sprites_x, sprites_y = self.sprites_per_sheet_x, self.sprites_per_sheet_y

        group_x_ofs = pos[0] * sprites_x * self.size
        group_y_ofs = pos[1] * sprites_y * self.size
        sprite_pose_i = 0

        # splitting group into singular sprites and storing into self.sprites section
        for row in range(sprites_y):
            for col in range(sprites_x):
                # this happens because the spritesheets have 23 sprites, not 24 (the bottom right corner is empty)
                if sprite_pose_i == 23: return
                error_sprite_name: str = error_sprite_base + f"[SpritePose.{SpritePose(sprite_pose_i).name}]"

                try:
                    top_corner_x: int = group_x_ofs + col * self.size
                    top_corner_y: int = group_y_ofs + row * self.size
                    width: int = self.size
                    height: int = self.size

                    new_sprite: pygame.Surface = pygame.Surface.subsurface(
                        self.spritesheets[spritesheet],
                        top_corner_x, top_corner_y,
                        width, height
                    )

                    # rect = pygame.Rect(
                    #     (group_x_ofs + col * self.size, group_y_ofs + row * self.size,),
                    #     (self.size, self.size),
                    # )
                    # new_sprite: pygame.Surface = pygame.Surface.subsurface(
                    #     self.spritesheets[spritesheet],
                    #     rect
                    # )

                    # new_sprite: pygame.Surface = pygame.Surface.subsurface(
                    #     self.spritesheets[spritesheet],
                    #     group_x_ofs + col * self.size,
                    #     group_y_ofs + row * self.size,
                    #     self.size, self.size,
                    # )

                    # sprite_loc = pygame.Rect(
                    #     left=group_x_ofs + col * self.size,
                    #     top=group_y_ofs + row * self.size,
                    #     width=self.size, height=self.size,
                    # )
                    # new_sprite: pygame.Surface = pygame.Surface.subsurface(
                    #     self.spritesheets[spritesheet],
                    #     sprite_loc
                    # )
                    # new_sprite: pygame.Surface = self.spritesheets[spritesheet].subsurface(sprite_loc)
                except ValueError as err:
                    # fallback for non-existent sprites
                    logger.warning(f"Tried to grab subsurface of nonexistent sprite: "
                                   f"error_sprite_name: {error_sprite_name}")
                    logger.warning(f"Saving as blank sprite")
                    new_sprite = self.blank_sprite

                # save the sprite
                if spritesheet == "acc_collar":
                    self.apply_palettes(sprite_pose=SpritePose(sprite_pose_i), style_name=name_to_cast,
                                        base_sprite=new_sprite, palette_colours=palette_colours)
                elif sprite_group is SpriteGroup.ClanSymbol:  # no_index == True
                    self.sprites[sprite_group][name_to_cast] = new_sprite
                elif sprite_group is SpriteGroup.Effect:
                    et: EffectType = sprite_group.to_cast_class(name_to_cast)
                    if not et in self.sprites[sprite_group]:
                        self.sprites[sprite_group][et] = {loc: {}}
                    elif loc not in self.sprites[sprite_group][et]:
                        self.sprites[sprite_group][et][loc] = {}
                    self.sprites[sprite_group][sprite_group.to_cast_class(name_to_cast)][loc][SpritePose(sprite_pose_i)] = \
                        new_sprite
                elif sprite_group is SpriteGroup.Pelt:
                    pattern: PeltPattern = PeltPattern(spritesheet[8:])
                    if pattern not in self.sprites[sprite_group]:
                        self.sprites[sprite_group][pattern] = {}
                    self.sprites[sprite_group][pattern][sprite_group.to_cast_class(name_to_cast)] = \
                        new_sprite
                else:
                    self.sprites[sprite_group][sprite_group.to_cast_class(name_to_cast)][SpritePose(sprite_pose_i)] = new_sprite

                # increment sprite pose before creating the next sprite
                sprite_pose_i += 1
        return

    def apply_palettes(self, sprite_pose: SpritePose, style_name: str,
                       base_sprite: pygame.Surface, palette_colours: list):
        """ Creates sprites for each colour palette variation.

        :param SpritePose sprite_pose: index of sprite
        :param str style_name: name of sprite
        :param Surface base_sprite: the sprite object to create variations of
        :param list[str] palette_colours: list of palette names
        """
        # first we create an array of our palette map
        filepath: str = fp.SPRITE_PALETTES_DIR_PATH + style_name + "_palette.png" # FIXME filepath
        full_map = pygame.image.load(file=filepath)
        map_array = pygame.PixelArray(full_map)

        # then create a dictionary associating the palette name with its row of the array
        colour_palettes = {}
        palette_colours = palette_colours.copy()
        palette_colours.insert(0, PALETTE_BASE_SPRITE_NAME) # FIXME change
        for row in range(0, map_array.shape[1]): # pylint: disable=unsubscriptable-object
            colour_name = palette_colours[row]
            colour_palettes.update( {colour_name: [full_map.unmap_rgb(px) for px in map_array[::, row]]} )

        # now we recolour the sprite
        for colour_name, palette in colour_palettes.items():
            collar_name = f"{style_name}_{colour_name}"
            acc: AccessoryName = AccessoryName(collar_name)
            if acc not in self.sprites[SpriteGroup.Accessory]:
                self.sprites[SpriteGroup.Accessory][acc] = {}
            if colour_name == PALETTE_BASE_SPRITE_NAME:  # FIXME change
                continue
            try:
                recolour_sprite = pygame.PixelArray(base_sprite.copy())
            except ValueError:
                raise ValueError(f"Tried to apply a palette to an empty sprite for {collar_name}")

            # we replace each colour on the base palette with its matching index from the colour palette
            for colour_i, colour in enumerate(palette):
                recolour_sprite.replace(color=colour_palettes[PALETTE_BASE_SPRITE_NAME][colour_i], repcolor=colour)  # FIXME change

            # convert back into a surface
            _sprite = recolour_sprite.make_surface()

            # add it to our sprite dict!
            # self.sprites[f"{name}_{color_name}{sprite_index}"] = _sprite
            self.sprites[SpriteGroup.Accessory][acc][sprite_pose] = _sprite

            # close the pixel array now that we're done
            recolour_sprite.close()

        map_array.close()
        return

    # ---------------------------------- CAT SPRITE ---------------------------------- #

    # TODO where is this used?
    def update_mask(self, cat):
        if cat.faded or cat.dead:
            # should never need a mask since they can't appear on the Clan screen
            cat.sprite_mask = None
            return

        val = pygame.mask.from_surface(
            surface=pygame.transform.scale(
                surface=cat.sprite,
                size=ui_scale_dimensions(dim=(self.size, self.size), # dim=(DEFAULT_SPRITE_SIZE, DEFAULT_SPRITE_SIZE)
                                         scale=screen_manager.window_scale)
            ),
            threshold=250
        )

        inflated_mask = pygame.Mask( size=(val.get_size()[0] + 10, val.get_size()[1] + 10,) )
        inflated_mask.draw(val, (5, 5))
        for _ in range(3):
            outline = inflated_mask.outline()
            for point in outline:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        try:
                            inflated_mask.set_at((point[0] + dx, point[1] + dy), 1)
                        except IndexError:
                            continue
        cat.sprite_mask = inflated_mask
        return

    # TODO
    def generate_sprite(
        self,
        cat,
        life_state=None,
        scars_hidden=False,
        acc_hidden=False,
        always_living=False,
        disable_sick_sprite=False,
    ) -> pygame.Surface:
        """
        Generates the sprite for a cat, with optional arguments that will override certain things.

        :param life_state: sets the age life_stage of the cat, overriding the one set by its age. Set to string.
        :param scars_hidden: If True, doesn't display the cat's scars. If False, display cat scars.
        :param acc_hidden: If True, hide the accessory. If false, show the accessory.
        :param always_living: If True, always show the cat with living lineart
        :param disable_sick_sprite: If true, never use the not_working lineart.
                        If false, use the cat.not_working() to determine the no_working art.
        """

        # TODO: apply opacity (which lowers as a cat fades),
        sprite_poses = list(SpritePose)
        # sprite_poses = sprites.POSE_DATA["poses"]

        if life_state is not None:
            age = life_state
        else:
            age = cat.age

        if always_living:
            dead = False
        else:
            dead = cat.dead

        # setting the cat_sprite (bc this makes things much easier)

        # sick sprites
        if (
            not disable_sick_sprite
            and cat.not_working()
            and age != CatAge.NEWBORN
            and constants.CONFIG["cat_sprites"]["sick_sprites"]
        ):
            if age in (CatAge.KITTEN, CatAge.ADOLESCENT):
                cat_sprite = sprite_poses["sick_young0"]
            else:
                cat_sprite = sprite_poses["sick_adult0"]

        # paralyzed sprites
        elif cat.pelt.paralyzed and age != CatAge.NEWBORN:
            if age in (CatAge.KITTEN, CatAge.ADOLESCENT):
                cat_sprite = sprite_poses[cat.pelt.cat_sprites["para_young"]]
            else:
                cat_sprite = sprite_poses[cat.pelt.cat_sprites["para_adult"]]

        # default sprites
        else:
            if constants.CONFIG["fun"]["all_cats_are_newborn"]:
                cat_sprite = sprite_poses[cat.pelt.cat_sprites["newborn"]]
            else:
                cat_sprite = sprite_poses[cat.pelt.cat_sprites[age]]

        new_sprite = pygame.Surface(
            (sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA
        )

        # generating the sprite
        try:
            if cat.pelt.name not in ["Tortie", "Calico"]:
                new_sprite.blit(
                    sprites.sprites[
                        cat.pelt.get_sprites_name() + cat.pelt.colour + cat_sprite
                    ],
                    (0, 0),
                )
            else:
                # Base Coat
                sprite_name = f"colours_{cat.pelt.tortie_base}{cat.pelt.colour}{cat_sprite}"
                new_sprite.blit(
                    sprites.sprites[sprite_name],
                    (0, 0),
                )

                # Create the patch image
                if cat.pelt.tortie_pattern == "Single":
                    tortie_pattern = "SolidColour"
                else:
                    tortie_pattern = cat.pelt.tortie_pattern

                sprite_name = (
                    f"colours_{tortie_pattern}{cat.pelt.tortie_colour}{cat_sprite}"
                )
                patches = sprites.sprites[sprite_name].copy()
                sprite_name = f"{sprites.TORTIE_DATA['spritesheet']}{cat.pelt.tortie_marking}{cat_sprite}"
                patches.blit(
                    sprites.sprites[sprite_name],
                    (0, 0),
                    special_flags=pygame.BLEND_RGBA_MULT,
                )

                # Add patches onto cat.
                new_sprite.blit(patches, (0, 0))

            # TINTS
            if (
                cat.pelt.tint is not None
                and cat.pelt.tint in sprites.cat_tints["tint_colours"]
            ):
                # Multiply with alpha does not work as you would expect - it just lowers the alpha of the
                # entire surface. To get around this, we first blit the tint onto a white background to dull it,
                # then blit the surface onto the sprite with pygame.BLEND_RGB_MULT
                tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                tint.fill(tuple(sprites.cat_tints["tint_colours"][cat.pelt.tint]))
                new_sprite.blit(tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
            if (
                cat.pelt.tint is not None
                and cat.pelt.tint in sprites.cat_tints["dilute_tint_colours"]
            ):
                tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                tint.fill(tuple(sprites.cat_tints["dilute_tint_colours"][cat.pelt.tint]))
                new_sprite.blit(tint, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

            # draw white patches
            if cat.pelt.white_patches is not None:
                sprite_name = f"{sprites.WHITE_DATA['spritesheet']}{cat.pelt.white_patches}{cat_sprite}"
                white_patches = sprites.sprites[sprite_name].copy()

                # Apply tint to white patches.
                if (
                    cat.pelt.white_patches_tint is not None
                    and cat.pelt.white_patches_tint
                    in sprites.white_patches_tints["tint_colours"]
                ):
                    tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                    tint.fill(
                        tuple(
                            sprites.white_patches_tints["tint_colours"][
                                cat.pelt.white_patches_tint
                            ]
                        )
                    )
                    white_patches.blit(tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

                new_sprite.blit(white_patches, (0, 0))

            # draw vit & points

            if cat.pelt.points:
                sprite_name = (
                    f"{sprites.WHITE_DATA['spritesheet']}{cat.pelt.points}{cat_sprite}"
                )

                points = sprites.sprites[sprite_name].copy()
                if (
                    cat.pelt.white_patches_tint is not None
                    and cat.pelt.white_patches_tint
                    in sprites.white_patches_tints["tint_colours"]
                ):
                    tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                    tint.fill(
                        tuple(
                            sprites.white_patches_tints["tint_colours"][
                                cat.pelt.white_patches_tint
                            ]
                        )
                    )
                    points.blit(tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                new_sprite.blit(points, (0, 0))

            if cat.pelt.vitiligo:
                sprite_name = (
                    f"{sprites.WHITE_DATA['spritesheet']}{cat.pelt.vitiligo}{cat_sprite}"
                )

                new_sprite.blit(
                    sprites.sprites[sprite_name],
                    (0, 0),
                )

            # draw eyes & scars1
            sprite_name = (
                f"{sprites.EYE_DATA['spritesheet'][0]}{cat.pelt.eye_colour}{cat_sprite}"
            )
            eyes = sprites.sprites[sprite_name].copy()
            if cat.pelt.eye_colour2 != None:
                sprite_name = f"{sprites.EYE_DATA['spritesheet'][1]}{cat.pelt.eye_colour2}{cat_sprite}"
                eyes.blit(
                    sprites.sprites[sprite_name],
                    (0, 0),
                )
            new_sprite.blit(eyes, (0, 0))

            if not scars_hidden:
                for scar in cat.pelt.scars:
                    if scar in cat.pelt.general_scars:
                        sprite_name = (
                            f"{sprites.SCAR_DATA['spritesheet']}{scar}{cat_sprite}"
                        )
                        new_sprite.blit(
                            sprites.sprites[sprite_name],
                            (0, 0),
                        )

            # setting the lineart color to override on accessories & missing bits
            lineart_color = (
                pygame.Color(
                    constants.CONFIG["cat_sprites"]["lineart_color_sc"]
                    if cat.status.group == CatGroup.STARCLAN
                    else constants.CONFIG["cat_sprites"]["lineart_color_df"]
                )
                if cat.status.group != CatGroup.UNKNOWN_RESIDENCE
                else None
            )

            gradient_surface = (
                sprites.sprites["line_ur_gradient" + cat_sprite]
                if dead and cat.status.group == CatGroup.UNKNOWN_RESIDENCE
                else None
            )

            def _recolor_lineart(
                sprite, color=None, source: pygame.Surface = None
            ) -> pygame.Surface:
                """
                Helper function to set the appropriate lineart color for the living status of the cat
                :param sprite: lineart to recolor
                :param color: color to apply to all pixels
                :param source: source surface of same size as sprite to use instead of color
                :return:
                """
                if not dead:
                    return sprite

                if color is None and source is None:
                    raise ValueError("Must provide either `color` or `source` for _recolor_lineart")

                out = sprite.copy()
                if color:
                    pixel_array = pygame.PixelArray(out)
                    pixel_array.replace((0, 0, 0), color, distance=0)
                    del pixel_array
                    return out

                width, height = sprite.get_size()
                for x in range(width):
                    for y in range(height):
                        if sprite.get_at((x, y)) == pygame.Color(0, 0, 0):
                            color = source.get_at((x, y))
                            sprite.set_at((x, y), color)
                return out

            # draw line art
            if game_setting_get("shaders") and not dead:
                new_sprite.blit(
                    sprites.sprites["shader_mask" + cat_sprite],
                    (0, 0),
                    special_flags=pygame.BLEND_RGB_MULT,
                )
                new_sprite.blit(sprites.sprites["shader_lighting" + cat_sprite], (0, 0))

            if not dead:
                new_sprite.blit(sprites.sprites["lineart" + cat_sprite], (0, 0))
            elif cat.status.group == CatGroup.UNKNOWN_RESIDENCE:
                new_sprite.blit(sprites.sprites["lineart_ur" + cat_sprite], (0, 0))
            elif cat.status.group == CatGroup.DARK_FOREST:
                new_sprite.blit(sprites.sprites["lineart_df" + cat_sprite], (0, 0))
            elif dead:
                new_sprite.blit(sprites.sprites["lineart_sc" + cat_sprite], (0, 0))

            # draw skin and scars2
            blendmode = pygame.BLEND_RGBA_MIN
            sprite_name = f"{sprites.SKIN_DATA['spritesheet']}{cat.pelt.skin}{cat_sprite}"
            new_sprite.blit(
                sprites.sprites[sprite_name],
                (0, 0),
            )

            if not scars_hidden:
                for scar in cat.pelt.scars:
                    if scar in cat.pelt.missing_part_scars:
                        sprite_name = f"{sprites.SCAR_MISSING_PART_DATA['spritesheet']}{scar}{cat_sprite}"
                        new_sprite.blit(
                            _recolor_lineart(
                                sprites.sprites[sprite_name],
                                lineart_color,
                                gradient_surface,
                            ),
                            (0, 0),
                            special_flags=blendmode,
                        )

            # draw accessories
            from scripts.cat.pelts import Pelt

            if not acc_hidden and cat.pelt.accessory:
                cat_accessories = cat.pelt.accessory
                categories = [
                    "collar_accessories",
                    "tail_accessories",
                    "body_accessories",
                    "head_accessories",
                ]
                for category in categories:
                    for accessory in cat_accessories:
                        if accessory in getattr(Pelt, category):
                            if accessory in cat.pelt.plant_accessories:
                                sprite_name = f"{sprites.PLANT_DATA['spritesheet']}{accessory}{cat_sprite}"
                                new_sprite.blit(
                                    _recolor_lineart(
                                        sprites.sprites[sprite_name],
                                        lineart_color,
                                        gradient_surface,
                                    ),
                                    (0, 0),
                                )
                            elif accessory in cat.pelt.wild_accessories:
                                sprite_name = f"{sprites.WILD_DATA['spritesheet']}{accessory}{cat_sprite}"
                                new_sprite.blit(
                                    _recolor_lineart(
                                        sprites.sprites[sprite_name],
                                        lineart_color,
                                        gradient_surface,
                                    ),
                                    (0, 0),
                                )
                            elif accessory in cat.pelt.collar_accessories:
                                sprite_name = f"{sprites.COLLAR_DATA['spritesheet']}{accessory}{cat_sprite}"
                                new_sprite.blit(
                                    _recolor_lineart(
                                        sprites.sprites[sprite_name],
                                        lineart_color,
                                        gradient_surface,
                                    ),
                                    (0, 0),
                                )

            # Apply fading fog
            if (
                cat.pelt.opacity <= 97
                and not cat.prevent_fading
                and get_clan_setting("fading")
                and dead
            ):
                stage = "0"
                if 80 >= cat.pelt.opacity > 45:
                    # Stage 1
                    stage = "1"
                elif cat.pelt.opacity <= 45:
                    # Stage 2
                    stage = "2"

                new_sprite.blit(
                    sprites.sprites["fademask" + stage + cat_sprite],
                    (0, 0),
                    special_flags=pygame.BLEND_RGBA_MULT,
                )

                if cat.status.group == CatGroup.STARCLAN:
                    temp = sprites.sprites["fadestarclan" + stage + cat_sprite].copy()
                    temp.blit(new_sprite, (0, 0))
                    new_sprite = temp
                elif cat.status.group == CatGroup.UNKNOWN_RESIDENCE:
                    temp = sprites.sprites["fadeur" + stage + cat_sprite].copy()
                    temp.blit(new_sprite, (0, 0))
                    new_sprite = temp
                else:
                    temp = sprites.sprites["fadedf" + stage + cat_sprite].copy()
                    temp.blit(new_sprite, (0, 0))
                    new_sprite = temp

            # ok! we have the sprite! now, do some layer things if the cat's already dead
            if dead:
                temp_sprite = pygame.Surface(
                    (sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA
                )

                if cat.status.group == CatGroup.STARCLAN:
                    # no underlay

                    # cat sprite
                    temp_sprite.blit(new_sprite, (0, 0))

                    # overlay
                    temp_sprite.blit(
                        sprites.sprites["line_sc_overlay" + cat_sprite],
                        (0, 0),
                    )
                elif cat.status.group == CatGroup.UNKNOWN_RESIDENCE:
                    # underlay
                    temp_sprite.blit(
                        sprites.sprites["line_ur_overlay" + cat_sprite],
                        (0, 0),
                    )

                    # cat sprite
                    temp_sprite.blit(new_sprite, (0, 0))

                    # overlay
                    temp_sprite.blit(
                        sprites.sprites["line_ur_overlay" + cat_sprite],
                        (0, 0),
                    )
                elif cat.status.group == CatGroup.DARK_FOREST:
                    # no underlay

                    # cat sprite
                    temp_sprite.blit(new_sprite, (0, 0))

                    # no overlay

                new_sprite = temp_sprite

            # reverse, if assigned so
            if cat.pelt.reverse:
                new_sprite = pygame.transform.flip(new_sprite, True, False)

        except (TypeError, KeyError):
            traceback.print_exc()
            logger.exception("Failed to load sprite")

            # Placeholder image
            new_sprite = image_cache.load_image(
                f"sprites/error_placeholder.png"
            ).convert_alpha()

        return new_sprite

    # --------------------------------- CLAN SYMBOLS --------------------------------- #

    # TODO docstring
    def get_clan_symbol(self, clan_obj, force_light=False) -> pygame.Surface:
        """ Change the colour of the symbol to match the requested theme, then return it.

        :param RedClan clan_obj: TODO
        :param force_light: Use to ignore dark mode and always display the light mode color

        :return: TODO
        """
        symbol_name = clan_obj.clan_symbol
        symbol = self.sprites[SpriteGroup.ClanSymbol][symbol_name]
        if symbol is None:
            logger.warning(f"{symbol_name} is not a known Clan symbol! Using default Clan background.")
            symbol = self.sprites[SpriteGroup.ClanSymbol][DEFAULT_CLAN_SYMBOL_NAME]

        recolored_symbol = copy(symbol)
        if not force_light:
            var = pygame.PixelArray(recolored_symbol)
            var.replace(color=config.game_config.themes[ThemeName.Light]["clan_symbol_colour"],
                        repcolor=config.game_config.themes[config.settings.Theme]["clan_symbol_colour"])
            del var

        return recolored_symbol


########################################################################################################################
# Instances
########################################################################################################################

sprite_manager = SpriteManager()
