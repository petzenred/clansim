# pelt.en.py - Pelt-related text strings used very often.


pelt_layers = {
    1: { # pelt - a combination of pattern and base color
        "pattern": [
            "agouti", "bengal", "classic", "mackerel", "marbled", "masked",
            "rosette", "single_color", "single_stripe", "smoke", "sokoke",
            "speckled", "tabby", "ticked",
        ],
        "base_color": [
            "WHITE", "PALEGREY", "SILVER", "GREY", "DARKGREY", "GHOST",
            "BLACK", "CREAM", "PALEGINGER", "GOLDEN", "GINGER", "DARKGINGER",
            "SIENNA", "LIGHTBROWN", "LILAC", "BROWN", "GOLDEN-BROWN", "DARKBROWN", "CHOCOLATE"
        ]
    },
    2: { # possible tortie patch (mask)

    },
    3: { # possible white patch - a combination of white patches and tints
        "white_patch": [],
        "white_patch_tint": [ "none", "offwhite", "cream", "darkcream", "gray", "pink" ]
    },
    4: { # scars

    },
    5: { # eyes

    },
    6: { # lineart

    },
    7: { # skin

    },
    8: { # missing limb (mask)

    },
    9: { # accessories

        # New man-made accs (i.e. collars) must be made with the full range of colors. As of the
        # writing of this guide, these are:
        # ["CRIMSON", "BLUE", "YELLOW", "CYAN", "RED", "LIME", "GREEN", "RAINBOW","BLACK", "SPIKES", "WHITE", "PINK", "PURPLE", "MULTI", "INDIGO"]
        # Please reference existing sprite sheets to match colors as best as possible.

    },
}


PELTS = {
    "WHITE": {
        "one": "pale",
        "many": "pale"
    },
    "FULLWHITE": "white",
    "PALEGREY": {
        "one": "gray",
        "many": "pale gray"
    },
    "SILVER": {
        "one": "silver",
        "many": "silver"
    },
    "GREY": {
        "one": "gray",
        "many": "gray"
    },
    "DARKGREY": {
        "one": "gray",
        "many": "dark gray"
    },
    "GHOST": {
        "one": "black",
        "many": "black"
    },
    "BLACK": {
        "one": "black",
        "many": "black"
    },
    "CREAM": {
        "one": "cream",
        "many": "cream"
    },
    "PALEGINGER": {
        "one": "ginger",
        "many": "pale ginger"
    },
    "GOLDEN": {
        "one": "golden",
        "many": "golden"
    },
    "GINGER": {
        "one": "ginger",
        "many": "ginger"
    },
    "DARKGINGER": {
        "one": "ginger",
        "many": "dark ginger"
    },
    "SIENNA": {
        "one": "ginger",
        "many": "dark ginger"
    },
    "LIGHTBROWN": {
        "one": "brown",
        "many": "light brown"
    },
    "LILAC": {
        "one": "brown",
        "many": "light brown"
    },
    "BROWN": {
        "one": "brown",
        "many": "brown"
    },
    "GOLDEN-BROWN": {
        "one": "brown",
        "many": "golden brown"
    },
    "DARKBROWN": {
        "one": "brown",
        "many": "dark brown"
    },
    "CHOCOLATE": {
        "one": "brown",
        "many": "dark brown"
    },
    "SingleColour": "single color",
    "SingleColour_long": "%{color}",
    "TwoColour": "two color",
    "TwoColour_long": "%{color}",
    "Tabby": "tabby",
    "Tabby_long": "%{color} tabby",
    "Speckled": "speckled",
    "Speckled_long": "speckled %{color}",
    "Bengal": "bengal",
    "Bengal_long": "unusually dappled %{color}",
    "Marbled": "marbled",
    "Marbled_long": "%{color} tabby",
    "Ticked": "ticked",
    "Ticked_long": "%{color} ticked",
    "Smoke": "smoke",
    "Smoke_long": "%{color} smoke",
    "Mackerel": "mackerel",
    "Mackerel_long": "%{color} tabby",
    "Classic": "classic",
    "Classic_long": "%{color} tabby",
    "Agouti": "agouti",
    "Agouti_long": "%{color} tabby",
    "Singlestripe": "single-striped",
    "Singlestripe_long": "dorsal-striped %{color}",
    "Rosette": "Rosette",
    "Rosette_long": "unusually spotted %{color}",
    "Sokoke": "Sokoke",
    "Sokoke_long": "%{color} tabby",
    "Masked": "Masked",
    "Masked_long": "masked %{color} tabby",
    "Calico": "calico",
    "Calico_tabby": "calico tabby",
    "Tortie": "tortie",
    "Tortie_tabby": "tortie tabby",
    "mottled": "mottled",
    "mottled_long": "%{color} mottled",
    "point": "%{color} point",
    "NOTAIL": "no tail",
    "HALFTAIL": "half a tail",
    "NOPAW": "three legs",
    "NOLEFTEAR": "a missing ear",
    "NORIGHTEAR": "a missing ear",
    "NOEAR": "no ears",
    "vitiligo": "vitiligo",
    "long_furred": "long-furred",
    "scarred": "scarred",
    "fur_short": "short",
    "fur_medium": "medium",
    "fur_long": "long"
}
