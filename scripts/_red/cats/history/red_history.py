# red_history.py - Classes for keeping track of important game events.

# -------------------------------------------------------------------------------- #
# ----------------------------------------

########################################################################################################################
# Imports
########################################################################################################################

from dataclasses import dataclass


########################################################################################################################
# Classes
########################################################################################################################

@dataclass
class Attachments:
    """ Class to keep track of a cat's personal attachments. """

    cat_id: int

    curr_clan_prefix: str
    prev_clan_prefixes: list[str]
    curr_litter_ids: list[int]
    parent_ids: list[int]
    curr_mate_ids: list[int]
    prev_mate_ids: list[int]
    curr_app_ids: list[int]
    prev_app_ids: list[int]
    curr_mentor_ids: list[int]
    prev_mentor_ids: list[int]

class RedHistory:
    """ Class to hold a cat's personal history. """

    backstory_str: str
    timeline: dict[int, str]
    attachments: Attachments

    def __init__(self, **kwargs):
        if not kwargs["save_file"]:
            self.backstory_str = kwargs["backstory_str"]
            self.timeline = {}
            self.attachments = Attachments(
                cat_id = kwargs["cat_id"],
                curr_clan_prefix = kwargs["clan_prefix"],
                prev_clan_prefixes = [],
                curr_litter_ids = [],
                parent_ids = [],
                curr_mate_ids = [],
                prev_mate_ids = [],
                curr_app_ids = [],
                prev_app_ids = [],
                curr_mentor_ids = [],
                prev_mentor_ids = []
            )
        else:
            self._parse_save_file(cat_id=kwargs["cat_id"], save_file=kwargs["save_file"])
        return

    def _parse_save_file(self, cat_id: int, save_file: dict):
        """ Parse the contents of a save file. """
        self.backstory_str = save_file["backstory_str"]
        self.timeline = save_file["timeline"]
        self.attachments = Attachments(
            cat_id = cat_id,
            curr_clan_prefix = save_file["attachments"]["curr_clan_prefix"],
            prev_clan_prefixes = save_file["attachments"]["prev_clan_prefixes"],
            curr_litter_ids = save_file["attachments"]["curr_litter_ids"],
            parent_ids = save_file["attachments"]["parent_ids"],
            curr_mate_ids = save_file["attachments"]["curr_mate_ids"],
            prev_mate_ids = save_file["attachments"]["prev_mate_ids"],
            curr_app_ids = save_file["attachments"]["curr_app_ids"],
            prev_app_ids = save_file["attachments"]["prev_app_ids"],
            curr_mentor_ids = save_file["attachments"]["curr_mentor_ids"],
            prev_mentor_ids = save_file["attachments"]["prev_mentor_ids"]
        )
        return
