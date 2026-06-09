# red_convert_cat.py - Functions for converting cats from old saves.

def convert_clangen_pelt(pelt_cd: dict, old_pelt_dict: dict) -> dict:
    """

    :param dict pelt_cd: the pelt section on the conversion dictionary YAML file
    """
    # TODO first, run this through the old Pelt class's Pelt.check_and_convert. That way, this function only ever needs to be concerned converting from the most modern version of ClanGen
    new_pelt_dict = {} # this will be passed to a CatPelt object as the parameter 'save_file'

    # PELT LENGTH
    new_pelt_dict["length"] = old_pelt_dict["pelt_length"]

    # EYE COLOUR
    if old_pelt_dict["eye_colour"] in pelt_cd["eye_colour"]:
        _ = pelt_cd["eye_colour"][old_pelt_dict["eye_colour"]]
    else:
        _ = old_pelt_dict["eye_colour"]
    new_pelt_dict["eye_colour"] = (_, _)
    # if the cat is heterochromatic, make sure that's accounted for
    if old_pelt_dict["eye_colour2"]:
        if old_pelt_dict["eye_colour2"] in pelt_cd["eye_colour"]:
            new_pelt_dict["eye_colour"][1] = pelt_cd["eye_colour"][old_pelt_dict["eye_colour2"]]

    # WHITE PATCHES
    # if the cat has vitiligo or is a point, white_patches will be None
    _ = None
    if old_pelt_dict["white_patches"] != "none":
        _ = old_pelt_dict["white_patches"]
    elif old_pelt_dict["vitiligo"]:
        _ = old_pelt_dict["vitiligo"]
    elif old_pelt_dict["vitiligo_markings"]:
        _ = old_pelt_dict["vitiligo_markings"]
    elif old_pelt_dict["points"]:
        _ = old_pelt_dict["points"]
    elif old_pelt_dict["point_markings"]:
        _ = old_pelt_dict["point_markings"]
    # convert old white patches
    if _ in pelt_cd["white_patches"]:
        _ = pelt_cd["white_patches"][_]
    new_pelt_dict["white_patches"] = _

    # PATTERNS, COLOURS, AND TORTOISESHELLS
    # first, handle the only thing that doesn't change between torties and non-torties
    if old_pelt_dict["pelt_color"] in pelt_cd["fur_colour"]:
        new_pelt_dict["colour"] = pelt_cd["fur_colour"][old_pelt_dict["pelt_color"]]
    else:
        new_pelt_dict["colour"] = old_pelt_dict["pelt_color"]

    # second, handle everything else
    if old_pelt_dict["pelt_name"].casefold() == "tortie":
        # pattern
        # Note that although ClanGen saved different patterns for the base coat and the tortie patches, they were always the same, so ClanSim doesn't bother
        _ = pelt_cd["pattern"]

        # tortie colour
        if old_pelt_dict["tortie_color"] in pelt_cd["fur_colour"]:
            tortie_colour = pelt_cd["fur_colour"][old_pelt_dict["tortie_color"]]
        else:
            tortie_colour = old_pelt_dict["tortie_color"]

        # tortie patches
        if old_pelt_dict["pattern"] in pelt_cd["fur_colour"]:
            tortie_patches = pelt_cd["tortie_patches"][old_pelt_dict["pattern"]]
        else:
            tortie_patches = old_pelt_dict["pattern"]
    else:
        _ = old_pelt_dict["pelt_name"]
        tortie_colour = None
        tortie_patches = None

    if _ in pelt_cd["pattern"]:
        pattern = pelt_cd["pattern"][_]
    else:
        pattern = _
    new_pelt_dict["tortie_colour"] = tortie_colour
    new_pelt_dict["pattern"] = pattern
    new_pelt_dict["tortie_patches"] = tortie_patches

    # SKIN COLOUR
    if old_pelt_dict["skin"] in pelt_cd["skin_colour"]:
        new_pelt_dict["skin_colour"] = pelt_cd["skin_colour"][old_pelt_dict["skin"]]
    else:
        new_pelt_dict["skin_colour"] = old_pelt_dict["skin"]

    # TINTS
    new_pelt_dict["colour_tint"] = old_pelt_dict["tint"]
    new_pelt_dict["white_patch_tint"] = old_pelt_dict["white_patches_tint"]

    # SPRITES
    sprites: dict = {
        "reverse": bool(old_pelt_dict["reverse"]),
        "kitten": int(old_pelt_dict["sprite_kitten"]),
        "adolescent": int(old_pelt_dict["sprite_adolescent"]),
        "adult": int(old_pelt_dict["sprite_adult"]),
        "senior": int(old_pelt_dict["sprite_senior"]),
        "opacity": int(old_pelt_dict["opacity"])
    }
    new_pelt_dict["sprite"] = sprites

    # SCARS AND ACCESSORIES
    new_pelt_dict["scars"] = old_pelt_dict["scars"]
    new_pelt_dict["accessories"] = old_pelt_dict["accessory"]

    return new_pelt_dict