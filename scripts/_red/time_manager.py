# time_manager.py - Class to handle the passage of time in the game.
from definitions import Season
########################################################################################################################
# Imports
########################################################################################################################

from scripts._red.red_exceptions import InitializationError
from scripts.game_structure.game_essentials import game
from scripts._red.text_handler import TextHandler
from scripts._red.clans.red_clan import RedClan, Camp

import logging
logger = logging.getLogger(__name__)


########################################################################################################################
# Classes
########################################################################################################################

class TimeManager:
    """ TODO """

    # TODO add a TimeManager object to game
    text_handler: TextHandler
    events_text: dict # TODO add this to a save file
    current_moon: int = 0 # TODO move this to time_manager
    current_season: Season = Season.Spring # TODO move this to time_manager
    _current_season_count: int = 0

    def __init__(self):
        self.text_handler = TextHandler()
        return

    # TODO
    def get_save_info(self):
        raise NotImplementedError(f"TimeManager.get_save_info()")
        return {
            "events_text": self.events_text,
            "time_info": {
                "current_moon": self.current_moon,
                "current_season": self.current_season,
                "current_season_count": self._current_season_count
            }
        }

    # TODO
    def moon_timeskip(self):
        """ Handles events that happen when the player hits the Timeskip button to end the moon. """
        events_text: dict = {}
        self._camp_events()
        self._timed_events()
        self._gathering_events()
        self._leader_focus_events()
        self._warrior_focus_events()
        self._war_events()
        self._rank_change_events()
        self._relationship_events()
        self._health_events()
        self._random_events()

        logger.debug(f"Finished the moon timeskip: advancing to moon {game.current_moon}")

    def _camp_events(self):
        """ Handle camp events - e.g. the use and spoiling of herbs and freshkill. """
        clan_obj: RedClan = game.cat_tracker.get_clan_object(clan_token=game.active_clan_token)
        rotted: dict = clan_obj.camp.timeskip_age_camp_stores()
        # TODO update the player on any rotted Clan resources

        # dict[clan_token, Clan object] - only extant Clans
        raise NotImplementedError("TimeManager._camp_events()")

    def _timed_events(self):
        """ Handle secret events which reveal themselves after a certain amount of time. """
        logger.debug(f"TimeManager._timed_events()")
        # TODO reveal of a kit's StarClan connection

        raise NotImplementedError("TimeManager._timed_events()")

    def _gathering_events(self):
        """ Handle events that happen during Gatherings. """
        raise NotImplementedError("TimeManager._gathering_events()")

    def _leader_focus_events(self):
        raise NotImplementedError("TimeManager._leader_focus_events()")

    def _warrior_focus_events(self):
        raise NotImplementedError("TimeManager._warrior_focus_events()")

    def _war_events(self):
        """ Handle events related to ongoing wars. """
        raise NotImplementedError("TimeManager._war_events()")

    def _rank_change_events(self):
        """ Handle events that change cats' names """
        logger.debug(f"TimeManager._rank_change_events()")
        # TODO promote apprentices

        # TODO retire elders

        # TODO if a warrior Clan doesn't have a leader or deputy, promote one

        # TODO make kits apprentices

        # TODO if the setting is active, have warriors/elders/etc. decide to be mediators

        raise NotImplementedError("TimeManager._name_change_events()")

    def _relationship_events(self):
        """ Handle events that change relationships between two cats in the active Clan. """
        logger.debug(f"TimeManager._relationship_events()")
        # TODO cats become mates

        # TODO cats break up

        # TODO random relationship events (the ones that show up in the events < relationships tab)
        raise NotImplementedError("TimeManager._relationship_events()")

    def _health_events(self):
        """ Handle changes in a cat's health, e.g. complications and deaths. """
        raise NotImplementedError("TimeManager._health_events()")

    def _random_events(self):
        """ Handle random events. """
        logger.debug(f"TimeManager._random_events()")
        # TODO disasters

        # TODO finding kittens

        # TODO loners join

        # TODO cats get grabbed by Twolegs

        # TODO lost cats return to the Clan

        # TODO new cats join the Clan

        # TODO permanent condition reveal

        # TODO pregnancies

        raise NotImplementedError("TimeManager._random_events()")