# conditions.py -
# If you add new conditions, make sure to add their key to conditions.en.yaml otherwise they will not display.

########################################################################################################################
# Imports
########################################################################################################################

from definitions import ConditionCategory, ConditionSeverity, Herb


########################################################################################################################
# Constants
########################################################################################################################

ILLNESSES: dict = {
    "festering_wound": {
    "category": ConditionCategory.Illness,
    "duration_moons": 3,
    "herbs": {
    "1": [
    Herb.Marigold,
    Herb.Burdock,
    Herb.OakLeaf,
    Herb.Ragwort,
    Herb.JuniperBerry,
    Herb.Poppy,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "infectiousness": 0,
    "medicine_duration_moons": 2,
    "medicine_mortality_risk": {
    "adolescent": 5,
    "adult": 10,
    "kitten": 3,
    "newborn": 3,
    "senior": 3,
    "senior adult": 8,
    "young adult": 8
    },
    "mortality_risk": {
    "adolescent": 3,
    "adult": 5,
    "kitten": 1,
    "newborn": 1,
    "senior": 2,
    "senior adult": 5,
    "young adult": 3
    },
    "complication_risks": [],
    "severity": ConditionSeverity.Severe
    },
    "infected_wound": {
    "category": ConditionCategory.Illness,
    "duration_moons": 3,
    "herbs": {
    "1": [
    Herb.Marigold,
    Herb.Burdock,
    Herb.WildGarlic,
    Herb.Poppy
    ],
    "2": [],
    "3": []
    },
    "infectiousness": 0,
    "medicine_duration_moons": 2,
    "medicine_mortality_risk": {
    "adolescent": 13,
    "adult": 20,
    "kitten": 8,
    "newborn": 5,
    "senior": 13,
    "senior adult": 15,
    "young adult": 15
    },
    "mortality_risk": {
    "adolescent": 8,
    "adult": 10,
    "kitten": 3,
    "newborn": 3,
    "senior": 5,
    "senior adult": 8,
    "young adult": 8
    },
    "complication_risks": [
    {
    "chance": 10,
    "name": "festering_wound"
    }
    ],
    "severity": ConditionSeverity.Major
    },
    "carrionplace_disease": {
    "category": ConditionCategory.Illness,
    "duration_moons": 3,
    "herbs": {
    "1": [
    Herb.Marigold,
    Herb.Burdock,
    Herb.WildGarlic,
    Herb.Poppy
    ],
    "2": [],
    "3": []
    },
    "infectiousness": 0,
    "medicine_duration_moons": 2,
    "medicine_mortality_risk": {
    "adolescent": 3,
    "adult": 3,
    "kitten": 2,
    "newborn": 2,
    "senior": 2,
    "senior adult": 3,
    "young adult": 3
    },
    "mortality_risk": {
    "adolescent": 2,
    "adult": 2,
    "kitten": 1,
    "newborn": 1,
    "senior": 1,
    "senior adult": 2,
    "young adult": 2
    },
    "complication_risks": [],
    "severity": ConditionSeverity.Severe
    },
    "constant_nightmares": {
    "category": ConditionCategory.Illness,
    "duration_moons": 2,
    "herbs": {
    "1": [
    Herb.JuniperBerry,
    Herb.Thyme,
    Herb.Poppy
    ],
    "2": [],
    "3": []
    },
    "infectiousness": 0,
    "medicine_duration_moons": 1,
    "medicine_mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [],
    "severity": ConditionSeverity.Major
    },
    "diarrhea": {
    "category": ConditionCategory.Illness,
    "duration_moons": 2,
    "herbs": {
    "1": [
    Herb.Betony,
    Herb.Mullein,
    Herb.JuniperBerry,
    Herb.Mallow
    ],
    "2": [],
    "3": []
    },
    "infectiousness": 0,
    "medicine_duration_moons": 2,
    "medicine_mortality_risk": {
    "adolescent": 15,
    "adult": 45,
    "kitten": 10,
    "newborn": 10,
    "senior": 13,
    "senior adult": 30,
    "young adult": 30
    },
    "mortality_risk": {
    "adolescent": 8,
    "adult": 15,
    "kitten": 3,
    "newborn": 3,
    "senior": 5,
    "senior adult": 10,
    "young adult": 10
    },
    "complication_risks": [],
    "severity": ConditionSeverity.Major
    },
    "fleas": {
    "category": ConditionCategory.Illness,
    "duration_moons": 4,
    "herbs": {
    "1": [
    Herb.Plantain
    ],
    "2": [],
    "3": []
    },
    "infectiousness": 15,
    "medicine_duration_moons": 2,
    "medicine_mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [
    {
    "chance": 20,
    "name": "torn_pelt"
    }
    ],
    "severity": ConditionSeverity.Minor
    },
    "greencough": {
    "category": ConditionCategory.Illness,
    "duration_moons": 3,
    "herbs": {
    "1": [
    Herb.Catmint,
    Herb.Tansy,
    Herb.Mullein,
    Herb.Plantain,
    Herb.JuniperBerry,
    Herb.Poppy,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "infectiousness": 30,
    "medicine_duration_moons": 2,
    "medicine_mortality_risk": {
    "adolescent": 12,
    "adult": 25,
    "kitten": 7,
    "newborn": 7,
    "senior": 7,
    "senior adult": 20,
    "young adult": 20
    },
    "mortality_risk": {
    "adolescent": 8,
    "adult": 10,
    "kitten": 3,
    "newborn": 3,
    "senior": 3,
    "senior adult": 8,
    "young adult": 8
    },
    "complication_risks": [
    {
    "chance": 60,
    "name": "yellowcough"
    }
    ],
    "severity": ConditionSeverity.Severe
    },
    "grief_stricken": {
    "category": ConditionCategory.Illness,
    "duration_moons": 5,
    "herbs": {
    "1": [
    Herb.JuniperBerry,
    Herb.Thyme,
    Herb.Poppy
    ],
    "2": [],
    "3": []
    },
    "infectiousness": 0,
    "medicine_duration_moons": 3,
    "medicine_mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [
    {
    "chance": 100,
    "name": "lasting grief"
    },
    {
    "chance": 15,
    "name": "constant_nightmares"
    }
    ],
    "severity": ConditionSeverity.Major
    },
    "heat_exhaustion": {
    "category": ConditionCategory.Illness,
    "duration_moons": 2,
    "herbs": {
    "1": [
    Herb.JuniperBerry,
    Herb.Ragwort,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "infectiousness": 0,
    "medicine_duration_moons": 2,
    "medicine_mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [
    {
    "chance": 5,
    "name": "heat_stroke"
    }
    ],
    "severity": ConditionSeverity.Major
    },
    "heat_stroke": {
    "category": ConditionCategory.Illness,
    "duration_moons": 1,
    "herbs": {
    "1": [
    Herb.JuniperBerry,
    Herb.Ragwort,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "infectiousness": 0,
    "medicine_duration_moons": 1,
    "medicine_mortality_risk": {
    "adolescent": 10,
    "adult": 20,
    "kitten": 5,
    "newborn": 5,
    "senior": 10,
    "senior adult": 25,
    "young adult": 15
    },
    "mortality_risk": {
    "adolescent": 5,
    "adult": 8,
    "kitten": 2,
    "newborn": 2,
    "senior": 3,
    "senior adult": 8,
    "young adult": 5
    },
    "complication_risks": [],
    "severity": ConditionSeverity.Severe
    },
    "kittencough": {
    "category": ConditionCategory.Illness,
    "duration_moons": 3,
    "herbs": {
    "1": [
    Herb.Catmint,
    Herb.Tansy,
    Herb.Mullein,
    Herb.Plantain,
    Herb.JuniperBerry,
    Herb.Poppy,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "infectiousness": 15,
    "medicine_duration_moons": 2,
    "medicine_mortality_risk": {
    "adolescent": 60,
    "adult": 0,
    "kitten": 5,
    "newborn": 5,
    "senior": 10,
    "senior adult": 0,
    "young adult": 0
    },
    "mortality_risk": {
    "adolescent": 15,
    "adult": 0,
    "kitten": 2,
    "newborn": 2,
    "senior": 5,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [
    {
    "chance": 10,
    "name": "whitecough"
    }
    ],
    "severity": ConditionSeverity.Severe
    },
    "malnourished": {
    "category": ConditionCategory.Illness,
    "duration_moons": 100,
    "herbs": {
    "1": [
    Herb.Thyme
    ],
    "2": [],
    "3": []
    },
    "infectiousness": 0,
    "medicine_duration_moons": 100,
    "medicine_mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [],
    "severity": ConditionSeverity.Minor
    },
    "redcough": {
    "category": ConditionCategory.Illness,
    "duration_moons": 50,
    "herbs": {
    "1": [
    Herb.Lungwort,
    Herb.Mullein,
    Herb.Tansy,
    Herb.Plantain,
    Herb.JuniperBerry,
    Herb.Ragwort,
    Herb.Poppy,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "infectiousness": 0,
    "medicine_duration_moons": 40,
    "medicine_mortality_risk": {
    "adolescent": 3,
    "adult": 3,
    "kitten": 2,
    "newborn": 2,
    "senior": 2,
    "senior adult": 3,
    "young adult": 3
    },
    "mortality_risk": {
    "adolescent": 2,
    "adult": 2,
    "kitten": 1,
    "newborn": 1,
    "senior": 1,
    "senior adult": 2,
    "young adult": 2
    },
    "complication_risks": [],
    "severity": ConditionSeverity.Severe
    },
    "running_nose": {
    "category": ConditionCategory.Illness,
    "duration_moons": 3,
    "herbs": {
    "1": [
    Herb.Ragwort,
    Herb.JuniperBerry,
    Herb.Poppy
    ],
    "2": [],
    "3": []
    },
    "infectiousness": 0,
    "medicine_duration_moons": 2,
    "medicine_mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [
    {
    "chance": 15,
    "name": "whitecough"
    }
    ],
    "severity": ConditionSeverity.Minor
    },
    "seizure": {
    "category": ConditionCategory.Illness,
    "duration_moons": 1,
    "herbs": {
    "1": [
    Herb.JuniperBerry,
    Herb.Poppy,
    Herb.Thyme,
    Herb.Ragwort
    ],
    "2": [],
    "3": []
    },
    "infectiousness": 0,
    "medicine_duration_moons": 1,
    "medicine_mortality_risk": {
    "adolescent": 70,
    "adult": 100,
    "kitten": 50,
    "newborn": 30,
    "senior": 70,
    "senior adult": 100,
    "young adult": 100
    },
    "mortality_risk": {
    "adolescent": 10,
    "adult": 20,
    "kitten": 5,
    "newborn": 2,
    "senior": 5,
    "senior adult": 20,
    "young adult": 20
    },
    "complication_risks": [],
    "severity": ConditionSeverity.Severe
    },
    "starving": {
    "category": ConditionCategory.Illness,
    "duration_moons": 100,
    "herbs": {
    "1": [
    Herb.Thyme
    ],
    "2": [],
    "3": []
    },
    "infectiousness": 0,
    "medicine_duration_moons": 100,
    "medicine_mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [],
    "severity": ConditionSeverity.Severe
    },
    "stomachache": {
    "category": ConditionCategory.Illness,
    "duration_moons": 2,
    "herbs": {
    "1": [
    Herb.JuniperBerry,
    Herb.Mallow,
    Herb.Ragwort,
    Herb.Poppy
    ],
    "2": [],
    "3": []
    },
    "infectiousness": 0,
    "medicine_duration_moons": 1,
    "medicine_mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [
    {
    "chance": 8,
    "name": "diarrhea"
    }
    ],
    "severity": ConditionSeverity.Minor
    },
    "whitecough": {
    "category": ConditionCategory.Illness,
    "duration_moons": 3,
    "herbs": {
    "1": [
    Herb.Catmint,
    Herb.Plantain,
    Herb.Tansy,
    Herb.Mullein,
    Herb.JuniperBerry,
    Herb.Ragwort,
    Herb.Poppy,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "infectiousness": 30,
    "medicine_duration_moons": 2,
    "medicine_mortality_risk": {
    "adolescent": 60,
    "adult": 70,
    "kitten": 15,
    "newborn": 15,
    "senior": 15,
    "senior adult": 70,
    "young adult": 70
    },
    "mortality_risk": {
    "adolescent": 20,
    "adult": 60,
    "kitten": 10,
    "newborn": 10,
    "senior": 10,
    "senior adult": 50,
    "young adult": 60
    },
    "complication_risks": [
    {
    "chance": 18,
    "name": "greencough"
    }
    ],
    "severity": ConditionSeverity.Major
    },
    "yellowcough": {
    "category": ConditionCategory.Illness,
    "duration_moons": 3,
    "herbs": {
    "1": [
    Herb.Lungwort
    ],
    "2": [],
    "3": []
    },
    "infectiousness": 30,
    "medicine_duration_moons": 3,
    "medicine_mortality_risk": {
    "adolescent": 10,
    "adult": 15,
    "kitten": 5,
    "newborn": 5,
    "senior": 5,
    "senior adult": 15,
    "young adult": 15
    },
    "mortality_risk": {
    "adolescent": 3,
    "adult": 5,
    "kitten": 2,
    "newborn": 2,
    "senior": 3,
    "senior adult": 5,
    "young adult": 5
    },
    "complication_risks": [
    {
    "chance": 80,
    "name": "redcough"
    }
    ],
    "severity": ConditionSeverity.Major
    },
}

INJURIES: dict = {
    "beak_bite": {
    "category": ConditionCategory.Injury,
    "also_got": [
    "torn_pelt",
    "blood_loss"
    ],
    "cause_permanent": [],
    "duration_moons": 2,
    "herbs": {
    "1": [
    Herb.Cobweb,
    Herb.Goldenrod,
    Herb.Marigold,
    Herb.OakLeaf,
    Herb.WildGarlic,
    Herb.Tansy,
    Herb.Poppy,
    Herb.Ragwort,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 45,
    "adult": 60,
    "kitten": 10,
    "newborn": 10,
    "senior": 15,
    "senior adult": 60,
    "young adult": 60
    },
    "complication_risks": [
    {
    "chance": 5,
    "name": "infected_wound"
    }
    ],
    "severity": ConditionSeverity.Major
    },
    "bee_sting": {
    "category": ConditionCategory.Injury,
    "also_got": [],
    "cause_permanent": [],
    "duration_moons": 2,
    "herbs": {
    "1": [
    Herb.BlackberryLeaf,
    Herb.Dandelion,
    Herb.Poppy
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 30,
    "adult": 50,
    "kitten": 20,
    "newborn": 10,
    "senior": 30,
    "senior adult": 50,
    "young adult": 50
    },
    "complication_risks": [],
    "severity": ConditionSeverity.Minor
    },
    "bite_wound": {
    "category": ConditionCategory.Injury,
    "also_got": [
    "torn_pelt",
    "blood_loss"
    ],
    "cause_permanent": [],
    "duration_moons": 3,
    "herbs": {
    "1": [
    Herb.Cobweb,
    Herb.Goldenrod,
    Herb.Marigold,
    Herb.OakLeaf,
    Herb.WildGarlic,
    Herb.Tansy,
    Herb.Poppy,
    Herb.Ragwort,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 2,
    "mortality_risk": {
    "adolescent": 45,
    "adult": 60,
    "kitten": 10,
    "newborn": 10,
    "senior": 15,
    "senior adult": 60,
    "young adult": 60
    },
    "complication_risks": [
    {
    "chance": 5,
    "name": "infected_wound"
    }
    ],
    "severity": ConditionSeverity.Major
    },
    "blood_loss": {
    "category": ConditionCategory.Injury,
    "also_got": [
    "shock"
    ],
    "cause_permanent": [],
    "duration_moons": 1,
    "herbs": {
    "1": [
    Herb.Cobweb,
    Herb.Horsetail,
    Herb.Marigold,
    Herb.Ragwort,
    Herb.JuniperBerry,
    Herb.Moss,
    Herb.Poppy
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 10,
    "adult": 25,
    "kitten": 5,
    "newborn": 5,
    "senior": 15,
    "senior adult": 25,
    "young adult": 20
    },
    "complication_risks": [],
    "severity": ConditionSeverity.Minor
    },
    "broken_back": {
    "category": ConditionCategory.Injury,
    "also_got": [],
    "cause_permanent": [
    "paralyzed"
    ],
    "duration_moons": 8,
    "herbs": {
    "1": [
    Herb.JuniperBerry,
    Herb.Ragwort,
    Herb.Poppy
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 6,
    "mortality_risk": {
    "adolescent": 25,
    "adult": 30,
    "kitten": 5,
    "newborn": 3,
    "senior": 10,
    "senior adult": 25,
    "young adult": 30
    },
    "complication_risks": [
    {
    "chance": 10,
    "name": "infected_wound"
    }
    ],
    "severity": ConditionSeverity.Severe
    },
    "broken_bone": {
    "category": ConditionCategory.Injury,
    "also_got": [
    "torn_pelt",
    "mangled_leg",
    "blood_loss",
    "scrapes",
    "bruises"
    ],
    "cause_permanent": [
    "weak_leg",
    "twisted_leg"
    ],
    "duration_moons": 5,
    "herbs": {
    "1": [
    Herb.Cobweb,
    Herb.Marigold,
    Herb.OakLeaf,
    Herb.WildGarlic,
    Herb.JuniperBerry,
    Herb.Ragwort,
    Herb.Poppy,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 3,
    "mortality_risk": {
    "adolescent": 45,
    "adult": 60,
    "kitten": 10,
    "newborn": 10,
    "senior": 15,
    "senior adult": 60,
    "young adult": 60
    },
    "complication_risks": [
    {
    "chance": 5,
    "name": "infected_wound"
    }
    ],
    "severity": ConditionSeverity.Severe
    },
    "broken_jaw": {
    "category": ConditionCategory.Injury,
    "also_got": [
    "blood_loss",
    "scrapes",
    "bruises"
    ],
    "cause_permanent": [
    "crooked_jaw"
    ],
    "duration_moons": 4,
    "herbs": {
    "1": [
    Herb.Cobweb,
    Herb.Marigold,
    Herb.OakLeaf,
    Herb.WildGarlic,
    Herb.JuniperBerry,
    Herb.Ragwort,
    Herb.Poppy,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 3,
    "mortality_risk": {
    "adolescent": 35,
    "adult": 50,
    "kitten": 10,
    "newborn": 10,
    "senior": 10,
    "senior adult": 50,
    "young adult": 50
    },
    "complication_risks": [
    {
    "chance": 5,
    "name": "infected_wound"
    }
    ],
    "severity": ConditionSeverity.Severe
    },
    "bruises": {
    "category": ConditionCategory.Injury,
    "also_got": [],
    "cause_permanent": [],
    "duration_moons": 1,
    "herbs": {
    "1": [],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [],
    "severity": ConditionSeverity.Minor
    },
    "burn": {
    "category": ConditionCategory.Injury,
    "also_got": [],
    "cause_permanent": [],
    "duration_moons": 2,
    "herbs": {
    "1": [
    Herb.Cobweb,
    Herb.Marigold,
    Herb.WildGarlic,
    Herb.OakLeaf,
    Herb.Goldenrod,
    Herb.JuniperBerry,
    Herb.Ragwort,
    Herb.Poppy,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 2,
    "mortality_risk": {
    "adolescent": 30,
    "adult": 60,
    "kitten": 10,
    "newborn": 10,
    "senior": 30,
    "senior adult": 50,
    "young adult": 50
    },
    "complication_risks": [
    {
    "chance": 25,
    "name": "infected_wound"
    }
    ],
    "severity": ConditionSeverity.Major
    },
    "cat_bite": {
    "category": ConditionCategory.Injury,
    "also_got": [
    "torn_pelt",
    "blood_loss"
    ],
    "cause_permanent": [],
    "duration_moons": 2,
    "herbs": {
    "1": [
    Herb.Cobweb,
    Herb.Goldenrod,
    Herb.Marigold,
    Herb.OakLeaf,
    Herb.WildGarlic,
    Herb.Tansy,
    Herb.Poppy,
    Herb.Ragwort,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 2,
    "mortality_risk": {
    "adolescent": 45,
    "adult": 60,
    "kitten": 10,
    "newborn": 10,
    "senior": 15,
    "senior adult": 60,
    "young adult": 60
    },
    "complication_risks": [
    {
    "chance": 5,
    "name": "infected_wound"
    }
    ],
    "severity": ConditionSeverity.Major
    },
    "claw_wound": {
    "category": ConditionCategory.Injury,
    "also_got": [
    "torn_pelt",
    "torn_ear",
    "blood_loss"
    ],
    "cause_permanent": [],
    "duration_moons": 3,
    "herbs": {
    "1": [
    Herb.Cobweb,
    Herb.Goldenrod,
    Herb.Marigold,
    Herb.OakLeaf,
    Herb.WildGarlic,
    Herb.Tansy,
    Herb.Poppy,
    Herb.Ragwort,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 2,
    "mortality_risk": {
    "adolescent": 40,
    "adult": 50,
    "kitten": 5,
    "newborn": 5,
    "senior": 10,
    "senior adult": 50,
    "young adult": 50
    },
    "complication_risks": [
    {
    "chance": 5,
    "name": "infected_wound"
    }
    ],
    "severity": ConditionSeverity.Major
    },
    "cracked_pads": {
    "category": ConditionCategory.Injury,
    "also_got": [],
    "cause_permanent": [],
    "duration_moons": 1,
    "herbs": {
    "1": [
    Herb.OakLeaf,
    Herb.Marigold,
    Herb.WildGarlic,
    Herb.Poppy
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [
    {
    "chance": 20,
    "name": "infected_wound"
    }
    ],
    "severity": ConditionSeverity.Minor
    },
    "damaged_eyes": {
    "category": ConditionCategory.Injury,
    "also_got": [],
    "cause_permanent": [
    "blind",
    "one_bad_eye",
    "failing_eyesight"
    ],
    "duration_moons": 6,
    "herbs": {
    "1": [
    Herb.Celandine,
    Herb.Cobweb,
    Herb.Goldenrod,
    Herb.Marigold,
    Herb.OakLeaf,
    Herb.WildGarlic,
    Herb.JuniperBerry,
    Herb.Ragwort,
    Herb.Poppy,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 4,
    "mortality_risk": {
    "adolescent": 50,
    "adult": 70,
    "kitten": 30,
    "newborn": 30,
    "senior": 50,
    "senior adult": 70,
    "young adult": 70
    },
    "complication_risks": [
    {
    "chance": 4,
    "name": "infected_wound"
    }
    ],
    "severity": ConditionSeverity.Major
    },
    "dehydrated": {
    "also_got": [
    "heat_exhaustion"
    ],
    "category": ConditionCategory.Injury,
    "cause_permanent": [],
    "duration_moons": 1,
    "herbs": {
    "1": [
    Herb.Ragwort,
    Herb.JuniperBerry,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 30,
    "adult": 80,
    "kitten": 10,
    "newborn": 10,
    "senior": 20,
    "senior adult": 50,
    "young adult": 50
    },
    "complication_risks": [
    {
    "chance": 10,
    "name": "heat_exhaustion"
    }
    ],
    "severity": ConditionSeverity.Major
    },
    "dislocated_joint": {
    "also_got": [
    "bruises",
    "sore",
    "joint_pain"
    ],
    "category": ConditionCategory.Injury,
    "cause_permanent": [
    "constant_joint_pain"
    ],
    "duration_moons": 2,
    "herbs": {
    "1": [
    Herb.Marigold,
    Herb.Ragwort,
    Herb.Daisy,
    Herb.Poppy
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [],
    "severity": ConditionSeverity.Major
    },
    "frostbite": {
    "also_got": [],
    "cause_permanent": [
    "lost_a_leg",
    "lost_their_tail"
    ],
    "category": ConditionCategory.Injury,
    "duration_moons": 2,
    "herbs": {
    "1": [
    Herb.JuniperBerry,
    Herb.Ragwort,
    Herb.Poppy,
    Herb.Moss,
    Herb.Dandelion
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 2,
    "mortality_risk": {
    "adolescent": 20,
    "adult": 30,
    "kitten": 10,
    "newborn": 10,
    "senior": 10,
    "senior adult": 20,
    "young adult": 25
    },
    "complication_risks": [
    {
    "chance": 4,
    "name": "running_nose"
    }
    ],
    "severity": ConditionSeverity.Major
    },
    "head_damage": {
    "also_got": [],
    "category": ConditionCategory.Injury,
    "cause_permanent": [
    "failing_eyesight",
    "one_bad_eye",
    "blind",
    "constantly_dizzy",
    "partial_hearing_loss",
    "persistent_headaches"
    ],
    "duration_moons": 5,
    "herbs": {
    "1": [
    Herb.JuniperBerry,
    Herb.Ragwort,
    Herb.Thyme
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 2,
    "mortality_risk": {
    "adolescent": 30,
    "adult": 50,
    "kitten": 15,
    "newborn": 20,
    "senior": 20,
    "senior adult": 40,
    "young adult": 40
    },
    "complication_risks": [
    {
    "chance": 20,
    "name": "headache"
    },
    {
    "chance": 20,
    "name": "severe_headache"
    }
    ],
    "severity": ConditionSeverity.Major
    },
    "headache": {
    "also_got": [],
    "category": ConditionCategory.Injury,
    "cause_permanent": [],
    "duration_moons": 1,
    "herbs": {
    "1": [
    Herb.Poppy,
    Herb.JuniperBerry
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [],
    "severity": ConditionSeverity.Minor
    },
    "joint_pain": {
    "also_got": [],
    "category": ConditionCategory.Injury,
    "cause_permanent": [],
    "duration_moons": 2,
    "herbs": {
    "1": [
    Herb.Marigold,
    Herb.Ragwort,
    Herb.Daisy,
    Herb.Poppy
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 2,
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [],
    "severity": ConditionSeverity.Minor
    },
    "lingering_shock": {
    "also_got": [],
    "category": ConditionCategory.Injury,
    "cause_permanent": [
    "recurring_shock"
    ],
    "duration_moons": 12,
    "herbs": {
    "1": [
    Herb.Thyme,
    Herb.JuniperBerry,
    Herb.Ragwort,
    Herb.Poppy
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 8,
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [],
    "severity": ConditionSeverity.Major
    },
    "mangled_leg": {
    "also_got": [
    "torn_pelt",
    "broken_bone",
    "dislocated_joint",
    "blood_loss",
    "scrapes",
    "bruises"
    ],
    "category": ConditionCategory.Injury,
    "cause_permanent": [
    "lost_a_leg",
    "weak_leg",
    "twisted_leg"
    ],
    "duration_moons": 3,
    "herbs": {
    "1": [
    Herb.Cobweb,
    Herb.Goldenrod,
    Herb.Marigold,
    Herb.WildGarlic,
    Herb.OakLeaf,
    Herb.Tansy,
    Herb.Poppy,
    Herb.Ragwort,
    Herb.JuniperBerry,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 3,
    "mortality_risk": {
    "adolescent": 50,
    "adult": 60,
    "kitten": 15,
    "newborn": 15,
    "senior": 15,
    "senior adult": 60,
    "young adult": 60
    },
    "complication_risks": [
    {
    "chance": 5,
    "name": "infected_wound"
    }
    ],
    "severity": ConditionSeverity.Severe
    },
    "mangled_tail": {
    "also_got": [
    "torn_pelt",
    "blood_loss"
    ],
    "category": ConditionCategory.Injury,
    "cause_permanent": [
    "lost_their_tail"
    ],
    "duration_moons": 3,
    "herbs": {
    "1": [
    Herb.Cobweb,
    Herb.Goldenrod,
    Herb.Marigold,
    Herb.WildGarlic,
    Herb.OakLeaf,
    Herb.Tansy,
    Herb.Poppy,
    Herb.Ragwort,
    Herb.JuniperBerry,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 3,
    "mortality_risk": {
    "adolescent": 50,
    "adult": 60,
    "kitten": 15,
    "newborn": 15,
    "senior": 15,
    "senior adult": 60,
    "young adult": 60
    },
    "complication_risks": [
    {
    "chance": 5,
    "name": "infected_wound"
    }
    ],
    "severity": ConditionSeverity.Severe
    },
    "phantom_pain": {
    "also_got": [],
    "category": ConditionCategory.Injury,
    "cause_permanent": [],
    "duration_moons": 2,
    "herbs": {
    "1": [
    Herb.Dandelion,
    Herb.Poppy,
    Herb.RaspberryLeaf
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [],
    "severity": ConditionSeverity.Major
    },
    "poisoned": {
    "also_got": [
    "shock"
    ],
    "category": ConditionCategory.Injury,
    "cause_permanent": [],
    "duration_moons": 2,
    "herbs": {
    "1": [
    Herb.Dandelion,
    Herb.Tansy,
    Herb.JuniperBerry,
    Herb.Ragwort,
    Herb.Poppy
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 15,
    "adult": 30,
    "kitten": 5,
    "newborn": 10,
    "senior": 15,
    "senior adult": 20,
    "young adult": 20
    },
    "complication_risks": [
    {
    "chance": 10,
    "name": "redcough"
    }
    ],
    "severity": ConditionSeverity.Major
    },
    "pregnant": {
    "also_got": [],
    "category": ConditionCategory.Injury,
    "cause_permanent": [],
    "duration_moons": 2,
    "herbs": {
    "1": [],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 3,
    "mortality_risk": {
    "adolescent": 0,
    "adult": 40,
    "kitten": 0,
    "senior": 20,
    "senior adult": 30,
    "young adult": 40
    },
    "complication_risks": [],
    "severity": ConditionSeverity.Major
    },
    "quilled_by_a_porcupine": {
    "also_got": [
    "torn_pelt"
    ],
    "category": ConditionCategory.Injury,
    "cause_permanent": [],
    "duration_moons": 2,
    "herbs": {
    "1": [
    Herb.Cobweb,
    Herb.Goldenrod,
    Herb.Marigold,
    Herb.OakLeaf,
    Herb.WildGarlic,
    Herb.JuniperBerry,
    Herb.Ragwort,
    Herb.Poppy,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 40,
    "adult": 60,
    "kitten": 20,
    "newborn": 10,
    "senior": 30,
    "senior adult": 50,
    "young adult": 50
    },
    "complication_risks": [
    {
    "chance": 5,
    "name": "infected_wound"
    }
    ],
    "severity": ConditionSeverity.Minor
    },
    "rat_bite": {
    "also_got": [
    "torn_pelt"
    ],
    "category": ConditionCategory.Injury,
    "cause_permanent": [],
    "duration_moons": 2,
    "herbs": {
    "1": [
    Herb.WildGarlic,
    Herb.Burdock,
    Herb.Tansy,
    Herb.Cobweb,
    Herb.Marigold,
    Herb.OakLeaf,
    Herb.Goldenrod,
    Herb.JuniperBerry,
    Herb.Poppy,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 45,
    "adult": 60,
    "kitten": 10,
    "newborn": 10,
    "senior": 15,
    "senior adult": 60,
    "young adult": 60
    },
    "complication_risks": [
    {
    "chance": 5,
    "name": "infected_wound"
    },
    {
    "chance": 5,
    "name": "festering_wound"
    }
    ],
    "severity": ConditionSeverity.Major
    },
    "recovering_from_birth": {
    "also_got": [
    "blood_loss"
    ],
    "category": ConditionCategory.Injury,
    "cause_permanent": [],
    "duration_moons": 3,
    "herbs": {
    "1": [
    Herb.OakLeaf,
    Herb.JuniperBerry,
    Herb.Ragwort,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 5,
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [
    {
    "chance": 15,
    "name": "infected_wound"
    }
    ],
    "severity": ConditionSeverity.Major
    },
    "scrapes": {
    "also_got": [],
    "category": ConditionCategory.Injury,
    "cause_permanent": [],
    "duration_moons": 1,
    "herbs": {
    "1": [
    Herb.Cobweb,
    Herb.Marigold,
    Herb.OakLeaf,
    Herb.WildGarlic
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [
    {
    "chance": 30,
    "name": "infected_wound"
    }
    ],
    "severity": ConditionSeverity.Minor
    },
    "severe_burn": {
    "also_got": [],
    "category": ConditionCategory.Injury,
    "cause_permanent": [
    "lost_their_tail",
    "lost_a_leg"
    ],
    "duration_moons": 4,
    "herbs": {
    "1": [
    Herb.Cobweb,
    Herb.Marigold,
    Herb.WildGarlic,
    Herb.OakLeaf,
    Herb.Goldenrod,
    Herb.JuniperBerry,
    Herb.Ragwort,
    Herb.Poppy,
    Herb.Moss
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 3,
    "mortality_risk": {
    "adolescent": 10,
    "adult": 30,
    "kitten": 5,
    "newborn": 5,
    "senior": 10,
    "senior adult": 30,
    "young adult": 30
    },
    "complication_risks": [
    {
    "chance": 15,
    "name": "infected_wound"
    }
    ],
    "severity": ConditionSeverity.Severe
    },
    "severe_headache": {
    "also_got": [],
    "category": ConditionCategory.Injury,
    "cause_permanent": [],
    "duration_moons": 1,
    "herbs": {
    "1": [
    Herb.Poppy,
    Herb.JuniperBerry
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [],
    "severity": ConditionSeverity.Major
    },
    "shivering": {
    "also_got": [
    "frostbite"
    ],
    "category": ConditionCategory.Injury,
    "cause_permanent": [],
    "duration_moons": 2,
    "herbs": {
    "1": [
    Herb.JuniperBerry,
    Herb.Ragwort,
    Herb.Tansy
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 30,
    "adult": 80,
    "kitten": 10,
    "newborn": 10,
    "senior": 20,
    "senior adult": 50,
    "young adult": 50
    },
    "complication_risks": [
    {
    "chance": 5,
    "name": "frostbite"
    }
    ],
    "severity": ConditionSeverity.Minor
    },
    "shock": {
    "also_got": [],
    "category": ConditionCategory.Injury,
    "cause_permanent": [],
    "duration_moons": 1,
    "herbs": {
    "1": [
    Herb.Thyme,
    Herb.JuniperBerry,
    Herb.Ragwort,
    Herb.Poppy
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 15,
    "adult": 30,
    "kitten": 8,
    "newborn": 10,
    "senior": 15,
    "senior adult": 30,
    "young adult": 30
    },
    "complication_risks": [
    {
    "chance": 15,
    "name": "lingering_shock"
    }
    ],
    "severity": ConditionSeverity.Major
    },
    "small_cut": {
    "also_got": [],
    "category": ConditionCategory.Injury,
    "cause_permanent": [],
    "duration_moons": 1,
    "herbs": {
    "1": [
    Herb.Marigold,
    Herb.OakLeaf,
    Herb.WildGarlic
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [
    {
    "chance": 40,
    "name": "infected_wound"
    }
    ],
    "severity": ConditionSeverity.Minor
    },
    "snake_bite": {
    "also_got": [
    "poisoned"
    ],
    "category": ConditionCategory.Injury,
    "cause_permanent": [],
    "duration_moons": 2,
    "herbs": {
    "1": [
    Herb.Tansy,
    Herb.Marigold,
    Herb.OakLeaf,
    Herb.Goldenrod,
    Herb.WildGarlic,
    Herb.JuniperBerry,
    Herb.Ragwort,
    Herb.Poppy
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 45,
    "adult": 60,
    "kitten": 10,
    "newborn": 10,
    "senior": 15,
    "senior adult": 60,
    "young adult": 60
    },
    "complication_risks": [
    {
    "chance": 5,
    "name": "infected_wound"
    }
    ],
    "severity": ConditionSeverity.Major
    },
    "sore": {
    "also_got": [],
    "category": ConditionCategory.Injury,
    "cause_permanent": [],
    "duration_moons": 1,
    "herbs": {
    "1": [
    Herb.Daisy,
    Herb.Dandelion,
    Herb.Marigold,
    Herb.Ragwort,
    Herb.Poppy
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [],
    "severity": ConditionSeverity.Minor
    },
    "sprain": {
    "also_got": [],
    "category": ConditionCategory.Injury,
    "cause_permanent": [],
    "duration_moons": 2,
    "herbs": {
    "1": [
    Herb.ElderLeaf,
    Herb.Dandelion,
    Herb.Poppy
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [],
    "severity": ConditionSeverity.Major
    },
    "tick_bites": {
    "also_got": [],
    "category": ConditionCategory.Injury,
    "cause_permanent": [],
    "duration_moons": 2,
    "herbs": {
    "1": [
    Herb.Moss,
    Herb.Plantain
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [
    {
    "chance": 40,
    "name": "infected_wound"
    }
    ],
    "severity": ConditionSeverity.Minor
    },
    "torn_ear": {
    "also_got": [],
    "category": ConditionCategory.Injury,
    "cause_permanent": [
    "partial_hearing_loss"
    ],
    "duration_moons": 1,
    "herbs": {
    "1": [
    Herb.Cobweb,
    Herb.Goldenrod,
    Herb.Marigold,
    Herb.OakLeaf,
    Herb.WildGarlic
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [
    {
    "chance": 25,
    "name": "infected_wound"
    }
    ],
    "severity": ConditionSeverity.Minor
    },
    "torn_pelt": {
    "also_got": [],
    "category": ConditionCategory.Injury,
    "cause_permanent": [],
    "duration_moons": 1,
    "herbs": {
    "1": [
    Herb.Cobweb,
    Herb.Goldenrod,
    Herb.Marigold,
    Herb.OakLeaf,
    Herb.WildGarlic,
    Herb.RaspberryLeaf
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 1,
    "mortality_risk": {
    "adolescent": 0,
    "adult": 0,
    "kitten": 0,
    "newborn": 0,
    "senior": 0,
    "senior adult": 0,
    "young adult": 0
    },
    "complication_risks": [
    {
    "chance": 25,
    "name": "infected_wound"
    }
    ],
    "severity": ConditionSeverity.Minor
    },
    "water_in_their_lungs": {
    "also_got": [],
    "category": ConditionCategory.Injury,
    "cause_permanent": [
    "raspy_lungs"
    ],
    "duration_moons": 3,
    "herbs": {
    "1": [
    Herb.JuniperBerry,
    Herb.Betony,
    Herb.Mullein,
    Herb.Tansy,
    Herb.Plantain,
    Herb.Ragwort
    ],
    "2": [],
    "3": []
    },
    "medicine_duration_moons": 2,
    "mortality_risk": {
    "adolescent": 50,
    "adult": 60,
    "kitten": 15,
    "newborn": 10,
    "senior": 30,
    "senior adult": 60,
    "young adult": 60
    },
    "complication_risks": [
    {
    "chance": 10,
    "name": "running_nose"
    },
    {
    "chance": 20,
    "name": "whitecough"
    }
    ],
    "severity": ConditionSeverity.Major
    },
}

PERMANENT_CONDITIONS: dict = {
    "allergies": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 500,
            "default_weight": 30
        },
        "herbs": {
            "1": [],
            "2": [],
            "3": []
        },
        "moons_until": 2,
        "mortality_risk": {
            "adolescent": 0,
            "adult": 0,
            "kitten": 0,
            "newborn": 0,
            "senior": 0,
            "senior adult": 0,
            "young adult": 0
        },
        "complication_risks": [
            {
            "chance": 20,
            "name": "running_nose"
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    "blind": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 50,
            "default_weight": 20
        },
        "herbs": {
            "1": [],
            "2": [],
            "3": []
        },
        "moons_until": 1,
        "mortality_risk": {
            "adolescent": 0,
            "adult": 0,
            "kitten": 0,
            "newborn": 0,
            "senior": 0,
            "senior adult": 0,
            "young adult": 0
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Major
    },
    "born_without_a_leg": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 10,
            "default_weight": 3
        },
        "herbs": {
            "1": [],
            "2": [],
            "3": []
        },
        "moons_until": 0,
        "mortality_risk": {
            "adolescent": 0,
            "adult": 0,
            "kitten": 0,
            "newborn": 0,
            "senior": 0,
            "senior adult": 0,
            "young adult": 0
        },
        "complication_risks": [
            {
            "chance": 20,
            "name": "sore"
            },
            {
            "chance": 40,
            "name": "joint_pain"
            }
        ],
        "severity": ConditionSeverity.Major
    },
    "born_without_a_tail": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 30,
            "default_weight": 9
        },
        "herbs": {
            "1": [],
            "2": [],
            "3": []
        },
        "moons_until": 0,
        "mortality_risk": {
            "adolescent": 0,
            "adult": 0,
            "kitten": 0,
            "newborn": 0,
            "senior": 0,
            "senior adult": 0,
            "young adult": 0
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Minor
    },
    "constant_joint_pain": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 10,
            "default_weight": 25
        },
        "herbs": {
            "1": [
                Herb.Daisy,
                Herb.JuniperBerry,
                Herb.Marigold,
                Herb.Ragwort
            ],
            "2": [],
            "3": []
        },
        "moons_until": 2,
        "mortality_risk": {
            "adolescent": 0,
            "adult": 0,
            "kitten": 0,
            "newborn": 0,
            "senior": 0,
            "senior adult": 0,
            "young adult": 0
        },
        "complication_risks": [
            {
                "chance": 10,
                "name": "joint_pain"
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    "constantly_dizzy": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 0,
            "default_weight": 0
        },
        "herbs": {
            "1": [],
            "2": [],
            "3": []
        },
        "moons_until": 0,
        "mortality_risk": {
            "adolescent": 0,
            "adult": 0,
            "kitten": 0,
            "newborn": 0,
            "senior": 0,
            "senior adult": 0,
            "young adult": 0
        },
        "complication_risks": [
            {
                "chance": 20,
                "name": "headache"
            }
        ],
        "severity": ConditionSeverity.Major
    },
    "crooked_jaw": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 0,
            "default_weight": 0
        },
        "herbs": {
            "1": [],
            "2": [],
            "3": []
        },
        "moons_until": 0,
        "mortality_risk": {
            "adolescent": 0,
            "adult": 0,
            "kitten": 0,
            "newborn": 0,
            "senior": 0,
            "senior adult": 0,
            "young adult": 0
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Major
    },
    "deaf": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 50,
            "default_weight": 20
        },
        "herbs": {
            "1": [],
            "2": [],
            "3": []
        },
        "moons_until": 1,
        "mortality_risk": {
            "adolescent": 0,
            "adult": 0,
            "kitten": 0,
            "newborn": 0,
            "senior": 0,
            "senior adult": 0,
            "young adult": 0
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Major
    },
    "failing_eyesight": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 50,
            "default_weight": 20
        },
        "herbs": {
            "1": [],
            "2": [],
            "3": []
        },
        "moons_until": 3,
        "mortality_risk": {
            "adolescent": 0,
            "adult": 0,
            "kitten": 0,
            "newborn": 0,
            "senior": 0,
            "senior adult": 0,
            "young adult": 0
        },
        "complication_risks": [
            {
                "chance": 50,
                "name": "blind"
            }
        ],
        "severity": ConditionSeverity.Major
    },
    "lasting grief": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 0,
            "default_weight": 0
        },
        "herbs": {
            "1": [
                Herb.Thyme,
                Herb.JuniperBerry,
                Herb.Poppy
            ],
            "2": [],
            "3": []
        },
        "moons_until": 0,
        "mortality_risk": {
            "adolescent": 0,
            "adult": 0,
            "kitten": 0,
            "newborn": 0,
            "senior": 0,
            "senior adult": 0,
            "young adult": 0
        },
        "complication_risks": [
            {
                "chance": 50,
                "name": "grief_stricken"
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    "lost_a_leg": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 0,
            "default_weight": 0
        },
        "herbs": {
            "1": [
                Herb.Daisy,
                Herb.JuniperBerry,
                Herb.Marigold,
                Herb.Ragwort
            ],
            "2": [],
            "3": []
        },
        "moons_until": 0,
        "mortality_risk": {
            "adolescent": 0,
            "adult": 0,
            "kitten": 0,
            "newborn": 0,
            "senior": 0,
            "senior adult": 0,
            "young adult": 0
        },
        "complication_risks": [
            {
                "chance": 70,
                "name": "infected_wound"
            },
            {
                "chance": 20,
                "name": "phantom_pain"
            },
            {
                "chance": 20,
                "name": "sore"
            }
        ],
        "severity": ConditionSeverity.Major
    },
    "lost_their_tail": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 0,
            "default_weight": 0
        },
        "herbs": {
            "1": [
                Herb.JuniperBerry,
                Herb.Ragwort
            ],
            "2": [],
            "3": []
        },
        "moons_until": 0,
        "mortality_risk": {
            "adolescent": 0,
            "adult": 0,
            "kitten": 0,
            "newborn": 0,
            "senior": 0,
            "senior adult": 0,
            "young adult": 0
        },
        "complication_risks": [
            {
                "chance": 70,
                "name": "infected_wound"
            },
            {
                "chance": 10,
                "name": "phantom_pain"
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    "one_bad_eye": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 10,
            "default_weight": 26
        },
        "herbs": {
            "1": [],
            "2": [],
            "3": []
        },
        "moons_until": 2,
        "mortality_risk": {
            "adolescent": 0,
            "adult": 0,
            "kitten": 0,
            "newborn": 0,
            "senior": 0,
            "senior adult": 0,
            "young adult": 0
        },
        "complication_risks": [
            {
                "chance": 80,
                "name": "failing_eyesight"
            }
        ],
        "severity": ConditionSeverity.Major
    },
    "paralyzed": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 5,
            "default_weight": 30
        },
        "herbs": {
            "1": [
                Herb.Daisy,
                Herb.JuniperBerry,
                Herb.Ragwort,
                Herb.Marigold
            ],
            "2": [],
            "3": []
        },
        "moons_until": 0,
        "mortality_risk": {
            "adolescent": 0,
            "adult": 0,
            "kitten": 0,
            "newborn": 0,
            "senior": 0,
            "senior adult": 0,
            "young adult": 0
        },
        "complication_risks": [
            {
                "chance": 60,
                "name": "infected_wound"
            },
            {
                "chance": 30,
                "name": "torn_pelt"
            },
            {
                "chance": 20,
                "name": "sore"
            },
            {
                "chance": 20,
                "name": "joint_pain"
            }
        ],
        "severity": ConditionSeverity.Severe
    },
    "partial_hearing_loss": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 5,
            "default_weight": 20
        },
        "herbs": {
            "1": [],
            "2": [],
            "3": []
        },
        "moons_until": 2,
        "mortality_risk": {
            "adolescent": 0,
            "adult": 0,
            "kitten": 0,
            "newborn": 0,
            "senior": 0,
            "senior adult": 0,
            "young adult": 0
        },
        "complication_risks": [
            {
                "chance": 80,
                "name": "deaf"
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    "persistent_headaches": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 15,
            "default_weight": 25
        },
        "herbs": {
            "1": [
                Herb.Poppy,
                Herb.JuniperBerry
            ],
            "2": [],
            "3": []
        },
        "moons_until": 4,
        "mortality_risk": {
            "adolescent": 0,
            "adult": 0,
            "kitten": 0,
            "newborn": 0,
            "senior": 0,
            "senior adult": 0,
            "young adult": 0
        },
        "complication_risks": [
            {
                "chance": 20,
                "name": "severe_headache"
            },
            {
                "chance": 20,
                "name": "headache"
            }
        ],
        "severity": ConditionSeverity.Major
    },
    "raspy_lungs": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 10,
            "default_weight": 20
        },
        "causes": [
            "event",
            "inheritance",
            "injury",
            "illness"
        ],
        "herbs": {
            "1": [
                Herb.Betony,
                Herb.Mullein
            ],
            "2": [],
            "3": []
        },
        "moons_until": 3,
        "mortality_risk": {
            "adolescent": 60,
            "adult": 90,
            "kitten": 20,
            "newborn": 20,
            "senior": 30,
            "senior adult": 60,
            "young adult": 80
        },
        "complication_risks": [
            {
                "chance": 20,
                "name": "whitecough"
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    "recurring_shock": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 0,
            "default_weight": 0
        },
        "herbs": {
            "1": [
                Herb.Thyme,
                Herb.JuniperBerry,
                Herb.Poppy
            ],
            "2": [],
            "3": []
        },
        "moons_until": 0,
        "mortality_risk": {
            "adolescent": 0,
            "adult": 0,
            "kitten": 0,
            "newborn": 0,
            "senior": 0,
            "senior adult": 0,
            "young adult": 0
        },
        "complication_risks": [
            {
            "chance": 20,
            "name": "constant_nightmares"
            }
        ],
        "severity": ConditionSeverity.Major
    },
    "seizure_prone": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 6,
            "default_weight": 40
        },
        "herbs": {
            "1": [
                Herb.Ragwort,
                Herb.JuniperBerry
            ],
            "2": [],
            "3": []
        },
        "moons_until": 3,
        "mortality_risk": {
            "adolescent": 0,
            "adult": 0,
            "kitten": 0,
            "newborn": 0,
            "senior": 0,
            "senior adult": 0,
            "young adult": 0
        },
        "complication_risks": [
            {
                "chance": 10,
                "name": "seizure"
            }
        ],
        "severity": ConditionSeverity.Major
    },
    "twisted_leg": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 0,
            "default_weight": 12
        },
        "herbs": {
            "1": [
                Herb.Daisy,
                Herb.JuniperBerry,
                Herb.Marigold,
                Herb.Ragwort
            ],
            "2": [],
            "3": []
        },
        "moons_until": 1,
        "mortality_risk": {
            "adolescent": 0,
            "adult": 0,
            "kitten": 0,
            "newborn": 0,
            "senior": 0,
            "senior adult": 0,
            "young adult": 0
        },
        "complication_risks": [
            {
                "chance": 20,
                "name": "sore"
            },
            {
                "chance": 40,
                "name": "joint_pain"
            }
        ],
        "severity": ConditionSeverity.Major
    },
    "wasting_disease": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 0,
            "default_weight": 0
        },
        "herbs": {
            "1": [
                Herb.JuniperBerry,
                Herb.Ragwort
            ],
            "2": [],
            "3": []
        },
        "moons_until": 1,
        "mortality_risk": {
            "adolescent": 40,
            "adult": 65,
            "kitten": 10,
            "newborn": 10,
            "senior": 10,
            "senior adult": 40,
            "young adult": 75
        },
        "complication_risks": [
            {
                "chance": 10,
                "name": "running_nose"
            },
            {
                "chance": 50,
                "name": "yellowcough"
            },
            {
                "chance": 60,
                "name": "redcough"
            }
        ],
        "severity": ConditionSeverity.Major
    },
    "weak_leg": {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 0,
            "default_weight": 12
        },
        "herbs": {
            "1": [
                Herb.Daisy,
                Herb.JuniperBerry,
                Herb.Marigold,
                Herb.Ragwort
            ],
            "2": [],
            "3": []
        },
        "moons_until": 3,
        "mortality_risk": {
            "adolescent": 0,
            "adult": 0,
            "kitten": 0,
            "newborn": 0,
            "senior": 0,
            "senior adult": 0,
            "young adult": 0
        },
        "complication_risks": [
            {
                "chance": 20,
                "name": "sore"
            },
            {
                "chance": 40,
                "name": "joint_pain"
            }
        ],
        "severity": ConditionSeverity.Minor
    }
}