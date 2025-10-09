# conversion_dict.py - Defines updates the text strings, etc.

"""
scripts.cat.pelts.Pelt.check_and_convert

def check_and_convert(self, convert_dict):
    \"""Checks for old-type properties for the appearance-related properties
    that are stored in Pelt, and converts them. To be run when loading a cat in.\"""

    # First, convert from some old names that may be in white_patches.
    if self.white_patches == "POINTMARK":
        self.white_patches = "SEALPOINT"
    elif self.white_patches == "PANTS2":
        self.white_patches = "PANTSTWO"
    elif self.white_patches == "ANY2":
        self.white_patches = "ANYTWO"
    elif self.white_patches == "VITILIGO2":
        self.white_patches = "VITILIGOTWO"

    if self.vitiligo == "VITILIGO2":
        self.vitiligo = "VITILIGOTWO"

    # Move white_patches that should be in vit or points.
    if self.white_patches in Pelt.vit:
        self.vitiligo = self.white_patches
        self.white_patches = None
    elif self.white_patches in Pelt.point_markings:
        self.points = self.white_patches
        self.white_patches = None

    if self.tortiepattern and "tortie" in self.tortiepattern:
        self.tortiepattern = sub("tortie", "", self.tortiepattern.lower())
        if self.tortiepattern == "solid":
            self.tortiepattern = "single"

    if self.white_patches in convert_dict["old_creamy_patches"]:
        self.white_patches = convert_dict["old_creamy_patches"][self.white_patches]
        self.white_patches_tint = "darkcream"
    elif self.white_patches in ["SEPIAPOINT", "MINKPOINT", "SEALPOINT"]:
        self.white_patches_tint = "none"

    # Eye Color Convert Stuff
    if self.eye_colour == "BLUE2":
        self.eye_colour = "COBALT"
    if self.eye_colour2 == "BLUE2":
        self.eye_colour2 = "COBALT"

    if self.eye_colour in ["BLUEYELLOW", "BLUEGREEN"]:
        if self.eye_colour == "BLUEYELLOW":
            self.eye_colour2 = "YELLOW"
        elif self.eye_colour == "BLUEGREEN":
            self.eye_colour2 = "GREEN"
        self.eye_colour = "BLUE"

    if self.length == "long":
        if self.cat_sprites["adult"] not in [9, 10, 11]:
            if self.cat_sprites["adult"] == 0:
                self.cat_sprites["adult"] = 9
            elif self.cat_sprites["adult"] == 1:
                self.cat_sprites["adult"] = 10
            elif self.cat_sprites["adult"] == 2:
                self.cat_sprites["adult"] = 11
            self.cat_sprites["young adult"] = self.cat_sprites["adult"]
            self.cat_sprites["senior adult"] = self.cat_sprites["adult"]
            self.cat_sprites["para_adult"] = 16
    else:
        self.cat_sprites["para_adult"] = 15
    if self.cat_sprites["senior"] not in [12, 13, 14]:
        if self.cat_sprites["senior"] == 3:
            self.cat_sprites["senior"] = 12
        elif self.cat_sprites["senior"] == 4:
            self.cat_sprites["senior"] = 13
        elif self.cat_sprites["senior"] == 5:
            self.cat_sprites["senior"] = 14

    if self.pattern in convert_dict["old_tortie_patches"]:
        old_pattern = self.pattern
        self.pattern = convert_dict["old_tortie_patches"][old_pattern][1]

        # If the pattern is old, there is also a chance the base color is stored in
        # tortiecolour. That may be different from the pelt color ("main" for torties)
        # generated before the "ginger-on-ginger" update. If it was generated after that update,
        # tortiecolour and pelt_colour will be the same. Therefore, let's also re-set the pelt color
        self.colour = self.tortiecolour
        self.tortiecolour = convert_dict["old_tortie_patches"][old_pattern][0]

    if self.pattern == "MINIMAL1":
        self.pattern = "MINIMALONE"
    elif self.pattern == "MINIMAL2":
        self.pattern = "MINIMALTWO"
    elif self.pattern == "MINIMAL3":
        self.pattern = "MINIMALTHREE"
    elif self.pattern == "MINIMAL4":
        self.pattern = "MINIMALFOUR"

    if isinstance(self.accessory, str):
        self.accessory = [self.accessory]


"""


def load_save():
    source, file_contents = _find_and_load_file()
    save = SaveManager(source, file_contents)


def _find_and_load_file() -> (str, dict):
    """ Check for JSON, CSV, and text files containing a directory of cats in the game. """
    try:
        if os.path.exists(CATS_JSON_PATH):
            with open(CATS_JSON_PATH, "r", encoding="utf-8") as read_file:
                return 'json', ujson.loads(read_file.read())

        elif os.path.exists(CATS_CSV_PATH):
            with open(CATS_CSV_PATH, "r", encoding="utf-8") as read_file:
                return 'csv', read_file.read()

        elif os.path.exists(CATS_TXT_PATH):
            with open(CATS_TXT_PATH, "r", encoding="utf-8") as read_file:
                return 'txt', ujson.loads(read_file.read())
        else:
            with open(CATS_JSON_PATH, "r", encoding="utf-8") as raise_fnf_exception:
                pass
    except FileNotFoundError as e:
        logger.exception(e)
        logger.error(f"Can't find a save file containing cats")
        raise
    except PermissionError as e:
        logger.exception(e)
        logger.error(f"ClanSim lacks permission to open the save file at {CATS_JSON_PATH}")
        raise
    except ujson.JSONDecodeError as e:
        logger.exception(e)
        logger.error(f"The save file at {CATS_JSON_PATH} is malformed")
        raise


def json_load():
    all_cats = []
    # Load the dictionary to bring old formats up-to-date
    with open(CONVERSION_DICT_PATH, "r", encoding="utf-8") as read_file:
        conversion_dict = ujson.loads(read_file.read())
    # Load the save file containing all cats
    save_file_contents = _find_and_load_file()

    old_tortie_patches = conversion_dict["old_tortie_patches"]

    # create new cat objects
    for i, cat in enumerate(save_file_contents):
        try:
            new_cat = Cat(
                ID=cat["ID"],
                prefix=cat["name_prefix"],
                suffix=cat["name_suffix"],
                specsuffix_hidden=(
                    cat["specsuffix_hidden"] if "specsuffix_hidden" in cat else False
                ),
                gender=cat["gender"],
                status=Rank(cat["status"]),
                parent1=cat["parent1"],
                parent2=cat["parent2"],
                moons=cat["moons"],
                eye_colour=cat["eye_colour"],
                loading_cat=True,
            )

            # TODO make eye_color an enum to go along with Pelt being a dataclass?
            if cat["eye_colour"] == "BLUE2":
                cat["eye_colour"] = "COBALT"
            if cat["eye_colour"] in ["BLUEYELLOW", "BLUEGREEN"]:
                if cat["eye_colour"] == "BLUEYELLOW":
                    cat["eye_colour2"] = "YELLOW"
                elif cat["eye_colour"] == "BLUEGREEN":
                    cat["eye_colour2"] = "GREEN"
                cat["eye_colour"] = "BLUE"
            if "eye_colour2" in cat:
                if cat["eye_colour2"] == "BLUE2":
                    cat["eye_colour2"] = "COBALT"

            new_cat.pelt = Pelt(
                name=cat["pelt_name"],
                length=cat["pelt_length"],
                colour=cat["pelt_color"],
                eye_color=cat["eye_colour"],
                eye_colour2=cat["eye_colour2"] if "eye_colour2" in cat else None,
                paralyzed=cat["paralyzed"],
                kitten_sprite=(
                    cat["sprite_kitten"]
                    if "sprite_kitten" in cat
                    else cat["spirit_kitten"]
                ),
                adol_sprite=(
                    cat["sprite_adolescent"]
                    if "sprite_adolescent" in cat
                    else cat["spirit_adolescent"]
                ),
                adult_sprite=(
                    cat["sprite_adult"]
                    if "sprite_adult" in cat
                    else cat["spirit_adult"]
                ),
                senior_sprite=(
                    cat["sprite_senior"]
                    if "sprite_senior" in cat
                    else cat["spirit_elder"]
                ),
                para_adult_sprite=(
                    cat["sprite_para_adult"] if "sprite_para_adult" in cat else None
                ),
                reverse=cat["reverse"],
                vitiligo=cat["vitiligo"] if "vitiligo" in cat else None,
                points=cat["points"] if "points" in cat else None,
                white_patches_tint=(
                    cat["white_patches_tint"]
                    if "white_patches_tint" in cat
                    else "offwhite"
                ),
                white_patches=cat["white_patches"],
                tortiebase=cat["tortie_base"],
                tortiecolour=cat["tortie_color"],
                tortiepattern=cat["tortie_pattern"],
                pattern=cat["pattern"],
                skin=cat["skin"],
                tint=cat["tint"] if "tint" in cat else "none",
                scars=cat["scars"] if "scars" in cat else [],
                accessory=cat["accessory"],
                opacity=cat["opacity"] if "opacity" in cat else 100,
            )

            # Runs a bunch of apperence-related convertion of old stuff.
            new_cat.pelt.check_and_convert(conversion_dict)

            # converting old specialty saves into new scar parameter
            if "specialty" in cat or "specialty2" in cat:
                if cat["specialty"] is not None:
                    new_cat.pelt.scars.append(cat["specialty"])
                if cat["specialty2"] is not None:
                    new_cat.pelt.scars.append(cat["specialty2"])

            new_cat.adoptive_parents = (
                cat["adoptive_parents"] if "adoptive_parents" in cat else []
            )

            new_cat.genderalign = cat["gender_align"]
            new_cat.pronouns = (
                cat["pronouns"]
                if "pronouns" in cat
                else {i18n.config.get("locale"): get_new_pronouns(new_cat.genderalign)}
            )
            new_cat.backstory = cat["backstory"] if "backstory" in cat else None
            if new_cat.backstory in BACKSTORIES["conversion"]:
                new_cat.backstory = BACKSTORIES["conversion"][new_cat.backstory]
            new_cat.birth_cooldown = (
                cat["birth_cooldown"] if "birth_cooldown" in cat else 0
            )
            new_cat.moons = cat["moons"]

            if "facets" in cat:
                facets = [int(i) for i in cat["facets"].split(",")]
                new_cat.personality = Personality(
                    trait=cat["trait"],
                    kit_trait=new_cat.age in ["newborn", "kitten"],
                    lawful=facets[0],
                    social=facets[1],
                    aggress=facets[2],
                    stable=facets[3],
                )
            else:
                new_cat.personality = Personality(
                    trait=cat["trait"], kit_trait=new_cat.age in ["newborn", "kitten"]
                )

            new_cat.mentor = cat["mentor"]
            new_cat.former_mentor = (
                cat["former_mentor"] if "former_mentor" in cat else []
            )
            new_cat.patrol_with_mentor = (
                cat["patrol_with_mentor"] if "patrol_with_mentor" in cat else 0
            )
            new_cat.no_kits = cat["no_kits"]
            new_cat.no_mates = cat["no_mates"] if "no_mates" in cat else False
            new_cat.no_retire = cat["no_retire"] if "no_retire" in cat else False
            new_cat.exiled = cat["exiled"]
            new_cat.driven_out = cat["driven_out"] if "driven_out" in cat else False

            if "skill_dict" in cat:
                new_cat.skills = CatSkills(cat["skill_dict"])
            elif "skill" in cat:
                if new_cat.backstory is None:
                    if "skill" == "formerly a loner":
                        backstory = choice(["loner1", "loner2", "rogue1", "rogue2"])
                        new_cat.backstory = backstory
                    elif "skill" == "formerly a kittypet":
                        backstory = choice(["kittypet1", "kittypet2"])
                        new_cat.backstory = backstory
                    else:
                        new_cat.backstory = "clanborn"
                new_cat.skills = CatSkills.get_skills_from_old(
                    cat["skill"], new_cat.status, new_cat.moons
                )

            new_cat.mate = cat["mate"] if type(cat["mate"]) is list else [cat["mate"]]
            if None in new_cat.mate:
                new_cat.mate = [i for i in new_cat.mate if i is not None]
            new_cat.previous_mates = (
                cat["previous_mates"] if "previous_mates" in cat else []
            )
            new_cat.dead = cat["dead"]
            new_cat.dead_for = cat["dead_moons"]
            new_cat.experience = cat["experience"]
            new_cat.apprentice = cat["current_apprentice"]
            new_cat.former_apprentices = cat["former_apprentices"]
            new_cat.df = cat["df"] if "df" in cat else False

            new_cat.outside = cat["outside"] if "outside" in cat else False
            new_cat.faded_offspring = (
                cat["faded_offspring"] if "faded_offspring" in cat else []
            )
            new_cat.prevent_fading = (
                cat["prevent_fading"] if "prevent_fading" in cat else False
            )
            new_cat.favourite = cat["favourite"] if "favourite" in cat else False

            if "died_by" in cat or "scar_event" in cat or "mentor_influence" in cat:
                new_cat.convert_history(
                    cat["died_by"] if "died_by" in cat else [],
                    cat["scar_event"] if "scar_event" in cat else [],
                )

            all_cats.append(new_cat)

        except KeyError as e:
            if "ID" in cat:
                key = f" ID #{cat['ID']} "
            else:
                key = f" at index {i} "
            game.switches[
                "error_message"
            ] = f"Cat{key}in clan_cats.json is missing {e}!"
            game.switches["traceback"] = e
            raise

    # replace cat ids with cat objects and add other needed variables
    for cat in all_cats:
        cat.load_conditions()

        # this is here to handle paralyzed cats in old saves
        if cat.pelt.paralyzed and "paralyzed" not in cat.permanent_condition:
            cat.get_permanent_condition("paralyzed")
        elif "paralyzed" in cat.permanent_condition and not cat.pelt.paralyzed:
            cat.pelt.paralyzed = True

        # load the relationships
        try:
            if not cat.dead:
                cat.load_relationship_of_cat()
                if cat.relationships is not None and len(cat.relationships) < 1:
                    cat.init_all_relationships()
            else:
                cat.relationships = {}
        except Exception as e:
            logger.exception(
                f"There was an error loading relationships for cat #{cat}."
            )
            game.switches[
                "error_message"
            ] = f"There was an error loading relationships for cat #{cat}."
            game.switches["traceback"] = e
            raise

        cat.inheritance = Inheritance(cat)

        try:
            # initialization of thoughts
            cat.thoughts()
        except Exception as e:
            logger.exception(
                f"There was an error when thoughts for cat #{cat} are created."
            )
            game.switches[
                "error_message"
            ] = f"There was an error when thoughts for cat #{cat} are created."
            game.switches["traceback"] = e
            raise

        # Save integrety checks
        if conf.game_config["save_load"]["load_integrity_checks"]:
            save_check()


def csv_load(all_cats):
    if game.switches["clan_list"][0].strip() == "":
        save_file_contents = ""
    else:
        if os.path.exists(
                get_save_dir() + "/" + game.switches["clan_list"][0] + "cats.csv"
        ):
            with open(
                    get_save_dir() + "/" + game.switches["clan_list"][0] + "cats.csv",
                    "r",
                    encoding="utf-8",
            ) as read_file:
                save_file_contents = read_file.read()
        else:
            with open(
                    get_save_dir() + "/" + game.switches["clan_list"][0] + "cats.txt",
                    "r",
                    encoding="utf-8",
            ) as read_file:
                save_file_contents = read_file.read()


def save_check():
    """Checks through loaded cats, checks and attempts to fix issues
    NOT currently working."""
    return

    for cat in Cat.all_cats:
        cat_ob = Cat.all_cats[cat]

        # Not-mutural mate relations
        # if cat_ob.mate:
        #    _temp_ob = Cat.all_cats.get(cat_ob.mate)
        #    if _temp_ob:
        #        # Check if the mate's mate feild is set to none
        #        if not _temp_ob.mate:
        #            _temp_ob.mate = cat_ob.ID
        #    else:
        #        # Invalid mate
        #        cat_ob.mate = None


def clangen_version_convert(version_info):
    """ Does all save-conversion that require referencing the saved version number.
    This is a separate function, since the version info is stored in clan.json, but most conversion needs to be
    done on the cats. Clan data is loaded in after cats, however. """

    if version_info is None:
        return

    if version_info["version_name"] == SAVE_CLANGEN_VERSION_NUMBER:
        # Save was made on current version
        return

    if version_info["version_name"] is None:
        version = 0
    else:
        version = version_info["version_name"]

    if version < 1:
        # Save was made before version number storage was implemented.
        # (ie, save file version 0)
        # This means the EXP must be adjusted.
        for c in Cat.all_cats.values():
            c.experience = c.experience * 3.2

    if version < 2:
        for c in Cat.all_cats.values():
            for con in c.injuries:
                moons_with = 0
                if "moons_with" in c.injuries[con]:
                    moons_with = c.injuries[con]["moons_with"]
                    c.injuries[con].pop("moons_with")
                c.injuries[con]["moon_start"] = game.clan_obj.age - moons_with

            for con in c.illnesses:
                moons_with = 0
                if "moons_with" in c.illnesses[con]:
                    moons_with = c.illnesses[con]["moons_with"]
                    c.illnesses[con].pop("moons_with")
                c.illnesses[con]["moon_start"] = game.clan_obj.age - moons_with

            for con in c.permanent_condition:
                moons_with = 0
                if "moons_with" in c.permanent_condition[con]:
                    moons_with = c.permanent_condition[con]["moons_with"]
                    c.permanent_condition[con].pop("moons_with")
                c.permanent_condition[con]["moon_start"] = game.clan_obj.age - moons_with

    if version < 3 and game.clan_obj.freshkill_pile:
        # freshkill start for older clans
        add_prey = game.clan_obj.freshkill_pile.amount_food_needed() * 2
        game.clan_obj.freshkill_pile.add_freshkill(add_prey)


def clansim_version_convert():
    """ """
    pass

