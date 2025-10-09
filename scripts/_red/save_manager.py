# load_save.py - Load a save file and parse through the cats contained in it.

"""
TODO
 - Reformat all save files to YAML
 - load Clan files
    - replace Game.read_clans
 - load cat files
 - load setting files
"""

########################################################################################################################
# Imports
########################################################################################################################


import i18n
import os
import ujson
from typing import Optional
import yaml
from random import choice
from shutil import move as shutil_move  # Recursively move a file or directory to another location.
                                        # This is similar to the Unix "mv" command. Return the file
                                        # or directory's destination.
from scripts._red.cats.red_cat import RedCat
from scripts._red.clans.red_clan import RedClan, Camp
from scripts._red.io_manager import io_manager
# from scripts.game_structure.localization import get_new_pronouns
from scripts.housekeeping.datadir import get_save_dir, get_temp_dir

import definitions # definitions.SAVE_CLANGEN_VERSION_NUMBER

import logging
logger = logging.getLogger(__name__)

########################################################################################################################
# Constants and Paths
########################################################################################################################

MAX_SAVE_ATTEMPTS: int = 15

TEMP_FILE_DIR = f"{get_temp_dir()}/"

# CATS_SAVE_FILE_DIR: str = f"{get_save_dir()}/{CLAN_NAME}/"
# CATS_JSON_PATH: str = CATS_SAVE_FILE_DIR + "clan_cats.json"
# CATS_CSV_PATH: str = CATS_SAVE_FILE_DIR + "cats.csv"
# CATS_TXT_PATH: str = CATS_SAVE_FILE_DIR + "cats.txt"


########################################################################################################################
# Functions
########################################################################################################################

# TODO: each Clan will have a random generator seed. Import it when a save is loaded. random.seed(clan_seed)

def load_cats():
    raise Exception(f"You should be calling load_save() from the same module")

########################################################################################################################
# Classes
########################################################################################################################

class SaveManager:
    """ A class to manage cats and Clans in each save game. """

    iom = io_manager

    save_version: int
    game_version: str
    active_clan_prefix: Optional[str]

    # ------------------------------------- INIT ------------------------------------- #

    # ------------------------------------ SETTER ------------------------------------ #

    def update_active_clan_prefix(self, new_active_clan_prefix: Optional[str]):
        """ Set the current Clan's name so the correct save files will be read.

        Called by the game.update_active_clan_prefix_everywhere() ONLY.
        """
        if new_active_clan_prefix is None:
            self.active_clan_prefix = None
        # make sure you aren't trying to switch to the Clan you're already using
        elif new_active_clan_prefix.casefold() == self.active_clan_prefix:
            logger.warning(f"Can't switch to the save that's already active: tried to switch from save "
                           f"'{self.active_clan_prefix}' to save '{new_active_clan_prefix}' in SaveManager")
        else:
            self.active_clan_prefix = new_active_clan_prefix
        return

    # ------------------------------------ GETTER ------------------------------------ #

    # TODO
    def get_available_saves(self) -> tuple(list[str], list[str]):
        """ Load the names of save files present in the saves/ directory. """
        saves = self.iom.get_valid_save_names()
        saved_clans = [filename for filename in saves if "." not in filename]
        invalid_clans = []
        for clan_name in saved_clans:
            if f"{clan_name}Clan.yaml" not in saves:
                invalid_clans.append(clan_name)
                saved_clans.pop(clan_name)
        return saved_clans, invalid_clans

    # ------------------------------------ LOADER ------------------------------------ #

    def load_game_settings(self):
        """ Read the settings that apply across all save files.

        Called by config.
        """
        return self.iom.read_game_settings_file()

    def load_clan_settings(self):
        """ Read the settings that apply across all save files.

        Called by config.
        """
        return self.iom.read_clan_settings_file()

    def load_save(self, game_obj):
        """ Load the save where the player's Clan is named `player_clan_name`. """
        # create RedClan objects and Clan-related objects (e.g. Camp objects)
        self._load_clan_details(game_obj=game_obj)
        # create RedCat objects
        self._load_cats()
        # TODO load conditions
        # TODO load relationships

        # TODO load ongoing events
        raise NotImplementedError("SaveManager.load_save")

    # TODO load_camp()
    def _load_clan_details(self, game_obj):
        """ Load the Clan details file ('saves/ExampleClan.yaml') and use it to create RedClan objects.
        Then, register those RedClans in the game object's cat tracker.
        """

        def load_camp() -> Camp:
            """ Parse the camp details file. """
            camp_details = self.iom.load_camp_details_file()

        clan_details: dict = self.iom.read_clan_details_file()

        game_obj.current_season = definitions.cast_to_season(clan_details.pop("current_season")) # starting_season
        game_obj.current_moon = int(clan_details.pop("current_moon"))

        # game details and afterlife guides
        game_obj.save_version = clan_details.pop("save_version")
        game_obj.game_version = clan_details.pop("game_version")
        game_obj.cat_tracker._last_id = clan_details.pop("last_id")
        game_obj.cat_tracker.set_afterlife_guides(
            sc_cat_id=int(clan_details.pop("sc_guide")),
            df_cat_id=int(clan_details.pop("df_guide"))
        )

        # NB: Clan details are added here, not in a function like RedCat._parse_save_file, since the way
        #   the player's Clan, other warrior Clans, and the 'Clan' of outsiders are treated is very different

        # Clans
        for clan_prefix in clan_details:
            clan_info: dict = clan_details[clan_prefix]

            # the player's Clan
            if clan_prefix == self.active_clan_prefix:
                clan_obj = RedClan(clan_prefix=self.active_clan_prefix,
                                   afterlife=clan_info.pop("default_afterlife"),
                                   moon_established=clan_info.pop("moon_established"))
                clan_obj.camp = load_camp() # camp_bg
                clan_obj.clan_symbol = clan_info.pop("clan_symbol")
                # ["cats"]["special"]["leader"]["leader_lives"]
                clan_obj.leader_lives_remaining = int(clan_info.pop("leader_lives_remaining"))
                clan_obj.past_leader_ids = clan_info.pop("past_leader_ids")
                clan_obj.past_deputy_ids = clan_info.pop("past_deputy_ids")
                clan_obj.past_healer_ids = clan_info.pop("past_healer_ids")

                leader_focus: Optional[dict] = clan_info.pop("leader_focus")
                if leader_focus:
                    clan_obj.leader_focus_clan_prefix = leader_focus.pop("leader_focus_clan_prefix")
                    clan_obj.leader_focus_clan_purpose = definitions.cast_to_leader_focus(
                        leader_focus.pop("clan_purpose"))
                    clan_obj.leader_focus_outsider_id = leader_focus.pop("outsider_in_focus_id")
                    clan_obj.leader_focus_outsider_purpose = definitions.cast_to_leader_focus(
                        leader_focus.pop("clan_purpose"))
                    del leader_focus

                warrior_focus: Optional[dict] = clan_info.pop("warrior_focus")
                if warrior_focus:
                    clan_obj.last_focus_change = warrior_focus.pop("last_focus_change")
                    clan_obj.warrior_focus = definitions.cast_to_warrior_focus(
                        warrior_focus.pop("warrior_focus_purpose"))
                    clan_obj.warrior_focus_arg = clan_info.pop("warrior_focus_arg") # this is a Clan prefix
                    del warrior_focus

            # outsiders
            elif clan_prefix == definitions.OUTSIDER_CLAN_PREFIX:
                RedClan(clan_prefix=clan_prefix,
                        afterlife=definitions.Location.OutsiderAfterlife,
                        moon_established=0)
                # outsiders don't have a camp, a clan symbol, or special positions

            # other warrior Clans # "other_clans"
            else:
                clan_obj = RedClan(clan_prefix=clan_prefix,
                                   afterlife=clan_info.pop("default_afterlife"),
                                   moon_established=clan_info.pop("moon_established"))
                clan_obj.camp = definitions.cast_to_camp_key(clan_info.pop("camp_key")) # camp_bg
                clan_obj.clan_symbol = clan_info.pop("clan_symbol")
                clan_obj.leader_lives_remaining = int(clan_info.pop("leader_lives_remaining"))
                clan_obj.past_leader_ids = clan_info.pop("past_leader_ids")
                clan_obj.past_deputy_ids = clan_info.pop("past_deputy_ids")
                clan_obj.past_healer_ids = clan_info.pop("past_healer_ids")

        return

    def _load_cats(self):
        """ Load the files containing details about the cats and use them to create RedCat objects.
         Register those RedCats in the game object's cat tracker.

         TODO add them to RedClan objects here?
         """
        cats_per_clan: dict = self.iom.read_cats_files()

        # afterlives
        for afterlife in (definitions.Location.StarClan.value,
                          definitions.Location.DarkForest.value,
                          definitions.Location.OutsiderAfterlife.value):
            cats_in_afterlife: dict = cats_per_clan.pop(afterlife)
            for cat_id in cats_in_afterlife:
                # cat is added to the cat tracker in the RedCat class
                RedCat(save_file=cats_in_afterlife[cat_id], cat_id=cat_id)

        # outsiders
        outsiders = cats_per_clan.pop(definitions.OUTSIDER_CLAN_PREFIX)
        for cat_id in outsiders:
            # cat is added to the cat tracker in the RedCat class
            RedCat(save_file=outsiders[cat_id], cat_id=cat_id)

        # warrior Clans
        clan_prefixes = cats_per_clan.keys()
        for clan_prefix in clan_prefixes:
            clan_cats = cats_per_clan.pop(clan_prefix)
            for cat_id in clan_cats:
                # cat is added to the cat tracker in the RedCat class
                RedCat(save_file=clan_cats[cat_id], cat_id=cat_id)
        return

    # ------------------------------------- SAVER ------------------------------------ #

    def save_game_settings(self, settings):
        """ """
        return self.iom.write_game_settings_file(game_settings=settings)

    # ------------------------------------ PRIVATE ----------------------------------- #

    # TODO
    def read_clans(self):
        """ Check which save files exist (e.g. which Clans the player has created). """
        # We want clanlist.txt to contain ONLY the name of the Clan that is currently loaded.
        # We will get the list of clans from the saves folder each Clan has its own folder,
        # and the name of the folder is the name of the clan so we can just get a list of all
        # the folders in the saves folder.

        # First, we need to make sure the saves folder exists.
        if not os.path.exists(get_save_dir()):
            os.makedirs(get_save_dir())
            logger.debug(f"Created saves folder")
            return None

        # Now we can get a list of all the folders in the saves folder.
        #   If there are none, return None.
        clan_list = [f.name for f in os.scandir(get_save_dir()) if f.is_dir()]
        if not clan_list:
            logger.debug("No clans found in saves folder")
            return None

        # The Clan specified in saves/currentclan.txt should be
        #   first in the list so we can load it automatically.
        if os.path.exists(get_save_dir() + "/clanlist.txt"):
            # TODO replace clanlist.txt with currentclan.txt
            pass
        if os.path.exists(definitions.CURRENTCLAN_FILENAME):
            # TODO load this clan?
            pass




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
        return clan_list

    # TODO
    def _load_clans(self):
        """ Read """
        pass

    # TODO
    def _load_cats(self, file_contents: dict):
        """ Read the JSON-formatted file contents and put it in the CatTracker. """
        pass
    #
    # def _parse_csv_txt(self, raw_file_contents: str):
    #     """ Parse the way cat.csv files are written to a JSON format.
    #
    #         CAT: ID(0) - prefix:suffix(1) - gender(2) - status(3) - age(4) - trait(5) - parent1(6) - parent2(7) - mentor(8)
    #         PELT: pelt(9) - colour(10) - white(11) - length(12)
    #         SPRITE: kitten(13) - apprentice(14) - warrior(15) - elder(16) - eye colour(17) - reverse(18)
    #         - white patches(19) - pattern(20) - tortiebase(21) - tortiepattern(22) - tortiecolour(23) - skin(24) - skill(25) - NONE(26) - spec(27) - accessory(28) -
    #         spec2(29) - moons(30) - mate(31)
    #         dead(32) - SPRITE:dead(33) - exp(34) - dead for _ moons(35) - current apprentice(36)
    #         (BOOLS, either TRUE OR FALSE) paralyzed(37) - no kits(38) - exiled(39)
    #         genderalign(40) - former apprentices list (41)[FORMER APPS SHOULD ALWAYS BE MOVED TO THE END]
    #     """
    #     if len(raw_file_contents) > 0:
    #         raw_file_contents = raw_file_contents.replace("\t", ",")
    #         for i in raw_file_contents.split("\n"):
    #
    #             if i.strip() != "":
    #                 attr = i.split(",")
    #                 for x in range(len(attr)):
    #                     attr[x] = attr[x].strip()
    #                     if attr[x] in ["None", "None "]:
    #                         attr[x] = None
    #                     elif attr[x].upper() == "TRUE":
    #                         attr[x] = True
    #                     elif attr[x].upper() == "FALSE":
    #                         attr[x] = False
    #                 game.switches[
    #                     "error_message"
    #                 ] = "1There was an error loading cat # " + str(attr[0])
    #                 the_pelt = Pelt(
    #                     colour=attr[2], name=attr[11], length=attr[9], eye_color=attr[17]
    #                 )
    #                 game.switches[
    #                     "error_message"
    #                 ] = "2There was an error loading cat # " + str(attr[0])
    #                 the_cat = Cat(
    #                     ID=attr[0],
    #                     prefix=attr[1].split(":")[0],
    #                     suffix=attr[1].split(":")[1],
    #                     gender=attr[2],
    #                     status=attr[3],
    #                     pelt=the_pelt,
    #                     parent1=attr[6],
    #                     parent2=attr[7],
    #                 )
    #
    #                 game.switches[
    #                     "error_message"
    #                 ] = "3There was an error loading cat # " + str(attr[0])
    #                 the_cat.age, the_cat.mentor = attr[4], attr[8]
    #                 game.switches[
    #                     "error_message"
    #                 ] = "4There was an error loading cat # " + str(attr[0])
    #                 (
    #                     the_cat.pelt.cat_sprites["kitten"],
    #                     the_cat.pelt.cat_sprites["adolescent"],
    #                 ) = int(attr[13]), int(attr[14])
    #                 game.switches[
    #                     "error_message"
    #                 ] = "5There was an error loading cat # " + str(attr[0])
    #                 the_cat.pelt.cat_sprites["adult"], the_cat.pelt.cat_sprites["elder"] = (
    #                     int(attr[15]),
    #                     int(attr[16]),
    #                 )
    #                 game.switches[
    #                     "error_message"
    #                 ] = "6There was an error loading cat # " + str(attr[0])
    #                 (
    #                     the_cat.pelt.cat_sprites["young adult"],
    #                     the_cat.pelt.cat_sprites["senior adult"],
    #                 ) = int(attr[15]), int(attr[15])
    #                 game.switches[
    #                     "error_message"
    #                 ] = "7There was an error loading cat # " + str(attr[0])
    #                 (
    #                     the_cat.pelt.reverse,
    #                     the_cat.pelt.white_patches,
    #                     the_cat.pelt.pattern,
    #                 ) = (attr[18], attr[19], attr[20])
    #                 game.switches[
    #                     "error_message"
    #                 ] = "8There was an error loading cat # " + str(attr[0])
    #                 (
    #                     the_cat.pelt.tortiebase,
    #                     the_cat.pelt.tortiepattern,
    #                     the_cat.pelt.tortiecolour,
    #                 ) = (attr[21], attr[22], attr[23])
    #                 game.switches[
    #                     "error_message"
    #                 ] = "9There was an error loading cat # " + str(attr[0])
    #                 the_cat.trait, the_cat.pelt.skin, the_cat.specialty = (
    #                     attr[5],
    #                     attr[24],
    #                     attr[27],
    #                 )
    #                 game.switches[
    #                     "error_message"
    #                 ] = "10There was an error loading cat # " + str(attr[0])
    #                 the_cat.skill = attr[25]
    #                 if len(attr) > 28:
    #                     the_cat.pelt.accessory = attr[28]
    #                 if len(attr) > 29:
    #                     the_cat.specialty2 = attr[29]
    #                 else:
    #                     the_cat.specialty2 = None
    #                 game.switches[
    #                     "error_message"
    #                 ] = "11There was an error loading cat # " + str(attr[0])
    #                 if len(attr) > 34:
    #                     the_cat.experience = int(attr[34])
    #                     experiencelevels = [
    #                         "very low",
    #                         "low",
    #                         "slightly low",
    #                         "average",
    #                         "somewhat high",
    #                         "high",
    #                         "very high",
    #                         "master",
    #                         "max",
    #                     ]
    #                     the_cat.experience_level = experiencelevels[
    #                         floor(int(the_cat.experience) / 10)
    #                     ]
    #                 else:
    #                     the_cat.experience = 0
    #                 game.switches[
    #                     "error_message"
    #                 ] = "12There was an error loading cat # " + str(attr[0])
    #                 if len(attr) > 30:
    #                     # Attributes that are to be added after the update
    #                     the_cat.moons = int(attr[30])
    #                     if len(attr) >= 31:
    #                         # assigning mate to cat, if any
    #                         the_cat.mate = [attr[31]]
    #                     if len(attr) >= 32:
    #                         # Is the cat dead
    #                         the_cat.dead = attr[32]
    #                         the_cat.pelt.cat_sprites["dead"] = attr[33]
    #                 game.switches[
    #                     "error_message"
    #                 ] = "13There was an error loading cat # " + str(attr[0])
    #                 if len(attr) > 35:
    #                     the_cat.dead_for = int(attr[35])
    #                 game.switches[
    #                     "error_message"
    #                 ] = "14There was an error loading cat # " + str(attr[0])
    #                 if len(attr) > 36 and attr[36] is not None:
    #                     the_cat.apprentice = attr[36].split(";")
    #                 game.switches[
    #                     "error_message"
    #                 ] = "15There was an error loading cat # " + str(attr[0])
    #                 if len(attr) > 37:
    #                     the_cat.pelt.paralyzed = bool(attr[37])
    #                 if len(attr) > 38:
    #                     the_cat.no_kits = bool(attr[38])
    #                 if len(attr) > 39:
    #                     the_cat.exiled = bool(attr[39])
    #                 if len(attr) > 40:
    #                     the_cat.genderalign = attr[40]
    #                 if len(attr) > 41 and attr[41] is not None:  # KEEP THIS AT THE END
    #                     the_cat.former_apprentices = attr[41].split(";")
    #         game.switches[
    #             "error_message"
    #         ] = "There was an error loading this clan's mentors, apprentices, relationships, or sprite info."
    #         for inter_cat in all_cats.values():
    #             # Load the mentors and apprentices after all cats have been loaded
    #             game.switches["error_message"] = (
    #                     "There was an error loading this clan's mentors/apprentices. Last cat read was "
    #                     + str(inter_cat)
    #             )
    #             inter_cat.mentor = Cat.all_cats.get(inter_cat.mentor)
    #             apps = []
    #             former_apps = []
    #             for app_id in inter_cat.apprentice:
    #                 app = Cat.all_cats.get(app_id)
    #                 # Make sure if cat isn't an apprentice, they're a former apprentice
    #                 if "apprentice" in app.status:
    #                     apps.append(app)
    #                 else:
    #                     former_apps.append(app)
    #             for f_app_id in inter_cat.former_apprentices:
    #                 f_app = Cat.all_cats.get(f_app_id)
    #                 former_apps.append(f_app)
    #             inter_cat.apprentice = [
    #                 a.ID for a in apps
    #             ]  # Switch back to IDs. I don't want to risk breaking everything.
    #             inter_cat.former_apprentices = [a.ID for a in former_apps]
    #             if not inter_cat.dead:
    #                 game.switches["error_message"] = (
    #                         "There was an error loading this clan's relationships. Last cat read was "
    #                         + str(inter_cat)
    #                 )
    #                 inter_cat.load_relationship_of_cat()
    #             game.switches["error_message"] = (
    #                     "There was an error loading a cat's sprite info. Last cat read was "
    #                     + str(inter_cat)
    #             )
    #             # update_sprite(inter_cat)
    #         # generate the relationship if some is missing
    #         if not the_cat.dead:
    #             game.switches[
    #                 "error_message"
    #             ] = "There was an error when relationships where created."
    #             for cat_id in all_cats.keys():
    #                 the_cat = all_cats.get(cat_id)
    #                 game.switches[
    #                     "error_message"
    #                 ] = f"There was an error when relationships for cat #{the_cat} are created."
    #                 if the_cat.relationships is not None and len(the_cat.relationships) < 1:
    #                     the_cat.create_all_relationships()
    #         game.switches["error_message"] = ""
    #

    # TODO
    def save(self, path: str, write_data, safe_save=False):
        """ If write_data is not a string, assumes you want this
        in YAML format. If safe_save is true, it will read back the file
        to check that the correct data has been written to the file.
        If not, it will simply write the data to the file with no other
        checks.

        :param
        """

        # If write_data is not a string, write it as a YAML.
        if type(write_data) is not str:
            _data = yaml.dump(write_data) # produces the document as a UTF-8 encoded str object.
        else:
            _data = write_data

        dir_name, file_name = os.path.split(path)

        if safe_save:
            # Write the save to a temporary file, read it back, and then save it.
            if not file_name:
                raise RuntimeError(f"Safe_Save: No file name was found in {path}")

            temp_file_path: str = TEMP_FILE_DIR + f"{file_name}.tmp"

            i = 0
            while True:
                # Attempt to write to temp file and read the entire file back again
                _read_data = self.iom._read_file(filepath=temp_file_path)

                # If the read data is not the same as the written data, the save attempt failed. Try again
                if _data != _read_data:
                    i += 1
                    if i > MAX_SAVE_ATTEMPTS:
                        logger.error(f"Safe_Save: {file_name} was unable to properly save {i} times. Saving Failed.")
                        raise RuntimeError(f"Safe_Save: {file_name} was unable to properly save {i} times")
                    logger.warning(f"Safe_Save: {file_name} was incorrectly saved. Trying again.")
                    continue

                # Move the temporary save file to the normal save file's name
                shutil_move(temp_file_path, path)
                return
        else:
            self.iom._read_file(filepath=path)