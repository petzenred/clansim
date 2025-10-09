# conf_manager.py - Class to manager configuration and settings. Used to avoid circular imports.

# -------------------------------------------------------------------------------- #
# ----------------------------------------

########################################################################################################################
# Imports
########################################################################################################################

__all__ = ["config"]

import definitions
from resources._red.game_config import *
from scripts._red.red_exceptions import InitializationError


########################################################################################################################
# Classes
########################################################################################################################

class ConfSettManager:
    """ Manages configuration and settings. """

    _save_manager = None

    settings: Settings = SETTINGS
    game_config: GameConfig = GAME_CONFIG
    cat_config: CatConfig = CAT_CONFIG
    rel_config: RelationshipConfig = RELATIONSHIP_CONFIG
    clan_config: ClanConfig = CLAN_CONFIG
    event_config: EventConfig = EVENT_CONFIG
    prey_config: PreyConfig = PREY_CONFIG
    rank_config: RankConfig = RANK_CONFIG
    biome_config: BiomeConfig = BIOME_CONFIG

    # ------------------------------------- INIT ------------------------------------- #

    def assign_save_manager(self, save_manager):
        """ Assign the save manager for loading game settings. Called by the game object. """
        self._save_manager = save_manager

    def load_game_settings(self):
        """ Load game settings. Called by the game object.  """
        game_setts: dict = self._save_manager.read_game_settings_file()
        while not game_setts:
            # create the game settings file with default settings if it doesn't exist yet
            self._save_manager.write_game_settings_file(self.settings)
            game_setts = self._save_manager.read_game_settings_file()

        # load general game settings
        self.settings.ShowMoonSeasonWidget = bool(game_setts["ShowMoonSeasonWidget"])
        self.settings.Language = definitions.cast_to_language(game_setts["LanguageCode"])
        self.settings.TextSize = int(game_setts["TextSize"])
        self.settings.Fullscreen = bool(game_setts["Fullscreen"])
        self.settings.FullscreenScaling = bool(game_setts["FullscreenScaling"])
        self.settings.DarkMode = bool(game_setts["DarkMode"])
        self.settings.Antialiasing = bool(game_setts["Antialiasing"])
        self.settings.UsePawCursor = bool(game_setts["UsePawCursor"])
        self.settings.UseKeybinds = bool(game_setts["UseKeybinds"])
        self.settings.UseShaders = bool(game_setts["UseShaders"])
        self.settings.AllowPatrolGore = bool(game_setts["AllowPatrolGore"])
        self.settings.Discord = bool(game_setts["Discord"])
        self.settings.AutoUpdate = bool(game_setts["AutoUpdate"])
        self.settings.UpdateShowChangelog = bool(game_setts["UpdateShowChangelog"])
        self.settings.SpecialDates = bool(game_setts["SpecialDates"])
        self.settings.NewClanRandomRelations = bool(game_setts["NewClanRandomRelations"])
        self.settings.DefaultPronounsTheyThem = bool(game_setts["DefaultPronounsTheyThem"])

        # load sound game settings
        self.settings.VolumeMusic = int(game_setts["VolumeMusic"])
        self.settings.VolumeSound = int(game_setts["VolumeSound"])
        self.settings.VolumeMute = bool(game_setts["VolumeMute"])

        if self.game_config.april_fools:
            self.game_config.oops_all_kittens = True
            self.game_config.easter_eggs = True
        else:
            self.game_config.oops_all_kittens = False
            self.game_config.easter_eggs = False

        # if something went wrong loading settings, stop the game
        if not self.settings:
            raise InitializationError(f"Something went wrong loading the game settings!")
        return

    def _ready_to_go(self):
        """ Check if all the external initialization has finished. """
        ready_to_go: bool = True
        if not self.settings:
            ready_to_go = False
        if not self._save_manager:
            ready_to_go = False
        if not ready_to_go:
            raise InitializationError(f"config hasn't been fully initialized yet")
        return

    # ------------------------------------ GETTER ------------------------------------ #

    # TODO
    def get_config_value(self, clan_at_war: bool = False, *args):
        """ Fetches a value from the self.game_config dictionary. Pass each key as a
        separate argument, in the same order you would access the dictionary.
        This function will apply war modifiers if the clan is currently at war. """
        self._ready_to_go()

        war_effected = {
            ("death_related", "leader_death_chance"): (
                "death_related",
                "war_death_modifier_leader",
            ),
            ("death_related", "classic_death_chance"): (
                "death_related",
                "war_death_modifier",
            ),
            ("death_related", "expanded_death_chance"): (
                "death_related",
                "war_death_modifier",
            ),
            ("death_related", "cruel season_death_chance"): (
                "death_related",
                "war_death_modifier",
            ),
            ("condition_related", "classic_injury_chance"): (
                "condition_related",
                "war_injury_modifier",
            ),
            ("condition_related", "expanded_injury_chance"): (
                "condition_related",
                "war_injury_modifier",
            ),
            ("condition_related", "cruel season_injury_chance"): (
                "condition_related",
                "war_injury_modifier",
            ),
        }

        # Get Value
        config_value = self.game_config
        for key in args:
            config_value = config_value[key]

        # Apply war if needed
        if clan_at_war and args in war_effected:
            # Grabs the modifer
            mod = self.game_config
            for key in war_effected[args]:
                mod = mod[key]

            config_value -= mod

        return config_value

    # ------------------------------------ LOADER ------------------------------------ #

    def load_clan_settings(self):
        """ Load Clan settings. Called by the game object.  """
        self._ready_to_go()
        clan_setts: dict = self._save_manager.read_clan_settings_file()

        # general settings
        self.settings.GameMode = definitions.cast_to_game_mode(clan_setts.pop("game_mode")) # gamemode
        self.settings.AutosaveFiveMoons = clan_setts.pop("autosave")
        self.settings.AllowDisasterEvents = clan_setts.pop("disasters")
        self.settings.ShowExactXPNut = clan_setts.pop("show_xp_nut") # showxp
        self.settings.AllowHealerPatrolSelect = clan_setts.pop("random_healer") # random_med_cat
        self.settings.AllowFading = clan_setts.pop("fading")
        self.settings.SaveCompleteFadedCopy = clan_setts.pop("save_faded_copy")

        # relationship settings
        self.settings.AllowAffairs = clan_setts.pop("affair")
        self.settings.MiracleGays = clan_setts.pop("save_sex_birth")
        self.settings.GayAdoptionRights = clan_setts.pop("same_sex_adoption")
        self.settings.UnknownSecondParent = clan_setts.pop("single_parentage")
        self.settings.RomanceFirstCousin = clan_setts.pop("romance_cousin") # romantic_with_former_mentor
        self.settings.RomanceFormerApprentice = clan_setts.pop("romance_app") # first_cousin_mates

        # role settings
        self.settings.AutoDeputy = clan_setts.pop("auto_choose_deputy") # # deputy
        self.settings.GraduateAtOneYear = clan_setts.pop("age_based_graduation") # # 12_moon_graduation
        self.settings.PermConditionRetirement = clan_setts.pop("condition_based_retirement") # retirement
        self.settings.RandomlyBecomeMediator = clan_setts.pop("become_mediator")

        # screen settings
        self.settings.ShowRelationsDead = clan_setts.pop("show_dead_relation")
        self.settings.ShowRelationsEmpty = clan_setts.pop("show_empty_relation")
        self.settings.ShowFavouriteHighlight = clan_setts.pop("show_fav")
        self.settings.ShowCampBackground = clan_setts.pop("camp_background") # backgrounds
        self.settings.ShowMoonSeasonWidget = clan_setts.pop("moons_seasons_widget") # moons_and_seasons
        self.settings.ShowDenLabels = clan_setts.pop("show_den_labels") # den_labels

        return




config = ConfSettManager()