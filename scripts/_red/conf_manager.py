# conf_manager.py - Class to manager configuration and settings. Used to avoid circular imports.

# -------------------------------------------------------------------------------- #
# ----------------------------------------

########################################################################################################################
# Imports
########################################################################################################################

__all__ = ["conf"]

import definitions
from resources._red.game_config import *
from scripts._red.load_save import save_manager


########################################################################################################################
# Classes
########################################################################################################################

class ConfSettManager:
    """ Manages configuration and settings. """

    settings: Settings = SETTINGS
    game_config: GameConfig = GAME_CONFIG
    cat_config: CatConfig = CAT_CONFIG
    rel_config: RelationshipConfig = RELATIONSHIP_CONFIG
    clan_config: ClanConfig = CLAN_CONFIG
    event_config: EventConfig = EVENT_CONFIG
    prey_config: PreyConfig = PREY_CONFIG
    rank_config: RankConfig = RANK_CONFIG
    biome_config: BiomeConfig = BIOME_CONFIG


    _save_manager = save_manager


    # ------------------------------------- INIT ------------------------------------- #

    def __init__(self):
        self._load_game_settings()
        if self.game_config.april_fools:
            self.game_config.oops_all_kittens = True
            self.game_config.easter_eggs = True
        else:
            self.game_config.oops_all_kittens = False
            self.game_config.easter_eggs = False

        # if something went wrong loading settings, stop the game
        if not self.settings:
            raise RuntimeWarning(f"Something went wrong loading the game settings!")
        return

    def _load_game_settings(self):
        """ """
        game_setts: dict = self._save_manager.load_game_settings()
        self.settings.MoonSeasonWidget = bool(game_setts["MoonSeasonWidget"])
        self.settings.Language = definitions.cast_to_language(game_setts["LanguageCode"])
        self.settings.TextSize = int(game_setts["TextSize"])
        self.settings.Fullscreen = bool(game_setts["Fullscreen"])
        self.settings.VolumeMusic = int(game_setts["VolumeMusic"])
        self.settings.VolumeSound = int(game_setts["VolumeSound"])
        self.settings.VolumeMute = bool(game_setts["VolumeMute"])
        self.settings.DarkMode = bool(game_setts["DarkMode"])
        self.settings.FullscreenScaling = bool(game_setts["FullscreenScaling"])
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
        return

    # ------------------------------------ GETTER ------------------------------------ #

    def get_config_value(self, clan_at_war: bool = False, *args):
        """Fetches a value from the self.game_config dictionary. Pass each key as a
        separate argument, in the same order you would access the dictionary.
        This function will apply war modifiers if the clan is currently at war."""

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

    # ------------------------------------ SETTER ------------------------------------ #

    def load_clan_settings(self, clan_name: str):
        """ """
        raise NotImplementedError("ConfSettManager.load_clan_settings")

    def toggle_setting(self, setting: str) -> bool:
        """ Change a boolean setting. """
        if setting in self.settings.__dict__.keys():
            if isinstance(self.settings.__getattribute__(setting), bool):
                if self.settings.__getattribute__(setting):
                    self.settings.__setattr__(setting, False)
                else:
                    self.settings.__setattr__(setting, True)
                return True
        return False



conf = ConfSettManager()