# red_cat.py - Contains the Cat class.

# -------------------------------------------------------------------------------- #
# ----------------------------------------

########################################################################################################################
# Imports
########################################################################################################################

# from __future__ import annotations

# import ujson  # type: ignore
import random
from dataclasses import dataclass, field

from definitions import (
    Age,
    GenderAlign, GenderKits, cast_to_gender_align, cast_to_gender_kits,
    Location, cast_to_location,
    Pronouns, DEFAULT_PRONOUNS, parse_to_pronouns,
    Rank, cast_to_rank,
    RedSkill, SkillCategory, cast_to_skill,

    cast_to_language,
    ConditionCategory,
)
from scripts.game_structure.game_essentials import game
from scripts._red.cats.history.red_backstory import (RedBackstoryCategory, RedBackstory,
                                                     cast_to_backstory, cast_to_backstory_category)
from scripts._red.cats.history.red_history import RedHistory
from scripts._red.cats.red_name import RedName
from scripts._red.cats.red_pelt import CatPelt
from scripts._red.cats.red_condition import RedCondition, get_random_permanent_condition
from scripts._red.config_manager import config

import logging

from scripts._red.general_utils import one_in_num_chance

logger = logging.getLogger(__name__)



########################################################################################################################
# Constants
########################################################################################################################


########################################################################################################################
# Classes
########################################################################################################################

@dataclass
class CatHealth:
    paralysed: bool = False
    birth_cooldown: int = 0
    conditions: list[RedCondition] = field(default_factory=list)


class RedCat:
    """ The cat class.

    TODO
     - create_cat() includes game.cat_tracker.add_new_cat(cat_obj, alive)
     - kill_cat() includes game.cat_tracker.kill_cat(cat_id, location)
    """

    cat_id: int
    name: RedName
    pelt: CatPelt
    alive: bool = True
    faded: bool = False # TODO handle this - FadedCats shouldn't really be made into RedCat objects

    # status
    location: Location
    clan_prefix: str
    health: CatHealth = CatHealth()
    rank: Rank = None
    backstory: RedBackstory = RedBackstory.Unknown
    moons: int # the cat's current age (once a cat dies, this never changes)
    moons_dead: int
    skills: dict
    gender_kits: GenderKits
    gender_align: GenderAlign
    pronouns: Pronouns

    age: Age # TODO there shouldn't be both moons and age

    nutrition: int = 71
    history: RedHistory # maybe this should just be a dictionary where the key is the moon an event happened
    afterlife: Location # which afterlife is this cat headed toward? By default, the same as their Clan

    # flags
    favourite_f: bool = False
    no_kits_f: bool = False  # is this cat barred from having kits
    no_retire_f: bool = False  # is this cat barred from retiring due to old age or permanent conditions
    no_romance_f: bool = False  # if this cat barred from romantic changes and interactions

    # ------------------------------------- INIT ------------------------------------- #

    def __init__(self, save_file: dict = None, **kwargs, ):
        """ Initialise the cat. """
        if len(kwargs) > 20:
            raise ValueError(f"Tried to initialize a RedCat object with more than 20 kwargs")

        # if loading the cat from a save file, do that
        if save_file:
            self._parse_save_file(cat_id=kwargs["cat_id"], save=save_file)
            return
        else:
            if ( "backstory" in kwargs.keys() or "backstory_category" in kwargs.keys() ) and \
                    "moons" in kwargs.keys() and "clan_name" in kwargs.keys() and "alive" in kwargs.keys():
                self.create_new_cat(**kwargs)
            else:
                backstory = "missing"
                if "backstory_category" in kwargs.keys():
                    backstory = kwargs["backstory_category"]
                if "backstory" in kwargs.keys():
                    backstory = cast_to_backstory(kwargs["backstory"])
                raise KeyError(f"Creating a cat from scratch requires the creator to "
                               f"provide a valid backstory or backstory category and a valid age in moons.\n"
                               f"Moons: {'missing' if 'moons' not in kwargs.keys() else kwargs['moons']}\n"
                               f"RedBackstory (/category): {backstory}\n"
                               f"Clan: {'missing' if 'clan_name' not in kwargs.keys() else kwargs['clan_name']}Clan\n"
                               f"Alive: {'missing' if 'alive' not in kwargs.keys() else kwargs['alive']}"
                               )

        if kwargs:
            logger.warning(f"Did not use the following passed arguments when "
                           f"generating RedCat object with cat_id {self.cat_id}: {kwargs}")
        return

    def _parse_save_file(self, cat_id: int, save: dict):
        """ Parse the save file entry for a single cat. """
        save_file_sections: list[str] = list(save.keys())

        self.cat_id = cat_id

        # parse the cat's gender
        if "gender" in save_file_sections:
            save_file_sections.remove("gender")
            self.gender_kits = GenderKits(save["gender"])
            self.gender_align = GenderAlign(save["gender"])
            # FIXME pronouns should be independent of language? how does the translation work?
            if save["gender"]["custom_pronouns"]:
                self.pronouns = parse_to_pronouns(
                    save["gender"][cast_to_language(config.settings.Language)]["custom_pronouns"]
                )
            else:
                self.pronouns = DEFAULT_PRONOUNS[cast_to_language(config.settings.Language)][self.gender_align]
        else:
            raise KeyError(f"Could not find key 'gender' in save file cats.yaml for RedCat {self.cat_id}")

        # parse the cat's name
        if "name" in save_file_sections:
            save_file_sections.remove("name")
            self.name = RedName(prefix=save["name"]["prefix"], suffix=save["name"]["suffix"],
                                special_suffix_hidden=save["name"]["special_suffix_hidden"], load_existing_name=True)
        else:
            raise AttributeError(f"Could not assign a name to RedCat {self.cat_id} from the save file cats.yaml")

        # parse the cat's status
        if "status" in save_file_sections:
            save_file_sections.remove("status")
            self.moons = int(save["status"]["moons"])
            self.moons_dead = int(save["status"]["moons_dead"]) # if moons_dead = -1, the cat is alive
            self.alive = self.moons_dead >= 0
            self.location = cast_to_location(save["status"]["location"])
            self.health = save["status"]["health"]
            self.rank = cast_to_rank(save["status"]["rank"])
        else:
            raise KeyError(f"Could not find key 'status' in save file cats.yaml for RedCat {self.cat_id}")

        # parse the cat's pelt
        if "pelt" in save_file_sections:
            save_file_sections.remove("pelt")
            self.pelt = CatPelt(loading_from_save=True, save_file=save["pelt"])
        else:
            raise KeyError(f"Could not find key 'pelt' in save file cats.yaml for RedCat {self.cat_id}")

        # parse the cat's flags
        if "flags" in save_file_sections:
            save_file_sections.remove("flags")
            self.favourite_f = save["flags"]["favourite"]
            self.no_kits_f = save["flags"]["no_kits"]
            self.no_retire_f = save["flags"]["no_retire"]
            self.no_romance_f = save["flags"]["no_romance"]
        else:
            raise KeyError(f"Could not find key 'flags' in save file cats.yaml for RedCat {self.cat_id}")

        # parse the cat's history
        if "history" in save_file_sections:
            save_file_sections.remove("history")
            self.history = RedHistory(save_file=save["history"], cat_id=self.cat_id)
        else:
            raise KeyError(f"Could not find key 'history' in save file cats.yaml for RedCat {self.cat_id}")

        # TODO parse the cat's personality
        if "personality" in save_file_sections:
            raise NotImplementedError(f"RedCat objects can't parse a 'personality' section from cats.yaml yet")
        else:
            raise KeyError(f"Could not find key 'personality' in save file cats.yaml for RedCat {self.cat_id}")

        # TODO parse the cat's relationships
        if "relationships" in save_file_sections:
            self.mate_id = save["relationships"]["mate_id"]
            raise NotImplementedError(f"RedCat objects can't parse a 'relationships' section from cats.yaml yet")
        else:
            raise KeyError(f"Could not find key 'relationships' in save file cats.yaml for RedCat {self.cat_id}")

        # TODO parse the cat's skills
        if "skills" in save_file_sections:
            raise NotImplementedError(f"RedCat objects can't parse a 'skills' section from cats.yaml yet")
        else:
            raise KeyError(f"Could not find key 'skills' in save file cats.yaml for RedCat {self.cat_id}")

        # if save_file_sections still has any keys in it, then there was a section we weren't looking for
        if save_file_sections:
            raise KeyError(f"Unexpected key or keys in cats.yaml for RedCat {self.cat_id}: {save_file_sections}")

        # TODO add the cat to game.cat_tracker
        game.cat_tracker.add_new_cat(cat_obj=self, cat_id=self.cat_id)
        return

    def create_new_cat(self, alive: bool, clan_name: str, moons: int, parents: list = None, **kwargs):
        """ Generate a cat.

        Any attributes of the RedCat class not given will be randomly chosen (or chosen based
        on the parents if they are provided.)
        """

        if not parents:
            parents = []

        def get_social_skill_xp() -> int:
            """ Determine how good the cat is a specific kind of social interaction. """
            xp: int = 0
            for _ in range(self.moons):
                xp += random.randint(*config.cat_config.base_timeskip_xp_gain_social)
            return xp

        def get_rank_skill_xp() -> int:
            """ Determine how much skill a cat developed over its lifetime.

            This function assumes that only warriors (not healers, mediators, etc.) retire because of old age.
            FIXME It also doesn't account for retirement due to conditions, not age.
            """
            moons_spent_working: int = 0
            moons_spent_learning: int = 0
            xp: int = 0
            xp_bounds: tuple = (0, 0)
            if self.age in (Age.Newborn, Age.Kitten):
                pass # keep xp at 0

            elif self.rank.apprentice:
                # cats who haven't started working yet
                moons_spent_learning: int = (self.moons - config.cat_config.apprentice_age_moons)
                for moon in range(moons_spent_learning):
                    xp += random.randint(*config.cat_config.base_timeskip_xp_gain_rank[self.rank])

            elif self.rank in (Rank.Loner, Rank.Rogue, Rank.Kittypet):
                # outsiders
                for _ in range(self.moons):
                    xp += random.randint(*config.cat_config.base_timeskip_xp_gain_rank[self.rank])

            elif self.rank is Rank.Elder:
                # cats who stopped learning once they retired
                moons_spent_learning = config.cat_config.warrior_age_moons - config.cat_config.apprentice_age_moons
                for _ in range(moons_spent_learning):
                    xp += random.randint(*config.cat_config.base_timeskip_xp_gain_rank[Rank.WarriorApp])
                moons_spent_working = config.cat_config.elder_age_moons - config.cat_config.warrior_age_moons
                for _ in range(moons_spent_working):
                    xp += random.randint(*config.cat_config.base_timeskip_xp_gain_rank[Rank.Warrior])

            elif self.rank is Rank.Healer:
                # healers have different learning rates than warriors and mediators
                moons_spent_working = self.moons - config.cat_config.warrior_age_moons
                for _ in range(moons_spent_working):
                    xp += random.randint(*config.cat_config.base_timeskip_xp_gain_rank[Rank.Healer])
                moons_spent_learning = config.cat_config.warrior_age_moons - config.cat_config.apprentice_age_moons
                for _ in range(moons_spent_learning):
                    xp += random.randint(*config.cat_config.base_timeskip_xp_gain_rank[Rank.WarriorApp])

            elif self.rank is Rank.Mediator:
                # mediators have different learning rates than warriors and healers
                moons_spent_working = self.moons - config.cat_config.warrior_age_moons
                for _ in range(moons_spent_working):
                    xp += random.randint(*config.cat_config.base_timeskip_xp_gain_rank[Rank.Mediator])
                moons_spent_learning = config.cat_config.warrior_age_moons - config.cat_config.apprentice_age_moons
                for _ in range(moons_spent_learning):
                    xp += random.randint(*config.cat_config.base_timeskip_xp_gain_rank[Rank.MediatorApp])

            elif self.rank in (Rank.Warrior, Rank.Deputy, Rank.Leader):
                # warriors have different learning rates than healers and mediators
                moons_spent_working = self.moons - config.cat_config.warrior_age_moons
                for _ in range(moons_spent_working):
                    xp += random.randint(*config.cat_config.base_timeskip_xp_gain_rank[self.rank])
                moons_spent_learning = config.cat_config.warrior_age_moons - config.cat_config.apprentice_age_moons
                for _ in range(moons_spent_learning):
                    xp += random.randint(*config.cat_config.base_timeskip_xp_gain_rank[Rank.WarriorApp])

            else:
                raise ValueError(f"Can't figure out how much XP to give to a {self.rank}")
            return xp

        if alive:
            self.alive = True
        else:
            self.alive = False

        # set age
        if moons < 0:
            raise ValueError(f"A cat can't be less than 0 moons old. What are you doing?")
        self.moons = int(moons)

        # set Clan
        self.clan_prefix = clan_name

        # set backstory - prioritize specific backstories over backstory categories
        if "backstory" in kwargs.keys():
            self.backstory = cast_to_backstory(kwargs["backstory"])
            kwargs.pop("backstory")
        if "backstory_category" in kwargs.keys():
            if self.backstory is RedBackstory.Unknown:
                bc: RedBackstoryCategory = cast_to_backstory_category(kwargs["backstory_category"])
                self.backstory = random.choice( [b for b in list(RedBackstory) if b.category is bc] )
            kwargs.pop("backstory_category")

        # pick a gender (a cat transing their gender is handled in a random event) and pronouns
        if "gender_kits" in kwargs:
            self.gender_kits = cast_to_gender_kits(kwargs.pop("gender_kits"))
        else:
            if one_in_num_chance(num=config.cat_config.chance_gender_kits_intersex):
                self.gender_kits = GenderKits.Intersex
            elif one_in_num_chance(num=2):
                self.gender_kits = GenderKits.Female
            else:
                self.gender_kits = GenderKits.Male
        if "gender_align" in kwargs:
            self.gender_align = cast_to_gender_align(kwargs.pop("gender_align"))
            self.pronouns = DEFAULT_PRONOUNS[cast_to_language(config.settings.Language)][self.gender_align]
        else:
            if one_in_num_chance(num=config.cat_config.chance_gender_align_trans):
                # technically this means that they might randomly pick the gender that matches GenderKits
                self.gender_align = random.choice(list(GenderAlign))
            else:
                if self.gender_kits is GenderKits.Female:
                    self.gender_align = GenderAlign.Female
                elif self.gender_kits is GenderKits.Male:
                    self.gender_align = GenderAlign.Male
                else:
                    self.gender_align = GenderAlign.NonBinary
            self.pronouns = DEFAULT_PRONOUNS[cast_to_language(config.settings.Language)][self.gender_align]

        # pick a rank
        if "rank" in kwargs.keys():
            self.rank = cast_to_rank(kwargs["rank"])
            kwargs.pop("rank")
        if self.backstory.category is RedBackstoryCategory.Kittypet:
            self.rank = Rank.Kittypet
            self.location = Location.TwolegNest
        if self.backstory.category is RedBackstoryCategory.Loner:
            self.rank = Rank.Loner
            self.location = Location.Wilderness
        if self.backstory.category is RedBackstoryCategory.Rogue:
            self.rank = Rank.Rogue
            self.location = Location.Wilderness
        if self.moons < config.cat_config.apprentice_age_moons:
            self.rank = Rank.Kit
            self.location = Location.ClanNursery
        elif self.moons <= config.cat_config.warrior_age_moons:
            self.rank = Rank.WarriorApp
            self.location = Location.ClanApprentice
        elif self.moons >= config.cat_config.elder_age_moons and one_in_num_chance(3):
            self.rank = Rank.Elder
            self.location = Location.ClanElder
        else:
            self.rank = Rank.Warrior
            self.location = Location.ClanWarrior

        # pick skill(s)
        self.skills = {}
        if "skills" in kwargs:
            for skill in kwargs["skills"]:
                if cast_to_skill(skill).category is SkillCategory.Social and \
                    not self.rank in (Rank.Mediator, Rank.MediatorApp):
                    self.skills[cast_to_skill(skill)] = get_social_skill_xp()
                else:
                    self.skills[cast_to_skill(skill)] = get_rank_skill_xp()
            kwargs.pop("skills")
        else:
            # all randomly generated cats start with one social skill and one skill appropriate to their rank
            # assign rank skill first so that mediators don't get messed up
            rank_skill: RedSkill = None
            # TODO add Queen rank
            if self.rank is Rank.Kittypet:
                # kittypets only get social skills
                rank_skill = random.choice( [s for s in list(RedSkill) if s.category is SkillCategory.Social] )
            elif self.rank in (Rank.Healer, Rank.HealerApp):
                rank_skill = random.choice( [s for s in list(RedSkill) if s.category is SkillCategory.Healer] )
            elif self.rank in (Rank.Mediator, Rank.MediatorApp):
                rank_skill = random.choice( [s for s in list(RedSkill) if s.category is SkillCategory.Mediator] )
            else:
                rank_skill = random.choice( [s for s in list(RedSkill) if s.category is SkillCategory.Warrior] )
            self.skills[rank_skill] = get_rank_skill_xp()

            # now assign the social rank
            soc_skill: RedSkill = random.choice( [s for s in list(RedSkill) if
                                                  s.category is SkillCategory.Social and s not in self.skills.keys()] )
            self.skills[soc_skill] = get_social_skill_xp()

            # randomly, some cats might be clairvoyant
            if one_in_num_chance(config.cat_config.chance_clairvoyant):
                self.skills[RedSkill.Clairvoyance] = get_social_skill_xp()

        # determine if the cat has a permanent condition, and if so, what it is
        # TODO handle condition inheritance
        self.health = CatHealth()
        if one_in_num_chance(config.cat_config.chance_condition):
            pc = []
            for parent in parents:
                pc.extend( [c.name for c in parent.health.conditions if c.category is ConditionCategory.Permanent] )
            c: RedCondition = get_random_permanent_condition(parent_conditions=pc)
            if c.name in pc:
                c.is_genetic = True
            self.add_condition(condition=c)

        # generate the cat's pelt
        self.pelt = CatPelt(gender=self.gender_kits, parent_pelts=[p.pelt for p in parents])

        # generate the cat's name
        prefix = None
        suffix = None
        biome = None
        if "prefix" in kwargs:
            prefix = kwargs.pop("prefix")
        if "suffix" in kwargs:
            suffix = kwargs.pop("suffix")
        clan_obj = game.cat_tracker.get_clan_object(self.clan_prefix)
        if clan_obj.camp.value:
            biome = clan_obj.camp.biome
        self.name = RedName(prefix=prefix, suffix=suffix, biome=biome)

        game.cat_tracker.add_new_cat(cat_obj=self)
        return

    # ------------------------------------- KILL ------------------------------------- #

    def kill_cat(self):
        raise NotImplementedError("RedCat.kill_cat")

    # --------------------------------- RANK CHANGES --------------------------------- #

    def change_rank

    # ---------------------------------- CONDITIONS ---------------------------------- #

    def add_condition(self, condition: RedCondition):
        """ """
        self.health.conditions.append(condition)
        if condition.name == "paralyzed":
            self.health.paralysed = True
        return

    def remove_condition(self, condition: RedCondition):
        """ Remove a condition that is already in the cat's health. """
        if condition in self.health.conditions:
            self.health.conditions.remove(condition)
        else:
            logger.warning(f"Was asked to remove a condition from cat {self.cat_id} that it didn't have")
        return

    # ------------------------------------- MOON ------------------------------------- #

    # TODO
    def moon_passes(self):
        """ Simulate a single moon passing for this cat. """
        # TODO update the cat's age
        # TODO has the afterlife they'll go to changed
        # TODO have they had a litter (maybe only check this for GenderKits.Female cats)
        # TODO will they ask someone to be their mate
        # TODO will they get hurt
        # TODO will they go missing
        # TODO if a kitten, will they fail to thrive
        raise NotImplementedError(f"RedCat.moon_passes")

    # ------------------------------------ GETTER ------------------------------------ #

    def get_queen_object(self):
        """ Get the RedCat object of the nursing queen looking after this kit.

        :return RedCat: the queen if there is one, or None
        """
        parent_ids = self.history.attachments.parent_ids
        if not parent_ids:
            return None
        parent_objs: list = game.cat_tracker.get_cat_objects(parent_ids)
        for cat_obj in parent_objs:
            if self.cat_id in cat_obj.history.attachments.curr_litter_ids:
                return cat_obj
        return None
