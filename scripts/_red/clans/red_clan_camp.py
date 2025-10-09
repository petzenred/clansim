# red_clan_camp.py - Contains the Camp class.

########################################################################################################################
# Imports
########################################################################################################################

from dataclasses import dataclass, field

from resources._red.camps import CAMP_DEN_PLACEMENTS, CAMP_CAT_PLACEMENTS, CAMP_SHADING
from scripts._red.config_manager import config
from definitions import (
    Biome, CampKey,
)


########################################################################################################################
# Dataclasses
########################################################################################################################

@dataclass
class Camp:
    """ Contains all the info about a Clan's camp. """

    # TODO update cat_tracker

    biome: Biome
    camp_key: CampKey = CampKey.NoCamp
    freshkill_pile: dict = field(default_factory=dict)  # {age_of_freshkill: amount_of_freshkill}
    herb_stores: dict = field(default_factory=dict)
    freshkill_rots_at_age: int = config.prey_config.freshkill_rots_after_moons

    @property
    def den_positions(self):
        return CAMP_DEN_PLACEMENTS[self]

    @property
    def cat_positions(self):
        return CAMP_CAT_PLACEMENTS[self]

    @property
    def cat_shading(self):
        if self in CAMP_SHADING:
            return CAMP_SHADING[self]
        else:
            return None

    def add_freshkill(self, amount: float):
        """ Adds some freshkill to the freshkill pile. """
        if 0 not in self.freshkill_pile.keys():
            self.freshkill_pile[0] = amount
        else:
            self.freshkill_pile[0] = self.freshkill_pile[0] + amount
        return

    def freshkill_moon(self, amount_to_eat: float) -> bool:
        """ Tries to feed everyone and then removes rotten freshkill. """
        # eat as much food as the Clan wants, or as much as is available
        if self.eat_freshkill(amount_to_eat):
            # once the Clan is done eating, remove uneaten
            # freshkill that will rot by the end of the month
            oldest_freshkill_age: int = max(self.freshkill_pile.keys())
            while oldest_freshkill_age > 0:
                new_fk_age = oldest_freshkill_age + 1
                if new_fk_age >= self.freshkill_rots_at_age:
                    self.freshkill_pile[oldest_freshkill_age] = 0
                else:
                    self.freshkill_pile[new_fk_age] = self.freshkill_pile[oldest_freshkill_age]
                    self.freshkill_pile[oldest_freshkill_age] = 0
                oldest_freshkill_age -= 1
            self.freshkill_pile.pop(0)
            return True
        return False

    def eat_freshkill(self, amount: float) -> tuple[bool, float]:
        """ Attempt to eat some amount from the freshkill pile.

        :param float amount: How much food you are attempting to eat.
        :return bool: True if there was enough food; False otherwise.
        """
        while self.freshkill_pile and amount:
            amount = self._private_remove_freshkill(
                age=max(self.freshkill_pile.keys()),
                amount=amount)
        if self.freshkill_pile:
            return True, 0
        return False, amount

    def _private_remove_freshkill(self, age: int, amount: float) -> float:
        """ Attempt to eat some amount at a specific age from the freshkill pile.

        Updates self.freshkill_pile if amount <= self.freshkill_pile[age].

        :param int age: How old is the freshkill you're trying to remove
        :param float amount: How much freshkill you are attempting to remove
        :return float: amount - the food available of age moons
        """
        if amount < 0:
            raise ValueError(f"You can't remove a negative amount of food from the freshkill pile")
        if age in self.freshkill_pile.keys():
            if amount < self.freshkill_pile[age]:
                self.freshkill_pile[age] = self.freshkill_pile[age] - amount
                amount = 0
            else:
                amount -= self.freshkill_pile[age]
                self.freshkill_pile.pop(age)
        return amount