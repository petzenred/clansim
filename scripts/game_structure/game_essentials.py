# game_essentials.py - Create the game object, a semi-global object which updates the screens and acts
#   as a central databank to access all game information.

########################################################################################################################
# Imports
########################################################################################################################

import os
from sys import exit as sys_exit
from typing import Optional

import pygame
import traceback
import ujson
from shutil import move as shutil_move
from types import FunctionType

from scripts._red.cat_tracker import CatTracker
from scripts._red.config_manager import config
from scripts._red.io_manager import io_manager
from scripts._red.red_exceptions import InitializationError

from scripts.event_class import Single_Event
from scripts.housekeeping.datadir import get_save_dir, get_temp_dir

from definitions import (
    CLAN_MEMBERS_SCREEN_NAME, GAME_SETTINGS_FILENAME, MAIN_MENU_SCREEN_NAME,
    GameMode, LanguageCode, Season,
)

import logging
logger = logging.getLogger(__name__)


########################################################################################################################
# Classes
########################################################################################################################

pygame.init()


# G A M E
class Game:
    """ The pygame Game object. """

    # ################## NEW GAME PARAMS ##################

    language_code: LanguageCode = LanguageCode.UnsetLanguage
    game_mode: GameMode = GameMode.UnsetGameMode
    cat_tracker: CatTracker = None
    active_clan_token: str = None
    current_moon: int = 0 # TODO move this to time_manager
    current_season: Season = Season.Spring # TODO move this to time_manager

    clansim_version: str # TODO set this

    fps: int = 30

    # game managers
    _save_manager = None # this is a SaveManager object, but can't be type hinted to avoid circular imports
    _screen_manager = None # this is the ScreenManager object, but can't be type hinted to avoid initialization problems

    error_msg: str = ""
    error_trace = None

    # ################## OLD GAME PARAMS ##################

    # Keeping track of various screens for various purposes
    current_screen_obj = None # TODO get rid of this - replace with screen_manager.curr_screen_name
    last_screen_forupdate = MAIN_MENU_SCREEN_NAME
    last_screen_forProfile = CLAN_MEMBERS_SCREEN_NAME
    last_list_forProfile = None

    # max_events_displayed = 10
    # event_scroll_ct = 0
    # max_allegiance_displayed = 17
    # allegiance_scroll_ct = 0
    # max_relation_events_displayed = 10
    # relation_scroll_ct = 0 = field(default_factory=list)

    max_clan_prefix_length: int = 10
    settings_changed: bool = False

    mediated = []  # Keep track of which couples have been mediated this moon.
    just_died = []  # keeps track of which cats died this moon via die()

    cur_events_list = []
    ceremony_events_list = []
    birth_death_events_list = []
    relation_events_list = []
    health_events_list = []
    other_clans_events_list = []
    misc_events_list = []
    herb_events_list = []
    freshkill_event_list = []

    allegiance_list = []

    cat_to_fade = []
    sub_tab_list = ["life events", "user notes"]

    # down = pygame.image.load("resources/images/buttons/arrow_down.png").convert_alpha()
    # up = pygame.image.load("resources/images/buttons/arrow_up.png").convert_alpha()

    # Sort-type
    sort_type = "rank"

    choose_cats = {}
    """cat_buttons = {
        'cat0': None,
        'cat1': None,
        'cat2': None,
        'cat3': None,
        'cat4': None,
        'cat5': None,
        'cat6': None,
        'cat7': None,
        'cat8': None,
        'cat9': None,
        'cat10': None,
        'cat11': None
    }"""
    patrol_cats = {}
    patrolled = []

    # store changing parts of the game that the user can toggle with buttons
    switches = {
        "cat": None,
        "clan_name": "",
        "leader": None,
        "deputy": None,
        "medicine_cat": None,
        "members": [],
        "re_roll": False,
        "roll_count": 0,
        "event": None,
        "cur_screen": MAIN_MENU_SCREEN_NAME,
        "last_screen": MAIN_MENU_SCREEN_NAME,
        "naming_text": "",
        "timeskip": False,
        "mate": None,
        "choosing_mate": False,
        "mentor": None,
        "setting": None,
        "save_settings": False,
        "list_page": 1,
        "events_left": 0,
        "save_clan": False,
        "saved_clan": False,
        "new_leader": False,
        "apprentice_switch": False,
        "deputy_switch": False,
        "clan_list": "",
        "switch_clan": False,
        "read_clans": False,
        "kill_cat": False,
        "current_patrol": [],
        "patrol_remove": False,
        "cat_remove": False,
        "fill_patrol": False,
        "patrol_done": False,
        "error_message": "",
        "traceback": "",
        "apprentice": None,
        "change_name": "",
        "change_suffix": "",
        "name_cat": None,
        "biome": None,
        "camp_bg": None,
        "language": "en",
        "options_tab": None,
        "profile_tab_group": None,
        "sub_tab_group": None,
        "gender_align": None,
        "show_details": False,
        "chosen_cat": None,
        "game_mode": "",
        "set_game_mode": False,
        "broke_up": False,
        "show_info": False,
        "patrol_chosen": "general",
        "favorite_sub_tab": None,
        "root_cat": None,
        "skip_conditions": [],
        "show_history_moons": False,
        "fps": 30,
        "war_rel_change_type": "neutral",
        "disallowed_symbol_tags": [],
        "saved_scroll_positions": {},
        "moon&season_open": False,
    }
    all_screens = {}
    current_events = {}
    _future_events = {} #
    map_info = {}

    # SETTINGS
    # settings = {}
    # settings["moon&season_open"] = False
    setting_lists = {}

    debug_settings = {
        "showcoords": False,
        "showbounds": False,
        "visualdebugmode": False,
        "showfps": False,
    }

    # Init Settings
    # _settings = GAME_SETTINGS
    #
    # for setting, values in _settings["__other"].items():
    #     settings[setting] = values[0]
    #     setting_lists[setting] = values
    #
    # _ = []
    # _.append(_settings["general"])
    #
    # for cat in _:  # Add all the settings to the settings dictionary
    #     for setting_name, inf in cat.items():
    #         settings[setting_name] = inf[2]
    #         setting_lists[setting_name] = [inf[2], not inf[2]]
    # del _settings
    # del _
    # End init settings


    # CLAN
    clan_obj = None
    cat_class = None

    rpc = None # TODO rename discord_rpc

    is_close_menu_open = False

    # ------------------------------------- INIT ------------------------------------- #

    def initialize(self, save_manager, screen_manager):
        config.load_game_settings()
        self._save_manager = save_manager
        self._screen_manager = screen_manager
        return

    def __init__(self):
        """ Create the Game object. """
        self.clicked = False # TODO can I get rid of this?
        self.keyspressed = []
        self.switch_screens = False
        return

    def _ready_to_go(self):
        """ Check if all the external initialization has finished. """
        ready_to_go: bool = True
        if not self._save_manager:
            ready_to_go = False
        if not ready_to_go:
            raise InitializationError(f"game hasn't been fully initialized yet")
        return

    # ------------------------------------ PUBLIC ------------------------------------ #

    def get_valid_invalid_saves(self) -> tuple[list[str], list[str]]:
        """ Return two lists of Clan prefixes, separated into valid save files and invalid save files."""
        return self._save_manager.get_available_saves()

    # ------------------------------------ PRIVATE ----------------------------------- #

    def update_active_clan_token_everywhere(self, new_active_clan_token: Optional[str]) -> bool:
        """ Update the active Clan.

        Updates: the game object, the save manager, the I/O manager, and the screen manager.

        :param new_active_clan_token: the name of the Clan in the save file you want to try to update the game to
        :return bool: True if the active Clan prefix was updated, False otherwise
        """
        # if new_active_clan_prefix is None:
        #     logger.info(f"Setting active Clan to None")
        #     self.active_clan_token = None
        #     self._save_manager.update_active_clan_prefix(new_active_clan_prefix=None)
        #     io_manager.update_active_clan_prefix(new_active_clan_prefix=None)
        #     return True
        # elif io_manager.check_save_validity(new_active_clan_prefix):
        #     logger.info(f"Setting active Clan to {new_active_clan_prefix}")
        #     self.active_clan_token = new_active_clan_prefix
        #     self._save_manager.update_active_clan_prefix(new_active_clan_prefix=new_active_clan_prefix)
        #     io_manager.update_active_clan_prefix(new_active_clan_prefix=new_active_clan_prefix)
        #     return True
        # else:
        #     logger.warning(f"Can't change active Clan to '{new_active_clan_prefix}' "
        #                    f"because there is no corresponding valid save")
        #     logger.warning(f"Setting active Clan to None")
        #     self.update_active_clan_prefix_everywhere(new_active_clan_prefix=None)
        #     return False

        logger.info(f"Setting active Clan to {new_active_clan_token}")
        self.active_clan_token = new_active_clan_token
        io_manager.update_active_clan_token(new_active_clan_token=new_active_clan_token)
        self._screen_manager.update_active_clan_token(new_active_clan_token=new_active_clan_token)

        if new_active_clan_token and not io_manager._check_save_validity(new_active_clan_token):
            logger.warning(f"Can't change active Clan to '{new_active_clan_token}' "
                           f"because there is no corresponding valid save")
            logger.warning(f"Setting active Clan to None")
            self.update_active_clan_token_everywhere(new_active_clan_token=None)
            return False
        return True

    # TODO use time_manager here
    def _update_future_events(self):
        """ Runs any events that are scheduled. """
        # update all events so they're one moon closer
        moons = list(self._future_events.keys())
        moons.sort() # make sure that the events are ordered so the closest events are parsed first
        for moon in moons:
            temp = self._future_events[moon]
            self._future_events[moon - 1] = temp
            self._future_events[moon] = []

        # run any events whose scheduled time has come
        # if self._future_events[0]:
        if self._future_events:
            num_events = len(self._future_events)
            for n in range(num_events):
                event: tuple = self._future_events.pop(n)
                function: FunctionType = event[0]
                kwargs: dict = event[1]
                args: list = event[2]
                function(*args, **kwargs)
        return

    # ------------------------------------ PUBLIC ------------------------------------ #

    def update_game(self):
        # replaced by screen_manager.queue_screen_switch()
        # if self.current_screen_obj != self.switches["cur_screen"]:
        #     self.current_screen_obj = self.switches["cur_screen"]
        #     self.switch_screens = True
        self.clicked = False
        self.keyspressed = []
        self._update_future_events()

    def add_to_future_events(self, moons: int, function: FunctionType, kwargs: dict = {}, args: list = []):
        """ Schedule an event to be run at a specified point in the future. """
        if moons not in self._future_events.keys():
            self._future_events[moons] = []
        self._future_events[moons].append((function, kwargs, args))

    def switch_to_new_save(self, new_active_clan_prefix: Optional[str]) -> bool:
        """ Switch to a different game save.

        Note that this method does NOT save the game first.

        :param new_active_clan_prefix: the name of the Clan in the save file you want to try to update the game to
        :return bool: True if the game successfully switched to the new save file, False otherwise
        """
        if self.update_active_clan_token_everywhere(new_active_clan_token=new_active_clan_prefix):
            # delete the old cat tracker
            if self.cat_tracker:
                del self.cat_tracker
            self.cat_tracker = None
            # load the new save file
            self._load_active_clan_save_file()
            return True
        else:
            logger.error(f"Couldn't switch to new save {new_active_clan_prefix}Clan")
            return False

    def _load_active_clan_save_file(self):
        """ Load the save file corresponding to the active Clan prefix. """
        self.cat_tracker = CatTracker()
        config.load_clan_settings()
        # TODO handle what happens if any of the save files are malformed
        # TODO create a custom MalformedSaveError to catch here to make that easier
        self._save_manager.load_save()
        # TODO move the stuff below to self.update_active_clan_prefix_everywhere
        clan_obj = self.cat_tracker.get_clan_object(clan_token=self.active_clan_token)
        self._screen_manager.set_active_clan_camp(camp_key=clan_obj.camp.camp_key)
        return

    def save(self):
        # TODO self.time_manager.get_save_info()
        self._save_clans_and_cats()
        self._save_events()
        raise NotImplementedError("game.save")

    def quit(self, savesettings: bool = False, clearevents: bool = False):
        """ Quits the game, avoids a bunch of repeated lines. """
        if savesettings:
            self._save_manager.save_game_settings()
        if clearevents:
            game.cur_events_list.clear()
        game.rpc.close_rpc.set()
        game.rpc.update_rpc.set()
        pygame.display.quit()
        pygame.quit()
        if game.rpc.is_alive():
            game.rpc.join(1)
        sys_exit()

    # ------------------------------------- SAVE ------------------------------------- #

    def _save_clans_and_cats(self):
        raise NotImplementedError("game._save_clans_and_cats")

    def _save_events(self):
        raise NotImplementedError("game._save_events")

    # ----------------------------------- OUTDATED ----------------------------------- #

    # TODO remove this once SaveManager is implemented
    @staticmethod
    def safe_save(path: str, write_data, check_integrity=False, max_attempts: int = 15):
        """If write_data is not a string, assumes you want this
        in json format. If check_integrity is true, it will read back the file
        to check that the correct data has been written to the file.
        If not, it will simply write the data to the file with no other
        checks."""

        # If write_data is not a string,
        if type(write_data) is not str:
            _data = ujson.dumps(write_data, indent=4)
        else:
            _data = write_data

        dir_name, file_name = os.path.split(path)

        if check_integrity:
            if not file_name:
                raise RuntimeError(f"Safe_Save: No file name was found in {path}")

            temp_file_path = get_temp_dir() + "/" + file_name + ".tmp"
            i = 0
            while True:
                # Attempt to write to temp file
                with open(temp_file_path, "w", encoding="utf-8") as write_file:
                    write_file.write(_data)
                    write_file.flush()
                    os.fsync(write_file.fileno())

                # Read the entire file back in
                with open(temp_file_path, "r", encoding="utf-8") as read_file:
                    _read_data = read_file.read()

                if _data != _read_data:
                    i += 1
                    if i > max_attempts:
                        print(
                            f"Safe_Save ERROR: {file_name} was unable to properly save {i} times. Saving Failed."
                        )
                        raise RuntimeError(
                            f"Safe_Save: {file_name} was unable to properly save {i} times!"
                        )
                    print(
                        f"Safe_Save: {file_name} was incorrectly saved. Trying again."
                    )
                    continue

                # This section is reached is the file was not nullied. Move the file and return True

                shutil_move(temp_file_path, path)
                return
        else:
            os.makedirs(dir_name, exist_ok=True)
            with open(path, "w", encoding="utf-8") as write_file:
                write_file.write(_data)
                write_file.flush()
                os.fsync(write_file.fileno())

    def read_clans(self):
        """with open(get_save_dir() + '/clanlist.txt', 'r') as read_file:
            clan_list = read_file.read()
            if_clans = len(clan_list)
        if if_clans > 0:
            clan_list = clan_list.split('\n')
            clan_list = [i.strip() for i in clan_list if i]  # Remove empty and whitespace
            return clan_list
        else:
            return None"""
        # All of the above is old code
        # Now, we want clanlist.txt to contain ONLY the name of the Clan that is currently loaded
        # We will get the list of clans from the saves folder
        # each Clan has its own folder, and the name of the folder is the name of the clan
        # so we can just get a list of all the folders in the saves folder

        # First, we need to make sure the saves folder exists
        if not os.path.exists(get_save_dir()):
            os.makedirs(get_save_dir())
            print("Created saves folder")
            return None

        # Now we can get a list of all the folders in the saves folder
        clan_list = [f.name for f in os.scandir(get_save_dir()) if f.is_dir()]

        # the Clan specified in saves/clanlist.txt should be first in the list
        # so we can load it automatically

        if os.path.exists(get_save_dir() + "/clanlist.txt"):
            with open(get_save_dir() + "/clanlist.txt", "r", encoding="utf-8") as f:
                loaded_clan = f.read().strip().splitlines()
                if loaded_clan:
                    loaded_clan = loaded_clan[0]
                else:
                    loaded_clan = None
            os.remove(get_save_dir() + "/clanlist.txt")
            if loaded_clan:
                self.safe_save(get_save_dir() + "/currentclan.txt", loaded_clan)
        elif os.path.exists(get_save_dir() + "/currentclan.txt"):
            with open(get_save_dir() + "/currentclan.txt", "r", encoding="utf-8") as f:
                loaded_clan = f.read().strip()
        else:
            loaded_clan = None

        if loaded_clan and loaded_clan in clan_list:
            clan_list.remove(loaded_clan)
            clan_list.insert(0, loaded_clan)

        # Now we can return the list of clans
        if not clan_list:
            print("No clans found")
            return None
        return clan_list

    def save_clanlist(self, loaded_clan=None):
        """clans = []
        if loaded_clan:
            clans.append(f"{loaded_clan}\n")

        for clan_name in self.switches['clan_list']:
            if clan_name and clan_name != loaded_clan:
                clans.append(f"{clan_name}\n")

        if clans:
            with open(get_save_dir() + '/clanlist.txt', 'w') as f:
                f.writelines(clans)"""
        if loaded_clan:
            if os.path.exists(get_save_dir() + "/clanlist.txt"):
                # we don't need clanlist.txt anymore
                os.remove(get_save_dir() + "/clanlist.txt")
            game.safe_save(f"{get_save_dir()}/currentclan.txt", loaded_clan)
        else:
            if os.path.exists(get_save_dir() + "/currentclan.txt"):
                os.remove(get_save_dir() + "/currentclan.txt")

    def save_settings(self, currentscreen=None):
        """Save user settings for later use"""
        if os.path.exists(get_save_dir() + GAME_SETTINGS_FILENAME):
            os.remove(get_save_dir() + GAME_SETTINGS_FILENAME)

        self.settings_changed = False
        try:
            game.safe_save(get_save_dir() + GAME_SETTINGS_FILENAME, self.settings)
        except RuntimeError:
            from scripts._red.screens.windows import SaveError

            SaveError(traceback.format_exc())
            if currentscreen is not None:
                currentscreen.change_screen(MAIN_MENU_SCREEN_NAME)

    def load_settings(self):
        """Load settings that user has saved from previous use"""

        try:
            with open(
                get_save_dir() + "/settings.json", "r", encoding="utf-8"
            ) as read_file:
                settings_data = ujson.loads(read_file.read())
        except FileNotFoundError:
            return

        for key, value in settings_data.items():
            if key in self.settings:
                self.settings[key] = value

        self.switches["language"] = self.settings["language"]

    def switch_setting(self, setting_name):
        """Call this function to change a setting given in the parameter by one to the right on it's list"""
        self.settings_changed = True

        # Give the index that the list is currently at
        list_index = self.setting_lists[setting_name].index(self.settings[setting_name])

        if (
            list_index == len(self.setting_lists[setting_name]) - 1
        ):  # The option is at the list's end, go back to 0
            self.settings[setting_name] = self.setting_lists[setting_name][0]
        else:
            # Else move on to the next item on the list
            self.settings[setting_name] = self.setting_lists[setting_name][
                list_index + 1
            ]

    def save_cats(self):
        """Save the cat data."""

        clanname = ""
        """ if game.switches['clan_name'] != '':
            clanname = game.switches['clan_name']
        elif len(game.switches['clan_name']) > 0:
            clanname = game.switches['clan_list'][0]"""
        if game.clan_obj is not None:
            clanname = game.clan_obj.name
        directory = get_save_dir() + "/" + clanname
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Delete all existing relationship files
        if not os.path.exists(directory + "/relationships"):
            os.makedirs(directory + "/relationships")
        for f in os.listdir(directory + "/relationships"):
            os.remove(os.path.join(directory + "/relationships", f))

        self.save_faded_cats(clanname)  # Fades cat and saves them, if needed

        clan_cats = []
        for inter_cat in self.cat_class.all_cats.values():
            cat_data = inter_cat.get_save_dict()
            clan_cats.append(cat_data)

            inter_cat.save_condition()

            if inter_cat.history:
                inter_cat.save_history(directory + "/history")
                # after saving, dump the history info
                inter_cat.history = None
            if not inter_cat.dead:
                inter_cat.save_relationship_of_cat(directory + "/relationships")

        self.safe_save(f"{get_save_dir()}/{clanname}/clan_cats.json", clan_cats)

    def save_faded_cats(self, clanname):
        """Deals with fades cats, if needed, adding them as faded"""
        if game.cat_to_fade:
            directory = get_save_dir() + "/" + clanname + "/faded_cats"
            if not os.path.exists(directory):
                os.makedirs(directory)

        copy_of_info = ""
        for cat in game.cat_to_fade:
            inter_cat = self.cat_class.all_cats[cat]

            # Add ID to list of faded cats.
            self.clan_obj.faded_ids.append(cat)

            # If they have a mate, break it up
            if inter_cat.mate:
                for mate_id in inter_cat.mate:
                    if mate_id in self.cat_class.all_cats:
                        self.cat_class.all_cats[mate_id].unset_mate(inter_cat)

            # If they have parents, add them to their parents "faded offspring" list:
            for x in inter_cat.get_parents():
                if x in self.cat_class.all_cats:
                    self.cat_class.all_cats[x].faded_offspring.append(cat)
                else:
                    parent_faded = self.add_faded_offspring_to_faded_cat(x, cat)
                    if not parent_faded:
                        print(f"WARNING: Can't find parent {x} of {cat.name}")

            # Get a copy of info
            if game.clan_obj.clan_settings["save_faded_copy"]:
                copy_of_info += (
                    ujson.dumps(inter_cat.get_save_dict(), indent=4)
                    + "\n--------------------------------------------------------------------------\n"
                )

            # SAVE TO IT'S OWN LITTLE FILE. This is a trimmed-down version for relation keeping only.
            cat_data = inter_cat.get_save_dict(faded=True)

            self.safe_save(
                f"{get_save_dir()}/{clanname}/faded_cats/{cat}.json", cat_data
            )

            # Remove the cat from the active cats lists
            self.clan_obj.remove_cat(cat)

        game.cat_to_fade = []

        # Save the copies, flush the file.
        if game.clan_obj.clan_settings["save_faded_copy"]:
            with open(
                get_save_dir() + "/" + clanname + "/faded_cats_info_copy.txt",
                "a",
                encoding="utf-8",
            ) as write_file:
                if not os.path.exists(
                    get_save_dir() + "/" + clanname + "/faded_cats_info_copy.txt"
                ):
                    # Create the file if it doesn't exist
                    with open(
                        get_save_dir() + "/" + clanname + "/faded_cats_info_copy.txt",
                        "w",
                        encoding="utf-8",
                    ) as create_file:
                        pass

                with open(
                    get_save_dir() + "/" + clanname + "/faded_cats_info_copy.txt",
                    "a",
                    encoding="utf-8",
                ) as write_file:
                    write_file.write(copy_of_info)

                    write_file.flush()
                    os.fsync(write_file.fileno())

    def save_events(self):
        """
        Save current events list to events.json
        """
        events_list = []
        for event in game.cur_events_list:
            events_list.append(event.to_dict())
        game.safe_save(f"{get_save_dir()}/{game.clan_obj.name}/events.json", events_list)

    def add_faded_offspring_to_faded_cat(self, parent, offspring):
        """In order to siblings to work correctly, and not to lose relation info on fading, we have to keep track of
        both active and faded cat's faded offpsring. This will add a faded offspring to a faded parents file.
        """
        try:
            with open(
                get_save_dir()
                + "/"
                + self.clan_obj.name
                + "/faded_cats/"
                + parent
                + ".json",
                "r",
                encoding="utf-8",
            ) as read_file:
                cat_info = ujson.loads(read_file.read())
        except:
            print("ERROR: loading faded cat")
            return False

        cat_info["faded_offspring"].append(offspring)

        self.safe_save(
            f"{get_save_dir()}/{self.clan_obj.name}/faded_cats/{parent}.json", cat_info
        )

        return True

    def load_events(self):
        """
        Load events from events.json and place into game.cur_events_list.
        """

        clanname = self.clan_obj.name
        events_path = f"{get_save_dir()}/{clanname}/events.json"
        events_list = []
        try:
            with open(events_path, "r", encoding="utf-8") as f:
                events_list = ujson.loads(f.read())
            for event_dict in events_list:
                event_obj = Single_Event.from_dict(event_dict, game.cat_class)
                if event_obj:
                    game.cur_events_list.append(event_obj)
        except FileNotFoundError:
            pass


########################################################################################################################
# Object creation
########################################################################################################################

game: Game = Game()
