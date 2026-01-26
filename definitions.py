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
from typing import Optional

import pygame

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
# TODO implement versioning not using github commits
SAVE_CLANSIM_VERSION_NUMBER: int = 1
VERSION_CLANSIM_NUMBER: tuple[int, int, int] = (0,1,0)
SAVE_CLANGEN_VERSION_NUMBER: int = 3
VERSION_CLANGEN_NUMBER: tuple[int, int, int] = (0,9,0)

# Decision and Interaction Keys
# TODO where are these still used?
INTERACTION_NEGATIVE: str = "negative_interaction"
INTERACTION_POSITIVE: str = "positive_interaction"

# Location Keys
# FIXME delete these
LOC_STARCLAN: str = "starclan" # TODO Location.StarClan
LOC_DARK_FOREST: str = "hell" # TODO Location.DarkForest
LOC_DEAD_OTHER: str = "UR"  # unknown residence # TODO Location.UnknownAfterlife
LOC_NOT_CLAN: str = "outside" # TODO LocationCategory.Outsiders
LOC_CLAN: str = "inside" # TODO LocationCategory.InsideClan
DEAD_LOCATIONS: list[str] = [LOC_STARCLAN, LOC_DARK_FOREST, LOC_DEAD_OTHER] # TODO LocationCategory.Afterlife


# ------------------------------ GAME WINDOW VALUES ------------------------------ #

DEFAULT_WINDOW_POS: tuple[int, int] = (0, 0)

DEFAULT_WINDOW_SIZE_X: int = 800
DEFAULT_WINDOW_SIZE_Y: int = 700

DEFAULT_SCREEN_SCALE: float = 1
# fullscreen screen scaling
FULLSCREEN_SCALE_ADJ: int = 20
FULLSCREEN_SCALE_MULT_X: int = 80
FULLSCREEN_SCALE_MULT_Y: int = 70
FULLSCREEN_SCALE_FACTOR: int = 10
# windowed screen scaling
WINDOWED_SCALE_MULT_X: int = 200
WINDOWED_SCALE_MULT_Y: int = 175 # TODO should this be 175/200? why does the game window scale taller faster than wider,
                               #    when the window is wider than it is tall?
WINDOWED_SCALE_FACTOR: int = 4

# ----------------------------- WARRIOR CLANS VALUES ----------------------------- #

# How long does freshkill last until it needs to be removed from the freshkill pile?
# TODO make this a lower number for the Cruel Season
FRESHKILL_ROTS_AT_MOONS: int = 4
REQUIRED_HEALERS_PER_CAT: dict = {}

# special Clan prefixes
STAR_CLAN_TOKEN: str = "_sc_"
DF_CLAN_TOKEN: str = "_df_"
UR_CLAN_TOKEN: str = "_ur_"
LONER_CLAN_TOKEN: str = "_outsider_"
# TODO make sure that none of these can be chosen as the player's Clan name
SPECIAL_CLAN_TOKENS: tuple = (STAR_CLAN_TOKEN, DF_CLAN_TOKEN, UR_CLAN_TOKEN, LONER_CLAN_TOKEN)

CLAN_TEMPERAMENT_WEIGHT: float = 0.3
TEMPERAMENT_THRESHOLD_LOW: float = (16/3)
TEMPERAMENT_THRESHOLD_HIGH: float = 2 * (16/3)

# ------------------------------------ SPRITES ----------------------------------- #

DEFAULT_SPRITES_PER_SPRITESHEET_X: int = 3
DEFAULT_SPRITES_PER_SPRITESHEET_Y: int = 8
DEFAULT_SPRITE_SIZE: int = 50

DEFAULT_CLAN_SYMBOL_NAME: str = "_DEFAULT_"

PLATFORM_WIDTH: int = 80
PLATFORM_HEIGHT: int = 70

EFFECT_MASK: str = "_mask"
EFFECT_LIGHTING: str = "_lighting"

FADE_OPACITY_THRESHOLD_0: int = 80 # at and below this number, the cat will be at stage 1 of fading
FADE_OPACITY_THRESHOLD_1: int = 45 # at and below this number, the cat will be at stage 2 of fading
FADE_OPACITY_THRESHOLD_2: int = 5 # at and below this number, the cat will be completly faded

# --------------------------------- Screen names --------------------------------- #

# TODO replace references to the below with the ScreenName class
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

SPRITE_RANGES: dict[str, tuple[int, int]] = {
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

# ------------------------------------- PATHS ------------------------------------ #

# TODO move these to resources/_red/red_filepaths.py

# settings paths - these are in saves/
CURRENTCLAN_FILENAME: str = "currentclan.txt"
GAME_SETTINGS_FILENAME: str = "game_settings.yaml"
SAVE_VERSION_FILENAME: str = "*_clan.yaml" # * is replaced with Clan token in the IOManager

# save paths - these are in saves/{clan_token}/
SAVE_CLANS_INFO_FILENAME: str = "clans_info.yaml"
SAVE_CAMP_FILENAME: str = "camp.yaml"
SAVE_CLAN_SETTINGS_FILENAME: str = "clan_settings.yaml"
SAVE_CONDITIONS_FILENAME: str = "conditions.yaml"
SAVE_RELATIONSHIPS_FILENAME: str = "relationships.yaml"
SAVE_CURRENT_MOON_EVENTS_FILENAME: str = "current_moon_events.yaml"
ONGOING_EVENTS_DIR: str = "ongoing_events"
ONGOING_EVENTS_FILENAME: str = "*_moons.yaml" # replaces * with number of moons until the event
CLAN_CATS_DIR: str = "cats"
FADED_CATS_INFO_FILENAME: str = "faded_cats_info_copy.txt"

# resource paths
MUSIC_PATH: str = "resources/audio/music/"
SOUNDS_PATH: str = "resources/audio/sounds/"
CONVERSION_DICT_PATH: str = "resources/dicts/conversion_dict.json"

IMAGE_RESOURCES_PATH = "resources/images/"
PATROL_IMAGE_PATH: str = "resources/images/patrol_screen/patrol_art/"
BACKGROUNDS_PATH: str = "resources/images/backgrounds/"

# starting at resources/lang/{language code}/
PATROL_LANG_PATH: str = "patrols/"


########################################################################################################################
# Enums
########################################################################################################################

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
        return logging.DEBUG


class GameMode(StrEnum):
    """ How difficult the game is. Part of Clan settings. """

    UnsetGameMode = "null"

    Classic = "classic"
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

    UnsetLanguage = "unset"

    English = "en"
    Espanol = "es"
    Deutch = "de"


class SortCats(Enum):
    """ How to sort cats. """

    Age = "age"
    Rank = "rank"

    # only applies to sorting dead cats
    MoonsDead = "moons dead"

class SortRelationships(Enum):
    """ How to sort relationships. """

    Total = "total"
    Age = "age" # how long ago did the two cats meet

# -------------------------------------- UI -------------------------------------- #

class ThemeName(StrEnum):
    """ The different possible themes. """

    Light = "light"
    Dark = "dark"
    Debug = "debug"


class ScreenBackground(StrEnum):
    """ Tracks background screens which the game can have. """

    ClanMenu = "" # works as the default

    MainMenu = "menu.png"
    MainMenuLogoless = "menu_logoless.png"
    MacInstaller = "mac_installer_bg_blank.png"

    UnknownResidenceCatsList = "urbg.png"
    OutsideCatsList = "outside_clan_bg.png"
    StarClanCatsList = "starclanbg.png"
    DarkForestCatsList = "darkforestbg.png"

    @property
    def path(self):
        if ".png" in self.value:
            return str(IMAGE_RESOURCES_PATH + "backgrounds/" + self.value)
        else:
            return None

    @property
    def blur_properties(self) -> dict:
        if self is ScreenBackground.ClanMenu:
            return {"vignette_strength": 0, "fade_color": None}
        elif self is ScreenBackground.StarClanCatsList:
            return {"blur_radius": 2}
        elif self in (ScreenBackground.MainMenuLogoless, ScreenBackground.DarkForestCatsList, ScreenBackground.UnknownResidenceCatsList):
            return {"blur_radius": 10}
        else:
            return {}


class BoxShape(StrEnum):
    """ Shapes generated text boxes can be. """

    Frame = "frame"
    RoundedBox = "rounded_box"

class ButtonStyle(StrEnum):
    MainMenu = "mainmenu"
    SquOval = "squoval"
    MenuLeft = "menu_left"
    MenuMiddle = "menu_middle"
    MenuRight = "menu_right"
    FilterDropDown = "filter_dropdown"
    ProfileLeft = "profile_left"
    ProfileMiddle = "profile_middle"
    ProfileRight = "profile_right"
    RoundedRect = "rounded_rect"
    DropDown = "dropdown"
    HorizontalTab = "horizontal_tab"
    HorizontalTabMirrored = "horizontal_tab_mirrored"
    VerticalTab = "vertical_tab"
    LadderTop = "ladder_top"
    LadderMiddle = "ladder_middle"
    LadderBottom = "ladder_bottom"
    Icon = "icon"
    IconTabTop = "icon_tab_top"
    IconTabLeft = "icon_tab_left"
    IconTabBottom = "icon_tab_bottom"
    IconTabRight = "icon_tab_right"

class Icon(StrEnum):
    Speaker = "\U0001F50A"
    MUTE = "\U0001F507"

    DICE = "\u2684"

    CAT_HEAD = "\U0001F431"

    STARCLAN = "\u26EA"
    DARKFOREST = "\U0001F4A7"
    CLAN_PLAYER = "\u2302"
    CLAN_OTHER = "\U0001F3F0"
    CLAN_UNKNOWN = "\U0001F3DA"

    PAW = "\U0001F43E"
    MOUSE = "\U0001F401"
    SCRATCHES = "\U0001F485"
    HERB = "\U0001F33F"

    NEWLEAF = "\U0001FAB4"
    GREENLEAF = "\u2600"
    LEAFFALL = "\U0001F342"
    LEAFBARE = "\u2744"

    ARROW_DOUBLELEFT = "\u23EA"
    ARROW_DOUBLERIGHT = "\u23E9"
    ARROW_LEFT = "\u2190"
    ARROW_UP = "\u2191"
    ARROW_RIGHT = "\u2192"
    ARROW_DOWN = "\u2193"

    MAGNIFY = "\U0001F50D"
    NOTEPAD = "\U0001F5C9"


class ScreenCategory(StrEnum):

    Any = "any"

    MainMenu = "main menu" # "menu screens"
    Creation = "creation screens" # "creation screens"

    Profile = "profile screens"
    Clan = "clan screens"

class ScreenName(StrEnum):

    ScreenUnset = ""

    MainMenu = "main_menu" # "main menu screen"
    GameSettings = "main_settings_screen" # "main settings screen"
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
    HealerDen = "healer_den" # "med den screen"
    WarriorDen = "warrior_den" # "warrior den screen"
    FreshkillPile = "clearing" # "fresh-kill pile screen"

    @property
    def category(self):
        if self in (self.NewClan, ):
            return ScreenCategory.Creation
        if self in (self.MainMenu, self.GameSettings, self.SwitchClan,):
            return ScreenCategory.MainMenu
        if self in (self.Profile, self.LeaderCeremony, self.ManageRoles, self.InspectSprite,
                    self.ChooseMate, self.ChooseMentor, self.AdoptiveParents, self.SeeRelationships,
                    self.FamilyTree, self.Mediation, self.SpecifyGender):
            return ScreenCategory.Profile
        if self in (self.Events, self.Camp, self.CatList, self.Patrol,
                    self.Allegiances, self.ClanSettings, self.LeaderDen, self.HealerDen,
                    self.WarriorDen, self.FreshkillPile):
            return ScreenCategory.Clan
        return ScreenCategory.Any


class ButtonName(StrEnum):
    """ Buttons. """

    GoScreenMainMenu = "go_screen_main_menu"
    GoScreenSwitchClan = "go_screen_switch_clan"
    GoScreenNewClan = "go_screen_new_clan"
    GoScreenGameSettings = "go_screen_game_settings"

    GoScreenEvents = "go_screen_events"
    GoScreenCamp = "go_screen_camp"
    GoScreenCatList = "go_screen_cat_list"
    GoScreenPatrol = "go_screen_patrol"

    GoScreenAllegiances = "go_screen_allegiances"
    GoScreenClanSettings = "go_screen_clan_settings"

    GoScreenLeaderDen = "go_screen_leader_den"
    GoScreenHealerDen = "go_screen_healer_den"
    GoScreenWarriorDen = "go_screen_warriors_den"
    GoScreenFreshkillPile = "go_screen_freshkill_pile"

    # GoScreen = "go_screen_"

    DropdownDens = "dropdown_dens" # "dens"
    DropdownChooseClan = "dropdown_choose_group"
    # Dropdown = "dropdown_"

    Mute = "mute"
    Unmute = "unmute"

    MoonsSeasonsArrow = "widget_moons_n_seasons_arrow"

    @property
    def go_to_screen_name(self):
        if self is self.GoScreenMainMenu:
            return ScreenName.MainMenu
        if self is self.GoScreenSwitchClan:
            return ScreenName.SwitchClan
        if self is self.GoScreenNewClan:
            return ScreenName.NewClan
        if self is self.GoScreenGameSettings:
            return ScreenName.GameSettings

        if self is self.GoScreenEvents:
            return ScreenName.Events
        if self is self.GoScreenCamp:
            return ScreenName.Camp
        if self is self.GoScreenCatList:
            return ScreenName.CatList
        if self is self.GoScreenPatrol:
            return ScreenName.Patrol

        if self is self.GoScreenAllegiances:
            return ScreenName.Allegiances
        if self is self.GoScreenClanSettings:
            return ScreenName.ClanSettings

        if self is self.GoScreenLeaderDen:
            return ScreenName.LeaderDen
        if self is self.GoScreenHealerDen:
            return ScreenName.HealerDen
        if self is self.GoScreenWarriorDen:
            return ScreenName.WarriorDen
        if self is self.GoScreenFreshkillPile:
            return ScreenName.FreshkillPile

        return ScreenName.ScreenUnset

# TODO replace the path part with references to fp
class UIElementPath(StrEnum):
    """ Tracks paths for commonly used """

    CoreVignette = "core_vignette.png"

    ClanNameHeader = "clan_name_heading.png" # "name_background"
    MoonsSeasonsWidget = "widget_moons_n_seasons" # FIXME .path won't return anything
    #WidgetMoonsSeasonsClosed = "widget_moons_n_seasons_closed"
    #WidgetMoonsSeasonsOpen = "widget_moons_n_seasons_open"

    DropdownDensBar = "bar_vertical.png" # "dens_bar"

    @property
    def path(self):
        if self is self.MoonsSeasonsWidget:
            return self.mns_paths
        if ".png" in self.value:
            return str(IMAGE_RESOURCES_PATH + self.value)
        else:
            return None

    @property
    def mns_paths(self):
        if self is not self.MoonsSeasonsWidget:
            raise ValueError(f"Only the MoonsSeasonsWidget UIElementPath object can access this")
        else:
            return {
                "closed": f"{self.value}_closed.png",
                "open": f"{self.value}_open.png"
            }

# ---------------------------------- World enums --------------------------------- #

class Biome(StrEnum):
    NoBiome = "no_biome"

    Forest = "forest"
    Mountain = "mountainous"
    Plains = "plains"
    Beach = "beach"
    Desert = "desert"
    Wetlands = "wetlands"
    Twolegplace = "twolegplace"

    def biomes(self) -> list[str]:
        return [e for e in self if e != self.NoBiome]

    def values(self) -> list[str]:
        return [e for e in self]

    @property
    def implemented_biome(self):
        if self in [self.Forest, self.Mountain, self.Plains, self.Beach]:
            return True
        return False
AVAILABLE_BIOMES: list[str] = [Biome.Forest, Biome.Mountain, Biome.Plains, Biome.Beach]


class HerbName(Enum):
    """ Contains all the herbs the cats can find in the game. """

    # TODO add these herbs
    # AlderBark = 24 # Forest; found in snowy season; eases toothaches when chewed
    # BirchSap = 24 # cure for yellowcough
    # Borage = 6 # chewed and eaten. Queens produce more and better milk, brings down fevers, soothes bad bellies and tight chests
    # Celandine = 8 # Forest, Plains, Wetland; Crushed into juice and trickled into the eye. Soothes weakened and damaged eyes.
    # ChervilRoot = 30 # Mountains, grows in rocky places; topical fights infections, eaten helps bellyaches and during kitting
    # Coltsfoot = 12 # Forest, Mountain, Plains, Wetland, grows best in greenleaf; eases breathing, kittencough, and whitecough
    # Ivy = 24 # used to bind broken bones with sticks

    NoHerb = "no_herb"

    BetonyLeaf = "betony_leaf"
    BlackberryLeaf = "blackberry_leaf" # mixed into a poultice to ease the pain of bee stings
    BurdockRoot = "burdock_root" # fights infections, when applied topically as a paste it numbs pain. Makes you sick if you eat too much
    Catmint = "catmint"
    Cobweb = "cobweb"
    DaisyLeaf = "daisy_leaf"
    DandelionLeaf = "dandelion_leaf" # the roots are also used to cure meadow saffron poisoning
    ElderLeaf = "elder_leaf" # bushes in Forest, Mountain; topical poultice soothes sprains and wrenched muscles
    Goldenrod = "goldenrod"
    Horsetail = "horsetail"
    JuniperBerry = "juniper_berry"
    LungwortLeaf = "lungwort_leaf"
    Mallow = "mallow" # roots and leaves are both used
    Marigold = "marigold" # petals, leaves, stems are all used
    Moss = "moss"
    MulleinLeaf = "mullein_leaf"
    OakLeaf = "oak_leaf"
    PlantainFlower = "plantain_flower"
    PoppySeed = "poppy_seed"
    RagwortLeaf = "ragwort_leaf"
    RaspberryLeaf = "raspberry_leaf"
    Rosemary = "rosemary" # FIXME this isn't used to treat any Condition
    TansyStem = "tansy_stem"
    ThymeLeaf = "thyme_leaf"
    WildGarlic = "wild_garlic"

    @property
    def lifetime_moons(self) -> int:
        """ How long an herb will last until it goes bad and needs to be replaced, in moons. """
        if self is self.NoHerb:
            raise ValueError(f"NoHerb doesn't have a lifetime")
        if self in (self.BurdockRoot, self.Cobweb, ):
            return 30
        if self in (self.Moss, ):
            return 24
        # everything else
        return 12


class Season(StrEnum):
    NoSeason = "no_season" # TODO change this to UnknownSeason

    Spring = "newleaf"
    Summer = "greenleaf"
    Autumn = "leaffall"
    Winter = "leafbare"

    @property
    def season_image_id(self):
        if self is self.Spring:
            return "#mns_image_newleaf"
        if self is self.Summer:
            return "#mns_image_greenleaf"
        if self is self.Autumn:
            return "#mns_image_leaffall"
        if self is self.Winter:
            return "#mns_image_leafbare"
        else:
            return None
AVAILABLE_SEASONS: list[Season] = [Season.Spring, Season.Summer, Season.Autumn, Season.Winter]
YEAR_SEASONS: list[Season] = [Season.Spring, Season.Spring, Season.Spring,
                              Season.Summer, Season.Summer, Season.Summer,
                              Season.Autumn, Season.Autumn, Season.Autumn,
                              Season.Winter, Season.Winter, Season.Winter]

# ----------------------------------- Cat enums ---------------------------------- #

class AgeCategory(Enum):
    """ How age should be sorted. """

    Newborn = "newborn"
    Kitten = "kitten"
    Adolescent = "adol"
    YoungAdult = "young_adult" # "adult", "young adult"
    SeniorAdult = "senior_adult" # "senior adult"
    Elder = "elder" # "senior"

    @property
    def is_adult(self):
        """ Doesn't include elders. """
        return True if self in (self.YoungAdult, self.SeniorAdult) else False


class ConditionCategory(Enum):
    """ Categories for the Condition enum. """

    Pregnancy = "pregnancy"
    Illness = "illness"
    Permanent = "permanent_condition"
    Injury = "injury"

class ConditionSeverity(IntEnum):
    """ How severe a condition is. """

    Minor = auto()
    Medium = auto()
    Major = auto()

class ConditionName(StrEnum):
    """ Every possible condition in the game. """

    # Pregnancy
    Expecting = "expecting" # "pregnant"
    Nursing = "nursing"
    BirthRecovery = "birth_recovery" # "recovering_from_birth"

    # Illness
    Festering = "festering_wound"
    Infected = "infected_wound"
    CarrionplaceDisease = "carrionplace_disease"
    Nightmares = "constant_nightmares"
    Diarrhea = "diarrhea"
    Fleas = "fleas"
    Grieving = "grief_stricken"
    HeatExhaustion = "heat_exhaustion"
    HeatStroke = "heat_stroke"
    RunningNose = "running_nose"
    Stomachache = "stomachache"
    Seizure = "seizure"
    Malnourished = "malnourished"
    Starving = "starving"
    Kittencough = "kittencough"
    Whitecough = "whitecough"
    Greencough = "greencough"
    Yellowcough = "yellowcough"
    Redcough = "redcough"

    # Permanent
    Allergies = "allergies"
    BadEye = "one_bad_eye"
    Blind = "blind"
    BornWithoutLeg = "born_without_leg"
    BornWithoutTail = "born_without_tail"
    ChronicHeadaches = "chronic_headaches"
    ChronicShock = "chronic_shock"
    ConstantlyDizzy = "constantly_dizzy"
    CrookedJaw = "crooked_jaw"
    Deaf = "deaf"
    FailingEyesight = "failing_eyesight"
    HearingLoss = "partial_hearing_loss"
    ChronicJointPain = "constant_joint_pain"
    LastingGrief = "lasting_grief"
    LostLeg = "lost_leg"
    LostTail = "lost_tail"
    Paralysed = "paralysed"
    RaspyLungs = "raspy_lungs"
    Seizures = "seizure_prone"
    TwistedLeg = "twisted_leg"
    WastingDisease = "wasting_disease"
    WeakLeg = "weak_leg"

    # Injury
    TornPelt = "torn_pelt"
    TornEar = "torn_ear"
    BeakBite = "beak_bite"
    BeeSting = "bee_string"
    BiteWound = "bite_wound"
    BrokenBack = "broken_back"
    BrokenBone = "broken_bone"
    BrokenJaw = "broken_jaw"
    Scrapes = "scrapes"
    Bruises = "bruises"
    MangledLeg = "mangled_leg"
    MangledTail = "mangled_tail"
    BloodLoss = "blood_loss"
    Shock = "shock"
    LingeringShock = "lingering_shock"
    Burn = "burn"
    SevereBurn = "severe_burn"
    Frostbite = "frostbite"
    CatBite = "cat_bite"
    RatBite = "rat_bite"
    SnakeBite = "snake_bite"
    TickBites = "tick_bites"
    ClawWound = "claw_wound"
    CrackedPads = "cracked_pads"
    DamagedEyes = "damaged_eyes"
    Dehydrated = "dehydrated"
    Dislocation = "dislocated_joint"
    JointPain = "joint_pain"
    Sore = "sore"
    HeadDamage = "head_damage"
    Headache = "headache"
    Migraine = "severe_headache"
    PhantomPain = "phantom_pain"
    Poisoned = "poisoned"
    Porcupine = "quilled_by_a_porcupine"
    Shivering = "shivering"
    SmallCut = "small_cut"
    Sprain = "sprain"
    SpicyLungs = "water_in_their_lungs"


class GenderKits(StrEnum):
    UnknownGenderKits = "unknown_genderkits"

    Male = "male"  # 1
    Female = "female"
    Intersex = "intersex"

class GenderAlign(StrEnum):
    Male = "tom"  # 1
    Female = "molly"
    NonBinary = "sam"


class LocationCategory(StrEnum):
    """ Categories for the Location enum. """

    Any = "any" # FIXME Nowhere
    Nowhere = "nowhere"

    InsideClan = "inside a warrior Clan"
    OutsideClan = "outside the warrior Clans"
    Afterlife = "dead"

class Location(StrEnum):
    """ Keeps track of a cat's physical position in the world. """

    NoLoc = "no_loc"

    ClanWarrior = "warrior_den" # "warrior's den in camp"
    ClanHealer = "healer_den" # "healer's den in camp"
    ClanApprentice = "app_den" # "apprentice's den in camp"
    ClanNursery = "nursery_den" # "nursery den in camp"
    ClanElder = "elder_den" # "elder's den in camp"
    ClanLeader = "leader_den" # "leader's den in camp"
    ClanOther = "camp" # "somewhere in camp"

    # Outside the Clans
    LeftClan = "ex_clan" # "former Clancat"
    Exiled = "exiled"
    DrivenAway = "driven_away" # "driven away"
    Lost = "lost"
    Wandering = "wandering" # for when a Clan cat leaves with the intention of returning one day
    TwolegNest = "twoleg_nest" # "Twoleg nest"
    Wilderness = "wilderness" # loners and rogues

    # Dead cats
    # if you add any more afterlives, make sure to add them to CatTracker.__init__()
    StarClan = "star_clan"  # used in text_handler.TextHandler.handle_text_content_event
    DarkForest = "dark_forest"  # used in text_handler.TextHandler.handle_text_content_event
    OutsiderAfterlife = "unknown_residence"  # used in text_handler.TextHandler.handle_text_content_event
    GhostResidence = "ghost_res" # where Clan cats go who have unfinished business
                                 # AND/OR who can't get into their proper afterlife
    RiverOfSpirits = "spirit_river" # connects all the other afterlives
    TribeEndlessHunting = "tribe_afterlife" # afterlife of the Tribe of Rushing Water
    TheAncestors = "wildcat_afterlife" # afterlife of the wildcats

    @property
    def category(self):
        if self in (self.ClanWarrior, self.ClanApprentice, self.ClanNursery, self.ClanHealer,
                    self.ClanElder, self.ClanOther, ):
            return LocationCategory.InsideClan
        if self in (self.LeftClan, self.Exiled, self.Lost, self.TwolegNest,
                    self.Wilderness, self.Wandering, self.DrivenAway):
            return LocationCategory.OutsideClan
        if self in (self.StarClan, self.DarkForest, self.OutsiderAfterlife, self.GhostResidence,
                    self.RiverOfSpirits, self.TribeEndlessHunting, self.TheAncestors, ):
            return LocationCategory.Afterlife
        return LocationCategory.Nowhere

    # TODO remove non-faded afterlife locations so the ghost interaction patrol events are with a specific cat?
    @property
    def patrol_interact_possible(self):
        if self in (self.Lost, self.StarClan, self.DarkForest, self.OutsiderAfterlife, self.DrivenAway):
            return False
        return True

    @property
    def afterlife_screen_background(self):
        """ Points the RedBaseScreen class to the correct effects for cats in the afterlife. """
        if self is self.StarClan:
            return ScreenBackground.StarClanCatsList
        elif self is self.DarkForest:
            return ScreenBackground.DarkForestCatsList
        elif self is self.OutsiderAfterlife:
            return ScreenBackground.UnknownResidenceCatsList
        else:
            raise ValueError(f"Can't return an afterlife screen background for location \"{self.name}\"")


# special Clan prefixes
# STAR_CLAN_TOKEN: str = "_sc_"
# STAR_CLAN_NAME: str = "StarClan"
# DF_CLAN_TOKEN: str = "_df_"
# DF_NAME: str = "the Place of No Stars"
# UR_CLAN_TOKEN: str = "_ur_"
# UR_CLAN_NAME: str = "an unknown residence"
# LONER_CLAN_TOKEN: str = "_outsider_"
# LONER_CLAN_NAME: str = ""
# # TODO make sure that none of these can be chosen as the player's Clan name
# SPECIAL_CLAN_TOKENS: tuple = (STAR_CLAN_TOKEN, DF_CLAN_TOKEN, UR_CLAN_TOKEN, LONER_CLAN_TOKEN)
class SpecialClanToken(StrEnum):

    # living cats
    Loners = "_loners_"

    # dead cats
    StarClan = "_sc_"
    DarkForest = "_df_"
    OutsiderAfterlife = "_ur_" # for kittypets, loners, and rogues
    GhostResidence = "_gr_" # where Clan cats go who have unfinished business
                            # AND/OR who can't get into their proper afterlife
    RiverSpirits = "_rs_"  # connects all the other afterlives
    TribeEndlessHunting = "_teh_"  # afterlife of the Tribe of Rushing Water
    TheAncestors = "_ta_"  # afterlife of the wildcats

    @property
    def afterlife_screen_background(self):
        """ Points the RedBaseScreen class to the correct effects for cats in the afterlife. """
        if self is self.StarClan:
            return ScreenBackground.StarClanCatsList
        elif self is self.DarkForest:
            return ScreenBackground.DarkForestCatsList
        elif self is self.OutsiderAfterlife:
            return ScreenBackground.UnknownResidenceCatsList
        else:
            raise ValueError(f"Can't return an afterlife screen background for location \"{self.name}\"")

    @property
    def is_afterlife(self):
        if self is self.Loners:
            return False
        else:
            return True


class Afterlife(StrEnum):
    """ Keeps track of special Clans that cats can be part of, almost none of which areactually warrior Clans. """

    StarClan = "star_clan"
    DarkForest = "dark_forest"
    OutsiderAfterlife = "unknown_res" # where loners, kittypets, etc. go. The default value
    GhostResidence = "ghost_res" # where Clan cats go who have unfinished business AND/OR who can't get into their proper afterlife
    RiverOfSpirits = "spirit_river" # connects all the other afterlives
    TribeEndlessHunting = "tribe_endless_hunting" # Tribe of Rushing Water
    TheAncestors = "the_ancestors" # The Wildcats

    @property
    def clan_name(self):
        if self is self.StarClan: return "StarClan"
        elif self is self.DarkForest: return "the Place of No Stars"
        elif self is self.OutsiderAfterlife: return "an unknown afterlife"
        elif self is self.GhostResidence: return "a ghostly realm"
        elif self is self.RiverOfSpirits: return "on the shore of the River of spirits"
        elif self is self.TribeEndlessHunting: return "the Tribe of Endless Hunting"
        elif self is self.TheAncestors: return "with the ancestors"
        raise ValueError(f"There is no name for the afterlife: {self.name}")


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


# Rank needs to be below Age for Rank.appropriate_ages
class Rank(StrEnum):
    """ Keeps track of a cat's social status within or outside a Clan. This can't change after death.

    NB: I thought about adding a Rank.Exiled, since arguably if you're exiled you don't have a
     rank in the Clan anymore. But there are some backstories about being exiled that include
     specific ranks (e.g. ClansOtherExileHighRank) that specify both a rank and exile.
     If said cat joins a new Clan, they might want to keep the same rank (e.g. ClansOtherHealer).
    """
    NoRank = "no_rank"

    # Non-Clan cats
    Kittypet = "kittypet"
    Loner = "loner"
    Rogue = "rogue"
    # TribeToBe = "tribe_to-be"
    # TribeGuard = "tribe_guard"
    # TribeHunter = "tribe_hunter"

    # Clan cats
    Leader = "leader"
    Deputy = "deputy"
    Healer = "healer"
    HealerApp = "healer_app"
    Mediator = "mediator"
    MediatorApp = "mediator_app"
    Warrior = "warrior"
    WarriorApp = "warrior_app"

    Kit = "kit"
    Elder = "elder"
    Queen = "queen" # not yet implemented
    QueenApp = "queen_app" # not yet implemented

    @property
    def is_healer(self) -> bool:
        return True if self in (self.Healer, self.HealerApp) else False

    @property
    def is_queen(self) -> bool:
        return True if self in (self.Queen, self.QueenApp) else False

    @property
    def able(self) -> bool:
        if self in [self.Leader, self.Deputy, self.Warrior, self.Healer, self.Mediator, self.WarriorApp,
                    self.HealerApp, self.MediatorApp]:
            return True
        return False

    @property
    def is_apprentice(self) -> bool:
        if self in [self.HealerApp, self.MediatorApp, self.WarriorApp]:
            return True
        return False

    @property
    def valid_hunter(self) -> bool:
        if self in [self.Leader, self.Deputy, self.Warrior, self.WarriorApp]:
            return True
        return False

    @property
    def is_outsider(self) -> bool:
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
            return Location.NoLoc
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

    UnknownRelAsp = "unknown_relationship_aspect"

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

    # INSIGHTFUL -> Reasoning

    UnsetSkill = "unset_skill"

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
    Navigating = "navigate"  # hunt: scavenging  border: forest, Twolegplace

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

    def get_bg_path(self, season: Season, theme: ThemeName) -> str: # TODO switch to os.path?
        if theme in ThemeName:
            # FIXME hardcoded path
            return f"resources/images/backgrounds/camp_bg/{season.value}/{self.value}_{theme.value}.png"
        raise ValueError(f"Unrecognized theme: {theme}")

    def get_den_positions(self):
        """ Get positions where the den labels on the camp background. """
        pass

    def get_cat_positions(self):
        """ Get positions where cats can appear on the camp background. """
        pass


class LeaderFocus(Enum):
    """ Options for what the leader in a Clan can focus on. """

    NoFocus = None # "no leader focus"
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


class ClanTemperament(Enum):
    """ Get the text value for a Clan's temperament. """

    Cunning = "cunning"
    Proud = "proud"
    Bloodthirsty = "bloodthirsty"
    Amiable = "amiable"
    Stoic = "stoic"
    Wary = "wary"
    Gracious = "gracious"
    Mellow = "mellow"
    Logical = "logical"


# ---------------------------------- Event enums --------------------------------- #

# TODO what's the point of HistoryTag AND Event AND EventCategory? Consolidate these.
class HistoryTag(StrEnum):
    """ Tags for events in history. Events can have more than one of these. """

    Birth = "birth"
    Death = "death"

    JoinClan = "join_clan"
    ChangeRank = "change_rank"

    Scar = "scar" # used for events where a cat is scarred

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

    UnsetPType = "unset_patrol_type"

    General = "general"  # TODO this should be a category, not a member
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

    UnsetPreyAmount = -1

    VerySmall = 0.5
    Small = 1.0
    Medium = 1.8
    Large = 2.4
    Huge = 3.2


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

class PeltPatternCategory(Enum):
    """ Inheritance weights for each pattern group. It goes: (striped, spotted, solid, exotic) """

    Striped = [50, 10, 5, 7]
    Spotted = [10, 50, 5, 5]
    Solid = [5, 5, 50, 0]
    Exotic = [15, 15, 1, 45]

    Random = [35, 20, 30, 5]

    @property
    def genetic_inheritance(self):
        return self.value

    def get_order(self) -> list:
        return [self.Striped, self.Spotted, self.Solid, self.Exotic]

# TODO make this an IntEnum with the value equal to the location on the sprite sheet
class PeltPattern(StrEnum):
    """ Codes for pelt patterns. """
    SolidColour = "solid_colour" # single_colour, single_solid
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
        if self in [self.SolidColour, self.Smoke, self.SingleStripe]:
            return PeltPatternCategory.Solid
        if self in [self.Bengal, self.Marbled, self.Masked]:
            return PeltPatternCategory.Exotic
        return PeltPatternCategory.Random

    @property
    def genetic_inheritance(self):
        return self.category.genetic_inheritance


# TODO make this an IntEnum with the value equal to the location on the sprite sheet
class TortiePatches(StrEnum):
    """ Tortie pelt patterns. """

    One = "one"
    Two = "two"
    Three = "three"
    Four = "four"
    Redtail = "redtail"
    Delilah = "delilah"
    MinimalOne = "minimal_one"
    MinimalTwo = "minimal_two"
    MinimalThree = "minimal_three"
    MinimalFour = "minimal_four"
    Half = "half"
    Oreo = "oreo"
    Swoop = "swoop"
    Mottled = "mottled"
    SideMask = "sidemask"
    EyeDot = "eyedot"
    Bandana = "bandana"
    PacMan = "pacman"
    Streamstrike = "streamstrike"
    Oriole = "oriole"
    Chimera = "chimera"
    Daub = "daub"
    Ember = "ember"
    Blanket = "blanket"
    Robin = "robin"
    Brindle = "brindle"
    Paige = "paige"
    Rosetail = "rosetail"
    Safi = "safi"
    Smudged = "smudged"
    Dapplenight = "dapplenight"
    Streak = "streak"
    Mask = "mask"
    Chest = "chest"
    ArmTail = "armtail"
    Smoke = "smoke"
    GrumpyFace = "grumpyface"
    Brie = "brie"
    Beloved = "beloved"
    Body = "body"
    Shiloh = "shiloh"
    Freckled = "freckled"
    Heartbeat = "heartbeat"


class PeltColourCategory(Enum):
    """ Inheritance weights for each colour group. It goes: (ginger_colours, black_colours, white_colours, brown_colours) """
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
    """ Codes for pelt base colours. """

    # category: white
    White = "white"
    PaleGrey = "pale_grey" # palegrey
    Silver = "silver"

    # category: black
    Grey = "grey"
    DarkGrey = "dark_grey" # darkgrey
    Ghost = "ghost"
    Black = "black"

    # category: ginger
    Cream = "cream"
    PaleGinger = "pale_ginger" #paleginger
    Golden = "golden"
    Ginger = "ginger"
    DarkGinger = "dark_ginger" # darkginger
    Sienna = "sienna"

    # category: brown
    LightBrown = "light_brown" # lightbrown
    Lilac = "lilac"
    Brown = "brown"
    GoldenBrown = "golden_brown" # goldenbrown/golden-brown
    DarkBrown = "dark_brown" # darkbrown
    Chocolate = "chocolate"

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
                    ColourTint.WarmDilute, ColourTint.Yellow, ]

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
            # Note that although the ginger pelt colours includes Sienna and the "warm" colour group doesn't, because
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
    """ RGB values of the tints that base pelts colour can have. """

    NoTint = None
    Pink = "pink"
    Grey = "grey"
    Red = "red"
    Black = "black"
    Orange = "orange"
    Yellow = "yellow"
    Purple = "purple"
    Blue = "blue"
    Dilute = "dilute"
    WarmDilute = "warm_dilute"
    CoolDilute = "cool_dilute"

    @property
    def colour_value(self):
        if self is self.Pink:
            return (253, 237, 237)
        elif self is self.Grey:
            return (225, 225, 225)
        elif self is self.Red:
            return (248, 226, 228)
        elif self is self.Black:
            return  (195, 195, 195)
        elif self is self.Orange:
            return (255, 247, 235)
        elif self is self.Yellow:
            return (250, 248, 225)
        elif self is self.Purple:
            return (235, 225, 244)
        elif self is self.Blue:
            return (218, 237, 245)
        elif self is self.Dilute:
            return (20, 20, 20)
        elif self is self.WarmDilute:
            return (25, 15, 7)
        elif self is self.CoolDilute:
            return (7, 15, 25)
        return None


class PeltLengthCategory(Enum):
    """ Genetic weights for each pelt length. It goes: (short, medium, long) """
    Short = [150, 150, 0] # [50, 10, 2]
    Medium = [75, 150, 75] # [25, 50, 25]
    Long = [0, 150, 150] # [2, 10, 50]

    Random = [100, 100, 100]

    @property
    def genetic_inheritance(self):
        return self.value

    def get_order(self) -> list:
        return [self.Short, self.Medium, self.Long]

class PeltLength(Enum):
    """ The lengths and textures that pelts can have. """

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


class WhitePatchCategory(Enum):
    """ Inheritance weights for each pattern group. It goes: (nowhite,low,mid,high,mostly,full,point,vitiligo)

    If you're not sure which category a white patch pattern should go into:
        low = 1%-25%
        mid = 26% - 50%
        high = 51% - 75%
        mostly = 76% - 99%
        full = 100% (there's only one object in this category)
    """
    NoWhitePatch = None
    Low = "low"
    Mid = "mid"
    High = "high"
    Mostly = "mostly"
    Full = "full"

    Point = "point"
    Vitiligo = "vitiligo"

    Random = [10, 100, 100, 100, 50, 10, 5, 1]  # [10, 10, 10, 10, 1]

    @property
    def genetic_inheritance(self):
        if self is self.NoWhitePatch:
            return [15, 40, 5, 0, 10, 0, 0, 0]
        elif self is self.Low:
            return [20, 40, 30, 15, 10, 0, 0, 0]  # little_white = [30, 40, 20, 15, 5, 0]
        elif self is self.Mid:
            return [5, 10, 40, 15, 10, 0, 0, 0]  # mid_white = [10, 40, 15, 10, 0]
        elif self is self.High:
            return [0, 15, 20, 40, 10, 1, 0, 0]  # high_white = [15, 20, 40, 10, 1]
        elif self is self.Mostly:
            return [0, 5, 15, 20, 40, 5, 0, 0]  # mostly_white = [5, 15, 20, 40, 5]
        elif self is self.Full:
            return [0, 0, 5, 15, 40, 10, 0, 0]  # full_white = [0, 5, 15, 40, 10]
        elif self is self.Point:
            return [10, 100, 100, 100, 100, 10, 100, 0]  # point
        elif self is self.Vitiligo:
            return [10, 100, 100, 100, 100, 10, 5, 50]  # vit
        else:
            return [10, 100, 100, 100, 50, 10, 5, 1]

    def get_order(self) -> list:
        return [self.NoWhitePatch, self.Low, self.Mid, self.High, self.Mostly, self.Full, self.Point, self.Vitiligo]

class WhitePatches(Enum):
    """ White patches for pelts. """

    _SendToRandom = "Send to me to WhitePatchCategory.Random, please!"

    # WhitePatchCategory.NoWhitePatch
    NoWhitePatch = None

    # WhitePatchCategory.Low

    # WhitePatchCategory.Mid

    # WhitePatchCategory.High

    # WhitePatchCategory.Mostly

    # WhitePatchCategory.Full
    FullWhite = "fullwhite"

    # WhitePatchCategory.Point
    ColourPoint = "colourpoint"
    SepiaPoint = "sepiapoint"
    MinkPoint = "minkpoint"
    SealPoint = "sealpoint"

    # WhitePatchCategory.Vitiligo
    Vitiligo = "vitiligo"
    VitiligoTwo = "vitiligotwo"

    Wrap = "wrap" # TODO any
    Tuxedo = "tuxedo"
    Little = "little"
    Coat = "coat" # TODO anytwo
    Moon = "moon"
    Phantom = "phantom"
    Powder = "powder"
    Bleached = "bleached"
    FadeSpots = "fadespots"
    Savannah = "savannah"
    Pebbleshine = "pebbleshine"

    Extra = "extra"
    OneEar = "oneear"
    Broken = "broken"
    LightTuxedo = "lighttuxedo"
    Ragdoll = "ragdoll"
    Piebald = "piebald"
    Curved = "curved"
    Petal = "petal"
    ShibaInu = "shibainu"
    Owl = "owl"

    Tip = "tip"
    Fancy = "fancy"
    Freckles = "freckles"
    RingTail = "ringtail"
    HalfFace = "halfface"
    PantsTwo = "pantstwo"
    Goatee = "goatee"
    Paws = "paws"
    Mitaine = "mitaine"
    BrokenBlaze = "brokenblaze"
    Beard = "beard"

    Tail = "tail"
    Blaze = "blaze"
    Bib = "bib"
    Vee = "vee"
    Unders = "unders" # TODO change to HalfBottom? Is that what this is?
    Belly = "belly"
    TailTip = "tailtip"
    Toes = "toes"
    TopCover = "topcover" # TODO change to HalfTop

    Apron = "apron"
    CapSaddle = "capsaddle"
    MaskMantle = "maskmantle"
    Star = "star"
    ToesTail = "toestail"
    Pants = "pants" # TODO change to HalfBack
    ReversePants = "reversepants" # change to TODO HalfFront
    Skunk = "skunk"
    HalfWhite = "halfwhite"
    Appaloosa = "appaloosa"

    Heart = "heart"
    LilTwo = "liltwo"
    Glass = "glass"
    Moorish = "moorish"
    Mao = "mao"
    ChestSpeck = "chestspeck"  # TODO is this really Mostly white?
    Wings = "wings"
    Painted = "painted"
    HeartTwo = "hearttwo"
    WoodPecker = "woodpecker"

    Boots = "boots"
    Miss = "miss"
    Cow = "cow"
    CowTwo = "cowtwo"
    Bub = "bub"
    BowTie = "bowtie"
    Mustache = "mustache"
    ReverseHeart = "reverseheart"
    Sparrow = "sparrow"
    Vest = "vest"
    Sparkle = "sparkle"

    RightEar = "rightear"
    LeftEar = "leftear"
    Estrella = "estrella"
    ShootingStar = "shootingstar"
    EyeSpot = "eyespot"
    ReverseEye = "reverseeye"
    FadeBelly = "fadebelly"
    Front = "front"
    Pebble = "pebble"
    TailTwo = "tailtwo"
    BackSpot = "backspot"
    EyeBags = "eyebags"

    BlazeChestPawsBroken = "fctwo"
    BlazeChestPawsContinuous = "fcone"

    Locket = "locket"
    BlazeMask = "blazemask"
    Tears = "tears"
    Van = "van"

    # Based on cats in the books
    Buzzardfang = "buzzardfang"
    Lightsong = "lightsong"
    Blackstar = "blackstar"
    Ravenpaw = "ravenpaw"
    Dapplepaw = "dapplepaw"
    Blossomstep = "blossomstep"
    Hawkblaze = "hawkblaze"
    Buddy = "buddy"
    Bullseye = "bullseye"
    Buster = "buster"
    Cake = "cake"
    Damien = "damien"
    Digit = "digit"
    Diva = "diva"
    Dougie = "dougie"
    Farofa = "farofa"
    Finn = "finn"
    Honey = "honey"
    Karpati = "karpati"
    Kropka = "kropka"
    Lovebug = "lovebug"
    Luna = "luna"
    Mia = "mia"
    Mister = "mister"
    Prince = "prince"
    Princess = "princess"
    Rosina = "rosina"
    Sammy = "sammy"
    Scar = "scar"
    Scourge = "scourge"
    Smokey = "smokey"
    Squeaks = "squeaks"
    Trixie = "trixie"

    @property
    def category(self):
        if self in [self.Little, self.LightTuxedo, self.Buzzardfang, self.Tip, self.Blaze, self.Bib, self.Vee,
                    self.Paws, self.Belly, self.TailTip, self.Toes, self.BrokenBlaze, self.LilTwo, self.Scourge,
                    self.ToesTail, self.Ravenpaw, self.Honey, self.Luna, self.Extra, self.Mustache,
                    self.ReverseHeart, self.Sparkle, self.RightEar, self.LeftEar, self.Estrella, self.ReverseEye,
                    self.BackSpot, self.EyeBags, self.Locket, self.BlazeMask, self.Tears]:
            return WhitePatchCategory.Low
        if self in [self.Tuxedo, self.Fancy, self.Unders, self.Damien, self.Skunk, self.Mitaine, self.Squeaks,
                    self.Star, self.Wings, self.Diva, self.Savannah, self.FadeSpots, self.FadeBelly, self.Beard,
                    self.Dapplepaw, self.TopCover, self.WoodPecker, self.Miss, self.BowTie, self.Vest, self.Digit,
                    self.BlazeChestPawsBroken, self.BlazeChestPawsContinuous, self.Mia, self.Rosina, self.Princess,
                    self.Dougie, ]:
            return WhitePatchCategory.Mid
        if self in [self.Appaloosa, self.Blossomstep, self.Broken, self.Bub, self.Bullseye, self.Buster, self.Cake,
                    self.Coat, self.Curved, self.Farofa, self.Finn, self.Freckles, self.Front, self.Glass, self.Goatee,
                    self.HalfFace, self.HalfWhite, self.Hawkblaze, self.Mister, self.Mao, self.MaskMantle, self.Owl,
                    self.Painted, self.Pants, self.PantsTwo, self.Piebald, self.Prince, self.ReversePants,
                    self.RingTail, self.Sammy, self.Scar, self.ShibaInu, self.Sparrow, self.Trixie, self.Wrap, ]:
            return WhitePatchCategory.High
        if self in [self.Apron, self.Blackstar, self.Boots, self.Cow, self.CowTwo, self.CapSaddle, self.ChestSpeck,
                    self.Buddy, self.EyeSpot, self.Heart, self.HeartTwo, self.Kropka, self.Lightsong, self.Lovebug,
                    self.Moorish, self.OneEar, self.Pebble, self.Pebbleshine, self.Petal, self.ShootingStar,
                    self.Tail, self.TailTwo, self.Van, ]:
            return WhitePatchCategory.Mostly
        if self is WhitePatches.FullWhite:
            return WhitePatchCategory.Full
        if self in [self.ColourPoint, self.MinkPoint, self.Ragdoll, self.SepiaPoint, self.SealPoint]:
            return WhitePatchCategory.Point
        if self in [self.Bleached, self.Karpati, self.Moon, self.Phantom, self.Powder, self.Smokey,
                    self.Vitiligo, self.VitiligoTwo, ]:
            return WhitePatchCategory.Vitiligo
        if self is self._SendToRandom:
            return WhitePatchCategory.Random
        return WhitePatchCategory.Random

    @property
    def genetic_inheritance(self):
        return self.category.genetic_inheritance

class WhitePatchTint(Enum):
    """ RGB values of the tints that white patches can have. """

    NoTint = None
    WhitePatchDarkCream = "dark_cream"
    WhitePatchCream = "cream"
    WhitePatchOffwhite = "offwhite"
    WhitePatchGrey = "grey"
    WhitePatchPink = "pink"

    @property
    def colour_value(self) -> Optional[tuple[int, int, int]]:
        if self is self.WhitePatchCream:
            return (247, 241, 225)
        elif self is self.WhitePatchDarkCream:
            return (236, 229, 208)
        elif self is self.WhitePatchGrey:
            return (208, 225, 229)
        elif self is self.WhitePatchOffwhite:
            return (238, 249, 252)
        elif self is self.WhitePatchPink:
            return (254, 248, 249)
        return None


class EyeColourCategory(Enum):
    """ Inheritance weights for each eye colour group. It goes: (yellow, green, blue) """
    Yellow = [50, 20, 0]
    Green = [20, 40, 20]
    Blue = [0, 20, 50]

    Random = [10, 10, 10]

    @property
    def genetic_inheritance(self):
        return self.value

    def get_order(self) -> list:
        return [self.Yellow, self.Green, self.Blue]

class EyeColour(StrEnum):
    """ Eye colours for cats. """

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
    """ Inheritance weights for each skin colour group. It goes: (cool,warm,brown,marbled) """
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
    """ Skin colours for cats. """

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
    DarkestBrown = "dark" # dark is darker than black. slightly confusing
    DarkBrown = "dark_brown"
    Brown = "brown"
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
        if self in [self.DarkestBrown, self.DarkBrown, self.Brown, self.LightBrown, self.Chocolate]:
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

class ScarName(StrEnum):
    """ Scars cats have on their body, AND missing limbs. """

    # scars from other cats, other animals
    ScratchEye = "scratch_eye" # "a scar over one eye"
    ScratchChest = "scratch_chest" # "one"
    ScratchSide = "scratch_side"
    ScratchBack = "scratch_back" # "two"
    ScratchBackPaw = "scratch_back_paw" # "four"

    MangledLeg = "mangled_leg"
    MangledTail = "mangled_tail"

    BiteLeg = "leg_bite"
    BiteNeck = "neck_bite"
    BiteRat = "rat_bite"
    BiteCatChest = "cat_bite_chest" # CATBITE
    BiteCatLeg = "cat_bite_leg" # CATEBITETWO
    Brightheart = "brightheart"

    BlindRight = "blind_right"
    BlindLeft = "blind_left"
    BlindBoth = "blind_both"

    BeakCheek = "beak_cheek"
    BeakLower = "beak_lower"
    BeakSide = "beak_side"

    QuillChunkPaw = "quill_chunk"
    QuillScratchCheek = "quill_scratch"
    QuillScratchSide = "quill_side"

    Snout = "snout"
    Bridge = "bridge"
    Cheek = "cheek"
    Face = "face"
    Throat = "throat"
    Side = "side"
    Belly = "belly"
    HindLeg = "hindleg"
    Back = "back"
    TailBase = "tail_base"
    TailScar = "tail_scar"

    # "special" scars that could only happen in a special event
    BurnPaws = "burn_paws"
    BurnBelly = "burn_belly"
    BurnRump = "burn_rump"
    BurnTail = "burn_tail"
    FrostFace = "frost_face"
    FrostHindPaw = "frost_hind" # frostsock
    FrostForePaw = "frost_fore" # frostmitt
    FrostTail = "frost_tail"
    SnakeShoulder = "snake_shoulder" # snake
    SnakeHindLeg = "snake_leg" # snaketwo
    Toe = "toe"
    ToeTrap = "toe_trap"

    # TODO TornEars
    TornLeftEar = "torn_left_ear" # "a torn left ear"
    TornRightEar = "torn_right_ear" # "a torn right ear"
    NoLeftEar = "no_left_ear" # "no left ear"
    NoRightEar = "no_right_ear" # "no right ear"
    NoEars = "no_ears" # "missing ears"
    NoPaw = "no_leg" # "one missing leg"
    NoTail = "no_tail" # "no tail"
    HalfTail = "half_tail" # "half a tail"

    @property
    def category(self):
        if self in (self.ScratchEye, self.ScratchChest, self.ScratchSide, self.ScratchBack, self.ScratchBackPaw,
                    self.MangledLeg, self.MangledTail, self.BlindRight, self.BlindLeft, self.BlindBoth,
                    self.BiteLeg, self.BiteNeck, self.BiteRat, self.BiteCatChest, self.BiteCatLeg,
                    self.Brightheart, self.BeakCheek, self.BeakLower, self.BeakSide,
                    self.QuillChunkPaw, self.QuillScratchCheek, self.QuillScratchSide,
                    self.Snout, self.Bridge, self.Cheek, self.Face, self.Throat, self.Side,
                    self.Belly, self.HindLeg, self.Back, self.TailBase, self.TailScar,):
            return ScarCategory.Normal
        if self in (self.BurnPaws, self.BurnBelly, self.BurnRump, self.BurnTail,
                    self.FrostFace, self.FrostHindPaw, self.FrostForePaw, self.FrostTail,
                    self.SnakeShoulder, self.SnakeHindLeg, self.Toe, self.ToeTrap,):
            return ScarCategory.SpecialEvent
        if self in (self.BiteLeg, self.BiteNeck, self.BiteRat, self.BiteCatLeg, self.BiteCatChest, self.Brightheart,):
            return ScarCategory.Bite
        if self in (self.BurnPaws, self.BurnBelly, self.BurnRump, self.BurnTail,):
            return ScarCategory.Burn
        if self in (self.FrostFace, self.FrostHindPaw, self.FrostForePaw, self.FrostTail,):
            return ScarCategory.Frostbite
        if self in (self.TornLeftEar, self.TornRightEar, self.NoLeftEar, self.NoRightEar,
                    self.NoEars, self.NoPaw, self.NoTail, self.HalfTail,):
            return ScarCategory.MissingLimb
        return None


class AccessoryName(StrEnum):

    # "acc_plant_"
    PlantMapleLeaf = "maple_leaf"
    PlantHolly = "holly"
    PlantBlueberries = "blueberries"
    PlantForgetMeNots = "forget_me_nots"
    PlantRyeStalk = "rye_stalk"
    PlantCattail = "cattail"
    PlantRedPoppy = "red_poppy"
    PlantOrangePoppy = "orange_poppy"
    PlantCyanPoppy = "cyan_poppy"
    PlantWhitePoppy = "white_poppy"
    PlantPinkPoppy = "pink_poppy"
    PlantBluebells = "bluebells"
    PlantLilyOfTheValley = "lily_of_the_valley"
    PlantSnapdragon = "snapdragon"
    PlantHerbs = "herbs"
    PlantPetals = "petals"
    PlantNettle = "nettle"
    PlantHeather = "heather"
    PlantGorse = "gorse"
    PlantJuniper = "juniper"
    PlantRaspberry = "raspberry"
    PlantLavender = "lavender"
    PlantOakLeaf = "oak_leaf"
    PlantCatmint = "catmint"
    PlantMapleSeed = "maple_seed"
    PlantLaurel = "laurel"
    PlantBulbWhite = "bulb_white"
    PlantBulbYellow = "bulb_yellow"
    PlantBulbOrange = "bulb_orange"
    PlantBulbPink = "bulb_pink"
    PlantBulbBlue = "bulb_blue"
    PlantCloser = "closer"
    PlantDaisy = "daisy"
    PlantWisteria = "wisteria"
    PlantRoseMallow = "rose_mallow"
    PlantPickleweed = "pickleweed"
    PlantGoldenCreepingJenny = "golden_creeping_jenny"
    PlantDesertWillow = "desert_willow"
    PlantCactusFlower = "cactus_flower"
    PlantPrairieFire = "prairie_fire"
    PlantVerbenaEar = "verbena_ear"
    PlantVerbenaPelt = "verbena_pelt"
    PlantDryHerbs = "dry_herbs"
    PlantDryCatmint = "dry_catmint"
    PlantDryNettle = "dry_nettles"
    PlantDryLaurel = "dry_laurels"

    WildRedFeathers = "red_feathers"
    WildBlueFeathers = "blue_feathers"
    WildJayFeathers = "jay_feathers"
    WildGullFeathers = "gull_feathers"
    WildSparrowFeathers = "sparrow_feathers"
    WildMothWings = "moth_wings"
    WildRosyMothWings = "rosy_moth_wings"
    WildMorphoButterfly = "morpho_butterfly"
    WildMonarchButterfly = "monarch_butterfly"
    WildCicadaWings = "cicada_wings"
    WildBlackCicada = "black_cicada"
    WildRoadrunnerFeathers = "roadrunner_feather"

    # "acc_collar_"
    CollarBowBase = "bow_base"
    CollarBowCrimson = "bow_crimson"
    CollarBowBlue = "bow_blue"
    CollarBowYellow = "bow_yellow"
    CollarBowCyan = "bow_cyan"
    CollarBowOrange = "bow_orange"
    CollarBowLime = "bow_lime"
    CollarBowWhite = "bow_white"
    CollarBowBlack = "bow_black"
    CollarBowGreen = "bow_green"
    CollarBowPink = "bow_pink"
    CollarBowPurple = "bow_purple"
    CollarBowRose = "bow_rose"
    CollarBowIndigo = "bow_indigo"

    CollarBowFoilBase = "bow_foil_base"
    CollarBowFoilBlack = "bow_foil_black_gold"

    CollarBowGradientBase = "bow_gradient_base"
    CollarBowGradientRainbow = "bow_gradient_rainbow"

    CollarLeatherBase = "leather_base"
    CollarLeatherCrimson = "leather_crimson"
    CollarLeatherBlue = "leather_blue"
    CollarLeatherYellow = "leather_yellow"
    CollarLeatherCyan = "leather_cyan"
    CollarLeatherOrange = "leather_orange"
    CollarLeatherLime = "leather_lime"
    CollarLeatherWhite = "leather_white"
    CollarLeatherBlack = "leather_black"
    CollarLeatherGreen = "leather_green"
    CollarLeatherPink = "leather_pink"
    CollarLeatherPurple = "leather_purple"
    CollarLeatherRose = "leather_rose"
    CollarLeatherIndigo = "leather_indigo"

    CollarLeatherSpikeBase = "leather_spike_base"
    CollarLeatherSpikeCrimson = "leather_spike_crimson_gold"
    CollarLeatherSpikeBlue = "leather_spike_blue_gold"
    CollarLeatherSpikeYellow = "leather_spike_yellow_silver"
    CollarLeatherSpikeCyan = "leather_spike_cyan_gold"
    CollarLeatherSpikeOrange = "leather_spike_orange_silver"
    CollarLeatherSpikeLime = "leather_spike_lime_silver"
    CollarLeatherSpikeWhite = "leather_spike_white_gold"
    CollarLeatherSpikeBlack = "leather_spike_black_gold"
    CollarLeatherSpikeGreen = "leather_spike_green_silver"
    CollarLeatherSpikePink = "leather_spike_pink_gold"
    CollarLeatherSpikePurple = "leather_spike_purple_gold"
    CollarLeatherSpikeRose = "leather_spike_rose_gold"
    CollarLeatherSpikeIndigo = "leather_spike_indigo_gold"

    CollarLeatherGradientBase = "leather_gradient_base"
    CollarLeatherGradientRainbow = "leather_gradient_rainbow"

    CollarLeatherBellBase = "leather_bell_base"
    CollarLeatherBellCrimson = "leather_bell_crimson"
    CollarLeatherBellBlue = "leather_bell_blue"
    CollarLeatherBellYellow = "leather_bell_yellow"
    CollarLeatherBellCyan = "leather_bell_cyan"
    CollarLeatherBellOrange = "leather_bell_orange"
    CollarLeatherBellLime = "leather_bell_lime"
    CollarLeatherBellWhite = "leather_bell_white"
    CollarLeatherBellBlack = "leather_bell_black"
    CollarLeatherBellGreen = "leather_bell_green"
    CollarLeatherBellPink = "leather_bell_pink"
    CollarLeatherBellPurple = "leather_bell_purple"
    CollarLeatherBellRose = "leather_bell_rose"
    CollarLeatherBellIndigo = "leather_bell_indigo"

    CollarLeatherBellSpikeBase = "leather_bell_spike_base"
    CollarLeatherBellSpikeCrimson = "leather_bell_spike_crimson_gold"
    CollarLeatherBellSpikeBlue = "leather_bell_spike_blue_gold"
    CollarLeatherBellSpikeYellow = "leather_bell_spike_yellow_silver"
    CollarLeatherBellSpikeCyan = "leather_bell_spike_cyan_gold"
    CollarLeatherBellSpikeOrange = "leather_bell_spike_orange_silver"
    CollarLeatherBellSpikeLime = "leather_bell_spike_lime_silver"
    CollarLeatherBellSpikeWhite = "leather_bell_spike_white_gold"
    CollarLeatherBellSpikeBlack = "leather_bell_spike_black_gold"
    CollarLeatherBellSpikeGreen = "leather_bell_spike_green_silver"
    CollarLeatherBellSpikePink = "leather_bell_spike_pink_gold"
    CollarLeatherBellSpikePurple = "leather_bell_spike_purple_gold"
    CollarLeatherBellSpikeRose = "leather_bell_spike_rose_gold"
    CollarLeatherBellSpikeIndigo = "leather_bell_spike_indigo_gold"

    CollarLeatherBellGradientBase = "leather_bell_gradient_base"
    CollarLeatherBellGradientRainbow = "leather_bell_gradient_rainbow"

    CollarNylonBase = "nylon_base"
    CollarNylonCrimson = "nylon_crimson"
    CollarNylonBlue = "nylon_blue"
    CollarNylonYellow = "nylon_yellow"
    CollarNylonCyan = "nylon_cyan"
    CollarNylonOrange = "nylon_orange"
    CollarNylonLime = "nylon_lime"
    CollarNylonWhite = "nylon_white"
    CollarNylonBlack = "nylon_black"
    CollarNylonBlackGold = "nylon_black_gold"
    CollarNylonGreen = "nylon_green"
    CollarNylonPink = "nylon_pink"
    CollarNylonPurple = "nylon_purple"
    CollarNylonRose = "nylon_rose"
    CollarNylonIndigo = "nylon_indigo"

    CollarNylonGradientBase = "nylon_gradient_base"
    CollarNylonGradientRainbow = "nylon_gradient_rainbow"

    CollarNylonBellBase = "nylon_bell_base"
    CollarNylonBellCrimson = "nylon_bell_crimson"
    CollarNylonBellBlue = "nylon_bell_blue"
    CollarNylonBellYellow = "nylon_bell_yellow"
    CollarNylonBellCyan = "nylon_bell_cyan"
    CollarNylonBellOrange = "nylon_bell_orange"
    CollarNylonBellLime = "nylon_bell_lime"
    CollarNylonBellWhite = "nylon_bell_white"
    CollarNylonBellBlack = "nylon_bell_black"
    CollarNylonBellBlackGold = "nylon_bell_black_gold"
    CollarNylonBellGreen = "nylon_bell_green"
    CollarNylonBellPink = "nylon_bell_pink"
    CollarNylonBellPurple = "nylon_bell_purple"
    CollarNylonBellRose = "nylon_bell_rose"
    CollarNylonBellIndigo = "nylon_bell_indigo"

    CollarNylonBellGradientBase = "nylon_bell_gradient_base"
    CollarNylonBellGradientRainbow = "nylon_bell_gradient_rainbow"


class SpritePose(IntEnum):
    """ Connects sprite bases to positions on spritesheets. """

    UnchosenPose = -1

    Newborn0 = 0
    Newborn1 = 1
    Newborn2 = 2
    Kitten0 = 3
    Kitten1 = 4
    Kitten2 = 5
    Adolescent0 = 6
    Adolescent1 = 7
    Adolescent2 = 8
    AdultShort0 = 9
    AdultShort1 = 10
    AdultShort2 = 11
    AdultLong0 = 12
    AdultLong1 = 13
    AdultLong2 = 14
    Senior0 = 15
    Senior1 = 16
    Senior2 = 17
    ParaAdultShort = 18
    ParaAdultLong = 19
    ParaYoung = 20
    SickAdult = 21
    SickYoung = 22

    @classmethod
    def get_age_sprites(cls, age: str):
        if age == "newborn":
            return [cls.Newborn0, cls.Newborn1, cls.Newborn2]
        elif age == "kitten":
            return [cls.Kitten0, cls.Kitten1, cls.Kitten2]
        elif age == "adolescent":
            return [cls.Adolescent0, cls.Adolescent1, cls.Adolescent2]
        elif age == "adult":
            return {PeltLength.Long: [cls.AdultLong0, cls.AdultLong1, cls.AdultLong2],
                    PeltLength.Short: [cls.AdultShort0, cls.AdultShort1, cls.AdultShort2]}
        return [cls.Senior0, cls.Senior1, cls.Senior2]


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
    LanguageCode.English: {
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
     :return GameMode: None returns UnsetGameMode; GameModes return themselves; strings will be matched to
                       enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, GameMode, or NoneType object
     """
    if isinstance(to_cast, GameMode):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() in ("null", GameMode.UnsetGameMode.value, ):
            return GameMode.UnsetGameMode
        if to_cast.casefold() == "classic":
            return GameMode.Classic
        if to_cast.casefold() == "expanded":
            return GameMode.Expanded
        if to_cast.casefold() == "cruel season":
            return GameMode.CruelSeason
        raise KeyError(f"Could not cast unrecognized string to GameMode: {to_cast}")
    if to_cast is None:
        return GameMode.UnsetGameMode
    raise TypeError(f"Must be string, None, or GameMode to cast to GameMode. Can't cast {type(to_cast)} to GameMode")


def cast_to_biome(to_cast) -> Biome:
    """ If possible, return a Biome object.

     :param to_cast: something to be cast to a Biome object
     :ptype: str, Biome, NoneType
     :return Biome: None returns NoBiome; Biomes return themselves; strings will be matched to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, Biome, or NoneType object
     """
    if isinstance(to_cast, Biome):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() in (Biome.NoBiome.value, "any", "no_biome", ):
            return Biome.NoBiome
        if to_cast.casefold() in (Biome.Beach, "beach", ):
            return Biome.Beach
        if to_cast.casefold() in (Biome.Desert, "desert", ):
            return Biome.Desert
        if to_cast.casefold() in (Biome.Forest, "forest", ):
            return Biome.Forest
        if to_cast.casefold() in (Biome.Mountain, "mountain", "mountainous", ):
            return Biome.Mountain
        if to_cast.casefold() in (Biome.Plains, "plains", ):
            return Biome.Plains
        if to_cast.casefold() in (Biome.Wetlands, "wetlands", ):
            return Biome.Wetlands
        if to_cast.casefold() in (Biome.Twolegplace, "twolegplace", ):
            return Biome.Twolegplace
        raise KeyError(f"Could not cast unrecognized string to Biome: {to_cast}")
    if to_cast is None:
        return Biome.NoBiome
    raise TypeError(f"Must be string, None, or Biome to cast to Biome. Can't cast {type(to_cast)} to Biome")


def cast_to_camp_key(to_cast) -> CampKey:
    """ If possible, return a CampKey object.

     :param to_cast: something to be cast to a CampKey object
     :ptype: str, CampKey, NoneType
     :return CampKey: None returns NoCamp; CampKeys return themselves; strings will be matched to enum member strings.
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
     :return LeaderFocus: None returns NoFocus; LeaderFocus return themselves; strings will be
                          matched to enum member strings.
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
     :return WarriorFocus: None returns NoFocus; WarriorFocuss return themselves; strings will be matched
                           to enum member strings.
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


def cast_to_herb(to_cast) -> HerbName:
    """ If possible, return a HerbName object.

     :param to_cast: something to be cast to a HerbName object
     :ptype: str, HerbName, NoneType
     :return HerbName: None returns NoHerb; Herbs return themselves; strings will be matched to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, HerbName, or NoneType object
     """
    if isinstance(to_cast, HerbName):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() in HerbName:
            return HerbName(to_cast.casefold())
        if to_cast.casefold() in ("no_herb", "any", ):
            return HerbName.NoHerb
        if to_cast.casefold() in ("elderleaf", "elder leaf", "elder_leaf", "elder_leaves", ):
            return HerbName.ElderLeaf
        if to_cast.casefold() in ("cobweb", "cob-web", "cobwebs", ):
            return HerbName.Cobweb
        if to_cast.casefold() in ("daisy", ):
            return HerbName.DaisyLeaf
        if to_cast.casefold() in ("horsetail", ):
            return HerbName.Horsetail
        if to_cast.casefold() in ("juniper", ):
            return HerbName.JuniperBerry
        if to_cast.casefold() in ("lungwort", ):
            return HerbName.LungwortLeaf
        if to_cast.casefold() in ("mallow", ):
            return HerbName.Mallow
        if to_cast.casefold() in ("marigold", ):
            return HerbName.Marigold
        if to_cast.casefold() in ("moss", ):
            return HerbName.Moss
        if to_cast.casefold() in ("oakleaf", "oak leaf", "oak_leaf", ):
            return HerbName.OakLeaf
        if to_cast.casefold() in ("ragwort", ):
            return HerbName.RagwortLeaf
        if to_cast.casefold() in ("raspberry", ):
            return HerbName.RaspberryLeaf
        if to_cast.casefold() in ("tansy", ):
            return HerbName.TansyStem
        if to_cast.casefold() in ("thyme", ):
            return HerbName.ThymeLeaf
        if to_cast.casefold() in ("wildgarlic", "wild garlic", "wild_garlic", ):
            return HerbName.WildGarlic
        if to_cast.casefold() in ("dandelion", ):
            return HerbName.DandelionLeaf
        if to_cast.casefold() in ("mullein", ):
            return HerbName.MulleinLeaf
        if to_cast.casefold() in ("rosemary", ):
            return HerbName.Rosemary
        if to_cast.casefold() in ("burdock", ):
            return HerbName.BurdockRoot
        if to_cast.casefold() in ("blackberry", ):
            return HerbName.BlackberryLeaf
        if to_cast.casefold() in ("betony", ):
            return HerbName.BetonyLeaf
        if to_cast.casefold() in ("goldenrod", ):
            return HerbName.Goldenrod
        if to_cast.casefold() in ("poppy", ):
            return HerbName.PoppySeed
        if to_cast.casefold() in ("plantain", ):
            return HerbName.PlantainFlower
        if to_cast.casefold() in ("catmint", ):
            return HerbName.Catmint
        raise KeyError(f"Could not cast unrecognized string to HerbName: {to_cast}")
    if to_cast is None:
        return HerbName.NoHerb
    else:
        raise TypeError(f"Must be string, None, or HerbName to cast to HerbName: {to_cast}")


def cast_to_language(to_cast) -> LanguageCode:
    """ If possible, return a LanguageCode object.

     :param to_cast: something to be cast to a LanguageCode object
     :ptype: str, LanguageCode, NoneType
     :return LanguageCode: None returns UnsetLanguage; Languages return themselves; strings
                           will be matched to enum member strings.
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
        return LanguageCode.UnsetLanguage
    raise TypeError(f"Must be string, None, or LanguageCode to cast to LanguageCode. Can't cast {type(to_cast)} to LanguageCode")


def cast_to_location(to_cast) -> Location:
    """ If possible, return a Location object.

     :param to_cast: something to be cast to a Location object
     :ptype: str, Location, NoneType
     :return Location: None returns NoLoc; Locations return themselves; strings will be matched to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, Location, or NoneType object
     """
    if isinstance(to_cast, Location):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() in (Location.NoLoc.value, "any"):
            return Location.NoLoc
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
        return Location(to_cast)
    if to_cast is None:
        return Location.NoLoc
    else:
        raise TypeError(f"Must be string, None, or Location to cast to Location: {to_cast}")


def cast_to_rank(to_cast) -> Rank:
    """ If possible, return a Rank object.

     :param to_cast: something to be cast to a Rank object
     :ptype: str, Rank, NoneType
     :return Rank: None returns NoRank; Ranks return themselves; strings will be matched to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, Rank, or NoneType object
     :raises TypeError: if to_case is a string that should be used for Location
     """
    if isinstance(to_cast, Rank):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() in ("any", "no_rank", ):
            return Rank.NoRank
        if to_cast.casefold() in ("kittypet", ):
            return Rank.Kittypet
        if to_cast.casefold() in ("loner", ):
            return Rank.Loner
        if to_cast.casefold() in ("rogue", ):
            return Rank.Rogue
        if to_cast.casefold() in ("leader", ):
            return Rank.Leader
        if to_cast.casefold() in ("deputy", ):
            return Rank.Deputy
        if to_cast.casefold() in ("medicine cat", "healer", ):
            return Rank.Healer
        if to_cast.casefold() in ("medicine cat apprentice", "healer apprentice", ):
            return Rank.HealerApp
        if to_cast.casefold() in ("mediator", ):
            return Rank.Mediator
        if to_cast.casefold() in ("mediator apprentice", ):
            return Rank.MediatorApp
        if to_cast.casefold() in ("warrior", ):
            return Rank.Warrior
        if to_cast.casefold() in ("warrior apprentice", "apprentice", ):
            return Rank.WarriorApp
        if to_cast.casefold() in ("kit", "newborn", "kitten", ):
            return Rank.Kit
        if to_cast.casefold() in ("elder", ):
            return Rank.Elder
        if to_cast.casefold() in [
            "sc", "starclan", "star clan", # -> Location.tarClan
            "df", "darkforest", "dark forest", # Location.DarkForest
            "unknownresidence", "unknown residence", # Location.OutsiderAfterlife
            "former Clancat", "left clan", # Location.Location.LeftClan
            "exiled", # Location.Exiled
            "lost" # Location.Lost
        ]:
            raise TypeError(f"Can no longer use \"{to_cast}\" as a rank")
        return Rank(to_cast)
    if to_cast is None:
        return Rank.NoRank
    raise TypeError(f"Must be string, None, or Rank to cast to Rank: {to_cast}")


def cast_to_relationship_aspect(to_cast) -> RelationshipAspect:
    """ If possible, return a RelationshipAspect object.

     :param to_cast: something to be cast to a RelationshipAspect object
     :ptype: str, RelationshipAspect, NoneType
     :return RelationshipAspect: None returns UnknownRelAsp; RelationshipAspects return themselves; strings will
                                 be matched to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, RelationshipAspect, or NoneType object
     :raises TypeError: if to_case is a string that should be used for Location
     """
    if isinstance(to_cast, RelationshipAspect):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() in ("unknown_relationship_aspect", ):
            return RelationshipAspect.UnknownRelAsp
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
        return RelationshipAspect.UnknownRelAsp
    raise TypeError(f"Must be string, None, or RelationshipAspect to cast to RelationshipAspect: {to_cast}")


def cast_to_season(to_cast) -> Season:
    """ If possible, return a Season object.

     :param to_cast: something to be cast to a Season object
     :ptype: str, Season, NoneType
     :return Season: None returns NoSeason; Seasons return themselves; strings will be matched to enum member strings.
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
        return Season.NoSeason
    else:
        raise TypeError(f"Must be string, None, or Season to cast to Season: {to_cast}")


def cast_to_skill(to_cast) -> RedSkill:
    """ If possible, return a RedSkill object.

     :param to_cast: something to be cast to a RedSkill object
     :ptype: str, RedSkill, NoneType
     :return RedSkill: None returns UnsetSkill; RedSkills return themselves; strings will
                       be matched to enum member strings.
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
        return RedSkill.UnsetSkill
    raise TypeError(f"Must be string, None, or RedSkill to cast to RedSkill. Can't cast {type(to_cast)} to RedSkill")


def cast_to_patrol_type(to_cast) -> PatrolType:
    """ If possible, return a PatrolType object.

     :param to_cast: something to be cast to a PatrolType object
     :ptype: str, PatrolType, NoneType
     :return PatrolType: None returns UnsetPType; PatrolTypes return themselves; strings will be
                         matched to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, PatrolType, or NoneType object
     """
    if isinstance(to_cast, PatrolType):
        return to_cast
    if isinstance(to_cast, str):
        if to_cast.casefold() in (PatrolType.UnsetPType.value, "any",):
            return PatrolType.UnsetPType
        if to_cast.casefold() in (PatrolType.General.value, ):
            return PatrolType.General
        if to_cast.casefold() in (PatrolType.Train.value, "train", "training", ):
            return PatrolType.Train
        if to_cast.casefold() in (PatrolType.Border.value, ):
            return PatrolType.Border
        if to_cast.casefold() in (PatrolType.Hunting.value, "hunt", "hunting", ):
            return PatrolType.Hunting
        raise KeyError(f"Could not cast unrecognized string to PatrolType: {to_cast}")
    if to_cast is None:
        return PatrolType.UnsetPType
    else:
        raise TypeError(f"Must be string, None, or PatrolType to cast to PatrolType: {to_cast}")


def cast_to_gender_align(to_cast) -> GenderAlign:
    """ If possible, return a GenderAlign object.

     :param to_cast: something to be cast to a GenderAlign object
     :ptype: str, GenderAlign, NoneType
     :return GenderAlign: None returns NonBinary; GenderAligns return themselves; strings will
                          be matched to enum member strings.
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
     :return GenderKits: None returns UnknownGenderKits; GenderKits return themselves; strings will
                         be matched to enum member strings.
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
        return GenderKits.UnknownGenderKits
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
