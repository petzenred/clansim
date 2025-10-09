# red_pelt.py - Enums, dataclasses, and classes related to cat appearance.
import random
from dataclasses import dataclass, field
from enum import StrEnum, Enum
from operator import index
from random import choice
from typing import Optional

from definitions import (
    Age, GenderKits,
    PeltPatternCategory, PeltColourCategory, PeltLengthCategory, WhitePatchPatternCategory,
    EyeColourCategory, SkinColourCategory, ScarCategory, AccessoryCategory,
    PeltPattern, TortiePattern, PeltColour, ColourTint, PeltLength, WhitePatchPattern, WhitePatchTint,
    EyeColour, SkinColour, ScarPelt, PeltAccessories,
    SPRITE_RANGES, VITILIGO_CHANCE_MODIFIER_PER_PARENT, POINT_CHANCE_MODIFIER_PER_PARENT,
    HETEROCHROMIA_CHANCE_MODIFIER_PER_PARENT, SpriteModifier,
)
from scripts._red.general_utils import one_in_num_chance
from scripts._red.config_manager import config

import logging
logger = logging.getLogger(__name__)


########################################################################################################################
# Constants
########################################################################################################################

CAT_GENERATION_SETTINGS: dict = config.get_config_value("cat_generation")


########################################################################################################################
# Classes
########################################################################################################################

# @dataclass
class Genome:
    """ Holds integer chances for each inheritable trait category. Default values are for random cat generation. """
    tortie_possible_f: bool = True
    tortie_chance_modifier: int = 0 # "base_male_tortie", "base_female_tortie"
    heterochromatic_chance_modifier: int = 0
    point_chance_modifier: int = 0
    vitiligo_chance_modifier: int = 0
    # permanent_condition_chance: int = CAT_GENERATION_SETTINGS["base_permanent_condition"]
    pattern: list[int] = PeltPatternCategory.Random.genetic_inheritance
    length: list[int] = PeltLengthCategory.Random.genetic_inheritance
    colour: list[int] = PeltColourCategory.Random.genetic_inheritance
    tortie_colour: list[int] = PeltColourCategory.Random.genetic_inheritance
    white_patch_pattern: list[int] = WhitePatchPatternCategory.Random.genetic_inheritance
    eye_colour: list[int] = EyeColourCategory.Random.genetic_inheritance
    skin_colour: list[int] = SkinColourCategory.Random.genetic_inheritance

    def get_lists(self):
        return ["pattern", "length", "colour", "tortie_colour", "white_patch_pattern", "eye_colour", "skin_colour"]
        # return [self.pattern, self.length, self.colour, self.tortie_colour,
        #         self.white_patch_pattern, self.eye_colour, self.skin_colour]


@dataclass
class CatPelt:
    """ Holds all appearance information for a cat.

    TODO
     - add def __repr__
     - add a game rule where only kittypets can be randomly generated with 'exotic' pelts
     - if you have an all-white pelt, or no white patches, keep white patch pattern DNA but remove white patches
     - add all sprites
     - set specific sprite
        - self.curr_sprite
        - change health - sick, healthy, para, scar
        - change dead cat sprites - StarClan, DarkForest, and faded
        - change age
        - add an accessory
        - remove an accessory
    """
    _genome: Genome = None
    _genetic_code_set_f: bool = False

    # TODO should be generated automatically by TextHandler
    short_text: str = None # this will appear on the cat's Profile
    text: str = None # name = "SingleColour"

    length: PeltLength = None # "short"
    colour: PeltColour = None # "WHITE"
    tortie_colour: Optional[PeltColour] = None # tortiecolour: str = None
    colour_tint: ColourTint = None # str = "none"
    pattern: Optional[PeltPattern] = None # None # this is also tortiebase, a str
    tortie_pattern: Optional[TortiePattern] = None # tortiepattern: str = None
    white_patch_pattern: Optional[WhitePatchPattern] = None # str
    white_patch_tint: WhitePatchTint = None # str = "none"
    skin_colour: SkinColour = None # skin: str = "BLACK"
    eye_colour: tuple[EyeColour, EyeColour] = None # "BLUE", eye_colour2 = None
    accessories: tuple = () # accessory: list = None # TODO
    scars: tuple = () # TODO

    curr_sprite: int = 0 # TODO
    cat_sprite_reverse: bool = False
    cat_sprite_kit: int = 0
    cat_sprite_adolescent: int = 0
    cat_sprite_adult: int = 0
    cat_sprite_elder: int = 0
    cat_sprite_opacity: int = 100

    def __init__(self, gender: GenderKits = None, parent_pelts: list = None, mother_pelt=None, father_pelt=None,
                 loading_from_save: bool = False, save_file: dict = None):
        """ Make a new pelt.

        :param gender: The gender of the cat whose pelt is being generated. Needed for tortoiseshell stuff.
        :param mother_pelt: The pelt of the cat's mother, if they have one.
        :ptype CatPelt: CatPelt
        :param father_pelt: The pelt of the cat's father, if they have one.
        :ptype CatPelt: CatPelt
        """
        if loading_from_save:
            self._load_pelt_from_save(save_file)

        else:
            if not isinstance(gender, GenderKits):
                raise TypeError(f"Can't generate a CatPelt without a valid gender. {gender} is not a GenderKits object")

            # Any parent pelts passed to CatPelt should also be CatPelt objects
            if not parent_pelts:
                parent_pelts = []
            for p_pelt in parent_pelts:
                if not isinstance(p_pelt, type(self)):
                    raise TypeError(f"Tried to use non-CatPelt object for genetic inheritance: {p_pelt}")

            # Make sure genetic code is set
            if not self._genetic_code_set_f:
                self._set_genetic_code(parent_pelts)

            # Decide if the cat is a tortoiseshell
            if not parent_pelts:
                tortie_f: bool = one_in_num_chance(num=CAT_GENERATION_SETTINGS["wildcard_tortie"])
            else:
                if self._genome.tortie_possible_f:
                    if gender is GenderKits.Male:
                        tortie_f: bool = one_in_num_chance(
                            num=CAT_GENERATION_SETTINGS["base_male_tortie"],
                            modifier=self._genome.tortie_chance_modifier)
                    else:
                        tortie_f: bool = one_in_num_chance(
                            num=CAT_GENERATION_SETTINGS["base_female_tortie"],
                            modifier=self._genome.tortie_chance_modifier)
                else:
                    tortie_f = False

            # Generate a pelt
            self._pick_pelt_length(parent_pelts=parent_pelts)
            self._pick_colours_and_colour_tint(tortie_f=tortie_f, parent_pelts=parent_pelts)
            self._pick_patterns(parent_pelts=parent_pelts)
            self._pick_white_patches_and_white_patch_tint(parent_pelts=parent_pelts)
            self._pick_sprites()
            self._pick_eye_colours(parent_pelts=parent_pelts)
            self._pick_skin_colour(parent_pelts=parent_pelts)

        return

    # ------------------------------------ PUBLIC ------------------------------------ #

    def update_sprite(self, sprite_mod: SpriteModifier, age: Age = None):
        # Cat gets sick/hurt, heals, and becomes paralyzed
        if sprite_mod is SpriteModifier.GetSick:
            pass
        if sprite_mod is SpriteModifier.FeelBetter:
            pass
        if sprite_mod is SpriteModifier.Paralyze:
            pass

        # Cat gets new swag or gives their swag away
        if sprite_mod is SpriteModifier.GiveAccessory:
            pass
        if sprite_mod is SpriteModifier.TakeAccessory:
            pass

        # Cat ages up
        if sprite_mod is SpriteModifier.AgeChange:
            pass
            # if age is None:
            #     raise TypeError(f"Tried to update cat age without a valid Age parameter")
            # else:
            #     pass

        # Sucks to suck
        if sprite_mod is SpriteModifier.StarClan:
            pass
        if sprite_mod is SpriteModifier.DarkForest:
            pass
        if sprite_mod is SpriteModifier.UnknownResidence:
            pass
        if sprite_mod is SpriteModifier.Faded:
            pass

        raise NotImplementedError("CatPelt.update_sprite")

    # ------------------------------------ PRIVATE ----------------------------------- #

    def _load_pelt_from_save(self, save: dict):
        """ Parse the dictionary from a save file to buld this CatPelt object. """
        self.length = PeltLength(save["length"])
        self.colour = PeltColour(save["colour"])
        self.colour_tint = ColourTint(save["colour_tint"])
        self.tortie_colour = PeltColour(save["tortie_colour"])
        self.pattern = PeltPattern(save["pattern"])
        self.tortie_pattern = TortiePattern(save["tortie_pattern"])
        self.white_patch_pattern = WhitePatchPattern(save["white_patch_pattern"])
        self.white_patch_tint = WhitePatchTint(save["white_patch_tint"])
        self.skin_colour = SkinColour(save["skin_colour"])
        self.eye_colour = tuple( EyeColour(save["eye_colour"][0]), EyeColour(save["eye_colour"][1]) )
        accessories = []
        for a in save["accessories"]:
            accessories.append(PeltAccessories(a))
        self.accessories = tuple(accessories)
        scars = []
        for s in save["scars"]:
            scars.append(ScarPelt(s))
        self.scars = tuple(scars)

        sprites = save["sprite"]
        self.curr_sprite = sprites["curr_sprite"]
        self.cat_sprite_reverse = sprites["reverse"]
        self.cat_sprite_kit = sprites["kitten"]
        self.cat_sprite_adolescent = sprites["adolescent"]
        self.cat_sprite_adult = sprites["adult"]
        self.cat_sprite_elder = sprites["senior"]
        self.cat_sprite_opacity = sprites["opacity"]

        return

    def _set_genetic_code(self, parent_pelts: list = None):
        """ Set the weights for all aspects of the pelt. """
        self._genome = Genome()

        if parent_pelts:
            if len(parent_pelts) == 1:
                # if we only have one parent, then use random genetics for the second parent
                p_pelt = parent_pelts.pop()

            else:
                temp_pelt = parent_pelts.pop(0)
                p_pelt = parent_pelts.pop(0)

                # if we have enough parents, only use their genes, no random genetics
                self._genome = temp_pelt._genome

                # cats can be torties if one of their parents is a tortie OR if their parents are ginger and black
                tortie_condition = any([temp_pelt.tortie_colour, p_pelt.tortie_colour])
                no_tortie_condition = [temp_pelt.colour.category, p_pelt.colour.category].count(PeltColourCategory.Ginger) != 1
                if tortie_condition and not no_tortie_condition:
                    self._genome.tortie_possible_f = True
                else:
                    self._genome.tortie_possible_f = False

                # self._genome.pattern = temp_pelt._genome.pattern.genetic_inheritance
                # self._genome.length = temp_pelt._genome.length.genetic_inheritance
                # self._genome.colour = temp_pelt._genomecolour.genetic_inheritance
                # self._genome.tortie_colour = temp_pelt._genome.tortie_colour.genetic_inheritance
                # self._genome.white_patch_pattern = temp_pelt._genome.white_patch_pattern.genetic_inheritance
                # self._genome.eye_colour = temp_pelt._genome.eye_colour.genetic_inheritance
                # self._genome.skin_colour = temp_pelt._genome.skin_colour.genetic_inheritance

            for gene_name in self._genome.get_lists():
                p_gene = p_pelt._genome.__getattribute__(gene_name)
                gene = self._genome.__getattribute__(gene_name)
                # logger.debug(f"{gene_name} : gene={gene}\tp_gene={p_gene}")
                for i in range(len(gene)):
                    gene[i] += p_gene[i]
            # if the parent has vitiligo, colour points, or heterochromia, make those more likely
            if p_pelt.white_patch_pattern.category is WhitePatchPatternCategory.Vitiligo:
                self._genome.vitiligo_chance_modifier += VITILIGO_CHANCE_MODIFIER_PER_PARENT
            if p_pelt.white_patch_pattern.category is WhitePatchPatternCategory.Point:
                self._genome.point_chance_modifier += POINT_CHANCE_MODIFIER_PER_PARENT
            if p_pelt.eye_colour[0] is not p_pelt.eye_colour[1]:
                self._genome.point_chance_modifier += HETEROCHROMIA_CHANCE_MODIFIER_PER_PARENT

        self._genetic_code_set_f = True

    def _pick_pelt_length(self, parent_pelts):
        # depending on game settings, there is a chance that one of the parent's traits is directly inherited
        if parent_pelts and one_in_num_chance(num=CAT_GENERATION_SETTINGS["direct_inheritance"]):
            self.length = choice(parent_pelts).length
            return

        length_category = random.choices(
            population=
                [length for length in list(PeltLengthCategory) if length is not PeltLengthCategory.Random],
            weights=self._genome.length,
            k=1)[0]
        self.length = random.choice([l for l in list(PeltLength) if l.category is length_category])
        return

    def _pick_colours_and_colour_tint(self, tortie_f: bool, parent_pelts: list):
        """
        Pick the cat's colour(s). The default colour for tortie_colour is ginger, so:
        If the cat is a tortie, randomize the base colour to anything other than ginger.
        If the cat isn't a tortie, set tortie_colour to None and randomize pelt colour.
        """
        def randomize_tortie_colour():
            """ Pick colour and colour tint before using this. """
            # torties are ginger and a non-ginger colour (and the non-ginger colour can't be white)
            colour_category_order = list(self.colour.category.get_order())
            ginger_index = colour_category_order.index(PeltColourCategory.Ginger)
            if self.colour.category is PeltColourCategory.Ginger:
                self._genome.colour[ginger_index] = 0
            else:
                self._genome.colour = [0] * len(colour_category_order)
                self._genome.colour[ginger_index] = 1
            tortie_colour_category = random.choices(
                population=[colour for colour in list(PeltColourCategory)
                            if colour is not PeltColourCategory.Random],
                weights=self._genome.colour,
                k=1)[0]
            self.tortie_colour = choice([c for c in PeltColour if c.category is tortie_colour_category])

            # torties' non-ginger colour can't be white
            if self.colour is PeltColour.White:
                # a different pelt colour in the same PeltColourCategory as White
                self.colour = PeltColour.Silver
            if self.tortie_colour is PeltColour.White:
                # a different pelt colour in the same PeltColourCategory as White
                self.tortie_colour = PeltColour.Silver
            return

        # depending on game settings, there is a chance that one of the parent's traits is directly inherited
        if parent_pelts and one_in_num_chance(num=CAT_GENERATION_SETTINGS["direct_inheritance"]):
            if len(parent_pelts) == 1:
                # if only one parent, give them the parent's colour
                self.colour = parent_pelts[0].colour
                self.colour_tint = parent_pelts[0].colour_tint
                if tortie_f:
                    if parent_pelts[0].tortie_colour:
                        self.tortie_colour = parent_pelts[0].tortie_colour
                    else:
                        randomize_tortie_colour()
                else:
                    self.tortie_colour = None
                return
            else:
                # if two parents, inherited pelt colour(s) depends on tortie status of kit and parents
                if tortie_f:
                    if parent_pelts[0].tortie_colour: # tortie kit + tortie parent_1 = make kit identical to parent_1
                        self.colour = parent_pelts[0].colour
                        self.colour_tint = parent_pelts[0].colour_tint
                        self.tortie_colour = parent_pelts[0].tortie_colour
                    elif parent_pelts[1].tortie_colour: # tortie kit + tortie parent_2 = make kit identical to parent_2
                        self.colour = parent_pelts[1].colour
                        self.colour_tint = parent_pelts[1].colour_tint
                        self.tortie_colour = parent_pelts[1].tortie_colour
                    else: # tortie kit + no tortie parents = make kit a tortie of the parents' colours
                        self.colour = parent_pelts[0].colour
                        self.colour_tint = parent_pelts[0].colour_tint
                        self.tortie_colour = parent_pelts[1].colour
                else:
                    # if the kit isn't a tortie, just grab a random parent's base pelt colour
                    lucky_parent_pelt = choice(parent_pelts)
                    self.colour = lucky_parent_pelt.colour
                    self.colour_tint = lucky_parent_pelt.colour_tint
                return

        # randomly generate fur colour
        colour_category = random.choices(
            population=[colour for colour in list(PeltColourCategory) if colour is not PeltColourCategory.Random],
            weights=self._genome.colour,
            k=1)[0]
        self.colour = choice([c for c in PeltColour if c.category is colour_category])
        self.colour_tint = choice(self.colour.colour_tints)

        # pick torties' secondary fur colour
        if tortie_f:
            print(f"Hark, a tortie")
            randomize_tortie_colour()
        else:
            self.tortie_colour = None

        return

    def _pick_patterns(self, parent_pelts: list):
        # depending on game settings, there is a chance that one of the parent's traits is directly inherited
        if parent_pelts and one_in_num_chance(num=CAT_GENERATION_SETTINGS["direct_inheritance"]):
            self.pattern = choice(parent_pelts).pattern
        else:
            pattern_category = random.choices(
                population=[p for p in list(PeltPatternCategory) if p is not PeltPatternCategory.Random],
                weights=self._genome.pattern,
                k=1)[0]
            self.pattern = choice([p for p in PeltPattern if p.category is pattern_category])
        if self.tortie_colour:
            # IRL tortie patterns are always 100% random so this works
            self.tortie_pattern = choice(list(TortiePattern))
        return

    def _pick_white_patches_and_white_patch_tint(self, parent_pelts: list):
        """ If a tortoiseshell has low- or mid-white, they're a tortie; if they have more white than that,
        they're a calico. Torties can also have vitiligo and be pointed; it's very cute.
        """
        # TODO white patches
        #  points
        #       CAT_GENERATION_SETTINGS["random_point_chance"]
        #       torties can't be pointed in ClanGen/Clan Sim (they can in IRL)
        #       your white patches are high_white or higher
        #  vitiligo
        #       CAT_GENERATION_SETTINGS["vit_chance"]
        #       anyone can roll vitiligo, not just cats who rolled to have white in their pelt
        #       if your white patch qualifies as vitiligo, don't use a white patch tint
        #  other white patches
        #       Calicos with white patches are Torties
        # Roll for the random chance of being pointed or having vitiligo
        # if one_in_num_chance(num=CAT_GENERATION_SETTINGS["random_point_chance"],
        #                           modifier=self._genome.point_chance_modifier):
        #     points = [point for point in WhitePatchPattern if point.category is WhitePatchPatternCategory.Point]
        #     white_patch_pattern = random.choice(points)
        # elif one_in_num_chance(num=CAT_GENERATION_SETTINGS["vit_chance"],
        #                             modifier=self._genome.vitiligo_chance_modifier):
        #     vitiligo = [point for point in WhitePatchPattern if point.category is WhitePatchPatternCategory.Vitiligo]
        #     white_patch_pattern = random.choice(vitiligo)
        # else:
        #     unallowed: list[WhitePatchPatternCategory] = [
        #         WhitePatchPatternCategory.Point, WhitePatchPatternCategory.Vitiligo, WhitePatchPatternCategory.Random]
        white_patch_pattern = None
        white_patch_tint = None

        try:
            if self.colour is PeltColour.White:
                # white cats don't have white patches
                white_patch_pattern = WhitePatchPattern.NoWhitePatch
                white_patch_tint = WhitePatchTint.NoTint
            elif parent_pelts and one_in_num_chance(num=CAT_GENERATION_SETTINGS["direct_inheritance"]):
                # depending on game settings, there is a chance that one of the parent's traits is directly inherited
                lucky_parent_pelt = choice(parent_pelts)
                white_patch_pattern = lucky_parent_pelt.white_patch_pattern
                if not self.tortie_colour:
                    white_patch_tint = lucky_parent_pelt.white_patch_tint

            # randomly generate
            else:
                white_patch_pattern_category = random.choices(
                    population=[
                        p for p in list(WhitePatchPatternCategory) if p is not WhitePatchPatternCategory.Random],
                    weights=self._genome.white_patch_pattern,
                    k=1)[0]
                if white_patch_pattern_category is WhitePatchPatternCategory.NoWhitePatch:
                    # Cats without white patches don't get white patch tints
                    white_patch_pattern = WhitePatchPattern.NoWhitePatch
                    white_patch_tint = WhitePatchTint.NoTint
                elif self.tortie_colour:
                    # Torties and calicos don't get white patch tints
                    white_patch_tint = WhitePatchTint.NoTint
                if white_patch_pattern_category is not WhitePatchPatternCategory.NoWhitePatch:
                    white_patch_pattern = choice(
                        [p for p in WhitePatchPattern if p.category is white_patch_pattern_category])

            # Now that we have a white patch pattern picked out, pick a tint and we're done.
            white_patch_tint = choice(self.colour.white_patch_tints)

        except IndexError as e:
            logger.exception(f"Tried to pick a white patch pattern from an empty sequence", e)
            logger.error(f"After failing to pick a white patch pattern, "
                         f"CatPelt is defaulting to a random low-white patch with no tint.")
            white_patch_pattern = choice(
                [p for p in WhitePatchPattern if p.category is WhitePatchPatternCategory.Low])

        except AttributeError as e:
            logger.exception(f"Somehow CatPelt managed to set self.white_patch_pattern as a member of the "
                             f"WhitePatchPatternCategory class, instead of the WhitePatchPattern class.", e)
            logger.error(f"After failing to pick a white patch pattern, "
                         f"CatPelt is defaulting to a random low-white patch with no tint.")
            white_patch_pattern = choice(
                [p for p in WhitePatchPattern if p.category is WhitePatchPatternCategory.Low])

        finally:
            if white_patch_pattern:
                self.white_patch_pattern = white_patch_pattern
            else:
                self.white_patch_pattern = WhitePatchPattern.NoWhitePatch
            if white_patch_tint:
                self.white_patch_tint = white_patch_tint
            else:
                self.white_patch_tint = WhitePatchTint.NoTint

        return

    def _pick_sprites(self):
        # Pick the cat's sprites
        self.cat_sprite_reverse = one_in_num_chance(num=2)
        self.cat_sprite_kit = random.randint(*SPRITE_RANGES['sprite_kit'])
        self.cat_sprite_adolescent = random.randint(*SPRITE_RANGES['sprite_adolescent'])
        if self.length is PeltLength.Long:
            self.cat_sprite_adult = random.randint(*SPRITE_RANGES['sprite_adult_long'])
        else:
            self.cat_sprite_adult = random.randint(*SPRITE_RANGES['sprite_adult_short_med'])
        self.cat_sprite_elder = random.randint(*SPRITE_RANGES['sprite_elder'])
        return

    def _pick_eye_colours(self, parent_pelts: list):
        # depending on game settings, there is a chance that one of the parent's traits is directly inherited
        if parent_pelts and one_in_num_chance(num=CAT_GENERATION_SETTINGS["direct_inheritance"]):
            self.eye_colour = choice(parent_pelts).eye_colour
            return
        # Set the first eye's colour
        new_eyes = []
        eye_colour_category = random.choices(
            population=[c for c in list(EyeColourCategory) if c is not EyeColourCategory.Random],
            weights=self._genome.eye_colour,
            k=1)[0]
        new_eyes.append(choice([c for c in EyeColour if c.category is eye_colour_category]))
        # Set second eye's colour
        if one_in_num_chance(num=CAT_GENERATION_SETTINGS["base_heterochromia"],
                             modifier=self._genome.heterochromatic_chance_modifier):
            eye_colour_category = random.choices(
                population=[c for c in list(EyeColourCategory) if c is not EyeColourCategory.Random],
                weights=self._genome.eye_colour,
                k=1)[0]
            new_eyes.append(choice([c for c in EyeColour if
                                         (c.category is eye_colour_category and
                                          c is not new_eyes[0])]))
        else:
            new_eyes.append(new_eyes[0])

        self.eye_colour = tuple(new_eyes)
        return

    def _pick_skin_colour(self, parent_pelts: list):
        # depending on game settings, there is a chance that one of the parent's traits is directly inherited.
        if parent_pelts and one_in_num_chance(num=CAT_GENERATION_SETTINGS["direct_inheritance"]):
            self.skin_colour = choice(parent_pelts).skin_colour
            return
        skin_colour_category = random.choices(
            population=[c for c in list(SkinColourCategory) if c is not SkinColourCategory.Random],
            weights=self._genome.skin_colour,
            k=1)[0]
        self.skin_colour = choice([c for c in SkinColour if c.category is skin_colour_category])
        return