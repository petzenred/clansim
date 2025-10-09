# general_utils.py - Utility functions used by scattered modules. Used to avoid circular imports.

# -------------------------------------------------------------------------------- #
# ----------------------------------------

########################################################################################################################
# Imports
########################################################################################################################

import random


########################################################################################################################
# Functions
########################################################################################################################

def one_in_num_chance(num: int, modifier: int = 0) -> bool:
    """ Return a bool with a 1 in num chance of being True.

    Specifically, the chance of getting true is: 0 < (random.randrange(num) - modifier)

    :param num: Return a boolean with a 1 in num chance of being True.
    :param modifier: If not 0, this will be
    """
    return not (0 < (random.randrange(num) - modifier))