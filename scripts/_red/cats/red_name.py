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

import random

from definitions import (
    Biome, EyeColour, PeltColour, PeltPattern,
    TortiePatches, Rank, RedSkill, WhitePatches,
    cast_to_biome, cast_to_skill
)
from resources._red.cat_names import SPECIAL_NAMES, OTHER, OUTSIDERS, PREFIXES, SUFFIXES
from scripts.game_structure.game_essentials import game
from scripts._red.io_manager import io_manager
from scripts._red.config_manager import config

import logging

logger = logging.getLogger(__name__)


########################################################################################################################
# Classes
########################################################################################################################

class RedName:
    """ Stores & handles name generation.

    TODO
     - legacy naming (prefix and suffix)
     - personalities (prefix and suffix)
     - skill (suffix) - this would require re-rolling their last name when they graduate
     - white patch pattern (prefix and suffix)
     - tortie pattern (prefix and suffix)
    """

    cat_obj = None  # this is a RedCat object but the RedCat class imports RedName so it can't be type-hinted here
    biome: Biome
    prefix: str
    suffix: str

    special_ranks: dict[Rank, str] = None

    _blacklist: list[str] = None
    _animal_names: list[str] = None

    prefix_source = None  # used (A) on the Allegiances screen (e.g. if a cat was named after their
    # eye colour, that will show up in their description in the allegiances)
    # (B) to make sure that cats' prefixes and suffixes don't contradict each other TODO
    # (C) to influence their warrior ceremony text TODO

    special_suffix_hidden_f: bool

    def __init__(
            self,
            cat_obj,
            save_file: dict = None,
            **kwargs
    ):
        """ TODO """
        self._blacklist = OTHER["blacklist"]
        self.special_ranks = OTHER["special_ranks_and_suffixes"]
        self._animal_names = OTHER["animal_parts"]

        self.cat_obj = cat_obj
        if save_file:
            self.prefix = save_file["prefix"]
            self.prefix_source = save_file["prefix_source"] # TODO this should be a TypeType, e.g. Biome
            self.suffix = save_file["suffix"]
            if self.suffix is None:
                self.suffix = ""
            self.special_suffix_hidden_f = bool(save_file["special_suffix_hidden_f"])
            pass
        else:
            if "prefix" in kwargs:
                self.prefix = kwargs["prefix"]
            if "prefix_source" in kwargs:
                self.prefix_source = kwargs["prefix_source"] # TODO this should be a TypeType, e.g. Biome
            if "suffix" in kwargs:
                self.suffix = kwargs["suffix"]
                if self.suffix is None:
                    self.suffix = ""
            if "biome" in kwargs:
                self.biome = cast_to_biome(to_cast=kwargs["biome"])
            if "special_suffix_hidden_f" in kwargs:
                self.special_suffix_hidden_f = bool(kwargs["special_suffix_hidden_f"])

            # decide prefix first
            # if the cat isn't a Clan cat, give them an appropriate name
            if hasattr(self.cat_obj, "rank") and self.cat_obj.rank.is_outsider:
                self.prefix_source = None
                self.prefix = random.choice(OUTSIDERS[self.cat_obj.rank])
            else:
                # generate a Clan cat prefix
                self.prefix_source, self.prefix = self.get_random_prefix()
                self.prefix = self.prefix.title()
            logger.debug(f"Attempting to verify name prefix for cat #{self.cat_obj.cat_id}")

            # decide suffix next
            if hasattr(self.cat_obj, "rank") and not self.cat_obj.rank.is_outsider:
                self.suffix = self.get_random_suffix()
            logger.debug(f"Attempting to verify name suffix for cat #{self.cat_obj.cat_id}")

        return

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        # Handles predefined suffixes (such as leaders being -star),
        # and suffixes based on ages (fixes #2004, just trust me)

        # ClanGen adjusts ranks automatically for cats who are lost and exiled (e.g. 6-month-olds always go from
        #   -kit to -paw), but that's not how it works (e.g. Ravenpaw kept his name, and cats shouldn't get a
        #   warrior name unless and until they return to their Clan) so ClanSim does not.

        if config.game_config.april_fools:
            return f"{self.prefix}egg"

        if self.cat_obj.rank in self.special_ranks:
            return self.prefix + self.special_ranks[self.cat_obj.rank]
        else:
            return self.prefix + self.suffix

    def get_random_prefix(self) -> tuple:
        """ Generate a name prefix.

        :return Any | None: prefix source (a class like EyeColour, PeltColour, etc.). None indicates the name is
            from the 'normal'/random list
        :return str: a randomly chosen prefix from the indicated source
        """
        _the_cat_prefixes: dict = {}

        # name after appearance
        # TODO game setting for only naming cats after their appearance?
        if hasattr(self.cat_obj, "pelt") and self.cat_obj.pelt is not None:
            # name after pelt colour
            if config.settings.NamesUsePeltColour:
                # if the cat's pelt is covered up by a full-body white patch, it makes no
                # sense for them to be named after their pelt's underlying/invisible colour
                if self.cat_obj.white_patches is not WhitePatches.FullWhite \
                    and self.cat_obj.pelt.colour in PREFIXES[PeltColour]:
                    _the_cat_prefixes[PeltColour] = PREFIXES[PeltColour][self.cat_obj.pelt.colour]

            # name after eye colour
            if config.settings.NamesUseEyeColour:
                if self.cat_obj.pelt.eye_colour in PREFIXES[EyeColour]:
                    _the_cat_prefixes[EyeColour] = PREFIXES[EyeColour][self.cat_obj.pelt.eye_colour]

            # name after pelt pattern # TODO also tortie_pattern, if that comes back
            if config.settings.NamesUsePeltPattern:
                # if the cat's pelt is covered up by a full-body white patch, it makes no
                # sense for them to be named after their pelt's underlying/invisible pattern
                if self.cat_obj.white_patches is not WhitePatches.FullWhite \
                    and self.cat_obj.pelt.pattern in PREFIXES[PeltPattern]:
                    _the_cat_prefixes[PeltPattern] = PREFIXES[PeltPattern][self.cat_obj.pelt.pattern]

            # name after white patch pattern
            if config.settings.NamesUseWhitePatchPattern:
                if self.cat_obj.pelt.white_patches in PREFIXES[WhitePatches]:
                    _the_cat_prefixes[WhitePatches] = PREFIXES[WhitePatches][
                        self.cat_obj.pelt.white_patches]

            # name after tortie patches
            if config.settings.NamesUseTortiePatches:
                # if the cat's pelt is covered up by a full-body white patch, it makes no
                # sense for them to be named after their pelt's underlying/invisible pattern
                if self.cat_obj.white_patches is not WhitePatches.FullWhite \
                        and self.cat_obj.pelt.tortie_patches in PREFIXES[TortiePatches]:
                    _the_cat_prefixes[TortiePatches] = PREFIXES[TortiePatches][self.cat_obj.pelt.tortie_patches]

        # name after Clan biome
        if config.settings.NamesUseBiome:
            if self.biome is not Biome.NoBiome and self.biome in PREFIXES[Biome]:
                _the_cat_prefixes[Biome] = PREFIXES[Biome][self.biome]

        # TODO name after a dead cat
        if config.settings.NamesUseLegacy:
            pass

        # TODO name after personality

        # pick a valid prefix and return it
        prefix = ""
        if not _the_cat_prefixes:
            logger.warning(f"Couldn't find any potential prefixes for cat #{self.cat_obj.cat_id}; "
                           f"defaulting to random prefix")
            # None is the key for the list of "normal"/random names
            prefix_source = None
            while not self._verify_prefix(prefix=prefix):
                prefix = random.choice(PREFIXES[prefix_source])
        else:
            while not self._verify_prefix(prefix=prefix):
                prefix_source = random.choice(list(_the_cat_prefixes.keys()))
                prefix = random.choice(_the_cat_prefixes[prefix_source])
        return prefix_source, prefix

    def get_random_suffix(self) -> str:
        """ Generate a name suffix. """
        # no need to track suffix source
        _the_cat_suffixes: dict = {}

        # decide if the cat should be named after their appearance, the biome they're from, their strongest skill,
        #   or a dead cat

        # TODO implement prefix-suffix matching using self.prefix_source
        #   For example, if the cat is solid black with amber eyes, and the chosen prefix is "Amber"
        #   after the eye colour, don't let the suffix be "fur" or "pelt"

        # name after Clan biome
        if config.settings.NamesUseBiome:
            if self.biome is not Biome.NoBiome and self.biome in SUFFIXES[Biome]:
                _the_cat_suffixes[Biome] = SUFFIXES[Biome][self.biome]

        # name after appearance
        if hasattr(self.cat_obj, "pelt") and self.cat_obj.pelt is not None:
            # name after pelt pattern # TODO also tortie_pattern, if that comes back
            if (config.settings.NamesUsePeltPattern
                    and self.cat_obj.pelt.pattern in SUFFIXES[PeltPattern]):
                _the_cat_suffixes[PeltPattern] = SUFFIXES[PeltPattern][self.cat_obj.pelt.pattern]

            # name after tortie patches
            if (config.settings.NamesUseTortiePatches
                    and self.cat_obj.pelt.tortie_patches in SUFFIXES[TortiePatches]):
                _the_cat_suffixes[TortiePatches] = SUFFIXES[TortiePatches][self.cat_obj.pelt.tortie_patches]

            # name after white patch pattern
            if (config.settings.NamesUseWhitePatchPattern
                    and self.cat_obj.pelt.white_patches in SUFFIXES[WhitePatches]):
                _the_cat_suffixes[WhitePatches] = \
                    SUFFIXES[WhitePatches][self.cat_obj.pelt.white_patches]

        # TODO name after the cat's strongest skill
        if config.settings.NamesUseSkill:
            pass

        # TODO name after a dead cat
        if config.settings.NamesUseLegacy:
            pass

        # pick a suffix
        suffix = ""
        if not _the_cat_suffixes:
            logger.warning(f"Couldn't find any potential suffixes for cat #{self.cat_obj.cat_id}; "
                           f"defaulting to random suffix")
            # None is the key for the list of "normal"/random names
            while not self._verify_suffix(suffix=suffix):
                suffix = random.choice(SUFFIXES[None])
        else:
            while not self._verify_suffix(suffix=suffix):
                suffix_source = random.choice(_the_cat_suffixes)
                suffix = random.choice(SUFFIXES[suffix_source])
        return suffix

    def _verify_prefix(self, prefix: str) -> bool:
        """ Check the chosen prefix is acceptable. """
        # Make sure the prefix exists before checking anything else
        if not prefix:
            return False
        # Check for prefix duplication within the cat's Clan. It's not unheard of for cats in different Clans
        #   to be using the same prefix (e.g. Lionblaze and Lioneye), so that's allowed.
        if prefix in game.cat_tracker.get_name_prefixes_of_clan(clan_token=self.cat_obj.clan_token):
            return False
        return True

    def _verify_suffix(self, suffix: str) -> bool:
        """ Ensure the chosen suffix is acceptable. """
        # Some checks only make sense for Clan cats
        if not self.cat_obj.rank.is_outsider:
            # Make sure the suffix has been set before checking anything
            if not suffix:
                return False
            # Prevent triple letter names from joining prefix and suffix from occurring (ex. Beeeye)
            # FIXME: this assumes both a prefix and a suffix of at least 3 letters
            if (self.prefix[-2:] + suffix[0]) or (self.prefix[-1] + suffix[:2]):
                return False
            # Prevent suffixes containing the prefix (ex. Butterflyfly)
            if self.prefix in suffix or suffix in self.prefix:
                return False

        # Prevent the inappropriate names
        if str(self.prefix + suffix).casefold() in self._blacklist:
            return False
        # Prevent double animal names (ex. Spiderfalcon)
        if self.prefix in self._animal_names and suffix in self._animal_names:
            return False
        # Prevent double names (ex. Iceice)
        if self.prefix.casefold() == suffix.casefold():
            return False
        # TODO Prevent legacy-named cats from sharing a suffix with their namesake as well as a prefix
        #   It is fine for the prefix and suffix to both be legacy names, as long as they're from different cats
        return True
