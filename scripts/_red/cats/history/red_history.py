# red_history.py - Classes for keeping track of important game events.

# -------------------------------------------------------------------------------- #
# ----------------------------------------

########################################################################################################################
# Imports
########################################################################################################################

from dataclasses import dataclass
from typing import Optional

from definitions import HistoryTag


########################################################################################################################
# Classes
########################################################################################################################

@dataclass
class Attachments:
    """ Class to keep track of a cat's personal attachments. """

    curr_clan_prefix: str # FIXME
    prev_clan_prefixes: list[str] # FIXME

    curr_mentor_ids: list[int]
    prev_mentor_ids: list[int]
    curr_app_ids: list[int]
    prev_app_ids: list[int]

    bio_parent_ids: list[int]
    adpt_parent_ids: list[int]
    litter_mate_ids: list[int]
    sibling_ids: list [int]

    curr_mate_ids: list[int]
    prev_mate_ids: list[int]
    child_ids: list[int]

class RedHistory:
    """ Class to hold a cat's personal history. """

    cat_id: int

    backstory_str: str
    attachments: Attachments

    """ Timeline is in this format:
    moon, "text string", [tag, tag], [involved cat id, involved cat id]
    
    -98: [
        {
            text: "{CAT/main} was raised alone by {PRONOUN/main/poss} mother under a Twoleg dumpster.",
            tags: {HistoryTag.Birth: None},
            cat_dict: { "main": 1 },
            clan_dict: {},
        },
    ],
    0: [
        {
            text: "{CAT/main} was recruited to help found {CLAN/main}Clan by a cat with stars with in their fur who came to {CAT/main} in {PRONOUN/main/poss} dreams.",
            tags: {HistoryTag.JoinClan: "Wind", HistoryTag.RankChange: "warrior", },
            cat_dict: { "main": 1, }
            clan_dict: { "main": "Wind", }
        },
        {
            text: "{CLAN/afterlife} chose ",
            tags: {},
            cat_dict: {},
            clan_dict: {"main": "Wind", "afterlife": "_star_"},
        },
    ],
    3: [
        {
            text: "",
            tags: {},
            cat_dict: {},
            clan_dict: {},
        },
    ],
    
    0,"Pheasantstar was originally a loner, but was recruited to help found TestClan.", [HistoryTag.Birth], [12]
    3,"Pheasantstar was attacked by a rogue on a solo patrol. He escaped mostly unscathed, but was 
        left with a scar across his muzzle to remember the incident.", [HistoryTag.Scar], [21] # 21 is the cat_id of the rogue
    4,"Pheasantstar was killed by a dog. The leader has 8 lives left.",[HistoryTag.Death], []
    """
    timeline: dict[int, str]

    def __init__(self, **kwargs):
        if kwargs["save_file"]:
            self._parse_save_file(cat_id=kwargs["cat_id"], save_file=kwargs["save_file"])

        else:
            self.cat_id = kwargs["cat_id"]
            self.backstory_str = kwargs["backstory_str"]
            self.timeline = {}
            self.attachments = Attachments(
                curr_clan_prefix = kwargs["clan_token"],
                prev_clan_prefixes = kwargs["prev_clan_prefixes"],

                curr_mentor_ids=kwargs["curr_mentor_ids"],
                prev_mentor_ids=kwargs["prev_mentor_ids"],
                curr_app_ids = kwargs["curr_app_ids"],
                prev_app_ids = kwargs["prev_app_ids"],

                bio_parent_ids = kwargs["bio_parent_ids"],
                adpt_parent_ids = kwargs["adpt_parent_ids"],
                litter_mate_ids = kwargs["litter_mate_ids"],
                sibling_ids = kwargs["sibling_ids"],

                curr_mate_ids = kwargs["curr_mate_ids"],
                prev_mate_ids = kwargs["prev_mate_ids"],
                child_ids = kwargs["child_ids"]
            )
        return

    def _parse_save_file(self, cat_id: int, save_file: dict):
        """ Parse the contents of a save file. """
        self.cat_id = cat_id
        self.backstory_str = save_file["backstory_str"]
        self.timeline = save_file["timeline"]
        self.attachments = Attachments(
            curr_clan_prefix = save_file["attachments"]["curr_clan_prefix"],
            prev_clan_prefixes = save_file["attachments"]["prev_clan_prefixes"],

            curr_mentor_ids=save_file["attachments"]["curr_mentor_ids"],
            prev_mentor_ids=save_file["attachments"]["prev_mentor_ids"],
            curr_app_ids = save_file["attachments"]["curr_app_ids"],
            prev_app_ids = save_file["attachments"]["prev_app_ids"],

            bio_parent_ids = save_file["attachments"]["bio_parent_ids"],
            adpt_parent_ids = save_file["attachments"]["adpt_parent_ids"],
            litter_mate_ids = save_file["attachments"]["litter_mate_ids"],
            sibling_ids = save_file["attachments"]["sibling_ids"],

            curr_mate_ids = save_file["attachments"]["curr_mate_ids"],
            prev_mate_ids = save_file["attachments"]["prev_mate_ids"],
            child_ids = save_file["attachments"]["child_ids"]
        )
        return

    # TODO
    def update_attachments(self):
        """ """
        raise NotImplementedError("RedHistory.update_attachments")

    def get_scars_or_deaths(self, deaths: bool = False) -> list:
        """
        This returns the death/scar history list for the cat.

        [
            {
                'involved': ID,
                'text': text,
                "moon": moon
            },
            {
                'involved': ID,
                "text": text,
                "moon": moon
            }
            ]

        If there are no events with the scar or death tags, an empty list is returned.
        :param deaths: request death history, if False returns scar history
        """
        result: list = []
        desired_tag: HistoryTag = HistoryTag.Scar
        if deaths:
            desired_tag = HistoryTag.Death

        for event in self.timeline:
            tags: list[HistoryTag] = event[2]
            for tag in tags:
                if tag is desired_tag:
                    result.append(event)

        return result
