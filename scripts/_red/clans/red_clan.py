# red_clan.py - Contains the RedClan class. Say that five times fast.

########################################################################################################################
# Imports
########################################################################################################################

from dataclasses import dataclass, field
from typing import Union

from definitions import (
    CampKey, GameMode, Location, Rank, Season, WarriorFocus,
    FRESHKILL_ROTS_AT_MOONS, Biome, OUTSIDER_CLAN_PREFIX, LeaderFocus, LocationCategory
)
from scripts._red.cats.red_cat import RedCat
from scripts._red.config_manager import config
from scripts.game_structure.game_essentials import game


########################################################################################################################
# Dataclasses
########################################################################################################################

@dataclass
class Camp:
    """ Contains all the info about a Clan's camp. """

    biome: Biome
    camp_key: CampKey = CampKey.NoCamp
    freshkill_pile: dict = field(default_factory=dict)  # {age_of_freshkill: amount_of_freshkill}
    herb_stores: dict = field(default_factory=dict)
    freshkill_rots_at_age: int = FRESHKILL_ROTS_AT_MOONS

    # TODO den_positions
    # TODO cat_positions
    # TODO update cat_tracker

    def add_freshkill(self, amount: float):
        """ Adds some freshkill to the freshkill pile. """
        if 0 not in self.freshkill_pile.keys():
            self.freshkill_pile[0] = amount
        else:
            self.freshkill_pile[0] = self.freshkill_pile[0] + amount
        return

    def freshkill_moon(self, amount_to_eat: float) -> bool:
        """ Tries to feed everyone and then removes rotten freshkill. """
        # eat as much food as the Clan wants, or as much as is available
        if self.eat_freshkill(amount_to_eat):
            # once the Clan is done eating, remove uneaten
            # freshkill that will rot by the end of the month
            oldest_freshkill_age: int = max(self.freshkill_pile.keys())
            while oldest_freshkill_age > 0:
                new_fk_age = oldest_freshkill_age + 1
                if new_fk_age >= self.freshkill_rots_at_age:
                    self.freshkill_pile[oldest_freshkill_age] = 0
                else:
                    self.freshkill_pile[new_fk_age] = self.freshkill_pile[oldest_freshkill_age]
                    self.freshkill_pile[oldest_freshkill_age] = 0
                oldest_freshkill_age -= 1
            self.freshkill_pile.pop(0)
            return True
        return False

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

    def _private_remove_freshkill(self, age: int, amount: float) -> float:
        """ Attempt to eat some amount at a specific age from the freshkill pile.

        Updates self.freshkill_pile if amount <= self.freshkill_pile[age].

        :param int age: How old is the freshkill you're trying to remove
        :param float amount: How much freshkill you are attempting to remove
        :return float: amount - the food available of age moons
        """
        if amount < 0:
            raise ValueError(f"You can't remove a negative amount of food from the freshkill pile")
        if age in self.freshkill_pile.keys():
            if amount < self.freshkill_pile[age]:
                self.freshkill_pile[age] = self.freshkill_pile[age] - amount
                amount = 0
            else:
                amount -= self.freshkill_pile[age]
                self.freshkill_pile.pop(age)
        return amount


########################################################################################################################
# Classes
########################################################################################################################

# TODO move `utility.clan_symbol_sprite` to either `red_clan.py` or `sprites.py`

# TODO include a HealerDen object
class RedClan:
    """ Clans full of Cats.

    Outsiders are also represented by Clans; there's one for kittypets and one for loners and rogues.
    """
    # TODO StarClan and the Dark Forest don't have reputations or inter-Clan relationships
    clan_prefix: str  # name
    clan_symbol: str

    # Clan history
    moon_established: int  # TODO inspired by LifeGen, allow Clans to be older when they are generated
    moon_destroyed: int = -1
    past_leader_ids: list[RedCat] = [] # TODO update in CatTracker.kill_cat, CatTracker.switch_clan
    past_deputy_ids: list[RedCat] = [] # TODO update in CatTracker.kill_cat, CatTracker.switch_clan
    past_healer_ids: list[RedCat] = [] # TODO update in CatTracker.kill_cat, CatTracker.switch_clan
    # clan_background: str
    # clan_flavours: list
    # clan_naming_themes: list  # TODO maybe replace this with leader naming themes?

    camp: Union[Camp | CampKey]  # Camp for the player Clan, CampKey for other warrior Clans
    default_afterlife: Location = Location.StarClan
    leader_lives_remaining = 0  # leader_lives # TODO should this be part of the Cat object?
    # NB: StarClan and Dark Forest cats aren't divided by Clan since in both, explicitly Clan differences are ignored
    clan_cats: dict[int, RedCat] = {}
    clan_cats_by_rank: dict[Rank, RedCat | list[RedCat]] = {
        Rank.Leader: None,
        Rank.Deputy: None,
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
    warrior_focus: WarriorFocus = WarriorFocus.NoFocus  # focus
    warrior_focus_arg: str = None  # focus_arg # For example, if the focus is on befriending WindClan, this would be "Wind"
    last_focus_change: int = 0  # moons_with_focus

    # leader focus
    leader_focus_clan_prefix: str = None  # e.g. "Thunder", "Sky"
    leader_focus_clan_purpose: LeaderFocus = LeaderFocus.NoFocus
    leader_focus_outsider_id: int = -1
    leader_focus_outsider_purpose: LeaderFocus = LeaderFocus.NoFocus

    # keeping self._amount_every_moon updated is computationally faster than calculating it every moon
    _amount_every_moon: float = 0

    # ------------------------------------- INIT ------------------------------------- #

    def __init__(self, clan_prefix: str, afterlife: Location, moon_established: int = 0):
        self.clan_prefix = clan_prefix
        self.moon_established = moon_established

        if afterlife.category is LocationCategory.Afterlife:
            self.default_afterlife = afterlife
        else:
            self.default_afterlife = Location.StarClan

        game.cat_tracker.add_new_clan(self)

    # --------------------------------- RANK CHANGES --------------------------------- #

    def new_leader(self, cat_obj: RedCat = None, leader_lives_remaining: int = 9):
        """ Set a given cat as the Clan leader, or promote the deputy. """
        if self.clan_cats_by_rank[Rank.Leader]:
            raise ValueError(f"{self.clan_prefix}Clan already has a leader, you can't choose a new one!")
        if not cat_obj:
            if not self.clan_cats_by_rank[Rank.Deputy]:
                self.new_deputy()
            self.new_leader(self.clan_cats_by_rank[Rank.Deputy])
            self.clan_cats_by_rank[Rank.Deputy] = None
        else:
            self.clan_cats_by_rank[Rank.Leader] = cat_obj
            self.leader_lives_remaining = 9
        return

    def kill_leader(self, remove_all_lives: bool = False):
        """ Take a leader's life. If the leader has run out of lives, kill them and set the position to empty. """
        if remove_all_lives:
            self.leader_lives_remaining = 0
        else:
            self.leader_lives_remaining -= 1
        if not self.leader_lives_remaining:
            # FIXME make a DeathEvent
            self.clan_cats_by_rank[Rank.Leader] = None
        return

    # TODO implement automatically choosing a deputy
    def new_deputy(self, cat_obj: RedCat = None):
        """ Promote a warrior to deputy. """
        if cat_obj:
            if not cat_obj in self.clan_cats_by_rank[Rank.Warrior]:
                raise KeyError(f"{cat_obj.name} not a Rank.Warrior; please make them "
                               f"one before electing them as deputy")
            self.clan_cats_by_rank[Rank.Warrior].remove(cat_obj)
            self.clan_cats_by_rank[Rank.Deputy] = cat_obj
        else:
            # choose a new deputy automatically
            raise NotImplementedError(f"Clan.new_deputy()")

    def change_rank(self, cat_obj: RedCat, new_rank: Rank, old_rank: Rank):
        """ Change a cat's rank (e.g. from warrior apprentice to healer apprentice). """

        # double-check that the cat's internal storage has been updated
        if not cat_obj.rank is new_rank:
            cat_obj.rank = new_rank

        # remove cat from their old rank
        if old_rank is Rank.Leader:
            raise ValueError(f"In order to demote a leader, use Clan.kill_leader(), not Clan.change_rank().")
        elif old_rank is Rank.Deputy:
            self.clan_cats_by_rank[Rank.Deputy] = None
        else:
            self.clan_cats_by_rank[old_rank].remove(cat_obj)
            if old_rank in (Rank.Healer, Rank.HealerApp):
                game.cat_tracker.remove_healer_cat(cat_obj=cat_obj)
            elif old_rank in (Rank.Queen, Rank.QueenApp):
                game.cat_tracker.remove_queen(clan_prefix=self.clan_prefix, professional=True, cat_obj=cat_obj)

        # add cat to their new rank
        if new_rank is Rank.Leader:
            self.new_leader(cat_obj=cat_obj)
        elif new_rank is Rank.Deputy:
            self.new_deputy(cat_obj=cat_obj)
        else:
            self.clan_cats_by_rank[new_rank].append(cat_obj)
            if new_rank in (Rank.Healer, Rank.HealerApp):
                game.cat_tracker.add_healer_cat(cat_obj=cat_obj)
            elif new_rank in (Rank.Queen, Rank.QueenApp):
                game.cat_tracker.add_queen(clan_prefix=self.clan_prefix, professional=True, cat_obj=cat_obj)

        return

    def new_healer_or_app(self, apprentice: bool, cat_obj: RedCat = None):
        """ Add a new healer or healer apprentice. """
        if apprentice:
            self.clan_cats_by_rank[Rank.HealerApp].append(cat_obj)
            game.cat_tracker.add_healer_cat(cat_obj)
        else:
            self.clan_cats_by_rank[Rank.Healer].append(cat_obj)
            game.cat_tracker.add_healer_cat(cat_obj)
        return

    def new_professional_queen_or_app(self, apprentice: bool, cat_obj: RedCat = None):
        """ Add a new queen or queen apprentice. """
        if apprentice:
            self.clan_cats_by_rank[Rank.QueenApp].append(cat_obj)
        else:
            self.clan_cats_by_rank[Rank.Queen].append(cat_obj)
            game.cat_tracker.add_queen(clan_prefix=self.clan_prefix, professional=True, cat_obj=cat_obj)
        return

    def add_cat_to_clan(self, position: Rank, cat_obj: RedCat):
        """ Add a cat to the Clan. """
        if cat_obj.cat_id in self.clan_cats:
            raise ValueError(f"{cat_obj.name} is already in {self.clan_prefix}Clan!")
        else:
            self.clan_cats[cat_obj.cat_id] = cat_obj
            cat_obj.clan_prefix = self.clan_prefix
            if self.clan_prefix == OUTSIDER_CLAN_PREFIX:
                # TODO account for the difference between rogues and loners
                cat_obj.rank = Rank.Loner
            else:
                if position is Rank.Leader:
                    self.clan_cats_by_rank[Rank.Warrior].append(cat_obj)
                    self.new_leader(cat_obj)
                elif position is Rank.Deputy:
                    self.clan_cats_by_rank[Rank.Warrior].append(cat_obj)
                    self.new_deputy(cat_obj)
                elif position is Rank.Healer:
                    self.clan_cats_by_rank[Rank.Healer].append(cat_obj)
                    game.cat_tracker.add_healer_cat(cat_obj)
                elif position is Rank.HealerApp:
                    self.clan_cats_by_rank[Rank.HealerApp].append(cat_obj)
                    game.cat_tracker.add_healer_cat(cat_obj)
                elif position is Rank.Queen:
                    self.clan_cats_by_rank[Rank.Queen].append(cat_obj)
                    game.cat_tracker.add_queen(clan_prefix=self.clan_prefix, professional=True, cat_obj=cat_obj)
                elif position is Rank.QueenApp:
                    self.clan_cats_by_rank[Rank.QueenApp].append(cat_obj)
                elif position is Rank.Mediator:
                    self.clan_cats_by_rank[Rank.Mediator].append(cat_obj)
                elif position is Rank.MediatorApp:
                    self.clan_cats_by_rank[Rank.MediatorApp].append(cat_obj)
                elif position is Rank.Warrior:
                    self.clan_cats_by_rank[Rank.Warrior].append(cat_obj)
                elif position is Rank.WarriorApp:
                    self.clan_cats_by_rank[Rank.WarriorApp].append(cat_obj)
                elif position is Rank.Kit:
                    self.clan_cats_by_rank[Rank.Kit].append(cat_obj)
                elif position is Rank.Elder:
                    self.clan_cats_by_rank[Rank.Elder].append(cat_obj)
        return

    def remove_cat_from_clan(self, cat_obj: RedCat):
        """ Remove a cat from the Clan.

        Called by CatTracker.change_cat_clan() and CatTracker.kill_cat().
        """
        cat_id: int = cat_obj.cat_id
        if cat_id in self.clan_cats:
            self.clan_cats.pop(cat_id)
        else:
            raise KeyError(f"{cat_obj.name} not in {self.clan_prefix}Clan, so can't be removed from it")

        # handle cats in special Clan positions
        cat_rank = cat_obj.rank
        if cat_rank is Rank.Leader:
            self.clan_cats_by_rank[Rank.Leader] = None
        elif cat_rank is Rank.Deputy:
            self.clan_cats_by_rank[Rank.Deputy] = None
        else:
            for rank in [r for r in self.clan_cats_by_rank if r not in (Rank.Leader, Rank.Deputy)]:
                if cat_obj in self.clan_cats_by_rank[rank]:
                    self.clan_cats_by_rank[rank].remove(cat_obj)
            if cat_rank in (Rank.Healer, Rank.HealerApp):
                game.cat_tracker.remove_healer_cat(cat_obj)
            elif cat_rank in (Rank.Queen, Rank.QueenApp):
                game.cat_tracker.remove_queen(clan_prefix=self.clan_prefix, professional=True, cat_obj=cat_obj)

        return

    def enough_healers_to_treat_cats(self) -> bool:
        """ Returns True if the Clan has enough medics and False otherwise. """
        # this is always allowed in story mode
        if config.settings.GameMode is GameMode.Story:
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
