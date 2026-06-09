# red_filepaths.py - Like definitions.py, but only contains filepaths.

# -------------------------------------------------------------------------------- #
# ----------------------------------------

########################################################################################################################
# Imports
########################################################################################################################

from pathlib import Path
from dataclasses import dataclass

from definitions import ThemeName
from scripts.housekeeping.datadir import get_cache_dir, get_data_dir, get_resources_dir, get_save_dir


########################################################################################################################
# Constants
########################################################################################################################

# ----------------------------------------

GAME_SETTINGS_FILEPATH: Path = Path(get_save_dir(), "game_settings.yaml")
CURRENTCLAN_FILE_PATH: Path = Path(get_save_dir(), "currentclan.txt")

# -------------------------------------- UI -------------------------------------- #

# themes and screen scaling
THEME_FILEPATHS: dict[ThemeName, Path] = {
    ThemeName.Dark: Path(get_resources_dir(), "_red/theme/dark_theme.json"),
    ThemeName.Light: Path(get_resources_dir(), "_red/theme/light_theme.json")
}
SCREEN_SCALE_OUTPUT_FILEPATH: Path = Path(get_resources_dir(), "_red/theme/screen_scale_output.json")

# boxes
GENERATED_BOX_FRAME: Path = Path(get_resources_dir(), "images/generated_boxes/frame.png")
GENERATED_BOX_ROUNDED_BOX: Path = Path(get_resources_dir(), "images/generated_boxes/rounded_box.png")

# fonts

FONTS_DIRPATH: Path = Path(get_resources_dir(), "fonts")
# FIXME pygame.font.Font, in definitions.py
@dataclass
class Font:
    Name: str
    Regular: Path
    Bold: Path = None # optional
    Italic: Path = None # optional
    BoldItalic: Path = None # optional

NOTOSANS_FONT: Font = Font(
    Name="notosans",
    Regular=Path(FONTS_DIRPATH, "NotoSans-Medium.ttf"),
    Bold=Path(FONTS_DIRPATH, "NotoSans-ExtraBold.ttf"),
    Italic=Path(FONTS_DIRPATH, "NotoSans-MediumItalic.ttf"),
    BoldItalic=Path(FONTS_DIRPATH, "NotoSans-ExtraBoldItalic.ttf")
)

CLANGEN_FONT: Font = Font(Name="clangen", Regular=Path(FONTS_DIRPATH, "clangen.ttf"))

# buttons and UI elements
BUTTON_MAINMENU_NORMAL: Path = Path(get_resources_dir(), "images/generated_buttons/mainmenu_normal.png")
BUTTON_MAINMENU_HOVERED: Path = Path(get_resources_dir(), "images/generated_buttons/mainmenu_hovered.png")
BUTTON_MAINMENU_DISABLED: Path = Path(get_resources_dir(), "images/generated_buttons/mainmenu_disabled.png")

BUTTON_SQUOVAL_NORMAL: Path = Path(get_resources_dir(), "images/generated_buttons/general_normal.png")
BUTTON_SQUOVAL_HOVERED: Path = Path(get_resources_dir(), "images/generated_buttons/general_hovered.png")
BUTTON_SQUOVAL_DISABLED: Path = Path(get_resources_dir(), "images/generated_buttons/general_disabled.png")

ICON_TAB: Path = Path(get_resources_dir(), "images/generated_buttons/icon_tab.png")


BAR_VERTICAL: Path = Path(get_resources_dir(), "images/bar_vertical.png")
BAR_HORIZONTAL: Path = Path(get_resources_dir(), "images/bar_horizontal.png")
CLAN_NAME_HEADER: Path = Path(get_resources_dir(), "images/all_clan_menu_screens/clan_name_heading.png")
MNS_OPEN: Path = Path(get_resources_dir(), "images/all_clan_menu_screens/moons_seasons_open.png")
MNS_CLOSED: Path = Path(get_resources_dir(), "images/all_clan_menu_screens/moons_seasons_closed.png")
SEARCH_BAR: Path = Path(get_resources_dir(), "images/all_clan_menu_screens/search_bar.png")
MARKER_FAV: Path = Path(get_resources_dir(), "images/all_clan_menu_screens/marker_favourite.png")

CORE_VIGNETTE: Path = Path(get_resources_dir(), "images/core_vignette.png")

# ----------------------------------- LANGUAGE ----------------------------------- #

TRANSLATION_DICTS_FILEPATH: Path = Path(get_resources_dir(), "lang/")


# ----------------------------------------

# TODO remove this
# NAMES_DICT: Path = Path(get_resources_dir(), "_red/cat_names.en.yaml")

# ------------------------------------ SPRITES ----------------------------------- #

SPRITE_DIRPATH: Path = Path(get_data_dir(), "sprites") # TODO replace below with this and os.scan_dir

PLATFORM_SPRITES: str = "platforms"
CLAN_SYMBOL_SPRITES: str = "clan_symbols"
CLAN_SYMBOL_NAMES: Path = Path(get_resources_dir(), "_red/clan_symbols.yaml")
ERROR_PLACEHOLDER: Path = Path(SPRITE_DIRPATH, "error_placeholder.png")

SPRITE_EFFECTS_DIRPATH: Path = Path(SPRITE_DIRPATH, "effect")
SPRITE_FADE_FOG_DIRPATH: Path = Path(SPRITE_DIRPATH, "fade_fog")
SPRITE_PALETTES_DIR_PATH: Path = Path(SPRITE_DIRPATH, "palettes")

SPRITE_DATA_DICTS: dict[str, Path] = {
    "COLLAR_DATA": Path(SPRITE_DIRPATH, "dicts/collar_sprite_data.yaml"),
    "WILD_DATA": Path(SPRITE_DIRPATH, "dicts/wild_sprite_data.yaml"),
    "PLANT_DATA": Path(SPRITE_DIRPATH, "dicts/plant_sprite_data.yaml"),
    "SCAR_PELT_DATA": Path(SPRITE_DIRPATH, "dicts/scar_pelt_sprite_data.yaml"),
    "SCAR_MISSING_DATA": Path(SPRITE_DIRPATH, "dicts/scar_missing_sprite_data.yaml"),
    "SKIN_DATA": Path(SPRITE_DIRPATH, "dicts/skin_sprite_data.yaml"),
    "TORTIE_DATA": Path(SPRITE_DIRPATH, "dicts/tortie_patches_sprite_data.yaml"),
    "PELT_DATA": Path(SPRITE_DIRPATH, "dicts/pelt_sprite_data.yaml"),
    "EYE_BOTH_DATA": Path(SPRITE_DIRPATH, "dicts/eye_both_sprite_data.yaml"),
    "EYE_RIGHT_DATA": Path(SPRITE_DIRPATH, "dicts/eye_right_sprite_data.yaml"),
    "WHITE_DATA": Path(SPRITE_DIRPATH, "dicts/white_patches_sprite_data.yaml"),
    "CLAN_SYMBOL_DATA": Path(SPRITE_DIRPATH, "dicts/_2_clan_symbol_sprite_data.yaml")
}

LINEART: Path = Path(SPRITE_DIRPATH, "effect/lineart.png")
AF_LINEART: Path = Path(SPRITE_DIRPATH, "effect/aprilfoolslineart.png")

# ------------------------------- MAIN MENU SCREEN ------------------------------- #

MENU_IMAGE: Path = Path(get_resources_dir(), "images/menu.png")
ERROR_MSG: Path = Path(get_resources_dir(), "images/errormsg.png")
CHANGELOG_POPUP_SHOWN: Path = Path(get_cache_dir(), "changelog_popup_shown")
SUPRESS_UPDATE_POPUP: Path = Path(get_cache_dir(), "suppress_update_popup")

