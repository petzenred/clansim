# ui_directory.py -

from enum import StrEnum

from definitions import IMAGE_RESOURCES_PATH


class Button(StrEnum):
    """ """
    GoScreenEvents = "go_screen_events"
    GoScreenCamp = "go_screen_camp"
    GoScreenCatList = "go_screen_cat_list"
    GoScreenPatrol = "go_screen_patrol"
    GoScreenMainMenu = "go_screen_main_menu"
    GoScreenAllegiances = "go_screen_allegiances"
    GoScreenClanSettings = "go_screen_clan_settings"
    GoScreenLeaderDen = "go_screen_leader_den"
    GoScreenHealerDen = "go_screen_healer_den"
    GoScreenWarriorsDen = "go_screen_warriors_den"
    GoScreenClearing = "go_screen_clearing"
    GoScreen = "go_screen_"

    DropdownDens = "dropdown_dens" # "dens"
    DropdownChooseGroup = "dropdown_choose_group"
    Dropdown = "dropdown_"

    Mute = "mute"
    Unmute = "unmute"


class UIElement(StrEnum):
    """ """

    CoreVignette = "vignette.png"

    ClanNameHeading = "clan_name_heading.png" # "name_background"
    WidgetMoonsSeasons = "widget_moons_n_seasons"
    #WidgetMoonsSeasonsClosed = "widget_moons_n_seasons_closed"
    #WidgetMoonsSeasonsOpen = "widget_moons_n_seasons_open"
    WidgetMoonsSeasonsArrow = "widget_moons_n_seasons_arrow"

    BarVertical = "bar_vertical.png"
    BarHorizontal = "bar_horizontal.png"

    DensBar = "bar_vertical.png" # "dens_bar"

    @property
    def path(self):
        if ".png" in self.value:
            return str(IMAGE_RESOURCES_PATH + self.value)
        else:
            return None


class Background(StrEnum):
    """ """

    Menu = "menu.png"
    MenuLogoless = "menu_logoless.png"
    MacInstaller = "mac_installer_bg_blank.png"

    UnknownResidenceCatsList = "urbg.png"
    OutsideCatsList = "outside_clan_bg.png"
    StarClanCatsList = "starclanbg.png"
    DarkForestCatsList = "darkforestbg.png"

    @property
    def path(self):
        if ".png" in self.value:
            return str(IMAGE_RESOURCES_PATH + "backgrounds/" + self.value)
        else:
            return None




IMAGE_PATHS: dict = {
    UIElement.ClanNameHeading: IMAGE_RESOURCES_PATH + "clan_name_heading.png",
}