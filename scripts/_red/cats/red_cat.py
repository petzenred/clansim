# red_cat.py - Contains the RedCat class.

########################################################################################################################
# Imports
########################################################################################################################

import random
from dataclasses import dataclass, field

import pygame

from definitions import (
    GenderAlign, GenderKits, cast_to_gender_align, cast_to_gender_kits,
    Location, cast_to_location,
    Pronouns, DEFAULT_PRONOUNS, parse_to_pronouns,
    Rank, cast_to_rank,
    RedSkill, SkillCategory, cast_to_skill,

    cast_to_language,
    ConditionCategory, SpritePose, PeltLength, Biome,
)
from scripts._red.red_exceptions import InitializationError
from scripts.game_structure.game_essentials import game
from scripts._red.cats.history.red_backstory import (RedBackstoryCategory, RedBackstory,
                                                     cast_to_backstory, cast_to_backstory_category)
from scripts._red.cats.history.red_history import RedHistory
from scripts._red.cats.red_personality import RedPersonality
from scripts._red.cats.red_name import RedName
from scripts._red.cats.red_pelt import CatPelt
from scripts._red.cats.red_condition import RedCondition, get_random_permanent_condition
from scripts._red.config_manager import config

from scripts._red.utils.general_utils import one_in_num_chance

import logging
logger = logging.getLogger(__name__)


########################################################################################################################
# Constants
########################################################################################################################


########################################################################################################################
# Classes
########################################################################################################################

@dataclass
class CatHealth:
    in_healer_den: bool = False # sick
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
    name: RedName = None
    pelt: CatPelt
    sprite_pose: SpritePose = SpritePose.UnchosenPose
    sprite_obj: pygame.Surface = None
    alive: bool = True
    faded: bool = False # TODO handle this - FadedCats shouldn't really be made into RedCat objects
    accessories: list = list() # TODO

    # personality
    lawfulness: int
    sociability: int
    aggression: int
    stability: int

    # status
    location: Location
    clan_token: str
    health: CatHealth = CatHealth()
    rank: Rank = None
    moons: int # the cat's current age (once a cat dies, this never changes)
    moons_dead: int
    skills: dict = {}
    gender_kits: GenderKits
    gender_align: GenderAlign
    pronouns: Pronouns

    nutrition: int = 71 # FIXME hardcoded number
    history: RedHistory # maybe this should just be a dictionary where the key is the moon an event happened
    backstory: RedBackstory = RedBackstory.Unknown
    # TODO dynamically update a cat's afterlife - maybe in RedPersonality? This is affected by their history
    #  and their personality
    afterlife: Location # which afterlife is this cat headed toward? By default, the same as their Clan

    # flags
    favourite_f: bool = False
    no_kits_f: bool = False  # is this cat barred from having kits
    no_retire_f: bool = False  # is this cat barred from retiring due to old age or permanent conditions
    no_romance_f: bool = False  # if this cat barred from romantic changes and interactions

    # ------------------------------------- INIT ------------------------------------- #

    def __init__(self, save_file: dict = None, autoadd_to_cat_tracker: bool = True, **kwargs, ):
        """ Initialize the cat. """
        if len(kwargs) > 20:
            raise ValueError(f"Tried to initialize a RedCat object with more than 20 kwargs. What the heck")

        # if loading the cat from a save file, do that
        if save_file:
            self.clan_token = kwargs.pop("clan_token")
            self._parse_cat_save_file(cat_id=kwargs["cat_id"], save_file=save_file)
            return
        else:
            required_keys: list[str] = ["moons", "clan_token", "alive", ]
            # make sure all the required keys are provided
            for rk in required_keys:
                if rk not in kwargs:
                    raise InitializationError(f"Can't initialize cat because of missing key \"{rk}\"")
            if not "backstory" in kwargs or not "backstory_category" in kwargs:
                bs: str = "missing" if "backstory" not in kwargs else kwargs["backstory"]
                raise InitializationError(
                    f"Creating a cat from scratch requires the creator to provide a valid backstory or "
                        f"backstory category and a valid age in moons.\n"
                    f"Moons [int]: {'missing' if 'moons' not in kwargs.keys() else kwargs['moons']}\n"
                    f"Backstory [RedBackstory/RedBackstoryCategory]: "
                        f"{bs if 'backstory_category' not in kwargs else kwargs['backstory_category']}\n"
                    f"Clan token [str]: {'missing' if 'clan_token' not in kwargs.keys() else kwargs['clan_token']}\n"
                    f"Clan name [str]: {'missing' if 'clan_name' not in kwargs.keys() else kwargs['clan_name']}\n"
                    f"Alive [bool]: {'missing' if 'alive' not in kwargs.keys() else kwargs['alive']}"
                )

            self._create_new_cat(autoadd_to_cat_tracker=autoadd_to_cat_tracker, **kwargs)

        if kwargs:
            logger.warning(f"Did not use the following passed arguments when "
                           f"generating RedCat object with cat_id {self.cat_id}: {kwargs}")
        return

    def _parse_cat_save_file(self, cat_id: int, save_file: dict):
        """ Parse the save file entry for a single cat. """
        save_file_sections: list[str] = list(save_file.keys())

        self.cat_id = cat_id

        try:
            # TODO parse the cat's nutrition - maybe integrate nutrition into health?

            # parse the cat's status
            # this needs to happen before parsing the cat's name
            # since verifying a name references this object.clan_token
            if "status" in save_file_sections:
                save_file_sections.remove("status")
                self.moons = int(save_file["status"]["moons"])
                self.moons_dead = int(save_file["status"]["moons_dead"]) # if moons_dead = -1, the cat is alive
                self.alive = self.moons_dead < 0
                self.location = cast_to_location(save_file["status"]["location"])
                self.health = CatHealth(save_file["status"]["health"])
                self.rank = cast_to_rank(save_file["status"]["rank"])
            else:
                raise InitializationError(f"Could not find key 'status' in save file for "
                                          f"cat #{self.cat_id} from {self.clan_token}")

            # parse the cat's name
            if "name" in save_file_sections:
                save_file_sections.remove("name")
                self.name = RedName(cat_obj=self, save_file=save_file["name"])
            else:
                raise InitializationError(f"Could not find key 'name' in save file for cat #{self.cat_id}")

            # parse the cat's gender
            if "gender" in save_file_sections:
                save_file_sections.remove("gender")
                self.gender_kits = GenderKits(save_file["gender"]["kits"])
                self.gender_align = GenderAlign(save_file["gender"]["align"])
                # FIXME pronouns should be independent of language? how does the translation work?
                if save_file["gender"]["custom_pronouns"]:
                    self.pronouns = parse_to_pronouns(
                        save_file["gender"]["custom_pronouns"][cast_to_language(config.settings.Language)]
                    )
                else:
                    self.pronouns = DEFAULT_PRONOUNS[cast_to_language(config.settings.Language)][self.gender_align]
            else:
                raise InitializationError(f"Could not find key 'gender' in save file for "
                                          f"cat #{self.cat_id} from {self.clan_token}")

            # parse the cat's pelt
            if "pelt" in save_file_sections:
                save_file_sections.remove("pelt")
                self.pelt = CatPelt(loading_from_save=True, save_file=save_file["pelt"])
            else:
                raise InitializationError(f"Could not find key 'pelt' in save file for "
                                          f"cat #{self.cat_id} from {self.clan_token}")

            # parse the cat's flags
            if "flags" in save_file_sections:
                save_file_sections.remove("flags")
                self.favourite_f = save_file["flags"]["favourite"]
                self.no_kits_f = save_file["flags"]["no_kits"]
                self.no_retire_f = save_file["flags"]["no_retire"]
                self.no_romance_f = save_file["flags"]["no_romance"]
            else:
                raise InitializationError(f"Could not find key 'flags' in save file for "
                                          f"cat #{self.cat_id} from {self.clan_token}")

            # parse the cat's personality
            if "personality" in save_file_sections:
                save_file_sections.remove("personality")
                self.lawfulness = int(save_file["personality"]["lawfulness"])
                self.sociability = int(save_file["personality"]["sociability"])
                self.aggression = int(save_file["personality"]["aggression"])
                self.stability = int(save_file["personality"]["stability"])
            else:
                raise InitializationError(f"Could not find key 'personality' in save file for "
                                          f"cat #{self.cat_id} from {self.clan_token}")

            # parse the cat's skills
            if "skills" in save_file_sections:
                # skills is a dictionary of names and the amount of XP the cat has in said skill
                save_file_sections.remove("skills")
                for skill_name in save_file["skills"]:
                    self.skills[RedSkill(skill_name)] = save_file["skills"][skill_name]
            else:
                raise InitializationError(f"Could not find key 'skills' in save file for cat #{self.cat_id} "
                                          f"from {self.clan_token}")

            # TODO parse the cat's history
            # if "history" in save_file_sections:
            #     save_file_sections.remove("history")
            #     self.history = RedHistory(save_file=save["history"], cat_id=self.cat_id)
            # else:
            #     raise InitializationError(f"Could not find key 'history' in save file for "
            #                               f"cat #{self.cat_id} from {self.clan_token}")

            # TODO parse the cat's relationships
            # TODO relationships is now its own file
            # if "relationships" in save_file_sections:
            #     self.mate_id = save["relationships"]["mate_id"]
            #     raise NotImplementedError(f"RedCat objects can't parse a 'relationships' section from cats.yaml yet")
            # else:
            #     raise KeyError(f"Could not find key 'relationships' in save file for cat #{self.cat_id}")

        except BaseException as err:
            logger.exception(msg=f"There was an exception while loading cat #{self.cat_id} from {self.clan_token}",
                             exc_info=err)
            msg: str = f"{self.name} (cat_id #{self.cat_id})" if self.name else f" with cat_id #{self.cat_id}"
            msg += (f", member of group with token \"{self.clan_token}\" wasn't added to the CatTracker "
                    f"because something went wrong while parsing their save file")
            logger.warning(msg)
            # TODO close the game if there's an error when loading, instead of letting it hang. But in main, not here
            game.quit(savesettings=False, clearevents=False)

        else:
            # if there are any keys remaining in the save file that didn't get used, make sure that gets logged
            if save_file:
                logger.warning(f"After creating the {self.name} RedCat object (Clan token {self.clan_token}), there "
                               f"was some information in the save file which wasn't used:\n{save_file_sections}")

            game.cat_tracker.add_cat_to_tracker(cat_obj=self, cat_id=self.cat_id)
            return

    def _create_new_cat(self, autoadd_to_cat_tracker: bool, **kwargs):
        """ Generate a cat.

        Any attributes of the RedCat class not given will be randomly chosen (or chosen based
        on the parents if they are provided.)

        TODO make sure that cats who are generated already dead have a Clan that they were a member of, if relevant
        """

        if "parents" not in kwargs:
            parents = []
        else:
            parents = kwargs.pop("parents")

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
            if self.moons < config.cat_config.adolescent_age_moons:
                pass # keep xp at 0

            elif self.rank.is_apprentice:
                # cats who haven't started working yet
                moons_spent_learning: int = (self.moons - config.cat_config.adolescent_age_moons)
                for moon in range(moons_spent_learning):
                    xp += random.randint(*config.cat_config.base_timeskip_xp_gain_rank[self.rank])

            elif self.rank in (Rank.Loner, Rank.Rogue, Rank.Kittypet):
                # outsiders
                for _ in range(self.moons):
                    xp += random.randint(*config.cat_config.base_timeskip_xp_gain_rank[self.rank])

            elif self.rank is Rank.Elder:
                # cats who stopped learning once they retired
                moons_spent_learning = config.cat_config.young_adult_age_moons - config.cat_config.adolescent_age_moons
                for _ in range(moons_spent_learning):
                    xp += random.randint(*config.cat_config.base_timeskip_xp_gain_rank[Rank.WarriorApp])
                moons_spent_working = config.cat_config.elder_age_moons - config.cat_config.young_adult_age_moons
                for _ in range(moons_spent_working):
                    xp += random.randint(*config.cat_config.base_timeskip_xp_gain_rank[Rank.Warrior])

            elif self.rank is Rank.Healer:
                # healers have different learning rates than warriors and mediators
                moons_spent_working = self.moons - config.cat_config.young_adult_age_moons
                for _ in range(moons_spent_working):
                    xp += random.randint(*config.cat_config.base_timeskip_xp_gain_rank[Rank.Healer])
                moons_spent_learning = config.cat_config.young_adult_age_moons - config.cat_config.adolescent_age_moons
                for _ in range(moons_spent_learning):
                    xp += random.randint(*config.cat_config.base_timeskip_xp_gain_rank[Rank.WarriorApp])

            elif self.rank is Rank.Mediator:
                # mediators have different learning rates than warriors and healers
                moons_spent_working = self.moons - config.cat_config.young_adult_age_moons
                for _ in range(moons_spent_working):
                    xp += random.randint(*config.cat_config.base_timeskip_xp_gain_rank[Rank.Mediator])
                moons_spent_learning = config.cat_config.young_adult_age_moons - config.cat_config.adolescent_age_moons
                for _ in range(moons_spent_learning):
                    xp += random.randint(*config.cat_config.base_timeskip_xp_gain_rank[Rank.MediatorApp])

            elif self.rank in (Rank.Warrior, Rank.Deputy, Rank.Leader):
                # warriors have different learning rates than healers and mediators
                moons_spent_working = self.moons - config.cat_config.young_adult_age_moons
                for _ in range(moons_spent_working):
                    xp += random.randint(*config.cat_config.base_timeskip_xp_gain_rank[self.rank])
                moons_spent_learning = config.cat_config.young_adult_age_moons - config.cat_config.adolescent_age_moons
                for _ in range(moons_spent_learning):
                    xp += random.randint(*config.cat_config.base_timeskip_xp_gain_rank[Rank.WarriorApp])

            else:
                raise ValueError(f"Can't figure out how much XP to give to a {self.rank}")
            return xp

        if kwargs["alive"]:
            self.alive = True
        else:
            self.alive = False

        # set age
        if kwargs["moons"] < 0:
            raise ValueError(f"A cat can't be less than 0 moons old. What are you doing?")
        self.moons = int(kwargs["moons"])

        # set Clan
        self.clan_token = kwargs["clan_token"]

        # FIXME cat history and backstory
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
        if self.moons < config.cat_config.adolescent_age_moons:
            self.rank = Rank.Kit
            self.location = Location.ClanNursery
        elif self.moons <= config.cat_config.young_adult_age_moons:
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
        prefix = ""
        suffix = ""
        biome = Biome.NoBiome
        if "prefix" in kwargs:
            prefix = kwargs.pop("prefix")
        if "suffix" in kwargs:
            suffix = kwargs.pop("suffix")
        clan_obj = game.cat_tracker.get_clan_object(self.clan_token)
        if clan_obj.camp.value:
            biome = clan_obj.camp.biome
        self.name = RedName(cat_obj=self, prefix=prefix, suffix=suffix, biome=biome,)

        # add the cat to the cat tracker (maybe)
        if autoadd_to_cat_tracker:
            game.cat_tracker.add_cat_to_tracker(cat_obj=self)
        return

    # ------------------------------- SETTER FUNCTIONS ------------------------------- #

    def kill(self):
        """ Kill this cat. """
        # the CatTracker updates the RedClan object this cat is a member of
        game.cat_tracker.kill_cat(cat_obj=self, afterlife=self.afterlife)

        self.location = self.afterlife # leave Clan prefix as it was, but change the location
        self.alive = False
        self.moons_dead = 0

        # TODO account for death message being passed (e.g. from Kill Cat screen in profile menu, or from an event)
        return

    def change_clan(self, new_clan_token: str, new_rank: Rank = None):
        """ Move the cat to a new Clan, potentially with a new rank.

        :param str new_clan_token: the Clan's identifying token
        :param Rank new_rank: the rank to add the cat to
        """
        # Can't really change too much here, since when nursing queens switch Clans, their kits are automatically
        # moved with them in the CatTracker. Therefore, all the work is done there.
        game.cat_tracker.change_cat_clan(new_clan_token=new_clan_token, cat_obj=self, new_rank=new_rank)
        return

    def change_rank(self, new_rank: Rank):
        """ Update the cat's rank, and update their Clan on the rank change.

        :param Rank new_rank: the rank to add the cat to
        """
        clan_obj = game.cat_tracker.get_clan_object(clan_token=self.clan_token)
        clan_obj.change_cat_rank_from_cat_object(cat_obj=self, new_rank=new_rank, old_rank=self.rank)
        return

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
        # TODO have they had a litter or gotten pregnant
        if self.gender_kits is GenderKits.Female or config.settings.MiracleGays:
            pass
        # TODO will they ask someone to be their mate
        # TODO will they get hurt
        # TODO will they go missing
        # TODO if a kitten, will they fail to thrive
        raise NotImplementedError(f"RedCat.moon_passes")

    # ------------------------------------ GETTER ------------------------------------ #

    def get_queen_object(self):
        """ Get the RedCat object of the nursing queen looking after this kit.

        :return: the queen if there is one, or None
        :rtype: RedCat
        """
        parent_ids = self.history.attachments.parent_ids
        if not parent_ids:
            return None
        parent_objs: list = game.cat_tracker.get_cat_objects(parent_ids)
        for cat_obj in parent_objs:
            if self.cat_id in cat_obj.history.attachments.curr_litter_ids:
                return cat_obj
        return None

    # TODO
    def get_sprite(self) -> pygame.Surface:
        """ Update the cat's sprite if necessary and return it.

        :return: the cat's sprite
        :rtype: pygame.Surface
        """
        """
        
            # First, check if the cat is faded.
            if cat.faded:
                # Don't update the sprite if the cat is faded.
                return
    
            # apply
            cat.sprite = generate_sprite(cat)
            # update class dictionary
            cat.all_cats[cat.ID] = cat
        
        """
        raise NotImplementedError("RedCat.get_sprite")

    # ------------------------------------ PRIVATE ----------------------------------- #

    # TODO
    def _update_sprite_pose(self):
        """ TODO """
        # cats in the healer's den
        if self.health.in_healer_den:
            if self.moons < config.cat_config.young_adult_age_moons:
                self.sprite_pose = SpritePose.SickAdult
            else:
                self.sprite_pose = SpritePose.SickYoung

        # cats who are permanently paralysed
        if self.health.paralysed:
            if self.moons < config.cat_config.young_adult_age_moons:
                self.sprite_pose = SpritePose.ParaYoung
            else:
                if self.pelt.length is PeltLength.Long:
                    self.sprite_pose = SpritePose.ParaAdultLong
                else:
                    self.sprite_pose = SpritePose.ParaAdultShort

        # all other cats
        if self.moons < 1:
            self.sprite_pose = self.pelt.sprites[""]


