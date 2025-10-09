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

from definitions import OUTSIDER_CLAN_PREFIX, Location, LocationCategory, Rank
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

    all_clans: dict # dict{clan_prefix: Clan object} - only extant Clans
    destroyed_clans: dict # dict{clan_prefix: Clan object} - only destroyed Clans
    all_clans_ever: dict # dict{clan_prefix: Clan object} - all Clans ever generated in the
                         # active save file, extant and destroyed.

    all_cats: dict # dict{cat_id: Cat object} - only living cats
    sc_guide_cat_id: int
    df_guide_cat_id: int
    dead_cats_starclan: list # list of Cat and FadedCat objects
    dead_cats_darkforest: list # list of Cat and FadedCat objects
    dead_cats_outsider_afterlife: list # list of Cat and FadedCat objects
    all_cats_ever: dict # dict{cat_id: RedCat object} - contains every RedCat and/or
                        # FadedCat object ever generated in the save file, alive and dead.


    # -------------------------- Used for specific purposes -------------------------- #

    # living_medicine_cats is used to make some patrol filtering easier
    living_medicine_cats: list

    # used when rationing freshkill and when writing the Clan Allegiances screen
    # dict{clan_prefix: {Rank.Queen: [RedCat, RedCat], Rank.QueenApp: [RedCat], queen_obj: [kit_obj, kit_obj]} }
    living_queens_and_kits_by_clan_prefix: dict

    # scripts.game_structure.load_cat

    def __init__(self, last_id=0):
        self._last_id = last_id

        self.all_clans = {}
        self.destroyed_clans = {}
        self.all_clans_ever = {}

        self.all_cats = {}
        self.dead_cats_starclan = []
        self.dead_cats_darkforest = []
        self.dead_cats_outsider_afterlife = []
        self.all_cats_ever = {}

        self.living_medicine_cats = []
        self.living_queens_and_kits_by_clan_prefix = {
            OUTSIDER_CLAN_PREFIX: {None: []}
        } # note that outsiders don't have professional queens
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
        """ Get the RedCat object for the queen looking after a kit. """
        for clan_prefix in self.living_queens_and_kits_by_clan_prefix:
            qc = self.living_queens_and_kits_by_clan_prefix[clan_prefix]
            for queen in qc:
                if kit_obj in qc[queen]:
                    return clan_prefix, queen
        raise ValueError(f"Can't find which queen the kit {kit_obj.name} belongs to")

    def get_clan_object(self, clan_prefix: str):
        """ Get a Clan object when you have the Clan's prefix.

        :param str clan_prefix: the Clan's name prefix (e.g. "Thunder" for ThunderClan)
        :return Clan: the Clan object corresponding to clan_prefix
        """
        return self.all_clans_ever[clan_prefix]

    def get_cat_objects(self, cat_id: int | list[int]) -> list[int]:
        """ Get a RedCat object.

        :param list cat_id: the ID(s) of the cat(s) requested
        :return list[RedCat]: list of the RedCat objects with the requested IDs
        """
        result: list = []
        if isinstance(cat_id, int):
            result.append(self.all_cats_ever[cat_id])
        else:
            for _ in cat_id:
                result.append(self.all_cats_ever[_])
        return result

    def get_name_prefixes_of_clan(self, clan_prefix: str):
        clan_obj = self.all_clans[clan_prefix]
        return [c.name.prefix for c in clan_obj.clan_cats.values()]

    # ------------------------------------ SETTER ------------------------------------ #

    def set_afterlife_guides(self, sc_cat_id: int, df_cat_id: int):
        self.sc_guide_cat_id = sc_cat_id
        self.df_guide_cat_id = df_cat_id
        return

    def add_new_clan(self, clan_obj):
        """ Add a Clan to the tracker.

        :param Clan clan_obj: the new Clan object to add to the tracker
        """
        logger.debug(f"CatTracker.add_new_clan ( {clan_obj.clan_prefix} )")

        # make sure there isn't already a Clan named this
        extant_clan_names = [c for c in self.all_clans] # note that this allows for a destroyed Clan to be revived
        if clan_obj.clan_prefix in extant_clan_names:
            raise ValueError(f"There's already a Clan called {clan_obj.clan_prefix}! There can't be two")
        # if the Clan name isn't repeated, add it to the tracker
        self.all_clans[clan_obj.clan_prefix] = clan_obj
        self.all_clans_ever[clan_obj.clan_prefix] = clan_obj
        if clan_obj.clan_prefix == OUTSIDER_CLAN_PREFIX:
            # outsiders don't have professional queens
            self.living_queens_and_kits_by_clan_prefix.update({clan_obj.clan_prefix: {None: []}})
        else:
            self.living_queens_and_kits_by_clan_prefix.update({clan_obj.clan_prefix: {None: [], Rank.Queen: []}})
        return

    def destroy_clan(self, clan_obj):
        """ Update a Clan in the tracker after it's destroyed.

        Also moves all the RedCat objects in the Clan to be loners.

        :param Clan clan_obj: the Clan object representing the Clan that's been destroyed
        """
        logger.debug(f"CatTracker.destroy_clan( {clan_obj.clan_prefix} )")

        # make sure the Clan exists before it's destroyed
        if clan_obj.clan_prefix not in self.all_clans:
            raise ValueError(f"cat_tracker was told to destroy {clan_obj.clan_prefix}Clan, "
                             f"but that Clan doesn't currently exist")

        # add all the cats in the destroyed Clan to Outsiders
        # NB: don't remove clan_cats_by_rank in case you want to check
        #   who the leader of a destroyed Clan was, or the like
        clan_cat_ids: list[int] = list(clan_obj.clan_cats.keys())
        for cat_id in clan_cat_ids:
            cat_obj = clan_obj.clan_cats.pop(cat_id)
            self.all_clans[OUTSIDER_CLAN_PREFIX].clan_cats[cat_id] = cat_obj

        # update how the Clan is tracked
        self.all_clans.pop(clan_obj.clan_prefix)
        self.destroyed_clans[clan_obj.clan_prefix] = clan_obj

        return

    def add_new_cat_to_clan(self, new_clan_prefix: str, cat_obj):
        """ Add a newly-created cat to a Clan. Does not handle the cat leaving their old Clan.

        Does not change cat_obj.rank or cat_obj.clan_prefix.

        Called by RedClan.add_cat_to_clan().
        """

        # professional queens
        if cat_obj.rank in (Rank.Queen, Rank.QueenApp):
            # case 1: a professional Clan queen moves to a different warrior Clan
            if new_clan_prefix != OUTSIDER_CLAN_PREFIX:
                self.add_queen(clan_prefix=new_clan_prefix, professional=True, cat_obj=cat_obj)
            # case 2: a professional Clan queen becomes an outsider
            # do nothing
            # case 3: an outsider joins a Clan (never automatically become a professional queen)
            # do nothing

        # nursing queens
        # if a nursing queen switches clans, they automatically bring their kits with them

    def change_cat_clan(self, new_clan_prefix: str, cat_obj, moving_kit_with_queen=False):
        """ Change which Clan a living or dead cat belongs to. """
        old_clan_prefix: str = cat_obj.clan_prefix
        logger.debug(f"Moving {cat_obj.name} from "
              f"{f"{old_clan_prefix}Clan" if old_clan_prefix != OUTSIDER_CLAN_PREFIX else "outsiders"} to "
              f"{f"{new_clan_prefix}Clan" if new_clan_prefix != OUTSIDER_CLAN_PREFIX else "outsiders"} "
              f"in the cat tracker")

        # make sure a Cat isn't moved 'between' the same Clan
        if new_clan_prefix == old_clan_prefix:
            raise ValueError(f"{cat_obj.name} can't become a member of "
                             f"{f"{new_clan_prefix}Clan" if new_clan_prefix != OUTSIDER_CLAN_PREFIX else "outsiders"} "
                             f"because {cat_obj.name} already is one")

        # update Clan objects
        self.all_clans_ever[old_clan_prefix].remove_cat_from_clan(cat_obj)
        self.all_clans_ever[new_clan_prefix].add_cat_to_clan(cat_obj)

        # professional queens
        # case 1: professional Clan queen moving to a different warrior Clan
        if ((OUTSIDER_CLAN_PREFIX not in (new_clan_prefix, old_clan_prefix)) and
                cat_obj in self.living_queens_and_kits_by_clan_prefix[old_clan_prefix][Rank.Queen]):
            self.remove_queen(clan_prefix=old_clan_prefix, professional=True, cat_obj=cat_obj)
            self.add_queen(clan_prefix=new_clan_prefix, professional=True, cat_obj=cat_obj)
        # case 2: professional Clan queen becoming an outsider
        if (new_clan_prefix == OUTSIDER_CLAN_PREFIX and
                cat_obj in self.living_queens_and_kits_by_clan_prefix[old_clan_prefix][Rank.Queen]):
            self.remove_queen(clan_prefix=old_clan_prefix, professional=True, cat_obj=cat_obj)
        # case 3: outsider joining a Clan - do nothing here

        # nursing queens
        # if a nursing queen switches clans, they automatically bring their kits with them
        if cat_obj in self.living_queens_and_kits_by_clan_prefix[old_clan_prefix]:
            self.add_queen(clan_prefix=new_clan_prefix, professional=False, cat_obj=cat_obj)
            kits = self.remove_queen(clan_prefix=old_clan_prefix, professional=False, cat_obj=cat_obj)
            for kit in kits:
                self.change_cat_clan(new_clan_prefix=new_clan_prefix, cat_obj=kit, moving_kit_with_queen=True)
                self.give_kit_to_queen(clan_prefix=new_clan_prefix, kit_obj=kit, new_queen_obj=cat_obj)

        # kits who aren't automatically being moved with their queen
        if cat_obj.moons < config.cat_config.apprentice_age_moons and not moving_kit_with_queen:
            raise ValueError(f"Kits can't move Clans independently!")
            # FIXME handle foundlings

        return

    def add_new_cat(self, cat_obj, cat_id: int = None) -> int:
        """ Add a cat to the cat tracker.

        :param RedCat cat_obj: the RedCat object
        :param int cat_id: the already-set ID of the cat object (used when reading a save file)
        :return int: the ID of the cat
        """
        logger.debug(f"Adding {cat_obj.name} to the cat tracker")

        if not cat_id:
            cat_id = self._get_new_id()
        self.all_cats_ever[cat_id] = cat_obj

        # if alive, add the cat to all_cats
        if cat_obj.alive:
            self.all_cats[cat_id] = cat_obj

            # if a healer, add to living_medicine_cats
            if cat_obj.rank in (Rank.Healer, Rank.HealerApp):
                self.add_healer_cat(cat_obj)

        else:
            # if a dead, add to the appropriate afterlife
            if cat_obj.backstory.afterlife is Location.StarClan:
                self.dead_cats_starclan.append(cat_obj)
            elif cat_obj.backstory.afterlife is Location.DarkForest:
                self.dead_cats_darkforest.append(cat_obj)
            elif cat_obj.backstory.afterlife is Location.OutsiderAfterlife:
                self.dead_cats_outsider_afterlife.append(cat_obj)
            else:
                raise ValueError(f"Couldn't figure out which afterlife to send {cat_obj.name} to")
        return cat_id

    def kill_cat(self, cat_id: int, location: Location):
        """ Update how a cat is tracked after it dies.

        :param int cat_id: the ID of the cat who's died
        :param Location location: where the cat is going after it dies.
        :raises ValueError: if location.category isn't LocationCategory.Afterlife
        """
        cat_obj = self.all_cats[cat_id]
        logger.debug(f"Killing cat {cat_obj.name} in the cat tracker")

        if location.category is not LocationCategory.Afterlife:
            raise ValueError(f"Can't send dead cat {cat_obj.name} to non-afterlife location: {location}")

        # move the cat from the list of living cats to their appropriate afterlife
        cat_obj = self.all_cats.pop(cat_id)
        self.all_clans_ever[cat_obj.clan_prefix].remove_cat_from_clan(cat_obj)
        if location is Location.StarClan:
            cat_obj.clan_prefix = Location.StarClan.value
            self.dead_cats_starclan.append(cat_obj)
        elif location is Location.DarkForest:
            cat_obj.clan_prefix = Location.DarkForest.value
            self.dead_cats_darkforest.append(cat_obj)
        elif location is Location.OutsiderAfterlife:
            cat_obj.clan_prefix = Location.OutsiderAfterlife.value
            self.dead_cats_outsider_afterlife.append(cat_obj)
        else:
            # don't put faded cats into one of the dead "Clans"
            pass

        # REMOVE FROM SPECIFIC LIVING CAT TRACKERS
        # remove a healer
        if cat_obj in self.living_medicine_cats:
            self.living_medicine_cats.pop(cat_obj)

        # remove a kit
        if cat_obj.moons < config.cat_config.apprentice_age_moons:
            self.remove_kit_from_queen(kit_obj=cat_obj)

        # remove a nursing queen
        kits = self.remove_queen(clan_prefix=cat_obj.clan_prefix, professional=False, cat_obj=cat_obj)
        if kits:
            # add the kits they were nursing to 'None'
            for kit in kits:
                self.give_kit_to_queen(clan_prefix=cat_obj.clan_prefix, kit_obj=kit)

        # remove a professional queen
        self.remove_queen(clan_prefix=cat_obj.clan_prefix, professional=True, cat_obj=cat_obj)

        return

    def add_healer_cat(self, cat_obj):
        """ Add a cat to the list of living healers.
        Catches cats who are already in the list without throwing an error.

        Called by CatTracker.add_new_cat() and RedClan.new_healer_or_app().

        :param RedCat cat_obj: the cat to add to the list of living healers.
        """
        logger.debug(f"Adding {cat_obj.name} to list of healers in the cat tracker")
        if cat_obj not in self.living_medicine_cats:
            self.living_medicine_cats.append(cat_obj)
        return

    def remove_healer_cat(self, cat_obj):
        """ Remove a cat from the list of living healers.
        Catches cats who aren't in the list without throwing an error.

        Called by the RedClan.remove_cat_from_clan() and RedClan.change_rank().

        :param RedCat cat_obj: the cat to remove from the list of living healers.
        """
        logger.debug(f"Removing {cat_obj.name} from list of healers in the cat tracker")
        if cat_obj in self.living_medicine_cats:
            self.living_medicine_cats.remove(cat_obj)
        return

    def add_queen(self, cat_obj, clan_prefix: str, professional: bool = False):
        """ Add a cat to the list of queens in their current Clan.

        Called by RedClan.change_rank(), and CatTracker.change_cat_clan().

        :param RedCat cat_obj: the queen to add
        :param str clan_prefix: the first part of the Clan name the queen belongs to
            (e.g. 'Thunder' for ThunderClan)
        :param bool professional: True if the cat is a professional queen, False if they're a nursing queen
        """
        if professional and cat_obj:
            logger.debug(f"Adding professional queen {cat_obj.name} to {clan_prefix}Clan")
        else:
            logger.debug(f"Adding nursing queen {cat_obj.name} to {clan_prefix}Clan")

        if professional:
            # TODO QueenApp
            if clan_prefix == OUTSIDER_CLAN_PREFIX:
                raise ValueError(f"Tried to make {cat_obj.name} a professional queen, but outsiders aren't allowed")
            self.living_queens_and_kits_by_clan_prefix[clan_prefix][Rank.Queen].append(cat_obj)
        else:
            # this line will only come up if somehow the None cat got removed, e.g. if something went wrong.
            # If something has gone wrong, self.add_kits_of_queen() will cause problems without this line
            if cat_obj is not None:
                self.living_queens_and_kits_by_clan_prefix[clan_prefix][cat_obj] = []
        return

    def remove_queen(self, clan_prefix: str, professional: bool, cat_obj) -> Optional[list]:
        """ Remove a professional queen from the queen tracker.

        Catches cats who aren't queens without throwing an error.

        Called by RedClan.remove_cat_from_clan(), RedClan.change_rank(),
        CatTracker.kill_cat(), and CatTracker.change_cat_clan().

        :param str clan_prefix: the first part of the Clan name the queen/kits belong to
            (e.g. 'Thunder' for ThunderClan)
        :param bool professional: True if the cat is a professional queen, False if they're a nursing queen
        :param RedCat cat_obj: the queen to remove
        :return list[RedCat]: if removing a nursing queen, the list of kits the queen was looking after
        :raises ValueError: if you try to remove a professional outsider queen, since those shouldn't exist
        """
        if cat_obj is None:
            logger.debug(f"Can't remove the None queen!")
            return

        # outsiders can't be professional queens
        if clan_prefix == OUTSIDER_CLAN_PREFIX and professional:
            raise ValueError(f"Can't remove professional queen {cat_obj.name} because they're an outsider and "
                             f"outsiders can't be professional queens")
        elif professional:
            # TODO QueenApp
            logger.debug(f"Removing professional queen {cat_obj.name} from {clan_prefix}Clan")
            if cat_obj in self.living_queens_and_kits_by_clan_prefix[clan_prefix][Rank.Queen]:
                self.living_queens_and_kits_by_clan_prefix[clan_prefix][Rank.Queen].remove(cat_obj)
        else:
            # remove a nursing queen
            if cat_obj in self.living_queens_and_kits_by_clan_prefix[clan_prefix]:
                return self.living_queens_and_kits_by_clan_prefix[clan_prefix].pop(cat_obj)
        return

    def give_kit_to_queen(self, clan_prefix: str, kit_obj, new_queen_obj=None):
        """ Add a kit to the care of a queen. If the kit is currently being cared for by a different queen,
        this method will automatically remove the kit from the other queen's care first.

        Called when kits join a Clan, because they're either born or found.

        :param str clan_prefix: the first part of the Clan name the queen/kits belong to
            (e.g. 'Thunder' for ThunderClan)
        :param RedCat kit_obj: kitten to add to the care of the given queen
        :param RedCat new_queen_obj: the queen to look after the kit. Default value is None
        :raises ValueError: if the kit and the new queen are not in the same Clan
        """
        if new_queen_obj:
            logger.debug(f"Giving kit {kit_obj.name} to care of queen {new_queen_obj.name} in cat tracker")
            if not kit_obj.clan_prefix == new_queen_obj.clan_prefix:
                raise ValueError(f"Before {new_queen_obj.name} can care for {kit_obj.name}, "
                                 f"they must belong to the same Clan")
        else:
            logger.debug(f"Giving kit {kit_obj.name} to queen 'None' in cat tracker")
        # remove the kit from the care of their old queen
        try:
            clan_prefix, old_queen_obj = self._get_clan_and_queen_of_kit(kit_obj)
            if old_queen_obj is not None:
                self.remove_kit_from_queen(kit_obj)
        except:
            # the kit didn't have a current queen
            pass
        # add the kit to the care of their new queen
        if not new_queen_obj in self.living_queens_and_kits_by_clan_prefix[clan_prefix]:
            self.add_queen(clan_prefix=clan_prefix, cat_obj=new_queen_obj)
        # this works because when you grab a list specifically, you get the list itself, not a copy
        self.living_queens_and_kits_by_clan_prefix[clan_prefix][new_queen_obj].append(kit_obj)
        return

    def remove_kit_from_queen(self, kit_obj):
        """ Remove a kitten from the care of a queen.

        :param RedCat kit_obj: kitten to remove from the care of their current queen
        """
        clan_prefix, queen_obj = self._get_clan_and_queen_of_kit(kit_obj)
        if queen_obj:
            logger.debug(f"Removing kit {kit_obj.name} from the care of queen {queen_obj.name}")
        else:
            logger.debug(f"Removing kit {kit_obj.name} from the care of queen None")
        self.living_queens_and_kits_by_clan_prefix[clan_prefix][queen_obj].remove(kit_obj)
        # if the nursing queen is out of kits, remove them
        if not self.living_queens_and_kits_by_clan_prefix[clan_prefix][queen_obj]:
            self.remove_queen(clan_prefix=clan_prefix, professional=False, cat_obj=queen_obj)
        return
