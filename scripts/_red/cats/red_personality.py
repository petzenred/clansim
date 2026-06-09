# red_personality.py - Classes for keeping track of a cat's personality.

########################################################################################################################
# Imports
########################################################################################################################

from dataclasses import dataclass
from enum import IntEnum
from random import randint, choice

import logging

logger = logging.getLogger(__name__)


########################################################################################################################
# Constants and Paths
########################################################################################################################

########################################################################################################################
# Classes
########################################################################################################################

class HiddenPersonality(IntEnum):
    """ hidden personality quirks that cats can have which impact thoughts and relationship events """
    # note: these are int enums so they don't get spoiled in the save file
    Gossip = 1
    Funny = 2
    Romantic = 3 # these cats are more likely to develop crushes
    Judgemental = 4 # TODO
    Inappropriate = 5 # these cats are thoughtless - think Foxleap
    Obsessive = 6 # TODO maybe replace this with Intense?
    Altruistic = 7 # TODO maybe connect this to the wandering healer backgrounds?
    Neat = 8 # these cats hate messiness, groom themselves frequently, and don't get along with Messy cats
    Messy = 9 # these cats make a mess everywhere, don't stay very well groomed, and don't get along with Neat cats
    AppreciatesNature = 10 # these cats often stop to appreciate natural beauty
    LovesKits = 11 # these cats have mostly positive interactions with kits and apprentices, and gain Mentoring and
                   # KitSitting skill faster
    HatesKits = 12 # these cats have mostly negative interactions with kits and apprentices, and gain Mentoring and
                   # KitSitting skill slower
    Genius = 13 # these cats learn skills quickly but have a harder time getting along with other cats
    Familial = 14 # these cats have stronger relationships with family members, and are hit harder when family dies
    GhostWalker = 15 # these cats can talk to ghosts while they are awake
    LovesMentoring = 16 # these cats enjoy the challenges of mentoring, and will gain Mentoring skill faster
    HatesMentoring = 17 # these cats dislike the challenges of mentoring, and will gain Mentoring skill slower
    Perfectionist = 18 # these cats are harder on themselves and others when it comes to their duties
    Affectionate = 19 # TODO
    FreeSpirit = 20 # these cats are more likely to be discontent with Clan life and to question Clan rules and
                    # boundaries. They tend not to get along very well with cats who have a lot of Clan Pride or who
                    # are Traditional, and are more likely to support changes to Clan culture and the Warrior Code.
    Talkative = 21 # these cats never. Shut. Up.
    Territorial = 22 # TODO
    Hyperactive = 23 # these cats get unhappy if they don't go out on patrol for too long - or just do SOMETHING active!
    ClanPride = 24 # these cats hold their Clan above everything else, and value loyalty to it highly. They also don't
                   # get along very well with Free Spirits
    Glutton = 25 # these cats are always hungry
                 # TODO have that one patrol about breaking the Code by eating on patrol have said outcome be more
                 #  likely
    Attractive = 26 # other cats are more likely to develop crushes on this cat
    Traditional = 27 # these cats are less likely to agree with changes to the Clan's culture and the Warrior Code
    Picky = 28 # these cats are willing to eat SOME foods, and only those foods

    # TODO I would like to have conditional hidden traits - maybe some cats (children of leaders, legacy-named cats)
    #  could feel either proud or resentful of that legacy and its expectations

    # hopeful? bashful? perfectionist?


@dataclass
class RedPersonality:
    """ Class which tracks an individual cat's personality and hidden traits """
    # TODO add this to RedCat, RedCat._create_new_cat(), and RedCat._parse_cat_save_file()
    #  and RedCat.save() once I write it
    # TODO have the four attributes
    # TODO have a hidden personality trait
    # TODO keeps track of changes their mentor makes to their personality

    cat_id: int

    # facets
    """
    Facets can be found here (https://github.com/ClanGenOfficial/clangen/blob/development/resources/dicts/traits/trait_ranges.json).
    Facets operate on a range of 0-16. 0 is low. 16 is high. 8 can be considered a midpoint.

    Lawfulness
        Low: "I put little stock in rules, both my internal rules and the rules of those around me. I am quick to
            shrug off possible consequences."
        High: "I am strict in how I interface with the society I live within. I put a lot of stock in a moral code,
            though that code may be personal and private or society-wide and well-known."
    Sociability
        Low: "I struggle to navigate the social web around me and may struggle to understand what makes others tick."
        High: "I’m savvy in conversation and have a great understanding of how other cats think and behave."
    Aggression
        Low: "I am slow to confront both other cats and my own beliefs. I might act cautiously and may struggle to
            assert myself."
        High: "I assert myself in all I do, making my opinions clear and rarely waiting to consider what other
            cats want."
    Stability
        Low: "I am quick to change my opinions and make decisions. I don’t spend much time considering the
            consequences of what I do."
        High: "I am slow to change my opinions and make decisions. I’m consistent and grounded."
    """
    lawfulness: int #
    sociability: int #
    aggression: int #
    stability: int #

    # opinions of outsiders
    other_clans: int # range between 0 and 16 where 16 is xenophilic and 0 is xenophobic
    kittypets: int #
    loners: int

    # innate spiritual connections; ranges from 0 to 7, with a higher number indicating a stronger spiritual connection
    sc_connection: int
    df_connection: int

    # hidden
    hidden_trait: HiddenPersonality

    def __init__(self, cat_id: int, load_from_save: bool = False, **kwargs):
        self.cat_id = int(cat_id)
        if load_from_save:
            self._parse_cat_save_file(save_file=kwargs)
        else:
            self._create_new_personality(**kwargs)
        return

    # -------------------------------- SETTER METHODS -------------------------------- #

    def _parse_cat_save_file(self, save_file: dict):
        """ Parse the cat's personality values """
        try:
            self.lawfulness = int(save_file.pop("lawfulness"))
            self.sociability = int(save_file.pop("sociability"))
            self.aggression = int(save_file.pop("aggression"))
            self.stability = int(save_file.pop("stability"))

            self.sc_connection = int(save_file.pop("sc_connection"))
            self.df_connection = int(save_file.pop("df_connection"))

            self.other_clans = int(save_file.pop("other_clans"))
            self.kittypets = int(save_file.pop("kittypets"))
            self.loners = int(save_file.pop("loners"))

            self.hidden_trait = HiddenPersonality( randint(0, len(HiddenPersonality)) )

        except Exception as e:
            logger.exception(f"Something went wrong while reading the RedPersonality of cat_id={self.cat_id} from "
                             f"the save file",
                             exc_info=e)
        finally:
            return

    def _create_new_personality(self, **kwargs):
        """ Create a new personality from scratch.

        TODO
         - maybe change randint into something that will be weighed toward 8
        """
        # personality facets
        if "lawfulness" in kwargs:
            self.lawfulness = int(kwargs.pop("lawfulness"))
        else:
            self.lawfulness = randint(0, 16)
        if "sociability" in kwargs:
            self.sociability = int(kwargs.pop("sociability"))
        else:
            self.sociability = randint(0, 16)
        if "aggression" in kwargs:
            self.aggression = int(kwargs.pop("aggression"))
        else:
            self.aggression = randint(0, 16)
        if "stability" in kwargs:
            self.stability = int(kwargs.pop("stability"))
        else:
            self.stability = randint(0, 16)

        # opinions of outsiders
        # FIXME instead of these being randomly generated, they should be based on the Clan culture and affected by
        #  family and mentor opinions
        if "other_clans" in kwargs:
            self.other_clans = int(kwargs.pop("other_clans"))
        else:
            self.other_clans = randint(0, 16)
        if "kittypets" in kwargs:
            self.kittypets = int(kwargs.pop("kittypets"))
        else:
            self.kittypets = randint(0, 16)
        if "loners" in kwargs:
            self.loners = int(kwargs.pop("loners"))
        else:
            self.loners = randint(0, 16)

        # hidden
        if "sc_connection" in kwargs:
            self.sc_connection = int(kwargs.pop("sc_connection"))
        else:
            self.sc_connection = randint(0, 16)
        if "df_connection" in kwargs:
            self.df_connection = int(kwargs.pop("df_connection"))
        else:
            self.df_connection = randint(0, 16)
        if "hidden_trait" in kwargs:
            self.hidden_trait = HiddenPersonality(kwargs.pop("hidden_trait"))
        else:
            # TODO maybe give them more than one?
            self.hidden_trait = HiddenPersonality( randint(0, len(HiddenPersonality)) )

    # -------------------------------- GETTER METHODS -------------------------------- #

    def save(self):
        """ Convert this RedPersonality object to a dictionary """
        return {
            "lawfulness": self.lawfulness,
            "sociability": self.sociability,
            "aggression": self.aggression,
            "stability": self.stability,
            "sc_connection": self.sc_connection,
            "df_connection": self.df_connection,
            "other_clans": self.other_clans,
            "kittypets": self.kittypets,
            "loners": self.loners,
            "hidden_trait": self.hidden_trait,
        }
