# red_backstory.py - 
from enum import StrEnum

from definitions import Location

class RedBackstoryCategory(StrEnum):
    """ Categories for backstory strings. """

    Unknown = "unknown"

    Clanborn = "Clanborn"
    HalfClan = "HalfClan"
    Loner = "loner"
    Rogue = "rogue"
    Kittypet = "kittypet"
    Foundling = "orphaned"

    @property
    def outsider(self):
        if self in (self.Loner, self.Rogue, self.Kittypet):
            return True
        return False

class RedBackstory(StrEnum):
    """ Background strings for cats.

    TODO
     - Cats with Guided backstories have the StarClan skill
     - Randomize generic backgrounds, maybe using the cast_to_backstory() method?
     - {CLAN/cat.main/birth.loc}

    FIXME
     - CONJU vs VERB
    """

    # "%{name}'s past history is unknown."
    Unknown = "unknown"

    ##########################################################################################
    ### Non-specific backstories that I think should be randomized into other backstories. ###
    ##########################################################################################
    # "clan_founder"
    # TODO always randomize to another background
    ClanFounder = "{CAT/main} is one of the founding members of {CLAN/main}Clan."

    # "otherclan1"
    # TODO have this randomly turned into one of the other Clans backstories
    Clans_Other1 = "{CAT/main} was born into another Clan, but came to {CLAN/main}Clan by choice."

    # "otherclan4"
    # TODO have this randomly turned into one of the other Clans backstories
    Clans_Other2 = ("{CAT/main} grew up in another Clan, but chose to leave that life and "
                    "live in {CLAN/main}Clan instead.")

    # "ostracized_warrior"
    # TODO have this randomly turned into one of the other Clans_Exile backstories
    Clans_Exile_Ostracized = "{CAT/main} was ostracized from {PRONOUN/main/poss} old Clan, but no one really knows why."

    # "outsider1"
    # TODO have this randomly turn into a different background
    Kit_Outsider = "{CAT/main} was born outside of the Clans."

    # "loner1"
    # TODO have this randomly turned into one of the other Loner backstories
    Loner_Choice = "{CAT/main} joined {CLAN/main}Clan by choice after living life as a loner."

    # "rogue1"
    # TODO have this randomly turned into one of the other Rogue backstories
    Rogue_Choice = "{CAT/main} joined {CLAN/main}Clan by choice after tiring of life as a rogue."

    # "kittypet1"
     # TODO have this randomly turned into one of the other Kittypet backstories
    Kittypet_Choice = "{CAT/main} joined {CLAN/main}Clan by choice after living life with Twolegs as a kittypet."

    #################
    ### Clan cats ###
    #################

    # "clanborn"
    NativeClan = ("{CAT/main} was born in {CLAN/main}Clan, where {PRONOUN/m_c/subject} currently "
                  "{VERB/m_c/reside/resides}.")

    NativeKittypet = ("{CAT/main} was born a kittypet, and is content to stay with their Twolegs, "
                      "at least for the moment.")

    NativeLoner = "{CAT/main} is and always has been a loner. They don't seem to be interested in joining a Clan."

    NativeRogue = "{CAT/main} is and always has been a rogue. They don't seem to be interested in joinging a Clan."

    ###################
    ### Other Clans ###
    ###################

    # "tragedy_survivor1"
    ClansOtherTragedy = ("Something horrible happened to {CAT/main}'s previous Clan. {PRONOUN/main/subject/CAP} "
                         "{CONJU/main/refuse/refuses} to speak about it.")

    # "refugee5"
    ClansOtherWashedAway = ("CAT/main} got washed away from {PRONOUN/main/poss} former territory in a flood that "
                            "destroyed {PRONOUN/main/poss} home but was glad to find a new home in {CLAN/main}Clan.")

    # "otherclan2"
    # TODO change to "{CAT/main} was unhappy in {CLAN/main/birth} and decided to move to {CLAN/main/current} instead."
    ClansOtherUnhappy = "{CAT/main} was unhappy in {PRONOUN/main/poss} old Clan and decided to come here instead."

    # "refugee1"
    # TODO storyline: another Clan's tyrannical leader
    ClansOtherTyrantLeader = ("{CAT/main} came to {CLAN/main}Clan after fleeing from {PRONOUN/main/poss} former "
                              "Clan and the tyrannical leader that had taken over.")

    # "otherclan3"
    # TODO storyline: another Clan stays in your camp temporarily after a flood
    ClansOtherDisaster = ("{CAT/main}\'s Clan stayed with {CLAN/main}Clan after a disaster struck {PRONOUN/main/poss} "
                          "old one, and decided to stay after the rest of {PRONOUN/main/poss} Clan returned home.")

    # "disgraced1"
    # TODO storyline: what transgression did they commit?
    ClansOtherExileCrime = ("{CAT/main} was cast out of {PRONOUN/main/poss} old Clan for some transgression "
                            "that {PRONOUN/main/subject}{CONJU/main/'re/'s} not keen on talking about.")

    # "disgraced2"
    # TODO storyline: what was this cat falsely accused of, and who did really did it?
    ClansOtherExileFalse = ("{CAT/main} was exiled from {PRONOUN/main/poss} old Clan for something "
                            "{PRONOUN/main/subject} didn't do and came here to seek safety.")

    # "disgraced3"
    # TODO storyline: what are they keeping secret that they were exiled for?
    ClansOtherExileHighRank = ("{CAT/main} once held a high rank in another Clan but was exiled "
                               "for reasons {PRONOUN/main/subject} {CONJU/main/refuse/refuses} to share.")

    # "retired_leader"
    # TODO remove this, e.g. have retired_leader replaced with a different backstory - maybe ClansOtherExileHighRank
    # ClansOtherFailedLeader = ("{CAT/main} used to be the leader of {CLAN/other} before deciding "
    #                           "{PRONOUN/main/subject} needed a change of scenery after leadership became too much. "
    #                           "{PRONOUN/main/subject/CAP} returned {PRONOUN/main/poss} nine lives and let "
    #                           "{PRONOUN/main/poss} deputy take over before coming to {CLAN/main}Clan.")

    # "healer"
    # TODO storyline: why would a healer leave their old Clan?
    ClansOtherHealer = "{CAT/main} was once a healer in another Clan."

    # "guided4"
    # TODO storyline: why did StarClan lead this cat to this Clan?
    Clans_Guided =  ("{CAT/main} used to live in a different Clan, until a sign from StarClan told "
                     "{PRONOUN/main/object} to leave.")

    # "abandoned3"
    # TODO replace the random {CLAN/other} with a specific reference to whichever Clan that main was born into
    # TODO replace 'left here' with 'left somewhere specific'?
    Clans_ForeignKit = ("{CAT/main} was born in {CLAN/other}, but {PRONOUN/main/subject} {CONJU/main/were/was} "
                        "left here as a kit for {CLAN/main}Clan to raise.")

    # "halfclan1"
    HalfClan_BornHere = ("{CAT/main} was born into {CLAN/main}Clan, but one of {PRONOUN/main/poss} "
                         "parents resides in another Clan.")

    # "halfclan2"
    HalfClan_BornThere = ("{CAT/main} was born in another Clan, but chose to come to {CLAN/main}Clan "
                          "to be with {PRONOUN/main/poss} other parent.")

    # "halfclan3"
    # TODO deal with difference between ClanGen and LifeGen "halfclan3"
    HalfClan_ParentsHere = ("{CAT/main} was born to parents from different Clans, but their foreign parent "
                            "chose to come to {CLAN/main}Clan to be with {PRONOUN/m_c/poss} other parent.")

    # "outsider_roots1"
    HalfClan_LonerParent = ("{CAT/main} was born into {CLAN/main}Clan, but one of {PRONOUN/main/poss} "
                            "parents is an outsider that belongs to no Clan.")

    # "outsider2"
    # TODO how did they end up in {CLAN/main}Clan?
    HalfClan_OutsideBirth = ("{CAT/main} was born outside of a Clan, but at {PRONOUN/main/poss} birth one parent "
                             "was a member of a Clan.")

    #########################
    ### Loners and Rogues ###
    #########################

    # "loner2"
    Loner_Barn = ("{CAT/main} used to live in a barn, but mostly stayed away from Twolegs. {PRONOUN/main/subject/CAP} "
                  "decided Clan life might be an interesting change of pace.")

    # "loner3"
    # TODO deal with difference between ClanGen and LifeGen "loner3"
    Loner_Wanderer = ("{CAT/main} wandered the world, aimless and free, but always alone - until {PRONOUN/main/subject}"
                      " found {CLAN/main}Clan and finally found somewhere {PRONOUN/main/subject} "
                      "{CONJU/main/think/thinks} {PRONOUN/main/subject} might belong.")

    # "loner4"
    # TODO deal with difference between ClanGen and LifeGen "loner4"
    Loner_Love = ("{CAT/main} wandered the world, aimless and free, but always alone - "
                  "until {PRONOUN/main/subject} found someone worth staying for.")

    # "tragedy_survivor4"
    Loner_Tragedy = ("{CAT/main} used to be a loner, but joined {CLAN/main}Clan after something terrible made "
                     "{PRONOUN/main/object} leave {PRONOUN/main/poss} old home behind.")

    # "wandering_healer1"
    Loner_HealerWander = ("{CAT/main} used to wander, helping those where {PRONOUN/main/subject} could, and "
                       "eventually found {CLAN/main}Clan.")

    # "wandering_healer2"
    Loner_HealerStay = ("{CAT/main} used to live in a specific spot, offering help to all who "
                     "wandered by, but eventually found {PRONOUN/main/poss} way to {CLAN/main}Clan.")

    LonerHealerLearn = "{CAT/main} joined {CLAN/main}Clan to hone in on {PRONOUN/main/poss} healing skills."

    # "refugee2"
    Loner_Refugee = ("{CAT/main} used to live as a loner, but after another cat chased "
                     "{PRONOUN/main/object} from {PRONOUN/main/poss} home, {PRONOUN/main/subject} "
                     "took refuge in {CLAN/main}Clan.")

    # "guided3"
    Loner_Guided = ("{CAT/main} used to live as a loner. A starry-furred cat appeared to "
                    "{PRONOUN/main/object} one day, and then led {PRONOUN/main/object} to the Clan.")

    # abandoned2
    # TODO brought by who?
    Loner_AbandonedKit = ("{CAT/main} was born outside of {CLAN/main}Clan, but was brought by {CAT/main/rel.parent} "
                          "as a kit and has lived here ever since.")

    # "outsider_roots2"
    Loner_FollowedKit = ("{CAT/main} was born outside {CLAN/cat.main/birth.loc}, but came to live in "
                         "{CLAN/main}Clan with {PRONOUN/main/poss} parent at a young age.")

    # "rogue2"
    Rogue_Twolegplace = ("{CAT/main} used to live in a Twolegplace, scrounging for what {PRONOUN/main/subject} "
                         "could find. {PRONOUN/main/subject/CAP} thought living in {CLAN/main}Clan might offer "
                         "{PRONOUN/main/object} more security.")

    # "rogue3"
    Rogue_ChasedOut = ("{CAT/main} used to live alone in {PRONOUN/main/poss} own territory, but was "
                       "chased out by something and eventually found {CLAN/main}Clan.")

    # "tragedy_survivor2"
    Rogue_Tragedy = ("{CAT/main} used to be part of a rogue group, but joined {CLAN/main}Clan after "
                     "something terrible happened to it.")

    # "refugee4"
    # TODO storyline - a rogue group lead by a tyrannical leader
    Rogue_TyrantLeader = ("{CAT/main} used to be in a rogue group, but joined {CLAN/main}Clan after "
                          "fleeing from the group's tyrannical leader.")

    # "guided2"
    Rogue_Guided = ("{CAT/main} used to live a rough life as a rogue. While wandering, {PRONOUN/main/subject} "
                    "found a set of starry pawprints, and followed them to the Clan.")

    #################
    ### Kittypets ###
    #################
    # "kittypet2"
    Kittypet_Boat = ("{CAT/main} used to live on something called a 'boat' with Twolegs, but "
                     "decided to join {CLAN/main}Clan.")

    # "kittypet3"
    # TODO storyline: this cat wants to return to their Twolegs
    Kittypet_Moved = ("{CAT/main} used to be a kittypet. {PRONOUN/main/subject/CAP} got lost after wandering away, "
                      "and when {PRONOUN/main/subject} returned home, {PRONOUN/main/subject} found "
                      "{PRONOUN/main/poss} Twolegs were gone. {PRONOUN/main/subject/CAP} eventually found "
                      "{PRONOUN/main/poss} way to {CLAN/main}Clan.")

    # "kittypet4"
    Kittypet_Abandoned = ("{CAT/main} used to be a kittypet. One day, {PRONOUN/main/subject} got sick, "
                          "and {PRONOUN/main/poss} Twolegs brought {PRONOUN/main/object} into the belly "
                          "of a monster. The Twolegs then left {PRONOUN/main/object} to fend for "
                          "{PRONOUN/main/self}.")

    #     "refugee3"
    Kittypet_Cruel = ("{CAT/main} used to be a kittypet, but joined {CLAN/main}Clan after fleeing from "
                      "{PRONOUN/main/poss} cruel Twoleg.")

    # "refugee6"
    # TODO storyline: this cat wants to return to their Twolegs
    Kittypet_Sick = ("{CAT/main} used to be a kittypet, but joined {CLAN/main}Clan after being found sick and weak "
                     "after eating something {PRONOUN/main/subject} shouldn't have.")

    # "tragedy_survivor3"
    Kittypet_Tragedy = ("{CAT/main} used to be a kittypet, but joined {CLAN/main}Clan after something "
                        "terrible happened to {PRONOUN/main/poss} Twolegs.")

    # "guided1"
    Kittypet_Guided = ("{CAT/main} used to be a kittypet, but after dreaming of starry-furred cats, "
                       "{PRONOUN/main/subject} followed their whispers to the Clan.")

    ##################
    ### Foundlings ###
    ##################

    # "abandoned1"
    # TODO deal with difference between ClanGen and LifeGen backstory "abandoned1" and "orphaned1"
    Kit_Foundling = "{CAT/main} was found by {CLAN/main}Clan as a kit and has been living with them ever since."
    # "m_c was found with a deceased parent. The Clan took {PRONOUN/m_c/object} in, but doesn't hide where
    # {PRONOUN/m_c/subject} came from."

    # "abandoned4"
    Kit_Twoleg = "{CAT/main} was found and taken in after being abandoned by {PRONOUN/main/poss} Twolegs as a kit."

    # "orphaned1"
    Kit_Aware = ("{CAT/main} was found with a deceased parent. {CLAN/main}Clan took {PRONOUN/main/object} "
                 "in, but doesn't hide where {PRONOUN/main/subject} came from.")

    # "orphaned2"
    Kit_Unaware = ("{CAT/main} was found with a deceased parent. {CLAN/main}Clan took {PRONOUN/main/object} in, but "
                   "doesn't tell {PRONOUN/main/object} where {PRONOUN/main/subject} really came from." )

    # "orphaned3"
    Kit_CarWreck = ("{CAT/main} was found as a kit among the wreckage of a Monster with no parents "
                    "in sight and got brought to live in {CLAN/main}Clan.")

    # "orphaned4"
    # TODO storyline: who fought the battle, and why was a kit there?
    #   Maybe it was a battle between two other Clans, and one was wiped out?
    Kit_Battlefield = ("{CAT/main} was found as a kit hiding near a place of battle where there were "
                       "no survivors and got brought to live in {CLAN/main}Clan.")

    # "orphaned5"
    Kit_ParentBodies = ("{CAT/main} was found as a kit hiding near {PRONOUN/main/poss} parent's bodies "
                        "and got brought to live in {CLAN/main}Clan.")

    # "orphaned6"
    Kit_Ocean = "{CAT/main} was found flailing in the ocean as a teeny kit, no parent in sight."

    # "orphaned7"
    Kit_Fox = ("{CAT/main} was found stashed high up in a tree with claw marks marking the base. "
               "No parents were found nearby, however there were fox paw prints not too far away.")

    # "outsider3"
    Kit_LostParent = "{CAT/main} was born outside of a Clan, while {PRONOUN/main/poss} parent was lost."

    @property
    def category(self):
        """ Get a backstory's category. """
        if self in (
            self.ClanFounder, self.Clans_Other1, self.Clans_Other2, self.Clans_Exile_Ostracized,
            self.NativeClan, self.ClansOtherTragedy, self.ClansOtherWashedAway, self.ClansOtherUnhappy,
            self.ClansOtherTyrantLeader, self.ClansOtherDisaster, self.ClansOtherExileCrime, self.ClansOtherExileFalse,
            self.ClansOtherExileHighRank, self.ClansOtherFailedLeader, self.ClansOtherHealer, self.Clans_Guided,
            self.Clans_ForeignKit,
        ):
            return RedBackstoryCategory.Clanborn
        if self in (
            self.HalfClan_BornHere, self.HalfClan_BornThere, self.HalfClan_ParentsHere, self.HalfClan_LonerParent,
            self.HalfClan_OutsideBirth,
        ):
            return RedBackstoryCategory.HalfClan
        if self in (
                self.Kit_Outsider, self.Loner_Choice, self.Loner_Barn, self.Loner_Wanderer,
                self.Loner_Love, self.Loner_Tragedy, self.Loner_HealerWander, self.Loner_HealerStay,
                self.Loner_Refugee, self.Rogue_TyrantLeader, self.Loner_Guided, self.Loner_FollowedKit,
                self.Loner_AbandonedKit,
        ):
            return RedBackstoryCategory.Loner
        if self in (
            self.Kit_Outsider, self.Rogue_Choice, self.Rogue_Twolegplace, self.Rogue_ChasedOut,
            self.Rogue_Tragedy, self.Rogue_Guided,
        ):
            return RedBackstoryCategory.Rogue
        if self in (
            self.Kit_Outsider, self.Kittypet_Boat, self.Kittypet_Moved, self.Kittypet_Abandoned,
            self.Kittypet_Cruel, self.Kittypet_Sick, self.Kittypet_Tragedy, self.Kittypet_Guided,
        ):
            return RedBackstoryCategory.Kittypet
        if self in (
            self.Kit_Foundling, self.Kit_Twoleg, self.Kit_Aware, self.Kit_Unaware,
            self.Kit_CarWreck, self.Kit_Battlefield, self.Kit_ParentBodies, self.Kit_Ocean,
            self.HalfClan_OutsideBirth, self.Kit_LostParent,
            self.Loner_AbandonedKit, self.Loner_FollowedKit, self.Clans_ForeignKit,
        ):
            return RedBackstoryCategory.Foundling
        return RedBackstoryCategory.Unknown

    @property
    def afterlife(self):
        """ Which afterlife should cats with a certain backstory go to? """
        if self.category in (RedBackstoryCategory.Clanborn, RedBackstoryCategory.HalfClan, RedBackstoryCategory.Foundling, ):
            return Location.StarClan
        # TODO account for DarkForest Clan cats
        return Location.OutsiderAfterlife

def cast_to_backstory(to_cast) -> RedBackstory:
    """ If possible, return a RedBackstory object.

     :param to_cast: something to be cast to a RedBackstory object
     :ptype: str, RedBackstory, NoneType
     :return RedBackstory: None returns Any; RedBackstorys return themselves; strings will be matched to
        enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, RedBackstory, or NoneType object
     """
    if isinstance(to_cast, RedBackstory):
        return to_cast
    if isinstance(to_cast, str):
        bks = [b for b in list(RedBackstory) if b.value.casefold() == to_cast.casefold()]
        if bks:
            return bks[0]
        else:
            raise KeyError(f"Could not cast unrecognized string to RedBackstory: {to_cast}")
    if to_cast is None:
        return RedBackstory.Unknown
    raise TypeError(f"Must be string, None, or RedBackstory to cast to RedBackstory. Can't "
                    f"cast {type(to_cast)} to RedBackstory")


def cast_to_backstory_category(to_cast) -> RedBackstoryCategory:
    """ If possible, return a RedBackstoryCategory object.

     :param to_cast: something to be cast to a RedBackstoryCategory object
     :ptype: str, RedBackstoryCategory, NoneType
     :return RedBackstoryCategory: None returns Any; BackstoryCategorys return themselves; strings will be matched
        to enum member strings.
     :raises KeyError: if to_cast is a string, and there is no corresponding enum member for to_cast
     :raises TypeError: if to_cast isn't a str, RedBackstoryCategory, or NoneType object
     """
    if isinstance(to_cast, RedBackstoryCategory):
        return to_cast
    if isinstance(to_cast, str):
        bkc = [b for b in list(RedBackstoryCategory) if b.value.casefold() == to_cast.casefold()]
        if bkc:
            return bkc[0]
        else:
            raise KeyError(f"Could not cast unrecognized string to RedBackstoryCategory: {to_cast}")
    if to_cast is None:
        return RedBackstoryCategory.Unknown
    raise TypeError(f"Must be string, None, or RedBackstoryCategory to cast to RedBackstoryCategory. Can't "
                    f"cast {type(to_cast)} to RedBackstoryCategory")
