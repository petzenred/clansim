# healer_den.py - Objects related to healer's dens.

########################################################################################################################
# Imports
########################################################################################################################

from definitions import (
    Herb
)
from scripts._red.cats.red_condition import RedCondition


########################################################################################################################
# Classes
########################################################################################################################

class HealerDen:
    """ A class to keep track of everything related to the healer's den. """

    storage: dict = {} # [Herb: int]
    healer_ids: list[int] = []

    current_ailments: dict # RedCondition: int where the ints are the ids of cats with that ailment