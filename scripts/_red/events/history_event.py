# history_event.py - Class for events that are stored in a cat's history.

# -------------------------------------------------------------------------------- #
# ----------------------------------------

########################################################################################################################
# Imports
########################################################################################################################

from scripts._red.events.base_event import *
from scripts._red.config_manager import config
from definitions import Event, EventCategory, BirthType


########################################################################################################################
# Dataclasses
########################################################################################################################

class HistoryEvent(BaseEvent):
    """ Base class for events recorded in a cat's history. """

    moon: int  # when the event happened
    __repr__: dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.__repr__:
            raise ValueError(f"Missing a representation for {type(self)}!")
        return


class BirthEvent(HistoryEvent):
    """ Have you heard about the birds and the world generation?

    The main cat should be the one giving birth.
    """
    # TODO implement BirthEvent class.
    #   Include the cat giving birth, the other parent(s), all cats being born
    #   Add this event to the History of all cats involved

    parent_ids: list[int]
    new_cat_ids: list[int]

    age_at_birth: int = 0 # if a cat was made as an adult, not actually born, this won't be 0

    def __init__(self, birth_type: BirthType, **kwargs):
        """ Initiating cat creation...

        :param birth_type: member of an enum to indicate which kwargs are required.
        :param list[int] parent_ids: a list of cat IDs for the parents of the cats. The first female cat in the list
            is used as the cat giving birth. Required for pregnancies and foundlings.
        :param list
        """
        self.__repr__ = {EventType.Birth: {"type": birth_type}}
        super().__init__(**kwargs)

        if birth_type is BirthType.Pregnancy:
            self.pregnancy_moon_0()
            # Schedule the
            # game.add_to_future_events(self, moons: int, function: FunctionType, kwargs: dict, args: list)
            game.add_to_future_events(moons=1, function=self.pregnancy_moon_1, kwargs={}, args=[])
            game.add_to_future_events(moons=2, function=self.pregnancy_moon_2, kwargs={}, args=[])
            game.add_to_future_events(moons=3, function=self.pregnancy_birth, kwargs={}, args=[])
        if "parent_ids" in kwargs.keys():
            self.parent_ids = kwargs["parent_ids"]
        else:
            self.parent_ids = []


        for kwarg in kwargs:
            self.__repr__[kwarg] = kwargs[kwarg]
        return

    def pregnancy_moon_0(self):
        """ Called when a pregnancy begins."""
        # TODO pick the size of the litter
        # TODO pick fathers
        # TODO pick how many kits each father is fathering
        # TODO cat.health.birth_cooldown = config.cat_config.{mother/father}_birth_cooldown_moons
        return

    def pregnancy_moon_1(self):
        """ Called the moon after a cat becomes pregnant. """

    def pregnancy_moon_2(self):
        """ Called the moon before a cat gives birth. """
        # TODO check if the mother needs
        return

    def pregnancy_birth(self):
        """ Called when a cat gives birth. """
        # TODO create kittens
        return

class DeathEvent(HistoryEvent):
    """ Skill issue lol """
    # TODO implement DeathEvent class
    #   Include cause of death and murder details (whodunnit and whydunnit)

class ClanChangeEvent(HistoryEvent):
    """ When a cat moves from one Clan to another.

    Remember that outsiders are in their own Clan now, so exile is included here.

    Sometimes also involves a RankChangeEvent. """

    old_clan_name: str
    new_clan_name: str

class RankChangeEvent(HistoryEvent):
    """ Include role changes, promotions, retirements, etc. """
