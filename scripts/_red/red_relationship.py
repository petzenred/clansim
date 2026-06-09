# red_relationship.py - Class containing Relationship details.

# -------------------------------------------------------------------------------- #
# ----------------------------------------

########################################################################################################################
# Imports
########################################################################################################################

# this prevents other modules importing anything but the global object 'global_rels'
#   at the bottom of this file without specifically trying to
__all__ = ['global_rels']

import random

from scripts._red.io_manager import io_manager
from scripts._red.config_manager import config
from scripts.game_structure.game_essentials import game
from definitions import RelationshipAspect, cast_to_relationship_aspect


########################################################################################################################
# Methods
########################################################################################################################

def _load_relationships_file():
    """ Parse the relationships file. """
    return io_manager.read_relationships_save_file()


########################################################################################################################
# Class
########################################################################################################################

# TODO combine this with game.cat_tracker?
class RedRelationshipTracker:
    """ Holds relationship information and allows the game to edit them safely. """

    cat_relationships: dict
    clan_relationships: dict

    # ------------------------------------- INIT ------------------------------------- #

    def __init__(self):
        self.refresh_from_save_file()
        return

    def refresh_from_save_file(self):
        """ Replace the currently-saved relationships from the active Clan's savefile.

        WARNING! Doesn't save the current relationships first. You'll lose data if you
        use this method without saving first.
        """
        relationships = _load_relationships_file()

        # parse cat relationships
        self.cat_relationships: dict = {}
        for from_cat_id in relationships["cats"]:
            from_cat_rels: dict = {}
            for to_cat_id in relationships["cats"][from_cat_id]:
                old_rel: dict = relationships["cats"][from_cat_id][to_cat_id]
                to_cat_rel: dict = {}
                # get rid of relationships that are empty
                if not [aspect for aspect in old_rel.values() if bool(aspect)]:
                    continue
                # replace word keys with enum keys
                for aspect in list(old_rel.keys()):
                    if aspect == "log":
                        to_cat_rel.update({"log": old_rel["log"]})
                        continue # don't need to do anything with this
                    aspect_value: int = old_rel.pop(aspect)
                    aspect_enum: RelationshipAspect = cast_to_relationship_aspect(aspect)
                    to_cat_rel.update({aspect_enum: aspect_value})
                from_cat_rels.update({to_cat_id: to_cat_rel})
            self.cat_relationships.update({from_cat_id: from_cat_rels})

        # TODO parse Clan relationships
        self.clan_relationships = relationships["clans"]
        return

    def get_save_file_data(self) -> tuple[dict, dict]:
        """ Get the current relationship data. """
        return self.cat_relationships, self.clan_relationships

    # ------------------------------------- CATS ------------------------------------- #

    def cat_change_relationship(self, holder: int, subject: int):
        """ Update a relationship between two cats. """
        raise NotImplementedError("RedRelationshipTracker.cat_change_relationship")

    def cat_get_relationship(self, holder: int, subject: int):
        """ Get the details of how holder feels about subject. """
        return self.cat_relationships[holder][subject]

    def cat_get_highest_romance(self,
                                holder_id: int,
                                exclude_mate: bool = False,
                                only_potential_mate: bool = True
                                ) -> int:
        """ Get the cat_id of the cat who holder has the strongest romantic feelings for.

        If two or more cats tie, one of the tied cats will be randomly chosen.

        :param int holder_id: the cat whose romantic interest you're searching for
        :param bool exclude_mate: if True, cats who are the mate of holder will be filtered out
        :param bool only_potential_mate: if True, cats who couldn't become the mate of holder will be
            filtered out (e.g. kittens)
        :return int: the ID of the cat who holder has the strongest romantic feelings for
        """
        max_love_value: int = 0
        winner_ids: list = [None]
        for to_cat_id in self.cat_relationships[holder_id]:
            rel = self.cat_relationships[holder_id][to_cat_id]
            if rel[RelationshipAspect.Romance] > max_love_value:
                max_love_value = rel[RelationshipAspect.Romance]
                winner_ids = [to_cat_id]
            elif max_love_value and rel[RelationshipAspect.Romance] == max_love_value:
                winner_ids.append(to_cat_id)

        for winner_id in winner_ids:
            if exclude_mate:
                if winner_id in game.cat_tracker.living_cats[holder_id].mate_ids:
                    winner_ids.remove(winner_id)
            if only_potential_mate:
                if not self.cat_is_potential_mate(holder_id=holder_id, subject_id=winner_id, no_mates=False):
                    winner_ids.remove(winner_id)

        return random.choice(winner_ids)

    def cat_is_potential_mate(self, holder_id: int, subject_id: int, no_mates: bool = True) -> bool:
        """ Checks if the two cats provided are allowed to become mates.

        :param int holder_id: the cat_id of the first of the cats whose compatibility is being checked
        :param int subject: the cat_id of the second of the cats whose compatibility is being checked
        :param bool no_mates: if True, the method can only return True if both cats are single
        """
        # get the RedCat objects from the cat tracker
        holder_obj = game.cat_tracker.living_cats[holder_id]
        subject_obj = game.cat_tracker.living_cats[subject_id]
        # cats can't be mates with themselves
        if holder_id == subject_id:
            return False
        # children can't have mates, not apprentices regardless of age
        if (holder_obj.moons < config.cat_config.young_adult_age_moons) or holder_obj.rank.is_apprentice:
            return False
        # if only single cats are allowed, make sure both cats are single
        if no_mates and (holder_obj.mate_ids or subject_obj.mate_ids):
            return False
        if config.settings.RomanceFormerApprentice: # TODO make sure True for this *DIS*allows dating ex-apprentices
            if subject_id in holder_obj.prev_apps or holder_id in subject_obj.prev_apps:
                return False
        if config.settings.RomanceFirstCousin:
            # TODO fill this out when I figure out how parents are saved - if the two cats have
            #   at least one grandparent in common, then they're first cousins
            pass
        if abs(holder_obj.moons - subject_obj.moons) >= config.rel_config.mates_max_age_diff:
            return False
        return True



    # TODO create new relationship
    # TODO scripts.utility.check_relationship_value(cat_from, cat_to, rel_value=None)
    # TODO scripts.utility.get_personality_compatibility(cat1, cat2)
    # TODO scripts.utility.get_cats_of_romantic_interest(cat)
    # TODO scripts.utility.get_amount_of_cats_with_relation_value_towards(cat, value, living_cats)
    # TODO scripts.utility.filter_relationship_type(
    #         group: list, filter_types: List[str], event_id: str = None, patrol_leader=None
    # )
    # TODO scripts.utility.gather_cat_objects(
    #         Cat, abbr_list: List[str], event, stat_cat=None, extra_cat=None
    # )
    # TODO scripts.utility.unpack_rel_block(
    #         Cat, relationship_effects: List[dict], event=None, stat_cat=None, extra_cat=None
    # )
    # TODO scripts.utility.change_relationship_values(
    #         cats_to: list,
    #         cats_from: list,
    #         romantic_love: int = 0,
    #         platonic_like: int = 0,
    #         dislike: int = 0,
    #         admiration: int = 0,
    #         comfortable: int = 0,
    #         jealousy: int = 0,
    #         trust: int = 0,
    #         auto_romance: bool = False,
    #         log: str = None)

    # ------------------------------------ CLANS ------------------------------------- #

    # TODO
    def clan_get_relationship(self, holder=None, subject=None):
        """ Get the details of how holder feels about subject. """
        raise NotImplementedError("RedRelationshipTracker.clan_get_relationship")

    # TODO
    def clan_update_relationship(self, clan_1, clan_2, change: int):
        """ Update the relationship between two Clans. """
        raise NotImplementedError("RedRelationshipTracker.clan_update_relationship")


########################################################################################################################
# Objects
########################################################################################################################

global_rels: RedRelationshipTracker = RedRelationshipTracker()
