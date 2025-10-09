# base_event.py - Base class for event classes.

# -------------------------------------------------------------------------------- #
# ----------------------------------------

########################################################################################################################
# Imports
########################################################################################################################

########################################################################################################################
# Classes
########################################################################################################################



from dataclasses import dataclass, field
from enum import StrEnum
from types import NoneType
from typing import Union

from definitions import Event, EventCategory, Location, Rank, Season
from scripts.game_structure.game_essentials import game
from scripts._red.text_handler import text_handler


########################################################################################################################
# Enums and Dataclasses
########################################################################################################################

# TODO once secret histories are working, add a ConfessEvent class
#  if two cats know a secret, and there's another cat with a pelt identical to one of them who doesn't know,
#  have an event where the unknowing cat is accidentally told the secret by the non-identical cat

# text_handler.handle_text_content_event(text=, event=)

class EventType(StrEnum):
    """ An enum to classify different event types """

    Any = "any"
    Birth = "birth"
    # TODO implement BirthEvent class.
    #  Include the cat giving birth, the other parent(s), all cats being born
    Adoption = "adoption"
    # TODO implement AdoptEvent class.
    #  Include who is adopting, and who is being adopted
    Death = "death" # TODO implement DeathEvent class
    Patrol = "patrol" # TODO implement PatrolEvent class
    # TODO PatrolStart/PatrolEvent vs. PatrolOutcome?
    Interaction = "interaction" # TODO implement InteractionEvent class

    # ---------------------------------- Clan events --------------------------------- #

    ClanJoin = "clan_join"
    # TODO implement ClanJoin class
    #  old_rank: Rank - covers difference between loners, cats from other Clans, kittypets, etc.
    #  new_rank: Rank - covers difference between warriors, medicine cats, etc.
    #  clan: Clan - should this just be a string?
    #  cat_age: int -  age of the cat when they joined in moons
    #  clan_age: int - age of the Clan when the cat joined in moons
    #  founder: bool - did this cat join the Clan as it was being founded?
    ClanLeave = "clan_leave"
    # TODO implement ClanLeave class
    #  old_rank: Rank
    #  new_rank: Rank - covers difference between Rank.LeftClan and Rank.Exiled
    #  clan: Clan - should this just be a string?
    #  cat_age: int - age of the cat when they left in moons
    #  clan_age: int - age of the Clan when the cat left in moons

    # ------------------------- Rank changes and ceremonies -------------------------- #
    RankChange = "rank_change"
    # TODO implement RankChange class
    #  cat: Cat - which cat's rank is changing?
    #  rank_old: Rank
    #  rank_new: Rank
    #  ceremony: BaseEvent = None - an associated Ceremony event
    MentorChange = "mentor_change"
    # TODO implement MentorChange class
    #  apprentice: Cat - the apprentice
    #  mentor_old: Cat - which cat is losing an apprentice
    #  mentor_new: Cat - which cat is gaining an apprentice

    # TODO murder, injury, illness, scar, recovery, mate, breakup, war_start, war_battle, war_end
    # TODO how to handle moon_* visit - split into SC and DF visits?



class BaseEvent:
    """ A base class for events """

    cat_dict: dict # [cat code: RedCat object]
    text: str # unformatted version of what will be printed in the game's window
    moon: int # when the event happened
    before_gamestart_allowed: bool # can this event type happen in the Clan's pre-game history?
    tags: list[str]

    tile: tuple[int, int] # TODO this will be used when the tilemap is implemented

    def __init__(self, **kwargs):
        self.before_gamestart_allowed = False # can this event type happen in the Clan's pre-game history?
        self.tags = []
        self.tile = (-1, -1)

        self._parse_cat_dict(kwargs["cat_dict"])

        return

    def _parse_cat_dict(self, cat_dict: dict):
        """ Parse the given dictionary of involved cats. """
        self.cat_dict["main"] = cat_dict.pop("main")
        for cat_code in cat_dict:
            self.cat_dict[cat_code] = cat_dict[cat_code]
        return

    @property
    def main(self):
        return self.cat_dict["main"]



class LeadCeremony(BaseEvent):
    """ Event dataclass detailing how a Clan cat's leadership ceremony went. """

    df: bool = False # Was it a Dark Forest leadership ceremony?
    sc: bool = True # Was it a StarClan leadership ceremony?
    intro: Union[str, int] = "default" # index of the intro used in the leadership ceremony
    lives: list[dict] = field(default_factory=list) # each dictionary contains the index of the life, the cat who gave it, and the virtue given
    outro: Union[str, int] = "default"  # index of the outro used in the leadership ceremony



class BirthEvent(BaseEvent):
    """ Event dataclass detailing how a cat was created. """

    parents: dict = None # dictionary should specify who's giving birth and who isn't
    new_cats: list = field(default_factory=list) # the cats being born or created
    age_at_birth: int = 0 # if a cat was made as an adult, not actually born, this won't be 0




########################################################################################################################
# Methods
########################################################################################################################

def cast_to_event_type(to_cast) -> EventType:
    """ If possible, return an EventType object.

     :param to_cast: something to be cast to an EventType object
     :ptype: str, EventType, NoneType
     :return EventType: None returns Any; EventTypes return themselves; strings will be matched to EventType strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding EventType for to_cast
     :raises TypeError: if to_cast isn't a str, EventType, or NoneType object
     """
    if isinstance(to_cast, EventType):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() in ["general", "any"]:
            return EventType.Any
        if to_cast.casefold() in ["patrol"]:
            return EventType.Patrol
        if to_cast.casefold() in ["interaction", "relationship"]:
            return EventType.Interaction
        raise KeyError(f"Can't cast to EventType: {to_cast}")
    if to_cast is None:
        return EventType.Any
    else:
        raise TypeError(f"In order to cast to EventType, to_cast must be a string object, "
                        f"and EventType object, or None. However, type(to_cast) was {type(to_cast)}")


def generate_leadership_ceremony(new_leader) -> LeadCeremony:
    """ Generate a leadership ceremony event for a Clan leader.

    TODO
     - make sure the cat is logged as their clan's leader when this is generated

    :param new_leader: a Cat object who is the new leader of a Clan
    """
    # TODO Make sure the cat's history has been loaded, and reload it if it hasn't been
    # new_leader.history.check_load()

    # The text used will depend on whether the Clan's guide is from StarClan or the Dark Forest.
    guide_sc_b: bool = True
    if game.clan_obj.instructor.location == Location.StarClan:
        pass  # TODO use StarClan dictionary
    elif game.clan_obj.instructor.location == Location.DarkForest:
        guide_sc_b = False
        pass  # TODO use Dark Forest dictionary
    else:
        raise AttributeError(f"Clan guides should be from either StarClan or the Dark Forest, "
                             f"but {game.clan_obj}'s guide is in '{game.clan_obj.instructor.location}'")

    # ---------------------------------- INTROS ---------------------------------- #

    # TODO filter through all possible intros to get ones that are valid for new_leader

    # TODO pick a random intro

    # ---------------------------------- LIVES ----------------------------------- #

    # TODO filter through all possible lives to get ones that are valid for new_leader

    # TODO choose 9 random lives

    # TODO choose 9 different virtues, so each life has a unique one

    # TODO replace name codes (m_c, r_c, c_n)

    # TODO replace pronouns and Clan names

    # ---------------------------------- OUTROS ---------------------------------- #

    # TODO filter through all possible outros to get ones that are valid for new_leader

    # TODO pick a random outro

    # ---------------------------------- FORMAT ---------------------------------- #

    # TODO replace name codes (m_c, r_c, c_n)

    # TODO replace pronouns and Clan names

    # TODO create the LeadCeremony object and return it


########################################################################################################################
# Classes
########################################################################################################################

