# pylint: disable=line-too-long
"""

TODO: Docs


"""  # pylint: enable=line-too-long

import os
import re as regex
from itertools import combinations
from math import floor
from random import choice, randint, random, sample
from sys import exit as sys_exit
from typing import List, Tuple, TYPE_CHECKING, Type, Union

import i18n
import pygame
import ujson
from pygame_gui.core import ObjectID

from scripts.game_structure.localization import (
    load_lang_resource,
    determine_plural_pronouns,
    get_lang_config,
)

from definitions import (
    Age, Rank, Season, YEAR_SEASONS,
)
from scripts.game_structure import image_cache, localization
from scripts.cat.sprites import sprites
from scripts.game_structure.game_essentials import game
import scripts.game_structure.screen_settings  # must be done like this to get updates when we change screen size etc


""" 
Getting Cats -> mostly now in cat_tracker.py

"""

if TYPE_CHECKING:
    from scripts.cat.cats import Cat

import logging
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------- #
#                               Getting Cats                                   #
# ---------------------------------------------------------------------------- #


def get_alive_clan_queens(living_cats):
    living_kits = [
        cat
        for cat in living_cats
        if not (cat.dead or cat.outside) and cat.status in [Rank.Kit, Rank.Newborn]
    ]

    queen_dict = {}
    for cat in living_kits.copy():
        parents = cat.get_parents()
        # Fetch parent object, only alive and not outside.
        parents = [
            cat.fetch_cat(i)
            for i in parents
            if cat.fetch_cat(i)
               and not (cat.fetch_cat(i).dead or cat.fetch_cat(i).outside)
        ]
        if not parents:
            continue

        if (
                len(parents) == 1
                or len(parents) > 2
                or all(i.gender == "male" for i in parents)
                or parents[0].gender == "female"
        ):
            if parents[0].ID in queen_dict:
                queen_dict[parents[0].ID].append(cat)
                living_kits.remove(cat)
            else:
                queen_dict[parents[0].ID] = [cat]
                living_kits.remove(cat)
        elif len(parents) == 2:
            if parents[1].ID in queen_dict:
                queen_dict[parents[1].ID].append(cat)
                living_kits.remove(cat)
            else:
                queen_dict[parents[1].ID] = [cat]
                living_kits.remove(cat)
    return queen_dict, living_kits


def get_alive_status_cats(
        Cat: Union["Cat", Type["Cat"]],
        get_status: list,
        working: bool = False,
        sort: bool = False,
) -> list:
    """
    returns a list of cat objects for all living cats of get_status in Clan
    :param Cat Cat: Cat class
    :param list get_status: list of statuses searching for
    :param bool working: default False, set to True if you would like the list to only include working cats
    :param bool sort: default False, set to True if you would like list sorted by descending moon age
    """

    alive_cats = [
        i
        for i in Cat.all_cats.values()
        if i.status in get_status and not i.dead and not i.outside
    ]

    if working:
        alive_cats = [i for i in alive_cats if not i.not_working()]

    if sort:
        alive_cats = sorted(alive_cats, key=lambda cat: cat.moons, reverse=True)

    return alive_cats


def get_living_cat_count(Cat):
    """
    Returns the int of all living cats, both in and out of the Clan
    :param Cat: Cat class
    """
    count = 0
    for the_cat in Cat.all_cats.values():
        if the_cat.dead:
            continue
        count += 1
    return count


def get_living_clan_cat_count(Cat):
    """
    Returns the int of all living cats within the Clan
    :param Cat: Cat class
    """
    count = 0
    for the_cat in Cat.all_cats.values():
        if the_cat.dead or the_cat.exiled or the_cat.outside:
            continue
        count += 1
    return count


def get_cats_same_age(Cat, cat, age_range=10):
    """
    Look for all cats in the Clan and returns a list of cats which are in the same age range as the given cat.
    :param Cat: Cat class
    :param cat: the given cat
    :param int age_range: The allowed age difference between the two cats, default 10
    """
    cats = []
    for inter_cat in Cat.all_cats.values():
        if inter_cat.dead or inter_cat.outside or inter_cat.exiled:
            continue
        if inter_cat.ID == cat.ID:
            continue

        if inter_cat.ID not in cat.relationships:
            cat.create_one_relationship(inter_cat)
            if cat.ID not in inter_cat.relationships:
                inter_cat.create_one_relationship(cat)
            continue

        if (
                inter_cat.moons <= cat.moons + age_range
                and inter_cat.moons <= cat.moons - age_range
        ):
            cats.append(inter_cat)

    return cats


def get_free_possible_mates(cat):
    """Returns a list of available cats, which are possible mates for the given cat."""
    cats = []
    for inter_cat in cat.all_cats.values():
        if inter_cat.dead or inter_cat.outside or inter_cat.exiled:
            continue
        if inter_cat.ID == cat.ID:
            continue

        if inter_cat.ID not in cat.relationships:
            cat.create_one_relationship(inter_cat)
            if cat.ID not in inter_cat.relationships:
                inter_cat.create_one_relationship(cat)
            continue

        if inter_cat.is_potential_mate(cat, for_love_interest=True):
            cats.append(inter_cat)
    return cats


def get_random_moon_cat(
        Cat, main_cat, parent_child_modifier: bool = True, mentor_app_modifier: bool = True
):
    """
    returns a random cat for use in moon events
    :param Cat: Cat class
    :param main_cat: cat object of main cat in event
    :param parent_child_modifier: increase the chance of the random cat being a
    parent of the main cat. Default True
    :param mentor_app_modifier: increase the chance of the random cat being a mentor or
    app of the main cat. Default True
    TODO
     - Move this function so that you don't have to pass Cat as a param to avoid circular imports.
    """
    random_cat: Cat = None

    # grab list of possible random cats
    possible_r_c = list(
        filter(
            lambda c: not c.dead
                      and not c.exiled
                      and not c.outside
                      and (c.ID != main_cat.ID),
            Cat.all_cats.values(),
        )
    )

    if possible_r_c:
        random_cat = choice(possible_r_c)
        if parent_child_modifier and not int(random() * 3):
            possible_parents = []
            if main_cat.parent1:
                if Cat.fetch_cat(main_cat.parent1) in possible_r_c:
                    possible_parents.append(main_cat.parent1)
            if main_cat.parent2:
                if Cat.fetch_cat(main_cat.parent2) in possible_r_c:
                    possible_parents.append(main_cat.parent2)
            if main_cat.adoptive_parents:
                for parent in main_cat.adoptive_parents:
                    if Cat.fetch_cat(parent) in possible_r_c:
                        possible_parents.append(parent)
            if possible_parents:
                random_cat = Cat.fetch_cat(choice(possible_parents))
        if mentor_app_modifier:
            if (
                    main_cat.status.apprentice
                    and main_cat.mentor
                    and not int(random() * 3)
            ):
                random_cat = Cat.fetch_cat(main_cat.mentor)
            elif main_cat.apprentice and not int(random() * 3):
                random_cat = Cat.fetch_cat(choice(main_cat.apprentice))

    if isinstance(random_cat, str):
        logger.warning(f"Random cat was {random_cat} instead of cat object")
        random_cat = Cat.fetch_cat(random_cat)
    return random_cat


def get_warring_clan():
    """
    returns enemy clan if a war is currently ongoing
    """
    enemy_clan = None
    if game.clan_obj.war.get("at_war", False):
        for other_clan in game.clan_obj.all_clans:
            if other_clan.name == game.clan_obj.war["enemy"]:
                enemy_clan = other_clan

    return enemy_clan


# ---------------------------------------------------------------------------- #
#                          Handling Outside Factors                            #
# ---------------------------------------------------------------------------- #


def get_current_season():
    """
    function to handle the math for finding the Clan's current season
    :return: the Clan's current season
    """

    if game._game_config["lock_season"]:
        game.clan_obj.current_season = game.clan_obj.starting_season
        return game.clan_obj.starting_season

    modifiers = {Season.Spring: 0, Season.Summer: 3, Season.Autumn: 6, Season.Winter: 9}
    index = game.clan_obj.age % 12 + modifiers[game.clan_obj.starting_season]

    if index > 11:
        index = index - 12

    game.clan_obj.current_season = YEAR_SEASONS[index]

    return game.clan_obj.current_season


def change_clan_reputation(difference):
    """
    will change the Clan's reputation with outsider cats according to the difference parameter.
    """
    game.clan_obj.reputation += difference


def change_clan_relations(other_clan, difference):
    """
    will change the Clan's relation with other clans according to the difference parameter.
    """
    # grab the clan that has been indicated
    other_clan = other_clan
    # grab the relation value for that clan
    y = game.clan_obj.all_clans.index(other_clan)
    clan_relations = int(game.clan_obj.all_clans[y].relations)
    # change the value
    clan_relations += difference
    # making sure it doesn't exceed the bounds
    if clan_relations > 30:
        clan_relations = 30
    elif clan_relations < 0:
        clan_relations = 0
    # setting it in the Clan save
    game.clan_obj.all_clans[y].relations = clan_relations


def get_other_clan(clan_name):
    """
    returns the clan object of given clan name
    """
    for clan in game.clan_obj.all_clans:
        if clan.name == clan_name:
            return clan


# ---------------------------------------------------------------------------- #
#                             Cat Relationships                                #
# ---------------------------------------------------------------------------- #

# TODO use global_rels.cat_get_highest_romance instead
def get_highest_romantic_relation(
        relationships, exclude_mate=False, potential_mate=False
):
    """Returns the relationship with the highest romantic value."""
    max_love_value = 0
    current_max_relationship = None
    for rel in relationships:
        if rel.romantic_love < 0:
            continue
        if exclude_mate and rel.cat_from.ID in rel.cat_to.mate:
            continue
        if potential_mate and not rel.cat_to.is_potential_mate(
                rel.cat_from, for_love_interest=True
        ):
            continue
        if rel.romantic_love > max_love_value:
            current_max_relationship = rel
            max_love_value = rel.romantic_love

    return current_max_relationship

# TODO replace with global_rels.
def check_relationship_value(cat_from, cat_to, rel_value=None):
    """
    returns the value of the rel_value param given
    :param cat_from: the cat who is having the feelings
    :param cat_to: the cat that the feelings are directed towards
    :param rel_value: the relationship value that you're looking for,
    options are: romantic, platonic, dislike, admiration, comfortable, jealousy, trust
    """
    if cat_to.ID in cat_from.relationships:
        relationship = cat_from.relationships[cat_to.ID]
    else:
        relationship = cat_from.create_one_relationship(cat_to)

    if rel_value == "romantic":
        return relationship.romantic_love
    elif rel_value == "platonic":
        return relationship.platonic_like
    elif rel_value == "dislike":
        return relationship.dislike
    elif rel_value == "admiration":
        return relationship.admiration
    elif rel_value == "comfortable":
        return relationship.comfortable
    elif rel_value == "jealousy":
        return relationship.jealousy
    elif rel_value == "trust":
        return relationship.trust
    else:
        raise KeyError(f"Could not account for relationship value: {rel_value}")

# TODO replace with global_rels.
def get_personality_compatibility(cat1, cat2):
    """Returns:
    True - if personalities have a positive compatibility
    False - if personalities have a negative compatibility
    None - if personalities have a neutral compatibility
    """
    personality1 = cat1.personality
    personality2 = cat2.personality

    # If neither cat has a personality trait, return neutral compatibility.
    if (personality1.trait is None) or (personality2.trait is None):
        return None

    if personality1.trait == personality2.trait:
        return True

    compatibility_score: int = 0
    for aspect in ['lawfulness', 'sociability', 'aggression', 'stability']:
        diff = abs(personality1.__getitem__(aspect) - personality2.__getitem__(aspect))
        if diff <= 4:
            compatibility_score += 1
        elif diff >= 6:
            compatibility_score -= 1
    if compatibility_score >= 2:
        return True
    elif compatibility_score <= 2:
        return False
    else:
        return None

# TODO replace with global_rels.
def get_cats_of_romantic_interest(cat):
    """Returns a list of cats, those cats are love interest of the given cat"""
    cats = []
    for inter_cat in cat.all_cats.values():
        if inter_cat.dead or inter_cat.outside or inter_cat.exiled:
            continue
        if inter_cat.ID == cat.ID:
            continue

        if inter_cat.ID not in cat.relationships:
            cat.create_one_relationship(inter_cat)
            if cat.ID not in inter_cat.relationships:
                inter_cat.create_one_relationship(cat)
            continue

        # Extra check to ensure they are potential mates
        if (
                inter_cat.is_potential_mate(cat, for_love_interest=True)
                and cat.relationships[inter_cat.ID].romantic_love > 0
        ):
            cats.append(inter_cat)
    return cats

# TODO replace with global_rels.
def get_amount_of_cats_with_relation_value_towards(cat, value, all_cats):
    """
    Looks how many cats have the certain value
    :param cat: cat in question
    :param value: value which has to be reached
    :param all_cats: list of cats which has to be checked
    """

    # collect all true or false if the value is reached for the cat or not
    # later count or sum can be used to get the amount of cats
    # this will be handled like this, because it is easier / shorter to check
    relation_dict = {
        "romantic_love": [],
        "platonic_like": [],
        "dislike": [],
        "admiration": [],
        "comfortable": [],
        "jealousy": [],
        "trust": [],
    }

    for inter_cat in all_cats:
        if cat.ID in inter_cat.relationships:
            relation = inter_cat.relationships[cat.ID]
        else:
            continue

        relation_dict["romantic_love"].append(relation.romantic_love >= value)
        relation_dict["platonic_like"].append(relation.platonic_like >= value)
        relation_dict["dislike"].append(relation.dislike >= value)
        relation_dict["admiration"].append(relation.admiration >= value)
        relation_dict["comfortable"].append(relation.comfortable >= value)
        relation_dict["jealousy"].append(relation.jealousy >= value)
        relation_dict["trust"].append(relation.trust >= value)

    return_dict = {
        "romantic_love": sum(relation_dict["romantic_love"]),
        "platonic_like": sum(relation_dict["platonic_like"]),
        "dislike": sum(relation_dict["dislike"]),
        "admiration": sum(relation_dict["admiration"]),
        "comfortable": sum(relation_dict["comfortable"]),
        "jealousy": sum(relation_dict["jealousy"]),
        "trust": sum(relation_dict["trust"]),
    }

    return return_dict

# TODO replace with global_rels.
def filter_relationship_type(
        group: list, filter_types: List[str], event_id: str = None, patrol_leader=None
):
    """
    filters for specific types of relationships between groups of cat objects, returns bool
    :param list[Cat] group: the group of cats to be tested (make sure they're in the correct order (i.e. if testing for
    parent/child, the cat being tested as parent must be index 0)
    :param list[str] filter_types: the relationship types to check for. possible types: "siblings", "mates",
    "mates_with_pl" (PATROL ONLY), "not_mates", "parent/child", "child/parent", "mentor/app", "app/mentor",
    (following tags check if value is over given int) "romantic_int", "platonic_int", "dislike_int", "comfortable_int",
    "jealousy_int", "trust_int"
    :param str event_id: if the event has an ID, include it here
    :param Cat patrol_leader: if you are testing a patrol, ensure you include the self.patrol_leader here
    """
    if not filter_types:
        return True

    # keeping this list here just for quick reference of what tags are handled here
    possible_rel_types = [
        "siblings",
        "mates",
        "mates_with_pl",
        "not_mates",
        "parent/child",
        "child/parent",
        "mentor/app",
        "app/mentor",
    ]

    possible_value_types = [
        "romantic",
        "platonic",
        "dislike",
        "comfortable",
        "jealousy",
        "trust",
        "admiration",
    ]

    if "siblings" in filter_types:
        test_cat = group[0]
        testing_cats = [cat for cat in group if cat.ID != test_cat.ID]

        siblings = [test_cat.is_sibling(inter_cat) for inter_cat in testing_cats]
        if not all(siblings):
            return False

    if "mates" in filter_types:
        # first test if more than one cat
        if len(group) == 1:
            return False

        # then if cats don't have the needed number of mates
        if not all(len(i.mate) >= (len(group) - 1) for i in group):
            return False

        # Now the expensive test.  We have to see if everone is mates with each other
        # Hopefully the cheaper tests mean this is only needed on events with a small number of cats
        for x in combinations(group, 2):
            if x[0].ID not in x[1].mate:
                return False

    # check if all cats are mates with p_l (they do not have to be mates with each other)
    if "mates_with_pl" in filter_types:
        # First test if there is more than one cat
        if len(group) == 1:
            return False

        # Check each cat to see if it is mates with the patrol leader
        for cat in group:
            if cat.ID == patrol_leader.ID:
                continue
            if cat.ID not in patrol_leader.mate:
                return False

    # Check if all cats are not mates
    if "not_mates" in filter_types:
        # opposite of mate check
        for x in combinations(group, 2):
            if x[0].ID in x[1].mate:
                return False

    # Check if the cats are in a parent/child relationship
    if "parent/child" in filter_types:
        if patrol_leader:
            if patrol_leader in group:
                group.remove(patrol_leader)
            group.insert(0, patrol_leader)
        # It should be exactly two cats for a "parent/child" event
        if len(group) != 2:
            return False
        # test for parentage
        if not group[0].is_parent(group[1]):
            return False

    if "child/parent" in filter_types:
        if patrol_leader:
            if patrol_leader in group:
                group.remove(patrol_leader)
            group.insert(0, patrol_leader)
        # It should be exactly two cats for a "parent/child" event
        if len(group) != 2:
            return False
        # test for parentage
        if not group[1].is_parent(group[0]):
            return False

    if "mentor/app" in filter_types:
        if patrol_leader:
            if patrol_leader in group:
                group.remove(patrol_leader)
            group.insert(0, patrol_leader)
        # It should be exactly two cats for a "parent/child" event
        if len(group) != 2:
            return False
        # test for parentage
        if not group[1].ID in group[0].apprentice:
            return False

    if "app/mentor" in filter_types:
        if patrol_leader:
            if patrol_leader in group:
                group.remove(patrol_leader)
            group.insert(0, patrol_leader)
        # It should be exactly two cats for a "parent/child" event
        if len(group) != 2:
            return False
        # test for parentage
        if not group[0].ID in group[1].apprentice:
            return False

    # Filtering relationship values
    break_loop = False
    for v_type in possible_value_types:
        # first get all tags for current value types
        tags = [constraint for constraint in filter_types if v_type in constraint]

        # If there is not a tag for the current value type, check next one
        if len(tags) == 0:
            continue

            # there should be only one value constraint for each value type
        elif len(tags) > 1:
            logger.error(
                f"Event {event_id} has multiple relationship constraints for the value {v_type}."
            )
            break_loop = True
            break

        # try to extract the value/threshold from the text
        try:
            threshold = int(tags[0].split("_")[1])
        except:
            logger.error(
                f"Event {event_id} with the relationship constraint for the value does not {v_type} follow the formatting guidelines."
            )
            break_loop = True
            break

        if threshold > 100:
            logger.error(
                f"Event {event_id} has a relationship constraint for the value {v_type}, which is higher than the max value of a relationship."
            )
            break_loop = True
            break

        if threshold <= 0:
            logger.error(
                f"Event {event_id} has a relationship constraint for the value {v_type}, which is lower than the min value of a relationship or 0."
            )
            break_loop = True
            break

        # each cat has to have relationships with this relationship value above the threshold
        fulfilled = True
        for inter_cat in group:
            rel_above_threshold = []
            group_ids = [cat.ID for cat in group]
            relevant_relationships = list(
                filter(
                    lambda rel: rel.cat_to.ID in group_ids
                                and rel.cat_to.ID != inter_cat.ID,
                    list(inter_cat.relationships.values()),
                )
            )

            # get the relationships depending on the current value type + threshold
            if v_type == "romantic":
                rel_above_threshold = [
                    i for i in relevant_relationships if i.romantic_love >= threshold
                ]
            elif v_type == "platonic":
                rel_above_threshold = [
                    i for i in relevant_relationships if i.platonic_like >= threshold
                ]
            elif v_type == "dislike":
                rel_above_threshold = [
                    i for i in relevant_relationships if i.dislike >= threshold
                ]
            elif v_type == "comfortable":
                rel_above_threshold = [
                    i for i in relevant_relationships if i.comfortable >= threshold
                ]
            elif v_type == "jealousy":
                rel_above_threshold = [
                    i for i in relevant_relationships if i.jealousy >= threshold
                ]
            elif v_type == "trust":
                rel_above_threshold = [
                    i for i in relevant_relationships if i.trust >= threshold
                ]
            elif v_type == "admiration":
                rel_above_threshold = [
                    i for i in relevant_relationships if i.admiration >= threshold
                ]

            # if the lengths are not equal, one cat has not the relationship value which is needed to another cat of
            # the event
            if len(rel_above_threshold) + 1 != len(group):
                fulfilled = False
                break

        if not fulfilled:
            break_loop = True
            break

    # if break is used in the loop, the condition are not fulfilled
    # and this event should not be added to the filtered list
    if break_loop:
        return False

    return True

# TODO replace with global_rels.
def gather_cat_objects(
        Cat, abbr_list: List[str], event, stat_cat=None, extra_cat=None
) -> list:
    """
    gathers cat objects from list of abbreviations used within an event format block
    :param Cat Cat: Cat class
    :param list[str] abbr_list: The list of abbreviations, supports "m_c", "r_c", "p_l", "s_c", "app1" through "app6",
    "clan", "some_clan", "patrol", "multi", "n_c{index}"
    :param event: the controlling class of the event (e.g. Patrol, HandleShortEvents), default None
    :param Cat stat_cat: if passing the Patrol class, must include stat_cat separately
    :param Cat extra_cat: if not passing an event class, include the single affected cat object here. If you are not
    passing a full event class, then be aware that you can only include "m_c" as a cat abbreviation in your rel block.
    The other cat abbreviations will not work.
    :return: list of cat objects
    """
    out_set = set()

    for abbr in abbr_list:
        if abbr == "m_c":
            if extra_cat:
                out_set.add(extra_cat)
            else:
                out_set.add(event.main_cat)
        elif abbr == "r_c":
            out_set.add(event.random_cat)
        elif abbr == "p_l":
            out_set.add(event.patrol_leader)
        elif abbr == "s_c":
            out_set.add(stat_cat)
        elif abbr == "app1" and len(event.patrol_apprentices) >= 1:
            out_set.add(event.patrol_apprentices[0])
        elif abbr == "app2" and len(event.patrol_apprentices) >= 2:
            out_set.add(event.patrol_apprentices[1])
        elif abbr == "app3" and len(event.patrol_apprentices) >= 3:
            out_set.add(event.patrol_apprentices[2])
        elif abbr == "app4" and len(event.patrol_apprentices) >= 4:
            out_set.add(event.patrol_apprentices[3])
        elif abbr == "app5" and len(event.patrol_apprentices) >= 5:
            out_set.add(event.patrol_apprentices[4])
        elif abbr == "app6" and len(event.patrol_apprentices) >= 6:
            out_set.add(event.patrol_apprentices[5])
        elif abbr == "clan":
            out_set.update(
                [x for x in Cat.all_cats_list if not (x.dead or x.outside or x.exiled)]
            )
        elif abbr == "some_clan":  # 1 / 8 of clan cats are affected
            clan_cats = [
                x for x in Cat.all_cats_list if not (x.dead or x.outside or x.exiled)
            ]
            out_set.update(
                sample(clan_cats, randint(1, max(1, round(len(clan_cats) / 8))))
            )
        elif abbr == "patrol":
            out_set.update(event.patrol_cats)
        elif abbr == "multi":
            cat_num = randint(1, max(1, len(event.patrol_cats) - 1))
            out_set.update(sample(event.patrol_cats, cat_num))
        elif regex.match(r"n_c:[0-9]+", abbr):
            index = regex.match(r"n_c:([0-9]+)", abbr).group(1)
            index = int(index)
            if index < len(event.new_cats):
                out_set.update(event.new_cats[index])
        else:
            logger.warning(f"Unsupported abbreviation {abbr}")

    return list(out_set)

# TODO replace with global_rels.
def unpack_rel_block(
        Cat, relationship_effects: List[dict], event=None, stat_cat=None, extra_cat=None
):
    """
    Unpacks the info from the relationship effect block used in patrol and moon events, then adjusts rel values
    accordingly.

    :param Cat Cat: Cat class
    :param list[dict] relationship_effects: the relationship effect block
    :param event: the controlling class of the event (e.g. Patrol, HandleShortEvents), default None
    :param Cat stat_cat: if passing the Patrol class, must include stat_cat separately
    :param Cat extra_cat: if not passing an event class, include the single affected cat object here. If you are not passing a full event class, then be aware that you can only include "m_c" as a cat abbreviation in your rel block.  The other cat abbreviations will not work.
    """
    possible_values = (
        "romantic",
        "platonic",
        "dislike",
        "comfort",
        "jealous",
        "trust",
        "respect",
    )

    for block in relationship_effects:
        cats_from = block.get("cats_from", [])
        cats_to = block.get("cats_to", [])
        amount = block.get("amount")
        values = [x for x in block.get("values", ()) if x in possible_values]

        # Gather actual cat objects:
        cats_from_ob = gather_cat_objects(Cat, cats_from, event, stat_cat, extra_cat)
        cats_to_ob = gather_cat_objects(Cat, cats_to, event, stat_cat, extra_cat)

        # Remove any "None" that might have snuck in
        if None in cats_from_ob:
            cats_from_ob.remove(None)
        if None in cats_to_ob:
            cats_to_ob.remove(None)

        # Check to see if value block
        if not (cats_to_ob and cats_from_ob and values and isinstance(amount, int)):
            logger.warning(f"Relationship block incorrectly formatted: {block}")
            continue

        positive = False

        # grabbing values
        romantic_love = 0
        platonic_like = 0
        dislike = 0
        comfortable = 0
        jealousy = 0
        admiration = 0
        trust = 0
        if "romantic" in values:
            romantic_love = amount
            if amount > 0:
                positive = True
        if "platonic" in values:
            platonic_like = amount
            if amount > 0:
                positive = True
        if "dislike" in values:
            dislike = amount
            if amount < 0:
                positive = True
        if "comfort" in values:
            comfortable = amount
            if amount > 0:
                positive = True
        if "jealous" in values:
            jealousy = amount
            if amount < 0:
                positive = True
        if "trust" in values:
            trust = amount
            if amount > 0:
                positive = True
        if "respect" in values:
            admiration = amount
            if amount > 0:
                positive = True

        if positive:
            effect = i18n.t("relationships.positive_postscript")
        else:
            effect = i18n.t("relationships.negative_postscript")

        # Get log
        log1 = None
        log2 = None
        if block.get("log"):
            log = block.get("log")
            if isinstance(log, str):
                log1 = log
            elif isinstance(log, list):
                if len(log) >= 2:
                    log1 = log[0]
                    log2 = log[1]
                elif len(log) == 1:
                    log1 = log[0]
            else:
                logger.warning(f"something is wrong with relationship log: {log}")

        if not log1:
            if hasattr(event, "text"):
                try:
                    log1 = event.text + effect
                except AttributeError:
                    logger.warning(
                        f"Event changed relationships but did not create a relationship log"
                    )
            else:
                log1 = i18n.t("defaults.relationship_log") + effect
        if not log2:
            if hasattr(event, "text"):
                try:
                    log2 = event.text + effect
                except AttributeError:
                    logger.warning(
                        f"Event changed relationships but did not create a relationship log"
                    )
            else:
                log2 = i18n.t("defaults.relationship_log") + effect

        change_relationship_values(
            cats_to_ob,
            cats_from_ob,
            romantic_love,
            platonic_like,
            dislike,
            admiration,
            comfortable,
            jealousy,
            trust,
            log=log1,
        )

        if block.get("mutual"):
            change_relationship_values(
                cats_from_ob,
                cats_to_ob,
                romantic_love,
                platonic_like,
                dislike,
                admiration,
                comfortable,
                jealousy,
                trust,
                log=log2,
            )

# TODO replace with global_rels.
def change_relationship_values(
        cats_to: list,
        cats_from: list,
        romantic_love: int = 0,
        platonic_like: int = 0,
        dislike: int = 0,
        admiration: int = 0,
        comfortable: int = 0,
        jealousy: int = 0,
        trust: int = 0,
        auto_romance: bool = False,
        log: str = None,
):
    """
    changes relationship values according to the parameters.

    :param list[Cat] cats_from: list of cat objects whose rel values will be affected
    (e.g. cat_from loses trust in cat_to)
    :param list[Cat] cats_to: list of cats objects who are the target of that rel value
    (e.g. cat_from loses trust in cat_to)
    :param int romantic_love: amount to change romantic, default 0
    :param int platonic_like: amount to change platonic, default 0
    :param int dislike: amount to change dislike, default 0
    :param int admiration: amount to change admiration (respect), default 0
    :param int comfortable: amount to change comfort, default 0
    :param int jealousy: amount to change jealousy, default 0
    :param int trust: amount to change trust, default 0
    :param bool auto_romance: if the cat_from already has romantic value with cat_to, then the platonic_like param value
    will also be applied to romantic, default False
    :param str log: the string to append to the relationship log of cats involved
    """

    # This is just for test prints - DON'T DELETE - you can use this to test if relationships are changing
    """changed = False
    if romantic_love == 0 and platonic_like == 0 and dislike == 0 and admiration == 0 and \
            comfortable == 0 and jealousy == 0 and trust == 0:
        changed = False
    else:
        changed = True"""

    # pick out the correct cats
    for single_cat_from in cats_from:
        for single_cat_to in cats_to:
            # make sure we aren't trying to change a cat's relationship with themself
            if single_cat_from == single_cat_to:
                continue

            # if the cats don't know each other, start a new relationship
            if single_cat_to.ID not in single_cat_from.relationships:
                single_cat_from.create_one_relationship(single_cat_to)

            rel = single_cat_from.relationships[single_cat_to.ID]

            # here we just double-check that the cats are allowed to be romantic with each other
            if (
                    single_cat_from.is_potential_mate(single_cat_to, for_love_interest=True)
                    or single_cat_to.ID in single_cat_from.mate
            ):
                # if cat already has romantic feelings then automatically increase romantic feelings
                # when platonic feelings would increase
                if rel.romantic_love > 0 and auto_romance:
                    romantic_love = platonic_like

                # now gain the romance
                rel.romantic_love += romantic_love

            # gain other rel values
            rel.platonic_like += platonic_like
            rel.dislike += dislike
            rel.admiration += admiration
            rel.comfortable += comfortable
            rel.jealousy += jealousy
            rel.trust += trust

            # for testing purposes - DON'T DELETE - you can use this to test if relationships are changing
            """
            print(str(single_cat_from.name) + " gained relationship with " + str(rel.cat_to.name) + ": " +
                  "Romantic: " + str(romantic_love) +
                  " /Platonic: " + str(platonic_like) +
                  " /Dislike: " + str(dislike) +
                  " /Respect: " + str(admiration) +
                  " /Comfort: " + str(comfortable) +
                  " /Jealousy: " + str(jealousy) +
                  " /Trust: " + str(trust)) if changed else print("No relationship change")"""

            if log and isinstance(log, str):
                log_text = log + i18n.t(
                    "relationships.age_postscript",
                    name=str(single_cat_to.name),
                    count=single_cat_to.moons,
                )
                if log_text not in rel.log:
                    rel.log.append(log_text)


# ---------------------------------------------------------------------------- #
#                               Text Adjust                                    #
# ---------------------------------------------------------------------------- #


def get_leader_life_notice() -> str:
    """
    Returns a string specifying how many lives the leader has left or notifying of the leader's full death
    """
    if game.clan_obj.instructor.df:
        return i18n.t("cat.history.leader_lives_left_df", count=game.clan_obj.leader_lives)
    return i18n.t("cat.history.leader_lives_left_sc", count=game.clan_obj.leader_lives)


# TODO move these values to goame_config.yaml
def get_other_clan_relation(relation):
    """
    converts int value into string relation and returns string: "hostile", "neutral", or "ally"
    :param relation: the other_clan.relations value
    """

    if int(relation) >= 17:
        return "ally"
    elif 7 < int(relation) < 17:
        return "neutral"
    elif int(relation) <= 7:
        return "hostile"


def pronoun_repl(m, cat_pronouns_dict, raise_exception=False):
    """Helper function for add_pronouns. If raise_exception is
    False, any error in pronoun formatting will not raise an
    exception, and will use a simple replacement "error" """

    # Add protection about the "insert" sometimes used
    if m.group(0) == "{insert}":
        return m.group(0)

    inner_details = m.group(1).split("/")
    out = None

    try:
        if inner_details[1].upper() == "PLURAL":
            inner_details.pop(1)  # remove plural tag so it can be processed as normal
            catlist = []
            for cat in inner_details[1].split("+"):
                try:
                    catlist.append(cat_pronouns_dict[cat][1])
                except KeyError:
                    logger.warning(f"Missing pronouns for {cat}")
                    continue
            d = determine_plural_pronouns(catlist)
        else:
            try:
                d = cat_pronouns_dict[inner_details[1]][1]
            except KeyError:
                if inner_details[0].upper() == "ADJ":
                    # find the default - this is a semi-expected behaviour for the adj tag as it may be called when
                    # there is no relevant cat
                    return inner_details[localization.get_default_adj()]
                else:
                    logger.warning(
                        f"Could not get pronouns for {inner_details[1]}. Using default."
                    )
                    logger.warning(
                        f"Could not get pronouns for {inner_details[1]}. Using default."
                    )
                    d = choice(localization.get_new_pronouns("default"))

        if inner_details[0].upper() == "PRONOUN":
            out = d[inner_details[2]]
        elif inner_details[0].upper() == "VERB":
            out = inner_details[d["conju"] + 1]
        elif inner_details[0].upper() == "ADJ":
            out = inner_details[(d["gender"] + 2) if "gender" in d else 2]

        if out is not None:
            if inner_details[-1] == "CAP":
                out = out.capitalize()
            return out

        if raise_exception:
            raise KeyError(
                f"Pronoun tag: {m.group(1)} is not properly indicated as a PRONOUN or VERB tag."
            )

        logger.warning(f"Failed to find pronoun: {m.group(1)}")
        return "error1"
    except (KeyError, IndexError) as err:
        if raise_exception:
            raise

        logger.exception(f"Failed to find pronoun: {m.group(1)}", err)
        return "error2"


def name_repl(m, cat_dict):
    """Name replacement"""
    return cat_dict[m.group(0)][0]


def process_text(text, cat_dict, raise_exception=False):
    """Add the correct name and pronouns into a string."""
    adjust_text = regex.sub(
        r"(?<!%)\{(.*?)}", lambda x: pronoun_repl(x, cat_dict, raise_exception), text
    )

    name_patterns = [r"(?<!\{)" + regex.escape(l) + r"(?!\})" for l in cat_dict]
    adjust_text = regex.sub(
        "|".join(name_patterns), lambda x: name_repl(x, cat_dict), adjust_text
    )
    return adjust_text


def adjust_list_text(list_of_items: List) -> str:
    """
    returns the list in correct grammar format (i.e. item1, item2, item3 and item4)
    this works with any number of items
    :param list_of_items: the list of items you want converted
    :return: the new string
    """

    if not isinstance(list_of_items, list):
        logger.warning("non-list object was passed to adjust_list_text")
        list_of_items = list(list_of_items)

    if len(list_of_items) == 0:
        item1 = ""
        item2 = ""
    elif len(list_of_items) == 1:
        item1 = list_of_items[0]
        item2 = ""
    elif len(list_of_items) == 2:
        item1 = list_of_items[0]
        item2 = list_of_items[1]
    else:
        item1 = ", ".join(list_of_items[:-1])
        if get_lang_config().get("oxford_comma"):
            item1 += ","
        item2 = list_of_items[-1]

    return i18n.t("utility.items", count=len(list_of_items), item1=item1, item2=item2)


def adjust_prey_abbr(patrol_text):
    """
    checks for prey abbreviations and returns adjusted text
    """
    global PREY_LISTS
    if langs["prey"] != i18n.config.get("locale"):
        langs["prey"] = i18n.config.get("locale")
        PREY_LISTS = load_lang_resource("patrols/prey_text_replacements.json")

    for abbr in PREY_LISTS["abbreviations"]:
        if abbr in patrol_text:
            chosen_list = PREY_LISTS["abbreviations"].get(abbr)
            chosen_list = PREY_LISTS[chosen_list]
            prey = choice(chosen_list)
            patrol_text = patrol_text.replace(abbr, prey)

    return patrol_text


def get_special_snippet_list(
        chosen_list, amount, sense_groups=None, return_string=True
):
    """
    function to grab items from various lists in snippet_collections.json
    list options are:
    -prophecy_list - sense_groups = sight, sound, smell, emotional, touch
    -omen_list - sense_groups = sight, sound, smell, emotional, touch
    -clair_list  - sense_groups = sound, smell, emotional, touch, taste
    -dream_list (this list doesn't have sense_groups)
    -story_list (this list doesn't have sense_groups)
    :param chosen_list: pick which list you want to grab from
    :param amount: the amount of items you want the returned list to contain
    :param sense_groups: list which senses you want the snippets to correspond with:
     "touch", "sight", "emotional", "sound", "smell" are the options. Default is None, if left as this then all senses
     will be included (if the list doesn't have sense categories, then leave as None)
    :param return_string: if True then the function will format the snippet list with appropriate commas and 'ands'.
    This will work with any number of items. If set to True, then the function will return a string instead of a list.
    (i.e. ["hate", "fear", "dread"] becomes "hate, fear, and dread") - Default is True
    :return: a list of the chosen items from chosen_list or a formatted string if format is True
    """
    biome = game.clan_obj.biome.casefold()
    global SNIPPETS
    if langs["snippet"] != i18n.config.get("locale"):
        langs["snippet"] = i18n.config.get("locale")
        SNIPPETS = load_lang_resource("snippet_collections.json")

    # these lists don't get sense specific snippets, so is handled first
    if chosen_list in ["dream_list", "story_list"]:
        if (
                chosen_list == "story_list"
        ):  # story list has some biome specific things to collect
            snippets = SNIPPETS[chosen_list]["general"]
            snippets.extend(SNIPPETS[chosen_list][biome])
        elif (
                chosen_list == "clair_list"
        ):  # the clair list also pulls from the dream list
            snippets = SNIPPETS[chosen_list]
            snippets.extend(SNIPPETS["dream_list"])
        else:  # the dream list just gets the one
            snippets = SNIPPETS[chosen_list]

    else:
        # if no sense groups were specified, use all of them
        if not sense_groups:
            if chosen_list == "clair_list":
                sense_groups = ["taste", "sound", "smell", "emotional", "touch"]
            else:
                sense_groups = ["sight", "sound", "smell", "emotional", "touch"]

        # find the correct lists and compile them
        snippets = []
        for sense in sense_groups:
            snippet_group = SNIPPETS[chosen_list][sense]
            snippets.extend(snippet_group["general"])
            snippets.extend(snippet_group[biome])

    # now choose a unique snippet from each snip list
    unique_snippets = []
    for snip_list in snippets:
        unique_snippets.append(choice(snip_list))

    # pick out our final snippets
    final_snippets = sample(unique_snippets, k=amount)

    if return_string:
        text = adjust_list_text(final_snippets)
        return text
    else:
        return final_snippets


def find_special_list_types(text: str):
    """
    purely to identify which senses are being called for by a snippet abbreviation
    returns adjusted text, sense list, list type, and cat_tag
    """
    senses = []
    list_text = None
    list_type = None
    words = text.split(" ")
    for bit in words:
        if "_list" in bit:
            list_text = bit
            # just getting rid of pesky punctuation
            list_text = list_text.replace(".", "")
            list_text = list_text.replace(",", "")
            break

    if not list_text:
        return text, None, None, None

    parts_of_tag = list_text.split("/")

    try:
        cat_tag = parts_of_tag[1]
    except IndexError:
        cat_tag = None

    if "omen_list" in list_text:
        list_type = "omen_list"
    elif "prophecy_list" in list_text:
        list_type = "prophecy_list"
    elif "dream_list" in list_text:
        list_type = "dream_list"
    elif "clair_list" in list_text:
        list_type = "clair_list"
    elif "story_list" in list_text:
        list_type = "story_list"
    else:
        logger.error("WARNING: no list type found for %s", list_text)
        return text, None, None, None

    if "_sight" in list_text:
        senses.append("sight")
    if "_sound" in list_text:
        senses.append("sound")
    if "_smell" in list_text:
        senses.append("smell")
    if "_emotional" in list_text:
        senses.append("emotional")
    if "_touch" in list_text:
        senses.append("touch")
    if "_taste" in list_text:
        senses.append("taste")

    text = text.replace(list_text, list_type)

    return text, senses, list_type, cat_tag


def history_text_adjust(text, other_clan_name, clan, other_cat_rc=None):
    """
    we want to handle history text on its own because it needs to preserve the pronoun tags and cat abbreviations.
    this is so that future pronoun changes or name changes will continue to be reflected in history
    """
    vowels = ["A", "E", "I", "O", "U"]

    if "o_c_n" in text:
        pos = 0
        for x in range(text.count("o_c_n")):
            if "o_c_n" in text:
                for y in vowels:
                    if str(other_clan_name).startswith(y):
                        modify = text.split()
                        if "o_c_n" in modify:
                            pos = modify.index("o_c_n")
                        if "o_c_n's" in modify:
                            pos = modify.index("o_c_n's")
                        if "o_c_n." in modify:
                            pos = modify.index("o_c_n.")
                        if modify[pos - 1] == "a":
                            modify.remove("a")
                            modify.insert(pos - 1, "an")
                        text = " ".join(modify)
                        break

        text = text.replace("o_c_n", str(other_clan_name))

    if "c_n" in text:
        text = text.replace("c_n", clan.name)
    if "r_c" in text and other_cat_rc:
        text = selective_replace(text, "r_c", str(other_cat_rc.name))
    return text


def selective_replace(text, pattern, replacement):
    i = 0
    while i < len(text):
        index = text.find(pattern, i)
        if index == -1:
            break
        start_brace = text.rfind("{", 0, index)
        end_brace = text.find("}", index)
        if start_brace != -1 and end_brace != -1 and start_brace < index < end_brace:
            i = index + len(pattern)
        else:
            text = text[:index] + replacement + text[index + len(pattern):]
            i = index + len(replacement)

    return text


def ongoing_event_text_adjust(Cat, text, clan=None, other_clan_name=None):
    """
    This function is for adjusting the text of ongoing events
    :param Cat: the cat class
    :param text: the text to be adjusted
    :param clan: the name of the clan
    :param other_clan_name: the other Clan's name if another Clan is involved
    """
    cat_dict = {}
    if "lead_name" in text:
        kitty = Cat.fetch_cat(game.clan_obj.leader)
        cat_dict["lead_name"] = (str(kitty.name), choice(kitty.pronouns))
    if "dep_name" in text:
        kitty = Cat.fetch_cat(game.clan_obj.deputy)
        cat_dict["dep_name"] = (str(kitty.name), choice(kitty.pronouns))
    if "med_name" in text:
        kitty = choice(get_alive_status_cats(Cat, [Rank.Healer], working=True))
        cat_dict["med_name"] = (str(kitty.name), choice(kitty.pronouns))

    if cat_dict:
        text = process_text(text, cat_dict)

    if other_clan_name:
        text = text.replace("o_c_n", other_clan_name)
    if clan:
        clan_name = str(clan.name)
    else:
        if game.clan_obj is None:
            clan_name = game.switches["clan_list"][0]
        else:
            clan_name = str(game.clan_obj.name)

    text = text.replace("c_n", clan_name + "Clan")

    return text


def event_text_adjust(
        Cat: Type["Cat"], # TODO move this method to another module so you don't need to import this class
        text,
        *,
        patrol_leader=None,
        main_cat=None,
        random_cat=None,
        stat_cat=None,
        victim_cat=None,
        patrol_cats: list = None,
        patrol_apprentices: list = None,
        new_cats: list = None,
        multi_cats: list = None,
        clan=None,
        other_clan=None,
        chosen_herb: str = None,
):
    """
    handles finding abbreviations in the text and replacing them appropriately, returns the adjusted text
    :param Cat Cat: always pass the Cat class
    :param str text: the text being adjusted
    :param Cat patrol_leader: Cat object for patrol_leader (p_l), if present
    :param Cat main_cat: Cat object for main_cat (m_c), if present
    :param Cat random_cat: Cat object for random_cat (r_c), if present
    :param Cat stat_cat: Cat object for stat_cat (s_c), if present
    :param Cat victim_cat: Cat object for victim_cat (mur_c), if present
    :param list[Cat] patrol_cats: List of Cat objects for cats in patrol, if present
    :param list[Cat] patrol_apprentices: List of Cat objects for patrol_apprentices (app#), if present
    :param list[Cat] new_cats: List of Cat objects for new_cats (n_c:index), if present
    :param list[Cat] multi_cats: List of Cat objects for multi_cat (multi_cat), if present
    :param Clan clan: pass game.clan
    :param OtherClan other_clan: OtherClan object for other_clan (o_c_n), if present
    :param str chosen_herb: string of chosen_herb (chosen_herb), if present
    """
    vowels = ["A", "E", "I", "O", "U"]

    if not text:
        text = "This should not appear, report as a bug please! Tried to adjust the text, but no text was provided."
        print("WARNING: Tried to adjust text, but no text was provided.")

    # this check is really just here to catch odd bug edge-cases from old saves, specifically in death history
    # otherwise we should really *never* have lists being passed as the text
    if isinstance(text, list):
        text = text[0]

    replace_dict = {}

    # special lists - this needs to happen first for pronoun tag reasons
    text, senses, list_type, cat_tag = find_special_list_types(text)
    if list_type:
        sign_list = get_special_snippet_list(
            list_type, amount=randint(1, 3), sense_groups=senses
        )
        text = text.replace(list_type, str(sign_list))
        if cat_tag:
            text = text.replace("cat_tag", cat_tag)

    # main_cat
    if "m_c" in text:
        if main_cat:
            replace_dict["m_c"] = (str(main_cat.name), choice(main_cat.pronouns))

    # patrol_lead
    if "p_l" in text:
        if patrol_leader:
            replace_dict["p_l"] = (
                str(patrol_leader.name),
                choice(patrol_leader.pronouns),
            )

    # random_cat
    if "r_c" in text:
        if random_cat:
            replace_dict["r_c"] = (str(random_cat.name), get_pronouns(random_cat))

    # stat cat
    if "s_c" in text:
        if stat_cat:
            replace_dict["s_c"] = (str(stat_cat.name), get_pronouns(stat_cat))

    # other_cats
    if patrol_cats:
        other_cats = [
            i
            for i in patrol_cats
            if i not in [patrol_leader, random_cat, patrol_apprentices]
        ]
        other_cat_abbr = ["o_c1", "o_c2", "o_c3", "o_c4"]
        for i, abbr in enumerate(other_cat_abbr):
            if abbr not in text:
                continue
            if len(other_cats) > i:
                replace_dict[abbr] = (
                    str(other_cats[i].name),
                    choice(other_cats[i].pronouns),
                )

    # patrol_apprentices
    app_abbr = ["app1", "app2", "app3", "app4", "app5", "app6"]
    for i, abbr in enumerate(app_abbr):
        if abbr not in text:
            continue
        if len(patrol_apprentices) > i:
            replace_dict[abbr] = (
                str(patrol_apprentices[i].name),
                choice(patrol_apprentices[i].pronouns),
            )

    # new_cats (include pre version)
    if "n_c" in text:
        for i, cat_list in enumerate(new_cats):
            if len(new_cats) > 1:
                pronoun = localization.get_new_pronouns("default plural")[0]
            else:
                pronoun = choice(cat_list[0].pronouns)

            replace_dict[f"n_c:{i}"] = (str(cat_list[0].name), pronoun)
            replace_dict[f"n_c_pre:{i}"] = (str(cat_list[0].name.prefix), pronoun)

    # mur_c (murdered cat for reveals)
    if "mur_c" in text:
        replace_dict["mur_c"] = (str(victim_cat.name), get_pronouns(victim_cat))

    # lead_name
    if "lead_name" in text:
        leader = Cat.fetch_cat(game.clan_obj.leader)
        replace_dict["lead_name"] = (str(leader.name), choice(leader.pronouns))

    # dep_name
    if "dep_name" in text:
        deputy = Cat.fetch_cat(game.clan_obj.deputy)
        replace_dict["dep_name"] = (str(deputy.name), choice(deputy.pronouns))

    # med_name
    if "med_name" in text:
        med = choice(get_alive_status_cats(Cat, [Rank.Healer], working=True))
        replace_dict["med_name"] = (str(med.name), choice(med.pronouns))

    # assign all names and pronouns
    if replace_dict:
        text = process_text(text, replace_dict)

    # multi_cat
    if "multi_cat" in text:
        name_list = []
        for _cat in multi_cats:
            name_list.append(str(_cat.name))
        list_text = adjust_list_text(name_list)
        text = text.replace("multi_cat", list_text)

    # other_clan_name
    if "o_c_n" in text:
        other_clan_name = other_clan.name
        pos = 0
        for x in range(text.count("o_c_n")):
            if "o_c_n" in text:
                for y in vowels:
                    if str(other_clan_name).startswith(y):
                        modify = text.split()
                        if "o_c_n" in modify:
                            pos = modify.index("o_c_n")
                        if "o_c_n's" in modify:
                            pos = modify.index("o_c_n's")
                        if "o_c_n." in modify:
                            pos = modify.index("o_c_n.")
                        if modify[pos - 1] == "a":
                            modify.remove("a")
                            modify.insert(pos - 1, "an")
                        text = " ".join(modify)
                        break

        text = text.replace("o_c_n", str(other_clan_name) + "Clan")

    # clan_name
    if "c_n" in text:
        try:
            clan_name = clan.name
        except AttributeError:
            clan_name = game.switches["clan_list"][0]

        pos = 0
        for x in range(text.count("c_n")):
            if "c_n" in text:
                for y in vowels:
                    if str(clan_name).startswith(y):
                        modify = text.split()
                        if "c_n" in modify:
                            pos = modify.index("c_n")
                        if "c_n's" in modify:
                            pos = modify.index("c_n's")
                        if "c_n." in modify:
                            pos = modify.index("c_n.")
                        if modify[pos - 1] == "a":
                            modify.remove("a")
                            modify.insert(pos - 1, "an")
                        text = " ".join(modify)
                        break

        text = text.replace("c_n", str(clan_name) + "Clan")

    # prey lists
    text = adjust_prey_abbr(text)

    # acc_plural (only works for main_cat's acc)
    if "acc_plural" in text:
        text = text.replace(
            "acc_plural", i18n.t(f"cat.accessories.{main_cat.pelt.accessory[-1]}", count=2)
        )

    # acc_singular (only works for main_cat's acc)
    if "acc_singular" in text:
        text = text.replace(
            "acc_singular",
            i18n.t(f"cat.accessories.{main_cat.pelt.accessory[-1]}", count=1),
        )

    if "given_herb" in text:
        text = text.replace(
            "given_herb", i18n.t(f"conditions.herbs.{chosen_herb}", count=2)
        )

    return text


def leader_ceremony_text_adjust(
        Cat,
        text,
        leader,
        life_giver=None,
        virtue=None,
        extra_lives=None,
):
    """
    used to adjust the text for leader ceremonies
    """
    replace_dict = {
        "m_c_star": (str(leader.name.prefix + "star"), choice(leader.pronouns)),
        "m_c": (str(leader.name.prefix + leader.name.suffix), choice(leader.pronouns)),
    }

    if life_giver:
        replace_dict["r_c"] = (
            str(Cat.fetch_cat(life_giver).name),
            choice(Cat.fetch_cat(life_giver).pronouns),
        )

    text = process_text(text, replace_dict)

    if virtue:
        virtue = process_text(virtue, replace_dict)
        text = text.replace("[virtue]", virtue)

    if extra_lives:
        text = text.replace("[life_num]", str(extra_lives))

    text = text.replace("c_n", str(game.clan_obj.name) + "Clan")

    return text


def ceremony_text_adjust(
        Cat,
        text,
        cat,
        old_name=None,
        dead_mentor=None,
        mentor=None,
        previous_alive_mentor=None,
        random_honor=None,
        living_parents=(),
        dead_parents=(),
):
    clanname = str(game.clan_obj.name + "Clan")

    random_honor = random_honor
    random_living_parent = None
    random_dead_parent = None

    adjust_text = text

    cat_dict = {
        "m_c": (
            (str(cat.name), choice(cat.pronouns)) if cat else ("cat_placeholder", None)
        ),
        "(mentor)": (
            (str(mentor.name), choice(mentor.pronouns))
            if mentor
            else ("mentor_placeholder", None)
        ),
        "(deadmentor)": (
            (str(dead_mentor.name), get_pronouns(dead_mentor))
            if dead_mentor
            else ("dead_mentor_name", None)
        ),
        "(previous_mentor)": (
            (str(previous_alive_mentor.name), choice(previous_alive_mentor.pronouns))
            if previous_alive_mentor
            else ("previous_mentor_name", None)
        ),
        "l_n": (
            (str(game.clan_obj.leader.name), choice(game.clan_obj.leader.pronouns))
            if game.clan_obj.leader
            else ("leader_name", None)
        ),
        "c_n": (clanname, None),
    }

    if old_name:
        cat_dict["(old_name)"] = (old_name, None)

    if random_honor:
        cat_dict["r_h"] = (random_honor, None)

    if "p1" in adjust_text and "p2" in adjust_text and len(living_parents) >= 2:
        cat_dict["p1"] = (
            str(living_parents[0].name),
            choice(living_parents[0].pronouns),
        )
        cat_dict["p2"] = (
            str(living_parents[1].name),
            choice(living_parents[1].pronouns),
        )
    elif living_parents:
        random_living_parent = choice(living_parents)
        cat_dict["p1"] = (
            str(random_living_parent.name),
            choice(random_living_parent.pronouns),
        )
        cat_dict["p2"] = (
            str(random_living_parent.name),
            choice(random_living_parent.pronouns),
        )

    if (
            "dead_par1" in adjust_text
            and "dead_par2" in adjust_text
            and len(dead_parents) >= 2
    ):
        cat_dict["dead_par1"] = (
            str(dead_parents[0].name),
            get_pronouns(dead_parents[0]),
        )
        cat_dict["dead_par2"] = (
            str(dead_parents[1].name),
            get_pronouns(dead_parents[1]),
        )
    elif dead_parents:
        random_dead_parent = choice(dead_parents)
        cat_dict["dead_par1"] = (
            str(random_dead_parent.name),
            get_pronouns(random_dead_parent),
        )
        cat_dict["dead_par2"] = (
            str(random_dead_parent.name),
            get_pronouns(random_dead_parent),
        )

    adjust_text = process_text(adjust_text, cat_dict)

    return adjust_text, random_living_parent, random_dead_parent


def get_pronouns(Cat: "Cat"):
    """Get a cat's pronoun even if the cat has faded to prevent crashes (use gender-neutral pronouns when the cat has faded)"""
    if Cat.pronouns == {}:
        return localization.get_new_pronouns("default")
    else:
        return choice(Cat.pronouns)


def shorten_text_to_fit(
        name, length_limit, font_size=None, font_type="resources/fonts/NotoSans-Medium.ttf"
):
    length_limit = length_limit * scripts.game_structure.screen_settings.screen_scale
    if font_size is None:
        font_size = 15
    font_size = floor(font_size * scripts.game_structure.screen_settings.screen_scale)

    if font_type == "clangen":
        font_type = "resources/fonts/clangen.ttf"
    # Create the font object
    font = pygame.font.Font(font_type, font_size)

    # Add dynamic name lengths by checking the actual width of the text
    total_width = 0
    short_name = ""
    ellipsis_width = font.size("...")[0]
    for index, character in enumerate(name):
        char_width = font.size(character)[0]

        # Check if the current character is the last one and its width is less than or equal to ellipsis_width
        if index == len(name) - 1 and char_width <= ellipsis_width:
            short_name += character
        else:
            total_width += char_width
            if total_width + ellipsis_width > length_limit:
                break
            short_name += character

    # If the name was truncated, add "..."
    if len(short_name) < len(name):
        short_name += "..."

    return short_name


# ---------------------------------------------------------------------------- #
#                                    Sprites                                   #
# ---------------------------------------------------------------------------- #


def ui_scale(rect: pygame.Rect):
    """
    Scales a pygame.Rect appropriately for the UI scaling currently in use.
    :param rect: a pygame.Rect
    :return: the same pygame.Rect, scaled for the current UI.
    """
    # offset can be negative to allow for correct anchoring
    rect[0] = floor(rect[0] * scripts.game_structure.screen_settings.screen_scale)
    rect[1] = floor(rect[1] * scripts.game_structure.screen_settings.screen_scale)
    # if the dimensions are negative, it's dynamically scaled, ignore
    rect[2] = (
        floor(rect[2] * scripts.game_structure.screen_settings.screen_scale)
        if rect[2] > 0
        else rect[2]
    )
    rect[3] = (
        floor(rect[3] * scripts.game_structure.screen_settings.screen_scale)
        if rect[3] > 0
        else rect[3]
    )

    return rect


def ui_scale_dimensions(dim: Tuple[int, int]):
    """
    Use to scale the dimensions of an item - WILL IGNORE NEGATIVE VALUES
    :param dim: The dimensions to scale
    :return: The scaled dimensions
    """
    return (
        floor(dim[0] * scripts.game_structure.screen_settings.screen_scale)
        if dim[0] > 0
        else dim[0],
        floor(dim[1] * scripts.game_structure.screen_settings.screen_scale)
        if dim[1] > 0
        else dim[1],
    )


def ui_scale_offset(coords: Tuple[int, int]):
    """
    Use to scale the offset of an item (i.e. the first 2 values of a pygame.Rect).
    Not to be confused with ui_scale_blit.
    :param coords: The coordinates to scale
    :return: The scaled coordinates
    """
    return (
        floor(coords[0] * scripts.game_structure.screen_settings.screen_scale),
        floor(coords[1] * scripts.game_structure.screen_settings.screen_scale),
    )


def ui_scale_value(val: int):
    """
    Use to scale a single value according to the UI scale. If you need this one,
    you're probably doing something unusual. Try to avoid where possible.
    :param val: The value to scale
    :return: The scaled value
    """
    return floor(val * scripts.game_structure.screen_settings.screen_scale)


def ui_scale_blit(coords: Tuple[int, int]):
    """
    Use to scale WHERE to blit an item, not the SIZE of it. (0, 0) is the top left corner of the pygame_gui managed window,
    this adds the offset from fullscreen etc. to make it blit in the right place. Not to be confused with ui_scale_offset.
    :param coords: The coordinates to blit to
    :return: The scaled, correctly offset coordinates to blit to.
    """
    return floor(
        coords[0] * scripts.game_structure.screen_settings.screen_scale
        + scripts.game_structure.screen_settings.offset[0]
    ), floor(
        coords[1] * scripts.game_structure.screen_settings.screen_scale
        + scripts.game_structure.screen_settings.offset[1]
    )


# TODO move to either red_clan.py or sprites.py
def clan_symbol_sprite(clan, return_string=False, force_light=False):
    """
    returns the clan symbol for the given clan_name, if no symbol exists then random symbol is chosen
    :param clan: the clan object
    :param return_string: default False, set True if the sprite name string is required rather than the sprite image
    :param force_light: Set true if you want this sprite to override the dark/light mode changes with the light sprite
    """
    clan_name = clan.name
    if clan.chosen_symbol:
        if return_string:
            return clan.chosen_symbol
        else:
            if game.settings["dark mode"] and not force_light:
                return sprites.dark_mode_symbol(sprites.sprites[clan.chosen_symbol])
            else:
                return sprites.sprites[clan.chosen_symbol]
    else:
        possible_sprites = []
        for sprite in sprites.clan_symbols:
            name = sprite.strip("1234567890")
            if f"symbol{clan_name.upper()}" == name:
                possible_sprites.append(sprite)
        if return_string:  # returns the str of the symbol
            if possible_sprites:
                return choice(possible_sprites)
            else:
                # give random symbol if no matching symbol exists
                print(
                    f"WARNING: attempted to return symbol string, but there's no clan symbol for {clan_name.upper()}.  Random symbol string returned."
                )
                return f"{choice(sprites.clan_symbols)}"

        # returns the actual sprite of the symbol
        if possible_sprites:
            if game.settings["dark mode"] and not force_light:
                return sprites.dark_mode_symbol(
                    sprites.sprites[choice(possible_sprites)]
                )
            else:
                return sprites.sprites[choice(possible_sprites)]
        else:
            # give random symbol if no matching symbol exists
            print(
                f"WARNING: attempted to return symbol sprite, but there's no clan symbol for {clan_name.upper()}.  Random symbol sprite returned."
            )
            return sprites.dark_mode_symbol(
                sprites.sprites[f"{choice(sprites.clan_symbols)}"]
            )


def generate_sprite(
        cat,
        life_state=None,
        scars_hidden=False,
        acc_hidden=False,
        always_living=False,
        no_not_working=False,
) -> pygame.Surface:
    """
    Generates the sprite for a cat, with optional arguments that will override certain things.

    :param life_state: sets the age life_stage of the cat, overriding the one set by its age. Set to string.
    :param scars_hidden: If True, doesn't display the cat's scars. If False, display cat scars.
    :param acc_hidden: If True, hide the accessory. If false, show the accessory.
    :param always_living: If True, always show the cat with living lineart
    :param no_not_working: If true, never use the not_working lineart.
                    If false, use the cat.not_working() to determine the no_working art.
    """

    if life_state is not None:
        age = life_state
    else:
        age = cat.age.value

    if always_living:
        dead = False
    else:
        dead = cat.dead

    # setting the cat_sprite (bc this makes things much easier)
    if (
            not no_not_working
            and cat.not_working()
            and age != Rank.Newborn
            and game._game_config["cat_sprites"]["sick_sprites"]
    ):
        if age in [Rank.Kit, "adolescent"]:
            cat_sprite = str(19)
        else:
            cat_sprite = str(18)
    elif cat.pelt.paralyzed and age != Rank.Newborn:
        if age in [Rank.Kit, "adolescent"]:
            cat_sprite = str(17)
        else:
            if cat.pelt.length == "long":
                cat_sprite = str(16)
            else:
                cat_sprite = str(15)
    else:
        if age == Rank.Elder and not game._game_config["fun"]["all_cats_are_newborn"]:
            age = "senior"

        if game._game_config["fun"]["all_cats_are_newborn"]:
            cat_sprite = str(cat.pelt.cat_sprites[Rank.Newborn])
        else:
            cat_sprite = str(cat.pelt.cat_sprites[age])

    new_sprite = pygame.Surface(
        (sprites.size, sprites.size), pygame.HWSURFACE | pygame.SRCALPHA
    )

    # generating the sprite
    try:
        if cat.pelt.name not in ["Tortie", "Calico"]:
            new_sprite.blit(
                sprites.sprites[
                    cat.pelt.get_sprites_name() + cat.pelt.colour + cat_sprite
                    ],
                (0, 0),
            )
        else:
            # Base Coat
            new_sprite.blit(
                sprites.sprites[cat.pelt.tortiebase + cat.pelt.colour + cat_sprite],
                (0, 0),
            )

            # Create the patch image
            if cat.pelt.tortiepattern == "Single":
                tortie_pattern = "SingleColour"
            else:
                tortie_pattern = cat.pelt.tortiepattern

            patches = sprites.sprites[
                tortie_pattern + cat.pelt.tortiecolour + cat_sprite
                ].copy()
            patches.blit(
                sprites.sprites["tortiemask" + cat.pelt.pattern + cat_sprite],
                (0, 0),
                special_flags=pygame.BLEND_RGBA_MULT,
            )

            # Add patches onto cat.
            new_sprite.blit(patches, (0, 0))

        # TINTS
        if (
                cat.pelt.tint != "none"
                and cat.pelt.tint in sprites.cat_tints["tint_colours"]
        ):
            # Multiply with alpha does not work as you would expect - it just lowers the alpha of the
            # entire surface. To get around this, we first blit the tint onto a white background to dull it,
            # then blit the surface onto the sprite with pygame.BLEND_RGB_MULT
            tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
            tint.fill(tuple(sprites.cat_tints["tint_colours"][cat.pelt.tint]))
            new_sprite.blit(tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
        if (
                cat.pelt.tint != "none"
                and cat.pelt.tint in sprites.cat_tints["dilute_tint_colours"]
        ):
            tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
            tint.fill(tuple(sprites.cat_tints["dilute_tint_colours"][cat.pelt.tint]))
            new_sprite.blit(tint, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

        # draw white patches
        if cat.pelt.white_patches is not None:
            white_patches = sprites.sprites[
                "white" + cat.pelt.white_patches + cat_sprite
                ].copy()

            # Apply tint to white patches.
            if (
                    cat.pelt.white_patches_tint != "none"
                    and cat.pelt.white_patches_tint
                    in sprites.white_patches_tints["tint_colours"]
            ):
                tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                tint.fill(
                    tuple(
                        sprites.white_patches_tints["tint_colours"][
                            cat.pelt.white_patches_tint
                        ]
                    )
                )
                white_patches.blit(tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

            new_sprite.blit(white_patches, (0, 0))

        # draw vit & points

        if cat.pelt.points:
            points = sprites.sprites["white" + cat.pelt.points + cat_sprite].copy()
            if (
                    cat.pelt.white_patches_tint != "none"
                    and cat.pelt.white_patches_tint
                    in sprites.white_patches_tints["tint_colours"]
            ):
                tint = pygame.Surface((sprites.size, sprites.size)).convert_alpha()
                tint.fill(
                    tuple(
                        sprites.white_patches_tints["tint_colours"][
                            cat.pelt.white_patches_tint
                        ]
                    )
                )
                points.blit(tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
            new_sprite.blit(points, (0, 0))

        if cat.pelt.vitiligo:
            new_sprite.blit(
                sprites.sprites["white" + cat.pelt.vitiligo + cat_sprite], (0, 0)
            )

        # draw eyes & scars1
        eyes = sprites.sprites["eyes" + cat.pelt.eye_colour + cat_sprite].copy()
        if cat.pelt.eye_colour2 != None:
            eyes.blit(
                sprites.sprites["eyes2" + cat.pelt.eye_colour2 + cat_sprite], (0, 0)
            )
        new_sprite.blit(eyes, (0, 0))

        if not scars_hidden:
            for scar in cat.pelt.scars:
                if scar in cat.pelt.scars1:
                    new_sprite.blit(
                        sprites.sprites["scars" + scar + cat_sprite], (0, 0)
                    )
                if scar in cat.pelt.scars3:
                    new_sprite.blit(
                        sprites.sprites["scars" + scar + cat_sprite], (0, 0)
                    )

        # draw line art
        if game.settings["shaders"] and not dead:
            new_sprite.blit(
                sprites.sprites["shaders" + cat_sprite],
                (0, 0),
                special_flags=pygame.BLEND_RGB_MULT,
            )
            new_sprite.blit(sprites.sprites["lighting" + cat_sprite], (0, 0))

        if not dead:
            new_sprite.blit(sprites.sprites["lines" + cat_sprite], (0, 0))
        elif cat.df:
            new_sprite.blit(sprites.sprites["lineartdf" + cat_sprite], (0, 0))
        elif dead:
            new_sprite.blit(sprites.sprites["lineartdead" + cat_sprite], (0, 0))
        # draw skin and scars2
        blendmode = pygame.BLEND_RGBA_MIN
        new_sprite.blit(sprites.sprites["skin" + cat.pelt.skin + cat_sprite], (0, 0))

        if not scars_hidden:
            for scar in cat.pelt.scars:
                if scar in cat.pelt.scars2:
                    new_sprite.blit(
                        sprites.sprites["scars" + scar + cat_sprite],
                        (0, 0),
                        special_flags=blendmode,
                    )

        # draw accessories
        from scripts.cat.pelts import Pelt
        if not acc_hidden and cat.pelt.accessory:
            cat_accessories = cat.pelt.accessory
            categories = ["collars", "tail_accessories", "body_accessories", "head_accessories"]
            for category in categories:
                for accessory in cat_accessories:
                    if accessory in getattr(Pelt, category):
                        if accessory in cat.pelt.plant_accessories:
                            new_sprite.blit(
                                sprites.sprites["acc_herbs" + accessory + cat_sprite],
                                (0, 0),
                            )
                        elif accessory in cat.pelt.wild_accessories:
                            new_sprite.blit(
                                sprites.sprites["acc_wild" + accessory + cat_sprite],
                                (0, 0),
                            )
                        elif accessory in cat.pelt.collars:
                            new_sprite.blit(
                                sprites.sprites["collars" + accessory + cat_sprite], (0, 0)
                            )

        # Apply fading fog
        if (
                cat.pelt.opacity <= 97
                and not cat.prevent_fading
                and game.clan_obj.clan_settings["fading"]
                and dead
        ):
            stage = "0"
            if 80 >= cat.pelt.opacity > 45:
                # Stage 1
                stage = "1"
            elif cat.pelt.opacity <= 45:
                # Stage 2
                stage = "2"

            new_sprite.blit(
                sprites.sprites["fademask" + stage + cat_sprite],
                (0, 0),
                special_flags=pygame.BLEND_RGBA_MULT,
            )

            if cat.df:
                temp = sprites.sprites["fadedf" + stage + cat_sprite].copy()
                temp.blit(new_sprite, (0, 0))
                new_sprite = temp
            else:
                temp = sprites.sprites["fadestarclan" + stage + cat_sprite].copy()
                temp.blit(new_sprite, (0, 0))
                new_sprite = temp

        # reverse, if assigned so
        if cat.pelt.reverse:
            new_sprite = pygame.transform.flip(new_sprite, True, False)

    except (TypeError, KeyError):
        logger.exception("Failed to load sprite")

        # Placeholder image
        new_sprite = image_cache.load_image(
            f"sprites/error_placeholder.png"
        ).convert_alpha()

    return new_sprite


def update_sprite(cat):
    # First, check if the cat is faded.
    if cat.faded:
        # Don't update the sprite if the cat is faded.
        return

    # apply
    cat.sprite = generate_sprite(cat)
    # update class dictionary
    cat.all_cats[cat.ID] = cat


def apply_opacity(surface, opacity):
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            pixel = list(surface.get_at((x, y)))
            pixel[3] = int(pixel[3] * opacity / 100)
            surface.set_at((x, y), tuple(pixel))
    return surface


# ---------------------------------------------------------------------------- #
#                                     OTHER                                    #
# ---------------------------------------------------------------------------- #


def chunks(L, n):
    return [L[x: x + n] for x in range(0, len(L), n)]


def clamp(value: float, minimum_value: float, maximum_value: float) -> float:
    """
    Takes a value and returns it constrained to a certain range
    :param value: The input value
    :param minimum_value: Lower bound
    :param maximum_value: Upper bound
    :return: Clamped float.
    """
    if value < minimum_value:
        return minimum_value
    elif value > maximum_value:
        return maximum_value
    return value


def is_iterable(y):
    try:
        0 in y
    except TypeError:
        return False


def get_text_box_theme(theme_name=None):
    """Updates the name of the theme based on dark or light mode"""
    if game.settings["dark mode"]:
        return ObjectID("#dark", theme_name)
    else:
        return theme_name


def quit(savesettings=False, clearevents=False):
    """
    Quits the game, avoids a bunch of repeated lines
    """
    if savesettings:
        game.save_game_settings(None)
    if clearevents:
        game.cur_events_list.clear()
    game.rpc.close_rpc.set()
    game.rpc.update_rpc.set()
    pygame.display.quit()
    pygame.quit()
    if game.rpc.is_alive():
        game.rpc.join(1)
    sys_exit()


resource_directory = "resources/dicts/conditions/"
with open(os.path.normpath(f"{resource_directory}illnesses.json"), "r", encoding="utf-8") as read_file:
    ILLNESSES = ujson.loads(read_file.read())

with open(os.path.normpath(f"{resource_directory}injuries.json"), "r", encoding="utf-8") as read_file:
    INJURIES = ujson.loads(read_file.read())

with open(
        os.path.normpath(f"{resource_directory}permanent_conditions.json"), "r", encoding="utf-8"
) as read_file:
    PERMANENT = ujson.loads(read_file.read())

langs = {"snippet": None, "prey": None}

SNIPPETS = None
PREY_LISTS = None

with open(
        os.path.normpath("resources/dicts/backstories.json"), "r", encoding="utf-8"
) as read_file:
    BACKSTORIES = ujson.loads(read_file.read())
