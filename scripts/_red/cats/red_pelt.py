# red_pelt.py - Enums, dataclasses, and classes related to cat appearance.
import random
from dataclasses import dataclass
from random import choice
from sys import exc_info
from typing import Optional

from definitions import (
    GenderKits,
    PeltPatternCategory, PeltColourCategory, PeltLengthCategory, WhitePatchCategory,
    EyeColourCategory, SkinColourCategory, PeltPattern, TortiePatches, PeltColour, ColourTint, PeltLength,
    WhitePatches, WhitePatchTint,
    EyeColour, SkinColour, ScarName, AccessoryName,
    SPRITE_RANGES, VITILIGO_CHANCE_MODIFIER_PER_PARENT, POINT_CHANCE_MODIFIER_PER_PARENT,
    HETEROCHROMIA_CHANCE_MODIFIER_PER_PARENT, SpritePose,
)
from scripts._red.red_exceptions import InitializationError
from scripts._red.utils.general_utils import one_in_num_chance
from scripts._red.config_manager import config

import logging
logger = logging.getLogger(__name__)


########################################################################################################################
# Classes
########################################################################################################################

@dataclass
class Genome:
    """ Holds integer weights for each inheritable trait category. Default values are for random cat generation. """
    tortie_possible_f: bool = True
    tortie_chance_modifier: int = 0 # "base_male_tortie", "base_female_tortie"
    heterochromatic_chance_modifier: int = 0
    point_chance_modifier: int = 0
    vitiligo_chance_modifier: int = 0
    # permanent_condition_chance: int = config.cat_config.hance_permanent_condition

    # *.genetic_inheritance is a list of integers, which I don't want to change to tuples for forward-compatibility
    #   reasons, but which can't be type-hinted because you can't type hint a mutable type in a dataclass.
    length = PeltLengthCategory.Random.genetic_inheritance
    colour = PeltColourCategory.Random.genetic_inheritance
    pattern = PeltPatternCategory.Random.genetic_inheritance
    tortie_colour = PeltColourCategory.Random.genetic_inheritance
    # TODO find a better name for tortie_patches_pattern - it's too easy to confuse it with tortie_patches
    tortie_patches_pattern = PeltPatternCategory.Random.genetic_inheritance
    # TODO change name to white_patches and WhitePatches, like TortiePatches
    white_patch_pattern = WhitePatchCategory.Random.genetic_inheritance
    eye_colour = EyeColourCategory.Random.genetic_inheritance
    skin_colour = SkinColourCategory.Random.genetic_inheritance

    def get_gene_names(self) -> list[str]:
        return ["length", "colour", "pattern",
                "tortie_colour", "tortie_patches_pattern",
                "white_patches", "eye_colour", "skin_colour"]


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

    sprites: dict[str, SpritePose]
    sprite_reverse: bool = False
    sprite_opacity: int = 100

    _genome: Genome = None
    _genetic_code_set_f: bool = False

    # TODO should be generated automatically by TextHandler
    short_text: str = None # this will appear on the cat's Profile screen
    text: str = None # this will appear in the allegiances

    # TODO should defaults be No* (e.g. ColourTint.NoTint) or None? Having
    #  both is confusing, but None doesn't work for StrEnum classes
    length: PeltLength = None
    colour: PeltColour = None
    tortie_colour: Optional[PeltColour] = None # tortie_colour: str | None, default = None
    colour_tint: ColourTint = None # tint: str, default="none"
    pattern: Optional[PeltPattern] = None # tortie_base: str
    tortie_patches: Optional[TortiePatches] = None # tortie_marking: str | None, default = None
    tortie_patches_pattern: Optional[PeltPattern] = None # tortie_pattern: str | None, default = None
    white_patches: Optional[WhitePatches] = None # white_patches: str | None, default = None
    white_patch_tint: WhitePatchTint = None # white_patches_tint: str | None, default = None
    skin_colour: SkinColour = None # skin: str
    eye_colour: tuple[EyeColour, EyeColour] = None # "BLUE", eye_colour2: str | None, default = None
    accessories: tuple = () # accessory: list[str] = [] # TODO
    scars: tuple = () # TODO


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
                tortie_f: bool = one_in_num_chance(num=config.cat_config.tortie_chance_wildcard)
            else:
                if self._genome.tortie_possible_f:
                    if gender is GenderKits.Male:
                        tortie_f: bool = one_in_num_chance(
                            num=config.cat_config.tortie_chance_male,
                            modifier=self._genome.tortie_chance_modifier)
                    else:
                        tortie_f: bool = one_in_num_chance(
                            num=config.cat_config.tortie_chance_female,
                            modifier=self._genome.tortie_chance_modifier)
                else:
                    tortie_f = False

            # Generate a pelt
            self._pick_pelt_length(parent_pelts=parent_pelts)
            self._pick_colours_and_colour_tint(tortie_f=tortie_f, parent_pelts=parent_pelts)
            self._pick_patterns(parent_pelts=parent_pelts)
            self._pick_white_patches_and_white_patch_tint(parent_pelts=parent_pelts)
            self._pick_sprite_poses() # this has to go after length is chosen
            self._pick_eye_colours(parent_pelts=parent_pelts)
            self._pick_skin_colour(parent_pelts=parent_pelts)

        return

    # ------------------------------------ PUBLIC ------------------------------------ #

    # TODO call this from RedCat.save_cat()
    def save_cat_pelt(self) -> dict[str, str | int | None]:
        """ Method called when saving the RedCat object that this pelt belongs to.

        :return dict: strings and ints that should be saved as-is in the save file
        """
        return {
            "length": self.length.value,
            "colour": self.colour.value,
            "colour_tint": self.colour_tint.value,
            "tortie_colour": self.tortie_colour.value,
            "pattern": self.pattern.value,
            "tortie_patches": self.tortie_patches.value,
            "tortie_patches_pattern": self.tortie_patches_pattern.value,
            "white_patches": self.white_patches.value,
            "white_patch_tint": self.white_patch_tint.value,
            "skin_colour": self.skin_colour.value,
            "eye_colour": [self.eye_colour[0].value, self.eye_colour[1].value],
            "accessories": [acc.value for acc in self.accessories],
            "scars": [scar.value for scar in self.scars],
            "sprite": {
                "reverse": self.sprite_reverse,
                "opacity": self.sprite_opacity,
                "newborn": self.sprites["newborn"].name,
                "kitten": self.sprites["kitten"].name,
                "adolescent": self.sprites["adolescent"].name,
                "adult": self.sprites["adult"].name,
                "senior": self.sprites["senior"].name
            }
        }

    # ------------------------------------ PRIVATE ----------------------------------- #

    def _load_pelt_from_save(self, save: dict):
        """ Parse the dictionary from a save file to buld this CatPelt object. """
        try:
            self._genome = Genome()

            # set pelt aspects without genetic inheritance
            self.colour_tint = ColourTint(save["colour_tint"])
            self.white_patch_tint = WhitePatchTint(save["white_patch_tint"])

            # set pelt aspects and genetic inheritance
            # set genome so genetic inheritance works for any kittens this cat has
            self.length = PeltLength(save["length"])
            self._genome.length = self.length.genetic_inheritance
            self.colour = PeltColour(save["colour"])
            self._genome.colour = self.colour.genetic_inheritance
            self.pattern = PeltPattern(save["pattern"])
            self._genome.pattern = self.pattern.genetic_inheritance
            # TODO make white_patches a list
            self.white_patches = WhitePatches(save["white_patches"])
            self._genome.white_patch_pattern = self.white_patches.genetic_inheritance
            self.skin_colour = SkinColour(save["skin_colour"])
            self._genome.skin_colour = self.skin_colour.genetic_inheritance
            self.eye_colour = ( EyeColour(save["eye_colour"][0]), EyeColour(save["eye_colour"][1]) )
            self._genome.eye_colour = self.eye_colour[0].genetic_inheritance
            if self.eye_colour[0].category != self.eye_colour[1].category: # heterochromia
                self._genome.eye_colour += self.eye_colour[1].genetic_inheritance

            # tortoiseshells
            # TODO test these with save["tortie_key"] = None
            if save["tortie_patches"]:
                self.tortie_patches = TortiePatches(save["tortie_patches"])
                self.tortie_colour = PeltColour(save["tortie_colour"])
                self.tortie_patches_pattern = PeltPattern(save["tortie_patches_pattern"])
                self._genome.tortie_colour = self.tortie_colour.genetic_inheritance
                self._genome.tortie_patches_pattern = self.tortie_patches_pattern.genetic_inheritance

            # set scars and accessories
            accessories = []
            for a in save["accessories"]:
                accessories.append(AccessoryName(a))
            self.accessories = tuple(accessories)
            scars = []
            for s in save["scars"]:
                scars.append(ScarName(s))
            self.scars = tuple(scars)

            # sprite poses
            sprites = save["sprite"]
            self.sprite_reverse = sprites.pop("reverse")
            self.sprite_opacity = sprites.pop("opacity")
            self.sprites = {}
            for age, name in sprites.items():
                if age == "adult":
                    if self.length is PeltLength.Long:
                        self.sprites[age] = SpritePose.__getitem__(name=name)
                    else:
                        self.sprites[age] = SpritePose.__getitem__(name=name)
                else:
                    self.sprites[age] = SpritePose.__getitem__(name=name)

            self._genetic_code_set_f = True
        except Exception as e:
            raise e

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
                no_tortie_condition = [temp_pelt.colour.category, p_pelt.colour.category]\
                                          .count(PeltColourCategory.Ginger) != 1
                if tortie_condition and not no_tortie_condition:
                    self._genome.tortie_possible_f = True
                else:
                    self._genome.tortie_possible_f = False

                # self._genome.pattern = temp_pelt._genome.pattern.genetic_inheritance
                # self._genome.length = temp_pelt._genome.length.genetic_inheritance
                # self._genome.colour = temp_pelt._genomecolour.genetic_inheritance
                # self._genome.tortie_colour = temp_pelt._genome.tortie_colour.genetic_inheritance
                # self._genome.white_patches = temp_pelt._genome.white_patches.genetic_inheritance
                # self._genome.eye_colour = temp_pelt._genome.eye_colour.genetic_inheritance
                # self._genome.skin_colour = temp_pelt._genome.skin_colour.genetic_inheritance

            for gene_name in self._genome.get_gene_names():
                p_gene = p_pelt._genome.__getattribute__(gene_name)
                gene = self._genome.__getattribute__(gene_name)
                # logger.debug(f"{gene_name} : gene={gene}\tp_gene={p_gene}")
                for i in range(len(gene)):
                    self._genome.__setattr__(gene_name, gene[i] + p_gene[i])
            # if the parent has vitiligo, colour points, or heterochromia, make those more likely
            if p_pelt.white_patches.category is WhitePatchCategory.Vitiligo:
                self._genome.vitiligo_chance_modifier += VITILIGO_CHANCE_MODIFIER_PER_PARENT
            if p_pelt.white_patches.category is WhitePatchCategory.Point:
                self._genome.point_chance_modifier += POINT_CHANCE_MODIFIER_PER_PARENT
            if p_pelt.eye_colour[0] is not p_pelt.eye_colour[1]:
                self._genome.point_chance_modifier += HETEROCHROMIA_CHANCE_MODIFIER_PER_PARENT

        self._genetic_code_set_f = True
        return

    def _pick_pelt_length(self, parent_pelts):
        # depending on game settings, there is a chance that one of the parent's traits is directly inherited
        if parent_pelts and one_in_num_chance(num=config.cat_config.chance_direct_inheritance):
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
        if parent_pelts and one_in_num_chance(num=config.cat_config.chance_direct_inheritance):
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
        """ Pick a pelt pattern (and potentially pattern for tortie patches) based on genetics. """
        pelts = []
        pelts_to_pick: int = 1 if not self.tortie_colour else 2
        for pelt_no in range(pelts_to_pick):
            # depending on game settings, there is a chance that some of the parents' traits are directly inherited
            if parent_pelts and one_in_num_chance(num=config.cat_config.chance_direct_inheritance):
                inherited_pelts = [pp.pattern for pp in parent_pelts]
                inherited_pelts.extend([pp.tortie_patches_pattern for pp in parent_pelts if pp.tortie_patches_pattern])
                pelts.append(choice(inherited_pelts))
            else:
                pattern_category = random.choices(
                    population=[p for p in list(PeltPatternCategory) if p is not PeltPatternCategory.Random],
                    weights=self._genome.pattern,
                    k=1)[0]
                pelts.append(choice([p for p in PeltPattern if p.category is pattern_category]))

        self.pattern = pelts[0]
        if self.tortie_colour:
            self.tortie_patches_pattern = pelts[1]
            # IRL tortie patterns are always 100% random so this works
            self.tortie_patches = choice(list(TortiePatches))

        return

    def _pick_white_patches_and_white_patch_tint(self, parent_pelts: list):
        """ If a tortoiseshell has low- or mid-white, they're a tortie; if they have more white than that,
        they're a calico. Torties can also have vitiligo and be pointed; it's very cute.
        """
        # TODO white patches
        #  points
        #       config.cat_config.["random_point_chance"]
        #       torties can't be pointed in ClanGen/Clan Sim (they can in IRL)
        #       your white patches are high_white or higher
        #  vitiligo
        #       config.cat_config.["vit_chance"]
        #       anyone can roll vitiligo, not just cats who rolled to have white in their pelt
        #       if your white patch qualifies as vitiligo, don't use a white patch tint
        #  other white patches
        #       Calicos with white patches are Torties
        # Roll for the random chance of being pointed or having vitiligo
        # if one_in_num_chance(num=config.cat_config.["random_point_chance"],
        #                           modifier=self._genome.point_chance_modifier):
        #     points = [point for point in WhitePatches if point.category is WhitePatchCategory.Point]
        #     white_patches = random.choice(points)
        # elif one_in_num_chance(num=config.cat_config.["vit_chance"],
        #                             modifier=self._genome.vitiligo_chance_modifier):
        #     vitiligo = [point for point in WhitePatches if point.category is WhitePatchCategory.Vitiligo]
        #     white_patches = random.choice(vitiligo)
        # else:
        #     unallowed: list[WhitePatchCategory] = [
        #         WhitePatchCategory.Point, WhitePatchCategory.Vitiligo, WhitePatchCategory.Random]
        white_patch_pattern = None
        white_patch_tint = None

        try:
            if self.colour is PeltColour.White:
                # white cats don't have white patches
                # TODO change this so the white patch isn't rendered, but the data is kept for inheritance reasons
                white_patch_pattern = WhitePatches.NoWhitePatch
                white_patch_tint = WhitePatchTint.NoTint
            elif parent_pelts and one_in_num_chance(num=config.cat_config.chance_direct_inheritance):
                # depending on game settings, there is a chance that one of the parent's traits is directly inherited
                lucky_parent_pelt = choice(parent_pelts)
                white_patch_pattern = lucky_parent_pelt.white_patch_pattern
                if not self.tortie_colour:
                    white_patch_tint = lucky_parent_pelt.white_patch_tint

            # randomly generate
            else:
                white_patch_pattern_category = random.choices(
                    population=[
                        p for p in list(WhitePatchCategory) if p is not WhitePatchCategory.Random],
                    weights=self._genome.white_patch_pattern,
                    k=1)[0]
                if white_patch_pattern_category is WhitePatchCategory.NoWhitePatch:
                    # Cats without white patches don't get white patch tints
                    white_patch_pattern = WhitePatches.NoWhitePatch
                    white_patch_tint = WhitePatchTint.NoTint
                elif self.tortie_colour:
                    # Torties and calicos don't get white patch tints
                    white_patch_tint = WhitePatchTint.NoTint
                if white_patch_pattern_category is not WhitePatchCategory.NoWhitePatch:
                    white_patch_pattern = choice(
                        [p for p in WhitePatches if p.category is white_patch_pattern_category])

            # Now that we have a white patch pattern picked out, pick a tint and we're done.
            white_patch_tint = choice(self.colour.white_patch_tints)

        except IndexError as e:
            logger.exception(f"Tried to pick a white patch pattern from an empty sequence", e)
            logger.error(f"After failing to pick a white patch pattern, "
                         f"CatPelt is defaulting to a random low-white patch with no tint.")
            white_patch_pattern = choice(
                [p for p in WhitePatches if p.category is WhitePatchCategory.Low])

        except AttributeError as e:
            logger.exception(f"Somehow CatPelt managed to set self.white_patches as a member of the "
                             f"WhitePatchCategory class, instead of the WhitePatches class.", e)
            logger.error(f"After failing to pick a white patch pattern, "
                         f"CatPelt is defaulting to a random low-white patch with no tint.")
            white_patch_pattern = choice(
                [p for p in WhitePatches if p.category is WhitePatchCategory.Low])

        finally:
            if white_patch_pattern:
                self.white_patches = white_patch_pattern
            else:
                self.white_patches = WhitePatches.NoWhitePatch
            if white_patch_tint:
                self.white_patch_tint = white_patch_tint
            else:
                self.white_patch_tint = WhitePatchTint.NoTint

        return

    def _pick_sprite_poses(self):
        """ Randomly pick sprite poses for each stage of the cat's life. """
        # Pick the cat's sprites
        self.sprite_reverse = random.choice([True, False])
        self.sprite_opacity = 100
        self.sprites = {
            "newborn": random.choice(SpritePose.get_age_sprites(age="newborn")),
            "kitten": random.choice(SpritePose.get_age_sprites(age="kitten")),
            "adolescent": random.choice(SpritePose.get_age_sprites(age="adolescent")),
            "senior": random.choice(SpritePose.get_age_sprites(age="senior")),
        }
        if self.length is PeltLength.Long:
            self.sprites["adult"] = random.choice(SpritePose.get_age_sprites(age="adult")[PeltLength.Long])
        else:
            self.sprites["adult"] = random.choice(SpritePose.get_age_sprites(age="adult")[PeltLength.Short])
        return

    def _pick_eye_colours(self, parent_pelts: list):
        # depending on game settings, there is a chance that one of the parent's traits is directly inherited
        if parent_pelts and one_in_num_chance(num=config.cat_config.chance_direct_inheritance):
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
        if one_in_num_chance(num=config.cat_config.base_chance_heterochromia,
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
        if parent_pelts and one_in_num_chance(num=config.cat_config.chance_direct_inheritance):
            self.skin_colour = choice(parent_pelts).skin_colour
            return
        skin_colour_category = random.choices(
            population=[c for c in list(SkinColourCategory) if c is not SkinColourCategory.Random],
            weights=self._genome.skin_colour,
            k=1)[0]
        self.skin_colour = choice([c for c in SkinColour if c.category is skin_colour_category])
        return