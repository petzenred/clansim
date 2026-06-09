# conversion_utils.py -
from operator import sub

########################################################################################################################
# Imports
########################################################################################################################

from definitions import ConvertType

import logging

logger = logging.getLogger(__name__)


########################################################################################################################
# Methods
########################################################################################################################

# TODO
def update_clansim_save():
    """ Update a save file from a previous version of ClanSim. """
    pass


# TODO
def convert_clangen_save():
    """ Convert a ClanGen save file to one compatible with ClanSim.

    Works on ClanGen save files up to ClanGen version TODO.
    """
    pass


########################################################################################################################
# Classes
########################################################################################################################



class ConversionManager:
    """

    TODO
     - implement a convert_cat_from_save class to update history, pelt, etc.
    """

    def __init__(self):
        logger.debug(f"Created a new ConversionManager object")
        return

    # TODO
    def update_clansim_save(self):
        """ Update a save file from a previous version of ClanSim. """
        pass

    # TODO
    def convert_clangen_save(self):
        """ Convert a ClanGen save file to one compatible with ClanSim.

        Works on ClanGen save files up to ClanGen version TODO.
        """

        pass

    def convert_old_stuff(self, type: ConvertType):
        """ """

        if type is ConvertType.Pelt:
            pass
        if type is ConvertType.SaveFile:
            currentclan = "test" # TODO
            self.convert_clan_save(clan_name=currentclan)

    def convert_clan_save(self, clan_name: str):
        """ """
        old_save_file_path: str = "saves/{clan_name}clan.json"
        new_save_file_path: str = "saves/{clan_name}Clan.yaml"
        # TODO read files
        clan_json: dict = {}
        cats_json: dict = {}

        other_clans: list = []
        clan_yaml = {
            "last_warrior_focus_change": None,
            "clans_in_focus": [],
            "gamemode":  clan_json["gamemode"],
            "save_version": 0, # TODO
            "game_version": 0, # TODO
            "starting_season": "newleaf",
            "sc_guide": int(clan_json["instructor"]),
            "df_guide": None, # TODO probably need to make a new cat for this for old files
            clan_name: {
                "clan_symbol": clan_json["clan_symbol"],
                "age_moons": clan_json["clanage"],
                "reputation": {"temperament": ""},
                "camp": {
                    "biome": clan_json["biome"],
                    "background": clan_json["camp_bg"],
                    "freshkill": {},
                },
                "cats": {
                    "special": {
                        "leader": {
                            "cat_id": 0,
                            "remaining_lives": 9,
                            "predecessors": [],
                        },
                        "deputy": {

                        },
                        "medicine": {
                            "predecessors": [],
                        },
                    },
                    "general": { "cats": list(clan_json["clan_cats"]), }
                }
            }
        }
        cats_yaml: list[dict] = []
        for _ in cats_json:
            cats_yaml.update({int()})


        return

    def _convert_cat_from_save(self, cats_json: dict, clan_name: str):
        """ """
        cats_yaml: dict = {}

        for cat_json in cats_json:
            cat_yaml = {}
            cat_yaml.update({"name": {
                "prefix": cat_json["name_prefix"],
                "suffix": cat_json["name_suffix"],
                "special_suffix_hidden_f": bool(cat_json["specsuffix_hidden"])
            }})
            cat_yaml.update({"status": {
                "clan_token": clan_name,
                "location": None,
                "health": {
                    "paralyzed": None,
                    "moons_since_last_litter": None
                },
                "rank": None,
                "mate": None,
                "apprentices": []
            }})
            cat_yaml.update({"gender": {
                "kits": cat_json["gender"],
                "align": cat_json["gender_align"],
                "custom_pronouns": {
                    "en": {
                        "subject": "he",
                        "object": "him",
                        "poss": "his",
                        "inposs": "his",
                        "self": "himself",
                        "conju": 2,
                        "gender": 1
                    }
                }
            }})
            facets = cat_json["facets"].split(",")
            cat_yaml.update({"personality": {
                "lawfulness": facets[0],
                "sociability": facets[1],
                "aggression": facets[2],
                "stability": facets[3]
            }})
            cat_yaml.update({"flags": {
                "favourite": cat_json["favourite"],
                "no_kits": cat_json["no_kits"],
                "no_retire": cat_json["no_retire"],
                "no_romance": cat_json["no_mates"]
            }})
            cat_yaml.update({"pelt": {
                "length": "short",
                "colour": "golden",
                "colour_tint": None,
                "tortie_colour": "lilac",
                "pattern": "rosette",
                "tortie_pattern": "rosette",
                "white_patches": "fctwo",
                "white_patch_tint": "offwhite",
                "skin_colour": "darkbrown",
                "eye_colour": ["sage", "sage"],
                "accessories": [],
                "scars": []
            }})
            cat_yaml.update({"history": {
                "backstory": cat_json["backstory"],
                "birth": {
                    "moon": 0,
                    "season": "newleaf",
                    "parents": None,
                    "new_cats": [1],
                    "age_at_birth": 99
                },
                "": cat_json[""],
                "": cat_json[""],
                "": cat_json[""],
                "": cat_json[""],
            }})
        return

    # def _convert_pelts(self, convert_dict): # pelts.Pelt.check_and_convert
    #     """Checks for old-type properties for the appearance-related properties
    #     that are stored in CatPelt, and converts them. To be run when loading a cat in."""
    #     # TODO CatPeltPatternCategory.Striped used to be 'tabby', CatPeltPatternCategory.Solid used to be 'plain'
    #     # TODO TwoColour used to be a separate colour name for SingleColour cats with white.
    #     # TODO EyeColour works differently now
    #
    #     tabbies = ["Tabby", "Ticked", "Mackerel", "Classic", "Sokoke", "Agouti"]
    #     spotted = ["Speckled", "Rosette"]
    #     plain = ["SingleColour", "TwoColour", "Smoke", "Singlestripe"]
    #     exotic = ["Bengal", "Marbled", "Masked"]
    #     torties = ["Tortie", "Calico"]
    #     pelt_categories = [tabbies, spotted, plain, exotic, torties]
    #
    #     # SPRITE NAMES
    #     single_colours = [
    #         "WHITE",
    #         "PALEGREY",
    #         "SILVER",
    #         "GREY",
    #         "DARKGREY",
    #         "GHOST",
    #         "BLACK",
    #         "CREAM",
    #         "PALEGINGER",
    #         "GOLDEN",
    #         "GINGER",
    #         "DARKGINGER",
    #         "SIENNA",
    #         "LIGHTBROWN",
    #         "LILAC",
    #         "BROWN",
    #         "GOLDEN-BROWN",
    #         "DARKBROWN",
    #         "CHOCOLATE",
    #     ]
    #     ginger_colours = ["CREAM", "PALEGINGER", "GOLDEN", "GINGER", "DARKGINGER", "SIENNA"]
    #     black_colours = ["GREY", "DARKGREY", "GHOST", "BLACK"]
    #     white_colours = ["WHITE", "PALEGREY", "SILVER"]
    #     brown_colours = [
    #         "LIGHTBROWN",
    #         "LILAC",
    #         "BROWN",
    #         "GOLDEN-BROWN",
    #         "DARKBROWN",
    #         "CHOCOLATE",
    #     ]
    #     colour_categories = [ginger_colours, black_colours, white_colours, brown_colours]
    #     eye_sprites = [
    #         "YELLOW",
    #         "AMBER",
    #         "HAZEL",
    #         "PALEGREEN",
    #         "GREEN",
    #         "BLUE",
    #         "DARKBLUE",
    #         "BLUEYELLOW",
    #         "BLUEGREEN",
    #         "GREY",
    #         "CYAN",
    #         "EMERALD",
    #         "PALEBLUE",
    #         "PALEYELLOW",
    #         "GOLD",
    #         "HEATHERBLUE",
    #         "COPPER",
    #         "SAGE",
    #         "COBALT",
    #         "SUNLITICE",
    #         "GREENYELLOW",
    #         "BRONZE",
    #         "SILVER",
    #         "ORANGE"
    #     ]
    #     little_white = [
    #         "LITTLE",
    #         "LIGHTTUXEDO",
    #         "BUZZARDFANG",
    #         "TIP",
    #         "BLAZE",
    #         "BIB",
    #         "VEE",
    #         "PAWS",
    #         "BELLY",
    #         "TAILTIP",
    #         "TOES",
    #         "BROKENBLAZE",
    #         "LILTWO",
    #         "SCOURGE",
    #         "TOESTAIL",
    #         "RAVENPAW",
    #         "HONEY",
    #         "LUNA",
    #         "EXTRA",
    #         "MUSTACHE",
    #         "REVERSEHEART",
    #         "SPARKLE",
    #         "RIGHTEAR",
    #         "LEFTEAR",
    #         "ESTRELLA",
    #         "REVERSEEYE",
    #         "BACKSPOT",
    #         "EYEBAGS",
    #         "LOCKET",
    #         "BLAZEMASK",
    #         "TEARS",
    #     ]
    #     mid_white = [
    #         "TUXEDO",
    #         "FANCY",
    #         "UNDERS",
    #         "DAMIEN",
    #         "SKUNK",
    #         "MITAINE",
    #         "SQUEAKS",
    #         "STAR",
    #         "WINGS",
    #         "DIVA",
    #         "SAVANNAH",
    #         "FADESPOTS",
    #         "BEARD",
    #         "DAPPLEPAW",
    #         "TOPCOVER",
    #         "WOODPECKER",
    #         "MISS",
    #         "BOWTIE",
    #         "VEST",
    #         "FADEBELLY",
    #         "DIGIT",
    #         "FCTWO",
    #         "FCONE",
    #         "MIA",
    #         "ROSINA",
    #         "PRINCESS",
    #         "DOUGIE",
    #     ]
    #     high_white = [
    #         "ANY",
    #         "ANYTWO",
    #         "BROKEN",
    #         "FRECKLES",
    #         "RINGTAIL",
    #         "HALFFACE",
    #         "PANTSTWO",
    #         "GOATEE",
    #         "PRINCE",
    #         "FAROFA",
    #         "MISTER",
    #         "PANTS",
    #         "REVERSEPANTS",
    #         "HALFWHITE",
    #         "APPALOOSA",
    #         "PIEBALD",
    #         "CURVED",
    #         "GLASS",
    #         "MASKMANTLE",
    #         "MAO",
    #         "PAINTED",
    #         "SHIBAINU",
    #         "OWL",
    #         "BUB",
    #         "SPARROW",
    #         "TRIXIE",
    #         "SAMMY",
    #         "FRONT",
    #         "BLOSSOMSTEP",
    #         "BULLSEYE",
    #         "FINN",
    #         "SCAR",
    #         "BUSTER",
    #         "HAWKBLAZE",
    #         "CAKE",
    #     ]
    #     mostly_white = [
    #         "VAN",
    #         "ONEEAR",
    #         "LIGHTSONG",
    #         "TAIL",
    #         "HEART",
    #         "MOORISH",
    #         "APRON",
    #         "CAPSADDLE",
    #         "CHESTSPECK",
    #         "BLACKSTAR",
    #         "PETAL",
    #         "HEARTTWO",
    #         "PEBBLESHINE",
    #         "BOOTS",
    #         "COW",
    #         "COWTWO",
    #         "LOVEBUG",
    #         "SHOOTINGSTAR",
    #         "EYESPOT",
    #         "PEBBLE",
    #         "TAILTWO",
    #         "BUDDY",
    #         "KROPKA",
    #     ]
    #     point_markings = ["COLOURPOINT", "RAGDOLL", "SEPIAPOINT", "MINKPOINT", "SEALPOINT"]
    #     vit = [
    #         "VITILIGO",
    #         "VITILIGOTWO",
    #         "MOON",
    #         "PHANTOM",
    #         "KARPATI",
    #         "POWDER",
    #         "BLEACHED",
    #         "SMOKEY",
    #     ]
    #     white_sprites = [
    #         little_white,
    #         mid_white,
    #         high_white,
    #         mostly_white,
    #         point_markings,
    #         vit,
    #         "FULLWHITE",
    #     ]
    #
    #     skin_sprites = [
    #         "BLACK",
    #         "PINK",
    #         "DARKBROWN",
    #         "BROWN",
    #         "LIGHTBROWN",
    #         "DARK",
    #         "DARKGREY",
    #         "GREY",
    #         "DARKSALMON",
    #         "SALMON",
    #         "PEACH",
    #         "DARKMARBLED",
    #         "MARBLED",
    #         "LIGHTMARBLED",
    #         "DARKBLUE",
    #         "BLUE",
    #         "LIGHTBLUE",
    #         "RED",
    #     ]
    #
    #     sprites_names = {
    #         "SingleColour": "single",
    #         "TwoColour": "single",
    #         "Tabby": "tabby",
    #         "Marbled": "marbled",
    #         "Rosette": "rosette",
    #         "Smoke": "smoke",
    #         "Ticked": "ticked",
    #         "Speckled": "speckled",
    #         "Bengal": "bengal",
    #         "Mackerel": "mackerel",
    #         "Classic": "classic",
    #         "Sokoke": "sokoke",
    #         "Agouti": "agouti",
    #         "Singlestripe": "singlestripe",
    #         "Masked": "masked",
    #         "Tortie": None,
    #         "Calico": None,
    #     }
    #
    #     # First, convert from some old names that may be in white_patches.
    #     if self.white_patches == "POINTMARK":
    #         self.white_patches = "SEALPOINT"
    #     elif self.white_patches == "PANTS2":
    #         self.white_patches = "PANTSTWO"
    #     elif self.white_patches == "ANY2":
    #         self.white_patches = "ANYTWO"
    #     elif self.white_patches == "VITILIGO2":
    #         self.white_patches = "VITILIGOTWO"
    #
    #     if self.vitiligo == "VITILIGO2":
    #         self.vitiligo = "VITILIGOTWO"
    #
    #     # Move white_patches that should be in vit or points.
    #     # CatPelt.white_patches -> CatPelt.white_patches
    #     if self.white_patches in CatPelt.vit:
    #         self.vitiligo = self.white_patches
    #         self.white_patches = None
    #     elif self.white_patches in CatPelt.point_markings:
    #         self.points = self.white_patches
    #         self.white_patches = None
    #
    #     # TODO  CatPelt.tortiepattern -> # TODO CatPelt.pattern
    #     # TODO "tortie?" -> "?"
    #     # TODO "solid" -> PeltPattern.SingleColour
    #     # TODO self.tortiepattern vs self.pattern vs self.tortiespots
    #     if self.tortiepattern and "tortie" in self.tortiepattern:
    #         self.tortiepattern = sub("tortie", "", self.tortiepattern.lower())
    #         if self.tortiepattern == "solid":
    #             self.tortiepattern = "single"
    #     if self.pattern in convert_dict["old_tortie_patches"]:
    #         old_pattern = self.pattern
    #         self.pattern = convert_dict["old_tortie_patches"][old_pattern][1]
    #         # TODO maybe ClanGen wants it so torties can be ginger-on-ginger
    #         # If the pattern is old, there is also a chance the base color is stored in
    #         # tortiecolour. That may be different from the pelt color ("main" for torties)
    #         # generated before the "ginger-on-ginger" update. If it was generated after that update,
    #         # tortiecolour and pelt_colour will be the same. Therefore, let's also re-set the pelt color
    #         self.colour = self.tortiecolour
    #
    #     if self.white_patches in convert_dict["old_creamy_patches"]:
    #         self.white_patches = convert_dict["old_creamy_patches"][self.white_patches]
    #         self.white_patches_tint = "darkcream"
    #     elif self.white_patches in ["SEPIAPOINT", "MINKPOINT", "SEALPOINT"]:
    #         self.white_patches_tint = "none"
    #
    #     # Eye Color Convert Stuff
    #     if self.eye_colour == "BLUE2":
    #         self.eye_colour = "COBALT"
    #     if self.eye_colour2 == "BLUE2":
    #         self.eye_colour2 = "COBALT"
    #
    #     if self.eye_colour in ["BLUEYELLOW", "BLUEGREEN"]:
    #         if self.eye_colour == "BLUEYELLOW":
    #             self.eye_colour2 = "YELLOW"
    #         elif self.eye_colour == "BLUEGREEN":
    #             self.eye_colour2 = "GREEN"
    #         self.eye_colour = "BLUE"
    #
    #     # TODO account for new long-furred sprites
    #     if self.length == "long":
    #         if self.cat_sprites["adult"] not in [9, 10, 11]:
    #             if self.cat_sprites["adult"] == 0:
    #                 self.cat_sprites["adult"] = 9
    #             elif self.cat_sprites["adult"] == 1:
    #                 self.cat_sprites["adult"] = 10
    #             elif self.cat_sprites["adult"] == 2:
    #                 self.cat_sprites["adult"] = 11
    #             self.cat_sprites["young adult"] = self.cat_sprites["adult"]
    #             self.cat_sprites["senior adult"] = self.cat_sprites["adult"]
    #             self.cat_sprites["para_adult"] = 16
    #     else:
    #         self.cat_sprites["para_adult"] = 15
    #     if self.cat_sprites["senior"] not in [12, 13, 14]:
    #         if self.cat_sprites["senior"] == 3:
    #             self.cat_sprites["senior"] = 12
    #         elif self.cat_sprites["senior"] == 4:
    #             self.cat_sprites["senior"] = 13
    #         elif self.cat_sprites["senior"] == 5:
    #             self.cat_sprites["senior"] = 14
    #         self.tortiecolour = convert_dict["old_tortie_patches"][old_pattern][0]
    #
    #     if self.pattern == "MINIMAL1":
    #         self.pattern = "MINIMALONE"
    #     elif self.pattern == "MINIMAL2":
    #         self.pattern = "MINIMALTWO"
    #     elif self.pattern == "MINIMAL3":
    #         self.pattern = "MINIMALTHREE"
    #     elif self.pattern == "MINIMAL4":
    #         self.pattern = "MINIMALFOUR"
    #
    #     if isinstance(self.accessory, str):
    #         self.accessory = [self.accessory]
