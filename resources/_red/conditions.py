# conditions.py - TODO
# If you add new conditions, make sure to add their key to conditions.en.yaml otherwise they will not display.

########################################################################################################################
# Imports
########################################################################################################################

from definitions import ConditionCategory, ConditionName, ConditionSeverity, HerbName, AgeCategory

########################################################################################################################
# Constants
########################################################################################################################

ILLNESSES: dict = {
    ConditionName.Festering: {
        "category": ConditionCategory.Illness,
        "duration_moons": 3,
        "herbs": {
            "1": [
                HerbName.Marigold,
                HerbName.BurdockRoot,
                HerbName.OakLeaf,
                HerbName.RagwortLeaf,
                HerbName.JuniperBerry,
                HerbName.PoppySeed,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "infectiousness": 0,
        "medicine_duration_moons": 2,
        "medicated_mortality_risk": {
            AgeCategory.Newborn: 3,
            AgeCategory.Kitten: 3,
            AgeCategory.Adolescent: 5,
            AgeCategory.YoungAdult: 8,
            AgeCategory.SeniorAdult: 8,
            AgeCategory.Elder: 3,
        },
        "mortality_risk": {
            AgeCategory.Newborn: 1,
            AgeCategory.Kitten: 1,
            AgeCategory.Adolescent: 3,
            AgeCategory.YoungAdult: 3,
            AgeCategory.SeniorAdult: 5,
            AgeCategory.Elder: 8,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Major
    },
    ConditionName.Infected: {
        "category": ConditionCategory.Illness,
        "duration_moons": 3,
        "herbs": {
            "1": [
                HerbName.Marigold,
                HerbName.BurdockRoot,
                HerbName.WildGarlic,
                HerbName.PoppySeed
            ],
            "2": [],
            "3": []
        },
        "infectiousness": 0,
        "medicine_duration_moons": 2,
        "medicated_mortality_risk": {
            AgeCategory.Newborn: 5,
            AgeCategory.Kitten: 8,
            AgeCategory.Adolescent: 13,
            AgeCategory.YoungAdult: 15,
            AgeCategory.SeniorAdult: 15,
            AgeCategory.Elder: 13,
        },
        "mortality_risk": {
            AgeCategory.Newborn: 3,
            AgeCategory.Kitten: 3,
            AgeCategory.Adolescent: 8,
            AgeCategory.YoungAdult: 8,
            AgeCategory.SeniorAdult: 8,
            AgeCategory.Elder: 5,
        },
        "complication_risks": [
            {
                "chance": 10,
                "name": ConditionName.Festering
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.CarrionplaceDisease: {
        "category": ConditionCategory.Illness,
        "duration_moons": 3,
        "herbs": {
            "1": [
                HerbName.Marigold,
                HerbName.BurdockRoot,
                HerbName.WildGarlic,
                HerbName.PoppySeed
            ],
            "2": [],
            "3": []
        },
        "infectiousness": 0,
        "medicine_duration_moons": 2,
        "medicated_mortality_risk": {
            AgeCategory.Newborn: 2,
            AgeCategory.Kitten: 2,
            AgeCategory.Adolescent: 3,
            AgeCategory.YoungAdult: 3,
            AgeCategory.SeniorAdult: 3,
            AgeCategory.Elder: 2,
        },
        "mortality_risk": {
            AgeCategory.Newborn: 1,
            AgeCategory.Kitten: 1,
            AgeCategory.Adolescent: 2,
            AgeCategory.YoungAdult: 2,
            AgeCategory.SeniorAdult: 2,
            AgeCategory.Elder: 1,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Major
    },
    ConditionName.Nightmares: {
        "category": ConditionCategory.Illness,
        "duration_moons": 2,
        "herbs": {
            "1": [
                HerbName.JuniperBerry,
                HerbName.ThymeLeaf,
                HerbName.PoppySeed
            ],
            "2": [],
            "3": []
        },
        "infectiousness": 0,
        "medicine_duration_moons": 1,
        "medicated_mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.Diarrhea: {
        "category": ConditionCategory.Illness,
        "duration_moons": 2,
        "herbs": {
            "1": [
                HerbName.BetonyLeaf,
                HerbName.MulleinLeaf,
                HerbName.JuniperBerry,
                HerbName.Mallow
            ],
            "2": [],
            "3": []
        },
        "infectiousness": 0,
        "medicine_duration_moons": 2,
        "medicated_mortality_risk": {
            AgeCategory.Newborn: 10,
            AgeCategory.Kitten: 10,
            AgeCategory.Adolescent: 15,
            AgeCategory.YoungAdult: 30,
            AgeCategory.SeniorAdult: 30,
            AgeCategory.Elder: 13,
        },
        "mortality_risk": {
            AgeCategory.Newborn: 3,
            AgeCategory.Kitten: 3,
            AgeCategory.Adolescent: 8,
            AgeCategory.YoungAdult: 10,
            AgeCategory.SeniorAdult: 10,
            AgeCategory.Elder: 5,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.Fleas: {
        "category": ConditionCategory.Illness,
        "duration_moons": 4,
        "herbs": {
            "1": [
                HerbName.PlantainFlower
            ],
            "2": [],
            "3": []
        },
        "infectiousness": 15,
        "medicine_duration_moons": 2,
        "medicated_mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "mortality_risk": {
            AgeCategory.Newborn: 30,
            AgeCategory.Kitten: 20,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 20,
                "name": ConditionName.TornPelt
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.Greencough: {
        "category": ConditionCategory.Illness,
        "duration_moons": 3,
        "herbs": {
            "1": [
                HerbName.Catmint,
                HerbName.TansyStem,
                HerbName.MulleinLeaf,
                HerbName.PlantainFlower,
                HerbName.JuniperBerry,
                HerbName.PoppySeed,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "infectiousness": 30,
        "medicine_duration_moons": 2,
        "medicated_mortality_risk": {
            AgeCategory.Newborn: 7,
            AgeCategory.Kitten: 7,
            AgeCategory.Adolescent: 12,
            AgeCategory.YoungAdult: 25,
            AgeCategory.SeniorAdult: 20,
            AgeCategory.Elder: 7,
        },
        "mortality_risk": {
            AgeCategory.Newborn: 3,
            AgeCategory.Kitten: 4,
            AgeCategory.Adolescent: 8,
            AgeCategory.YoungAdult: 10,
            AgeCategory.SeniorAdult: 8,
            AgeCategory.Elder: 3,
        },
        "complication_risks": [
            {
                "chance": 60,
                "name": ConditionName.Yellowcough
            }
        ],
        "severity": ConditionSeverity.Major
    },
    ConditionName.Grieving: {
        "category": ConditionCategory.Illness,
        "duration_moons": 5,
        "herbs": {
            "1": [
                HerbName.JuniperBerry,
                HerbName.ThymeLeaf,
                HerbName.PoppySeed
            ],
            "2": [],
            "3": []
        },
        "infectiousness": 0,
        "medicine_duration_moons": 3,
        "medicated_mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 100,
                "name": ConditionName.LastingGrief
            },
            {
                "chance": 15,
                "name": ConditionName.Nightmares
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.HeatExhaustion: {
        "category": ConditionCategory.Illness,
        "duration_moons": 2,
        "herbs": {
            "1": [
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "infectiousness": 0,
        "medicine_duration_moons": 2,
        "medicated_mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 5,
                "name": ConditionName.HeatStroke
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.HeatStroke: {
        "category": ConditionCategory.Illness,
        "duration_moons": 1,
        "herbs": {
            "1": [
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "infectiousness": 0,
        "medicine_duration_moons": 1,
        "medicated_mortality_risk": {
            AgeCategory.Newborn: 5,
            AgeCategory.Kitten: 5,
            AgeCategory.Adolescent: 10,
            AgeCategory.YoungAdult: 15,
            AgeCategory.SeniorAdult: 25,
            AgeCategory.Elder: 10,
        },
        "mortality_risk": {
            AgeCategory.Newborn: 2,
            AgeCategory.Kitten: 4,
            AgeCategory.Adolescent: 5,
            AgeCategory.YoungAdult: 5,
            AgeCategory.SeniorAdult: 8,
            AgeCategory.Elder: 3,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Major
    },
    ConditionName.Kittencough: {
        "category": ConditionCategory.Illness,
        "duration_moons": 3,
        "herbs": {
            "1": [
                HerbName.Catmint,
                HerbName.TansyStem,
                HerbName.MulleinLeaf,
                HerbName.PlantainFlower,
                HerbName.JuniperBerry,
                HerbName.PoppySeed,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "infectiousness": 15,
        "medicine_duration_moons": 2,
        "medicated_mortality_risk": {
            AgeCategory.Newborn: 5,
            AgeCategory.Kitten: 5,
            AgeCategory.Adolescent: 60,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 10,
        },
        "mortality_risk": {
            AgeCategory.Newborn: 2,
            AgeCategory.Kitten: 2,
            AgeCategory.Adolescent: 15,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 5,
        },
        "complication_risks": [
            {
                "chance": 10,
                "name": ConditionName.Whitecough
            }
        ],
        "severity": ConditionSeverity.Major
    },
    ConditionName.Malnourished: {
        "category": ConditionCategory.Illness,
        "duration_moons": 100,
        "herbs": {
            "1": [
                HerbName.ThymeLeaf
            ],
            "2": [],
            "3": []
        },
        "infectiousness": 0,
        "medicine_duration_moons": 100,
        "medicated_mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.Redcough: {
        "category": ConditionCategory.Illness,
        "duration_moons": 50,
        "herbs": {
            "1": [
                HerbName.LungwortLeaf,
                HerbName.MulleinLeaf,
                HerbName.TansyStem,
                HerbName.PlantainFlower,
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf,
                HerbName.PoppySeed,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "infectiousness": 0,
        "medicine_duration_moons": 40,
        "medicated_mortality_risk": {
            AgeCategory.Newborn: 2,
            AgeCategory.Kitten: 2,
            AgeCategory.Adolescent: 3,
            AgeCategory.YoungAdult: 3,
            AgeCategory.SeniorAdult: 3,
            AgeCategory.Elder: 2,
        },
        "mortality_risk": {
            AgeCategory.Newborn: 1,
            AgeCategory.Kitten: 1,
            AgeCategory.Adolescent: 2,
            AgeCategory.YoungAdult: 2,
            AgeCategory.SeniorAdult: 2,
            AgeCategory.Elder: 1,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Major
    },
    ConditionName.RunningNose: {
        "category": ConditionCategory.Illness,
        "duration_moons": 3,
        "herbs": {
            "1": [
                HerbName.RagwortLeaf,
                HerbName.JuniperBerry,
                HerbName.PoppySeed
            ],
            "2": [],
            "3": []
        },
        "infectiousness": 0,
        "medicine_duration_moons": 2,
        "medicated_mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 15,
                "name": ConditionName.Whitecough
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.Seizure: {
        "category": ConditionCategory.Illness,
        "duration_moons": 1,
        "herbs": {
            "1": [
                HerbName.JuniperBerry,
                HerbName.PoppySeed,
                HerbName.ThymeLeaf,
                HerbName.RagwortLeaf
            ],
            "2": [],
            "3": []
        },
        "infectiousness": 0,
        "medicine_duration_moons": 1,
        "medicated_mortality_risk": {
            AgeCategory.Newborn: 30,
            AgeCategory.Kitten: 50,
            AgeCategory.Adolescent: 70,
            AgeCategory.YoungAdult: 150,
            AgeCategory.SeniorAdult: 150,
            AgeCategory.Elder: 70,
        },
        "mortality_risk": {
            AgeCategory.Newborn: 15,
            AgeCategory.Kitten: 25,
            AgeCategory.Adolescent: 50,
            AgeCategory.YoungAdult: 100,
            AgeCategory.SeniorAdult: 100,
            AgeCategory.Elder: 35,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Major
    },
    ConditionName.Starving: {
        "category": ConditionCategory.Illness,
        "duration_moons": 100,
        "herbs": {
            "1": [
                HerbName.ThymeLeaf
            ],
            "2": [],
            "3": []
        },
        "infectiousness": 0,
        "medicine_duration_moons": 100,
        "medicated_mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Major
    },
    ConditionName.Stomachache: {
        "category": ConditionCategory.Illness,
        "duration_moons": 2,
        "herbs": {
            "1": [
                HerbName.JuniperBerry,
                HerbName.Mallow,
                HerbName.RagwortLeaf,
                HerbName.PoppySeed
            ],
            "2": [],
            "3": []
        },
        "infectiousness": 0,
        "medicine_duration_moons": 1,
        "medicated_mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 8,
                "name": ConditionName.Diarrhea
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.Whitecough: {
        "category": ConditionCategory.Illness,
        "duration_moons": 3,
        "herbs": {
            "1": [
                HerbName.Catmint,
                HerbName.PlantainFlower,
                HerbName.TansyStem,
                HerbName.MulleinLeaf,
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf,
                HerbName.PoppySeed,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "infectiousness": 30,
        "medicine_duration_moons": 2,
        "medicated_mortality_risk": {
            AgeCategory.Newborn: 15,
            AgeCategory.Kitten: 15,
            AgeCategory.Adolescent: 60,
            AgeCategory.YoungAdult: 70,
            AgeCategory.SeniorAdult: 70,
            AgeCategory.Elder: 15,
        },
        "mortality_risk": {
            AgeCategory.Newborn: 10,
            AgeCategory.Kitten: 10,
            AgeCategory.Adolescent: 20,
            AgeCategory.YoungAdult: 60,
            AgeCategory.SeniorAdult: 50,
            AgeCategory.Elder: 10,
        },
        "complication_risks": [
            {
                "chance": 18,
                "name": ConditionName.Greencough
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.Yellowcough: {
        "category": ConditionCategory.Illness,
        "duration_moons": 3,
        "herbs": {
            "1": [
                HerbName.LungwortLeaf
            ],
            "2": [],
            "3": []
        },
        "infectiousness": 30,
        "medicine_duration_moons": 3,
        "medicated_mortality_risk": {
            AgeCategory.Newborn: 5,
            AgeCategory.Kitten: 5,
            AgeCategory.Adolescent: 10,
            AgeCategory.YoungAdult: 15,
            AgeCategory.SeniorAdult: 15,
            AgeCategory.Elder: 5,
        },
        "mortality_risk": {
            AgeCategory.Newborn: 2,
            AgeCategory.Kitten: 2,
            AgeCategory.Adolescent: 3,
            AgeCategory.YoungAdult: 5,
            AgeCategory.SeniorAdult: 5,
            AgeCategory.Elder: 3,
        },
        "complication_risks": [
            {
                "chance": 80,
                "name": ConditionName.Redcough
            }
        ],
        "severity": ConditionSeverity.Medium
    },
}

INJURIES: dict = {
    ConditionName.BeakBite: {
        "category": ConditionCategory.Injury,
        "also_got": [
            ConditionName.TornPelt,
            ConditionName.BloodLoss
        ],
        "cause_permanent": [],
        "duration_moons": 2,
        "herbs": {
            "1": [
                HerbName.Cobweb,
                HerbName.Goldenrod,
                HerbName.Marigold,
                HerbName.OakLeaf,
                HerbName.WildGarlic,
                HerbName.TansyStem,
                HerbName.PoppySeed,
                HerbName.RagwortLeaf,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 10,
            AgeCategory.Kitten: 10,
            AgeCategory.Adolescent: 45,
            AgeCategory.YoungAdult: 60,
            AgeCategory.SeniorAdult: 60,
            AgeCategory.Elder: 15,
        },
        "complication_risks": [
            {
                "chance": 5,
                "name": ConditionName.Infected
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.BeeSting: {
        "category": ConditionCategory.Injury,
        "also_got": [],
        "cause_permanent": [],
        "duration_moons": 2,
        "herbs": {
            "1": [
                HerbName.BlackberryLeaf,
                HerbName.DandelionLeaf,
                HerbName.PoppySeed
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 10,
            AgeCategory.Kitten: 20,
            AgeCategory.Adolescent: 30,
            AgeCategory.YoungAdult: 50,
            AgeCategory.SeniorAdult: 50,
            AgeCategory.Elder: 30,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.BiteWound: {
        "category": ConditionCategory.Injury,
        "also_got": [
            ConditionName.TornPelt,
            ConditionName.BloodLoss
        ],
        "cause_permanent": [],
        "duration_moons": 3,
        "herbs": {
            "1": [
                HerbName.Cobweb,
                HerbName.Goldenrod,
                HerbName.Marigold,
                HerbName.OakLeaf,
                HerbName.WildGarlic,
                HerbName.TansyStem,
                HerbName.PoppySeed,
                HerbName.RagwortLeaf,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 2,
        "mortality_risk": {
            AgeCategory.Newborn: 10,
            AgeCategory.Kitten: 10,
            AgeCategory.Adolescent: 45,
            AgeCategory.YoungAdult: 60,
            AgeCategory.SeniorAdult: 60,
            AgeCategory.Elder: 15,
        },
        "complication_risks": [
            {
                "chance": 5,
                "name": ConditionName.Infected
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.BloodLoss: {
        "category": ConditionCategory.Injury,
        "also_got": [
            ConditionName.Shock
        ],
        "cause_permanent": [],
        "duration_moons": 1,
        "herbs": {
            "1": [
                HerbName.Cobweb,
                HerbName.Horsetail,
                HerbName.Marigold,
                HerbName.RagwortLeaf,
                HerbName.JuniperBerry,
                HerbName.Moss,
                HerbName.PoppySeed
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 5,
            AgeCategory.Kitten: 5,
            AgeCategory.Adolescent: 10,
            AgeCategory.YoungAdult: 25,
            AgeCategory.SeniorAdult: 20,
            AgeCategory.Elder: 15,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.BrokenBack: {
        "category": ConditionCategory.Injury,
        "also_got": [],
        "cause_permanent": [
            "paralyzed"
        ],
        "duration_moons": 8,
        "herbs": {
            "1": [
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf,
                HerbName.PoppySeed
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 6,
        "mortality_risk": {
            AgeCategory.Newborn: 3,
            AgeCategory.Kitten: 5,
            AgeCategory.Adolescent: 25,
            AgeCategory.YoungAdult: 30,
            AgeCategory.SeniorAdult: 25,
            AgeCategory.Elder: 10,
        },
        "complication_risks": [
            {
                "chance": 10,
                "name": ConditionName.Infected
            }
        ],
        "severity": ConditionSeverity.Major
    },
    ConditionName.BrokenBone: {
        "category": ConditionCategory.Injury,
        "also_got": [
            ConditionName.TornPelt,
            ConditionName.MangledLeg,
            ConditionName.BloodLoss,
            ConditionName.Scrapes,
            ConditionName.Bruises
        ],
        "cause_permanent": [
            "weak_leg",
            "twisted_leg"
        ],
        "duration_moons": 5,
        "herbs": {
            "1": [
                HerbName.Cobweb,
                HerbName.Marigold,
                HerbName.OakLeaf,
                HerbName.WildGarlic,
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf,
                HerbName.PoppySeed,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 3,
        "mortality_risk": {
            AgeCategory.Newborn: 10,
            AgeCategory.Kitten: 10,
            AgeCategory.Adolescent: 45,
            AgeCategory.YoungAdult: 60,
            AgeCategory.SeniorAdult: 60,
            AgeCategory.Elder: 15,
        },
        "complication_risks": [
            {
                "chance": 5,
                "name": ConditionName.Infected
            }
        ],
        "severity": ConditionSeverity.Major
    },
    ConditionName.BrokenJaw: {
        "category": ConditionCategory.Injury,
        "also_got": [
            ConditionName.BloodLoss,
            ConditionName.Scrapes,
            ConditionName.Bruises
        ],
        "cause_permanent": [
            ConditionName.CrookedJaw
        ],
        "duration_moons": 4,
        "herbs": {
            "1": [
                HerbName.Cobweb,
                HerbName.Marigold,
                HerbName.OakLeaf,
                HerbName.WildGarlic,
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf,
                HerbName.PoppySeed,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 3,
        "mortality_risk": {
            AgeCategory.Newborn: 10,
            AgeCategory.Kitten: 10,
            AgeCategory.Adolescent: 35,
            AgeCategory.YoungAdult: 50,
            AgeCategory.SeniorAdult: 50,
            AgeCategory.Elder: 10,
        },
        "complication_risks": [
            {
                "chance": 5,
                "name": ConditionName.Infected
            }
        ],
        "severity": ConditionSeverity.Major
    },
    ConditionName.Bruises: {
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
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.Burn: {
        "category": ConditionCategory.Injury,
        "also_got": [],
        "cause_permanent": [],
        "duration_moons": 2,
        "herbs": {
            "1": [
                HerbName.Cobweb,
                HerbName.Marigold,
                HerbName.WildGarlic,
                HerbName.OakLeaf,
                HerbName.Goldenrod,
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf,
                HerbName.PoppySeed,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 2,
        "mortality_risk": {
            AgeCategory.Newborn: 10,
            AgeCategory.Kitten: 10,
            AgeCategory.Adolescent: 30,
            AgeCategory.YoungAdult: 50,
            AgeCategory.SeniorAdult: 50,
            AgeCategory.Elder: 30,
        },
        "complication_risks": [
            {
                "chance": 25,
                "name": ConditionName.Infected
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.CatBite: {
        "category": ConditionCategory.Injury,
        "also_got": [
            ConditionName.TornPelt,
            ConditionName.BloodLoss
        ],
        "cause_permanent": [],
        "duration_moons": 2,
        "herbs": {
            "1": [
                HerbName.Cobweb,
                HerbName.Goldenrod,
                HerbName.Marigold,
                HerbName.OakLeaf,
                HerbName.WildGarlic,
                HerbName.TansyStem,
                HerbName.PoppySeed,
                HerbName.RagwortLeaf,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 2,
        "mortality_risk": {
            AgeCategory.Newborn: 10,
            AgeCategory.Kitten: 10,
            AgeCategory.Adolescent: 45,
            AgeCategory.YoungAdult: 60,
            AgeCategory.SeniorAdult: 60,
            AgeCategory.Elder: 15,
        },
        "complication_risks": [
            {
                "chance": 5,
                "name": ConditionName.Infected
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.ClawWound: {
        "category": ConditionCategory.Injury,
        "also_got": [
            ConditionName.TornPelt,
            ConditionName.TornEar,
            ConditionName.BloodLoss
        ],
        "cause_permanent": [],
        "duration_moons": 3,
        "herbs": {
            "1": [
                HerbName.Cobweb,
                HerbName.Goldenrod,
                HerbName.Marigold,
                HerbName.OakLeaf,
                HerbName.WildGarlic,
                HerbName.TansyStem,
                HerbName.PoppySeed,
                HerbName.RagwortLeaf,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 2,
        "mortality_risk": {
            AgeCategory.Newborn: 5,
            AgeCategory.Kitten: 5,
            AgeCategory.Adolescent: 40,
            AgeCategory.YoungAdult: 50,
            AgeCategory.SeniorAdult: 50,
            AgeCategory.Elder: 10,
        },
        "complication_risks": [
            {
                "chance": 5,
                "name": ConditionName.Infected
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.CrackedPads: {
        "category": ConditionCategory.Injury,
        "also_got": [],
        "cause_permanent": [],
        "duration_moons": 1,
        "herbs": {
            "1": [
                HerbName.OakLeaf,
                HerbName.Marigold,
                HerbName.WildGarlic,
                HerbName.PoppySeed
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 20,
                "name": ConditionName.Infected
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.DamagedEyes: {
        "category": ConditionCategory.Injury,
        "also_got": [],
        "cause_permanent": [
            ConditionName.Blind,
            ConditionName.BadEye,
            ConditionName.FailingEyesight
        ],
        "duration_moons": 6,
        "herbs": {
            "1": [
                # HerbName.Celandine,
                HerbName.Cobweb,
                HerbName.Goldenrod,
                HerbName.Marigold,
                HerbName.OakLeaf,
                HerbName.WildGarlic,
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf,
                HerbName.PoppySeed,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 4,
        "mortality_risk": {
            AgeCategory.Newborn: 30,
            AgeCategory.Kitten: 30,
            AgeCategory.Adolescent: 50,
            AgeCategory.YoungAdult: 70,
            AgeCategory.SeniorAdult: 70,
            AgeCategory.Elder: 50,
        },
        "complication_risks": [
            {
                "chance": 4,
                "name": ConditionName.Infected
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.Dehydrated: {
        "also_got": [
            ConditionName.HeatExhaustion
        ],
        "category": ConditionCategory.Injury,
        "cause_permanent": [],
        "duration_moons": 1,
        "herbs": {
            "1": [
                HerbName.RagwortLeaf,
                HerbName.JuniperBerry,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 10,
            AgeCategory.Kitten: 10,
            AgeCategory.Adolescent: 30,
            AgeCategory.YoungAdult: 50,
            AgeCategory.SeniorAdult: 50,
            AgeCategory.Elder: 20,
        },
        "complication_risks": [
            {
                "chance": 10,
                "name": ConditionName.HeatExhaustion
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.Dislocation: {
        "also_got": [
            ConditionName.Bruises,
            ConditionName.Sore,
            ConditionName.JointPain
        ],
        "category": ConditionCategory.Injury,
        "cause_permanent": [
            ConditionName.ChronicJointPain
        ],
        "duration_moons": 2,
        "herbs": {
            "1": [
                HerbName.Marigold,
                HerbName.RagwortLeaf,
                HerbName.DaisyLeaf,
                HerbName.PoppySeed
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.Frostbite: {
        "also_got": [],
        "cause_permanent": [
            ConditionName.LostLeg,
            ConditionName.LostTail
        ],
        "category": ConditionCategory.Injury,
        "duration_moons": 2,
        "herbs": {
            "1": [
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf,
                HerbName.PoppySeed,
                HerbName.Moss,
                HerbName.DandelionLeaf
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 2,
        "mortality_risk": {
            AgeCategory.Newborn: 10,
            AgeCategory.Kitten: 10,
            AgeCategory.Adolescent: 20,
            AgeCategory.YoungAdult: 20,
            AgeCategory.SeniorAdult: 25,
            AgeCategory.Elder: 10,
        },
        "complication_risks": [
            {
                "chance": 4,
                "name": ConditionName.RunningNose
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.HeadDamage: {
        "also_got": [],
        "category": ConditionCategory.Injury,
        "cause_permanent": [
            ConditionName.FailingEyesight,
            ConditionName.BadEye,
            ConditionName.Blind,
            ConditionName.ConstantlyDizzy,
            ConditionName.HearingLoss,
            ConditionName.ChronicHeadaches
        ],
        "duration_moons": 5,
        "herbs": {
            "1": [
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf,
                HerbName.ThymeLeaf
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 2,
        "mortality_risk": {
            AgeCategory.Newborn: 10,
            AgeCategory.Kitten: 15,
            AgeCategory.Adolescent: 30,
            AgeCategory.YoungAdult: 40,
            AgeCategory.SeniorAdult: 40,
            AgeCategory.Elder: 20,
        },
        "complication_risks": [
            {
                "chance": 20,
                "name": ConditionName.Headache
            },
            {
                "chance": 20,
                "name": ConditionName.Migraine
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.Headache: {
        "also_got": [],
        "category": ConditionCategory.Injury,
        "cause_permanent": [],
        "duration_moons": 1,
        "herbs": {
            "1": [
                HerbName.PoppySeed,
                HerbName.JuniperBerry
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.JointPain: {
        "also_got": [],
        "category": ConditionCategory.Injury,
        "cause_permanent": [],
        "duration_moons": 2,
        "herbs": {
            "1": [
                HerbName.Marigold,
                HerbName.RagwortLeaf,
                HerbName.DaisyLeaf,
                HerbName.PoppySeed
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 2,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.LingeringShock: {
        "also_got": [],
        "category": ConditionCategory.Injury,
        "cause_permanent": [
            ConditionName.ChronicShock
        ],
        "duration_moons": 12,
        "herbs": {
            "1": [
                HerbName.ThymeLeaf,
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf,
                HerbName.PoppySeed
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 8,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.MangledLeg: {
        "also_got": [
            ConditionName.TornPelt,
            ConditionName.BrokenBone,
            ConditionName.Dislocation,
            ConditionName.BloodLoss,
            ConditionName.Scrapes,
            ConditionName.Bruises
        ],
        "category": ConditionCategory.Injury,
        "cause_permanent": [
            ConditionName.LostLeg,
            "weak_leg",
            "twisted_leg"
        ],
        "duration_moons": 3,
        "herbs": {
            "1": [
                HerbName.Cobweb,
                HerbName.Goldenrod,
                HerbName.Marigold,
                HerbName.WildGarlic,
                HerbName.OakLeaf,
                HerbName.TansyStem,
                HerbName.PoppySeed,
                HerbName.RagwortLeaf,
                HerbName.JuniperBerry,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 3,
        "mortality_risk": {
            AgeCategory.Newborn: 10,
            AgeCategory.Kitten: 15,
            AgeCategory.Adolescent: 50,
            AgeCategory.YoungAdult: 60,
            AgeCategory.SeniorAdult: 60,
            AgeCategory.Elder: 10,
        },
        "complication_risks": [
            {
                "chance": 5,
                "name": ConditionName.Infected
            }
        ],
        "severity": ConditionSeverity.Major
    },
    ConditionName.MangledTail: {
        "also_got": [
            ConditionName.TornPelt,
            ConditionName.BloodLoss
        ],
        "category": ConditionCategory.Injury,
        "cause_permanent": [
            ConditionName.LostTail
        ],
        "duration_moons": 3,
        "herbs": {
            "1": [
                HerbName.Cobweb,
                HerbName.Goldenrod,
                HerbName.Marigold,
                HerbName.WildGarlic,
                HerbName.OakLeaf,
                HerbName.TansyStem,
                HerbName.PoppySeed,
                HerbName.RagwortLeaf,
                HerbName.JuniperBerry,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 3,
        "mortality_risk": {
            AgeCategory.Newborn: 10,
            AgeCategory.Kitten: 15,
            AgeCategory.Adolescent: 50,
            AgeCategory.YoungAdult: 60,
            AgeCategory.SeniorAdult: 60,
            AgeCategory.Elder: 10,
        },
        "complication_risks": [
            {
                "chance": 5,
                "name": ConditionName.Infected
            }
        ],
        "severity": ConditionSeverity.Major
    },
    ConditionName.PhantomPain: {
        "also_got": [],
        "category": ConditionCategory.Injury,
        "cause_permanent": [],
        "duration_moons": 2,
        "herbs": {
            "1": [
                HerbName.DandelionLeaf,
                HerbName.PoppySeed,
                HerbName.RaspberryLeaf
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.Poisoned: {
        "also_got": [
            ConditionName.Shock
        ],
        "category": ConditionCategory.Injury,
        "cause_permanent": [],
        "duration_moons": 2,
        "herbs": {
            "1": [
                HerbName.DandelionLeaf,
                HerbName.TansyStem,
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf,
                HerbName.PoppySeed
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 5,
            AgeCategory.Kitten: 10,
            AgeCategory.Adolescent: 15,
            AgeCategory.YoungAdult: 20,
            AgeCategory.SeniorAdult: 20,
            AgeCategory.Elder: 15,
        },
        "complication_risks": [
            {
                "chance": 10,
                "name": ConditionName.Redcough
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.Porcupine: {
        "also_got": [
            ConditionName.TornPelt
        ],
        "category": ConditionCategory.Injury,
        "cause_permanent": [],
        "duration_moons": 2,
        "herbs": {
            "1": [
                HerbName.Cobweb,
                HerbName.Goldenrod,
                HerbName.Marigold,
                HerbName.OakLeaf,
                HerbName.WildGarlic,
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf,
                HerbName.PoppySeed,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 10,
            AgeCategory.Kitten: 20,
            AgeCategory.Adolescent: 40,
            AgeCategory.YoungAdult: 50,
            AgeCategory.SeniorAdult: 50,
            AgeCategory.Elder: 30,
        },
        "complication_risks": [
            {
                "chance": 5,
                "name": ConditionName.Infected
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.RatBite: {
        "also_got": [
            ConditionName.TornPelt
        ],
        "category": ConditionCategory.Injury,
        "cause_permanent": [],
        "duration_moons": 2,
        "herbs": {
            "1": [
                HerbName.WildGarlic,
                HerbName.BurdockRoot,
                HerbName.TansyStem,
                HerbName.Cobweb,
                HerbName.Marigold,
                HerbName.OakLeaf,
                HerbName.Goldenrod,
                HerbName.JuniperBerry,
                HerbName.PoppySeed,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 10,
            AgeCategory.Kitten: 10,
            AgeCategory.Adolescent: 45,
            AgeCategory.YoungAdult: 60,
            AgeCategory.SeniorAdult: 60,
            AgeCategory.Elder: 15,
        },
        "complication_risks": [
            {
                "chance": 5,
                "name": ConditionName.Infected
            },
            {
                "chance": 5,
                "name": ConditionName.Festering
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.Scrapes: {
        "also_got": [],
        "category": ConditionCategory.Injury,
        "cause_permanent": [],
        "duration_moons": 1,
        "herbs": {
            "1": [
                HerbName.Cobweb,
                HerbName.Marigold,
                HerbName.OakLeaf,
                HerbName.WildGarlic
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 30,
                "name": ConditionName.Infected
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.SevereBurn: {
        "also_got": [],
        "category": ConditionCategory.Injury,
        "cause_permanent": [
            ConditionName.LostTail,
            ConditionName.LostLeg
        ],
        "duration_moons": 4,
        "herbs": {
            "1": [
                HerbName.Cobweb,
                HerbName.Marigold,
                HerbName.WildGarlic,
                HerbName.OakLeaf,
                HerbName.Goldenrod,
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf,
                HerbName.PoppySeed,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 3,
        "mortality_risk": {
            AgeCategory.Newborn: 5,
            AgeCategory.Kitten: 5,
            AgeCategory.Adolescent: 10,
            AgeCategory.YoungAdult: 30,
            AgeCategory.SeniorAdult: 30,
            AgeCategory.Elder: 10,
        },
        "complication_risks": [
            {
                "chance": 15,
                "name": ConditionName.Infected
            }
        ],
        "severity": ConditionSeverity.Major
    },
    ConditionName.Migraine: {
        "also_got": [],
        "category": ConditionCategory.Injury,
        "cause_permanent": [],
        "duration_moons": 1,
        "herbs": {
            "1": [
                HerbName.PoppySeed,
                HerbName.JuniperBerry
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.Shivering: {
        "also_got": [
            ConditionName.Frostbite
        ],
        "category": ConditionCategory.Injury,
        "cause_permanent": [],
        "duration_moons": 2,
        "herbs": {
            "1": [
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf,
                HerbName.TansyStem
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 10,
            AgeCategory.Kitten: 10,
            AgeCategory.Adolescent: 30,
            AgeCategory.YoungAdult: 50,
            AgeCategory.SeniorAdult: 50,
            AgeCategory.Elder: 20,
        },
        "complication_risks": [
            {
                "chance": 5,
                "name": ConditionName.Frostbite
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.Shock: {
        "also_got": [],
        "category": ConditionCategory.Injury,
        "cause_permanent": [],
        "duration_moons": 1,
        "herbs": {
            "1": [
                HerbName.ThymeLeaf,
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf,
                HerbName.PoppySeed
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 8,
            AgeCategory.Kitten: 10,
            AgeCategory.Adolescent: 15,
            AgeCategory.YoungAdult: 30,
            AgeCategory.SeniorAdult: 30,
            AgeCategory.Elder: 15,
        },
        "complication_risks": [
            {
                "chance": 15,
                "name": ConditionName.LingeringShock
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.SmallCut: {
        "also_got": [],
        "category": ConditionCategory.Injury,
        "cause_permanent": [],
        "duration_moons": 1,
        "herbs": {
            "1": [
                HerbName.Marigold,
                HerbName.OakLeaf,
                HerbName.WildGarlic
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 40,
                "name": ConditionName.Infected
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.SnakeBite: {
        "also_got": [
            ConditionName.Poisoned
        ],
        "category": ConditionCategory.Injury,
        "cause_permanent": [],
        "duration_moons": 2,
        "herbs": {
            "1": [
                HerbName.TansyStem,
                HerbName.Marigold,
                HerbName.OakLeaf,
                HerbName.Goldenrod,
                HerbName.WildGarlic,
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf,
                HerbName.PoppySeed
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 10,
            AgeCategory.Kitten: 10,
            AgeCategory.Adolescent: 45,
            AgeCategory.YoungAdult: 60,
            AgeCategory.SeniorAdult: 60,
            AgeCategory.Elder: 15,
        },
        "complication_risks": [
            {
                "chance": 5,
                "name": ConditionName.Infected
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.Sore: {
        "also_got": [],
        "category": ConditionCategory.Injury,
        "cause_permanent": [],
        "duration_moons": 1,
        "herbs": {
            "1": [
                HerbName.DaisyLeaf,
                HerbName.DandelionLeaf,
                HerbName.Marigold,
                HerbName.RagwortLeaf,
                HerbName.PoppySeed
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.Sprain: {
        "also_got": [],
        "category": ConditionCategory.Injury,
        "cause_permanent": [],
        "duration_moons": 2,
        "herbs": {
            "1": [
                HerbName.ElderLeaf,
                HerbName.DandelionLeaf,
                HerbName.PoppySeed
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.TickBites: {
        "also_got": [],
        "category": ConditionCategory.Injury,
        "cause_permanent": [],
        "duration_moons": 2,
        "herbs": {
            "1": [
                HerbName.Moss,
                HerbName.PlantainFlower
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 40,
                "name": ConditionName.Infected
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.TornEar: {
        "also_got": [],
        "category": ConditionCategory.Injury,
        "cause_permanent": [
            ConditionName.HearingLoss
        ],
        "duration_moons": 1,
        "herbs": {
            "1": [
                HerbName.Cobweb,
                HerbName.Goldenrod,
                HerbName.Marigold,
                HerbName.OakLeaf,
                HerbName.WildGarlic
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 25,
                "name": ConditionName.Infected
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.TornPelt: {
        "also_got": [],
        "category": ConditionCategory.Injury,
        "cause_permanent": [],
        "duration_moons": 1,
        "herbs": {
            "1": [
                HerbName.Cobweb,
                HerbName.Goldenrod,
                HerbName.Marigold,
                HerbName.OakLeaf,
                HerbName.WildGarlic,
                HerbName.RaspberryLeaf
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 25,
                "name": ConditionName.Infected
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.SpicyLungs: {
        "also_got": [],
        "category": ConditionCategory.Injury,
        "cause_permanent": [
            ConditionName.RaspyLungs
        ],
        "duration_moons": 3,
        "herbs": {
            "1": [
                HerbName.JuniperBerry,
                HerbName.BetonyLeaf,
                HerbName.MulleinLeaf,
                HerbName.TansyStem,
                HerbName.PlantainFlower,
                HerbName.RagwortLeaf
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 2,
        "mortality_risk": {
            AgeCategory.Newborn: 10,
            AgeCategory.Kitten: 15,
            AgeCategory.Adolescent: 50,
            AgeCategory.YoungAdult: 60,
            AgeCategory.SeniorAdult: 60,
            AgeCategory.Elder: 30,
        },
        "complication_risks": [
            {
                "chance": 10,
                "name": ConditionName.RunningNose
            },
            {
                "chance": 20,
                "name": ConditionName.Whitecough
            }
        ],
        "severity": ConditionSeverity.Medium
    },
}

PERMANENT_CONDITIONS: dict = {
    ConditionName.Allergies: {
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
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 20,
                "name": ConditionName.RunningNose
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.BadEye: {
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
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 80,
                "name": ConditionName.FailingEyesight
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.Blind: {
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
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.BornWithoutLeg: {
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
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 20,
                "name": ConditionName.Sore
            },
            {
                "chance": 40,
                "name": ConditionName.JointPain
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.BornWithoutTail: {
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
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.ChronicHeadaches: {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 15,
            "default_weight": 25
        },
        "herbs": {
            "1": [
                HerbName.PoppySeed,
                HerbName.JuniperBerry
            ],
            "2": [],
            "3": []
        },
        "moons_until": 4,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 20,
                "name": ConditionName.Migraine
            },
            {
                "chance": 20,
                "name": ConditionName.Headache
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.ChronicShock: {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 0,
            "default_weight": 0
        },
        "herbs": {
            "1": [
                HerbName.ThymeLeaf,
                HerbName.JuniperBerry,
                HerbName.PoppySeed
            ],
            "2": [],
            "3": []
        },
        "moons_until": 0,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 20,
                "name": ConditionName.Nightmares
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.ConstantlyDizzy: {
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
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 20,
                "name": ConditionName.Headache
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.CrookedJaw: {
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
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.Deaf: {
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
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.FailingEyesight: {
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
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 50,
                "name": ConditionName.Blind
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.HearingLoss: {
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
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 80,
                "name": "deaf"
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.ChronicJointPain: {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 10,
            "default_weight": 25
        },
        "herbs": {
            "1": [
                HerbName.DaisyLeaf,
                HerbName.JuniperBerry,
                HerbName.Marigold,
                HerbName.RagwortLeaf
            ],
            "2": [],
            "3": []
        },
        "moons_until": 2,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 10,
                "name": ConditionName.JointPain
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.LastingGrief: {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 0,
            "default_weight": 0
        },
        "herbs": {
            "1": [
                HerbName.ThymeLeaf,
                HerbName.JuniperBerry,
                HerbName.PoppySeed
            ],
            "2": [],
            "3": []
        },
        "moons_until": 0,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 50,
                "name": ConditionName.Grieving
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.LostLeg: {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 0,
            "default_weight": 0
        },
        "herbs": {
            "1": [
                HerbName.DaisyLeaf,
                HerbName.JuniperBerry,
                HerbName.Marigold,
                HerbName.RagwortLeaf
            ],
            "2": [],
            "3": []
        },
        "moons_until": 0,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 70,
                "name": ConditionName.Infected
            },
            {
                "chance": 20,
                "name": ConditionName.PhantomPain
            },
            {
                "chance": 20,
                "name": ConditionName.Sore
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.LostTail: {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 0,
            "default_weight": 0
        },
        "herbs": {
            "1": [
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf
            ],
            "2": [],
            "3": []
        },
        "moons_until": 0,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 70,
                "name": ConditionName.Infected
            },
            {
                "chance": 10,
                "name": ConditionName.PhantomPain
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.Paralysed: {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 5,
            "default_weight": 30
        },
        "herbs": {
            "1": [
                HerbName.DaisyLeaf,
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf,
                HerbName.Marigold
            ],
            "2": [],
            "3": []
        },
        "moons_until": 0,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 60,
                "name": ConditionName.Infected
            },
            {
                "chance": 30,
                "name": ConditionName.TornPelt
            },
            {
                "chance": 20,
                "name": ConditionName.Sore
            },
            {
                "chance": 20,
                "name": ConditionName.JointPain
            }
        ],
        "severity": ConditionSeverity.Major
    },
    ConditionName.RaspyLungs: {
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
                HerbName.BetonyLeaf,
                HerbName.MulleinLeaf
            ],
            "2": [],
            "3": []
        },
        "moons_until": 3,
        "mortality_risk": {
            AgeCategory.Newborn: 20,
            AgeCategory.Kitten: 20,
            AgeCategory.Adolescent: 60,
            AgeCategory.YoungAdult: 80,
            AgeCategory.SeniorAdult: 60,
            AgeCategory.Elder: 30,
        },
        "complication_risks": [
            {
                "chance": 20,
                "name": ConditionName.Whitecough
            }
        ],
        "severity": ConditionSeverity.Minor
    },
    ConditionName.Seizures: {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 6,
            "default_weight": 40
        },
        "herbs": {
            "1": [
                HerbName.RagwortLeaf,
                HerbName.JuniperBerry
            ],
            "2": [],
            "3": []
        },
        "moons_until": 3,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 10,
                "name": ConditionName.Seizure
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.TwistedLeg: {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 0,
            "default_weight": 12
        },
        "herbs": {
            "1": [
                HerbName.DaisyLeaf,
                HerbName.JuniperBerry,
                HerbName.Marigold,
                HerbName.RagwortLeaf
            ],
            "2": [],
            "3": []
        },
        "moons_until": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 20,
                "name": ConditionName.Sore
            },
            {
                "chance": 40,
                "name": ConditionName.JointPain
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.WastingDisease: {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 0,
            "default_weight": 0
        },
        "herbs": {
            "1": [
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf
            ],
            "2": [],
            "3": []
        },
        "moons_until": 1,
        "mortality_risk": {
            AgeCategory.Newborn: 50,
            AgeCategory.Kitten: 10,
            AgeCategory.Adolescent: 40,
            AgeCategory.YoungAdult: 75,
            AgeCategory.SeniorAdult: 40,
            AgeCategory.Elder: 10,
        },
        "complication_risks": [
            {
                "chance": 10,
                "name": ConditionName.RunningNose
            },
            {
                "chance": 50,
                "name": ConditionName.Yellowcough
            },
            {
                "chance": 60,
                "name": ConditionName.Redcough
            }
        ],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.WeakLeg: {
        "category": ConditionCategory.Permanent,
        "inheritance": {
            "per_parent_modifier": 0,
            "default_weight": 12
        },
        "herbs": {
            "1": [
                HerbName.DaisyLeaf,
                HerbName.JuniperBerry,
                HerbName.Marigold,
                HerbName.RagwortLeaf
            ],
            "2": [],
            "3": []
        },
        "moons_until": 3,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 20,
                "name": ConditionName.Sore
            },
            {
                "chance": 40,
                "name": ConditionName.JointPain
            }
        ],
        "severity": ConditionSeverity.Minor
    },
}

PREGNANCY_CONDITIONS: dict = {
    ConditionName.Expecting: {
        "also_got": [],
        "category": ConditionCategory.Pregnancy,
        "cause_permanent": [],
        "duration_moons": 2,
        "herbs": {
            "1": [],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 3,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 40,
            AgeCategory.SeniorAdult: 30,
            AgeCategory.Elder: 20,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Medium
    },
    ConditionName.Nursing: {
        "also_got": [],
        "category": ConditionCategory.Pregnancy,
        "cause_permanent": [],
        "duration_moons": 6, # in the books queens stay in the nursery until their kittens become apprentices
        "herbs": {
            "1": [], # TODO [HerbName.Borage, ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 2, # kittens stop nursing after 8-10 weeks
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [],
        "severity": ConditionSeverity.Medium

    },
    ConditionName.BirthRecovery: {
        "also_got": [
            ConditionName.BloodLoss
        ],
        "category": ConditionCategory.Pregnancy,
        "cause_permanent": [],
        "duration_moons": 3,
        "herbs": {
            "1": [
                HerbName.OakLeaf,
                HerbName.JuniperBerry,
                HerbName.RagwortLeaf,
                HerbName.Moss
            ],
            "2": [],
            "3": []
        },
        "medicine_duration_moons": 5,
        "mortality_risk": {
            AgeCategory.Newborn: 0,
            AgeCategory.Kitten: 0,
            AgeCategory.Adolescent: 0,
            AgeCategory.YoungAdult: 0,
            AgeCategory.SeniorAdult: 0,
            AgeCategory.Elder: 0,
        },
        "complication_risks": [
            {
                "chance": 15,
                "name": ConditionName.Infected
            }
        ],
        "severity": ConditionSeverity.Medium
    },
}