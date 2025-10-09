# definitions.py - Variables that will be used all over the project (globals) are put here to avoid inconsistencies.
# GNU Terry Pratchett

# -------------------------------------------------------------------------------- #
# ----------------------------------------

# Resources directory is in resources/resource_dir.py

########################################################################################################################
# Imports
########################################################################################################################

import logging
from dataclasses import dataclass
from enum import Enum, IntEnum, StrEnum, auto

# !!!!!!!!!!!!!!!!!!! DO NOT IMPORT ANYTHING FROM THIS PROJECT !!!!!!!!!!!!!!!!!!! #

########################################################################################################################
# Constants and Paths
########################################################################################################################

# NB: if you're adding a chance for something to happen, please use an integer value out of 100 (2% is 2, not 0.02)

APP_NAME_DEFAULT: str = "ClanSim"
APP_NAME_LONG: str = "Clan Simulator"
APP_NAME_BETA: str = "ClanSimBeta"
APP_AUTHOR: str = "ClanSim"

TIMESTR_FORMAT: str = "%Y%m%d_%H%M%S"

# this is saved in the Clan save-file, and is used for save-file conversion
SAVE_CLANSIM_VERSION_NUMBER: int = 1
VERSION_CLANSIM_NUMBER: str = "0.1.0"
SAVE_CLANGEN_VERSION_NUMBER: int = 3
VERSION_CLANGEN_NUMBER: str = "0.9.0"

# Decision and Interaction Keys
INTERACTION_NEGATIVE: str = "negative_interaction"
INTERACTION_POSITIVE: str = "positive_interaction"

# Location Keys
# TODO replace these
LOC_STARCLAN: str = "starclan" # TODO Location.StarClan
LOC_DARK_FOREST: str = "hell" # TODO Location.DarkForest
LOC_DEAD_OTHER: str = "UR"  # unknown residence # TODO Location.UnknownAfterlife
LOC_NOT_CLAN: str = "outside" # TODO LocationCategory.Outsiders
LOC_CLAN: str = "inside" # TODO LocationCategory.InsideClan
DEAD_LOCATIONS: list[str] = [LOC_STARCLAN, LOC_DARK_FOREST, LOC_DEAD_OTHER] # TODO LocationCategory.Afterlife


# ----------------------------- Warrior Clans values ----------------------------- #

# How long does freshkill last until it needs to be removed from the freshkill pile?
# TODO make this a lower number for the Cruel Season
FRESHKILL_ROTS_AT_MOONS: int = 4
REQUIRED_HEALERS_PER_CAT: dict = {}
OUTSIDER_CLAN_PREFIX: str = "_outsider_" # TODO make sure this can't be chosen as the player's Clan name

# --------------------------------- Screen names --------------------------------- #

# TODO replace referrences to the below with the ScreenName class
MAIN_MENU_SCREEN_NAME: str = "main menu screen"
MAIN_SETTINGS_SCREEN_NAME: str = "main settings screen"
NEW_CLAN_SCREEN_NAME: str = "new clan screen"
SWITCH_CLAN_SCREEN_NAME: str = "switch clan screen"

PROFILE_SCREEN_NAME: str = "profile screen"
PROFILE_ADOPT_SCREEN_NAME: str = "choose adoptive parent screen"
PROFILE_CEREMONY_SCREEN_NAME: str = ""
PROFILE_FAMILY_SCREEN_NAME: str = ""
PROFILE_GENDER_SCREEN_NAME: str = ""
PROFILE_MATE_SCREEN_NAME: str = ""
PROFILE_MEDIATION_SCREEN_NAME: str = ""
PROFILE_MENTOR_SCREEN_NAME: str = ""
PROFILE_RELATIONSHIPS_SCREEN_NAME: str = ""
PROFILE_ROLE_SCREEN_NAME: str = ""
PROFILE_SPRITE_INSPECT_SCREEN_NAME: str = ""

CLAN_ALLEGIANCES_SCREEN_NAME: str = "allegiances screen"
CLAN_CAMP_SCREEN_NAME: str = ""
CLAN_FRESHKILL_SCREEN_NAME: str = ""
CLAN_EVENTS_SCREEN_NAME: str = ""
CLAN_MEMBERS_SCREEN_NAME: str = ""
CLAN_PATROL_SCREEN_NAME: str = ""
CLAN_SETTINGS_SCREEN_NAME: str = ""

MED_DEN_SCREEN_NAME: str = ""
LEADER_DEN_SCREEN_NAME: str = ""
WARRIOR_DEN_SCREEN_NAME: str = ""

CREATION_SCREENS_KEY: str = "creation screens"
CREATION_SCREENS = [NEW_CLAN_SCREEN_NAME]
MAIN_MENU_SCREENS_KEY: str = "menu screens"
MAIN_MENU_SCREENS = [MAIN_SETTINGS_SCREEN_NAME, MAIN_MENU_SCREEN_NAME, SWITCH_CLAN_SCREEN_NAME]

SPRITE_RANGES: dict[str: tuple[int, int]] = {
    'sprite_newborn': (20, 20),
    'sprite_kit': (0, 2),
    'sprite_adolescent': (3, 5),
    'sprite_young_sick': (19, 19),  # sprite_sick_young
    'sprite_young_para': (17, 17),  # sprite_para_young
    'sprite_adult_long': (6, 8),  # also sprite_young_adult, sprite_senior_adult, sprite_adult
    'sprite_adult_short_med': (9, 11),  # also sprite_young_adult, sprite_senior_adult, sprite_adult
    'sprite_adult_sick': (18, 18),  # sprite_sick_adult
    'sprite_adult_long_para': (16, 16),  # sprite_para_adult
    'sprite_adult_short_med_para': (15, 15),  # sprite_para_adult
    'sprite_elder': (12, 14)
}

VITILIGO_CHANCE_MODIFIER_PER_PARENT: int = 1
POINT_CHANCE_MODIFIER_PER_PARENT: int = 1
HETEROCHROMIA_CHANCE_MODIFIER_PER_PARENT: int = 1


# ------------------------------------- Paths ------------------------------------ #

# settings paths - these are in saves/
CURRENTCLAN_FILENAME: str = "currentclan.txt"
GAME_SETTINGS_FILENAME: str = "settings.yaml"
SAVE_CLAN_DETAILS_FILENAME: str = "*Clan.yaml" # replaces * with Clan prefix

# save paths - these are in saves/{clan_prefix}/
SAVE_CAMP_FILENAME: str = "camp.yaml"
SAVE_CLAN_SETTINGS_FILENAME: str = "clan_settings.yaml"
SAVE_CONDITIONS_FILENAME: str = "conditions.yaml"
SAVE_RELATIONSHIPS_FILENAME: str = "relationships.yaml"
SAVE_CURRENT_MOON_EVENTS_FILENAME: str = "current_moon_events.yaml"
ONGOING_EVENTS_DIR: str = "ongoing_events/"
ONGOING_EVENTS_FILENAME: str = "*_moons.yaml" # replaces * with number of moons until the event
CLAN_CATS_DIR: str = "cats/"
FADED_CATS_INFO_FILENAME: str = "faded_cats_info_copy.txt"

# resource paths
MUSIC_PATH: str = "resources/audio/music/"
SOUNDS_PATH: str = "resources/audio/sounds/"
CONVERSION_DICT_PATH: str = "resources/dicts/conversion_dict.json"

IMAGE_RESOURCES_PATH = "resources/images/"
PATROL_IMAGE_PATH: str = "resources/images/patrol_art/"
BACKGROUNDS_PATH: str = "resources/images/backgrounds/"

# starting at resources/lang/{language code}/
PATROL_LANG_PATH: str = "patrols/"


########################################################################################################################
# Enums
########################################################################################################################

# -------------------------------------------------------------------------------- #

# ---------------------------------- Game enums ---------------------------------- #

class Environment(StrEnum):
    """ Enum for different environments in which to run the game. """

    Codespace = "github codespace"
    SourceCode = "source code"
    Executable = "executable"

    @property
    def log_level(self):
        if self is self.Codespace:
            return logging.DEBUG
        if self is self.SourceCode:
            return logging.DEBUG
        if self is self.Executable:
            return logging.INFO

class GameMode(StrEnum):
    """ How difficult the game is. Part of Clan settings. """

    Unset = "null"

    Story = "classic"
    Expanded = "expanded"
    CruelSeason = "cruel season"

    @property
    def num_cats_per_healer(self):
        if self is self.Expanded:
            return 10
        if self is self.CruelSeason:
            return 7
        return -1


class ConvertType(Enum):
    """ Determines which function the ConversionManager will use to convert stuff. """

    Pelt = "pelt"
    ClanCatsJson = "clan_cats.json"
    SaveFile = "save_file"


class LanguageCode(StrEnum):
    """ Codes for implemented languages. """

    Unset = "unset"

    English = "en"
    Espanol = "es"
    Deutch = "de"


class SortCats(Enum):
    """ How to sort cats. """

    Default = "rank"

    Age = "age"
    Rank = "rank"

    # only applies to sorting dead cats
    MoonsDead = "moons dead"

class SortRelationships(Enum):
    """ How to sort relationships. """

    Default = "total"

    Total = "total"
    Age = "age" # how long ago did the two cats meet


# ---------------------------------- World enums --------------------------------- #

class Biome(StrEnum):
    Any = "any"
    Forest = "forest"
    Mountain = "mountainous"
    Plains = "plains"
    Beach = "beach"
    Desert = "desert"
    Wetlands = "wetlands"
    Twolegplace = "twolegplace"

    def biomes(self) -> list[str]:
        return [e for e in self if e != "any"]

    def values(self) -> list[str]:
        return [e for e in self]

    @property
    def implemented_biome(self):
        if self in [self.Forest, self.Mountain, self.Plains, self.Beach]:
            return True
        return False
AVAILABLE_BIOMES: list[str] = [Biome.Forest, Biome.Mountain, Biome.Plains, Biome.Beach]


class Herb(Enum):
    """ Contains all the herbs the cats can find in the game. """

    Any = 0

    Betony = 12
    BlackberryLeaf = 12 # mixed into a poultice to ease the pain of bee stings
    BurdockRoot = 30 # fights infections, when applied topically as a paste it numbs pain. Makes you sick if you eat too much
    Catmint = 12
    Daisy = 12
    Dandelion = 12
    ElderLeaf = 12 # bushes in Forest, Mountain; topical poultice soothes sprains and wrenched muscles
    Goldenrod = 12
    Horsetail = 12
    JuniperBerry = 12 # TODO is this juniper berries for juniper leaves
    Lungwort = 12
    Mallow = 12
    Marigold = 12
    Moss = 24
    Mullein = 12
    OakLeaf = 12
    Plantain = 12
    Poppy = 12
    Ragwort = 12
    RaspberryLeaf = 12
    Rosemary = 12
    Tansy = 12
    Thyme = 12

    # AlderBark = 24 # Forest; found in snowy season; eases toothaches when chewed
    # BirchSap = 24 # cure for yellowcough
    # Borage = 6 # chewed and eaten. Queens produce more and better milk, brings down fevers, soothes bad bellies and tight chests
    # Celandine = 8 # Forest, Plains, Wetland; Crushed into juice and trickled into the eye. Soothes weakened and damaged eyes.
    # ChervilRoot = 30 # Mountains, grows in rocky places; topical fights infections, eaten helps bellyaches and during kitting
    # Cobweb = 24
    # Coltsfoot = 12 # Forest, Mountain, Plains, Wetland, grows best in greenleaf; eases breathing, kittencough, and whitecough
    # Ivy = 24 # used to bind broken bones with sticks
    # WildGarlic = 12

    @property
    def lifetime_moons(self):
        """ How long an herb will last until it goes bad and needs to be replaced, in moons. """
        return int(self.value)


class Season(StrEnum):
    Any = "any"
    Spring = "newleaf"
    Summer = "greenleaf"
    Autumn = "leaffall"
    Winter = "leafbare"
AVAILABLE_SEASONS: list[Season] = [Season.Spring, Season.Summer, Season.Autumn, Season.Winter]
YEAR_SEASONS: list[Season] = [Season.Spring, Season.Spring, Season.Spring,
                              Season.Summer, Season.Summer, Season.Summer,
                              Season.Autumn, Season.Autumn, Season.Autumn,
                              Season.Winter, Season.Winter, Season.Winter]


# ----------------------------------- Cat enums ---------------------------------- #

# TODO should Age be called AgeCategory?
class Age(IntEnum):
    """ Keeps track of a cat's age. """
    Any = auto() # "any"

    Newborn = auto() # "newborn"
    Kitten = auto() # "kitten"
    Adolescent = auto() # "adolescent"
    YoungAdult = auto() # "young adult"
    Adult = auto() # "adult"
    SeniorAdult = auto() # "senior adult"
    Senior = auto() # "senior"

    @property
    def is_baby(self):
        return self < self.Adolescent

    @property
    def is_adult(self):
        return self > self.Adolescent


class ConditionCategory(Enum):
    """ Categories for the Condition enum. """

    Pregnancy = "pregnancy"
    Illness = "illness"
    Permanent = "permanent_condition"
    Injury = "injury"

class ConditionSeverity(IntEnum):
    """ How severe a condition is. """

    Minor = auto()
    Major = auto()
    Severe = auto()


class GenderKits(StrEnum):
    Male = "male"  # 1
    Female = "female"
    Intersex = "intersex"

class GenderAlign(StrEnum):
    Male = "tom"  # 1
    Female = "molly"
    NonBinary = "sam"


class LocationCategory(StrEnum):
    """ Categories for the Location enum. """

    Any = "any"
    # the ONLY item in Nowhere is Location.DeadFaded, so that no interactions are ever possible with faded cats
    Nowhere = "faded"

    InsideClan = "inside a warrior Clan"
    OutsideClan = "outside the warrior Clans"
    Afterlife = "dead"

class Location(StrEnum):
    """ Keeps track of a cat's physical position in the world. """

    Any = "any"

    ClanWarrior = "warrior's den in camp"
    ClanHealer = "healer's den in camp"
    ClanApprentice = "apprentice's den in camp"
    ClanNursery = "nursery den in camp"
    ClanElder = "elder's den in camp"
    ClanLeader = "leader's den in camp"
    ClanOther = "somewhere in camp"

    # Outside of the Clans
    LeftClan = "former Clancat"
    Exiled = "exiled"
    DrivenAway = "driven away"
    Lost = "lost"
    TwolegNest = "Twoleg nest"
    Wilderness = "wilderness"
    Wandering = "wandering"

    # Dead cats
    StarClan = "starclan"  # used in text_handler.TextHandler.handle_text_content_event
    DarkForest = "darkforest"  # used in text_handler.TextHandler.handle_text_content_event
    OutsiderAfterlife = "unknownresidence"  # used in text_handler.TextHandler.handle_text_content_event
    DeadFaded = "faded"

    @property
    def category(self):
        if self in (self.ClanWarrior, self.ClanApprentice, self.ClanNursery, self.ClanHealer,
                    self.ClanElder, self.ClanOther, ):
            return LocationCategory.InsideClan
        if self in (self.LeftClan, self.Exiled, self.Lost, self.TwolegNest,
                    self.Wilderness, self.Wandering, self.DrivenAway):
            return LocationCategory.OutsideClan
        if self in (self.StarClan, self.DarkForest, self.OutsiderAfterlife, ):
            return LocationCategory.Afterlife
        if self is self.DeadFaded:
            return LocationCategory.Nowhere
        return LocationCategory.Any

    # TODO remove non-faded afterlife locations so the ghost interaction patrol events are with a specific cat?
    @property
    def patrol_interact_possible(self):
        if self in (self.Lost, self.StarClan, self.DarkForest, self.OutsiderAfterlife, self.DeadFaded, self.DrivenAway):
            return False
        return True


class NutritionCategory(IntEnum): # game_config.py < PREY_CONFIG < text_nutrition < lower_range, text
    """ Keeps track of how hungry a cat is. The value is the lower bound of the state.

    For example, if Hungry = 41 and Satiated = 61, A cat with 51 nutrition would be in the Hungry state.
    """

    Unknown = -1

    Starving = 0
    VeryHungry = 21
    Hungry = 41
    Satiated = 61
    Full = 81
    Stuffed = 91


class PersonalityTrait(Enum):
    """ Enum class for different personality aspects. """

    Unknown = "unknown"

    Aggression = "aggression"
    Lawfulness = "lawfulness"
    Sociability = "sociability"
    Stability = "stability"


# Rank needs to be below Age for Rank.appropriate_ages
class Rank(StrEnum):
    """ Keeps track of a cat's social status within or outside a Clan. This can't change after death.

    NB: I thought about adding a Rank.Exiled, since arguably if you're exiled you don't have a
     rank in the Clan anymore. But there are some backstories about being exiled that include
     specific ranks (e.g. ClansOtherExileHighRank) that specify both a rank and exile.
     If said cat joins a new Clan, they might want to keep the same rank (e.g. ClansOtherHealer).
    """

    Any = "any"

    # Non-Clan cats
    Kittypet = "kittypet"
    Loner = "loner"
    Rogue = "rogue"

    # Clan cats
    Leader = "leader"
    Deputy = "deputy"
    Healer = "healer"
    HealerApp = "healer apprentice"
    Mediator = "mediator"
    MediatorApp = "mediator apprentice"
    Warrior = "warrior"
    WarriorApp = "warrior apprentice"

    Kit = "kit"
    Elder = "elder"
    Queen = "queen"
    QueenApp = "queen apprentice"

    @property
    def able(self) -> bool:
        if self in [self.Leader, self.Deputy, self.Warrior, self.Healer, self.Mediator, self.WarriorApp,
                    self.HealerApp, self.MediatorApp]:
            return True
        return False

    @property
    def apprentice(self) -> bool:
        if self in [self.HealerApp, self.MediatorApp, self.WarriorApp]:
            return True
        return False

    @property
    def valid_hunter(self) -> bool:
        if self in [self.Leader, self.Deputy, self.Warrior, self.WarriorApp]:
            return True
        return False

    @property
    def appropriate_ages(self) -> tuple[Age]:
        if self in (self.Any, self.Kittypet, self.Loner, self.Rogue):
            return (Age.Any, )
        if self in (self.Leader, self.Deputy, self.Elder,
                    self.Healer, self.HealerApp,
                    self.Mediator, self.MediatorApp,
                    self.Warrior, self.WarriorApp):
            return tuple(*[a for a in list(Age) if a > Age.Kitten])
        if self is self.Kit:
            return (Age.Newborn, Age.Kitten)
        return (None, )

    @property
    def outsider(self) -> bool:
        if self in (self.Kittypet, self.Loner, self.Rogue, ):
            return True
        return False

    @property
    def default_location(self) -> Location:
        if self is self.Kittypet:
            return Location.TwolegNest
        if self in (self.Loner, self.Rogue, ):
            return Location.Wilderness
        if self in (self.Kit, ): # TODO add self.Queen, self.QueenApp
            return Location.ClanNursery
        if self is self.Elder:
            return Location.ClanElder
        if self in (self.Warrior, self.Deputy, self.Mediator, ):
            return Location.ClanWarrior
        if self in (self.Healer, self.HealerApp, ):
            return Location.ClanHealer
        if self in (self.MediatorApp, self.WarriorApp, ):
            return Location.ClanApprentice
        if self is self.Leader:
            return Location.ClanLeader
        else:
            return Location.Any
# TODO make it so that Rank.Newborn is sorted after Rank.Kit? Or will that happen anyway since it's by age within a Rank?
CLAN_ROLES_RANK_SORT_REVERSE_ORDER: list[Rank] = [  # This in is in reverse order: top of the list at the bottom
    Rank.Elder,  # Elders come last so to make the elders and warriors sections clearer
    Rank.Kit,
    # Rank.QueenApp,
    # Rank.Queen,
    Rank.WarriorApp,
    Rank.Warrior,
    Rank.MediatorApp,
    Rank.Mediator,
    Rank.HealerApp,
    Rank.Healer,
    Rank.Deputy,
    Rank.Leader,
]
CLAN_ROLES_FEEDING_ORDER: list[Rank] = [ # PREY_CONFIG["feeding_order"]
    Rank.Kit,
    # Rank.Queen,
    Rank.Elder,
    Rank.Healer,
    # Rank.QueenApp,
    Rank.HealerApp,
    Rank.WarriorApp,
    Rank.MediatorApp,
    Rank.Warrior,
    Rank.Mediator,
    Rank.Deputy,
    Rank.Leader
]


class RelationshipAspect(StrEnum):
    """ Different components of a relationship. """

    Unknown = "unknown_relationship_aspect"

    Romance = "romance" # romantic_love
    Friendship = "friendship" # platonic_like
    Dislike = "dislike"
    Respect = "respect" # admiration
    Comfort = "comfort" # comfortable
    Jealousy = "jealousy"
    Trust = "trust"


class SkillRank(IntEnum):
    """ TODO """
    Untrained = 0
    Trainee = 5
    Prepared = 10
    Competent = 25
    Proficient = 35
    Adept = 50 # Skilled
    Expert = 65
    Master = 80  # a cat should need to live a longer (or more eventful) life than most to reach this point

class SkillCategory(Enum):
    """ Categories for the Skill enum. """
    Unknown = "unknown"

    Supernatural = "supernatural skills"
    Leadership = "leadership skills" # skills that Clan cats want to see in a leader/deputy specifically
    Warrior = "warrior skills"
    Healer = "healer skills"
    Mediator = "mediator skills"
    Queen = "nursery queen skills"
    Hunting = "hunting skills"
    Movement = "movement skills"
    Social = "social skills"

class RedSkill(Enum):
    """ The skills a cat can develop, in or out of a Clan. """

    Unknown = "unknown"

    # TODO replace StarClan and DarkForest with faith
    StarClan = "starclan"
    DarkForest = "dark_forest"
    Clairvoyance = "future"

    Teaching = "teach"  # mentors
    CampKeeping = "camp"  # warriors
    Fighting = "fight"  # warriors
    Herbalism = "herb"  # healers
    Interpretation = "interpret"  # healers
    Mediation = "mediate"  # mediators
    KitSitting = "queen"  # nursery queens

    Fishing = "fish"  # aquatic prey
    Stalking = "stalk"  # rodent prey - mice, voles, etc.
    Ambushing = "ambush"  # small bird prey and rabbits
    Scavenging = "scavenge"  # Twoleg food
    Swimming = "swim"  # hunt: fishing     border: beach, wetlands
    Running = "run"  # hunt: stalking    border: plains, desert
    Climbing = "climb"  # hunt: ambushing   border: mountain, forest (you climb trees, not just mountains)
    Navigating = "navigate"  # hunt: scavenging  border: Twolegplace

    Comforting = "comfort"  # mediators, nursery queens
    Speaking = "speech" # mediators, Clan relations
    Reasoning = "reason"
    Observation = "observe"
    Storytelling = "story" # telling stories on patrol
    History = "history"

    @property
    def category(self):
        if self in (self.StarClan, self.DarkForest, self.Clairvoyance, ):
            return SkillCategory.Supernatural
        if self in (self.Fighting, self.Mediation, self.Speaking, self.Observation, self.Teaching, ):
            return SkillCategory.Leadership
        if self in (self.Fishing, self.Stalking, self.Ambushing, self.Scavenging,
                    self.Swimming, self.Running, self.Climbing, self.Navigating,
                    self.Fighting, ):
            return SkillCategory.Warrior
        if self in (self.StarClan, self.Clairvoyance, self.Herbalism, self.Interpretation,
                    self.Comforting, self.Observation, self.Reasoning, ):
            return SkillCategory.Healer
        if self in (self.Mediation, self.Comforting, self.Speaking, self.Reasoning, ):
            return SkillCategory.Mediator
        if self in (self.KitSitting, self.Comforting, self.Storytelling, self.Mediation,
                    self.Teaching, ):
            return SkillCategory.Queen
        if self in (self.Fishing, self.Stalking, self.Ambushing, self.Scavenging, ):
            return SkillCategory.Hunting
        if self in (self.Swimming, self.Running, self.Climbing, self.Navigating, ):
            return SkillCategory.Movement
        if self in (self.Comforting, self.Speaking, self.Reasoning, self.Observation,
                    self.Storytelling, self.History, self.Teaching, ):
            return SkillCategory.Social
        return SkillCategory.Unknown

    # Skill.get(self.path, "???")


# ---------------------------------- Clan enums ---------------------------------- #

class CampKey(Enum):
    """ Associates various camps with their reference keys. """

    NoCamp = False

    BeachTidepool = "camp_beach_tidepool"
    BeachTidalCave = "camp_beach_tidal_cave"
    BeachShipwreck = "camp_beach_shipwreck"
    BeachFjord = "camp_beach_fjord"
    ForestClearing = "camp_forest_clearing"
    ForestGully = "camp_forest_gully"
    ForestGrotto = "camp_forest_grotto"
    ForestLakeside = "camp_forest_lakeside"
    MountainCliff = "camp_mountain_cliff"
    MountainCavern = "camp_mountain_cavern"
    MountainCrystalRiver = "camp_mountain_crystal_river"
    MountainRuins = "camp_mountain_ruins"
    PlainsGrassland = "camp_plains_grassland"
    PlainsTunnel = "camp_plains_tunnel"
    PlainsWaste = "camp_plains_waste"

    def get_bg_path(self, season: Season, theme: str):
        if theme in ("dark", "light"):
            return f"{BACKGROUNDS_PATH}camps/{season.value}/{self.value}_{theme}.png"
        raise ValueError(f"Unrecognized theme: {theme}")

    def get_den_positions(self):
        """ Get positions where the den labels on the camp background. """
        pass

    def get_cat_positions(self):
        """ Get positions where cats can appear on the camp background. """
        pass


class LeaderFocus(Enum):
    """ Options for what the leader in a Clan can focus on. """

    NoFocus = "no leader focus"
    Provoke = "provoke Clan"
    Befriend = "befriend Clan"
    HuntDown = "hunt down" # FIXME make it more obvious this involves killing the cat in question
    DriveOff = "drive off"
    InviteIn = "invite in" # same as SearchFor


class WarriorFocus(Enum):
    """ Options for what the warriors and warrior apprentices in a Clan can focus on. """

    NoFocus = "business as usual"

    Herb = "herb"
    Prey = "prey"
    RR = "rest and recover"
    # since outsiders are treated as a Clan now, they're covered by Befriend and Antagonize
    Befriend = "befriend"
    Antagonize = "antagonize"
    Sabotage = "sabotage"
    Aid = "aid"
    Raid = "raid"
    Hoard = "hoard"


class FreshkillTactic(Enum):
    """ The different ways to prioritize who gets freshkill first. """

    Default = "status"

    Rank = "status"
    Youth = "youth"
    # TODO what's the difference between Nutrition and Hunger?
    Nutrition = "nutrition"
    Hunger = "hunger"
    Condition = "condition"
    Exp = "experience"


# ---------------------------------- Event enums --------------------------------- #

class EventCategory(StrEnum):
    """ Categories for events. Correspond to the lower base classes (e.g. MoonEvent). """

    Unknown = "unknown"

    History = "HistoryEvent"
    Moon = "MoonEvent"
    Patrol = "PatrolEvent"

class Event(StrEnum):
    """ Specific event classes. """

    Unknown = "unknown"

    # History events
    Birth = "birth"
    Death = "death"
    ClanChange = "Clan change"
    RankChange = "rank change"
    MentorChange = "mentor change"
    Disaster = "disaster"
    LeaderCeremony = "leader ceremony"

    # Moon events
    Pregnancy = "pregnancy"
    LeaderDenEvent = "leader den event"
    WarriorDenEvent = "warrior den event"
    MediationEvent = "mediation event"
    Outbreak = "outbreak"
    RelationshipChange = "relationship change"

    # Patrol events
    BecomeLost = "lost"

    @property
    def category(self):
        if self in (self.Birth, self.Death, self.ClanChange,
                    self.RankChange, self.MentorChange, self.Disaster, self.LeaderCeremony):
            return EventCategory.History
        if self in (self.Pregnancy, self.LeaderDenEvent, self.WarriorDenEvent, self.MediationEvent,
                    self.Outbreak, self.RelationshipChange):
            return EventCategory.Moon
        if self in (self.BecomeLost, ):
            return EventCategory.Patrol
        return EventCategory.Unknown


class BirthType(Enum):
    """ Specifies the circumstances of a cat's creation. """

    Unknown = "unknown"

    Generation = "generation" # e.g. the cats at the beginning of the game, rogues who you run into
    Pregnancy = "pregnancy"
    Foundling = "foundling"


class PatrolType(StrEnum):
    General = "general"  # TODO this should be a category, not a member
    Any = "any"
    Train = "training"
    Border = "border"
    Hunting = "hunting"
    Med = "med"

    @property
    def general(self):
        """ Returns True if called on training, border, or hunting patrols. False otherwise. """
        if self in [self.Train, self.Border, self.Hunting]:
            return True
        return False
GENERAL_PATROLS: list = [PatrolType.Border, PatrolType.Hunting, PatrolType.Train]

class HuntPreyAmount(Enum):
    """ Defines how much prey is caught for varying patrol success levels """

    Unknown = -1

    VerySmall = 0.5
    Small = 1.0
    Medium = 1.8
    Large = 2.4
    Huge = 3.2


# --------------------------------- Screen names --------------------------------- #

class ScreenCategory(StrEnum):

    Any = "any"

    MainMenu = "main menu" # "menu screens"
    Creation = "creation screens" # "creation screens"

class ScreenName(StrEnum):

    Unknown = ""

    MainMenu = "main_menu" # "main menu screen"
    MainSettings = "main_settings_screen" # "main settings screen"
    NewClan = "new_clan" # "new clan screen"
    SwitchClan = "switch_clan" # "switch clan screen"

    # profile screens
    Profile = "profile" # "profile screen"
    AdoptiveParents = "adoptive_parents" # "choose adoptive parent screen"
    LeaderCeremony = "leader_ceremony" # "leader ceremony screen"
    FamilyTree = "family_tree" # "family tree screen"
    SpecifyGender = "specify_gender" # "change gender screen"
    ChooseMate = "choose_mate" # "choose mate screen"
    Mediation = "mediation" # "mediation screen"
    ChooseMentor = "choose_mentor" # "choose mentor screen"
    SeeRelationships = "see_relationships" # "relationship screen"
    ManageRoles = "manage_roles" # "role screen"
    InspectSprite = "inspect_sprite" # "sprite inspect screen" # TODO give hover text

    Events = "events" # "events screen"
    Camp = "camp"# "camp screen"
    CatList = "cat_list" # "members screen"
    Patrol = "patrol" # "patrol screen"
    Allegiances = "allegiances" # "allegiances screen"
    ClanSettings = "clan_settings" # "clan settings screen"

    LeaderDen = "leader_den" # "leader den screen"
    HealerCatDen = "healer_cat_den" # "med den screen"
    WarriorsDen = "warriors_den" # "warrior den screen"
    Clearing = "clearing" # "fresh-kill pile screen"

    @property
    def category(self):
        if self in (self.NewClan, ):
            return ScreenCategory.Creation
        if self in (self.MainMenu, self.MainSettings, self.SwitchClan, ):
            return ScreenCategory.MainMenu
        return ScreenCategory.Any


# ------------------------------- Pelts and sprites ------------------------------ #
"""
How likely is a category to be inherited from a parent?
PeltPatternCategory.genetic inheritance is called on a striped tabby pelt, then:

For example: you want to know the chance of a cat with PeltPattern.Mackerel
passing on their pelt's pattern to their kits. You would access
 PeltPattern.Mackerel.genetic_inheritance, which would give a tuple that
looks like (50,10,5,7) which would mean:
 - 50 weight is added for the kit's pelt to be from the Striped category
 - 10 weight is added for the kit's pelt to be from the Spotted category
 - 5 weight is added for the kit's pelt to be from the Solid category
 - 7 weight is added for the kit's pelt to be from the Exotic category

 The chances for each category and each weight tuple do NOT need to add up to 100; they're
 weights, not percentages.
"""

class SpriteModifier(StrEnum):
    """ TODO """
    GetSick = "use sick sprite"
    FeelBetter = "don't use sick sprite"
    Paralyze = "para"

    StarClan = "starclan"
    DarkForest = "hell"
    UnknownResidence = "UR"
    Faded = "faded"

    GiveAccessory = "give_accessory"
    TakeAccessory = "take_accessory"

    AgeChange = "age_change"


class PeltPatternCategory(Enum):
    """ Weights for each pattern group. It goes: (striped, spotted, solid, exotic) """
    Striped = [50, 10, 5, 7]
    Spotted = [10, 50, 5, 5]
    Solid = [5, 5, 50, 0]
    Exotic = [15, 15, 1, 45]
    Random = [35, 20, 30, 15]

    @property
    def genetic_inheritance(self):
        return self.value

    def get_order(self) -> list:
        return [self.Striped, self.Spotted, self.Solid, self.Exotic]

# TODO make this an IntEnum with the value equal to the location on the sprite sheet
class PeltPattern(StrEnum):
    """ Codes for pelt patterns. Layer 1 in sprites. """
    SingleColour = "single_solid"
    Tabby = "tabby"
    Marbled = "marbled"
    Rosette = "rosette"
    Smoke = "smoke"
    Ticked = "ticked"
    Speckled = "speckled"
    Bengal = "bengal"
    Mackerel = "mackerel"
    Classic = "classic"
    Sokoke = "sokoke"
    Agouti = "agouti"
    SingleStripe = "single_stripe"
    Masked = "masked"

    @property
    def category(self):
        if self in [self.Tabby, self.Ticked, self.Mackerel, self.Classic, self.Sokoke, self.Agouti]:
            return PeltPatternCategory.Striped
        if self in [self.Speckled, self.Rosette]:
            return PeltPatternCategory.Spotted
        if self in [self.SingleColour, self.Smoke, self.SingleStripe]:
            return PeltPatternCategory.Solid
        if self in [self.Bengal, self.Marbled, self.Masked]:
            return PeltPatternCategory.Exotic
        return PeltPatternCategory.Random

    @property
    def genetic_inheritance(self):
        return self.category.genetic_inheritance

# TODO make this an IntEnum with the value equal to the location on the sprite sheet
class TortiePattern(Enum):
    """ Tortie pelt patterns. Layer 2 in sprites. """

    One = "ONE"
    Two = "TWO"
    Three = "THREE"
    Four = "FOUR"
    Redtail = "REDTAIL"
    Delilah = "DELILAH"
    MinimalOne = "MINIMALONE"
    MinimalTwo = "MINIMALTWO"
    MinimalThree = "MINIMALTHREE"
    MinimalFour = "MINIMALFOUR"
    Half = "HALF"
    Oreo = "OREO"
    Swoop = "SWOOP"
    Mottled = "MOTTLED"
    SideMask = "SIDEMASK"
    EyeDot = "EYEDOT"
    Bandana = "BANDANA"
    PacMan = "PACMAN"
    Streamstrike = "STREAMSTRIKE"
    Oriole = "ORIOLE"
    Chimera = "CHIMERA"
    Daub = "DAUB"
    Ember = "EMBER"
    Blanket = "BLANKET"
    Robin = "ROBIN"
    Brindle = "BRINDLE"
    Paige = "PAIGE"
    Rosetail = "ROSETAIL"
    Safi = "SAFI"
    Smudged = "SMUDGED"
    Dapplenight = "DAPPLENIGHT"
    Streak = "STREAK"
    Mask = "MASK"
    Chest = "CHEST"
    ArmTail = "ARMTAIL"
    Smoke = "SMOKE"
    GrumpyFace = "GRUMPYFACE"
    Brie = "BRIE"
    Beloved = "BELOVED"
    Body = "BODY"
    Shiloh = "SHILOH"
    Freckled = "FRECKLED"
    Heartbeat = "HEARTBEAT"


class PeltColourCategory(Enum):
    """ Weights for each colour group. It goes: (ginger_colours, black_colours, white_colours, brown_colours) """
    Ginger = [40, 0, 0, 10]
    Black = [0, 40, 2, 5]
    White = [0, 5, 40, 0]
    Brown = [10, 5, 0, 35]
    Random = [40, 40, 40, 40]

    @property
    def genetic_inheritance(self):
        return self.value

    def get_order(self) -> list:
        return [self.Ginger, self.Black, self.White, self.Brown]

# TODO make this an IntEnum with the value equal to the location on the sprite sheet
class PeltColour(Enum):
    """ Codes for pelt base colours. Layer 1 in sprites. """

    White = "WHITE"
    PaleGrey = "PALEGREY"
    Silver = "SILVER"
    Grey = "GREY"
    DarkGrey = "DARKGREY"
    Ghost = "GHOST"
    Black = "BLACK"

    Cream = "CREAM"
    PaleGinger = "PALEGINGER"
    Golden = "GOLDEN"
    Ginger = "GINGER"
    DarkGinger = "DARKGINGER"
    Sienna = "SIENNA"

    LightBrown = "LIGHTBROWN"
    Lilac = "LILAC"
    Brown = "BROWN"
    GoldenBrown = "GOLDEN-BROWN"
    DarkBrown = "DARKBROWN"
    Chocolate = "CHOCOLATE"

    @property
    def category(self):
        if self in [self.Cream, self.PaleGinger, self.Golden, self.Ginger, self.DarkGinger, self.Sienna]:
            return PeltColourCategory.Ginger
        if self in [self.Grey, self.DarkGrey, self.Ghost, self.Black]:
            return PeltColourCategory.Black
        if self in [self.White, self.PaleGrey, self.Silver]:
            return PeltColourCategory.White
        if self in [self.LightBrown, self.Lilac, self.Brown, self.GoldenBrown, self.DarkBrown, self.Chocolate]:
            return PeltColourCategory.Brown
        return PeltColourCategory.Random

    @property
    def genetic_inheritance(self):
        return self.category.genetic_inheritance

    @property
    def colour_tints(self):
        """ Which tint colour group a pelt base colour belongs to.

        Everyone can use 'basic' tints, as well as the tints from one of the tint colour groups.
        """
        if self is self.White:  # tint colour group: "white"
            return [ColourTint.Pink, ColourTint.Grey, ColourTint.Red, ColourTint.Orange, ColourTint.NoTint,
                    ColourTint.WarmDilute,
                    ColourTint.Yellow, ]

        elif self.category is PeltColourCategory.White:  # tint colour group: "cool"
            # Note that although the white pelt colours includes White and the "cool" colour group doesn't, because
            #   White was already handled above this it doesn't matter
            return [ColourTint.Pink, ColourTint.Grey, ColourTint.Red, ColourTint.Orange, ColourTint.NoTint,
                    ColourTint.WarmDilute,
                    ColourTint.Purple, ColourTint.Black, ColourTint.Dilute]

        elif self.category is PeltColourCategory.Black:  # tint colour group: "monochrome"
            return [ColourTint.Pink, ColourTint.Grey, ColourTint.Red, ColourTint.Orange, ColourTint.NoTint,
                    ColourTint.WarmDilute,
                    ColourTint.Blue, ColourTint.Black, ColourTint.Dilute, ColourTint.CoolDilute]

        elif (self is self.Sienna) or (self.category is PeltColourCategory.Brown):  # tint colour group: "brown"
            return [ColourTint.Pink, ColourTint.Grey, ColourTint.Red, ColourTint.Orange, ColourTint.NoTint,
                    ColourTint.WarmDilute,
                    ColourTint.Yellow, ColourTint.Purple, ColourTint.Black, ColourTint.Dilute, ColourTint.CoolDilute]

        elif self.category is PeltColourCategory.Ginger:  # tint colour group: "warm"
            # Note that although the white pelt colours includes Sienna and the "warm" colour group doesn't, because
            #   Sienna was already handled above this it doesn't matter
            return [ColourTint.Pink, ColourTint.Grey, ColourTint.Red, ColourTint.Orange, ColourTint.NoTint,
                    ColourTint.WarmDilute,
                    ColourTint.Yellow, ColourTint.Purple, ColourTint.Dilute, ColourTint.CoolDilute]

        return [ColourTint.Pink, ColourTint.Grey, ColourTint.Red, ColourTint.Orange, ColourTint.NoTint,
                ColourTint.WarmDilute]

    @property
    def white_patch_tints(self):
        """ Which tint colour group a pelt base colour belongs to.

        Everyone can use 'basic' tints, as well as the tints from one of the tint colour groups.

        Offwhite is passed twice on purpose! Don't delete the extra. Having it more than once
            makes it more likely to be chosen, which is intentional.
        """
        if self in [self.Grey, self.PaleGrey, self.Silver]:
            return [WhitePatchTint.NoTint, WhitePatchTint.WhitePatchOffwhite, WhitePatchTint.WhitePatchOffwhite,
                    WhitePatchTint.WhitePatchGrey]
        elif self.category is PeltColourCategory.Black:  # white patch tint group = "black"
            # Note that although the "black" colour group includes Grey and the "black" white tint colour group doesn't,
            #   because Grey was already handled above this it doesn't matter.
            return [WhitePatchTint.NoTint, WhitePatchTint.WhitePatchOffwhite, WhitePatchTint.WhitePatchOffwhite,
                    WhitePatchTint.WhitePatchGrey, WhitePatchTint.WhitePatchDarkCream, WhitePatchTint.WhitePatchCream]
        elif self.category is PeltColourCategory.Ginger:  # white patch tint group = "ginger"
            return [WhitePatchTint.NoTint, WhitePatchTint.WhitePatchOffwhite, WhitePatchTint.WhitePatchOffwhite,
                    WhitePatchTint.WhitePatchDarkCream, WhitePatchTint.WhitePatchCream, WhitePatchTint.WhitePatchPink]
        elif self.category is PeltColourCategory.Brown:  # white patch tint group = "brown"
            return [WhitePatchTint.NoTint, WhitePatchTint.WhitePatchOffwhite, WhitePatchTint.WhitePatchOffwhite,
                    WhitePatchTint.WhitePatchDarkCream, WhitePatchTint.WhitePatchCream]
        # white patch tint group = "white", and no white patch tint group
        return [WhitePatchTint.NoTint, WhitePatchTint.WhitePatchOffwhite, WhitePatchTint.WhitePatchOffwhite]

    @property
    def tabby_is_darker(self):
        if self in (self.Ghost, ):
            return False
        return True

class ColourTint(Enum):
    """ RGB values of the tints that base pelts colour can have. Layer 1 in sprites. """

    NoTint = None
    Pink = (253, 237, 237)
    Grey = (225, 225, 225)
    Red = (248, 226, 228)
    Black = (195, 195, 195)
    Orange = (255, 247, 235)
    Yellow = (250, 248, 225)
    Purple = (235, 225, 244)
    Blue = (218, 237, 245)
    Dilute = (20, 20, 20)
    WarmDilute = (25, 15, 7)
    CoolDilute = (7, 15, 25)

    @property
    def dilute(self):
        if self in [self.Dilute, self.WarmDilute, self.CoolDilute, self.NoTint]:
            return True
        return False


class PeltLengthCategory(Enum):
    """ Weights for each pelt length. It goes: (short, medium, long) """
    Short = [50, 10, 2]
    Medium = [25, 50, 25]
    Long = [2, 10, 50]
    Random = [10, 10, 10]

    @property
    def genetic_inheritance(self):
        return self.value

    def get_order(self) -> list:
        return [self.Short, self.Medium, self.Long]

class PeltLength(Enum):
    """ The lengths and textures that pelts can have. Layer 1 in sprites. """

    Short = "short"
    Medium = "medium"
    Long = "long"

    @property
    def category(self):
        if self is self.Short:
            return PeltLengthCategory.Short
        if self is self.Medium:
            return PeltLengthCategory.Medium
        if self is self.Long:
            return PeltLengthCategory.Long
        return PeltLengthCategory.Random

    @property
    def genetic_inheritance(self):
        return self.category.genetic_inheritance


class WhitePatchPatternCategory(Enum):
    """ Weights for each pattern group. It goes: (nowhite,low,mid,high,mostly,full,point,vitiligo)

    If you're not sure which category a white patch pattern should go into:
        low = 1%-25%

    """
    NoWhitePatch = [15, 40, 15, 5, 0, 0, 0, 0]
    Low = [20, 40, 30, 15, 5, 0, 0, 0]  # little_white = [30, 40, 20, 15, 5, 0]
    Mid = [5, 10, 40, 15, 10, 0, 0, 0]  # mid_white = [10, 40, 15, 10, 0]
    High = [0, 15, 20, 40, 10, 1, 0, 0]  # high_white = [15, 20, 40, 10, 1]
    Mostly = [0, 5, 15, 20, 40, 5, 0, 0]  # mostly_white = [5, 15, 20, 40, 5]
    Full = [0, 0, 5, 15, 40, 10, 0, 0]  # full_white = [0, 5, 15, 40, 10]

    Point = [10, 100, 100, 100, 100, 10, 100, 0]  # point
    Vitiligo = [10, 100, 100, 100, 100, 10, 5, 50]  # vit

    Random = [10, 100, 100, 100, 100, 10, 5, 1]  # [10, 10, 10, 10, 1]

    @property
    def genetic_inheritance(self):
        return self.value

    def get_order(self) -> list:
        return [self.NoWhitePatch, self.Low, self.Mid, self.High, self.Mostly, self.Full, self.Point, self.Vitiligo]

# TODO make this an IntEnum with the value equal to the location on the sprite sheet
class WhitePatchPattern(StrEnum):
    """ White patches for pelts.  Layer 3 in sprites. """

    NoWhitePatch = "no white"
    _SendToRandom = "Send to me to WhitePatchPatternCategory.Random, please!"

    FullWhite = "FULLWHITE"
    Wrap = "ANY"
    Tuxedo = "TUXEDO"
    Little = "LITTLE"
    ColourPoint = "COLOURPOINT"
    Coat = "ANYTWO"
    Moon = "MOON"
    Phantom = "PHANTOM"
    Powder = "POWDER"
    Bleached = "BLEACHED"
    FadeSpots = "FADESPOTS"
    Savannah = "SAVANNAH"
    Pebbleshine = "PEBBLESHINE"

    Extra = "EXTRA"
    Oneear = "ONEEAR"
    Broken = "BROKEN"
    LightTuxedo = "LIGHTTUXEDO"
    Ragdoll = "RAGDOLL"
    Vitiligo = "VITILIGO"
    Piebald = "PIEBALD"
    Curved = "CURVED"
    Petal = "PETAL"
    ShibaInu = "SHIBAINU"
    Owl = "OWL"

    Tip = "TIP"
    Fancy = "FANCY"
    Freckles = "FRECKLES"
    RingTail = "RINGTAIL"
    HalfFace = "HALFFACE"
    PantsTwo = "PANTSTWO"
    Goatee = "GOATEE"
    VitiligoTwo = "VITILIGOTWO"
    Paws = "PAWS"
    Mitaine = "MITAINE"
    BrokenBlaze = "BROKENBLAZE"
    Beard = "BEARD"

    Tail = "TAIL"
    Blaze = "BLAZE"
    Bib = "BIB"
    Vee = "VEE"
    Unders = "UNDERS"
    Belly = "BELLY"
    TailTip = "TAILTIP"
    Toes = "TOES"
    TopCover = "TOPCOVER"

    Apron = "APRON"
    CapSaddle = "CAPSADDLE"
    MaskMantle = "MASKMANTLE"
    Star = "STAR"
    ToesTail = "TOESTAIL"
    Pants = "PANTS"
    ReversePants = "REVERSEPANTS"
    Skunk = "SKUNK"
    HalfWhite = "HALFWHITE"
    Appaloosa = "APPALOOSA"

    Heart = "HEART"
    LilTwo = "LILTWO"
    Glass = "GLASS"
    Moorish = "MOORISH"
    SepiaPoint = "SEPIAPOINT"
    MinkPoint = "MINKPOINT"
    SealPoint = "SEALPOINT"
    Mao = "MAO"
    ChestSpeck = "CHESTSPECK"  # TODO is this really Mostly white?
    Wings = "WINGS"
    Painted = "PAINTED"
    HeartTwo = "HEARTTWO"
    WoodPecker = "WOODPECKER"

    Boots = "BOOTS"
    Miss = "MISS"
    Cow = "COW"
    CowTwo = "COWTWO"
    Bub = "BUB"
    BowTie = "BOWTIE"
    Mustache = "MUSTACHE"
    ReverseHeart = "REVERSEHEART"
    Sparrow = "SPARROW"
    Vest = "VEST"
    Sparkle = "SPARKLE"

    RightEar = "RIGHTEAR"
    LeftEar = "LEFTEAR"
    Estrella = "ESTRELLA"
    ShootingStar = "SHOOTINGSTAR"
    EyeSpot = "EYESPOT"
    ReverseEye = "REVERSEEYE"
    FadeBelly = "FADEBELLY"
    Front = "FRONT"
    Pebble = "PEBBLE"
    TailTwo = "TAILTWO"
    BackSpot = "BACKSPOT"
    EyeBags = "EYEBAGS"

    BlazeChestPawsBroken = "FCTWO"
    BlazeChestPawsContinuous = "FCONE"

    Locket = "LOCKET"
    BlazeMask = "BLAZEMASK"
    Tears = "TEARS"
    Van = "VAN"

    # Based on cats in the books
    Buzzardfang = "BUZZARDFANG"
    Lightsong = "LIGHTSONG"
    Blackstar = "BLACKSTAR"
    Ravenpaw = "RAVENPAW"
    Dapplepaw = "DAPPLEPAW"
    Blossomstep = "BLOSSOMSTEP"
    Hawkblaze = "HAWKBLAZE"
    Buddy = "BUDDY"
    Bullseye = "BULLSEYE"
    Buster = "BUSTER"
    Cake = "CAKE"
    Damien = "DAMIEN"
    Digit = "DIGIT"
    Diva = "DIVA"
    Dougie = "DOUGIE"
    Farofa = "FAROFA"
    Finn = "FINN"
    Honey = "HONEY"
    Karpati = "KARPATI"
    Kropka = "KROPKA"
    Lovebug = "LOVEBUG"
    Luna = "LUNA"
    Mia = "MIA"
    Mister = "MISTER"
    Prince = "PRINCE"
    Princess = "PRINCESS"
    Rosina = "ROSINA"
    Sammy = "SAMMY"
    Scar = "SCAR"
    Scourge = "SCOURGE"
    Smokey = "SMOKEY"
    Squeaks = "SQUEAKS"
    Trixie = "TRIXIE"

    @property
    def category(self):
        if self in [self.Little, self.LightTuxedo, self.Buzzardfang, self.Tip, self.Blaze, self.Bib, self.Vee,
                    self.Paws, self.Belly, self.TailTip, self.Toes, self.BrokenBlaze, self.LilTwo, self.Scourge,
                    self.ToesTail, self.Ravenpaw, self.Honey, self.Luna, self.Extra, self.Mustache,
                    self.ReverseHeart, self.Sparkle, self.RightEar, self.LeftEar, self.Estrella, self.ReverseEye,
                    self.BackSpot, self.EyeBags, self.Locket, self.BlazeMask, self.Tears]:
            return WhitePatchPatternCategory.Low
        if self in [self.Tuxedo, self.Fancy, self.Unders, self.Damien, self.Skunk, self.Mitaine, self.Squeaks,
                    self.Star, self.Wings, self.Diva, self.Savannah, self.FadeSpots, self.FadeBelly, self.Beard,
                    self.Dapplepaw, self.TopCover, self.WoodPecker, self.Miss, self.BowTie, self.Vest, self.Digit,
                    self.BlazeChestPawsBroken, self.BlazeChestPawsContinuous, self.Mia, self.Rosina, self.Princess,
                    self.Dougie, ]:
            return WhitePatchPatternCategory.Mid
        if self in [self.Appaloosa, self.Blossomstep, self.Broken, self.Bub, self.Bullseye, self.Buster, self.Cake,
                    self.Coat, self.Curved, self.Farofa, self.Finn, self.Freckles, self.Front, self.Glass, self.Goatee,
                    self.HalfFace, self.HalfWhite, self.Hawkblaze, self.Mister, self.Mao, self.MaskMantle, self.Owl,
                    self.Painted, self.Pants, self.PantsTwo, self.Piebald, self.Prince, self.ReversePants,
                    self.RingTail, self.Sammy, self.Scar, self.ShibaInu, self.Sparrow, self.Trixie, self.Wrap, ]:
            return WhitePatchPatternCategory.High
        if self in [self.Apron, self.Blackstar, self.Boots, self.Cow, self.CowTwo, self.CapSaddle, self.ChestSpeck,
                    self.Buddy, self.EyeSpot, self.Heart, self.HeartTwo, self.Kropka, self.Lightsong, self.Lovebug,
                    self.Moorish, self.Oneear, self.Pebble, self.Pebbleshine, self.Petal, self.ShootingStar,
                    self.Tail, self.TailTwo, self.Van, ]:
            return WhitePatchPatternCategory.Mostly
        if self is WhitePatchPattern.FullWhite:
            return WhitePatchPatternCategory.Full
        if self in [self.ColourPoint, self.MinkPoint, self.Ragdoll, self.SepiaPoint, self.SealPoint]:
            return WhitePatchPatternCategory.Point
        if self in [self.Bleached, self.Karpati, self.Moon, self.Phantom, self.Powder, self.Smokey,
                    self.Vitiligo, self.VitiligoTwo, ]:
            return WhitePatchPatternCategory.Vitiligo
        if self is self._SendToRandom:
            return WhitePatchPatternCategory.Random
        return WhitePatchPatternCategory.Random

    @property
    def genetic_inheritance(self):
        return self.category.genetic_inheritance

class WhitePatchTint(Enum):
    """ RGB values of the tints that white patches can have. Layer 3 in sprites. """

    NoTint = None
    WhitePatchDarkCream = (236, 229, 208)
    WhitePatchCream = (247, 241, 225)
    WhitePatchOffwhite = (238, 249, 252)
    WhitePatchGrey = (208, 225, 229)
    WhitePatchPink = (254, 248, 249)


class EyeColourCategory(Enum):
    """ Weights for each eye colour group. It goes: (yellow, green, blue) """
    Yellow = [50, 20, 0]
    Green = [20, 40, 20]
    Blue = [0, 20, 50]
    Random = [10, 10, 10]

    @property
    def genetic_inheritance(self):
        return self.value

    def get_order(self) -> list:
        return [self.Yellow, self.Green, self.Blue]

# TODO make this an IntEnum with the value equal to the location on the sprite sheet
class EyeColour(StrEnum):
    """ Eye colours for cats. Layer 5 in sprites. """

    Yellow = "yellow"
    Amber = "amber"
    Hazel = "hazel"
    PaleGreen = "pale_green"
    Green = "green"
    Blue = "blue"
    DarkBlue = "dark_blue"
    Grey = "grey"
    Cyan = "cyan"
    Emerald = "emerald"
    HeatherBlue = "heather_blue"
    SunlitIce = "sunlit_ice"
    Copper = "copper"
    Sage = "sage"
    Cobalt = "cobalt"
    PaleBlue = "pale_blue"
    Bronze = "bronze"
    Silver = "silver"
    PaleYellow = "pale_yellow"
    Gold = "gold"
    GreenYellow = "green_yellow"
    Orange = "orange"

    @property
    def category(self):
        if self in [self.Yellow, self.Amber, self.PaleYellow, self.Gold, self.Copper,
                    self.GreenYellow, self.Bronze, self.Silver, self.Orange]:
            return EyeColourCategory.Yellow
        if self in [self.PaleGreen, self.Green, self.Emerald, self.Sage, self.Hazel]:
            return EyeColourCategory.Green
        if self in [self.Blue, self.DarkBlue, self.Cyan, self.PaleBlue,
                    self.HeatherBlue, self.Cobalt, self.SunlitIce, self.Grey]:
            return EyeColourCategory.Blue
        return EyeColourCategory.Random

    @property
    def genetic_inheritance(self):
        return self.category.genetic_inheritance


class SkinColourCategory(Enum):
    """ Weights for each skin colour group. It goes: (cool,warm,brown,marbled) """
    Cool = [25, 15, 10, 5]
    Warm = [10, 25, 15, 5]
    Brown = [10, 15, 25, 5]
    Marbled = [5, 5, 5, 15]
    Random = [15, 15, 15, 15]

    @property
    def genetic_inheritance(self):
        return self.value

    def get_order(self) -> list:
        return [self.Cool, self.Warm, self.Brown, self.Marbled]

class SkinColour(StrEnum):
    """ Layer 7 in sprites. """

    # category = cool
    Black = "black"
    DarkGrey = "dark_grey"
    Grey = "grey"
    DarkBlue = "dark_blue"
    Blue = "blue"
    LightBlue = "light_blue"

    # category = warm
    Pink = "pink"
    DarkSalmon = "dark_salmon"
    Salmon = "salmon"
    Peach = "peach"
    Red = "red"

    # category = brown
    DarkBrown = "dark_brown"
    Brown = "BROWN"
    LightBrown = "light_brown"
    Chocolate = "chocolate"

    # category = marbled
    DarkMarbled = "dark_marbled"
    Marbled = "marbled"
    LightMarbled = "light_marbled"

    @property
    def category(self):
        if self in [self.Black, self.DarkGrey, self.Grey, self.DarkBlue, self.Blue, self.LightBlue]:
            return SkinColourCategory.Cool
        if self in [self.Pink, self.DarkSalmon, self.Salmon, self.Peach, self.Red]:
            return SkinColourCategory.Warm
        if self in [self.DarkBrown, self.Brown, self.LightBrown, self.Chocolate]:
            return SkinColourCategory.Brown
        if self in [self.DarkMarbled, self.Marbled, self.LightMarbled]:
            return SkinColourCategory.Marbled
        return SkinColourCategory.Random.genetic_inheritance

    @property
    def genetic_inheritance(self):
        return self.category.genetic_inheritance


class ScarCategory(Enum):
    """ Categories for each scar cats can get. No weights here, since these happen through events. """

    Normal = "normal"
    SpecialEvent = "special_event"
    Bite = "bite"
    Burn = "burn"
    Frostbite = "frostbite"
    MissingLimb = "missing_limb"

# TODO make this an IntEnum with the value equal to the location on the sprite sheet
class ScarPelt(StrEnum):
    """ Scars cats have on their body. Layer 4 in sprites. """
    # scars from other cats, other animals

    ScratchEye = "a scar over one eye"
    ScratchChest = "ONE"
    ScratchSide = "SCRATCHSIDE"
    ScratchBack = "TWO"
    ScratchBackPaw = "FOUR"

    MangledLeg = "MANLEG"
    MangledTail = "MANTAIL"

    BiteLeg = "LEGBITE"
    BiteNeck = "NECKBITE"
    BiteRat = "RATBITE"
    BiteCatChest = "CATBITE"
    BiteCatLeg = "CATBITETWO"
    Brightheart = "BRIGHTHEART"

    BlindRight = "a blind right eye"
    BlindLeft = "a blind left eye"
    BlindBoth = "blind"

    BeakCheek = "BEAKCHEEK"
    BeakLower = "BEAKLOWER"
    BeakSide = "BEAKSIDE"

    QuillChunkPaw = "QUILLCHUNK"
    QuillScratchCheek = "QUILLSCRATCH"
    QuillScratchSide = "QUILLSIDE"

    Snout = "SNOUT"
    Bridge = "BRIDGE"
    Cheek = "CHEEK"
    Face = "FACE"
    Throat = "THROAT"
    Side = "SIDE"
    Belly = "BELLY"
    HindLeg = "HINDLEG"
    Back = "BACK"
    TailBase = "TAILBASE"
    TailScar = "TAILSCAR"

    # "special" scars that could only happen in a special event
    BurnPaws = "BURNPAWS"
    BurnBelly = "BURNBELLY"
    BurnRump = "BURNRUMP"
    BurnTail = "BURNTAIL"
    FrostFace = "FROSTFACE"
    FrostHindPaw = "FROSTSOCK"
    FrostForePaw = "FROSTMITT"
    FrostTail = "FROSTTAIL"
    SnakeShoulder = "SNAKE"
    SnakeHindLeg = "SNAKETWO"
    Toe = "TOE"
    ToeTrap = "TOETRAP"

    # TODO TornEars
    TornLeftEar = "a torn left ear"
    TornRightEar = "a torn right ear"
    NoLeftEar = "no left ear"
    NoRightEar = "no right ear"
    NoEars = "missing ears"
    NoPaw = "one missing paw"
    NoTail = "no tail"
    HalfTail = "half a tail"

    @property
    def category(self):
        if self in [
            self.ScratchEye, self.ScratchChest, self.ScratchSide, self.ScratchBack, self.ScratchBackPaw,
            self.MangledLeg, self.MangledTail, self.BlindRight, self.BlindLeft, self.BlindBoth,
            self.BiteLeg, self.BiteNeck, self.BiteRat, self.BiteCatChest, self.BiteCatLeg,
            self.Brightheart, self.BeakCheek, self.BeakLower, self.BeakSide,
            self.QuillChunkPaw, self.QuillScratchCheek, self.QuillScratchSide,
            self.Snout, self.Bridge, self.Cheek, self.Face, self.Throat, self.Side,
            self.Belly, self.HindLeg, self.Back, self.TailBase, self.TailScar,
        ]:
            return ScarCategory.Normal
        if self in [self.BurnPaws, self.BurnBelly, self.BurnRump, self.BurnTail,
                    self.FrostFace, self.FrostHindPaw, self.FrostForePaw, self.FrostTail,
                    self.SnakeShoulder, self.SnakeHindLeg, self.Toe, self.ToeTrap]:
            return ScarCategory.SpecialEvent
        if self in [
            self.BiteLeg, self.BiteNeck, self.BiteRat, self.BiteCatLeg, self.BiteCatChest, self.Brightheart
        ]:
            return ScarCategory.Bite
        if self in [self.BurnPaws, self.BurnBelly, self.BurnRump, self.BurnTail]:
            return ScarCategory.Burn
        if self in [self.FrostFace, self.FrostHindPaw, self.FrostForePaw, self.FrostTail]:
            return ScarCategory.Frostbite
        if self in [self.TornLeftEar, self.TornRightEar, self.NoLeftEar, self.NoRightEar,
                    self.NoEars, self.NoPaw, self.NoTail, self.HalfTail]:
            return ScarCategory.MissingLimb
        return None

# Lineart is layer 6 in sprites.

class AccessoryCategory(Enum):
    """ """

    Herb = "healer_herb"
    Wild = "wild"
    Tail = "tail"
    Collar = "collar"
    Head = "head"
    Body = "body"


class PeltAccessories(StrEnum):
    """ Layer 9 in sprites. """

    # Herb accessories
    HerbMapleLeaf = "MAPLE LEAF"
    HerbHolly = "HOLLY"
    HerbBlueberries = "BLUE BERRIES"
    HerbForgetMeNots = "FORGET ME NOTS"
    HerbRyeStalk = "RYE STALK"
    HerbCattail = "CATTAIL"
    HerbPoppy = "POPPY"
    HerbOrangePoppy = "ORANGE POPPY"
    HerbCyanPoppy = "CYAN POPPY"
    HerbWhitePoppy = "WHITE POPPY"
    HerbPinkPoppy = "PINK POPPY"
    HerbBluebells = "BLUEBELLS"
    HerbLilyOfTheValley = "LILY OF THE VALLEY"
    HerbSnapdragon = "SNAPDRAGON"
    HerbHerbs = "HERBS"
    HerbPetals = "PETALS"
    HerbNettle = "NETTLE"
    HerbHeather = "HEATHER"
    HerbGorse = "GORSE"
    HerbJuniper = "JUNIPER"
    HerbRaspberry = "RASPBERRY"
    HerbLavender = "LAVENDER"
    HerbOakLeaves = "OAK LEAVES"
    HerbCatmint = "CATMINT"
    HerbMapleSeed = "MAPLE SEED"
    HerbLaurel = "LAUREL"
    HerbBulbWhite = "BULB WHITE"
    HerbBulbYellow = "BULB YELLOW"
    HerbBulbOrange = "BULB ORANGE"
    HerbBulbPink = "BULB PINK"
    HerbBulbBlue = "BULB BLUE"
    HerbClover = "CLOVER"
    HerbDaisy = "DAISY"
    HerbDryHerbs = "DRY HERBS"
    HerbDryCatmint = "DRY CATMINT"
    HerbDryNettles = "DRY NETTLES"
    HerbDryLaurels = "DRY LAURELS"

    # Wild accessories
    WildRedFeathers = "RED FEATHERS"
    WildBlueFeathers = "BLUE FEATHERS"
    WildJayFeathers = "JAY FEATHERS"
    WildGullFeathers = "GULL FEATHERS"
    WildSparrowFeathers = "SPARROW FEATHERS"
    WildMothWings = "MOTH WINGS"
    WildRosyMothWings = "ROSY MOTH WINGS"
    WildMorphoButterfly = "MORPHO BUTTERFLY"
    WildMonarchButterfly = "MONARCH BUTTERFLY"
    WildCicadaWings = "CICADA WINGS"
    WildBlackCicada = "BLACK CICADA"

    # Tail accessories
    TailRedFeathers = "RED FEATHERS"
    TailBlueFeathers = "BLUE FEATHERS"
    TailJayFeathers = "JAY FEATHERS"
    TailGullFeathers = "GULL FEATHERS"
    TailSparrowFeathers = "SPARROW FEATHERS"
    TailClover = "CLOVER"
    TailDaisy = "DAISY"

    # Collars
    CollarBlack = "BLACK"
    CollarBlackBell = "BLACKBELL"
    CollarBlackBow = "BLACKBOW"
    CollarBlackNylon = "BLACKNYLON"
    CollarBlue = "BLUE"
    CollarBlueBell = "BLUEBELL"
    CollarBlueBow = "BLUEBOW"
    CollarBlueNylon = "BLUENYLON"
    CollarCrimson = "CRIMSON"
    CollarCrimsonBell = "CRIMSONBELL"
    CollarCrimsonBow = "CRIMSONBOW"
    CollarCrimsonNylon = "CRIMSONNYLON"
    CollarCyan = "CYAN"
    CollarCyanBell = "CYANBELL"
    CollarCyanBow = "CYANBOW"
    CollarCyanNylon = "CYANNYLON"
    CollarGreen = "GREEN"
    CollarGreenBell = "GREENBELL"
    CollarGreenBow = "GREENBOW"
    CollarGreenNylon = "GREENNYLON"
    CollarIndigo = "INDIGO"
    CollarIndigoBell = "INDIGOBELL"
    CollarIndigoBow = "INDIGOBOW"
    CollarIndigoNylon = "INDIGONYLON"
    CollarLime = "LIME"
    CollarLimeBell = "LIMEBELL"
    CollarLimeBow = "LIMEBOW"
    CollarLimeNylon = "LIMENYLON"
    CollarMulti = "MULTI"
    CollarMultiBell = "MULTIBELL"
    CollarMultiBow = "MULTIBOW"
    CollarMultiNylon = "MULTINYLON"
    CollarPink = "PINK"
    CollarPinkBell = "PINKBELL"
    CollarPinkBow = "PINKBOW"
    CollarPinkNylon = "PINKNYLON"
    CollarPurple = "PURPLE"
    CollarPurpleBell = "PURPLEBELL"
    CollarPurpleBow = "PURPLEBOW"
    CollarPurpleNylon = "PURPLENYLON"
    CollarRainBow = "RAINBOW"
    CollarRainbowBell = "RAINBOWBELL"
    CollarRainbowBow = "RAINBOWBOW"
    CollarRainbowNylon = "RAINBOWNYLON"
    CollarRed = "RED"
    CollarRedBell = "REDBELL"
    CollarRedBow = "REDBOW"
    CollarRedNylon = "REDNYLON"
    CollarSpikes = "SPIKES"
    CollarSpikesBell = "SPIKESBELL"
    CollarSpikesBow = "SPIKESBOW"
    CollarSpikesNylon = "SPIKESNYLON"
    CollarWhite = "WHITE"
    CollarWhiteBell = "WHITEBELL"
    CollarWhiteBow = "WHITEBOW"
    CollarWhiteNylon = "WHITENYLON"
    CollarYellow = "YELLOW"
    CollarYellowBell = "YELLOWBELL"
    CollarYellowBow = "YELLOWBOW"
    CollarYellowNylon = "YELLOWNYLON"

    # Head accessories
    HeadBlackCicada = "BLACK CICADA"
    HeadBlueberries = "BLUE BERRIES"
    HeadBluebells = "BLUEBELLS"
    HeadBulbBlue = "BULB BLUE"
    HeadBulbOrange = "BULB ORANGE"
    HeadBulbPink = "BULB PINK"
    HeadBulbWhite = "BULB WHITE"
    HeadBulbYellow = "BULB YELLOW"
    HeadCatmint = "CATMINT"
    HeadCattail = "CATTAIL"
    HeadCicadaWings = "CICADA WINGS"
    HeadCyanPoppy = "CYAN POPPY"
    HeadDryCatmint = "DRY CATMINT"
    HeadDryLaurels = "DRY LAURELS"
    HeadDryNettles = "DRY NETTLES"
    HeadForgetMeNots = "FORGET ME NOTS"
    HeadGorse = "GORSE"
    HeadHeather = "HEATHER"
    HeadHolly = "HOLLY"
    HeadJuniper = "JUNIPER"
    HeadLaurel = "LAUREL"
    HeadLavender = "LAVENDER"
    HeadLilyOfTheValley = "LILY OF THE VALLEY"
    HeadMapleLeaf = "MAPLE LEAF"
    HeadMapleSeed = "MAPLE SEED"
    HeadMonarchButterfly = "MONARCH BUTTERFLY"
    HeadMorphoButterfly = "MORPHO BUTTERFLY"
    HeadMothWings = "MOTH WINGS"
    HeadNettle = "NETTLE"
    HeadOakLeaves = "OAK LEAVES"
    HeadOrangePoppy = "ORANGE POPPY"
    HeadPinkPoppy = "PINK POPPY"
    HeadPoppy = "POPPY"
    HeadRaspberry = "RASPBERRY"
    HeadRosyMothWings = "ROSY MOTH WINGS"
    HeadRyeStalk = "RYE STALK"
    HeadSnapdragon = "SNAPDRAGON"
    HeadWhitePoppy = "WHITE POPPY"

    # Body accessories
    BodyHerbs = "HERBS"
    BodyPetals = "PETALS"
    BodyDryHerbs = "DRY HERBS"

    @property
    def category(self):
        if self in [
            self.HerbBlueberries, self.HerbHolly, self.HerbJuniper, self.HerbRaspberry,

            self.HerbBluebells, self.HerbCyanPoppy, self.HerbDaisy, self.HerbForgetMeNots, self.HerbLavender,
            self.HerbLilyOfTheValley, self.HerbOrangePoppy, self.HerbPetals, self.HerbPinkPoppy, self.HerbPoppy,
            self.HerbSnapdragon, self.HerbWhitePoppy,

            self.HerbBulbBlue, self.HerbBulbOrange, self.HerbBulbPink, self.HerbBulbWhite, self.HerbBulbYellow,

            self.HerbCatmint, self.HerbCattail, self.HerbClover, self.HerbGorse, self.HerbHeather, self.HerbHerbs,
            self.HerbLaurel, self.HerbMapleLeaf, self.HerbMapleSeed, self.HerbNettle, self.HerbOakLeaves,
            self.HerbRyeStalk,

            self.HerbDryCatmint, self.HerbDryHerbs, self.HerbDryLaurels, self.HerbDryNettles,
        ]:
            return AccessoryCategory.Herb
        if self in [self.WildBlackCicada, self.WildBlueFeathers, self.WildCicadaWings, self.WildGullFeathers,
                    self.WildJayFeathers, self.WildMonarchButterfly, self.WildMorphoButterfly,
                    self.WildMothWings, self.WildRedFeathers, self.WildRosyMothWings, self.WildSparrowFeathers]:
            return AccessoryCategory.Wild
        if self in [self.TailRedFeathers, self.TailBlueFeathers, self.TailJayFeathers, self.TailGullFeathers,
                    self.TailSparrowFeathers, self.TailClover, self.TailDaisy]:
            return AccessoryCategory.Tail
        if self in [self.CollarBlack, self.CollarBlackBell, self.CollarBlackBow, self.CollarBlackNylon,
                    self.CollarBlue, self.CollarBlueBell, self.CollarBlueBow, self.CollarBlueNylon,
                    self.CollarCrimson, self.CollarCrimsonBell, self.CollarCrimsonBow, self.CollarCrimsonNylon,
                    self.CollarCyan, self.CollarCyanBell, self.CollarCyanBow, self.CollarCyanNylon,
                    self.CollarGreen, self.CollarGreenBell, self.CollarGreenBow, self.CollarGreenNylon,
                    self.CollarIndigo, self.CollarIndigoBell, self.CollarIndigoBow, self.CollarIndigoNylon,
                    self.CollarLime, self.CollarLimeBell, self.CollarLimeBow, self.CollarLimeNylon,
                    self.CollarMulti, self.CollarMultiBell, self.CollarMultiBow, self.CollarMultiNylon,
                    self.CollarPink, self.CollarPinkBell, self.CollarPinkBow, self.CollarPinkNylon,
                    self.CollarPurple, self.CollarPurpleBell, self.CollarPurpleBow, self.CollarPurpleNylon,
                    self.CollarRainBow, self.CollarRainbowBell, self.CollarRainbowBow, self.CollarRainbowNylon,
                    self.CollarRed, self.CollarRedBell, self.CollarRedBow, self.CollarRedNylon,
                    self.CollarSpikes, self.CollarSpikesBell, self.CollarSpikesBow, self.CollarSpikesNylon,
                    self.CollarWhite, self.CollarWhiteBell, self.CollarWhiteBow, self.CollarWhiteNylon,
                    self.CollarYellow, self.CollarYellowBell, self.CollarYellowBow, self.CollarYellowNylon]:
            return AccessoryCategory.Collar
        if self in [
            self.HeadBlueberries, self.HeadHolly, self.HeadJuniper, self.HeadRaspberry,

            self.HeadBluebells, self.HeadCyanPoppy, self.HeadForgetMeNots, self.HeadLavender, self.HeadLilyOfTheValley,
            self.HeadOrangePoppy, self.HeadPinkPoppy, self.HeadPoppy, self.HeadSnapdragon, self.HeadWhitePoppy,

            self.HeadBulbBlue, self.HeadBulbOrange, self.HeadBulbPink, self.HeadBulbWhite, self.HeadBulbYellow,

            self.HeadCatmint, self.HeadCattail, self.HeadGorse, self.HeadHeather, self.HeadLaurel, self.HeadMapleLeaf,
            self.HeadMapleSeed, self.HeadNettle, self.HeadOakLeaves, self.HeadRyeStalk,

            self.HeadDryCatmint, self.HeadDryLaurels, self.HeadDryNettles,

            self.HeadBlackCicada, self.HeadCicadaWings, self.HeadMonarchButterfly, self.HeadMorphoButterfly,
            self.HeadMothWings, self.HeadRosyMothWings,
        ]:
            return AccessoryCategory.Head
        if self in [self.BodyHerbs, self.BodyPetals, self.BodyDryHerbs]:
            return AccessoryCategory.Body
        return None


########################################################################################################################
# Dataclasses
########################################################################################################################

# ------------------------------------- Text ------------------------------------- #

@dataclass
class Pronouns:
    subject: str
    object: str
    poss: str
    inposs: str
    self: str
    conju: int
    parent: str
    sibling: str

DEFAULT_PRONOUNS: dict = {
    "en": {
        GenderAlign.Male: Pronouns(
            subject="he",
            object="him",
            poss="his",
            inposs="his",
            self="himself",
            conju=2,
            parent="father",
            sibling="brother"
        ),
        GenderAlign.Female: Pronouns(
            subject="she",
            object="her",
            poss="her",
            inposs="hers",
            self="herself",
            conju=2,
            parent="mother",
            sibling="sister"
        ),
        GenderAlign.NonBinary: Pronouns(
            subject="they",
            object="them",
            poss="their",
            inposs="theirs",
            self="themself",
            conju=1,
            parent="parent",
            sibling="sibling"
        )
    }
}


########################################################################################################################
# Methods
########################################################################################################################

def cast_to_game_mode(to_cast) -> GameMode:
    """ If possible, return a GameMode object.

     :param to_cast: something to be cast to a GameMode object
     :ptype: str, GameMode, NoneType
     :return GameMode: None returns Any; GameModes return themselves; strings will be matched to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, GameMode, or NoneType object
     """
    if isinstance(to_cast, GameMode):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() == "null":
            return GameMode.Unset
        if to_cast.casefold() == "classic":
            return GameMode.Story
        if to_cast.casefold() == "expanded":
            return GameMode.Expanded
        if to_cast.casefold() == "cruel season":
            return GameMode.CruelSeason
        raise KeyError(f"Could not cast unrecognized string to GameMode: {to_cast}")
    if to_cast is None:
        return GameMode.Unset
    raise TypeError(f"Must be string, None, or GameMode to cast to GameMode. Can't cast {type(to_cast)} to GameMode")


def cast_to_biome(to_cast) -> Biome:
    """ If possible, return a Biome object.

     :param to_cast: something to be cast to a Biome object
     :ptype: str, Biome, NoneType
     :return Biome: None returns Any; Biomes return themselves; strings will be matched to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, Biome, or NoneType object
     """
    if isinstance(to_cast, Biome):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() == "any":
            return Biome.Any
        if to_cast.casefold() == "beach":
            return Biome.Beach
        if to_cast.casefold() == "desert":
            return Biome.Desert
        if to_cast.casefold() == "forest":
            return Biome.Forest
        if to_cast.casefold() == "mountainous":
            return Biome.Mountain
        if to_cast.casefold() == "plains":
            return Biome.Plains
        if to_cast.casefold() == "wetlands":
            return Biome.Wetlands
        if to_cast.casefold() == "twolegplace":
            return Biome.Twolegplace
        raise KeyError(f"Could not cast unrecognized string to Biome: {to_cast}")
    if to_cast is None:
        return Biome.Any
    raise TypeError(f"Must be string, None, or Biome to cast to Biome. Can't cast {type(to_cast)} to Biome")


def cast_to_camp_key(to_cast) -> CampKey:
    """ If possible, return a CampKey object.

     :param to_cast: something to be cast to a CampKey object
     :ptype: str, CampKey, NoneType
     :return CampKey: None returns Any; CampKeys return themselves; strings will be matched to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, CampKey, or NoneType object
     """

    if isinstance(to_cast, CampKey):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() in (CampKey.BeachTidepool.value, "camp_beach_0", "Beachcamp1"):
            return CampKey.BeachTidepool
        if to_cast.casefold() in (CampKey.BeachTidalCave.value, "camp_beach_1", "Beachcamp2"):
            return CampKey.BeachTidalCave
        if to_cast.casefold() in (CampKey.BeachShipwreck.value, "camp_beach_2", "Beachcamp3"):
            return CampKey.BeachShipwreck
        if to_cast.casefold() in (CampKey.BeachFjord.value, "camp_beach_3", "Beachcamp4"):
            return CampKey.BeachFjord
        if to_cast.casefold() in (CampKey.ForestClearing.value, "camp_forest_0", "default"):
            return CampKey.ForestClearing
        if to_cast.casefold() in (CampKey.ForestGully.value, "camp_forest_1", "Forestcamp2"):
            return CampKey.ForestGully
        if to_cast.casefold() in (CampKey.ForestGrotto.value, "camp_forest_2", "Forestcamp3"):
            return CampKey.ForestGrotto
        if to_cast.casefold() in (CampKey.ForestLakeside.value, "camp_forest_3", "Forestcamp4"):
            return CampKey.ForestLakeside
        if to_cast.casefold() in (CampKey.MountainCliff.value, "camp_mountain_0", "Mountainouscamp1"):
            return CampKey.MountainCliff
        if to_cast.casefold() in (CampKey.MountainCavern.value, "camp_mountain_1", "Mountainouscamp2"):
            return CampKey.MountainCavern
        if to_cast.casefold() in (CampKey.MountainCrystalRiver.value, "camp_mountain_2", "Mountainouscamp3"):
            return CampKey.MountainCrystalRiver
        if to_cast.casefold() in (CampKey.MountainRuins.value, "camp_mountain_3", "Mountainouscamp4"):
            return CampKey.MountainRuins
        if to_cast.casefold() in (CampKey.PlainsGrassland.value, "camp_plains_0", "Plainscamp2"):
            return CampKey.PlainsGrassland
        if to_cast.casefold() in (CampKey.PlainsTunnel.value, "camp_plains_1", "Plainscamp3"):
            return CampKey.PlainsTunnel
        if to_cast.casefold() in (CampKey.PlainsWaste.value, "camp_plains_2"):
            return CampKey.PlainsWaste
        raise KeyError(f"Could not cast unrecognized string to CampKey: {to_cast}")
    if to_cast is None:
        return CampKey.NoCamp
    raise TypeError(f"Must be string, None, or CampKey to cast to CampKey. Can't cast {type(to_cast)} to CampKey")


def cast_to_leader_focus(to_cast) -> LeaderFocus:
    """ If possible, return a LeaderFocus object.

     :param to_cast: something to be cast to a LeaderFocus object
     :ptype: str, LeaderFocus, NoneType
     :return LeaderFocus: None returns Any; LeaderFocuss return themselves; strings will be matched to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, LeaderFocus, or NoneType object
     """
    if isinstance(to_cast, LeaderFocus):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() in (LeaderFocus.NoFocus.value, "no leader focus"):
            return LeaderFocus.NoFocus
        if to_cast.casefold() in (LeaderFocus.Provoke.value, "provoke Clan"):
            return LeaderFocus.Provoke
        if to_cast.casefold() in (LeaderFocus.Befriend.value, "befriend Clan"):
            return LeaderFocus.Befriend
        if to_cast.casefold() in (LeaderFocus.HuntDown.value, "hunt down"):
            return LeaderFocus.HuntDown
        if to_cast.casefold() in (LeaderFocus.DriveOff.value, "drive off"):
            return LeaderFocus.DriveOff
        if to_cast.casefold() in (LeaderFocus.InviteIn.value, "invite in", "search for"):
            return LeaderFocus.InviteIn
        raise KeyError(f"Could not cast unrecognized string to LeaderFocus: {to_cast}")
    if to_cast is None:
        return LeaderFocus.NoFocus
    raise TypeError(f"Must be string, None, or LeaderFocus to cast to "
                    f"LeaderFocus. Can't cast {type(to_cast)} to LeaderFocus")


def cast_to_warrior_focus(to_cast) -> WarriorFocus:
    """ If possible, return a WarriorFocus object.

     :param to_cast: something to be cast to a WarriorFocus object
     :ptype: str, WarriorFocus, NoneType
     :return WarriorFocus: None returns Any; WarriorFocuss return themselves; strings will be matched to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, WarriorFocus, or NoneType object
     """
    if isinstance(to_cast, WarriorFocus):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() in (WarriorFocus.NoFocus.value, "business as usual", "no warrior focus"):
            return WarriorFocus.NoFocus
        if to_cast.casefold() in (WarriorFocus.Herb.value, "herb"):
            return WarriorFocus.Herb
        if to_cast.casefold() in (WarriorFocus.Prey.value, "prey"):
            return WarriorFocus.Prey
        if to_cast.casefold() in (WarriorFocus.RR.value, "rest and recover"):
            return WarriorFocus.RR
        if to_cast.casefold() in (WarriorFocus.Befriend.value, "befriend"):
            return WarriorFocus.Befriend
        if to_cast.casefold() in (WarriorFocus.Antagonize.value, "antagonize"):
            return WarriorFocus.Antagonize
        if to_cast.casefold() in (WarriorFocus.Sabotage.value, "sabotage"):
            return WarriorFocus.Sabotage
        if to_cast.casefold() in (WarriorFocus.Aid.value, "aid"):
            return WarriorFocus.Aid
        if to_cast.casefold() in (WarriorFocus.Raid.value, "raid"):
            return WarriorFocus.Raid
        if to_cast.casefold() in (WarriorFocus.Hoard.value, "hoard"):
            return WarriorFocus.Hoard
        raise KeyError(f"Could not cast unrecognized string to WarriorFocus: {to_cast}")
    if to_cast is None:
        return WarriorFocus.NoFocus
    raise TypeError(f"Must be string, None, or WarriorFocus to cast to "
                    f"WarriorFocus. Can't cast {type(to_cast)} to WarriorFocus")


def cast_to_herb(to_cast) -> Herb:
    """ If possible, return a Herb object.

     :param to_cast: something to be cast to a Herb object
     :ptype: str, Herb, NoneType
     :return Herb: None returns Any; Herbs return themselves; strings will be matched to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, Herb, or NoneType object
     """
    if isinstance(to_cast, Herb):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() in ("elderleaf", "elder leaf", "elder_leaf", ):
            return Herb.ElderLeaf
        if to_cast.casefold() in ("cobweb", "cob-web", ):
            return Herb.Cobweb
        if to_cast.casefold() in ("daisy", ):
            return Herb.Daisy
        if to_cast.casefold() in ("horsetail", ):
            return Herb.Horsetail
        if to_cast.casefold() in ("juniper", ):
            return Herb.JuniperBerry
        if to_cast.casefold() in ("lungwort", ):
            return Herb.Lungwort
        if to_cast.casefold() in ("mallow", ):
            return Herb.Mallow
        if to_cast.casefold() in ("marigold", ):
            return Herb.Marigold
        if to_cast.casefold() in ("moss", ):
            return Herb.Moss
        if to_cast.casefold() in ("oakleaf", "oak leaf", "oak_leaf", ):
            return Herb.OakLeaf
        if to_cast.casefold() in ("ragwort", ):
            return Herb.Ragwort
        if to_cast.casefold() in ("raspberry", ):
            return Herb.RaspberryLeaf
        if to_cast.casefold() in ("tansy", ):
            return Herb.Tansy
        if to_cast.casefold() in ("thyme", ):
            return Herb.Thyme
        if to_cast.casefold() in ("wildgarlic", "wild garlic", "wild_garlic", ):
            return Herb.WildGarlic
        if to_cast.casefold() in ("dandelion", ):
            return Herb.Dandelion
        if to_cast.casefold() in ("mullein", ):
            return Herb.Mullein
        if to_cast.casefold() in ("rosemary", ):
            return Herb.Rosemary
        if to_cast.casefold() in ("burdock", ):
            return Herb.Burdock
        if to_cast.casefold() in ("blackberry", ):
            return Herb.BlackberryLeaf
        if to_cast.casefold() in ("betony", ):
            return Herb.Betony
        if to_cast.casefold() in ("goldenrod", ):
            return Herb.Goldenrod
        if to_cast.casefold() in ("poppy", ):
            return Herb.Poppy
        if to_cast.casefold() in ("plantain", ):
            return Herb.Plantain
        if to_cast.casefold() in ("catmint", ):
            return Herb.Catmint
        raise KeyError(f"Could not cast unrecognized string to Herb: {to_cast}")
    if to_cast is None:
        return Herb.Any
    else:
        raise TypeError(f"Must be string, None, or Herb to cast to Herb: {to_cast}")


def cast_to_language(to_cast) -> LanguageCode:
    """ If possible, return a LanguageCode object.

     :param to_cast: something to be cast to a LanguageCode object
     :ptype: str, LanguageCode, NoneType
     :return LanguageCode: None returns Any; Languages return themselves; strings will be matched to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, LanguageCode, or NoneType object
     """
    if isinstance(to_cast, LanguageCode):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() == "en":
            return LanguageCode.English
        if to_cast.casefold() == "es":
            return LanguageCode.Espanol
        if to_cast.casefold() == "de":
            return LanguageCode.Deutch
        raise KeyError(f"Could not cast unrecognized string to LanguageCode: {to_cast}")
    if to_cast is None:
        return LanguageCode.Unset
    raise TypeError(f"Must be string, None, or LanguageCode to cast to LanguageCode. Can't cast {type(to_cast)} to LanguageCode")


def cast_to_location(to_cast) -> Location:
    """ If possible, return a Location object.

     :param to_cast: something to be cast to a Location object
     :ptype: str, Location, NoneType
     :return Location: None returns Any; Locations return themselves; strings will be matched to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, Location, or NoneType object
     """
    if isinstance(to_cast, Location):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() == "any":
            return Location.Any
        if to_cast.casefold() in (Location.ClanWarrior.value, ):
            return Location.ClanWarrior
        if to_cast.casefold() in (Location.LeftClan.value, "former Clancat", "left clan", ):
            return Location.LeftClan
        if to_cast.casefold() in (Location.Exiled.value, "exiled", ):
            return Location.Exiled
        if to_cast.casefold() in (Location.Lost.value, "lost", ):
            return Location.Lost
        if to_cast.casefold() in (Location.StarClan.value, "sc", "starclan", "star clan", ):
            return Location.StarClan
        if to_cast.casefold() in (Location.DarkForest.value, "df", "darkforest", "dark forest", ):
            return Location.DarkForest
        if to_cast.casefold() in (Location.OutsiderAfterlife.value, "unknownresidence", "unknown residence", ):
            return Location.OutsiderAfterlife
        if to_cast.casefold() in (Location.ClanApprentice.value, ):
            return Location.ClanApprentice
        raise KeyError(f"Could not cast unrecognized string to Location: {to_cast}")
    if to_cast is None:
        return Location.Any
    else:
        raise TypeError(f"Must be string, None, or Location to cast to Location: {to_cast}")


def cast_to_rank(to_cast) -> Rank:
    """ If possible, return a Rank object.

     :param to_cast: something to be cast to a Rank object
     :ptype: str, Rank, NoneType
     :return Rank: None returns Any; Ranks return themselves; strings will be matched to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, Rank, or NoneType object
     :raises TypeError: if to_case is a string that should be used for Location
     """
    if isinstance(to_cast, Rank):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() == "any":
            return Rank.Any
        if to_cast.casefold() == "kittypet":
            return Rank.Kittypet
        if to_cast.casefold() == "loner":
            return Rank.Loner
        if to_cast.casefold() == "rogue":
            return Rank.Rogue
        if to_cast.casefold() == "leader":
            return Rank.Leader
        if to_cast.casefold() == "deputy":
            return Rank.Deputy
        if to_cast.casefold() in ("medicine cat", "healer", ):
            return Rank.Healer
        if to_cast.casefold() in ("medicine cat apprentice", "healer apprentice", ):
            return Rank.HealerApp
        if to_cast.casefold() == "mediator":
            return Rank.Mediator
        if to_cast.casefold() == "mediator apprentice":
            return Rank.MediatorApp
        if to_cast.casefold() == "warrior":
            return Rank.Warrior
        if to_cast.casefold() in ("warrior apprentice", "apprentice", ):
            return Rank.WarriorApp
        if to_cast.casefold() in ("kit", "newborn", "kitten", ):
            return Rank.Kit
        if to_cast.casefold() == "elder":
            return Rank.Elder
        if to_cast.casefold() in [
            "sc", "starclan", "star clan", # -> Location.tarClan
            "df", "darkforest", "dark forest", # Location.DarkForest
            "unknownresidence", "unknown residence", # Location.OutsiderAfterlife
            "former Clancat", "left clan", # Location.Location.LeftClan
            "exiled", # Location.Exiled
            "lost" # Location.Lost
        ]:
            raise TypeError(f"This string should be used for Location objects")
        raise KeyError(f"Could not cast unrecognized string to Rank: {to_cast}")
    if to_cast is None:
        return Rank.Any
    raise TypeError(f"Must be string, None, or Rank to cast to Rank: {to_cast}")


def cast_to_relationship_aspect(to_cast) -> RelationshipAspect:
    """ If possible, return a RelationshipAspect object.

     :param to_cast: something to be cast to a RelationshipAspect object
     :ptype: str, RelationshipAspect, NoneType
     :return RelationshipAspect: None returns Any; RelationshipAspects return themselves; strings will be matched to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, RelationshipAspect, or NoneType object
     :raises TypeError: if to_case is a string that should be used for Location
     """
    if isinstance(to_cast, RelationshipAspect):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() == "unknown_relationship_aspect":
            return RelationshipAspect.Unknown
        if to_cast.casefold() in ("comfort", "comfortable", ):
            return RelationshipAspect.Comfort
        if to_cast.casefold() in ("friendship", "platonic_like", ):
            return RelationshipAspect.Friendship
        if to_cast.casefold() in ("romance", "romantic_love", ):
            return RelationshipAspect.Romance
        if to_cast.casefold() in ("respect", "admiration", ):
            return RelationshipAspect.Respect
        if to_cast.casefold() in ("dislike", ):
            return RelationshipAspect.Dislike
        if to_cast.casefold() in ("jealousy", ):
            return RelationshipAspect.Jealousy
        if to_cast.casefold() in ("trust", ):
            return RelationshipAspect.Trust
        raise KeyError(f"Could not cast unrecognized string to RelationshipAspect: {to_cast}")
    if to_cast is None:
        return RelationshipAspect.Unknown
    raise TypeError(f"Must be string, None, or RelationshipAspect to cast to RelationshipAspect: {to_cast}")


def cast_to_season(to_cast) -> Season:
    """ If possible, return a Season object.

     :param to_cast: something to be cast to a Season object
     :ptype: str, Season, NoneType
     :return Season: None returns Any; Seasons return themselves; strings will be matched to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, Season, or NoneType object
     """
    if isinstance(to_cast, Season):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() in ["new-leaf", "newleaf"]:
            return Season.Spring
        if to_cast.casefold() in ["greenleaf", "green-leaf"]:
            return Season.Summer
        if to_cast.casefold() in ["leaffall", "leaf-fall"]:
            return Season.Autumn
        if to_cast.casefold() in ["leafbare", "leaf-bare"]:
            return Season.Winter
        raise KeyError(f"Could not cast unrecognized string to Season: {to_cast}")
    if to_cast is None:
        return Season.Any
    else:
        raise TypeError(f"Must be string, None, or Season to cast to Season: {to_cast}")


def cast_to_skill(to_cast) -> RedSkill:
    """ If possible, return a RedSkill object.

     :param to_cast: something to be cast to a RedSkill object
     :ptype: str, RedSkill, NoneType
     :return RedSkill: None returns Any; RedSkills return themselves; strings will be matched to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, RedSkill, or NoneType object
     """
    if isinstance(to_cast, RedSkill):
        return to_cast
    if isinstance(to_cast, str):
        sk = [b for b in list(RedSkill) if b.value.casefold() == to_cast.casefold()]
        if sk:
            return sk[0]
        else:
            raise KeyError(f"Could not cast unrecognized string to RedSkill: {to_cast}")
    if to_cast is None:
        return RedSkill.Unknown
    raise TypeError(f"Must be string, None, or RedSkill to cast to RedSkill. Can't cast {type(to_cast)} to RedSkill")


def cast_to_patrol_type(to_cast) -> PatrolType:
    """ If possible, return a PatrolType object.

     :param to_cast: something to be cast to a PatrolType object
     :ptype: str, PatrolType, NoneType
     :return PatrolType: None returns Any; PatrolTypes return themselves; strings will be matched to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, PatrolType, or NoneType object
     """
    if isinstance(to_cast, PatrolType):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() == PatrolType.Any.value:
            return PatrolType.Any
        if to_cast.casefold() == PatrolType.General.value:
            return PatrolType.General
        if to_cast in ["train", "training", ]:
            return PatrolType.Train
        if to_cast.casefold() == PatrolType.Border.value:
            return PatrolType.Border
        if to_cast.casefold() in ["hunt", "hunting"]:
            return PatrolType.Hunting
        raise KeyError(f"Could not cast unrecognized string to PatrolType: {to_cast}")
    if to_cast is None:
        return PatrolType.Any
    else:
        raise TypeError(f"Must be string, None, or PatrolType to cast to PatrolType: {to_cast}")


def cast_to_gender_align(to_cast) -> GenderAlign:
    """ If possible, return a GenderAlign object.

     :param to_cast: something to be cast to a GenderAlign object
     :ptype: str, GenderAlign, NoneType
     :return GenderAlign: None returns Any; GenderAligns return themselves; strings will be matched to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, GenderAlign, or NoneType object
     """
    if isinstance(to_cast, GenderAlign):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() == str(GenderAlign.Male):
            return GenderAlign.Male
        if to_cast.casefold() == str(GenderAlign.Female):
            return GenderAlign.Female
        if to_cast.casefold() == str(GenderAlign.NonBinary):
            return GenderAlign.NonBinary
        raise KeyError(f"Could not cast unrecognized string to GenderAlign: {to_cast}")
    if to_cast is None:
        return GenderAlign.NonBinary
    else:
        raise TypeError(f"Must be string, None, or GenderAlign to cast to GenderAlign: {to_cast}")


def cast_to_gender_kits(to_cast) -> GenderKits:
    """ If possible, return a GenderKits object.

     :param to_cast: something to be cast to a GenderKits object
     :ptype: str, GenderKits, NoneType
     :return GenderKits: None returns Any; GenderKits return themselves; strings will be matched to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, GenderKits, or NoneType object
     """
    if isinstance(to_cast, GenderKits):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() == str(GenderKits.Male):
            return GenderKits.Male
        if to_cast.casefold() == str(GenderKits.Female):
            return GenderKits.Female
        if to_cast.casefold() == str(GenderKits.Intersex):
            return GenderKits.Intersex
        raise KeyError(f"Could not cast unrecognized string to GenderAlign: {to_cast}")
    if to_cast is None:
        return GenderKits.Intersex
    else:
        raise TypeError(f"Must be string, None, or GenderAlign to cast to GenderAlign: {to_cast}")


def parse_to_pronouns(to_parse: dict) -> Pronouns:
    """ Parses a dictionary object to a Pronouns dataclass and returns the Pronouns. """
    if isinstance(to_parse, Pronouns):
        return to_parse
    elif isinstance(to_parse, dict):
        return Pronouns(
            subject=to_parse["subject"],
            object=to_parse["object"],
            poss=to_parse["poss"],
            inposs=to_parse["inposs"],
            self=to_parse["self"],
            conju=int(to_parse["conju"]),
            parent=to_parse["parent"],
            sibling=to_parse["sibling"]
        )
    else:
        raise TypeError(f"Must be a dictionary or Pronouns object to parse to Pronouns: {to_parse}")


def cast_to_personality_trait(to_cast) -> PersonalityTrait:
    """ If possible, return a PersonalityTrait object.

    :param to_cast: something to be cast to a PersonalityTrait object
    :ptype: str, PersonalityTrait, NoneType
    :return PersonalityTrait: None returns Any; PersonalityTraits return themselves; strings will be matched to enum member strings.
    :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
    :raises TypeError: if to_cast isn't a str, PersonalityTrait, or NoneType object
    """
    if isinstance(to_cast, PersonalityTrait):
        return to_cast
    if isinstance(to_cast, str):
        pt = [t for t in list(PersonalityTrait) if t.value.casefold() == to_cast.casefold()]
        if pt:
            return pt[0]
        else:
            raise KeyError(f"Could not cast unrecognized string to PersonalityTrait: {to_cast}")
    if to_cast is None:
        return PersonalityTrait.Unknown
    raise TypeError(f"Must be string, None, or PersonalityTrait to cast to PersonalityTrait. Can't cast {type(to_cast)} to PersonalityTrait")
