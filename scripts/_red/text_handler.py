# text_handler.py - A class for handling all things text string-related. For histories, events, etc.

########################################################################################################################
# Imports
########################################################################################################################

import random
from importlib import import_module
from modulefinder import Module

from resources._red.pelt import *

from definitions import (
    cast_to_rank,
    Rank, WhitePatchPattern, PeltLength, PeltPattern, EyeColour
)

import logging
logger = logging.getLogger(__name__)

# TODO remove everything between this and # Constants


########################################################################################################################
# Constants
########################################################################################################################

LOCALIZATION_RESOURCES_PATH: str = "resources.lang."


########################################################################################################################
# Classes
########################################################################################################################

class TextHandler:
    """ A class for handling all things text string-related. For use in UIs and in-game content.

    We use ISO 2-letter language codes for storing the language a player wants to use. This means that en
    is English, fr is French, es is Spanish, etc. Check online what the code is for the language you are
    planning to implement, as you'll need it in many places.

    There is a helper Python script in resources/lang called create_new_lang_files.py. By changing the
    2-letter code on line 7 of the file and running it, it will automatically create and rename all the
    files you'll need to localize into that language.
    """

    lang_iso_code: str
    lang_resources_path: str
    lang_module: Module

    default_pronouns: dict[int: dict[str: str]]

    _previous_lang_iso_code: str = None

    def __init__(self):
        return

    # ----------------------------------- INIT ----------------------------------- #

    def __load_lang_resources_cat(self):
        """ Programmatically import language modules. """
        try:
            self.lang_module = import_module(self.lang_resources_path)
            self.default_pronouns = self.lang_module.cat.en.PRONOUNS

        except ModuleNotFoundError as e:
            msg = (f"Something went wrong while loading language resources. Most likely the language "
                   f"code you tried to set, {self.lang_iso_code}, doesn't exist.")
            if self._previous_lang_iso_code:
                # Return to previous code if available.
                msg += f"Returning to previous language, {self.lang_iso_code}."
                self.lang_iso_code = self._previous_lang_iso_code
                self._previous_lang_iso_code = None
            elif self.lang_iso_code != 'en':
                # Try dev language as fallback.
                msg += f"Defaulting to English."
                self.lang_iso_code = 'en'
            else:
                # English isn't loading properly! Panic!
                msg += f"No fallback language available."
                logger.exception(msg, e)
                raise
            logger.error(msg)

        return

    # ---------------------------------- PUBLIC ---------------------------------- #

    def load_new_language(self, lang_iso_code: str):
        # TODO translator
        self.lang_iso_code = lang_iso_code
        self.lang_resources_path = LOCALIZATION_RESOURCES_PATH + self.lang_iso_code
        self.__load_lang_resources_cat()


    def change_language(self, new_language_code: str):
        self._previous_lang_iso_code = self.lang_iso_code
        self.lang_iso_code = new_language_code
        self.__load_lang_resources_cat()
        return

    def update_old_event_text(self, text):
        """ Updates old text for events to the current standard. """
        # TODO check resources.dicts.patrols.reformat_patrols
        # TODO move this to ConversionManager

    def handle_text_content_event(self, text, event):
        """ """
        if not isinstance(text, str):
            text: str = self._catch_old_text_types(text)

        # split the text into individual words/formatting codes/whatever to make filtering easier.
        text_by_word: list = text.split(" ")

        # update old text formatting codes to current ones.
        text_by_word = self._catch_old_text_formatting(text_by_word)

        cat_dict: dict = event.cat_dict # {str: Cat}
        result: str = ""

        for chunk in text_by_word:
            # search for brackets once the text has been passed through self._catch_old_text_formatting
            #  if there are none, there's nothing to be replaced in this chunk
            if '{' not in chunk:
                to_add = chunk
                result += chunk
                result += " "
                continue

            args = chunk[1,-2].split('/')
            to_add: str = ""

            if args[0] == 'CLAN':
                whose_clan_cat_code = args[1] # this is a string
                clan_obj = cat_dict[whose_clan_cat_code].clan_obj # this is a Clan object

                if len(args) == 2:
                    to_add = clan_obj.name # "Clan" should already be added
                else:
                    spec: str = args[2]
                    if spec == 'leader':
                        to_add = clan_obj.leader.name
                    elif spec == 'deputy':
                        to_add = clan_obj.deputy.name
                    elif spec == 'medicine':
                        med_cat_id = random.choice(clan_obj.med_cat_list) # this is an integer
                        to_add = random.choice(clan_obj.med_cat_list).name
                    elif spec == 'mediator':
                        to_add = random.choice(clan_obj.mediator_list).name
                    elif spec == 'biome':
                        to_add = clan_obj.camp.biome

            elif args[0] == 'CAT':
                cat_code: str = args[1]
                cat_obj = cat_dict[cat_code] # this is a Cat object

                if len(args) == 2:
                    to_add = cat_obj.name
                else:
                    if args[2][0:3] == 'rel':
                        # cat_rel is a list of Cat objects
                        if args[2] == 'rel.mate_ever':
                            cat_rel_list = [*cat_obj.history.mate_prev, *cat_obj.history.mate]
                        elif args[2] == 'rel.mate_prev':
                            cat_rel_list = cat_obj.history.mate_prev
                        elif args[2] == 'rel.mate':
                            cat_rel_list = cat_obj.history.mate
                        elif args[2] == 'rel.child':
                            cat_rel_list = cat_obj.history.children
                        elif args[2] == 'rel.parent':
                            cat_rel_list = cat_obj.history.parent
                        elif args[2] == 'rel.sibling':
                            cat_rel_list = cat_obj.history.sibling
                        elif args[2] == 'rel.littermate':
                            cat_rel_list = cat_obj.history.littermate
                        elif args[2] == 'rel.prev_mentor':
                            cat_rel_list = cat_obj.history.prev_mentor
                        elif args[2] == 'rel.mentor':
                            cat_rel_list = [cat_obj.history.mentor]
                        elif args[2] == 'rel.apprentice':
                            cat_rel_list = [cat_obj.history.apprentice]
                        else:
                            raise KeyError(f"Could not find a relationship attribute matching {args[2]}")

                        if len(args) > 2:
                            to_add = random.choice(cat_rel_list).name
                        else:
                            rel_filt: str = args[3]
                            filt_cat_rel_list: list = [] # filt_cat_rel_list is a list of Cat objects
                            if rel_filt == 'dead':
                                if len(args) > 3:
                                    cat_rel_rank: Rank = cast_to_rank(args[4])
                                    for single_cat_rel_obj in cat_rel_list: # single_cat_rel_obj is a Cat object
                                        if single_cat_rel_obj.rank is cat_rel_rank:
                                            filt_cat_rel_list.append(single_cat_rel_obj)
                                            to_add = random.choice(filt_cat_rel_list).name
                                else:
                                    filt_cat_rel_list = [c for c in cat_rel_list if c.dead]
                                    to_add = random.choice(filt_cat_rel_list).name

                            elif rel_filt in ['live', 'alive', 'living']:
                                filt_cat_rel_list = [c for c in cat_rel_list if not c.dead]
                                to_add = random.choice(filt_cat_rel_list).name

                            elif (rel_filt == 'all') and (len(cat_rel_list) > 1):
                                num_rels: int = len(cat_rel_list)
                                for i in range(num_rels):
                                    if i == (num_rels - 1):
                                        to_add += f"and {cat_rel_list[i]}"
                                    else:
                                        to_add += f"{cat_rel_list[i]}, "

                            elif 'emo' in rel_filt:
                                raise NotImplementedError(f"Relationships aren't implemented yet, so you can't filter "
                                                          f"for emotional relationships between cats yet. Sorry!")
                    elif [args][2][0:4] == 'hist':
                        if [args][2] == 'hist.birth.moon':
                            to_add = cat_obj.history.birth
                        else:
                            raise KeyError(f"Could not find a history attribute matching {args[2]}")
                    else:
                        if args[2] == 'rank':
                            to_add = cat_obj.rank
                        else:
                            raise KeyError(f"Could not find a cat code filter matching {args[2]}")


            elif args[0] == 'PRONOUN':
                """ Pronoun dict format:
                        subject: he
                        object: him
                        poss: his
                        inposs: his
                        self: himself
                        conju: 2
                        gender: 1
                """
                # if the cat uses custom pronouns, get them
                gender = cat_dict[args[1]].gender
                custom_pronouns_b: bool = gender.pronouns["custom"]
                cat_obj_pronouns: dict[str: str] = {}
                if custom_pronouns_b:
                    # If a cat has custom pronouns, gender.pronouns[ISO code] is a dictionary matching the pronoun format
                    cat_obj_pronouns = gender.pronouns[self.lang_iso_code]
                else:
                    cat_obj_pronouns = self.default_pronouns[gender.pronouns[self.lang_iso_code]]
                to_add = cat_obj_pronouns[args[2]]

            elif args[0] == 'VERB':
                # TODO handle VERB
                # {VERB/m_c/reside/resides}
                pass

            elif args[0] == 'ADJ':
                # TODO handle ADJ
                pass

            else: # stuff you need to do I/O operations for
                # TODO import snippet_collections.json

                # TODO handle STORY
                if args[0] == 'STORY':
                    pass

                # TODO handle DREAM
                elif args[0] == 'DREAM':
                    pass

                # TODO handle CLAIR
                elif args[0] == 'CLAIR':
                    pass

                # TODO handle OMEN
                elif args[0] == 'OMEN':
                    pass

                # TODO handle PROPHECY
                elif args[0] == 'PROPHECY':
                    pass

                else:
                    raise KeyError(f"Could not determine how to parse \"{chunk}\"")

            result += to_add
            result += " "
            continue

        return result[:-1] #

    def handle_text_content_allegiances(self, clan_obj):
        """ Assemble the string for an Allegiances screen. """

        def describe_pelt(pelt, name) -> str:
            """ Assembles a brief description of a cat's pelt for the Allegiances screen.

            For the extra detail:
                -> only include the extra detail if the rest of the description is very short
                1 if the cat was named after their eye colour, use their eye colour
                2 if the cat has an obvious scar (see resources/_red_text/pelt.py) use that
                3 if the cat has large white patches use that
            """
            # These are useful tools that will help us later!
            colour_source: dict[str: str] = PELT_COLOUR_TEXT[ScreenName.Allegiances]
            pattern_source: dict[str: str] = PELT_PATTERN_TEXT[ScreenName.Allegiances]
            eye_source: dict[str: str] = EYE_COLOUR_TEXT[ScreenName.Allegiances]
            colour_pattern = ""
            extra_detail: str = ""
            commas_f: bool = False
            extra_detail_f: bool = True
            mention_white_f: bool = False

            # are commas necessary?
            if pattern_source["before_colour"] \
                and not (pelt.white_patch_pattern is WhitePatchPattern.FullWhite) \
                and (ScarPelt.BlindBoth in pelt.scars):
                commas_f = True

            # pick an extra detail
            if pelt.white_patch_pattern.category in (
                    WhitePatchPatternCategory.Mostly, WhitePatchPatternCategory.High, WhitePatchPatternCategory.Mid):
                mention_white_f = True

            # the extra detail is eye colour
            if type(name.prefix_source) is EyeColour:
                eye_text: str = eye_source[name.prefix_source]
                vowel_f: bool = eye_text[0].lower() in "aeiou"
                if pelt.eye_colour[0] is pelt.eye_colour[1]:
                    extra_detail = f" with {eye_text} eyes"
                else:
                    extra_detail = f" with an {eye_text} eye" if eye_text[0].lower() in "aeiou" \
                        else f" with a {eye_text} eye"
            # the extra detail is scarring
            for has_scar in pelt.scars:
                break_f: bool = False
                for scar, scar_text in SCAR_TEXT[ScarPelt]:
                    if has_scar is scar:
                        if scar is ScarPelt.BlindBoth:
                            colour_pattern = "blind, " if commas_f else "blind "
                        else:
                            extra_detail = scar_text
                        break_f = True
                        break
                if break_f:
                    break
                else:
                    if has_scar in SCAR_TEXT[ScarCategory].keys():
                        extra_detail = SCAR_TEXT[ScarCategory][has_scar]

            # is the cat fluffy
            if pelt.length is PeltLength.Long:
                colour_pattern += "long-furred, " if commas_f else "long-furred "

            # if the cat is one solid colour, you probably want to
            #  include extra details like scars and/or eye colour
            #  (preferably if they're mid-high or higher, mention
            #  that)
            # cats can be one solid colour because of the FullWhite
            #   white patch or because of the SingleColour pattern
            if pelt.white_patch_pattern is WhitePatchPattern.FullWhite:
                colour_pattern += "white {GENDER}" + extra_detail
            elif pelt.pattern is PeltPattern.SingleColour:
                colour_pattern += colour_source[pelt.colour]
                if mention_white_f:
                    colour_pattern += " and white {GENDER}"
                else:
                    colour_pattern += " {GENDER}"

            # handle pointed cats
            elif pelt.white_patch_pattern in (WhitePatchPattern.ColourPoint,
                                            WhitePatchPattern.Ragdoll,
                                            WhitePatchPattern.SealPoint):
                colour_pattern += colour_source[pelt.colour] + " {GENDER} with a white body"
                mention_eyes_f = False

            # handle torties and calicos
            elif pelt.tortie_colour:
                colour_pattern += (f"{pattern_source[pelt.pattern]["before_colour"]} "
                                  f"{colour_source[pelt.colour]}-and-{colour_source[pelt.tortie_colour]}")
                if mention_white_f:
                    colour_pattern += " calico {GENDER}"
                else:
                    colour_pattern += " tortoiseshell {GENDER}"
                if pattern_source[pelt.pattern]["after_gender"]:
                    colour_pattern += f" {pattern_source[pelt.pattern]["after_gender"]}"
                # don't include extra details for tortoiseshells and calicos

            # handle everyone else
            else:
                colour_pattern += (f"{pattern_source[pelt.pattern]["before_colour"]} "
                                  f"{colour_source[pelt.colour]} {pattern_source[pelt.pattern]["after_colour"]}")
                colour_pattern += "{GENDER}"
                if pattern_source[pelt.pattern]["after_gender"]:
                    mention_eyes_f = False
                    colour_pattern += f" {pattern_source[pelt.pattern]["after_gender"]}"

            if extra_detail_f:
                colour_pattern += f" with {eye_source[pelt.eye_colour]} eyes"

            return colour_pattern


        allegiances: str = ""
        for rank in clan_obj.clan_cats:
            for cat in clan_obj.clan_cats[rank]:
                cat_text: str = f"{str(cat.name).upper} - "

                # describe the cat's pelt
                cat_desc = describe_pelt(pelt=cat.pelt, name=cat.name)



    # ---------------------------------- PRIVATE --------------------------------- #

    def _catch_old_text_types(self, text) -> str:
        """ Catches bug edge-cases from old saves. """
        try:
            # if text is a list, combine all entries in the list into a single string
            if isinstance(text, list):
                temp = ""
                for _ in text:
                    temp = temp + _
                text = temp
                del temp
        except Exception as e:
            logger.exception(f"Could not convert old text type to current text type", e)
            raise
        else:
            return text

    def _catch_old_text_formatting(self, text_by_word: list[str]) -> list[str]:
        """ Update text formatting.

        TODO
         - add brackets around all replaceable text
         - update name codes
         - update snippets
        """
        result: list[str] = []
        try:
            for chunk in [_ for _ in text_by_word if ("_" in _)]: # this applies to pretty much all formatting codes and nothing else
                # if the chunk isn't surrounded by brackets, add them
                if chunk[0] != "{":
                    chunk = "{" + chunk
                if chunk[-1] != "}":
                    chunk = chunk + "}"

                # TODO replace old name codes ["m_c" -> "{CAT/m_c}"], ["c_n" -> "{CLAN/m_c/name}"]

                # TODO replace snippets ["omen_list_sight" -> "{OMEN/sight}"]


            # TODO
            #   - name codes [m_c, r_c]
            #   - snippets

            # TODO old name codes
            #   - c_n -> {CLAN/m_c}
            #   - o_c_n -> {CLAN/r_c}

        except Exception as e:
            logger.exception(f"Could not convert old text format to current text format", e)
            raise

        else:
            return result

    def _filter_cats(self, text: str, cat_dict: dict) -> str:
        """ Filter text to replace cat pronouns and names.

        Intended for use with patrol text, event text, and history text.

        Possible codes for cat_code:
            "m_c": _r, # main cat
            "r_c": _r, # a random cat
            "r_c1": _r, # a random cat
            "r_c2": _r, # a random cat
            "n_c": _r, # newly generated cat
            "app1": _r, # a random cat with an apprentice rank
            "app2": _r, # a random cat with an apprentice rank
            "app3": _r, # a random cat with an apprentice rank
            "app4": _r, # a random cat with an apprentice rank
            "app5": _r, # a random cat with an apprentice rank
            "app6": _r, # a random cat with an apprentice rank
            "p_l": _r, # patrol leader
            "s_c": _r, # skilled cat - a cat who meets a specific stat_skill requirement
            "(mentor)": _r, # m_c's current mentor
            "l_n": _r, # m_c's Clan leader's name
            "dead_par1": _r, # a random dead cat who was once m_c's partner
            "dead_par2": _r, # a random dead cat who was once m_c's partner
            "p1": _r, # a random cat who is m_c's partner
            "p2": _r, # a random cat who is m_c's partner
            "(deadmentor)": _r, # a random dead cat who was once m_c's mentor
            "(previous_mentor)": _r, # a random living cat who was once m_c's mentor
            "mur_c": _r, # a random dead cat who m_c murdered
            "c_n": _r, # Clan name
            "o_c_n": _r, # other Clan name
            "lead_name": _r, # m_c's Clan leader
            "dep_name": _r, # m_c's Clan deputy
            "med_name": _r, # a random cat who is a medicine cat in m_c's Clan
            "cat_tag": _r, # a specific cat's name, used in filtering for snippets
        """

    def filter_text(self, text: str) -> str:
        """ Filter event text to replace pronoun codes, names, etc.

        Possible codes for cat_code:
            "m_c": _r, # main cat
            "r_c": _r, # a random cat
            "r_c1": _r, # a random cat
            "r_c2": _r, # a random cat
            "n_c": _r, # newly generated cat
            "app1": _r, # a random cat with an apprentice rank
            "app2": _r, # a random cat with an apprentice rank
            "app3": _r, # a random cat with an apprentice rank
            "app4": _r, # a random cat with an apprentice rank
            "app5": _r, # a random cat with an apprentice rank
            "app6": _r, # a random cat with an apprentice rank
            "p_l": _r, # patrol leader
            "s_c": _r, # skilled cat - a cat who meets a specific stat_skill requirement
            "(mentor)": _r, # m_c's current mentor
            "l_n": _r, # m_c's Clan leader's name
            "dead_par1": _r, # a random dead cat who was once m_c's partner
            "dead_par2": _r, # a random dead cat who was once m_c's partner
            "p1": _r, # a random cat who is m_c's partner
            "p2": _r, # a random cat who is m_c's partner
            "(deadmentor)": _r, # a random dead cat who was once m_c's mentor
            "(previous_mentor)": _r, # a random living cat who was once m_c's mentor
            "mur_c": _r, # a random dead cat who m_c murdered
            "c_n": _r, # Clan name
            "o_c_n": _r, # other Clan name
            "lead_name": _r, # m_c's Clan leader
            "dep_name": _r, # m_c's Clan deputy
            "med_name": _r, # a random cat who is a medicine cat in m_c's Clan
            "cat_tag": _r,
        """

        for cat_code in self.cat_dict:
            # cat_code is, for example, m_c
            cat_obj = self.cat_dict[cat_code]

            # replace cat's name
            text.replace(cat_code, cat_obj.name)

            # TODO replace cat pronouns

            # TODO replace Clan names

            # TODO replace verbs
            # Verbs are replaced using the pronoun_template "conju" attribute.
            # E.g. {VERB/continue/continues} + conju=1 -> continue
            pass

        return text

    def _filter_snippets(self, text: str):
        """ Filters things that should be replaced from resources/lang/{ISO code}/snippet_collections.json.

        These are: prophecies, omens, dreams, clairvoyant visions, and stories told on patrols.
        """

        # TODO handle story snippets

        # TODO handle dream snippets

        # TODO handle clairvoyance snippets

        # TODO handle omen snippets

        # TODO handle prophecy snippets


########################################################################################################################
# Instances
########################################################################################################################

text_handler: TextHandler = TextHandler()
