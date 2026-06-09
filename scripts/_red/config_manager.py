# conf_manager.py - Class to manager configuration and settings. Used to avoid circular imports.

# -------------------------------------------------------------------------------- #
# ----------------------------------------

########################################################################################################################
# Imports
########################################################################################################################

__all__ = ["config"]

import definitions
from resources._red.game_config import *
from scripts._red.io_manager import io_manager
from scripts._red.red_exceptions import InitializationError


########################################################################################################################
# Classes
########################################################################################################################

class ConfSettManager:
    """ Manages configuration and settings.

    TODO split Clan settings and game settings, since those are saved and loaded separately
    """

    iom = None

    settings: Settings = SETTINGS
    game_config: GameConfig = GAME_CONFIG
    screen_config: ScreenConfig = SCREEN_CONFIG
    cat_config: CatConfig = CAT_CONFIG
    rel_config: RelationshipConfig = RELATIONSHIP_CONFIG
    clan_config: ClanConfig = CLAN_CONFIG
    event_config: EventConfig = EVENT_CONFIG
    prey_config: PreyConfig = PREY_CONFIG
    rank_config: RankConfig = RANK_CONFIG
    biome_config: BiomeConfig = BIOME_CONFIG

    def _ready_to_go(self) -> bool:
        """ Check if all the external initialization has finished. """
        ready_f: bool = True
        if not self.settings:
            ready_f = False
        if not ready_f:
            raise InitializationError(f"Configuration/settings manager hasn't been fully initialized yet")
        return ready_f

    # ------------------------------------- INIT ------------------------------------- #

    def __init__(self):
        """ Prepare the configuration/settings manager for the game. """
        self.load_game_settings()

    def load_game_settings(self):
        """ Load game settings. """
        game_setts: dict = io_manager.read_game_settings_file()
        while not game_setts:
            # create the game settings file with default settings if it doesn't exist yet
            io_manager.write_game_settings_file(self.settings)
            game_setts = io_manager.read_game_settings_file()

        # load general game settings
        self.settings.ShowMoonSeasonWidget = bool(game_setts["ShowMoonSeasonWidget"])
        self.settings.Language = definitions.cast_to_language(game_setts["LanguageCode"])
        self.settings.TextSize = int(game_setts["TextSize"])
        self.settings.Fullscreen = bool(game_setts["Fullscreen"])
        self.settings.FullscreenScaling = bool(game_setts["FullscreenScaling"])
        self.settings.Theme = ThemeName(game_setts["ThemeName"])
        self.settings.Antialiasing = bool(game_setts["Antialiasing"])
        self.settings.UsePawCursor = bool(game_setts["UsePawCursor"])
        self.settings.UseKeybinds = bool(game_setts["UseKeybinds"])
        self.settings.UseShaders = bool(game_setts["UseShaders"])
        self.settings.AllowPatrolGore = bool(game_setts["AllowPatrolGore"])
        self.settings.Discord = bool(game_setts["Discord"])
        self.settings.AutoUpdate = bool(game_setts["AutoUpdate"])
        self.settings.ShowChangelogOnUpdate = bool(game_setts["ShowChangelogOnUpdate"])
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

    # ------------------------------------ GETTER ------------------------------------ #

    # TODO
    def get_config_value(self, clan_at_war: bool = False, *args):
        """ Fetches a value from the self.game_config dictionary. Pass each key as a
        separate argument, in the same order you would access the dictionary.
        This function will apply war modifiers if the clan is currently at war. """
        raise NotImplementedError("ConfSettManager.get_config_value()")
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

    # ------------------------------------ GETTER ------------------------------------ #

    # FIXME this method depends on hard-coded names for settings
    def update_setting(self, setting_name: str, new_value):
        """ Change a setting saved in ConfSettManager.settings.

        FIXME this method depends on hard-coded names for settings

        :param str setting_name: the CamelCase setting name that should be updated.
        :param new_value: the new value to set setting_name to. The type depends on setting_name.
        """
        self._ready_to_go()

        # make sure setting_name is valid
        if not setting_name in self.settings.__dict__:
            raise KeyError(f"{setting_name} isn't a valid setting")

        # make sure that new_value is the right type for setting_name
        if setting_name == "Language" and not isinstance(new_value, LanguageCode):
            raise TypeError(f"Must set a new language using a LanguageCode object")
        elif (setting_name in ("TextSize", "VolumeMusic", "VolumeSound", )
              and not isinstance(new_value, LanguageCode)
        ):
            raise TypeError(f"{setting_name} must be set to an integer value but tried to set it to: {new_value}")
        elif setting_name == "GameMode" and not isinstance(new_value, GameMode):
            raise TypeError(f"Must set a new game mode using a GameMode object, "
                            f"but tried to set it to {new_value}")
        elif setting_name == "LeaderFocus" and not isinstance(new_value, LeaderFocus):
            raise TypeError(f"Must set a new leader focus using a LeaderFocus "
                            f"object, but tried to set it to {new_value}")
        elif setting_name == "WarriorFocus" and not isinstance(new_value, WarriorFocus):
            raise TypeError(f"Must set a new warrior focus using a WarriorFocus "
                            f"object, but tried to set it to {new_value}")
        elif setting_name == "FreshkillTactic" and not isinstance(new_value, FreshkillTactic):
            raise TypeError(f"Must set Clan freshkill distribution tactic using a "
                            f"FreshkillTactic object, but tried to set it to {new_value}")
        else:
            if not isinstance(new_value, bool):
                raise TypeError(f"Must set {setting_name} to a boolean value, but tried to set it to {new_value}")


        # change the value and save settings
        self.settings.__setattr__(setting_name, new_value)
        io_manager.write_game_settings_file(self.settings)
        return


    # TODO
    def set_config_value(self):
        raise NotImplementedError("ConfSettManager.set_config_value")

    # ------------------------------------ LOADER ------------------------------------ #

    def load_clan_settings(self):
        """ Load Clan settings. Called by the game object.  """
        self._ready_to_go()
        clan_setts: dict = io_manager.read_clan_settings_file()

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
        self.settings.MiracleGays = clan_setts.pop("same_sex_birth")
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

        # name settings
        self.settings.NamesUseBiome = clan_setts.pop("biome_names")
        self.settings.NamesUsePeltColour = clan_setts.pop("pelt_colour_names")
        self.settings.NamesUseEyeColour = clan_setts.pop("eye_colour_names")
        self.settings.NamesUseLegacy = clan_setts.pop("legacy_names")
        self.settings.NamesUseSkill = clan_setts.pop("skill_names")

        return

    # ------------------------------------ SAVERS ------------------------------------ #

    def save_game_settings(self) -> bool:
        """ Does what it says on the tin, I don't know what to tell you. """
        return io_manager.write_game_settings_file(self.settings)


########################################################################################################################
# Instances
########################################################################################################################

config = ConfSettManager()
