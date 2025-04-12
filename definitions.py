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
BIOME_BEACH_KEY: str = "beach"
BIOME_DESERT_KEY: str = "desert"
BIOME_FOREST_KEY: str = "forest"
BIOME_MOUNTAIN_KEY: str = "mountainous"
BIOME_PLAINS_KEY: str = "plains"
BIOME_WETLANDS_KEY: str = "wetlands"
BIOME_TWOLEGPLACE_KEY: str = "twolegplace"
BIOME_KEYS: list[str] = [BIOME_BEACH_KEY, BIOME_DESERT_KEY, BIOME_FOREST_KEY, BIOME_MOUNTAIN_KEY,
                         BIOME_PLAINS_KEY, BIOME_WETLANDS_KEY, BIOME_TWOLEGPLACE_KEY]
IMPLEMENTED_BIOMES: list[str] = [BIOME_BEACH_KEY, BIOME_FOREST_KEY, BIOME_MOUNTAIN_KEY, BIOME_PLAINS_KEY]

# Seasons
SPRING_KEY: str = "newleaf"
SUMMER_KEY: str = "greenleaf"
AUTUMN_KEY: str = "leaffall"
WINTER_KEY: str = "leafbare"
YEAR_SEASONS: list[str] = [SPRING_KEY, SPRING_KEY, SPRING_KEY,
                           SUMMER_KEY, SUMMER_KEY, SUMMER_KEY,
                           AUTUMN_KEY, AUTUMN_KEY, AUTUMN_KEY,
                           WINTER_KEY, WINTER_KEY, WINTER_KEY]

# Clan roles
ROLE_LEADER_KEY: str = "leader"
ROLE_DEPUTY_KEY: str = "deputy"
ROLE_MEDICINE_KEY: str = "medicine cat"
ROLE_MEDICINE_APP_KEY: str = "medicine cat apprentice"
ROLE_MEDIATOR_KEY: str = "mediator"
ROLE_MEDIATOR_APP_KEY: str = "mediator apprentice"
ROLE_WARRIOR_KEY: str = "warrior"
ROLE_WARRIOR_APP_KEY: str = "apprentice"
ROLE_KIT_KEY: str = "kitten"
ROLE_NEWBORN_KEY: str = "newborn"
ROLE_ELDER_KEY: str = "elder"
CLAN_ROLES_RANK_SORT_REVERSE_ORDER: list[str] = [   # This in is in reverse order: top of the list at the bottom
    ROLE_ELDER_KEY, # Elders come last in books' CLAN ALLEGIANCES sections
    ROLE_NEWBORN_KEY,
    ROLE_KIT_KEY,
    ROLE_WARRIOR_APP_KEY,
    ROLE_WARRIOR_KEY,
    ROLE_MEDIATOR_APP_KEY,
    ROLE_MEDIATOR_KEY,
    ROLE_MEDICINE_APP_KEY,
    ROLE_MEDICINE_KEY,
    ROLE_DEPUTY_KEY,
    ROLE_LEADER_KEY,
]
CLAN_ROLES_ADULTS: list[str] = [ROLE_LEADER_KEY, ROLE_DEPUTY_KEY, ROLE_MEDICINE_KEY,
                                ROLE_MEDIATOR_KEY, ROLE_WARRIOR_KEY, ROLE_ELDER_KEY]
CLAN_ROLES_APPS: list[str] = [ROLE_WARRIOR_APP_KEY, ROLE_MEDIATOR_APP_KEY, ROLE_MEDICINE_APP_KEY]

# Patrol types
PATROL_MED_KEY: str = "gather"
PATROL_BORDER_KEY: str = "border"
PATROL_HUNT_KEY: str = "hunt"
PATROL_TRAIN_KEY: str = "train"
GENERAL_PATROLS: list[str] = [PATROL_BORDER_KEY, PATROL_HUNT_KEY, PATROL_TRAIN_KEY]


########################################################################################################################
# Decision and Interaction Keys
########################################################################################################################

NEGATIVE_INTERACTION_KEY: str = "negative_interaction"
POSITIVE_INTERACTION_KEY: str = "positive_interaction"


########################################################################################################################
# Location Keys
########################################################################################################################

LOC_STARCLAN_KEY: str = "starclan"
LOC_DARK_FOREST_KEY: str = "hell"
LOC_DEAD_OTHER_KEY: str = "UR"
LOC_NOT_CLAN_KEY: str = "outside"
LOC_CLAN_KEY: str = "inside"
DEAD_LOCATIONS: list[str] = [LOC_STARCLAN_KEY, LOC_DARK_FOREST_KEY, LOC_DEAD_OTHER_KEY]