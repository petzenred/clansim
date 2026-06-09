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
import platform
import subprocess
from pathlib import Path
from typing import Optional

import yaml
import tomllib

import definitions
import resources._red.red_filepaths as fp
from scripts._red.red_exceptions import InitializationError, InvalidSaveError, InvalidFileTypeError
from scripts.housekeeping.datadir import get_resources_dir, get_save_dir

import logging
logger = logging.getLogger(__name__)


########################################################################################################################
# Classes
########################################################################################################################

class IOManager:
    """ Class which the game should use to interact with system files. """

    # game settings
    game_settings_path: Path = fp.GAME_SETTINGS_FILEPATH
    active_clan_token: Optional[str] = None

    # filepaths used when loading a save
    current_clan_file_path: Path = fp.CURRENTCLAN_FILE_PATH
    active_clan_save_folder_filepath: Optional[Path] = None
    save_version_filepath: Optional[Path] = None

    clan_settings_filepath: Optional[Path] = None
    camp_filepath: Optional[Path] = None
    clans_info_filepath: Optional[Path] = None
    conditions_filepath: Optional[Path] = None
    relationships_filepath: Optional[Path] = None
    current_moon_events_filepath: Optional[Path] = None
    ongoing_events_dirpath: Optional[Path] = None
    clan_cats_dirpath: Optional[Path] = None
    outsider_clan_filepath: Optional[Path] = None
    df_cats_filepath: Optional[Path] = None
    sc_cats_filepath: Optional[Path] = None
    ur_cats_filepath: Optional[Path] = None
    # don't load faded cats' info

    # resources

    def _ready_to_go(self) -> bool:
        """ Check if all  initialization has finished and make sure there's an active Clan chosen. """
        ready_f: bool = True
        if not self.active_clan_token:
            ready_f = False
        if not self.active_clan_save_folder_filepath:
            ready_f = False
        if not ready_f:
            raise InitializationError(f"I/O manager hasn't been fully initialized yet")
        return ready_f

    # ------------------------------- LAST PLAYED CLAN ------------------------------- #

    def get_last_played_clan_token(self) -> str:
        # We want currentclan.txt to contain ONLY the name of the Clan that is currently loaded.
        # We will get the list of clans from the saves folder each Clan has its own folder,
        # and the name of the folder is the name of the clan so we can just get a list of all
        # the folders in the saves folder.
        if os.path.exists(self.current_clan_file_path):
            clan_token: str = self.read_file(filepath=self.current_clan_file_path)
            return clan_token
        else:
            return None

    def update_active_clan_token(self, new_active_clan_token: Optional[str]):
        """ Set the current Clan's name so the correct save files will be read.

        Called by the game.update_active_clan_token_everywhere() ONLY.
        """
        # make sure you aren't trying to switch to the Clan you're already using
        if new_active_clan_token and new_active_clan_token.casefold() == self.active_clan_token:
            logger.warning(f"Can't switch to the save that's already active: tried to switch from save "
                           f"'{self.active_clan_token}' to save '{new_active_clan_token}' in IOManager")
        else:
            self.active_clan_token = new_active_clan_token
            self._set_current_clan_filepaths(clan_token=new_active_clan_token)
        return

    def _set_current_clan_filepaths(self, clan_token = None):
        """ Set the save file's file paths for the next time anything needs to be loaded. """

        logger.debug(f"IOManager._set_current_clan_filepaths: {clan_token}")

        if clan_token is None:
            self.active_clan_save_folder_filepath = None
            self.save_version_filepath = None

            self.clan_settings_filepath = None
            self.camp_filepath = None
            self.clans_info_filepath = None
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
            self.active_clan_save_folder_filepath = Path(get_save_dir(), self.active_clan_token)

            # files and directories in saves/{clan_token}/
            self.save_version_filepath = Path(self.active_clan_save_folder_filepath,
                                              definitions.SAVE_VERSION_FILENAME)
            self.camp_filepath = Path(self.active_clan_save_folder_filepath,
                                      definitions.SAVE_CAMP_FILENAME)
            self.clan_settings_filepath = Path(self.active_clan_save_folder_filepath,
                                           definitions.SAVE_CLAN_SETTINGS_FILENAME)
            self.clans_info_filepath = Path(self.active_clan_save_folder_filepath,
                                            definitions.SAVE_CLANS_INFO_FILENAME)
            self.conditions_filepath = Path(self.active_clan_save_folder_filepath,
                                            definitions.SAVE_CONDITIONS_FILENAME)
            self.relationships_filepath = Path(self.active_clan_save_folder_filepath,
                                           definitions.SAVE_RELATIONSHIPS_FILENAME)
            self.current_moon_events_filepath = Path(self.active_clan_save_folder_filepath,
                                                 definitions.SAVE_CURRENT_MOON_EVENTS_FILENAME)
            self.ongoing_events_dirpath = Path(self.active_clan_save_folder_filepath,
                                               definitions.ONGOING_EVENTS_DIR)
            self.clan_cats_dirpath = Path(self.active_clan_save_folder_filepath,
                                          definitions.CLAN_CATS_DIR)

            # files in saves/{clan_token}/cats/
            self.outsider_clan_filepath = Path(self.clan_cats_dirpath, definitions.LONER_CLAN_TOKEN+ ".yaml")
            self.df_cats_filepath = Path(self.clan_cats_dirpath, definitions.DF_CLAN_TOKEN + ".yaml")
            self.sc_cats_filepath = Path(self.clan_cats_dirpath, definitions.STAR_CLAN_TOKEN+ ".yaml")
            self.ur_cats_filepath = Path(self.clan_cats_dirpath, definitions.UR_CLAN_TOKEN+ ".yaml")

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
            logger.warning("No saves folder existed. Created empty saves folder")

        else:
            for clan_token in [f.name for f in list(os.scandir(get_save_dir())) if f.is_dir()]:
                if self._check_save_validity(clan_token=clan_token):
                    valid_saves.append(clan_token)
                else:
                    invalid_saves.append(clan_token)

        return valid_saves, invalid_saves

    def _check_save_validity(self, clan_token: str) -> bool:
        """ Check if a save file is valid to play. """
        # was the method passed a valid clan token
        if not isinstance(clan_token, str):
            logger.error(f"Parameter clan_token needs to be a string but was a {type(clan_token)}")
            return False

        # TWO-PART TEST: does the save folder contain everything it should
        save_folder_path = Path(get_save_dir(), clan_token)
        save_folder_contents: list = list( os.scandir(save_folder_path) )
        folders: list = [f.name for f in save_folder_contents if f.is_dir()]
        files: list = [f.name for f in save_folder_contents if f.is_file()]

        # PART ONE: does the save folder contain all the required subfolders
        expected_folders: list = [definitions.ONGOING_EVENTS_DIR, definitions.CLAN_CATS_DIR]
        for folder in folders:
            if folder in expected_folders:
                expected_folders.remove(folder)
        if expected_folders:
            logger.debug(f"Found unexpected save folder(s) in save with token {clan_token}: {expected_folders}")
            return False

        # PART TWO: does the save folder "Example/" contain all the required save files
        expected_files: list = [
            definitions.SAVE_VERSION_FILENAME, definitions.SAVE_CLANS_INFO_FILENAME, definitions.SAVE_CAMP_FILENAME,
            definitions.SAVE_CLAN_SETTINGS_FILENAME, definitions.SAVE_CONDITIONS_FILENAME,
            definitions.SAVE_RELATIONSHIPS_FILENAME, definitions.SAVE_CURRENT_MOON_EVENTS_FILENAME,
        ]
        for file in files:
            if file in expected_files:
                expected_files.remove(file)
        if expected_files:
            logger.debug(f"Found unexpected save file(s): {expected_files}")
            return False

        return True

    # -------------------------------- PUBLIC READER --------------------------------- #

    def read_game_settings_file(self) -> dict:
        """ Read the file where the game settings are saved. """
        # doesn't use _ready_to_go() because it happens before that

        # make sure the game settings file exists before trying to read it
        if not os.path.exists(self.game_settings_path):
            logger.warning(f"Game settings file doesn't exist! You need to save a copy of them right away")
            self._write_file(filepath=self.game_settings_path, data="")

        return self.read_file(self.game_settings_path)

    def read_save_version_file(self) -> dict:
        """ Read the file where the game's and the save's version sare saved. """
        logger.debug(f"Reading save version file for save '{self.active_clan_token}'")
        self._ready_to_go()
        return self.read_file(self.save_version_filepath)

    def read_clan_settings_file(self) -> dict:
        """ Read the current save's file where the Clan-specific settings are loaded. """
        self._ready_to_go()
        return self.read_file(self.clan_settings_filepath)

    def read_cats_files(self) -> dict:
        """ Read the current save's files containing details about cats. """
        logger.debug(f"Reading Clan settings file for save '{self.active_clan_token}'")
        self._ready_to_go()
        cats_dir_path: Path = Path(self.active_clan_save_folder_filepath, definitions.CLAN_CATS_DIR)
        cats_per_clan: dict = {}
        for filename in os.scandir(cats_dir_path):
            filename: str = str(filename).split("'")[1]
            filepath: Path = Path(cats_dir_path, filename)

            if filename != definitions.FADED_CATS_INFO_FILENAME:
                clan_token = filename.split(".")[0]
                cats_per_clan[clan_token] = self.read_file(filepath=filepath)
            # if filename == definitions.FADED_CATS_INFO_FILENAME:
            #     pass # don't load up faded cats info
            # # afterlives
            # elif definitions.Location.StarClan in filename:
            #     cats_per_clan[definitions.Location.StarClan.value] = self._read_file(filepath=filepath)
            # elif definitions.Location.DarkForest in filename:
            #     cats_per_clan[definitions.Location.DarkForest.value] = self._read_file(filepath=filepath)
            # elif definitions.Location.OutsiderAfterlife in filename:
            #     cats_per_clan[definitions.Location.OutsiderAfterlife.value] = self._read_file(filepath=filepath)
            # # outsiders
            # elif definitions.LONER_CLAN_TOKEN in filename:
            #     cats_per_clan[definitions.LONER_CLAN_TOKEN] = self._read_file(filepath=filepath)
            # # warrior clans
            # else:
            #     clan_token = filename.split(".")[0]
            #     cats_per_clan[clan_token] = self._read_file(filepath=filepath)
        return cats_per_clan

    def read_save_details_file(self) -> dict:
        """ Read the current save's file where details about the game file are stored. """
        logger.debug(f"Reading save details file for save '{self.active_clan_token}'")
        self._ready_to_go()
        return self.read_file(self.save_version_filepath)

    def read_clan_info_file(self) -> dict:
        """ Read the current save's file where details about the Clans in the save file are stored. """
        logger.debug(f"Reading Clans info file for save '{self.active_clan_token}'")
        self._ready_to_go()
        return self.read_file(self.clans_info_filepath)

    def read_camp_save_file(self) -> dict:
        """ Read the current save's file where details about the Clan's camp are stored. """
        logger.debug(f"Reading camp file for save '{self.active_clan_token}'")
        self._ready_to_go()
        return self.read_file(self.camp_filepath)

    def read_conditions_save_file(self) -> dict:
        """ Read the current save's file where the health conditions of cats are stored. """
        logger.debug(f"Reading conditions file for save '{self.active_clan_token}'")
        self._ready_to_go()
        return self.read_file(self.conditions_filepath)

    def read_relationships_save_file(self) -> dict:
        """ Read the current save's file where the relationship values are stored. """
        logger.debug(f"Reading relationships file for save '{self.active_clan_token}'")
        self._ready_to_go()
        return self.read_file(self.relationships_filepath)

    def read_current_moon_events_file(self) -> dict:
        """ Read the current moon's events from the current save file. """
        logger.debug(f"Reading current moon events file for save '{self.active_clan_token}'")
        self._ready_to_go()
        return self.read_file(self.current_moon_events_filepath)

    def read_ongoing_events_files(self) -> dict:
        """ Read the ongoing events from the current save file. """
        logger.debug(f"Reading ongoing events for save '{self.active_clan_token}'")
        self._ready_to_go()

        ongoing_events: dict = {}
        dir_contents = os.scandir(self.ongoing_events_dirpath)
        for filename in dir_contents:
            filename = str(filename)
            time_until: int = int(filename[0])
            filepath: str = self.ongoing_events_dirpath + filename
            events: list = self.read_file(filepath=filepath)
            ongoing_events[time_until] = events

        return ongoing_events

    # -------------------------------- PUBLIC WRITER --------------------------------- #

    def write_game_settings_file(self, game_settings) -> bool:
        """ Save the current game settings to file. """
        self._ready_to_go()
        return self._write_file(filepath=self.game_settings_path, data=game_settings)

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
    def write_clans_info_files(self, clan_details) -> bool:
        """ Save the current save file's details about all Clans to file. """
        self._ready_to_go()
        raise NotImplementedError("IOManager.write_clans_info_files")

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

    def read_file(self, filepath: Path) -> list | dict | str:
        """ Read a file. This method exists to catch requests to read invalid file types. """
        # find
        filename, filetype = os.path.splitext(filepath)
        # filetype = filepath.split(".")[-1] # "shark/shark/blahaj.txt" -> ["shark/shark/blahaj", "txt"] -> "txt"
        if filetype.casefold() in (".json", ):
            return self._read_json(filepath)
        if filetype.casefold() in (".yaml", ".yml", ):
            return self._read_yaml(filepath)
        if filetype.casefold() in (".toml", ):
            return self._read_toml(filepath)
        if filetype.casefold() in (".text", ".txt", ):
            return self._read_text(filepath)
        # was asked to read an invalid file type
        raise ValueError(f"Was asked to read the following file: '{filepath}' but can only read the "
                         f"following file types: .json, .yaml, .yml, .toml, .tml, .text, .txt")

    @staticmethod
    def _read_json(filepath: Path) -> dict:
        """ Read a JSON file.

        :param Path filepath: JSON file to read from.
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
    def _read_yaml(filepath: Path) -> dict:
        """ Read a .yml or .yaml file.

        :param Path filepath: YAML file to read from.
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
    def _read_toml(filepath: Path) -> dict:
        """ Read a .toml file.

        :param Path filepath: TOML file to read from.
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
    def _read_text(filepath: Path):
        """ Read a .txt file.

        :param Path filepath: text file to read from.
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
    def _write_file(filepath: Path, data) -> bool:
        """ Write a YAML file.

        :param Path filepath: the complete path to the file that should be written to.
        :param data: a dictionary or string to write to the file.
        :return bool: True if the write was successful, False otherwise.
        """
        logger.debug(f"Attempting write to file: {filepath}")

        # make sure the filepath is formatted correctly
        dirpath, file = os.path.split(filepath)
        rootpath, filetype = os.path.splitext(filepath)

        # we only write YAML files in this house
        if filetype not in (".yaml", ".yml"):
            raise InvalidFileTypeError(f"Can only write .yaml or .yml files but was asked to write \"{file}\"")

        try:
            # make sure the file's directory exists
            if not os.path.exists(dirpath):
                os.makedirs(dirpath, exist_ok=True)
            # finally, actually try to write the file
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

    # ------------------------------ OPEN EXTERNAL LINK ------------------------------ #

    def open_external_link(self, link_target):
        platform_system: str = platform.system()
        if platform_system == "Darwin":
            subprocess.Popen(["open", "-u", link_target])
        elif platform_system == "Windows":
            os.system(f'start "" {link_target}')
        elif platform_system == "Linux":
            subprocess.Popen(["xdg-open", link_target])
        return

    def open_system_link(self, system_link: Path):
        platform_system: str = platform.system()
        if platform_system == "Darwin":
            subprocess.Popen(["open", "-R", system_link])
        elif platform_system == "Windows":
            os.startfile(system_link)  # pylint: disable=no-member
        elif platform_system == "Linux":
            subprocess.Popen(["xdg-open", system_link])
        return

########################################################################################################################
# Object creation
########################################################################################################################

# use this object instead of importing the class and creating a new instance to prevent read and/or write races
io_manager = IOManager()