# io_utils.py - I/O utility methods and classes.

# -------------------------------------------------------------------------------- #
# ----------------------------------------

########################################################################################################################
# Imports
########################################################################################################################

# this prevents other modules importing anything but the global object 'io_manager'
#   at the bottom of this file without specifically trying to
__all__ = ['io_manager']

import os
import json
from typing import Optional

import yaml
import tomllib

import definitions
from scripts._red.red_exceptions import InitializationError, InvalidSaveError, InvalidFileTypeError
from scripts.housekeeping.datadir import get_resources_dir, get_save_dir

import logging
logger = logging.getLogger(__name__)


########################################################################################################################
# Constants
########################################################################################################################

FILENAMES: dict = {

    # settings paths - these are in saves/
    "current_clan_file": "currentclan.txt",
    "game_settings": "settings.yaml",
    "clan_settings": "clan_settings.yaml",

    # save paths - these are in saves/{clan_prefix}/
    "clan_details": "Clan.yaml",
    "save_camp": "camp.yaml",
    "save_conditions": "conditions.yaml",
    "save_relationships": "relationships.yaml",
    "last_moon_events": "last_moon_events.yaml",
    "ongoing_events": "ongoing_events/",
    "ongoing_event_file": "_moons.yaml",
    "cats": "cats/",
    "faded_cats_info": "faded_cats_info_copy.txt",

    # resources
    "music": "resources/audio/music/",
    "sounds": "resources/audio/sounds/",
    "conversion_dict": "resources/dicts/conversion_dict.json",
    "cat_name": "resources/_red/cat_names.en.yaml",
    "clan_name": "resources/_red/clan_names.en.yaml",
}


########################################################################################################################
# Classes
########################################################################################################################

class IOManager:
    """ Class which the game should use to interact with system files. """

    # game settings
    game_settings_filepath: str = get_save_dir() + definitions.GAME_SETTINGS_FILENAME
    active_clan_prefix: Optional[str]

    # filepaths used when loading a save
    current_clan_file_filepath: str = get_save_dir() + definitions.CURRENTCLAN_FILENAME
    active_clan_save_folder_filepath: Optional[str]
    clan_settings_filepath: Optional[str]
    clan_details_filepath: Optional[str]
    camp_filepath: Optional[str]
    conditions_filepath: Optional[str]
    relationships_filepath: Optional[str]
    current_moon_events_filepath: Optional[str]
    ongoing_events_dirpath: Optional[str]
    clan_cats_dirpath: Optional[str]
    outsider_clan_filepath: Optional[str]
    df_cats_filepath: Optional[str]
    sc_cats_filepath: Optional[str]
    ur_cats_filepath: Optional[str]
    # don't load faded cats' info

    # resources

    # ------------------------------------- INIT ------------------------------------- #

    def _ready_to_go(self):
        """ Check if all  initialization has finished and make sure there's an active Clan chosen. """
        ready_to_go: bool = True
        if not self.active_clan_prefix:
            ready_to_go = False
        if not self.active_clan_save_folder_filepath:
            ready_to_go = False
        if not ready_to_go:
            raise InitializationError(f"I/O manager hasn't been fully initialized yet")
        return

    # ------------------------------- LAST PLAYED CLAN ------------------------------- #

    def get_last_played_clan_prefix(self):
        if os.path.exists(self.current_clan_file_filepath):
            clan_prefix: str = self._read_file(filepath=self.current_clan_file_filepath)
            return clan_prefix
        else:
            return None

    def update_active_clan_prefix(self, new_active_clan_prefix: Optional[str]):
        """ Set the current Clan's name so the correct save files will be read.

        Called by the game.update_active_clan_prefix_everywhere() ONLY.
        """
        # make sure you aren't trying to switch to the Clan you're already using
        if new_active_clan_prefix.casefold() == self.active_clan_prefix:
            logger.warning(f"Can't switch to the save that's already active: tried to switch from save "
                           f"'{self.active_clan_prefix}' to save '{new_active_clan_prefix}' in IOManager")
        else:
            self._set_current_clan_filepaths(clan_prefix=new_active_clan_prefix)
        return

    def _set_current_clan_filepaths(self, clan_prefix = None):
        """ Set the save file's file paths for the next time anything needs to be loaded. """
        if clan_prefix is None:
            self.active_clan_save_folder_filepath = None
            self.clan_details_filepath = None
            self.camp_filepath = None
            self.clan_settings_filepath = None
            self.conditions_filepath = None
            self.relationships_filepath = None
            self.current_moon_events_filepath = None
            self.ongoing_events_dirpath = None
            self.clan_cats_dirpath = None
            self.outsider_clan_filepath = None
            self.df_cats_filepath = None
            self.sc_cats_filepath = None
            self.ur_cats_filepath = None

        else:
            # files and directories in saves/
            self.active_clan_save_folder_filepath = get_save_dir() + self.active_clan_prefix + "/"
            self.clan_details_filepath = get_save_dir() + definitions.SAVE_CLAN_DETAILS_FILENAME
            self.clan_details_filepath.replace(f"*", self.active_clan_prefix)

            # files and directories in saves/{clan_prefix}/
            self.camp_filepath = self.active_clan_save_folder_filepath + definitions.SAVE_CAMP_FILENAME
            self.clan_settings_filepath = (self.active_clan_save_folder_filepath +
                                           definitions.SAVE_CLAN_SETTINGS_FILENAME)
            self.conditions_filepath = self.active_clan_save_folder_filepath + definitions.SAVE_CONDITIONS_FILENAME
            self.relationships_filepath = (self.active_clan_save_folder_filepath +
                                           definitions.SAVE_RELATIONSHIPS_FILENAME)
            self.current_moon_events_filepath = (self.active_clan_save_folder_filepath +
                                                 definitions.SAVE_CURRENT_MOON_EVENTS_FILENAME)
            self.ongoing_events_dirpath = self.active_clan_save_folder_filepath + definitions.ONGOING_EVENTS_DIR
            self.clan_cats_dirpath = self.active_clan_save_folder_filepath + definitions.CLAN_CATS_DIR

            # files in saves/{clan_prefix}/cats/
            self.outsider_clan_filepath = self.clan_cats_dirpath + definitions.OUTSIDER_CLAN_PREFIX + ".yaml"
            self.df_cats_filepath = self.clan_cats_dirpath + definitions.Location.DarkForest + ".yaml"
            self.sc_cats_filepath = self.clan_cats_dirpath + definitions.Location.StarClan + ".yaml"
            self.ur_cats_filepath = self.clan_cats_dirpath + definitions.Location.OutsiderAfterlife + ".yaml"

            # finally, make sure the requested Clan is a valid save file and reset all the file paths if it isn't
            valid_saves, invalid_saves = self.get_valid_save_names()
            if clan_prefix not in valid_saves:
                raise InvalidSaveError(f"Couldn't find the save file {clan_prefix} in "
                                       f"the list of valid Clan names: {valid_saves}")

        return

    # ---------------------------------- VALIDATION ---------------------------------- #
    # if only I could find this...

    def get_valid_save_names(self) -> tuple[list, list]:
        """ Fetch the names of save files present in the saves/ directory. """
        valid_saves: list = []
        invalid_saves: list = []

        # first make sure the "saves/" folder exists
        if not os.path.exists(get_save_dir()):
            os.makedirs(get_save_dir())
            logger.info("No saves folder existed. Created empty saves folder")

        else:
            for clan_prefix in [f.name for f in list(os.scandir(get_save_dir())) if f.is_dir()]:
                if self.check_save_validity(clan_prefix=clan_prefix):
                    valid_saves.append(clan_prefix)
                else:
                    invalid_saves.append(clan_prefix)

        return valid_saves, invalid_saves

    def check_save_validity(self, clan_prefix: str) -> bool:
        """ Check if a save file is valid to play. """

        # was the method passed a valid clan prefix
        if not isinstance(clan_prefix, str):
            logger.error(f"Parameter clan_prefix needs to be a string but was a {type(clan_prefix)}")
            return False

        # does a save folder "saves/Sky/" have a corresponding Clan details file "saves/SkyClan.yaml"
        if not os.path.exists(self.clan_details_filepath):
            logger.debug(f"{clan_prefix} save is missing expected file '{self.clan_details_filepath}'")
            return False

        # TWO-PART TEST: does the save folder contain everything it should
        save_folder_contents: list = list( os.scandir(self.active_clan_save_folder_filepath) )
        folders: list = [f.name for f in save_folder_contents if f.is_dir()]
        files: list = [f.name for f in save_folder_contents if f.is_file()]

        # PART ONE: does the save folder contain all the required subfolders
        expected_folders: list = [self.ongoing_events_dirpath, self.clan_cats_dirpath]
        for folder in folders:
            if folder in expected_folders:
                expected_folders.remove(folder)
        if expected_folders:
            logger.debug(f"Couldn't find expected save file folder(s): {expected_folders}")
            return False

        # PART TWO: does the save folder "Example/" contain all the required save files
        expected_files: list = [
            self.clan_details_filepath, self.clan_settings_filepath, self.camp_filepath, self.conditions_filepath,
            self.relationships_filepath, self.current_moon_events_filepath, self.outsider_clan_filepath,
            self.df_cats_filepath, self.sc_cats_filepath, self.ur_cats_filepath
        ]
        for file in files:
            if file in expected_files:
                expected_files.remove(file)
        if expected_files:
            logger.debug(f"Couldn't find expected save folder file(s): {expected_files}")
            return False

        return True

    # -------------------------------- PUBLIC READER --------------------------------- #

    def read_game_settings_file(self) -> dict:
        """ Read the file where the game settings are saved. """
        # make sure the game settings file exists before trying to read it
        self._ready_to_go()
        if not os.path.exists(self.game_settings_filepath):
            logger.warning(f"Game settings file doesn't exist! You need to save a copy of them right away")
            self._write_file(filepath=self.game_settings_filepath, data="")

        return self._read_file(self.game_settings_filepath)

    def read_clan_settings_file(self) -> dict:
        """ Read the current save's file where the Clan-specific settings are loaded. """
        self._ready_to_go()
        return self._read_file(self.clan_settings_filepath)

    def read_cats_files(self) -> dict:
        """ Read the current save's files containing details about cats. """
        logger.debug(f"Reading Clan settings file for save '{self.active_clan_prefix}'")
        self._ready_to_go()
        cats_dir_path: str = self.active_clan_save_folder_filepath + definitions.CLAN_CATS_DIR
        cats_per_clan: dict = {}
        for filename in os.scandir(cats_dir_path):
            filename: str = str(filename).split("'")[1]
            filepath: str = cats_dir_path + filename
            if filename == definitions.FADED_CATS_INFO_FILENAME:
                pass # don't load up faded cats info
            # afterlives
            elif definitions.Location.StarClan in filename:
                cats_per_clan[definitions.Location.StarClan.value] = self._read_file(filepath=filepath)
            elif definitions.Location.DarkForest in filename:
                cats_per_clan[definitions.Location.DarkForest.value] = self._read_file(filepath=filepath)
            elif definitions.Location.OutsiderAfterlife in filename:
                cats_per_clan[definitions.Location.OutsiderAfterlife.value] = self._read_file(filepath=filepath)
            # outsiders
            elif definitions.OUTSIDER_CLAN_PREFIX in filename:
                cats_per_clan[definitions.OUTSIDER_CLAN_PREFIX] = self._read_file(filepath=filepath)
            # warrior clans
            else:
                clan_prefix = filename.split(".")[0]
                cats_per_clan[clan_prefix] = self._read_file(filepath=filepath)
        return cats_per_clan

    def read_clan_details_file(self) -> dict:
        """ Read the current save's file where details about the Clans in the save file are stored. """
        logger.debug(f"Reading Clan details file for save '{self.active_clan_prefix}'")
        self._ready_to_go()
        return self._read_file(self.clan_details_filepath)

    def read_camp_save_file(self) -> dict:
        """ Read the current save's file where details about the Clan's camp are stored. """
        logger.debug(f"Reading camp file for save '{self.active_clan_prefix}'")
        self._ready_to_go()
        return self._read_file(self.camp_filepath)

    def read_conditions_save_file(self) -> dict:
        """ Read the current save's file where the health conditions of cats are stored. """
        logger.debug(f"Reading conditions file for save '{self.active_clan_prefix}'")
        self._ready_to_go()
        return self._read_file(self.conditions_filepath)

    def read_relationships_save_file(self) -> dict:
        """ Read the current save's file where the relationship values are stored. """
        logger.debug(f"Reading relationships file for save '{self.active_clan_prefix}'")
        self._ready_to_go()
        return self._read_file(self.relationships_filepath)

    def read_current_moon_events_file(self) -> dict:
        """ Read the current moon's events from the current save file. """
        logger.debug(f"Reading current moon events file for save '{self.active_clan_prefix}'")
        self._ready_to_go()
        return self._read_file(self.current_moon_events_filepath)

    def read_ongoing_events_files(self) -> dict:
        """ Read the ongoing events from the current save file. """
        logger.debug(f"Reading ongoing events for save '{self.active_clan_prefix}'")
        self._ready_to_go()

        ongoing_events: dict = {}
        dir_contents = os.scandir(self.ongoing_events_dirpath)
        for filename in dir_contents:
            filename = str(filename)
            time_until: int = int(filename[0])
            filepath: str = self.ongoing_events_dirpath + filename
            events: list = self._read_file(filepath=filepath)
            ongoing_events[time_until] = events

        return ongoing_events

    # -------------------------------- PUBLIC WRITER --------------------------------- #
a
    def write_game_settings_file(self, game_settings) -> bool:
        """ Save the current game settings to file. """
        self._ready_to_go()
        return self._write_file(filepath=self.game_settings_filepath, data=game_settings)

    def write_clan_settings_file(self, clan_settings) -> bool:
        """ Save the current save file's settings to file. """
        self._ready_to_go()
        return self._write_file(filepath=self.clan_settings_filepath, data=clan_settings)

    # TODO
    def write_cats_files(self, cats) -> bool:
        """ Save the current save file's RedCat objects to file. """
        self._ready_to_go()
        raise NotImplementedError("IOManager.write_cats_files")

    # TODO
    def write_clan_details_files(self, clan_details) -> bool:
        """ Save the current save file's Clan details to file. """
        self._ready_to_go()
        raise NotImplementedError("IOManager.write_clan_details_files")

    # TODO
    def write_camp_file(self, camp) -> bool:
        """ Save the current save file's camp details to file. """
        self._ready_to_go()
        raise NotImplementedError("IOManager.write_camp_file")

    # TODO
    def write_conditions_file(self, conditions) -> bool:
        """ Save the current save file's conditions to file. """
        self._ready_to_go()
        raise NotImplementedError("IOManager.write_conditions_file")

    def write_relationships_save_file(self, cat_relationships, clan_relationships) -> bool:
        """ Save the current relationship values. """
        self._ready_to_go()
        return self._write_file(filepath=self.relationships_filepath,
                                data={"cats": cat_relationships, "clans": clan_relationships})

    # TODO
    def write_current_moon_events_file(self, current_moon_events) -> bool:
        """ Save the current save file's current moon events to file. """
        self._ready_to_go()
        raise NotImplementedError("IOManager.write_current_moon_events_file")

    # TODO
    def write_ongoing_events_files(self, ongoing_events: dict) -> bool:
        """ Save the current save file's ongoing events to file.

        :param dict ongoing_events: each key should be how many moons until an event happens,
            and each value should be TODO
        """
        self._ready_to_go()
        raise NotImplementedError("IOManager.write_ongoing_events_files")

    # -------------------------------- PRIVATE READER -------------------------------- #

    def _read_file(self, filepath: str) -> list | dict | str:
        """ Read a file. This method exists to catch requests to read invalid file types. """
        # replace accidental //s with /s
        filepath = filepath.replace("//", "/")
        # find
        filetype = filepath.split(".")[-1] # "shark/shark/blahaj.txt" -> ["shark/shark/blahaj", "txt"] -> "txt"
        if filetype.casefold() in ("json", ):
            return self._read_json(filepath)
        if filetype.casefold() in ("yaml", "yml"):
            return self._read_yaml(filepath)
        if filetype.casefold() in ("toml"):
            return self._read_toml(filepath)
        if filetype.casefold() in ("text", "txt"):
            return self._read_text(filepath)
        # was asked to read an invalid file type
        raise ValueError(f"Was asked to read the following file: '{filepath}' but can only read the "
                         f"following file types: .json, .yaml, .yml, .toml, .tml, .text, .txt")

    @staticmethod
    def _read_json(filepath: str) -> dict:
        """ Read a JSON file.

        :param str filepath: JSON file to read from.
        :return dict: the contents as a Python object.
        :raises Exception: if the read fails
        """
        try:
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    result = json.loads(f.read())
                    return result
            else:
                raise ValueError(f"Can't read from file {filepath} because it doesn't exist")
        except Exception as e:
            logger.exception(e)
            logger.exception(f"Couldn't read from file {filepath}")
            raise

    @staticmethod
    def _read_yaml(filepath: str) -> dict:
        """ Read a .yml or .yaml file.

        :param str filepath: YAML file to read from.
        :return: the contents as a Python object.
        :raises Exception: if the read fails
        """
        try:
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as reader:
                    result = yaml.safe_load(reader.read())
                    return result
            else:
                raise ValueError(f"Can't read from file {filepath} because it doesn't exist")
        except Exception as e:
            logger.exception(f"Couldn't read from file {filepath}", e)
            raise

    @staticmethod
    def _read_toml(filepath: str) -> dict:
        """ Read a .toml file.

        :param str filepath: TOML file to read from.
        :return: the contents as a Python object.
        :raises Exception: if the read fails
        """
        try:
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as reader:
                    result = tomllib.loads(reader.read())
                    return result
            else:
                raise ValueError(f"Can't read from file {filepath} because it doesn't exist")
        except Exception as e:
            logger.exception(f"Couldn't read from file {filepath}", e)
            raise

    @staticmethod
    def _read_text(filepath: str):
        """ Read a .txt file.

        :param str filepath: text file to read from.
        :return: the contents as a Python object.
        :raises Exception: if the read fails
        """
        try:
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as reader:
                    result = reader.read()
                    return result
            else:
                raise ValueError(f"Can't read from file {filepath} because it doesn't exist")
        except Exception as e:
            logger.exception(f"Couldn't read from file {filepath}", e)
            raise

    # -------------------------------- PRIVATE WRITER -------------------------------- #

    @staticmethod
    def _write_file(filepath: str, data) -> bool:
        """ Write a YAML file.

        :param str filepath: the complete path to the file that should be written to.
        :param data: a dictionary or string to write to the file.
        :return bool: True if the write was successful, False otherwise.
        """
        logger.debug(f"Attempting write to file: {filepath}")

        # make sure the filepath is formatted correctly
        filepath: str = filepath.replace("//", "/")
        filepath_elements: list[str] = filepath.split('/')

        # only write YAML files
        filename = filepath_elements.pop(-1).lower()
        if filename[-5:] != ".yaml" and filename[-4:] != ".yml":
            raise InvalidFileTypeError(f"Can only write .yaml or .yml files but was asked to write to {filename}")

        # make sure the file's directory exists
        dir_name: str = ""
        for _ in filepath_elements:
            dir_name += f"{_}/"

        # finally, actually try to write the file
        try:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name, exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(yaml.dump(data))
                f.flush()
                os.fsync(f.fileno())
        except Exception as e:
            logger.exception(e)
            logger.exception(f"Couldn't write to file {filepath}")
            return False
        else:
            return True


########################################################################################################################
# Object creation
########################################################################################################################

# use this object instead of importing the class and creating a new instance to prevent read and/or write races
io_manager = IOManager()