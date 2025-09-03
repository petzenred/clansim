# condition.py - Class for managing conditions that cats can have.
import random

# -------------------------------------------------------------------------------- #
# ----------------------------------------

########################################################################################################################
# Imports
########################################################################################################################

from definitions import (
    ConditionCategory, ConditionSeverity,
    cast_to_herb,
)
from resources._red.conditions import ILLNESSES, INJURIES, PERMANENT_CONDITIONS
# conditions.yaml - List of all the conditions cats can have.
# If you add new conditions, make sure to add their key to conditions.en.yaml otherwise they will not display.

########################################################################################################################
# Classes
########################################################################################################################

class Condition:
    """ A pregnancy, an illness, an injury, or a permanent condition. """


    # -------------------------------- Read from file -------------------------------- #
    name: str
    category: ConditionCategory
    severity: ConditionSeverity
    herbs: dict # which herb [Herb]: how many are used per moon [int]
    mortality_risk: dict # age [Age]: weight [int]
    medicine_mortality_risk: dict # age [Age]: weight [int]
    complication_risks: list[dict]

    # illnesses only
    infectiousness: int = None

    # non-permanent conditions only
    cause_permanent: list = None
    duration_moons: int = None
    medicine_duration_moons: int = None

    # permanent conditions only
    is_genetic: bool = False
    inheritance: dict = None
    moons_until: int = None

    # ------------------------------------- Init ------------------------------------- #

    def __init__(self,
                 name: str,
                 category: ConditionCategory,
                 severity: ConditionSeverity,
                 herbs: dict,
                 mortality_risk: dict,
                 complication_risks: list[dict],
                 **kwargs):
        self.name = name
        self.category = category
        self.severity = severity
        if herbs:
            self._parse_herbs(herbs)
        self.mortality_risk = mortality_risk
        if "medicine_mortality_risk" in kwargs:
            self.medicine_mortality_risk = kwargs["medicine_mortality_risk"]
        else:
            self.medicine_mortality_risk = self.mortality_risk
        self.complication_risks = complication_risks

        if "infectiousness" in kwargs:
            self.infectiousness = kwargs["infectiousness"]
        if "cause_permanent" in kwargs:
            self.cause_permanent = kwargs["cause_permanent"]
        if "duration_moons" in kwargs:
            self.duration_moons = kwargs["duration_moons"]
        if "medicine_duration_moons" in kwargs:
            self.medicine_duration_moons = kwargs["medicine_duration_moons"]
        if "is_genetic" in kwargs:
            self.is_genetic = kwargs["is_genetic"]
        if "inheritance" in kwargs:
            self.inheritance = kwargs["inheritance"]
        if "moons_until" in kwargs:
            self.moons_until = kwargs["moons_until"]

    def _parse_herbs(self, herbs: dict):
        """ Parse strings to Herb objects. """
        self.herbs = {}
        for amount_needed in herbs:
            herbs_needed = herbs[amount_needed]
            for herb in herbs_needed:
                self.herbs.update({cast_to_herb(herb): amount_needed})


########################################################################################################################
# Functions
########################################################################################################################

def get_condition(condition_name: str, is_genetic: bool = False) -> Condition:
    """ Get a condition object. """
    if condition_name in PERMANENT_CONDITIONS:
        return Condition(name=condition_name, is_genetic=is_genetic, **PERMANENT_CONDITIONS[condition_name])
    elif condition_name in ILLNESSES:
        return Condition(name=condition_name, is_genetic=is_genetic, **ILLNESSES[condition_name])
    elif condition_name in INJURIES:
        return Condition(name=condition_name, is_genetic=is_genetic, **INJURIES[condition_name])
    else:
        raise ValueError(f"Unknown condition: {condition_name}")


def get_random_permanent_condition(parent_conditions: list = None) -> Condition:
    """ Get a random permanent condition if a randomly generated cat has one. """
    population: list = []
    weights: list = []
    for c_name in PERMANENT_CONDITIONS:
        population.append(c_name)
        weight = PERMANENT_CONDITIONS[c_name]["inheritance"]["default_weight"]
        if parent_conditions and c_name in parent_conditions:
            weight += PERMANENT_CONDITIONS[c_name]["inheritance"]["per_parent_modifier"]
        weights.append(weight)
    return random.choices(population=population, weights=weights, k=1)[0]
