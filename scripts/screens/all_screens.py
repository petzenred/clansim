from definitions import (
    MAIN_MENU_SCREEN_NAME,
    MAIN_SETTINGS_SCREEN_NAME,
    NEW_CLAN_SCREEN_NAME,
    SWITCH_CLAN_SCREEN_NAME,

    PROFILE_SCREEN_NAME,
    PROFILE_ADOPT_SCREEN_NAME,
    PROFILE_CEREMONY_SCREEN_NAME,
    PROFILE_FAMILY_SCREEN_NAME,
    PROFILE_GENDER_SCREEN_NAME ,
    PROFILE_MATE_SCREEN_NAME,
    PROFILE_MEDIATION_SCREEN_NAME,
    PROFILE_MENTOR_SCREEN_NAME,
    PROFILE_RELATIONSHIPS_SCREEN_NAME,
    PROFILE_ROLE_SCREEN_NAME,
    PROFILE_SPRITE_INSPECT_SCREEN_NAME,

    CLAN_ALLEGIANCES_SCREEN_NAME,
    CLAN_CAMP_SCREEN_NAME,
    CLAN_FRESHKILL_SCREEN_NAME,
    CLAN_EVENTS_SCREEN_NAME,
    CLAN_MEMBERS_SCREEN_NAME,
    CLAN_PATROL_SCREEN_NAME,
    CLAN_SETTINGS_SCREEN_NAME,

    MED_DEN_SCREEN_NAME,
    LEADER_DEN_SCREEN_NAME,
    WARRIOR_DEN_SCREEN_NAME
)

from .ClanAllegiancesScreen import ClanAllegiancesScreen
from .ProfileCeremonyScreen import ProfileCeremonyScreen
from .ProfileGenderScreen import ProfileGenderScreen
from .ProfileAdoptScreen import ProfileAdoptScreen
from .ProfileMateScreen import ProfileMateScreen
from .ProfileMentorScreen import ProfileMentorScreen
from .ClanCampScreen import ClanCampScreen
from .ClanSettingsScreen import ClanSettingsScreen
from .ClanFreshkillScreen import ClanFreshkillScreen
from .ClanEventsScreen import ClanEventsScreen
from .ProfileFamilyScreen import ProfileFamilyScreen
from .LeaderDenScreen import LeaderDenScreen
from .ClanMembersScreen import ClanMembersScreen
from .NewClanScreen import NewClanScreen
from .MedDenScreen import MedDenScreen
from .ProfileMediationScreen import ProfileMediationScreen
from .ClanPatrolScreen import ClanPatrolScreen
from .ProfileScreen import ProfileScreen
from .ProfileRelationshipsScreen import ProfileRelationshipsScreen
from .ProfileRoleScreen import ProfileRoleScreen
from .Screens import Screens
from .MainSettingsScreen import MainSettingsScreen
from .ProfileSpriteInspectScreen import ProfileSpriteInspectScreen
from .MainMenuScreen import MainMenuScreen
from .SwitchClanScreen import SwitchClanScreen
from .WarriorDenScreen import WarriorDenScreen

# ---------------------------------------------------------------------------- #
#                                  UI RULES                                    #
# ---------------------------------------------------------------------------- #
"""
SCREEN: 700 height x 800 width

MARGINS: 25px on all sides
    ~Any new buttons or text MUST be within these margins.
    ~Buttons on the edge of the screen should butt up right against the margin. 
    (i.e. the <<Main Menu button is placed 25px x 25px on most screens) 
    
BUTTONS:
    ~Buttons are 30px in height. Width can be anything, though generally try to keep to even numbers.
    ~Square icons are 34px x 34px.
    ~Generally keep text at least 5px away from the right and left /straight/ (do not count the rounded ends) edge 
    of the button (this rule is sometimes broken. the goal is to be consistent across the entire screen or button type)
    ~Generally, the vertical gap between buttons should be 5px
"""


class AllScreens:
    screens = Screens()

    main_menu_screen = MainMenuScreen(MAIN_MENU_SCREEN_NAME)
    main_settings_screen = MainSettingsScreen(MAIN_SETTINGS_SCREEN_NAME)
    new_clan_screen = NewClanScreen(NEW_CLAN_SCREEN_NAME)
    switch_clan_screen = SwitchClanScreen(SWITCH_CLAN_SCREEN_NAME)

    profile_screen = ProfileScreen(PROFILE_SCREEN_NAME)
    profile_adopt_screen = ProfileAdoptScreen(PROFILE_ADOPT_SCREEN_NAME)
    profile_ceremony_screen = ProfileCeremonyScreen(PROFILE_CEREMONY_SCREEN_NAME)
    profile_family_screen = ProfileFamilyScreen(PROFILE_FAMILY_SCREEN_NAME)
    profile_gender_screen = ProfileGenderScreen(PROFILE_GENDER_SCREEN_NAME)
    profile_mate_screen = ProfileMateScreen(PROFILE_MATE_SCREEN_NAME)
    profile_mediation_screen = ProfileMediationScreen(PROFILE_MEDIATION_SCREEN_NAME)
    profile_mentor_screen = ProfileMentorScreen(PROFILE_MENTOR_SCREEN_NAME)
    profile_relationship_screen = ProfileRelationshipsScreen(PROFILE_RELATIONSHIPS_SCREEN_NAME)
    profile_role_screen = ProfileRoleScreen(PROFILE_ROLE_SCREEN_NAME)
    profile_sprite_inspect_screen = ProfileSpriteInspectScreen(PROFILE_SPRITE_INSPECT_SCREEN_NAME)
    
    clan_allegiances_screen = ClanAllegiancesScreen(CLAN_ALLEGIANCES_SCREEN_NAME)
    clan_camp_screen = ClanCampScreen(CLAN_CAMP_SCREEN_NAME)
    clan_events_screen = ClanEventsScreen(CLAN_EVENTS_SCREEN_NAME)
    clan_freshkill_screen = ClanFreshkillScreen(CLAN_FRESHKILL_SCREEN_NAME)
    clan_members_screen = ClanMembersScreen(CLAN_MEMBERS_SCREEN_NAME)
    clan_patrol_screen = ClanPatrolScreen(CLAN_PATROL_SCREEN_NAME)
    clan_settings_screen = ClanSettingsScreen(CLAN_SETTINGS_SCREEN_NAME)

    leader_den_screen = LeaderDenScreen(LEADER_DEN_SCREEN_NAME)
    med_den_screen = MedDenScreen(MED_DEN_SCREEN_NAME)
    warrior_den_screen = WarriorDenScreen(WARRIOR_DEN_SCREEN_NAME)
    
    @classmethod
    def rebuild_all_screens(cls):
        cls.screens = Screens()

        cls.main_menu_screen = MainMenuScreen(MAIN_MENU_SCREEN_NAME)
        cls.main_settings_screen = MainSettingsScreen(MAIN_SETTINGS_SCREEN_NAME)
        cls.new_clan_screen = NewClanScreen(NEW_CLAN_SCREEN_NAME)
        cls.switch_clan_screen = SwitchClanScreen(SWITCH_CLAN_SCREEN_NAME)

        cls.profile_screen = ProfileScreen(PROFILE_SCREEN_NAME)
        cls.profile_adopt_screen = ProfileAdoptScreen(PROFILE_ADOPT_SCREEN_NAME)
        cls.profile_ceremony_screen = ProfileCeremonyScreen(PROFILE_CEREMONY_SCREEN_NAME)
        cls.profile_family_screen = ProfileFamilyScreen(PROFILE_FAMILY_SCREEN_NAME)
        cls.profile_gender_screen = ProfileGenderScreen(PROFILE_GENDER_SCREEN_NAME)
        cls.profile_mate_screen = ProfileMateScreen(PROFILE_MATE_SCREEN_NAME)
        cls.profile_mediation_screen = ProfileMediationScreen(PROFILE_MEDIATION_SCREEN_NAME)
        cls.profile_mentor_screen = ProfileMentorScreen(PROFILE_MENTOR_SCREEN_NAME)
        cls.profile_relationship_screen = ProfileRelationshipsScreen(PROFILE_RELATIONSHIPS_SCREEN_NAME)
        cls.profile_role_screen = ProfileRoleScreen(PROFILE_ROLE_SCREEN_NAME)
        cls.profile_sprite_inspect_screen = ProfileSpriteInspectScreen(PROFILE_SPRITE_INSPECT_SCREEN_NAME)

        cls.clan_allegiances_screen = ClanAllegiancesScreen(CLAN_ALLEGIANCES_SCREEN_NAME)
        cls.clan_camp_screen = ClanCampScreen(CLAN_CAMP_SCREEN_NAME)
        cls.clan_events_screen = ClanEventsScreen(CLAN_EVENTS_SCREEN_NAME)
        cls.clan_freshkill_screen = ClanFreshkillScreen(CLAN_FRESHKILL_SCREEN_NAME)
        cls.clan_members_screen = ClanMembersScreen(CLAN_MEMBERS_SCREEN_NAME)
        cls.clan_patrol_screen = ClanPatrolScreen(CLAN_PATROL_SCREEN_NAME)
        cls.clan_settings_screen = ClanSettingsScreen(CLAN_SETTINGS_SCREEN_NAME)

        cls.leader_den_screen = LeaderDenScreen(LEADER_DEN_SCREEN_NAME)
        cls.med_den_screen = MedDenScreen(MED_DEN_SCREEN_NAME)
        cls.warrior_den_screen = WarriorDenScreen(WARRIOR_DEN_SCREEN_NAME)
