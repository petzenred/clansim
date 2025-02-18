# definitions.py - a map for


APP_NAME_DEFAULT = "ClanSim"
APP_NAME_BETA = "ClanSimBeta"
APP_AUTHOR = "ClanSim"


# This is saved in the Clan save-file, and is used for save-file conversion.
CLANSIM_SAVE_VERSION_NUMBER = 0
CLANSIM_VERSION_NUMBER = "0.1.0"
CLANGEN_SAVE_VERSION_NUMBER = 3
CLANGEN_VERSION_NUMBER = "0.9.0"


# paths


# scripts paths
SPRITE_PATHS: dict = {
    'lineart': {'sprites/lineart/'},
    'tints': {'sprites/tints/'},
    'faded': {'sprites/faded/'},
    'paralyzed': {'sprites/paralyzed/'},
    'accessories': {'sprites/accessories/'},
    'april_fools': {'sprites/april_fools/'}
}

# screen names
MAIN_MENU_SCREEN_NAME = "main menu screen"
MAIN_SETTINGS_SCREEN_NAME = "main settings screen"
NEW_CLAN_SCREEN_NAME = "new clan screen"
SWITCH_CLAN_SCREEN_NAME = "switch clan screen"

PROFILE_SCREEN_NAME = "profile screen"
PROFILE_ADOPT_SCREEN_NAME = "choose adoptive parent screen"
PROFILE_CEREMONY_SCREEN_NAME = "leader ceremony screen"
PROFILE_FAMILY_SCREEN_NAME = "family tree screen"
PROFILE_GENDER_SCREEN_NAME = "change gender screen"
PROFILE_MATE_SCREEN_NAME = "choose mate screen"
PROFILE_MEDIATION_SCREEN_NAME = "mediation screen"
PROFILE_MENTOR_SCREEN_NAME = "choose mentor screen"
PROFILE_RELATIONSHIPS_SCREEN_NAME = "relationship screen"
PROFILE_ROLE_SCREEN_NAME = "role screen"
PROFILE_SPRITE_INSPECT_SCREEN_NAME = "sprite inspect screen"

CLAN_ALLEGIANCES_SCREEN_NAME = "allegiances screen"
CLAN_CAMP_SCREEN_NAME = "camp screen"
CLAN_FRESHKILL_SCREEN_NAME = "fresh-kill pile screen"
CLAN_EVENTS_SCREEN_NAME = "events screen"
CLAN_MEMBERS_SCREEN_NAME = "members screen"
CLAN_PATROL_SCREEN_NAME = "patrol screen"
CLAN_SETTINGS_SCREEN_NAME = "clan settings screen"

MED_DEN_SCREEN_NAME = "med den screen"
LEADER_DEN_SCREEN_NAME = "leader den screen"
WARRIOR_DEN_SCREEN_NAME = "warrior den screen"

CREATION_SCREENS = [NEW_CLAN_SCREEN_NAME]
MAIN_MENU_SCREENS = [MAIN_SETTINGS_SCREEN_NAME, MAIN_MENU_SCREEN_NAME, SWITCH_CLAN_SCREEN_NAME]
