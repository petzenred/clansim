# red_clan.py - Contains the RedClan class. Say that five times fast.

########################################################################################################################
# Imports
########################################################################################################################

import random
from cmath import exp
from dataclasses import dataclass, field
from errno import EILSEQ
from typing import Union, Optional

from definitions import (
    CLAN_TEMPERAMENT_WEIGHT,
    CampKey, GameMode, Location, Rank, Season, WarriorFocus,
    FRESHKILL_ROTS_AT_MOONS, Biome, LeaderFocus, LocationCategory, ClanTemperament,
    TEMPERAMENT_THRESHOLD_LOW, TEMPERAMENT_THRESHOLD_HIGH, cast_to_location, cast_to_camp_key,
    SpecialClanToken, cast_to_biome, cast_to_herb, HerbName
)
from scripts._red.cats.red_cat import RedCat
from scripts._red.config_manager import config
from scripts._red.red_exceptions import InitializationError
from scripts._red.utils.general_utils import one_in_num_chance
from scripts.game_structure.game_essentials import game
from scripts._red.sprite_manager import sprite_manager

import logging
logger = logging.getLogger(__name__)


########################################################################################################################
# Dataclasses
########################################################################################################################


class Camp:
    """ Contains all the info about a Clan's camp. """

    biome: Biome
    camp_key: CampKey
    freshkill_pile: list[float] # index is age of freshkill
    # TODO make sure this makes sense once Conditions are properly implemented
    herb_store: dict[HerbName, list[int]] # {herb_name, [amount_of_age_index, amount_of_age_index]}

    # TODO update cat_tracker

    # ------------------------------------- INIT ------------------------------------- #

    # TODO load den_positions
    # TODO load cat_positions
    def __init__(self, biome=Biome.NoBiome, camp_key=CampKey.NoCamp, freshkill_pile=None, herb_stores=None):
        if freshkill_pile is None:
            freshkill_pile = [0]
        self.freshkill_pile = freshkill_pile
        self.biome = cast_to_biome(biome)
        self.camp_key = cast_to_camp_key(camp_key)
        self.herb_store = {}
        if herb_stores:
            for herb_name, herb_info_list in herb_stores.items():
                self.herb_store[cast_to_herb(herb_name)] = herb_info_list

        # TODO load den_positions
        # TODO load cat_positions

        return

    # ------------------------------------ PUBLIC ------------------------------------ #

    def add_freshkill(self, amount: float):
        """ Adds freshkill to the freshkill pile. """
        self.freshkill_pile[0] += amount
        return

    def add_herb(self, herb_name: HerbName, amount: int):
        """ Adds fresh herbs to the herb store. """
        if herb_name not in self.herb_store:
            # the Clan doesn't have any of this herb
            self.herb_store[herb_name] = [0]
        self.herb_store[herb_name][0] += amount
        return

    def eat_freshkill(self, amount: float) -> tuple[bool, float]:
        """ Attempt to eat some amount from the freshkill pile.

        :param float amount: How much food you are attempting to eat.
        :return bool: True if there was enough food; False otherwise.
        """
        while self.freshkill_pile and amount:
            amount = self._private_remove_freshkill(
                age=max(self.freshkill_pile.keys()),
                amount=amount)
        if self.freshkill_pile:
            return True, 0
        return False, amount

    def use_herbs(self, treatment: dict[int, list[HerbName]]) -> bool:
        """ Attempt to use some amount of herbs from the herb store.

        :param dict treatment: the "herbs" section from the condition
        :return bool: if herbs were available (and used) for treatment
        """
        if not treatment:
            raise ValueError(f"Can't use herbs from herb store because there are no herbs listed as treatment")
        for amount, herbs in treatment.items():
            # TODO try herbs in a random order to avoid always using the alphabetically early herbs up first
            # nesting the loops like this ensures that the oldest of each herb is used up before newer herb stores
            # e.g. if you have { burdock_root: {4: 1, 2: 1}, marigold: {4: 1} } and need two herbs, you will end up
            #      with { burdock_root: {2: 1} } instead of { marigold: {4: 1} }
            while amount:
                for herb in herbs:
                    if herb in self.herb_store:
                        amount = self._private_remove_herb(
                            herb_name=herb,
                            age=max(self.herb_store[herb]),
                            amount=amount)
            # if treatment is finished, don't use any more herbs
            if not amount:
                break
        return amount > 0

    def timeskip_age_camp_stores(self) -> dict:
        """ Increase the age of all freshkill and herbs by one moon, and remove any resources that are too old.

        :return dict: which resources rotted, and how much of that resource was lost
        """
        rotted: dict = {"freshkill": self._age_freshkill()}
        rotted.update(self._age_herbs())
        return rotted

    # FIXME create function timeskip_age_camp_stores() which does this for the freshkill pile and for herbs
    def freshkill_moon(self, amount_to_eat: float) -> tuple[bool, float]:
        """ Tries to feed everyone and then removes rotten freshkill.

        :param float amount_to_eat: how much freshkill is needed to feed the entire Clan
        :return bool: whether the Clan had enough freshkill to feed everyone
        :return float: how much food is still needed if the entire Clan couldn't eat
        """
        # eat as much food as the Clan wants, or as much as is available
        clan_is_fed_f, amount_needed = self.eat_freshkill(amount_to_eat)
        if clan_is_fed_f:
            # once the Clan is done eating, remove uneaten
            # freshkill that will rot by the end of the month
            if max(self.freshkill_pile) + 1 == FRESHKILL_ROTS_AT_MOONS:
                self.freshkill_pile.pop(max(self.freshkill_pile))
            # update the age of non-rotting freshkill
            oldest_freshkill_age: int = max(self.freshkill_pile.keys())
            while oldest_freshkill_age > 0:
                new_fk_age = oldest_freshkill_age + 1
                if new_fk_age >= FRESHKILL_ROTS_AT_MOONS:
                    self.freshkill_pile[oldest_freshkill_age] = 0
                else:
                    self.freshkill_pile[new_fk_age] = self.freshkill_pile[oldest_freshkill_age]
                    self.freshkill_pile[oldest_freshkill_age] = 0
                oldest_freshkill_age -= 1
            self.freshkill_pile.pop(0)
            return True, 0
        return False, amount_needed

    # ----------------------------------------

    def _age_freshkill(self) -> float:
        """ Increase the age of all freshkill by one moon, and remove
        uneaten freshkill which will rot by the end of the month.

        :return float: the amount of freshkill that rotted
        """
        # age all the freshkill
        self.freshkill_pile.insert(0, 0)

        # remove rotted freshkill
        if len(self.freshkill_pile) > FRESHKILL_ROTS_AT_MOONS:
            logger.info(f"Removing rotted freshkill: {self.freshkill_pile[-1]}")
            return self.freshkill_pile.pop(-1)
        return 0

    def _age_herbs(self) -> dict[HerbName, int]:
        """ Increase the age of all herbs by one moon, and remove
        unused herbs which will rot by the end of the month.

        :return dict[HerbName, int]: which herbs rotted and how many of those herbs were lost
        """
        rotted_herbs: dict[HerbName, int] = {}
        for herb_name in self.herb_store:
            self.herb_store[herb_name].insert(0, 0)
            if len(self.herb_store[herb_name]) > herb_name.lifetime_moons:
                logger.debug(f"Removing rotted {herb_name.name} from herb store: {self.herb_store[herb_name][-1]}")
                self._private_remove_herb(herb_name=herb_name, age=-1, amount=self.herb_store[herb_name][-1])
            if sum(self.herb_store[herb_name]) == 0:
                self.herb_store.pop(herb_name)
        return rotted_herbs

    def _private_remove_freshkill(self, age: int, amount: float) -> float:
        """ Attempt to remove some amount of a specific age from the freshkill pile.

        Used when eating freshkill, and when removing rotted freshkill.

        Updates self.freshkill_pile if amount <= self.freshkill_pile[age].

        :param int age: how old the freshkill you're trying to remove is
        :param float amount: how much freshkill you are attempting to remove
        :return float: how much freshkill you still need
        """
        if amount < 0:
            raise ValueError(f"You can't remove a negative amount of food from the freshkill pile")
        if age in self.freshkill_pile:
            if amount < self.freshkill_pile[age]:
                self.freshkill_pile[age] -= amount
                amount = 0
            else:
                amount -= self.freshkill_pile[age]
                self.freshkill_pile[age] = 0
        return amount

    def _private_remove_herb(self, herb_name: HerbName, age: int, amount: int) -> int:
        """ Attempt to use some amount of some herbs of a specific age from the herb store.

        Updates self.herb_store if amount <= self.herb_store[age][herb_name].

        :param HerbName herb_name: which herb you're using
        :param int age: how old the herbs you're trying to remove is
        :param int amount: how many herbs you are attempting to remove
        :return int: how many herbs you still need
        """
        if self.herb_store[herb_name][age] >= amount:
            self.herb_store[herb_name][age] -= amount
            amount = 0
        else:
            amount -= self.herb_store[herb_name][age]
            self.herb_store[herb_name][age] = 0
        if sum(self.herb_store[herb_name]) == 0:
                self.herb_store.pop(herb_name)
        return amount


########################################################################################################################
# Classes
########################################################################################################################

# TODO move `utility.clan_symbol_sprite` to either `red_clan.py` or `sprite_manager.py`

# TODO include a HealerDen object
class RedClan:
    """ Clans full of Cats.

    Outsiders are also represented by Clans; there's one for kittypets and one for loners and rogues.
    """
    # TODO StarClan and the Dark Forest don't have reputations or inter-Clan relationships
    clan_token: str  # name
    clan_name: str # name
    clan_symbol: str
    warrior_clan_f: bool

    # Clan temperament
    net_cat_sociability: int
    net_cat_aggression: int

    # Clan history
    moon_established: int  # TODO inspired by LifeGen, allow Clans to be older when they are generated
    moon_destroyed: int
    # these only track cats who died or were lost in these roles
    past_leader_ids: list[int] # TODO update in CatTracker.kill_cat, CatTracker.switch_clan
    past_deputy_ids: list[int] # TODO update in CatTracker.kill_cat, CatTracker.switch_clan
    past_healer_ids: list[int] # TODO update in CatTracker.kill_cat, CatTracker.switch_clan
    # clan_background: str
    # clan_flavours: list
    # leader_naming_themes: list

    camp: Union[Camp | CampKey]  # Camp for the player Clan, CampKey for other warrior Clans
    default_afterlife: Location
    leader_lives_remaining: int  # leader_lives # TODO should this be part of the Cat object?
    # NB: StarClan and Dark Forest cats aren't divided by Clan since in both, explicitly Clan differences are ignored
    clan_cats: dict[int, RedCat]
    clan_cats_by_rank: dict[Rank, list[RedCat]]

    # warrior focus
    warrior_focus_purpose: WarriorFocus  # focus
    # For example, if the focus is on befriending WindClan and SkyClan, this would be ["wind", "sky", ]
    warrior_focus_arg: list[str]  # focus_arg
    last_warrior_focus_change: int  # moons_with_focus

    # leader focus
    leader_focus_clan_token: Optional[str]  # e.g. "Thunder", "Sky"
    leader_focus_clan_purpose: LeaderFocus
    leader_focus_outsider_id: Optional[int]
    leader_focus_outsider_purpose: LeaderFocus

    # keeping self._amount_every_moon updated is computationally faster than calculating it every moon
    _amount_every_moon: float # FIXME what is this? how much the Clan eats every moon?

    # ------------------------------------- INIT ------------------------------------- #

    def __init__(self, save_file: dict = None, **kwargs):

        try:
            self._init_values_for_clan()

            if save_file is not None:
                self.clan_token = kwargs.pop("clan_token")
                if self.clan_token == game.active_clan_token:
                    self._parse_player_clan_save_file(save_file=save_file, camp_details=kwargs.pop("camp_details"))
                elif self.clan_token in list(SpecialClanToken):
                    self._parse_special_clan_save_file(save_file=save_file)
                else:
                    self._parse_npc_clan_save_file(save_file=save_file)

            else:
                # make sure that all required keys are present
                required_keys: list[str] = ["warrior_clan_f", "moon_established", ]
                for rk in required_keys:
                    if rk not in kwargs:
                        raise KeyError(f"RedClan object is missing the key {rk} and can't be initialized")
                # create a new random Clan
                self._create_new_clan(**kwargs)

        except BaseException as err:
            token = kwargs["clan_token"] if "clan_token" in kwargs else self.clan_token
            msg: str = f"Something went wrong while trying to parse a Clan's save file (clan_token={token})"
            logger.exception(msg=msg, exc_info=err)
            logger.error(f"Clan with token \'{token}\' wasn't added to the CatTracker because of the error.")
            raise InitializationError(msg)

        else:
            game.cat_tracker.add_new_clan(self)
            return

    def _init_values_for_clan(self):
        """ This is here because if lists and dicts (such as the list of cats in the Clan) are initialized
        outside a function, they're shared between all instances of the class.
        """
        self.moon_destroyed = -1

        self.net_cat_sociability = 0
        self.net_cat_aggression = 0

        self.past_leader_ids = []
        self.past_deputy_ids = []
        self.past_healer_ids = []
        self.leader_lives_remaining = 0

        self.clan_cats = {}
        self.clan_cats_by_rank = {
            Rank.Leader: [],
            Rank.Deputy: [],
            Rank.Healer: [],
            Rank.HealerApp: [],
            Rank.Queen: [],
            Rank.QueenApp: [],
            Rank.Mediator: [],
            Rank.MediatorApp: [],
            Rank.Warrior: [],
            Rank.WarriorApp: [],
            Rank.Kit: [],
            Rank.Elder: []
        }

        # warrior focus
        self.warrior_focus_purpose = WarriorFocus.NoFocus  # focus
        # For example, if the focus is on befriending WindClan and SkyClan, this would be ["wind", "sky", ]
        self.warrior_focus_arg = []  # focus_arg
        self.last_warrior_focus_change = 0  # moons_with_focus

        # leader focus
        self.leader_focus_clan_token = None  # e.g. "Thunder", "Sky"
        self.leader_focus_clan_purpose = LeaderFocus.NoFocus
        self.leader_focus_outsider_id = None
        self.leader_focus_outsider_purpose = LeaderFocus.NoFocus

        # keeping self._amount_every_moon updated is computationally faster than calculating it every moon
        self._amount_every_moon = 0 # FIXME what is this? how much the Clan eats every moon?

        return

    def _parse_player_clan_save_file(self, save_file: dict, camp_details: dict):
        """ Parses the player's Clan, which is more complex than all other Clans.

        :param dict save_file: contains all the information about the Clan
        """
        # that's how the game, uh, is. Maybe one day you can play as the Tribe or smth
        self.warrior_clan_f = True

        self.clan_name = save_file.pop("clan_name")
        self.clan_symbol = save_file.pop("clan_symbol")
        self.default_afterlife = cast_to_location(to_cast=save_file.pop("default_afterlife"))
        self.moon_established = int(save_file.pop("moon_established"))
        # do not pop the number of remaining lives that the leader has here -
        #     that's handled when adding the leader's RedCat object to the Clan
        self.past_leader_ids = save_file.pop("past_leader_ids")
        self.past_deputy_ids = save_file.pop("past_deputy_ids")
        self.past_healer_ids = save_file.pop("past_healer_ids")

        leader_focus: Optional[dict] = save_file.pop("leader_focus")
        if leader_focus is None:
            self.leader_focus_clan_token = None
            self.leader_focus_clan_purpose = LeaderFocus.NoFocus
            self.leader_focus_outsider_id = None
            self.leader_focus_outsider_purpose = LeaderFocus.NoFocus
        else:
            self.leader_focus_clan_token = leader_focus["leader_focus_clan_token"]
            self.leader_focus_clan_purpose = LeaderFocus(leader_focus["clan_purpose"])
            self.leader_focus_outsider_id = int(leader_focus["outsider_in_focus_id"])
            self.leader_focus_outsider_purpose = LeaderFocus(leader_focus["outsider_purpose"])

        self.last_warrior_focus_change = int(save_file.pop("last_warrior_focus_change"))
        warrior_focus = save_file.pop("warrior_focus")
        if warrior_focus is None:
            self.warrior_focus_purpose = WarriorFocus.NoFocus
            self.warrior_focus_arg = []
        else:
            self.warrior_focus_purpose = WarriorFocus(warrior_focus["warrior_focus_purpose"])
            self.warrior_focus_arg = warrior_focus["warrior_focus_arg"]

        self.camp = Camp(biome=camp_details["biome"],
                         camp_key=camp_details["background"],
                         freshkill_pile=camp_details["freshkill_pile"],
                         herb_stores=camp_details["herb_store"])

        # TODO implement clan_background
        # TODO implement clan_flavours
        # TODO implement leader_naming_theme

        # if there are any keys remaining in the save file that didn't get used, make sure that gets logged
        if save_file:
            logger.warning(f"After creating the {self.clan_name} object, there was some "
                           f"information in the save file which wasn't used:\n{save_file.keys()}")
        return

    def _parse_special_clan_save_file(self, save_file: dict):
        """ Parses the 'Clan' all loners belong to, and afterlives.

        :param dict save_file: contains all the information about the Clan
        """
        self.clan_name = save_file.pop("clan_name")
        self.warrior_clan_f = bool(save_file.pop("warrior_clan_f"))
        self.moon_established: int = 0

        if self.clan_token == SpecialClanToken.Loners:
            self.default_afterlife = Location.OutsiderAfterlife

        # if there are any keys remaining in the save file that didn't get used, make sure that gets logged
        if save_file:
            logger.warning(f"After creating the {self.clan_name} object, there was some "
                           f"information in the save file which wasn't used:\n{save_file.keys()}")
        return

    def _parse_npc_clan_save_file(self, save_file: dict):
        """ Parse other warrior Clans, rogue groups, etc.

        :param dict save_file: contains all the information about the Clan
        """
        self.clan_name = save_file.pop("clan_name")
        self.clan_symbol = save_file.pop("clan_symbol")
        self.default_afterlife = cast_to_location(to_cast=save_file.pop("default_afterlife"))
        self.warrior_clan_f = bool(save_file.pop("warrior_clan_f"))
        self.moon_established = int(save_file.pop("moon_established"))
        self.camp = cast_to_camp_key(save_file.pop("camp_key"))
        # do not pop the number of remaining lives that the leader has here -
        #     that's handled when adding the leader's RedCat object to the Clan
        self.past_leader_ids = save_file.pop("past_leader_ids")
        self.past_deputy_ids = save_file.pop("past_deputy_ids")
        self.past_healer_ids = save_file.pop("past_healer_ids")

        # TODO implement clan_background
        # TODO implement clan_flavours
        # TODO implement leader_naming_theme

        # if there are any keys remaining in the save file that didn't get used, make sure that gets logged
        if save_file:
            logger.warning(f"After creating the {self.clan_name} object, there was some "
                           f"information in the save file which wasn't used:\n{save_file.keys()}")
        return

    def _create_new_clan(self, **kwargs):
        """ Create a new Clan (or outside group). """
        self.warrior_clan_f = bool(kwargs["warrior_clan_f"])

        # Clan location stuff
        if "camp" in kwargs:
            self.camp = kwargs.pop("camp")
        else:
            self.camp = random.choice(list(CampKey))
        if "default_afterlife" in kwargs:
            afterlife = Location(kwargs.pop("default_afterlife"))
            if afterlife.category is not LocationCategory.Afterlife:
                raise ValueError(f"{self.clan_name}'s afterlife is not an afterlife location: {afterlife}")
            else:
                self.default_afterlife = afterlife
        else:
            if one_in_num_chance(num=config.clan_config.chance_for_df_worshippers):
                self.default_afterlife = Location.DarkForest
            else:
                self.default_afterlife = Location.StarClan

        # Clan name and symbol
        if "clan_token" in kwargs:
            if not "clan_name" in kwargs or "clan_symbol" in kwargs:
                raise KeyError(f"Can't provide a clan_token without providing a clan_name and clan_symbol")
            self.clan_token = kwargs.pop("clan_token")
            self.clan_name = kwargs.pop("clan_name")
            self.clan_symbol = kwargs.pop("clan_symbol")
        else:
            prefix: str = random.choice(sprite_manager.symbol_dict.keys())
            while prefix in game.cat_tracker.all_clans.keys():
                prefix = random.choice(sprite_manager.symbol_dict.keys())
            self.clan_token = prefix.lower()
            variant = random.randint(0, sprite_manager.symbol_dict[prefix]["variants"] - 1)
            self.clan_name = prefix + "Clan"
            self.clan_symbol = f"symbol{prefix.upper()}{variant}"

        if "moon_established" in kwargs:
            self.moon_established = int(kwargs.pop("moon_established"))
        else:
            self.moon_established = game.current_moon

        # TODO implement clan_background
        # TODO implement clan_flavours
        # TODO implement leader_naming_theme

        return

    # ------------------------------------ SETTERS ----------------------------------- #

    # FIXME make a DeathEvent
    def kill_leader(self, cat_obj: RedCat = None, remove_all_lives: bool = False):
        """ Take a leader's life. If the leader has run out of lives, kill them and set the position to empty.

        :param RedCat cat_obj: if there's more than one leader, use this to specific which one is being killed
        :param bool remove_all_lives: whether you're killing a warrior Clan leader like Scourge did to Tigerclawstar
        """
        if not cat_obj:
            if len(self.clan_cats_by_rank[Rank.Leader]) == 1:
                cat_obj: RedCat = self.clan_cats_by_rank[Rank.Leader][0]
            else:
                raise ValueError(f"Because {self.clan_name} doesn't have one leader, you need to specify which "
                                 f"leader is dying when you call kill_leader(), but none was specified.")

        if remove_all_lives:
            self.leader_lives_remaining = 0
        else:
            self.leader_lives_remaining -= 1
        if not self.leader_lives_remaining:
            # FIXME make a DeathEvent
            self.clan_cats_by_rank[Rank.Leader].remove(cat_obj)
            if cat_obj.alive:
                cat_obj.kill()

        return

    def new_leader(self, leader_lives_remaining: int, cat_obj: RedCat = None) -> bool:
        """ Set a given cat as the Clan leader, or promote the deputy.

        :param Optional[RedCat] cat_obj: a specific cat to promote
        :param int leader_lives_remaining: how many lives the new leader should start with
        :return: True if a cat was successfully promoted, False if there were no eligible cats
        """
        if self.clan_cats_by_rank[Rank.Leader]:
            raise ValueError(f"{self.clan_name} already has a leader, you can't choose a new one!")

        # if no specific cat is requested, promote the deputy
        if not cat_obj:
            # if there isn't a deputy, promote one. If there aren't any eligible cats, return False
            if not self.clan_cats_by_rank[Rank.Deputy]:
                if not self.new_deputy():
                    return False
            # pick a random cat from the Clan's list of deputies (for the
            #     moment, this will always be a list with only one cat in it)
            cat_obj = self._pick_cat_for_promotion(choose_from_rank=Rank.Deputy)

        logger.debug(f"Making {cat_obj.name} the leader of {self.clan_name}")
        if cat_obj in self.clan_cats_by_rank[Rank.Deputy]:
            self.clan_cats_by_rank[Rank.Deputy].remove(cat_obj)
        self.clan_cats_by_rank[Rank.Leader].append(cat_obj)

        if self.warrior_clan_f:
            self.leader_lives_remaining = leader_lives_remaining
        else:
            self.leader_lives_remaining = 1

        return True

    def new_deputy(self, cat_obj: RedCat = None) -> bool:
        """ Promote a warrior to deputy.

        :param Optional[RedCat] cat_obj: a specific cat to promote
        :return: True if a cat was successfully promoted, False if there were no eligible cats
        """
        if not cat_obj:
            # if no specific cat is requested, promote a cat to deputy
            cat_obj = self._pick_cat_for_promotion(choose_from_rank=Rank.Warrior)
        elif not cat_obj in self.clan_cats_by_rank[Rank.Warrior]:
            raise KeyError(f"{cat_obj.name} not a Rank.Warrior; please make them "
                           f"one before electing them as deputy")

        # return False if there are no cats eligible to become deputy
        if not self.clan_cats_by_rank[Rank.Warrior]:
            return False


        logger.debug(f"Making {cat_obj.name} the deputy of {self.clan_name}")
        self.clan_cats_by_rank[Rank.Warrior].remove(cat_obj)
        self.clan_cats_by_rank[Rank.Deputy] = cat_obj

        return True

    # FIXME remove cat from their old rank
    def change_cat_rank_from_cat_object(self, cat_obj: RedCat, new_rank: Rank, old_rank: Rank):
        """ Change a cat's rank (e.g. from warrior apprentice to healer apprentice).

        Called by RedCat.change_rank().
        """

        # double-check that the cat's internal storage is updated by this method, not anywhere else
        if not cat_obj.rank is old_rank:
            cat_obj.rank = old_rank

        # FIXME remove cat from their old rank
        if old_rank is Rank.Leader:
            raise ValueError(f"In order to demote a leader, use Clan.kill_leader(), not Clan.change_rank().")
        elif old_rank is Rank.Deputy:
            self.clan_cats_by_rank[Rank.Deputy] = None
        else:
            self.clan_cats_by_rank[old_rank].remove(cat_obj)
            if old_rank in (Rank.Healer, Rank.HealerApp):
                game.cat_tracker.remove_healer_cat(cat_obj=cat_obj)
            elif old_rank in (Rank.Queen, Rank.QueenApp):
                game.cat_tracker.old_remove_nursing_queen(clan_token=self.clan_token, cat_obj=cat_obj)
        self._update_clan_temperament(cat_obj=cat_obj, subtract=True)

        # add cat to their new rank
        cat_obj.rank = new_rank
        if new_rank is Rank.Leader:
            num_lives: int = 9 if self.warrior_clan_f else 1
            self.new_leader(cat_obj=cat_obj, leader_lives_remaining=num_lives)
        elif new_rank is Rank.Deputy:
            self.new_deputy(cat_obj=cat_obj)
        else:
            self.clan_cats_by_rank[new_rank].append(cat_obj)
            if new_rank in (Rank.Healer, Rank.HealerApp):
                game.cat_tracker.add_healer_cat(cat_obj=cat_obj)
            elif new_rank in (Rank.Queen, Rank.QueenApp):
                game.cat_tracker.add_queen(cat_obj=cat_obj, clan_token=self.clan_token, professional=True)
        self._update_clan_temperament(cat_obj=cat_obj)

        return

    # FIXME account for the difference between rogues and loners
    # FIXME add nursing queens
    def add_cat_to_clan(self, rank: Rank, cat_obj: RedCat, leader_lives_remaining: int = 0):
        """ Add a cat to the Clan.

        :param Rank rank: the rank the cat should be added to the Clan at
        :param RedCat cat_obj: a specific cat to add to the Clan
        :param int leader_lives_remaining: if the cat being added is a leader,
        """
        logger.debug(f"Adding {cat_obj.name} to {self.clan_name}")
        if cat_obj.cat_id in self.clan_cats:
            raise ValueError(f"{cat_obj.name} is already in {self.clan_name}!")

        else:
            # add cat to the internal list of Clan cats
            self.clan_cats[cat_obj.cat_id] = cat_obj
            cat_obj.clan_token = self.clan_token

            # loners can only have the Loner rank
            # FIXME account for the difference between rogues and loners
            if self.clan_token == SpecialClanToken.Loners:
                cat_obj.rank = Rank.Loner

            else:
                if rank is Rank.Leader:
                    if self.clan_token in SpecialClanToken:
                        self.clan_cats_by_rank[Rank.Leader].append(cat_obj)
                    else:
                        if not leader_lives_remaining:
                            raise ValueError(f"Can't add leader {cat_obj.name} to {self.clan_name} "
                                             f"without knowing how many lives they have left!")
                        self.clan_cats_by_rank[Rank.Warrior].append(cat_obj) # DO NOT CHANGE FROM WARRIOR
                        self.new_leader(cat_obj=cat_obj, leader_lives_remaining=leader_lives_remaining)
                elif rank is Rank.Deputy:
                    if self.clan_token in SpecialClanToken:
                        self.clan_cats_by_rank[Rank.Deputy].append(cat_obj)
                    else:
                        self.clan_cats_by_rank[Rank.Warrior].append(cat_obj) # DO NOT CHANGE FROM WARRIOR
                        self.new_deputy(cat_obj=cat_obj)
                elif rank.is_healer:
                    self.clan_cats_by_rank[rank].append(cat_obj)
                    if cat_obj.alive:
                        game.cat_tracker.add_healer_cat(cat_obj=cat_obj)
                elif rank.is_queen:
                    self.clan_cats_by_rank[rank].append(cat_obj)
                    if cat_obj.alive:
                        game.cat_tracker.add_queen(cat_obj=cat_obj, clan_token=self.clan_token, professional=True)
                elif cat_obj.health.conditions:
                    # TODO if 'recovering from birth' is in the list of conditions
                    # FIXME add nursing queens
                    raise NotImplementedError(f"Can't add cats with health conditions yet")
                else:
                    self.clan_cats_by_rank[rank].append(cat_obj)

        # update Clan temperament
        self._update_clan_temperament(cat_obj=cat_obj)

        return

    def remove_cat_from_clan(self, cat_obj: RedCat):
        """ Remove a cat from the Clan.

        Called by CatTracker.change_cat_clan() and CatTracker.kill_cat().
        """
        cat_id: int = cat_obj.cat_id
        if cat_id in self.clan_cats:
            self.clan_cats.pop(cat_id)
        else:
            raise KeyError(f"{cat_obj.name} not in {self.clan_name}, so can't be removed from it")

        # handle the cat's rank
        if cat_obj in self.clan_cats_by_rank[cat_obj.rank]:
            self.clan_cats_by_rank[cat_obj.rank].remove(cat_obj)
        else:
            msg: str = (f"When removing {cat_obj.name} from {self.clan_name}, {cat_obj.name} "
                        f"wasn't listed under the correct rank \'{cat_obj.rank}\'")
            for cat_rank in self.clan_cats_by_rank.keys():
                if cat_obj in self.clan_cats_by_rank[cat_rank]:
                    msg += f" and was removed from rank \'{cat_rank}\' instead"
                    self.clan_cats_by_rank[cat_rank].remove(cat_obj)
                    break
            logger.warning(msg)

        if cat_obj.rank.is_healer:
            game.cat_tracker.remove_healer_cat(cat_obj=cat_obj)
        if cat_obj.rank.is_queen:
            game.cat_tracker.remove_professional_queen(clan_token=self.clan_token, cat_obj=cat_obj)

        # update Clan temperament
        self._update_clan_temperament(cat_obj=cat_obj, subtract=True)

        return

    def _update_clan_temperament(self, cat_obj: RedCat, subtract: bool = False):
        """ Update the Clan's temperament values.

        These should change when a cat is added, when a cat leaves, and when the leadership changes.
        The latter case is handled in RedCat.change_rank(). """
        if subtract:
            weight = 1 if cat_obj.rank in (Rank.Leader, Rank.Deputy) else CLAN_TEMPERAMENT_WEIGHT
            self.net_cat_sociability -= cat_obj.sociability * weight
            self.net_cat_aggression -= cat_obj.aggression * weight
        else:
            weight = 1 if cat_obj.rank in (Rank.Leader, Rank.Deputy) else CLAN_TEMPERAMENT_WEIGHT
            self.net_cat_sociability += cat_obj.sociability * weight
            self.net_cat_aggression += cat_obj.aggression * weight
        return

    # ----------------------------------- GETTERS ------------------------------------ #

    # TODO
    def _pick_cat_for_promotion(self, choose_from_rank: Rank):
        """ This automatically picks a cat to promote, either to deputy or leader if there's more than one deputy.

        :param Rank choose_from_rank: the rank of cats to pick a promotee from
        """
        raise NotImplementedError("RedClan._pick_cat_for_promotion")

    def enough_healers_to_treat_cats(self) -> bool:
        """ Returns True if the Clan has enough medics and False otherwise. """
        # this is always allowed in story mode
        if config.settings.GameMode is GameMode.Classic:
            return True

        num_healers: int = len(self.clan_cats_by_rank[Rank.Healer]) + len(self.clan_cats_by_rank[Rank.HealerApp])
        largest_clan_size: int = num_healers * config.settings.GameMode.num_cats_per_healer
        for rank in self.clan_cats_by_rank:
            if rank is Rank.Leader and self.clan_cats_by_rank[rank]:
                largest_clan_size -= 1
            elif rank is Rank.Deputy and self.clan_cats_by_rank[rank]:
                largest_clan_size -= 1
            else:
                largest_clan_size -= len(self.clan_cats_by_rank[rank])

        return largest_clan_size > -1

    def get_cats_within_age(self, pivot_moons: int, range_moons: int) -> list[RedCat]:
        """ Get all cats in the Clan within [range_moons] of [pivot_moons]. """
        result: list = []
        for cat_obj in self.clan_cats.values():
            if (pivot_moons - range_moons) <= cat_obj.moons <= (pivot_moons + range_moons):
                result.append(cat_obj)
        return result

    # TODO get all cats in the Clan who are potential romance partners of cat_obj
    def get_potential_clan_romances(self, cat_obj: RedCat):
        """ """
        potential_mates: list[RedCat] = list(self.clan_cats.values())
        potential_mates.remove(cat_obj)
        return NotImplementedError("RedClan.get_potential_clan_romances")

    def get_clan_temperament(self) -> ClanTemperament:
        """ Calculate the average sociability and aggression of the cats in this Clan.

        This is a low-resource implementation utilising the fact that the RedClan object tracks
        the net sociability and aggression of every cat in the Clan, accounting for leadership's
        impact.

        :return ClanTemperament: the Clan's temperament.
        """

        clan_size: int = len(self.clan_cats)
        # if all cats in the Clan have maximally sociable personalities, avg_clan_sociability will be 16
        avg_clan_sociability: int = round(self.net_cat_sociability/clan_size)
        # if all cats in the Clan have maximally aggressive personalities, avg_clan_aggression will be 16
        avg_clan_aggression: int = round(self.net_cat_aggression/clan_size)

        if avg_clan_sociability < TEMPERAMENT_THRESHOLD_LOW:
            # low social
            if avg_clan_aggression < TEMPERAMENT_THRESHOLD_LOW:
                return ClanTemperament.Cunning
            elif avg_clan_aggression >= TEMPERAMENT_THRESHOLD_HIGH:
                return ClanTemperament.Bloodthirsty
            else:
                return ClanTemperament.Proud
        elif avg_clan_sociability >= TEMPERAMENT_THRESHOLD_HIGH:
            # high social
            if avg_clan_aggression < TEMPERAMENT_THRESHOLD_LOW:
                return ClanTemperament.Gracious
            elif avg_clan_aggression >= TEMPERAMENT_THRESHOLD_HIGH:
                return ClanTemperament.Logical
            else:
                return ClanTemperament.Mellow
        else:
            # mid social
            if avg_clan_aggression < TEMPERAMENT_THRESHOLD_LOW:
                return ClanTemperament.Amiable
            elif avg_clan_aggression >= TEMPERAMENT_THRESHOLD_HIGH:
                return ClanTemperament.Wary
            else:
                return ClanTemperament.Stoic

    def get_random_cat(self, spec_rank: Rank = None, min_moons: int = -1, max_moons: int = 1000) -> Optional[RedCat]:
        """ Get a random cat from the Clan.

        :param Rank spec_rank: Rank which the random cat will have
        :param int min_moons: the lowest age the cat will have (inclusive). Dead cats use the age they died at
        :param int max_moons: the highest age the cat will have (inclusive). Dead cats use the age they died at

        :return RedCat: random cat from the Clan who meets the requirements, or None
        """
        # handle single-cat ranks off the bat to save some time, although why would you use this method to get them
        #   in the first place?
        if spec_rank in (Rank.Leader, Rank.Deputy):
            return self.clan_cats_by_rank[spec_rank]

        eligible_cats: list = []
        # get a list of eligible cats
        for cat_obj in self.clan_cats.values():
            if min_moons <= cat_obj.moons <= max_moons:
                if cat_obj.rank is spec_rank:
                    eligible_cats.append(cat_obj)

        # choose a random eligible cat, if possible
        try:
            return random.choice(eligible_cats)
        except IndexError:
            logger.error(f"Tried to grab a random {self.clan_name} cat, but there is no cat in who "
                         f"meets the requirements: rank={spec_rank}, {min_moons} <= age <= {max_moons}")
            logger.error(f"Returning None")
            return None
