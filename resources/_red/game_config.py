# _game_config.py - Combined the original `_game_config.json`, `prey_config.json`, and `screen_config.json`
#   in order to reduce load times by removing I/O operations.

from dataclasses import dataclass
from definitions import (
    Biome, GameMode, Herb, FreshkillTactic,
    Rank, Season, SortCats, SortRelationships,
    LanguageCode, LeaderFocus, WarriorFocus, Age,
)

@dataclass
class Settings:
    """ Saves game and Clan settings. """

    # -------------------------------- Game settings --------------------------------- #
    Language: LanguageCode = LanguageCode.English
    TextSize: int = 0 # 0, 1, 2
    Fullscreen: bool = False
    FullscreenScaling: bool = False
    DarkMode: bool = False
    Antialiasing: bool = True
    UseShaders: bool = False
    AllowPatrolGore: bool = False

    VolumeMusic: int = 100
    VolumeSound: int = 100
    VolumeMute: bool = False

    UsePawCursor: bool = False
    UseKeybinds: bool = False

    Discord: bool = False
    AutoUpdate: bool = True
    UpdateShowChangelog: bool = True
    SpecialDates: bool = True
    NewClanRandomRelations: bool = True
    DefaultPronounsTheyThem: bool = False


    # -------------------------------- Clan settings --------------------------------- #
    GameMode: GameMode = GameMode.Unset
    LeaderFocus: LeaderFocus = LeaderFocus.NoFocus
    WarriorFocus: WarriorFocus = WarriorFocus.NoFocus

    # general settings
    AutosaveFiveMoons: bool = False
    AllowDisasterEvents: bool = False
    ShowExactXPNut: bool = False
    AllowHealerPatrolSelect: bool = True
    AllowFading: bool = True
    SaveCompleteFadedCopy: bool = False

    # role settings
    AutoDeputy: bool = False
    GraduateAtOneYear: bool = False
    PermConditionRetirement: bool = False
    RandomlyBecomeMediator: bool = False

    # relation settings
    AllowAffairs: bool = False
    MiracleGays: bool = False
    GayAdoptionRights: bool = True # this shouldn't be True if MiracleGays is
    UnknownSecondParent: bool = False
    RomanceFormerApprentice: bool = False
    RomanceFirstCousin: bool = False

    # freshkill_tactics
    FreshkillTactic: FreshkillTactic = FreshkillTactic.Rank
    RationFreshkill: bool = False

    ShowRelationsDead: bool = False
    ShowRelationsEmpty: bool = False # TODO remove this, now that more cats will exist?
    # FavouriteSubTab: # TODO
    ShowDenLabels: bool = True
    ShowFavouriteHighlight: bool = True
    ShowCampBackground: bool = True
    ShowMoonSeasonWidget: bool = False
SETTINGS: Settings = Settings()

@dataclass
class GameConfig:
    """ Game configuration items. """

    savefile_integrity_checks: bool = True # ["save_load"]["load_integrity_checks"]

    # sorting
    sort_cats: SortCats = SortCats.Rank # ["sorting"]["sort_dead_by_total_age"], ["sorting"]["sort_rank_by_death"]
    sort_rels: SortRelationships = SortRelationships.Total # ["sorting"]["sort_by_rel_total"]

    # fun
    april_fools: bool = False # ["fun"]["april_fools"]
    oops_all_newborns: bool = False # ["fun"]["all_cats_are_newborn"], ["fun"]["newborns_can_roam"],
                                    # ["fun"]["newborns_can_patrol"]
    oops_all_kittens: bool = False
    always_halloween: bool = False # ["fun"]["always_halloween"]
    easter_eggs: bool = False

    # theme
    # TODO where are these used?
    light_mode_bg: tuple = (206, 194, 168)
    dark_mode_bg: tuple = (57, 50, 36)
    fullscreen_bg_light = {
        "vignette_alpha": 10,
        "fade_color": (150, 150, 148),
        "dropshadow_alpha": 30
    }
    fullscreen_bg_dark = {
        "vignette_alpha": 50,
        "fade_color": (100, 100, 100),
        "dropshadow_alpha": 100,
        "mainmenu_tint": (239, 229, 206)
    }
GAME_CONFIG: GameConfig = GameConfig()


@dataclass
class ScreenConfig:
    """ Screen configuration items. """
    pass
SCREEN_CONFIG: ScreenConfig = ScreenConfig()


@dataclass
class CatConfig:
    """
	"cat_generation": { # TODO change this to pelt_generation?
		# TODO - change so they're 1/value, not get_rand_bits(value)
		# base 1/chance that a cat will generate with a permanent condition. gets modified further in code
		"base_permanent_condition": 90,
		# 1 in 2^12 chance that a male cat will be a tortie
		"base_male_tortie": 8192,
		# 1 in 8 chance that a female cat will be a tortie
		"base_female_tortie": 8,
		"wildcard_tortie": 512,
		# 1 in 16 chance that a cat's pelt will directly inherit an attribute of a parent's pelt
		"direct_inheritance": 16,
		# base 1 in 120 chance that a cat will have heterochromia
		"base_heterochromia": 120,
		# base 1 in 2^8 chance that a cat will have vitiligo
		"vit_chance": 256,
		# base 1 in 2^5 chance that a cat will be pointed
		"random_point_chance": 32
	},
	"cat_name_controls": {
		"always_name_after_appearance": False,
		"allow_eye_names": True,
		"comment": [
			"Set always_name_after_appearance to true if you always want cats named after the color of their pelt.",
			"This overrides the chances of it otherwise. If cats can't find a pelt color, they will choose from normal_prefixes",
			"So as not to cause an error - false by default",
			"allow_eye_names allows cats to be named after the color of their eyes - true by default"
		]
	},
    "fading": {
        "age_to_fade": 202,
        "opacity_at_fade": 20,
        "visual_fading_speed": 5
    },
    "cat_ages": {
        "newborn": [0, 0],
        "kitten": [1, 5],
        "adolescent": [6, 11],
        "young adult": [12, 47],
        "adult": [48, 95],
        "senior adult": [96, 119],
        "senior": [120, 300],
        "comment": [
            "These HAVE to be in the correct order: where one ends, the next one begins on the next number.",
            "If you DON'T DO THIS, your game WILL break."
        ]
    },
    "cat_sprites": {
        "sick_sprites": True,
        "comment": "Set this to false to disable sick sprites."
    },
	"outside_ex":{
		"base_adolescent_timeskip_ex":[[2, 10],[4, 5]],
		"base_adult_timeskip_ex":[[4, 12],[6, 7]],
		"base_senior_timeskip_ex":[[3, 9],[3, 4]]
	},
    """

    apprentice_age_moons: int = 6
    warrior_age_moons: int = 12
    elder_age_moons: int = 120 # cats will start checking if they want to retire at this age
    elder_age_retirement_chance: int = 24   # once per moon, cats over the age above will have a
                                            # 1/elder_age_retirement_chance chance to retire

    # timeskips
    base_timeskip_xp_gain_rank = {
        # Clan cats who work
        Rank.WarriorApp: (4, 12),
        Rank.MediatorApp: (3, 10),
        Rank.HealerApp: (3, 7),
        Rank.Warrior: (2, 7),
        Rank.Mediator: (2, 7),
        Rank.Healer: (2, 7),
        Rank.Deputy: (2, 7),
        Rank.Leader: (2, 7),
        # Clan cats who don't work
        Rank.Elder: (0, 0),
        Rank.Kit: (0, 0),
        # Outsiders
        Rank.Kittypet: (1, 4),
        Rank.Loner: (4, 10),
        Rank.Rogue: (4, 10)
    }
    base_timeskip_xp_gain_social = (1, 4)

    # generating a random cat
    chance_gender_kits_intersex: int = 100 # 1/100
    chance_gender_align_trans: int = 30 # 1/30
    chance_clairvoyant: int = 200 # 1/200 chance that a cat is clairvoyant
    chance_condition: int = 200 # 1/200 chance that a cat is born with a permanent condition
CAT_CONFIG: CatConfig = CatConfig()


@dataclass
class RelationshipConfig:
    """ """

    max_moon_interactions_player: int = 2 # max_interaction = 5
    max_moon_interactions_special_player: int = 3 # max_interaction_special = 8
    max_moon_interactions_npc: int = 1
    max_moon_interactions_special_npc: int = 2

    mates_max_age_diff: int = 40 # mates.age_range

    """
        "in_decrease_value":{
            "low": 8,
            "medium": 12,
            "high": 16
        },
        "max_interaction": 5,
        "max_interaction_special": 8,
        "compatibility_effect": 5,
        "passive_influence_div": 1.5,
        "chance_for_neutral": 10,
        "chance_of_special_group": 8,
        "chance_romantic_not_mate": 15,
        "influence_condition_events": 20,
        "comment":[
            "chance_for_neutral - how high the chance is to make the interaction of the relationship to a 'neutral' instead of negative or positive",
            "chance_of_special_group - 1/chance often when a group event is happening not all cats are considered, only a special group, which is defined in group_types.json",
            "chance_romantic_not_mate - the base chance of an romantic interaction with another cat, when a cat has a mate",
            "influence_condition_events - how much an event with a condition can influence the relationship"
        ]
	"mates":{
		"chance_fulfilled_condition": 5,
		"chance_friends_to_lovers": 170,
		"confession": {
			"make_confession" : {
				"romantic": 30,
				"platonic": 15,
				"dislike": -15,
				"admiration": 0,
				"comfortable": 10,
				"jealousy": 0,
				"trust": 0
			},
			"accept_confession" : {
				"romantic": 17,
				"platonic": 15,
				"dislike": -10,
				"admiration": 0,
				"comfortable": 10,
				"jealousy": 0,
				"trust": 0
			}
		},
		"mate_condition": {
			"romantic": 20,
			"platonic": 30,
			"dislike": -10,
			"admiration": 0,
			"comfortable": 20,
			"jealousy": 0,
			"trust": 0
		},
		"platonic_to_romantic": {
			"romantic": 0,
			"platonic": 30,
			"dislike": -15,
			"admiration": 0,
			"comfortable": 20,
			"jealousy": 0,
			"trust": 0
		},
		"poly":{
			"current_mate_condition": {
				"romantic": 30,
				"platonic": 0,
				"dislike": 0,
				"admiration": 0,
				"comfortable": 15,
				"jealousy": -15,
				"trust": 25
			},
			"mates_to_each_other": {
				"romantic": 0,
				"platonic": 15,
				"dislike": -10,
				"admiration": 0,
				"comfortable": 15,
				"jealousy": -15,
				"trust": 20
			}
		},
		"comment":[
			"chance_fulfilled_condition - 1/chance of becoming mates when the conditions are fulfilled",
			"chance_friends_to_lovers - 1/chance of becoming mates, triggers with friends_to_lover (has to be a high number because many relationships are checked each moon)",
			"VALUES IN RELATIONSHIP DICT - 0: no condition; positive number: value has to be higher than number; negative number: value has to be lower than number",
			"confession (make_confession) - if one cat has these feelings for another, they confess (if there are more, the highest romantic will be chosen)",
			"confession (confess_acceptance) - if these conditions are fulfilled by the opposite cat, they accept, otherwise, they reject.",
			"conditions for mates - both relationships have to fulfill this condition",
			"poly (current_mate) - which conditions all current mate relationships has to have towards the main cat + vise versa",
            "poly (each_other) - which conditions all current mate relationships has to have towards the new possible mate + vise versa"
		]
	},
	"new_cat": {
		"parent_buff": {
			"kit_to_parent": {
				"romantic": 0,
				"platonic": 40,
				"dislike": 0,
				"admiration": 30,
				"comfortable": 40,
				"jealousy": 0,
				"trust": 50
			},
			"parent_to_kit": {
				"romantic": 0,
				"platonic": 40,
				"dislike": 0,
				"admiration": 30,
				"comfortable": 40,
				"jealousy": 0,
				"trust": 30
			}
		},
		"sib_buff": {
			"cat1_to_cat2": {
				"romantic": 0,
				"platonic": 40,
				"dislike": 0,
				"admiration": 10,
				"comfortable": 40,
				"jealousy": 0,
				"trust": 30
			},
			"cat2_to_cat1": {
				"romantic": 0,
				"platonic": 40,
				"dislike": 0,
				"admiration": 10,
				"comfortable": 40,
				"jealousy": 0,
				"trust": 30
			}
		},
		"rel_buff":{
			"new_to_clan_cat": {
				"romantic": 0,
				"platonic": 15,
				"dislike": 0,
				"admiration": 10,
				"comfortable": 15,
				"jealousy": 0,
				"trust": 15
			},
			"clan_cat_to_new":{
				"romantic": 0,
				"platonic": 15,
				"dislike": 0,
				"admiration": 5,
				"comfortable": 10,
				"jealousy": 0,
				"trust": 10
			}
		},
		"cat_amount_welcoming": 3
	},
    """
    pass
RELATIONSHIP_CONFIG: RelationshipConfig = RelationshipConfig()


@dataclass
class ClanConfig:
    """ """

    max_interactions_per_cat_per_moon: int = 2
    max_interactions_per_special_cat_per_moon: int = 6
    lock_starting_season: bool = False # forces the season to be locked at the Clan's starting_season # lock_season

    # TODO make becoming a mediator or healer dependent on skills, interest, and personality, not random chance
    # roles: dict = {
    #     "mediator_app_chance": 50,
    #     "base_medicine_app_chance": 41,
    #     "become_mediator_chances": {
    #         "warrior": 5000,
    #         "elder": 400
    #     }
    # }


    # Clan creation
    creation_rerolls: int = 3 # Set this to -1 for it to be infinite


    # Warriors' den focus
    focus_min_duration_moons: int = 3 # focus.duration

    # WarriorFocus.Herb

    # WarriorFocus.Prey - how much a working warrior/deputy/leader/warrior apprentice gathers on timeskip
    prey_warrior: int = 2 # focus.hunting.warrior
    prey_warrior_app: int = 1 # focus.hunting.apprentice

    # WarriorFocus.RR
    rest_and_recover = { # focus.rest and recover.
        "injury_prevent": 4,
        "illness_prevent": 6,
        "outbreak_prevention": 2,
        "moons_earlier_healed": 1,
        "comments": [
            "injury will be roughly prevented for every fourth cat",
            "illness will be roughly prevented for every sixth cat - illness is not as easy preventable as injuries",
            "Every second outbreak will be prevented",
            "moons earlier healed - the moon amount where the cats are earlier healed"
        ]
    }

    # WarriorFocus.Befriend
    befriend_outsiders: int = 5 # focus.outsiders.reputation # Defines how much increase or decrease the reputation is.
    befriend_clans: int = 2 # focus.other clans.relation # Defines how much increase or decrease the relation with other clans is.

    # WarriorFocus.Antagonize
    antagonize_outsiders: int = 5 # focus.outsiders.reputation # Defines how much increase or decrease the reputation is.
    antagnoize_clans: int = 2 # focus.other clans.relation # Defines how much increase or decrease the relation with other clans is.

    # WarriorFocus.Sabotage

    # WarriorFocus.Aid

    # Raiding other Clans should be more dangerous than hoarding is!
    # WarriorFocus.Raid # focus.raid other clans.prey_warrior
    focus_raid_prey_leader: int = 3 # focus.raid other clans.prey_warrior
    focus_raid_prey_deputy: int = 3
    focus_raid_prey_warrior: int = 3
    focus_raid_prey_apprentice: int = 1

    focus_raid_herb_healer: int = 4 # focus.raid other clans.herb_medicine
    focus_raid_herb_apprentice: int = 2

    # 1 in 18 that a fighting Rank will get hurt
    focus_raid_injury_chance_fighting: int = 18 # focus.raid other clans.injury_chance_warrior
    # 1 in 33 that a healer Rank will get hurt
    focus_raid_injury_chance_healing: int = 33 # focus.raid other clans.injury_chance_medicine cat
    # added to the above chances for each additional Clan raided above 1
    #   e.g. if you're raiding 3 Clans, then the chance a warrior will be hurt is (1 + 3 + 3)/18 = 7/18
    focus_raid_injury_add_clan_chance: int = 3 # focus.raid other clans.chance_increase_per_clan
    # likelihood of getting different kinds of injury during raiding
    # NB: current sum of injury weights is 100 - for easier understanding it should stay the same
    focus_raid_injuries: tuple = ( # focus.raid other clans.injuries
        ("claw_wound", 15), # focus.raid other clans.injuries.claw-wound
        ("cat_bite", 15), # focus.raid other clans.injuries.cat bite
        ("torn_pelt", 15), # focus.raid other clans.injuries.torn pelt
        ("torn_ear", 15), # focus.raid other clans.injuries.torn ear
        ("bite_wound", 10), # focus.raid other clans.injuries.bite-wound
        ("sprain", 10), # focus.raid other clans.injuries.
        ("bruises", 7), # focus.raid other clans.injuries.
        ("sore", 6), # focus.raid other clans.injuries.
        ("small_cut", 4), # focus.raid other clans.injuries.small cut
        ("cracked_pads", 3), # focus.raid other clans.injuries.cracked pads
    )
    focus_raid_relation_drop: int = 3 # focus.raid other clans.relation

    # Which ranks raid prey from other Clans?
    focus_raid_prey_ranks: tuple = ( Rank.Leader, Rank.Deputy, Rank.Warrior, Rank.WarriorApp, )
    # How much will each rankle
    focus_raid_herb_ranks: tuple = ( Rank.Healer, Rank.HealerApp, )

    # WarriorFocus.Hoard # focus.hoarding.
    focus_hoard_less_prey: int = 1 # focus.hoarding.prey_warrior
    focus_hoard_less_herb: int = 2 # focus.hoarding.herb_medicine
    # a cat can get EITHER injured OR sick, not both - for simpler distribution (50/50 chance decide which condition will be used)
    focus_hoard_injury_warrior: int = 25 # focus.hoarding.injury_chance_warrior
    focus_hoard_injury_healer: int = 35 # focus.hoarding.injury_chance_medicine cat
    focus_hoard_injuries: tuple = ( # focus.hoarding.injuries
        # current sum of injuries is 100 - for easier understanding it should stay the same
        ("cracked_pads", 15, ), # focus.hoarding.injuries.cracked pads
        ("sore", 15, ), # focus.hoarding.injuries.sore
        ("bruises", 15, ), # focus.hoarding.injuries.bruises
        ("sprain", 12, ), # focus.hoarding.injuries.sprain
        ("small_cut", 10, ), # focus.hoarding.injuries.small cut
        ("torn_pelt", 10, ), # focus.hoarding.injuries.torn pelt
        ("torn_ear", 10, ), # focus.hoarding.injuries.torn ear
        ("claw_wound", 5, ), # focus.hoarding.injuries.claw-wound
        ("bite_wound", 5, ), # focus.hoarding.injuries.bite-wound
        ("cat_bite", 3, ), # focus.hoarding.injuries.cat bite
    )

    focus_hoard_illness_chance: int = 35 # focus.hoarding.illness_chance
    focus_hoard_illnesses: tuple = (
        ("running_nose", 5, ), # focus.hoarding.illnesses.running nose
        ("whitecough", 1, ), # focus.hoarding.illnesses.whitecough
    )

    # Clan resources

    # used in HerbSupply.get_found_herbs()
    # ["clan_resources"]["herbs"]["primary_sense"] = 3
    # ["clan_resources"]["herbs"]["secondary_sense"] = 2
    # ["clan_resources"]["herbs"]["primary_clever"] = 3
    # ["clan_resources"]["herbs"]["secondary_clever"] = 2
CLAN_CONFIG: ClanConfig = ClanConfig()


# TODO should hunt patrol config go in here, rather than in biomes?
@dataclass
class EventConfig:
    """
	"accessory_generation": {
		"base_acc_chance": 150,
		"med_modifier": -80,
		"baby_modifier": -20,
		"elder_modifier": 20,
		"happy_trait_modifier": -30,
		"grumpy_trait_modifier": 30,
		"ceremony_modifier": -20,
		"multiple_acc_modifier": 50
	},
	"transition_related": {
		"base_trans_chance": 256,
		"adolescent_modifier": -128,
		"older_modifier": 256
	},
	"lost_cat": {
		"rejoin_chance": 20
	},
	"patrol_generation": {
		"classic_difficulty_modifier": 1,
		"expanded_difficulty_modifier": 2.5,
		"cruel season_difficulty_modifier": 3,
		"win_stat_cat_modifier": 10,
		"better_stat_modifier": 5,
		"best_stat_modifier": 10,
		"fail_stat_cat_modifier": -15,
		"chance_of_romance_patrol": 16,
		"debug_ensure_patrol_id": None,
		"debug_override_patrol_stat_requirements": False,
		"debug_ensure_patrol_outcome": None,
		"comment": [
			"the Cruel Season difficulty modifier needs to have a space rather than an underscore,",
			"due to how it's written in the save files. So don't try to 'fix' it."
		]
	},
	"event_generation": {
		"debug_ensure_event_id": None
	},
	"graduation": {
		"max_apprentice_age": {
			"medicine cat apprentice": 30,
			"apprentice": 25,
			"mediator apprentice": 25
		},
		"min_graduating_age": 10
	},
	"death_related": {
		"leader_death_chance": 50,
		"classic_death_chance": 500,
		"expanded_death_chance": 350,
		"cruel season_death_chance": 300,
		"war_death_modifier_leader": 95,
		"war_death_modifier": 250,
		"base_random_murder_chance": 25,
		"base_murder_kill_chance": 80,
		"old_age_death_start": 150,
		"old_age_death_curve": 4.5,
		"comment": [
			"old_age_death_curve is a multiplier that affects the chances of cats dying once they are over old_age_death_start moons.",
			"Average life expectancy with default old_age_death_start of 150 moons:",
			"1 = 189 moons, 2 = 178, 3 = 172, 4.5 (default) = 168, 8 = 163, 20 = 158"
		]
	},
	"condition_related": {
		"expanded_illness_chance": 250,
		"cruel season_illness_chance": 200,
		"classic_illness_chance": 500,
		"classic_injury_chance": 450,
		"expanded_injury_chance": 250,
		"cruel season_injury_chance": 150,
		"permanent_condition_chance": 15,
		"war_injury_modifier": 100
	},

	PREY_CONFIG: dict = {
    "hunter_bonus": {"1": 1, "2": 2, "3": 3},
    "hunter_exp_bonus": {
        "untrained": 0.1,
        "trainee": 1,
        "prepared": 2,
        "competent": 3,
        "proficient": 4,
        "skilled": 5,
        "expert": 6,
        "master": 7
    },
    "patrol_weight_adaption": {
        "1_class_bigger_prey_allowed": [15,19],
        "2_class_bigger_prey_allowed": [10,14],
        "3_class_bigger_prey_allowed": [5,9],
        "4_class_bigger_prey_allowed": [0,4]
    },
    "patrol_balance": {
        "comment": [
        "A season array consist of ['very_small', 'small', 'medium', 'large', 'huge']",
            "Numbers are the ratio how likely such a patrol will be used when hunting in this season.",
            "The sum of all ratio should be between 15 or 16.",
            "One common (weight:20) success outcome (ignoring skill + traits) must have these prey type types."
        ],
    },
    "comment": [
        "activate_deaths - activates the whole system, otherwise nutrition status of the cats doesn't have an effect",
        "activate_events - activates if events for freshkill pile are triggered or not",
        "start_amount - defines the amount of prey when a new freshkill-pile is made",
        "The auto parameters are for the prey each moon, each healthy warrior/apprentice will catch an amount of between these two values of prey.",
        "additional_prey - added amount for hunting patrol, to make it easier",
        "base_event_trigger_factor - (will be adapted in code based on clan size) this number will be used to multiply with the amount of prey the Clan needs, if the pile is bigger than this number, prey events will be triggered",
        "hunter_bonus is the factor which is be used to multiply on a hunting patrol.",
        "hunter_exp_bonus is the additional prey which will be added on a hunting patrol."
    ]
}

    """

    # ---------------------------------- timeskips ----------------------------------- #
    # whether events like an eagle stealing from the freshkill pile happen at timeskip
    moon_freshkill_events: bool = True # activate_events
    # how likely a random moon event resulting in a Clan cat's death are
    moon_event_weight_cat_death: int = 1
    # how likely a random moon event resulting in a Clan cat getting injured are
    moon_event_weight_cat_injury: int = 5

    # TODO what is the difference between moon_event_weight_prey_reduce and moon_freshkill_events_base_trigger_factor?
    moon_event_weight_prey_reduce: int = 8
    # how likely events like an eagle stealing for the freshkill pile are at timeship
    moon_freshkill_events_base_trigger_factor: int = 4 # base_event_trigger_factor

    # ----------------------------------- patrols ------------------------------------ #

    # --------------------------------- pregnancies ---------------------------------- #

    mother_birth_cooldown_moons: int = 6
    father_birth_cooldown_moons: int = 0

    """ 
    	"pregnancy": {
		"birth_cooldown": 6,
		"primary_chance_mated": 80,
		"primary_chance_unmated": 130,
		"random_affair_chance": 50,
		"unmated_random_affair_chance": 10,
		"one_kit_possibility": {"young adult": 8, "adult": 9, "senior adult": 10, "senior": 4},
        "two_kit_possibility": {"young adult": 10, "adult": 13, "senior adult": 15, "senior": 3},
        "three_kit_possibility": {"young adult": 17, "adult": 15, "senior adult": 5, "senior": 1},
        "four_kit_possibility": {"young adult": 12, "adult": 8, "senior adult": 2, "senior": 0},
        "five_kit_possibility": {"young adult": 6, "adult": 2, "senior adult": 0, "senior": 0},
		"max_kit_possibility": {"young adult": 2, "adult": 0, "senior adult": 0, "senior": 0},
		"min_kits": 1,
		"max_kits": 6,
		"comment": [
			"primary mated - 1/chance for kits, relationship and other factors will influence this chance",
			"primary unmated - 1/chance for kits, relationship and other factors will influence this chance",
			"The kit number is incremental. It is 1-6 as default so if you change these numbers, you should probably keep this in mind.",
			"As in, your max kits number should probably be 5 more than the min kits number.",
			"But that's not required - just makes more sense that way with how the litters are generated."
		]
	},
	"""

EVENT_CONFIG: EventConfig = EventConfig()


@dataclass
class PreyConfig:
    """ TODO """
    game_start_prey_amount: int = 60 # start_amount
    # if starvation isn't possible, then no matter no hungry cats get, they won't starve
    # TODO should this deactivate the entire system or just leave cats complaining about how starving they are forever?
    starvation_possible: bool = True # activate_death

    # how many moons a piece of freshkill will last before it 'rots' and it discarded
    freshkill_rots_after_moons: int = 4 # TODO change this for the Cruel Season
    # how much prey will warriors automatically catch on timeskips
    moon_auto_catch_prey_warrior = (2, 4) # auto_warrior_prey
    # how much prey will warrior apprentices automatically catch on timeskips
    moon_auto_catch_prey_app = (1, 2) # auto_apprentice_prey

    req_prey_sick_multiplier: int = 1 # condition increase
    req_prey_pregnant_multiplier: int = 1.5 # prey_requirement["queen/pregnant"]

    # hunting
    prey_amount_expanded_mode_modifier: int = 1 # additional_prey
    prey_amount_factor_very_small: float = 0.5
    prey_amount_factor_small: float = 1.0
    prey_amount_factor_medium: float = 1.8
    prey_amount_factor_large: float = 2.4
    prey_amount_factor_huge: float = 3.2

    # nutrition
    nutrition_malnourished_percentage: int = 45
    nutrition_starving_percentage: int = 20
PREY_CONFIG: PreyConfig = PreyConfig()


@dataclass
class RankConfig:
    """ Things to do with cats' ranks. If a configuration option seems like it would fit here and somewhere else, e.g.
    rank prey requirements, it goes here.
    """
    prey_requirement = {
        # Adults who patrol, fight, and hunt need 3
        Rank.Leader: 3,
        Rank.Deputy: 3,
        Rank.Warrior: 3,

        # Other working adults, and apprentices who patrol, fight, and hunt need 2
        Rank.Healer: 2,
        # Rank.Queen: 2,
        Rank.Mediator: 2,
        Rank.WarriorApp: 2,

        # Elders and apprentices who don't patrol, fight, and hunt need 1.5
        Rank.HealerApp: 1.5,
        Rank.MediatorApp: 1.5,
        # Rank.QueenApp: 1.5,
        Rank.Elder: 1.5,

        # Kittens need 0.5
        Rank.Kit: 0.5
    }
RANK_CONFIG: RankConfig = RankConfig()


@dataclass
class BiomeConfig:
    """ Used by patrols and world generation. """

    # random.choices(
    #     population=[amount for amount in list(HuntPreyAmount) if amount is not HuntPreyAmount.Unknown],
    #     weights=BIOME_CONFIG.seasonal_hunt_size_weights[biome][season],
    #     k=1)[0]
    # HuntPreyAmount.VerySmall, HuntPreyAmount.Small, HuntPreyAmount.Medium, HuntPreyAmount.Large, HuntPreyAmount.Huge
    seasonal_hunt_size_weights = {
        Biome.Forest: {
            Season.Spring: [2,5,5,2,1],
            Season.Summer: [1,3,6,4,2],
            Season.Autumn: [2,4,5,3,1],
            Season.Winter: [3,6,4,2,0]
        },
        Biome.Mountain: {
            Season.Spring: [2,5,5,2,1],
            Season.Summer: [1,3,6,4,2],
            Season.Autumn: [2,6,4,2,1],
            Season.Winter: [3,6,4,2,0]
        },
        Biome.Plains: {
            Season.Spring: [2,5,5,2,1],
            Season.Summer: [1,3,6,4,2],
            Season.Autumn: [2,4,5,3,1],
            Season.Winter: [3,6,4,2,0]
        },
        Biome.Beach: {
            Season.Spring: [2,5,5,2,1],
            Season.Summer: [2,5,5,2,1],
            Season.Autumn: [2,5,5,2,1],
            Season.Winter: [2,6,4,2,1]
        },
        Biome.Wetlands: {
            Season.Spring: [2,5,5,2,1],
            Season.Summer: [2,5,5,2,1],
            Season.Autumn: [2,5,5,2,1],
            Season.Winter: [2,6,4,2,1]
        },
        Biome.Desert: {
            Season.Spring: [2,6,4,2,1],
            Season.Summer: [3,6,4,2,0],
            Season.Autumn: [2,5,5,2,1],
            Season.Winter: [1,3,6,4,2]
        },
        Biome.Twolegplace: { NotImplementedError("BiomeConfig.seasonal_hunt_size_weights.(Biome.Twolegplace)"), },
    }

    # season_herb_weights_items = BIOME_CONFIG.seasonal_herb_weights.items()
    # random.choices(
    #     population=[pair[0] for pair in season_herb_weights_items],
    #     weights=[pair[1] for pair in season_herb_weights_items],
    #     k=1)[0]
    seasonal_herb_size_weights = {
        Biome.Forest: {
            Season.Spring: [2, 3, 2],
            Season.Summer: [1, 2, 3],
            Season.Autumn: [2, 3, 2],
            Season.Winter: [5, 2, 1]
        },
        Biome.Mountain: {
            Season.Spring: [2, 3, 2],
            Season.Summer: [1, 2, 3],
            Season.Autumn: [2, 3, 2],
            Season.Winter: [5, 2, 1]
        },
        Biome.Plains: {
            Season.Spring: [2, 3, 2],
            Season.Summer: [1, 2, 3],
            Season.Autumn: [2, 3, 2],
            Season.Winter: [5, 2, 1]
        },
        Biome.Beach: {
            Season.Spring: [2, 3, 2],
            Season.Summer: [1, 2, 3],
            Season.Autumn: [2, 3, 2],
            Season.Winter: [5, 2, 1]
        },
        Biome.Desert: {
            Season.Spring: [2, 3, 2],
            Season.Summer: [1, 2, 3],
            Season.Autumn: [2, 3, 2],
            Season.Winter: [5, 2, 1]
        },
        Biome.Wetlands: {
            Season.Spring: [2, 3, 2],
            Season.Summer: [1, 2, 3],
            Season.Autumn: [2, 3, 2],
            Season.Winter: [5, 2, 1]
        },
        Biome.Twolegplace: {}
    }
    seasonal_herb_weights = {
        Biome.Forest: {
            Season.Spring: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            },
            Season.Summer: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            },
            Season.Autumn: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            },
            Season.Winter: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            }
        },
        Biome.Mountain: {
            Season.Spring: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            },
            Season.Summer: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            },
            Season.Autumn: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            },
            Season.Winter: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            }
        },
        Biome.Plains: {
            Season.Spring: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            },
            Season.Summer: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            },
            Season.Autumn: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            },
            Season.Winter: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            }
        },
        Biome.Beach: {
            Season.Spring: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            },
            Season.Summer: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            },
            Season.Autumn: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            },
            Season.Winter: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            }
        },
        Biome.Desert: {
            Season.Spring: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            },
            Season.Summer: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            },
            Season.Autumn: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            },
            Season.Winter: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            }
        },
        Biome.Wetlands: {
            Season.Spring: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            },
            Season.Summer: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            },
            Season.Autumn: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            },
            Season.Winter: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            }
        },
        Biome.Twolegplace: {
            Season.Spring: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            },
            Season.Summer: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            },
            Season.Autumn: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            },
            Season.Winter: {
                Herb.ElderLeaf: 1,
                Herb.Cobweb: 1,
                Herb.Daisy: 1,
                Herb.Horsetail: 1,
                Herb.JuniperBerry: 1,
                Herb.Lungwort: 1,
                Herb.Mallow: 1,
                Herb.Marigold: 1,
                Herb.Moss: 1,
                Herb.OakLeaf: 1,
                Herb.Ragwort: 1,
                Herb.RaspberryLeaf: 1,
                Herb.Tansy: 1,
                Herb.Thyme: 1,
                Herb.WildGarlic: 1,
                Herb.Dandelion: 1,
                Herb.Mullein: 1,
                Herb.Rosemary: 1,
                Herb.Burdock: 1,
                Herb.BlackberryLeaf: 1,
                Herb.Betony: 1,
                Herb.Goldenrod: 1,
                Herb.Poppy: 1,
                Herb.Plantain: 1,
                Herb.Catmint: 1
            }
        }
    }

    # Clan resources

    # used in HerbSupply.get_found_herbs()
    # ["clan_resources"]["herbs"]["primary_sense"] = 3
    # ["clan_resources"]["herbs"]["secondary_sense"] = 2
    # ["clan_resources"]["herbs"]["primary_clever"] = 3
    # ["clan_resources"]["herbs"]["secondary_clever"] = 2

    """
    "clan_resources": {
        "herbs": {
            "comment": "Clan size * required_herbs_per_cat / adequate number will determine adequate supply qualifier. Clan size * required_herbs_per_cat * excess number will determine excess supply qualifier",
            "required_herbs_per_cat": 2,
            "adequate": 2,
            "excess": 2,
            "base_mortality_effect": 3,
            "base_duration_effect": 1,
            "base_risk_effect": 3,
            "general_amount_bonus": 2,
            Biome.Forest: {
                Season.Spring: [2, 3, 2],
                Season.Summer: [1, 2, 3],
                Season.Autumn: [2, 3, 2],
                Season.Winter: [5, 2, 1]
            },
            "mountainous": {
                Season.Spring: [2, 3, 2],
                Season.Summer: [1, 2, 3],
                Season.Autumn: [2, 3, 2],
                Season.Winter: [5, 2, 1]
            },
            "plains": {
                Season.Spring: [2, 3, 2],
                Season.Summer: [1, 2, 3],
                Season.Autumn: [2, 3, 2],
                Season.Winter: [5, 2, 1]
            },
            "beach": {
                Season.Spring: [2, 3, 2],
                Season.Summer: [1, 2, 3],
                Season.Autumn: [2, 3, 2],
                Season.Winter: [5, 2, 1]
            },
            "desert": {
                Season.Spring: [2, 3, 2],
                Season.Summer: [1, 2, 3],
                Season.Autumn: [2, 3, 2],
                Season.Winter: [5, 2, 1]
            },
            "wetlands": {
                Season.Spring: [2, 3, 2],
                Season.Summer: [1, 2, 3],
                Season.Autumn: [2, 3, 2],
                Season.Winter: [5, 2, 1]
            }
        }
    }
    """
BIOME_CONFIG: BiomeConfig = BiomeConfig()

@dataclass
class WarConfig:
    """ Configuration for when Clans are at war. """
