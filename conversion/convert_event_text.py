# convert_event_text.py

# TODO need to keep track of cats

# %{moon} -> I need to see this one personally
# %{join_age} -> {CAT/main/hist.birth/moon}
# %{birth_moon} -> {CAT/main/hist.birth/moon}
# %{birth_season} -> {CAT/main/hist.birth/season}
# PRONOUN/m_c/ -> PRONOUN/main/
# VERB/m_c/ -> VERB/main/
# %{influence}
# %{honor}
# %{mentors}
# %{apprentices}
# %{age}
# %{cardinal}

# Possible codes for cat_code:
#     "m_c": _r,  # main cat
#     "r_c": _r,  # a random cat
#     "r_c1": _r,  # a random cat
#     "r_c2": _r,  # a random cat
#     "n_c": _r,  # newly generated cat
#     "app1": _r,  # a random cat with an apprentice rank
#     "app2": _r,  # a random cat with an apprentice rank
#     "app3": _r,  # a random cat with an apprentice rank
#     "app4": _r,  # a random cat with an apprentice rank
#     "app5": _r,  # a random cat with an apprentice rank
#     "app6": _r,  # a random cat with an apprentice rank
#     "p_l": _r,  # patrol leader
#     "s_c": _r,  # skilled cat - a cat who meets a specific stat_skill requirement
#     "(mentor)": _r,  # m_c's current mentor
#     "l_n": _r,  # m_c's Clan leader's name
#     "dead_par1": _r,  # a random dead cat who was once m_c's partner
#     "dead_par2": _r,  # a random dead cat who was once m_c's partner
#     "p1": _r,  # a random cat who is m_c's partner
#     "p2": _r,  # a random cat who is m_c's partner
#     "(deadmentor)": _r,  # a random dead cat who was once m_c's mentor
#     "(previous_mentor)": _r,  # a random living cat who was once m_c's mentor
#     "mur_c": _r,  # a random dead cat who m_c murdered
#     "c_n": _r,  # Clan name
#     "o_c_n": _r,  # other Clan name
#     "lead_name": _r,  # m_c's Clan leader
#     "dep_name": _r,  # m_c's Clan deputy
#     "med_name": _r,  # a random cat who is a medicine cat in m_c's Clan
#     "cat_tag": _r,


# scripts.cat.pelts.Pelt.check_and_convert
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
pass