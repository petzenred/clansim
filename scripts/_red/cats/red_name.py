""" red_name.py - Module that handles the name generation for all cats.

TODO
 - Separate naming for kittypets, loners and rogues, and Clan cats.
 - Legacy naming - potential for cats to specifically re-use the prefix OR suffix of a dead cat they loved.
 - Clans or leaders have preferred naming themes.
 - If a Clan cat's name is based on its appearance, account for that in their name's suffix.
    E.g. if a black cat's prefix is "Amber" for their eye colour, don't combine that with "pelt".
 - Can use events in a cat's life to determine suffix (e.g. Leafpool).
 - Instead of reading JSON files, read Python dictionaries?
 - Prefixes and suffixes shouldn't use the same source.
"""

import contextlib
import os
import random
import ujson
from typing import Optional


from definitions import (
    Age, Backstory, Biome, EyeColour,
    Location, PeltColour, PeltPattern, Rank,
    RedSkill, TortiePattern, BackstoryCategory,
)
from scripts._red.cat_tracker import cat_tracker
from scripts._red.conf_manager import conf
from scripts._red.general_utils import one_in_num_chance
from scripts.housekeeping.datadir import get_save_dir

import logging
logger = logging.getLogger(__name__)

########################################################################################################################
# Constants
########################################################################################################################

GAME_CONFIG_CAT_NAME_CONTROLS: dict = conf.get_config_value("cat_name_controls")
GAME_CONFIG_FUN: dict = conf.get_config_value("fun")

# FIXME remove the manual dictionary below
# GAME_CONFIG_CAT_NAME_CONTROLS: dict = {
#     "always_name_after_appearance": False,
#     "allow_eye_names": True,
# }
# GAME_CONFIG_FUN: dict = {
#     "april_fools": False,
#     "all_cats_are_newborn": False,
#     "newborns_can_roam": False,
#     "newborns_can_patrol": False,
#     "always_halloween": False
# }

NAMES_DICT_PATH: str = "../../../resources/dicts/names/names.json"
PREFIX_LIST_PATH: str = str(get_save_dir() + "/prefixlist.txt")
SUFFIX_LIST_PATH: str = str(get_save_dir() + "/suffixlist.txt")
SPEC_SUFFIX_LIST_PATH: str = str(get_save_dir() + "/specialsuffixes.txt")


########################################################################################################################
# Classes
########################################################################################################################

class RedName:
    """
    Stores & handles name generation.
    """

    cat = None
    prefix: str = None
    suffix: str = None
    special_suffix_hidden: bool = None

    prefix_source = None # used on the Allegiances screen
    suffix_source = None

    if os.path.exists(NAMES_DICT_PATH):
        logger.debug(f"Loading names dictionary from {NAMES_DICT_PATH}")
        with open(NAMES_DICT_PATH, encoding="utf-8") as read_file:
            names_dict = ujson.loads(read_file.read())

        if os.path.exists(PREFIX_LIST_PATH):
            logger.debug(f"Loading prefix lists from {PREFIX_LIST_PATH}")
            with open(
                PREFIX_LIST_PATH, "r", encoding="utf-8"
            ) as read_file:
                name_list = read_file.read()
                if_names = len(name_list)
            if if_names > 0:
                new_names = name_list.split("\n")
                for new_name in new_names:
                    if new_name != "":
                        if new_name.startswith("-"):
                            while new_name[1:] in names_dict["normal_prefixes"]:
                                names_dict["normal_prefixes"].remove(new_name[1:])
                        else:
                            names_dict["normal_prefixes"].append(new_name)

        if os.path.exists(SUFFIX_LIST_PATH):
            logger.debug(f"Loading suffix lists from {SUFFIX_LIST_PATH}")
            with open(SUFFIX_LIST_PATH, "r", encoding="utf-8") as read_file:
                name_list = read_file.read()
                if_names = len(name_list)
            if if_names > 0:
                new_names = name_list.split("\n")
                for new_name in new_names:
                    if new_name != "":
                        if new_name.startswith("-"):
                            while new_name[1:] in names_dict["normal_suffixes"]:
                                names_dict["normal_suffixes"].remove(new_name[1:])
                        else:
                            names_dict["normal_suffixes"].append(new_name)

        if os.path.exists(SPEC_SUFFIX_LIST_PATH):
            logger.debug(f"Loading special suffix lists from {SPEC_SUFFIX_LIST_PATH}")
            with open(SPEC_SUFFIX_LIST_PATH, "r", encoding="utf-8") as read_file:
                name_list = read_file.read()
                if_names = len(name_list)
            if if_names > 0:
                new_names = name_list.split("\n")
                for new_name in new_names:
                    if new_name != "":
                        if new_name.startswith("-"):
                            del names_dict["special_suffixes"][new_name[1:]]
                        elif ":" in new_name:
                            _tmp = new_name.split(":")
                            names_dict["special_suffixes"][_tmp[0]] = _tmp[1]
    else:
        logger.error(f"Could not find the name dictionary file at {NAMES_DICT_PATH}! "
                     f"Importing names from module instead")
        from resources.dicts.names.names import names_dict as ND
        names_dict = ND

    def __init__(
        self,
        prefix: str = None,
        suffix: str = None,
        special_suffix_hidden: bool = False,
        load_existing_name: bool = False,
        biome: Biome = None,
        cat_obj=None, # this is a RedCat object but the RedCat class imports RedName so it can't be type-hinted here
    ):
        self.prefix = prefix
        self.suffix = suffix
        self.special_suffix_hidden = special_suffix_hidden
        self.cat = cat_obj
        try:
            colour: Optional[PeltColour] = cat_obj.pelt.colour
            tortie_colour: Optional[PeltColour] = cat_obj.pelt.tortie_colour
            eyes: Optional[tuple[EyeColour, EyeColour]] = cat_obj.pelt.eye_colour
            pattern: Optional[PeltPattern] = cat_obj.pelt.pattern
            tortie_pattern: Optional[TortiePattern] = cat_obj.pelt.tortie_pattern
            skills: Optional = cat_obj.skills
            backstory = cat_obj.backstory
            rank = cat_obj.rank
        except AttributeError:
            colour = None
            tortie_colour = None
            eyes = None
            pattern = None
            tortie_pattern = None
            skills = None
            backstory = None
            rank = None

        if not load_existing_name:
            # decide prefix first
            while not self._verify_prefix():
                if backstory and backstory.category.outsider:
                    self.prefix = self.names_dict["loner_names"]
                else:
                    self.prefix_source = None
                    self._give_prefix(eye_colour=eyes, pelt_colour=colour, tortie_colour=tortie_colour, biome=biome)

            # decide suffix next
            while not self._verify_suffix():
                if rank and rank.outsider:
                    self.suffix = ""
                    continue
                else:
                    self.suffix_source = None
                    self._give_suffix(pattern=pattern, tortie_pattern=tortie_pattern, biome=biome, skills=skills)

        return

    def __str__(self):
        return self.__repr__()

    def _verify_prefix(self) -> bool:
        """ Check the chosen prefix is acceptable. """
        # Make sure the prefix exists before checking anything else
        if not self.prefix:
            return False
        # Check for prefix duplication within the cat's Clan. It's not unheard of for cats in different Clans
        #   to be using the same prefix (e.g. Lionblaze and Lioneye), so that's allowed.
        if self.prefix in cat_tracker.name_prefixes_per_clan[self.cat.clan_prefix]:
            return False
        return True

    def _give_prefix(self,
                    eye_colour: tuple[EyeColour, EyeColour] = None,
                    pelt_colour: PeltColour = None,
                    tortie_colour: PeltColour = None,
                    biome: Biome = None,
                    skills: dict[RedSkill: int] = None
        ):
        """ Generate a name prefix. """
        prefix_source: dict = {}

        try:
            def add_pelt_colour_prefix():
                if pelt_colour and pelt_colour.value.casefold() in self.names_dict["colour_prefixes"]:
                    prefix_source.update({
                        pelt_colour: self.names_dict["colour_prefixes"][pelt_colour.value.casefold()]
                    })
                    # if the cat is a tortoiseshell, include their tortie colour
                    if tortie_colour and tortie_colour.value.casefold() in self.names_dict["colour_prefixes"]:
                        prefix_source.update({
                            tortie_colour: self.names_dict["colour_prefixes"][tortie_colour.value.casefold()]
                        })
                return

            def add_eye_colour_prefix():
                if (eye_colour and
                        (
                                eye_colour[0].value.casefold() in self.names_dict["eye_prefixes"]
                                or
                                eye_colour[1].value.casefold() in self.names_dict["eye_prefixes"]
                        )
                ):
                    if eye_colour[0].value.casefold() in self.names_dict["eye_prefixes"]:
                        prefix_source.update({
                            eye_colour[0]: self.names_dict["eye_prefixes"][eye_colour[0].value.casefold()]
                        })
                    # account for heterochromia
                    if (eye_colour[0] is not eye_colour[1]
                            and eye_colour[1].value.casefold() in self.names_dict["eye_prefixes"]):
                        prefix_source.update({
                            eye_colour[1]: self.names_dict["eye_prefixes"][eye_colour[1].value.casefold()]
                        })
                return

            def add_biome_colour_prefixes():
                if biome and biome.value.casefold() in self.names_dict["biome_prefixes"]:
                    prefix_source.update({
                        biome: self.names_dict["biome_prefixes"][biome.value.casefold()]
                    })
                return

            # decide if the cat should be named after their eye colour, pelt colour, the biome they're from,
            #   or an ancestor
            if GAME_CONFIG_CAT_NAME_CONTROLS["always_name_after_appearance"]:
                if pelt_colour:
                    add_pelt_colour_prefix()
                if eye_colour:
                    add_eye_colour_prefix()
                # TODO chance for a cat to be named after their white patch pattern
                if not prefix_source:
                    raise KeyError(f"Game config says to only use appearances to name cats, "
                                   f"but no appearance data is available")

            else:
                 # chance for a cat to be named after their eye colour
                if one_in_num_chance(num=4):
                    add_eye_colour_prefix()
                # chance for a cat to be named after their pelt colour
                if one_in_num_chance(num=4):
                    add_pelt_colour_prefix()
                # TODO chance for a cat to be named after their white patch pattern
                # chance for a cat to be named after the biome they're from
                if one_in_num_chance(num=8):
                    add_biome_colour_prefixes()
                # TODO chance for a cat to be named after an ancestor
                # TODO chance for a cat to be named after their primary skill

            # pick a prefix
            self.prefix_source = random.choice( list(prefix_source.keys()) )
            self.prefix = random.choice( prefix_source[self.prefix_source] )

        except IndexError:
            logger.error(f"Chosen prefix sources didn't provide any possible prefixes - defaulting to normal_prefixes")
            self.prefix = random.choice(self.names_dict["normal_prefixes"])

        except Exception as e:
            logger.exception(e)
            logger.error(f"Something went wrong while trying to choose a prefix source - defaulting to normal_prefixes")
            self.prefix = random.choice(self.names_dict["normal_prefixes"])

        return

    def _verify_suffix(self) -> bool:
        """ Ensure the chosen suffix is acceptable. """
        # Make sure the suffix has been set before checking anything
        if not self.suffix:
            return False
        # Prevent the inappropriate names
        if str(self.prefix + self.suffix).casefold() in self.names_dict["inappropriate_names"]:
            return False
        # Prevent triple letter names from joining prefix and suffix from occurring (ex. Beeeye)
        if (self.prefix[-2:] + self.suffix[0]) or (self.prefix[-1] + self.suffix[:2]):
            return False
        # Prevent double animal names (ex. Spiderfalcon)
        if self.prefix in self.names_dict["animal_prefixes"] and self.suffix in self.names_dict["animal_suffixes"]:
            return False
        # Prevent double names (ex. Iceice)
        if self.prefix.casefold() != self.suffix.casefold():
            return False
        # Prevent suffixes containing the prefix (ex. Butterflyfly)
        if self.prefix in self.suffix or self.suffix in self.prefix:
            return False
        # TODO Prevent legacy-named cats from sharing a suffix with their namesake as well as a prefix
        return True


    def _give_suffix(self,
                    pattern: PeltPattern = None,
                    tortie_pattern: PeltPattern = None,
                    biome: Biome = None,
                    skills: dict = None
                    ):
        """ Generate a name suffix. """
        try:
            if pattern and GAME_CONFIG_CAT_NAME_CONTROLS["always_name_after_appearance"]:
                suffix_source: list[str] = self.names_dict["pattern_suffixes"][pattern.value.casefold()]
                if tortie_pattern and tortie_pattern.value in self.names_dict["tortie_pattern_suffixes"]:
                    suffix_source.extend(self.names_dict["tortie_pattern_suffixes"][tortie_pattern.value.casefold()])
                # TODO chance for a cat to be named after their white patch pattern

            else:
                suffix_source: list[str] = self.names_dict["normal_suffixes"]
                # chance for cat to be named after their pelt pattern or tortie pattern
                if (pattern and
                        pattern.value in self.names_dict["pattern_suffixes"] and
                        one_in_num_chance(num=8)):
                    # Chance for True is '1/8'.
                    suffix_source.extend(self.names_dict["pattern_suffixes"][pattern.value.casefold()])
                    if tortie_pattern and tortie_pattern.value in self.names_dict["tortie_pattern_suffixes"]:
                        suffix_source.extend(self.names_dict["tortie_pattern_suffixes"][tortie_pattern.value.casefold()])
                # TODO chance for a cat to be named after their white patch pattern
                # chance for cat to be named after the biome they're from
                if (biome and
                      biome.value in self.names_dict["biome_suffixes"] and
                      one_in_num_chance(num=8)):
                    # Chance for True is '1/8'.
                    suffix_source.extend(self.names_dict["biome_suffixes"][biome.value.casefold()])
                # TODO chance for cat to be named after their highest skill

        except:
            logger.error(f"Something went wrong while trying to choose a suffix source. Defaulting to normal suffixes")
            suffix_source = self.names_dict["normal_suffixes"]

        # pick a suffix
        self.suffix = random.choice(suffix_source)
        return


    def __repr__(self):
        # Handles predefined suffixes (such as leaders being -star),
        # and suffixes based on ages (fixes #2004, just trust me)

        # Handles suffix assignment with outside cats
        # FIXME this isn't how it works - Ravenpaw kept his name, and cats shouldn't get a warrior name unless and until they return to their Clan

        adjusted_status = Rank.Any
        if self.cat.location not in [Location.Exiled, Location.Lost]:
            if self.cat.moons == 0:
                adjusted_status = Age.Newborn
            elif self.cat.moons < 6:
                adjusted_status = Rank.Kit
            elif (self.cat.rank.value.casefold() in self.names_dict["special_suffixes"] and
                  not self.special_suffix_hidden):
                adjusted_status = self.cat.rank.value.casefold()
            elif GAME_CONFIG_FUN["april_fools"]:
                return f"{self.prefix}egg"

        if adjusted_status is not Rank.Any:
            return self.prefix + self.names_dict["special_suffixes"][adjusted_status.casefold()]
        else:
            return self.prefix + self.suffix

