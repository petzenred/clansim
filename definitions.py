# definitions.py - strings, paths and enums that will be used all over the project are put here to avoid inconsistencies.
# GNU Terry Pratchett

from enum import StrEnum


APP_NAME_DEFAULT: str = "ClanSim"
APP_NAME_BETA: str = "ClanSimBeta"
APP_AUTHOR: str = "ClanSim"

TIMESTR_FORMAT: str = "%Y%m%d_%H%M%S"


# This is saved in the Clan save-file, and is used for save-file conversion.
SAVE_CLANSIM_VERSION_NUMBER = 0
VERSION_CLANSIM_NUMBER: str = "0.1.0"
SAVE_CLANGEN_VERSION_NUMBER = 3
VERSION_CLANGEN_NUMBER: str = "0.9.0"


########################################################################################################################
# Paths
########################################################################################################################

# resource paths
MUSIC_PATH: str = 'resources/audio/music/'
SOUNDS_PATH: str = 'resources/audio/sounds/'
PATROL_IMAGE_PATH: str = 'resources/images/patrol_art/'

# starting at resources/lang/{language code}/
PATROL_LANG_PATH: str = 'patrols/'

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
# TODO make ScreenName a StrEnum class
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
# TODO replace strings with enum references
########################################################################################################################

# Biomes
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

def cast_to_biome(_):
    if type(_) is Biome:
        return _
    if type(_) is str:
        if _ in ["any", "Any"]:
            return Biome.Any
        if _ in ["beach", "Beach"]:
            return Biome.Beach
        if _ in ["desert", "Desert"]:
            return Biome.Desert
        if _ in ["forest", "Forest"]:
            return Biome.Forest
        if _ in ["mountainous", "Mountainous"]:
            return Biome.Mountain
        if _ in ["plains", "Plains"]:
            return Biome.Plains
        if _ in ["wetlands", "Wetlands"]:
            return Biome.Wetlands
        if _ in ["twolegplace", "Twolegplace"]:
            return Biome.Twolegplace
        raise KeyError(f"Could not cast unrecognized string to Biome: {_}")
    else:
        raise TypeError(f"Must be string to cast to Biome: {_}")

AVAILABLE_BIOMES: list[str] = [Biome.Forest, Biome.Mountain, Biome.Plains, Biome.Beach]

# Seasons
class Season(StrEnum):
    Any = "any"
    Spring = "newleaf"
    Summer = "greenleaf"
    Autumn = "leaffall"
    Winter = "leafbare"

def cast_to_season(_: str):
    if type(_) is Season:
        return _
    if type(_) is str:
        if _ in ["new-leaf", "newleaf", "New-leaf", "New-Leaf", "Newleaf"]:
            return Season.Spring
        if _ in ["greenleaf", "green-leaf", "Greenleaf", "Green-leaf", "Green-Leaf"]:
            return Season.Summer
        if _ in ["leaffall", "Leaffall", "leaf-fall", "Leaf-fall", "Leaf-Fall"]:
            return Season.Autumn
        if _ in ["leafbare", "Leafbare", "leaf-bare", "Leaf-Bare", "Leaf-bare"]:
            return Season.Winter
        raise KeyError(f"Could not cast unrecognized string to Season: {_}")
    else:
        raise TypeError(f"Must be string to cast to Biome: {_}")

AVAILABLE_SEASONS: list[Season] = [Season.Spring, Season.Summer, Season.Autumn, Season.Winter]

YEAR_SEASONS: list[Season] = [Season.Spring, Season.Spring, Season.Spring,
                              Season.Summer, Season.Summer,Season.Summer,
                              Season.Autumn, Season.Autumn, Season.Autumn,
                              Season.Winter, Season.Winter, Season.Winter]

# Cat status

class Status(StrEnum):
    """ Keeps track of a cat's position within or outside a Clan. """

    Any = "any"

    # Dead cats
    DeadStarClan = "starclan"
    DeadDarkForest = "darkforest"
    DeadUnknownResidence = "unknownresidence"

    # Non-Clan cats
    Kittypet = "kittypet"
    Loner = "loner"
    Rogue = "rogue"
    ExClan = "former Clancat"
    Exiled = "exiled"

    # Clan cats
    Leader = "leader"
    Deputy = "deputy"
    Medicine = "medicine cat"
    MedicineApp = "medicine cat apprentice"
    Mediator = "mediator"
    MediatorApp = "mediator apprentice"
    Warrior = "warrior"
    WarriorApp = "warrior apprentice" # NB: this used to be "apprentice"

    Kit = "kitten"
    Newborn = "newborn"
    Elder = "elder"
    Lost = "lost"

    @property
    def able(self):
        if self in [self.Leader, self.Deputy, self.Warrior, self.Medicine, self.Mediator, self.WarriorApp, self.MedicineApp, self.MediatorApp]:
            return True
        return False

    @property
    def dead(self):
        if self in [self.DeadStarClan, self.DeadDarkForest, self.DeadUnknownResidence]:
            return True
        return False

    @property
    def apprentice(self):
        if self in [self.MedicineApp, self.MediatorApp, self.WarriorApp]:
            return True
        return False

    @property
    def adult(self):
        if self in [self.Leader, self.Deputy, self.Medicine, self.Mediator, self.Warrior, self.Elder]:
            return True
        return False

    @property
    def outside_clan(self):
        if self in [self.Kittypet, self.Loner, self.Rogue, self.ExClan, self.Exiled]:
            return True
        return False

    @property
    def valid_hunter(self):
        if self in [self.Leader, self.Deputy, self.Warrior, self.WarriorApp]:
            return True
        return False

CLAN_ROLES_RANK_SORT_REVERSE_ORDER: list[str] = [   # This in is in reverse order: top of the list at the bottom
    Status.Elder, # Elders come last in books' CLAN ALLEGIANCES sections
    Status.Newborn,
    Status.Kit,
    Status.WarriorApp,
    Status.Warrior,
    Status.MediatorApp,
    Status.Mediator,
    Status.MedicineApp,
    Status.Medicine,
    Status.Deputy,
    Status.Leader,
]

class Age(StrEnum):
    """ Keeps track of a cat's age. """
    Newborn = "newborn"
    Kitten = "kitten"
    Adolescent = "adolescent"
    YoungAdult = "young adult"
    Adult = "adult"
    SeniorAdult = "senior adult"
    Senior = "senior"

    @property
    def is_baby(self):
        return self in (Age.Kitten, Age.Newborn)

    @property
    def is_adult(self):
        if self in [self.YoungAdult, self.Adult, self.SeniorAdult, self.Senior]:
            return True
        return False

    @property
    def can_have_mate(self):
        return self not in (Age.Kitten, Age.Newborn, Age.Adolescent)

# Patrol types
class PatrolType(StrEnum):
    General = "general"
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

def cast_to_patrol_type(_):
    if type(_) is PatrolType:
        return _
    if type(_) is str:
        if _ in ["general", "any", "General", "Any"]:
            return PatrolType.General
        if _ in ["train", "Train", "training", "Training"]:
            return PatrolType.Train
        if _ in ["border", "Border"]:
            return PatrolType.Border
        if _ in ["hunt", "Hunt", "hunting", "Hunting"]:
            return PatrolType.Hunting
        raise KeyError(f"Could not cast unrecognized string to PatrolType: {_}")
    else:
        raise TypeError(f"Must be string to cast to PatrolType: {_}")

GENERAL_PATROLS: list = [PatrolType.Border, PatrolType.Hunting, PatrolType.Train]


########################################################################################################################
# Decision and Interaction Keys
########################################################################################################################

INTERACTION_NEGATIVE: str = "negative_interaction"
INTERACTION_POSITIVE: str = "positive_interaction"


########################################################################################################################
# Location Keys
########################################################################################################################
# TODO these can be combined with Cat Status
LOC_STARCLAN: str = "starclan"
LOC_DARK_FOREST: str = "hell"
LOC_DEAD_OTHER: str = "UR"  # unknown residence
LOC_NOT_CLAN: str = "outside"
LOC_CLAN: str = "inside"
DEAD_LOCATIONS: list[str] = [LOC_STARCLAN, LOC_DARK_FOREST, LOC_DEAD_OTHER]


########################################################################################################################
# Backstories
########################################################################################################################

class Backstory(StrEnum):
    """ Background strings for cats.

    TODO
     - Cats with Guided backstories have the StarClan skill
    """

    # "%{name}'s past history is unknown."
    Unknown = "unknown"

    ##########################################################################################
    ### Non-specific backstories that I think should be randomized into other backstories. ###
    ##########################################################################################
    ClanFounder = "clan_founder" # TODO always randomize to another background
    # "m_c is one of the founding members of the Clan."

    Clans_Other = "otherclan1" # TODO have this randomly turned into one of the other Clans backstories
    # "m_c was born into another Clan, but came to this Clan by choice."

    Clans_Choice = "otherclan4" # TODO have this randomly turned into one of the other Clans backstories
    # "m_c grew up in another Clan, but chose to leave that life and join the Clan {PRONOUN/m_c/subject} now {VERB/m_c/live/lives} in."

    Clans_Exile_Ostracized = "ostracized_warrior" # TODO have this randomly turned into one of the other Clans_Exile backstories
    # "m_c was ostracized from {PRONOUN/m_c/poss} old Clan, but no one really knows why."

    Kit_Outsider = "outsider1" # TODO have this randomly turn into a different background
    # "m_c was born outside of a Clan."

    Loner_Choice = "loner1" # TODO have this randomly turned into one of the other Loner backstories
    # "m_c joined the Clan by choice after living life as a loner."

    Rogue_Choice = "rogue1" # TODO have this randomly turned into one of the other Rogue backstories
    # "m_c joined the Clan by choice after living life as a rogue."

    Kittypet_Choice = "kittypet1" # TODO have this randomly turned into one of the other Kittypet backstories
    # "m_c joined the Clan by choice after living life with Twolegs as a kittypet."

    #################
    ### Clan cats ###
    #################
    Clans_Native = "clanborn"
    # "m_c was born into the Clan where {PRONOUN/m_c/subject} currently {VERB/m_c/reside/resides}."

    Clans_Tragedy = "tragedy_survivor1"
    # "Something horrible happened to m_c's previous Clan. {PRONOUN/m_c/subject/CAP} {VERB/m_c/refuse/refuses} to speak about it."

    Clans_WashedAway = "refugee5"
    # "m_c got washed away from {PRONOUN/m_c/poss} former territory in a flood that destroyed {PRONOUN/m_c/poss} home but was glad to find a new home in {PRONOUN/m_c/poss} new Clan here."

    Clans_Unhappy = "otherclan2"
    #"m_c was unhappy in {PRONOUN/m_c/poss} old Clan and decided to come here instead."

    Clans_TyrantLeader = "refugee1" # TODO storyline: another Clan's tyrannical leader
    # "m_c came to this Clan after fleeing from {PRONOUN/m_c/poss} former Clan and the tyrannical leader that had taken over."

    Clans_Disaster = "otherclan3" # TODO storyline: another Clan stays in your camp temporarily after a flood
    # "m_c's Clan stayed with the Clan after a disaster struck {PRONOUN/m_c/poss} old one, and decided to stay after the rest of {PRONOUN/m_c/poss} Clan returned home."

    Clans_Exile_Crime = "disgraced1" # TODO storyline: what transgression did they commit?
    # "m_c was cast out of {PRONOUN/m_c/poss} old Clan for some transgression that {PRONOUN/m_c/subject}{VERB/m_c/'re/'s} not keen on talking about."

    Clans_Exile_False = "disgraced2" # TODO storyline: what was this cat falsely accused of, and who did really did it?
    # "m_c was exiled from {PRONOUN/m_c/poss} old Clan for something {PRONOUN/m_c/subject} didn't do and came here to seek safety."

    Clans_Exile_Secret = "disgraced3" # TODO storyline: what are they keeping secret that they were exiled for?
    # "m_c once held a high rank in another Clan but was exiled for reasons {PRONOUN/m_c/subject} {VERB/m_c/refuse/refuses} to share."

    Clans_FailedLeader = "retired_leader"
    # "m_c used to be the leader of another Clan before deciding {PRONOUN/m_c/subject} needed a change of scenery after leadership became too much. {PRONOUN/m_c/subject/CAP} returned {PRONOUN/m_c/poss} nine lives and let {PRONOUN/m_c/poss} deputy take over before coming here."

    Clans_Medicine = "medicine_cat" # TODO storyline: why would a medicine cat leave their old Clan?
    # "m_c was once a medicine cat in another Clan."

    Clans_Guided = "guided4" # TODO storyline: why did StarClan lead this cat to this Clan?
    # "m_c used to live in a different Clan, until a sign from StarClan told {PRONOUN/m_c/object} to leave."

    Clans_ForeignKit = "abandoned3"
    # "m_c was born into another Clan, but {PRONOUN/m_c/subject} {VERB/m_c/were/was} left here as a kit for the Clan to raise."

    HalfClan_BornHere = "halfclan1"
    # "m_c was born into the Clan, but one of {PRONOUN/m_c/poss} parents resides in another Clan."

    HalfClan_BornThere = "halfclan2"
    # "m_c was born in another Clan, but chose to come to this Clan to be with {PRONOUN/m_c/poss} other parent."

    HalfClan_ParentsHere = "halfclan3"
    # "m_c was born to parents from different Clans, but their foreign parent chose to come to this Clan to be with {PRONOUN/m_c/poss} other parent."

    HalfClan_LonerParent = "outsider_roots1"
    # "m_c was born into the Clan, but one of {PRONOUN/m_c/poss} parents is an outsider that belongs to no Clan."

    HalfClan_OutsideBirth = "outsider2"
    # "m_c was born outside of a Clan, but at {PRONOUN/m_c/poss} birth one parent was a member of a Clan."

    ########################
    ### Loner and Rogues ###
    ########################

    Loner_Barn = "loner2"
    # "m_c used to live in a barn but mostly stayed away from Twolegs. {PRONOUN/m_c/subject/CAP} decided Clan life might be an interesting change of pace."

    Loner_Wanderer = "loner3"
    # "m_c wandered the world, aimless and free, but always alone."

    Loner_Love = "loner4"
    # "m_c wandered the world, aimless and free, but always alone - until {PRONOUN/m_c/subject} found someone worth staying for."

    Loner_Tragedy = "tragedy_survivor4"
    # "m_c used to be a loner, but joined the Clan after something terrible made {PRONOUN/m_c/object} leave {PRONOUN/m_c/poss} old home behind."

    Loner_MedWander = "wandering_healer1"
    # "m_c used to wander, helping those where {PRONOUN/m_c/subject} could, and eventually found the Clan."

    Loner_MedStay = "wandering_healer2"
    # "m_c used to live in a specific spot, offering help to all who wandered by, but eventually found {PRONOUN/m_c/poss} way to the Clan."

    Loner_Refugee = "refugee2"
    # "m_c used to live as a loner, but after another cat chased {PRONOUN/m_c/object} from {PRONOUN/m_c/poss} home, {PRONOUN/m_c/subject} took refuge in the Clan."

    Loner_TyrantLeader = "refugee4"
    # "m_c used to be in a rogue group, but joined the Clan after fleeing from the group's tyrannical leader."

    Loner_Guided = "guided3"
    # "m_c used to live as a loner. A starry-furred cat appeared to {PRONOUN/m_c/object} one day, and then led {PRONOUN/m_c/object} to the Clan."

    Loner_AbandonedKit = "abandoned2"
    # "m_c was born outside of the Clan, but was brought to the Clan as a kit and has lived here ever since."

    Loner_FollowedKit = "outsider_roots2"
    # "m_c was born outside the Clan but came to live there with {PRONOUN/m_c/poss} parent at a young age."

    Rogue_Twolegplace = "rogue2"
    # "m_c used to live in a Twolegplace, scrounging for what {PRONOUN/m_c/subject} could find. {PRONOUN/m_c/subject/CAP} thought the Clan might offer {PRONOUN/m_c/object} more security."

    Rogue_ChasedOut = "rogue3"
    # "m_c used to live alone in {PRONOUN/m_c/poss} own territory, but was chased out by something and eventually found the Clan."

    Rogue_Tragedy = "tragedy_survivor2"
    # "m_c used to be part of a rogue group, but joined the Clan after something terrible happened to it."

    Rogue_Guided = "guided2"
    # "m_c used to live a rough life as a rogue. While wandering, {PRONOUN/m_c/subject} found a set of starry pawprints, and followed them to the Clan."

    #################
    ### Kittypets ###
    #################
    Kittypet_Boat = "kittypet2"
    # "m_c used to live on something called a 'boat' with Twolegs, but decided to join the Clan."

    Kittypet_Moved = "kittypet3"
    # "m_c used to be a kittypet. {PRONOUN/m_c/subject/CAP} got lost after wandering away, and when {PRONOUN/m_c/subject} returned home, {PRONOUN/m_c/subject} found {PRONOUN/m_c/poss} Twolegs were gone. {PRONOUN/m_c/subject/CAP} eventually found {PRONOUN/m_c/poss} way to the Clan."

    Kittypet_Abandoned = "kittypet4"
    # "m_c used to be a kittypet. One day, {PRONOUN/m_c/subject} got sick, and {PRONOUN/m_c/poss} Twolegs brought {PRONOUN/m_c/object} into the belly of a monster. The Twolegs then left {PRONOUN/m_c/object} to fend for {PRONOUN/m_c/self}."

    Kittypet_Cruel = "refugee3"
    # "m_c used to be a kittypet, but joined the Clan after fleeing from {PRONOUN/m_c/poss} cruel Twoleg."

    Kittypet_Sick = "refugee6" # TODO storyline: this cat wants to return to their Twolegs
    # "m_c used to be a kittypet, but joined the Clan, sick and weak after eating something {PRONOUN/m_c/subject} shouldn't have."

    Kittypet_Tragedy = "tragedy_survivor3"
    # "m_c used to be a kittypet, but joined the Clan after something terrible happened to {PRONOUN/m_c/poss} Twolegs."

    Kittypet_Guided = "guided1"
    # "m_c used to be a kittypet, but after dreaming of starry-furred cats, {PRONOUN/m_c/subject} followed their whispers to the Clan."

    ##################
    ### Foundlings ###
    ##################

    Kit_Foundling = "abandoned1"
    # "m_c was found with a deceased parent. The Clan took {PRONOUN/m_c/object} in, but doesn't hide where {PRONOUN/m_c/subject} came from."

    Kit_Twoleg = "abandoned4"
    # "m_c was found and taken in after being abandoned by {PRONOUN/m_c/poss} Twolegs as a kit."

    Kit_Aware = "orphaned1"
    # "m_c was found with a deceased parent. The Clan took {PRONOUN/m_c/object} in, but doesn't hide where {PRONOUN/m_c/subject} came from."

    Kit_Unaware = "orphaned2"
    # "m_c was found with a deceased parent. The Clan took {PRONOUN/m_c/object} in, but doesn't tell {PRONOUN/m_c/object} where {PRONOUN/m_c/subject} really came from."

    Kit_CarWreck = "orphaned3"
    # "m_c was found as a kit among the wreckage of a Monster with no parents in sight and got brought to live in the Clan."

    Kit_Battlefield = "orphaned4"
    # TODO storyline: who fought the battle, and why was a kit there?
    #   Maybe it was a battle between two other Clans, and one was wiped out?
    # "m_c was found as a kit hiding near a place of battle where there were no survivors and got brought to live in the Clan."

    Kit_ParentBodies = "orphaned5"
    # "m_c was found as a kit hiding near {PRONOUN/m_c/poss} parents' bodies and got brought to live in the Clan."

    Kit_Ocean = "orphaned6"
    # "m_c was found flailing in the ocean as a teeny kitten, no parent in sight."

    Kit_LostParent = "outsider3"
    # "m_c was born outside of the Clan, while {PRONOUN/m_c/poss} parent was lost."

    @property
    def clanborn_backstories(self):
        """ Return True if a backstory indicates that the Cat was born into the Clans. """
        if self in [
            self.ClanFounder, self.Clans_Other, self.Clans_Choice, self.Clans_Exile_Ostracized,
            self.Clans_Native, self.Clans_Tragedy, self.Clans_WashedAway, self.Clans_Unhappy,
            self.Clans_TyrantLeader, self.Clans_Disaster, self.Clans_Exile_Crime, self.Clans_Exile_False,
            self.Clans_Exile_Secret, self.Clans_FailedLeader, self.Clans_Medicine, self.Clans_Guided,
            self.Clans_ForeignKit,
        ]:
            return True
        return False

    @property
    def half_clan_backstories(self):
        """ Return True if a backstory indicates that the Cat is half-Clan. """
        if self in [
            self.HalfClan_BornHere, self.HalfClan_BornThere, self.HalfClan_ParentsHere, self.HalfClan_LonerParent,
            self.HalfClan_OutsideBirth,
        ]:
            return True
        return False

    @property
    def loner_backstories(self):
        """ Return True if a backstory indicates that the Cat was a loner before joining a Clan. """
        if self in [
            self.Kit_Outsider, self.Loner_Choice, self.Loner_Barn, self.Loner_Wanderer,
            self.Loner_Love, self.Loner_Tragedy, self.Loner_MedWander, self.Loner_MedStay,
            self.Loner_Refugee, self.Loner_TyrantLeader, self.Loner_Guided, self.Loner_FollowedKit,
            self.Loner_AbandonedKit,
        ]:
            return True
        return False

    @property
    def rogue_backstories(self):
        """ Return True if a backstory indicates that the Cat was a rogue before joining a Clan. """
        if self in [
            self.Kit_Outsider, self.Rogue_Choice, self.Rogue_Twolegplace, self.Rogue_ChasedOut,
            self.Rogue_Tragedy, self.Rogue_Guided,
        ]:
            return True
        return False

    @property
    def kittypet_backstories(self):
        """ Return True if a backstory indicates that the Cat was a kittypet before joining a Clan. """
        if self in [
            self.Kit_Outsider, self.Kittypet_Boat, self.Kittypet_Moved, self.Kittypet_Abandoned,
            self.Kittypet_Cruel, self.Kittypet_Sick, self.Kittypet_Tragedy, self.Kittypet_Guided,
        ]:
            return True
        return False

    @property
    def outsider_backstories(self):
        """ """
        if self.loner_backstory or self.loner_backstory or self.rogue_backstory or self.kittypet_backstory:
            return True
        return False

    @property
    def clanborn_backstories(self):
        """ Return True if a backstory indicates that the Cat was born into the Clans. """
        return self.clan_backstories

    @property
    def orphaned_backstories(self):
        """ """
        if self in [
            self.Kit_Foundling, self.Kit_Twoleg, self.Kit_Aware, self.Kit_Unaware,
            self.Kit_CarWreck, self.Kit_Battlefield, self.Kit_ParentBodies, self.Kit_Ocean,
            self.HalfClan_OutsideBirth, self.Kit_LostParent,
            self.Loner_AbandonedKit, self.Loner_FollowedKit, self.Clans_ForeignKit,
        ]:
            return True
        return False

    # @property
    # def abandoned_backstories(self):
    #     """ """
