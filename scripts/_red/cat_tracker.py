# cat_tracker.py - Keeps track of all cats in the game.
from typing import Optional

# TODO replace all references to game.switches["clan_list"] with references to cat_tracker.all_clans
# TODO calling Cat.die() moves a cat from living_cats to dead_cats
# TODO add the player's Clan, eventually
# TODO add the StarClan and DF guides

########################################################################################################################
# Imports
########################################################################################################################

# This module is imported by game, which imports Cat and Clan (which imports Cat as well

from definitions import LONER_CLAN_TOKEN, Location, LocationCategory, Rank, SpecialClanToken
from scripts._red.config_manager import config

import logging
logger = logging.getLogger(__name__)


########################################################################################################################
# Classes
########################################################################################################################

class CatTracker:
    """ Used to keep track of all cats and Clans in the game. """

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! IMPORTANT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
    # Don't access any members of this class directly! Only use the methods, since     #
    # are set up with safety measures to prevent cats and Clans from being tracked     #
    # incorrectly.                                                                     #
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! IMPORTANT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #

    _last_id: int # the last ID given to a newly generated cat

    all_clans: dict # dict[clan_token, Clan object] - only extant Clans
    destroyed_clans: dict # dict[clan_token, Clan object] - only destroyed Clans
    all_clans_ever: dict # dict[clan_token, Clan object] - all Clans ever generated in the
                         # active save file, extant and destroyed.

    living_cats: dict # dict[cat_id, Cat object] - only living cats
    sc_guide_cat_id: int
    df_guide_cat_id: int
    dead_cats_by_location: dict[Location, dict] # dict[ Location, dict[cat_id, Cat object] ]
    all_cats_ever: dict # dict[cat_id, RedCat object] - contains every RedCat and/or
                        # FadedCat object ever generated in the save file, alive and dead.

    # -------------------------- Used for specific purposes -------------------------- #

    # living_clan_healers is used to make some patrol filtering easier
    living_clan_healers: list # list[*healer objects]
    # TODO when will this be used?
    living_professional_queens_by_clan_token: dict[str, list] # dict[clan token, list[*queen objects]]

    # used when rationing freshkill and when writing the Clan Allegiances screen
    living_nursing_queens_and_kits_by_clan_token: dict # dict[clan token, dict[queen object, list[*kit objects]]]

    # scripts.game_structure.load_cat

    def __init__(self, last_id=0):
        self._last_id = last_id

        self.all_clans = {}
        self.destroyed_clans = {}
        self.all_clans_ever = {}

        self.living_cats = {}
        self.dead_cats_by_location = {
            Location.StarClan: {},
            Location.DarkForest: {},
            Location.OutsiderAfterlife: {},
            Location.GhostResidence: {},
            Location.RiverOfSpirits: {},
            Location.TribeEndlessHunting: {},
            Location.TheAncestors: {},
        }
        self.all_cats_ever = {}

        self.living_clan_healers = []
        self.living_professional_queens_by_clan_token = {}
        self.living_nursing_queens_and_kits_by_clan_token = {}
        return

    # ------------------------------------ GETTER ------------------------------------ #

    def _get_new_id(self) -> int:
        """ Get the next ID available for a newly generated cat. """
        self._last_id += 1
        if self._last_id in self.all_cats_ever.keys():
            return self._get_new_id()
        else:
            return self._last_id

    def _get_clan_and_queen_of_kit(self, kit_obj):
        """ Get the RedCat object for the queen looking after a kit.

        :param kit_obj: the kit whose Clan and queen are to be fetched

        :return: the token of the Clan the kit belongs to,
                and either the queen looking after them or None is there isn't one
        :rtype: tuple[str, RedCat]
        """
        for clan_token in self.living_nursing_queens_and_kits_by_clan_token:
            qc = self.living_nursing_queens_and_kits_by_clan_token[clan_token]
            for queen in qc:
                if kit_obj in qc[queen]:
                    return clan_token, queen
        raise ValueError(f"Can't find which queen the kit {kit_obj.name} belongs to")

    def get_clan_object(self, clan_token: str):
        """ Get a Clan object when you have the Clan's token.

        :param str clan_token: the Clan's identifying token
        :return: the RedClan object corresponding to clan_token
        """
        return self.all_clans_ever[clan_token]

    def get_cat_objects(self, cat_id: int | list[int]) -> list:
        """ Get a RedCat object.

        :param list cat_id: the ID(s) of the cat(s) requested
        :return: list of the RedCat objects with the requested IDs
        """
        result: list = []
        if isinstance(cat_id, int):
            result.append(self.all_cats_ever[cat_id])
        elif isinstance(cat_id, list):
            for _ in cat_id:
                result.append(self.all_cats_ever[_])
        else:
            raise TypeError(f"Can't get cat objects from the cat tracker without an int or list of ints. Was "
                            f"given a {type(cat_id)} instead")
        return result

    def get_name_prefixes_of_clan(self, clan_token: str):
        clan_obj = self.all_clans[clan_token]
        return [c.name.prefix for c in clan_obj.clan_cats.values()]

    # ------------------------------------ SETTER ------------------------------------ #

    def add_cat_to_tracker(self, cat_obj, cat_id: int = None) -> int:
        """ Add a cat to the cat tracker.

        :param RedCat cat_obj: the RedCat object
        :param int cat_id: the already-set ID of the cat object (used if reading a save file)
        :return: the ID of the cat
        """
        if not cat_id:
            cat_id = self._get_new_id()
        self.all_cats_ever[cat_id] = cat_obj

        # if alive, add the cat to living_cats
        if cat_obj.alive:
            self.living_cats[cat_id] = cat_obj

            # don't add queens or healers to the relevant trackers because if a cat
            # with that rank is kicked out of their Clan, we don't want them added here
        # if dead, add to the appropriate afterlife
        else:
            self.dead_cats_by_location[cat_obj.location][cat_obj.cat_id] = cat_obj

        return cat_id

    def kill_cat(self, cat_obj, afterlife: Location):
        """ Update how a cat is tracked after it dies.

        :param RedCat cat_obj: the cat who's died
        :param Location afterlife: where the cat is going after it dies.
        :raises ValueError: if location.category isn't LocationCategory.Afterlife
        """
        logger.debug(f"Killing cat {cat_obj.name} in the cat tracker")

        if afterlife.category is not LocationCategory.Afterlife:
            raise ValueError(f"Can't send dead cat {cat_obj.name} to non-afterlife location: {afterlife}")

        # update the cat's Clan object
        clan_obj = self.all_clans_ever[cat_obj.clan_token]
        clan_obj.remove_cat_from_clan(cat_obj)
        if cat_obj.rank is Rank.Leader:
            clan_obj.past_leader_ids.append(cat_obj.cat_id)
        elif cat_obj.rank is Rank.Deputy:
            clan_obj.past_deputy_ids.append(cat_obj.cat_id)

        # move the cat from the list of living cats to their appropriate afterlife, unless they're faded
        if not cat_obj.faded:
            self.dead_cats_by_location[afterlife][cat_obj.cat_id] = cat_obj

        # REMOVE FROM SPECIFIC LIVING CAT TRACKERS
        # remove a healer
        if cat_obj in self.living_clan_healers:
            self.remove_healer_cat(cat_obj=cat_obj)
            clan_obj.past_healer_ids.append(cat_obj.cat_id)

        # remove a professional queen
        if cat_obj.rank.is_queen:
            self.remove_professional_queen(clan_token=clan_obj.clan_token, cat_obj=cat_obj)

        # remove a kit
        if cat_obj.moons < config.cat_config.adolescent_age_moons:
            self.remove_kit_from_queen(kit_obj=cat_obj)

        # remove a nursing queen
        for kit in self.remove_nursing_queen(clan_token=cat_obj.clan_token, cat_obj=cat_obj):
            # add the kits they were nursing to 'None'
            self.give_kit_to_queen(clan_token=cat_obj.clan_token, kit_obj=kit)

        return

    def add_new_clan(self, clan_obj):
        """ Add a Clan to the tracker. This should happen BEFORE any cats are added to the RedClan object.

        :param Clan clan_obj: the new Clan object to add to the tracker
        """
        logger.debug(f"CatTracker.add_new_clan ( {clan_obj.clan_token} )")

        # make sure there isn't already a Clan named this
        extant_clan_names = [c for c in self.all_clans] # note that this allows for a destroyed Clan to be revived
        if clan_obj.clan_token in extant_clan_names:
            raise KeyError(f"There's already a Clan with the token {clan_obj.clan_token}! There can't be two")
        # if the Clan name isn't repeated, add it to the tracker
        self.all_clans[clan_obj.clan_token] = clan_obj
        self.all_clans_ever[clan_obj.clan_token] = clan_obj
        self.living_nursing_queens_and_kits_by_clan_token[clan_obj.clan_token] = { None: [] }
        if not clan_obj.clan_token == SpecialClanToken.Loners:
            # outsiders don't have professional queens
            self.living_professional_queens_by_clan_token[clan_obj.clan_token] = []
        return

    def destroy_clan(self, clan_obj):
        """ Update a Clan in the tracker after it's destroyed.

        Also moves all the RedCat objects in the Clan to be loners.

        :param Clan clan_obj: the Clan object representing the Clan that's been destroyed
        """
        logger.debug(f"CatTracker.destroy_clan( {clan_obj.clan_token} )")

        # make sure the Clan exists before it's destroyed
        if clan_obj.clan_token not in self.all_clans:
            raise ValueError(f"cat_tracker was told to destroy the Clan associated with token {clan_obj.clan_token}, "
                             f"but that token doesn't currently exist")

        # add all the cats in the destroyed Clan to Outsiders
        # NB: don't remove clan_cats_by_rank in case you want to check
        #   who the leader of a destroyed Clan was, or the like
        for cat_id, cat_obj in clan_obj.items():
            self.change_cat_clan(new_clan_token=LONER_CLAN_TOKEN, cat_obj=cat_obj)

        # update how the Clan is tracked
        self.all_clans.pop(clan_obj.clan_token)
        self.destroyed_clans[clan_obj.clan_token] = clan_obj
        self.living_nursing_queens_and_kits_by_clan_token.pop(clan_obj.clan_token)

        return

    # TODO
    def add_new_cat_to_clan(self, clan_token: str, cat_obj):
        """ Add a newly-created cat to a Clan. Does not handle cats switching Clans.

        Does not change cat_obj.rank or cat_obj.clan_token.

        Called by RedClan.add_cat_to_clan().

        :param str clan_token: the Clan's identifying token
        :param RedCat cat_obj: the cat object
        """
        if clan_token not in self.all_clans.keys():
            raise KeyError(f"Can't add cat #{cat_obj.cat_id} to Clan with token \"{clan_token}\" "
                           f"because there is no Clan in the cat tracker with that token.")

        # stuff that's the same for all cats
        self.all_clans

        # professional queens
        if cat_obj.rank.is_queen:
            if clan_token != LONER_CLAN_TOKEN:
                self.add_queen(cat_obj=cat_obj, clan_token=clan_token, professional=True)

        # nursing queens
        # if a nursing queen switches clans, they automatically bring their kits with them
        cat_is_a_nursing_queen_f: bool = False # FIXME how do I figure this out?
        if cat_is_a_nursing_queen_f:
            self.add_queen(cat_obj=cat_obj, clan_token=clan_token, professional=False)

        # healers
        if cat_obj.rank.is_healer:
            if clan_token != LONER_CLAN_TOKEN:
                self.add_healer_cat(cat_obj=cat_obj)

        raise NotImplementedError("CatTracker.add_new_cat_to_clan")

    # FIXME handle kits properly
    def change_cat_clan(self, new_rank: Rank, new_clan_token: str, cat_obj,
                        moving_kit_with_queen=False, foundling_kit=False, queen_obj=None):
        """ Change which Clan a living or dead cat belongs to.

        Called by RedCat.change_clan().
        """
        old_clan_token: str = cat_obj.clan_token
        logger.debug(f"Moving {cat_obj.name} from group with token \"{old_clan_token}\" to group with "
                     f"token \"{new_clan_token}\" in the cat tracker")

        # make sure a Cat isn't moved 'between' the same Clan
        if new_clan_token == old_clan_token:
            logger.warning(f"{cat_obj.name} can't become a member of group with token {new_clan_token} "
                             f"because {cat_obj.name} already is one")
            return

        # update RedCat object
        cat_obj.clan_token = new_clan_token

        # if the cat is leaving the Clans, remove them from the list of healers
        if new_clan_token == SpecialClanToken.Loners:
            self.remove_healer_cat(cat_obj=cat_obj)

        # handle specific ranks
        # FIXME new
        # don't need to call remove_professional_queen or remove_healer_cat because those are called by RedClan
        if new_clan_token == SpecialClanToken.Loners:
            self.remove_healer_cat(cat_obj=cat_obj)
        self.remove_professional_queen(clan_token=old_clan_token, cat_obj=cat_obj)

        # FIXME old
        # healers
        # case 1: Clan healer moving to a different warrior Clan
        #   you don't need to do anything here, since the list of healer cats isn't split up by Clan
        # case 2: Clan healer becoming an outsider
        if new_clan_token == LONER_CLAN_TOKEN:
            self.remove_healer_cat(cat_obj=cat_obj)
        # case 3: outsider becoming a Clan healer
        if old_clan_token == LONER_CLAN_TOKEN and new_rank in (Rank.Healer, Rank.HealerApp,):
            self.add_healer_cat(cat_obj=cat_obj)
        # case 1: professional Clan queen moving to a different warrior Clan
        if LONER_CLAN_TOKEN not in (new_clan_token, old_clan_token) and cat_obj.rank.is_queen:
            self.old_remove_nursing_queen(clan_token=old_clan_token, cat_obj=cat_obj)
            self.add_queen(cat_obj=cat_obj, clan_token=new_clan_token, professional=True)
        # case 2: professional Clan queen becoming an outsider
        if new_clan_token == LONER_CLAN_TOKEN and cat_obj.rank.is_queen:
            # FIXME and cat_obj in self.living_nursing_queens_and_kits_by_clan_token[old_clan_token][Rank.Queen]
            self.old_remove_nursing_queen(clan_token=old_clan_token, cat_obj=cat_obj)
        # case 3: outsider joining a Clan as a professional queen (like Daisy!)
        if old_clan_token == LONER_CLAN_TOKEN and cat_obj.rank.is_queen:
            self.add_queen(cat_obj=cat_obj, clan_token=new_clan_token, professional=True)

        # nursing queens
        # if a nursing queen switches clans, they automatically bring their kits with them
        if cat_obj in self.living_nursing_queens_and_kits_by_clan_token[old_clan_token]:
            self.add_queen(cat_obj=cat_obj, clan_token=new_clan_token, professional=False)
            kits = self.old_remove_nursing_queen(clan_token=old_clan_token, cat_obj=cat_obj)
            for kit in kits:
                self.change_cat_clan(new_rank=new_rank, new_clan_token=new_clan_token,
                                     cat_obj=kit, queen_obj=cat_obj, )
                self.give_kit_to_queen(clan_token=new_clan_token, kit_obj=kit, new_queen_obj=cat_obj, )

        # kits FIXME - need to call RedCat.change_clan
        # if cat_obj.moons < config.cat_config.adolescent_age_moons and queen_obj:

        # foundlings
        if foundling_kit:
            self.give_kit_to_queen(clan_token=new_clan_token, kit_obj=cat_obj, new_queen_obj=None)

        # kits who aren't automatically being moved with their queen
        if (not moving_kit_with_queen or foundling_kit) and (cat_obj.moons < config.cat_config.adolescent_age_moons):
            raise ValueError(f"Kits can't move Clans independently!")
            # FIXME handle foundlings

        # update RedClan objects
        self.all_clans_ever[old_clan_token].remove_cat_from_clan(cat_obj=cat_obj)
        self.all_clans_ever[new_clan_token].add_cat_to_clan(cat_obj=cat_obj)

        return

    def add_healer_cat(self, cat_obj):
        """ Add a cat to the list of living healers.

        Catches cats who are already healers without throwing an error.

        Called by RedClan.new_healer_or_app().

        :param RedCat cat_obj: the cat to add to the list of living healers.
        """
        logger.debug(f"Adding {cat_obj.name} to list of healers in the cat tracker")
        if cat_obj not in self.living_clan_healers:
            self.living_clan_healers.append(cat_obj)
        return

    def remove_healer_cat(self, cat_obj):
        """ Remove a cat from the list of living healers.

        Catches cats who aren't healers without throwing an error.

        Called by the RedClan.remove_cat_from_clan() and RedClan.change_rank().

        :param RedCat cat_obj: the cat to remove from the list of living healers.
        """
        logger.debug(f"Removing {cat_obj.name} from list of healers in the cat tracker")
        if cat_obj in self.living_clan_healers:
            self.living_clan_healers.remove(cat_obj)
        return

    def add_queen(self, cat_obj, clan_token: str, professional: bool = False):
        """ Add a cat to the list of queens in their current Clan.

        Called by RedClan.change_rank(), and CatTracker.change_cat_clan().

        :param RedCat cat_obj: the queen to add
        :param str clan_token: the Clan's identifying token
        :param bool professional: True if the cat is a professional queen, False if they're a nursing queen
        """
        # make sure that the None object is always in the list of nursing queens
        if None not in self.living_nursing_queens_and_kits_by_clan_token[clan_token].keys():
            self.living_nursing_queens_and_kits_by_clan_token[clan_token][None] = []

        if cat_obj and professional and clan_token != SpecialClanToken.Loners:
            logger.debug(f"Adding professional queen {cat_obj.name} to group with token {clan_token}")
            self.living_professional_queens_by_clan_token[clan_token].append(cat_obj)
        elif cat_obj:
            logger.debug(f"Adding nursing queen {cat_obj.name} to group with token {clan_token}")
            self.living_nursing_queens_and_kits_by_clan_token[clan_token][cat_obj] = []
        else:
            logger.debug(f"Not adding {cat_obj} to any list of queens")
            return

    def remove_professional_queen(self, clan_token: str, cat_obj):
        """ Remove a professional queen from the queen tracker.

        Catches cats who aren't queens without throwing an error.

        :param str clan_token: the Clan's identifying token
        :param RedCat cat_obj: the queen to remove
        """
        if cat_obj and cat_obj.rank.is_queen:
            logger.debug(f"Removing professional queen {cat_obj.name} from Clan with token \"{clan_token}\"")
            self.living_nursing_queens_and_kits_by_clan_token[clan_token].remove(cat_obj)
        return

    def remove_nursing_queen(self, clan_token: str, cat_obj) -> list:
        """ Remove a nursing queen from the queen tracker.

        Catches cats who aren't queens without throwing an error.

        :param str clan_token: the Clan's identifying token
        :param RedCat cat_obj: the queen to remove
        :return: if the queen has is looking after any kits, list of RedCat objects of kits the queen was looking after
        """
        if cat_obj and cat_obj in self.living_nursing_queens_and_kits_by_clan_token[clan_token]:
            logger.debug(f"Removing nursing queen {cat_obj.name} from Clan with token \"{clan_token}\"")
            return self.living_nursing_queens_and_kits_by_clan_token[clan_token].pop(cat_obj)
        return []

    def old_remove_nursing_queen(self, clan_token: str, cat_obj) -> list:
        """ Remove a nursing queen from the queen tracker.

        Catches cats who aren't queens without throwing an error.

        :param str clan_token: the Clan's identifying token
        :param RedCat cat_obj: the queen to remove
        :return: if the queen has is looking after any kits, list of RedCat objects of kits the queen was looking after
        """
        if cat_obj and cat_obj in self.living_nursing_queens_and_kits_by_clan_token[clan_token]:
            logger.debug(f"Removing nursing queen {cat_obj.name} from Clan with token \"{clan_token}\"")
            return self.living_nursing_queens_and_kits_by_clan_token[clan_token].pop(cat_obj)
        return []

    def give_kit_to_queen(self, clan_token: str, kit_obj, new_queen_obj=None):
        """ Add a kit to the care of a queen. If the kit is currently being cared for by a different queen,
        this method will automatically remove the kit from the other queen's care first.

        Called when kits join a Clan, because they're either born or found.

        :param str clan_token: the Clan's identifying token
        :param RedCat kit_obj: kitten to add to the care of the given queen
        :param RedCat new_queen_obj: the queen to look after the kit. Default value is None
        :raises ValueError: if the kit and the new queen are not in the same Clan
        """
        if new_queen_obj:
            logger.debug(f"Giving kit {kit_obj.name} to care of queen {new_queen_obj.name} in cat tracker")
            if not kit_obj.clan_token == new_queen_obj.clan_token:
                raise ValueError(f"Before {new_queen_obj.name} can care for {kit_obj.name}, "
                                 f"they must belong to the same Clan")
        else:
            logger.debug(f"Giving kit {kit_obj.name} to queen 'None' in cat tracker")
        # remove the kit from the care of their old queen
        try:
            clan_token, old_queen_obj = self._get_clan_and_queen_of_kit(kit_obj)
            if old_queen_obj is not None:
                self.remove_kit_from_queen(kit_obj)
        except:
            # the kit didn't have a current queen
            pass
        # add the kit to the care of their new queen
        if not new_queen_obj in self.living_nursing_queens_and_kits_by_clan_token[clan_token]:
            self.add_queen(cat_obj=new_queen_obj, clan_token=clan_token)
        # this works because when you grab a list specifically, you get the list itself, not a copy
        self.living_nursing_queens_and_kits_by_clan_token[clan_token][new_queen_obj].append(kit_obj)
        return

    def remove_kit_from_queen(self, kit_obj):
        """ Remove a kitten from the care of a queen.

        :param RedCat kit_obj: kitten to remove from the care of their current queen
        """
        clan_token, queen_obj = self._get_clan_and_queen_of_kit(kit_obj)
        if queen_obj:
            logger.debug(f"Removing kit {kit_obj.name} from the care of queen {queen_obj.name}")
        else:
            logger.debug(f"Removing kit {kit_obj.name} from the care of queen None")
        self.living_nursing_queens_and_kits_by_clan_token[clan_token][queen_obj].remove(kit_obj)
        # if the nursing queen is out of kits, remove them
        if not self.living_nursing_queens_and_kits_by_clan_token[clan_token][queen_obj] and queen_obj is not None:
            self.old_remove_nursing_queen(clan_token=clan_token, cat_obj=queen_obj)
        return
