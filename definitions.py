# definitions.py - a map for


APP_NAME_DEFAULT: str = "ClanSim"
APP_NAME_BETA: str = "ClanSimBeta"
APP_AUTHOR: str = "ClanSim"

TIMESTR_FORMAT: str = "%Y%m%d_%H%M%S"


# This is saved in the Clan save-file, and is used for save-file conversion.
CLANSIM_SAVE_VERSION_NUMBER = 0
CLANSIM_VERSION_NUMBER: str = "0.1.0"
CLANGEN_SAVE_VERSION_NUMBER = 3
CLANGEN_VERSION_NUMBER: str = "0.9.0"


# paths
MUSIC_PATH: str = 'resources/audio/music/'
SOUNDS_PATH: str = 'resources/audio/sounds/'
PATROL_IMAGE_PATH: str = 'resources/images/patrol_art/'


# scripts paths
SPRITE_PATHS: dict = {
    'lineart': {'sprites/lineart/'},
    'tints': {'sprites/tints/'},
    'faded': {'sprites/faded/'},
    'paralyzed': {'sprites/paralyzed/'},
    'accessories': {'sprites/accessories/'},
    'april_fools': {'sprites/april_fools/'}
}


########################################################################################################################
# Screen Names
########################################################################################################################
MAIN_MENU_SCREEN_NAME: str = "main menu screen"
MAIN_SETTINGS_SCREEN_NAME: str = "main settings screen"
NEW_CLAN_SCREEN_NAME: str = "new clan screen"
SWITCH_CLAN_SCREEN_NAME: str = "switch clan screen"

PROFILE_SCREEN_NAME: str = "profile screen"
PROFILE_ADOPT_SCREEN_NAME: str = "choose adoptive parent screen"
PROFILE_CEREMONY_SCREEN_NAME: str = "leader ceremony screen"
PROFILE_FAMILY_SCREEN_NAME: str = "family tree screen"
PROFILE_GENDER_SCREEN_NAME: str = "change gender screen"
PROFILE_MATE_SCREEN_NAME: str = "choose mate screen"
PROFILE_MEDIATION_SCREEN_NAME: str = "mediation screen"
PROFILE_MENTOR_SCREEN_NAME: str = "choose mentor screen"
PROFILE_RELATIONSHIPS_SCREEN_NAME: str = "relationship screen"
PROFILE_ROLE_SCREEN_NAME: str = "role screen"
PROFILE_SPRITE_INSPECT_SCREEN_NAME: str = "sprite inspect screen"

CLAN_ALLEGIANCES_SCREEN_NAME: str = "allegiances screen"
CLAN_CAMP_SCREEN_NAME: str = "camp screen"
CLAN_FRESHKILL_SCREEN_NAME: str = "fresh-kill pile screen"
CLAN_EVENTS_SCREEN_NAME: str = "events screen"
CLAN_MEMBERS_SCREEN_NAME: str = "members screen"
CLAN_PATROL_SCREEN_NAME: str = "patrol screen"
CLAN_SETTINGS_SCREEN_NAME: str = "clan settings screen"

MED_DEN_SCREEN_NAME: str = "med den screen"
LEADER_DEN_SCREEN_NAME: str = "leader den screen"
WARRIOR_DEN_SCREEN_NAME: str = "warrior den screen"

CREATION_SCREENS_KEY: str = "creation screens"
CREATION_SCREENS = [NEW_CLAN_SCREEN_NAME]
MAIN_MENU_SCREENS_KEY: str = "menu screens"
MAIN_MENU_SCREENS = [MAIN_SETTINGS_SCREEN_NAME, MAIN_MENU_SCREEN_NAME, SWITCH_CLAN_SCREEN_NAME]

########################################################################################################################
# Game Element Keys
########################################################################################################################

# Biomes
BIOME_ANY: str = "any"
BIOME_BEACH: str = "beach"
BIOME_DESERT: str = "desert"
BIOME_FOREST: str = "forest"
BIOME_MOUNTAIN: str = "mountainous"
BIOME_PLAINS: str = "plains"
BIOME_WETLANDS: str = "wetlands"
BIOME_TWOLEGPLACE: str = "twolegplace"
BIOME_KEYS: list[str] = [BIOME_BEACH, BIOME_DESERT, BIOME_FOREST, BIOME_MOUNTAIN,
                         BIOME_PLAINS, BIOME_WETLANDS, BIOME_TWOLEGPLACE]
IMPLEMENTED_BIOMES: list[str] = [BIOME_BEACH, BIOME_FOREST, BIOME_MOUNTAIN, BIOME_PLAINS]

# Seasons
SEASON_ANY: str = "any"
SEASON_SPRING: str = "newleaf"
SEASON_SUMMER: str = "greenleaf"
SEASON_AUTUMN: str = "leaffall"
SEASON_WINTER: str = "leafbare"
YEAR_SEASONS: list[str] = [SEASON_SPRING, SEASON_SPRING, SEASON_SPRING,
                           SEASON_SUMMER, SEASON_SUMMER, SEASON_SUMMER,
                           SEASON_AUTUMN, SEASON_AUTUMN, SEASON_AUTUMN,
                           SEASON_WINTER, SEASON_WINTER, SEASON_WINTER]

# Cat status
STATUS_ANY: str = "any"
STATUS_LIVING: str = "living"       # TODO this status is redundant with the others
STATUS_NONCLAN: str = "outside cat" # TODO this should be a category, like clan_roles_apps
STATUS_CLAN: str = "clancat"        # TODO this should be a category, like clan_roles_apps

STATUS_DEAD_STARCLAN: str = "starclan"
STATUS_DEAD_DARK_FOREST: str = "darkforest"
STATUS_DEAD_UNKNOWN_RESIDENCE: str = "unknownresidence"

STATUS_KITTYPET: str = "kittypet"
STATUS_LONER: str = "loner"
STATUS_ROGUE: str = "rogue"
STATUS_EXCLAN: str = "former Clancat"
STATUS_EXILED: str = "exiled"

STATUS_LEADER: str = "leader"
STATUS_DEPUTY: str = "deputy"
STATUS_MEDICINE: str = "medicine cat"
STATUS_MEDICINE_APP: str = "medicine cat apprentice"
STATUS_MEDIATOR: str = "mediator"
STATUS_MEDIATOR_APP: str = "mediator apprentice"
STATUS_WARRIOR: str = "warrior"
STATUS_WARRIOR_APP: str = "apprentice"    # TODO differentiate between any apprentice and warrior apprentices
STATUS_KIT: str = "kitten"
STATUS_NEWBORN: str = "newborn"
STATUS_ELDER: str = "elder"
STATUS_LOST: str = "lost"

CLAN_ROLES_RANK_SORT_REVERSE_ORDER: list[str] = [   # This in is in reverse order: top of the list at the bottom
    STATUS_ELDER, # Elders come last in books' CLAN ALLEGIANCES sections
    STATUS_NEWBORN,
    STATUS_KIT,
    STATUS_WARRIOR_APP,
    STATUS_WARRIOR,
    STATUS_MEDIATOR_APP,
    STATUS_MEDIATOR,
    STATUS_MEDICINE_APP,
    STATUS_MEDICINE,
    STATUS_DEPUTY,
    STATUS_LEADER,
]
CLAN_STATUS_ADULTS: list[str] = [STATUS_LEADER, STATUS_DEPUTY, STATUS_MEDICINE,
                                 STATUS_MEDIATOR, STATUS_WARRIOR, STATUS_ELDER]
CLAN_STATUS_APPS: list[str] = [STATUS_WARRIOR_APP, STATUS_MEDIATOR_APP, STATUS_MEDICINE_APP]
STATUS_DEAD_GROUP: list[str] = [STATUS_DEAD_STARCLAN, STATUS_DEAD_DARK_FOREST, STATUS_DEAD_UNKNOWN_RESIDENCE]
STATUS_OUTSIDE_CLAN_GROUP: list[str] = [STATUS_KITTYPET, STATUS_LONER, STATUS_ROGUE,
                                        STATUS_EXCLAN, STATUS_EXILED]

# Patrol types
PATROL_MED: str = "gather"
PATROL_BORDER: str = "border"
PATROL_HUNT: str = "hunt"
PATROL_TRAIN: str = "train"
GENERAL_PATROLS: list[str] = [PATROL_BORDER, PATROL_HUNT, PATROL_TRAIN]


########################################################################################################################
# Decision and Interaction Keys
########################################################################################################################

INTERACTION_NEGATIVE: str = "negative_interaction"
INTERACTION_POSITIVE: str = "positive_interaction"


########################################################################################################################
# Location Keys
########################################################################################################################
# These can be combined with Cat Status
LOC_STARCLAN: str = "starclan"
LOC_DARK_FOREST: str = "hell"
LOC_DEAD_OTHER: str = "UR"  # unknown residence
LOC_NOT_CLAN: str = "outside"
LOC_CLAN: str = "inside"
DEAD_LOCATIONS: list[str] = [LOC_STARCLAN, LOC_DARK_FOREST, LOC_DEAD_OTHER]