from definitions import (
  PeltColour, ColourTint, WhitePatchPattern, PeltPattern,
  ScreenName, WhitePatchPatternCategory, EyeColour, ScarPelt, ScarCategory
)

WHITE_PATCH_PATTERN_CATEGORY_TEXT = {
  WhitePatchPatternCategory.Point: "darker paws, tail, and face" # also works for WhitePatchPattern.Bleached
}

WHITE_PATCH_PATTERN_TEXT = {
  WhitePatchPattern.Vitiligo: "dots of differently-coloured fur",
  WhitePatchPattern.VitiligoTwo: "white patches spotted along {PRONOUN/main/poss} back",
  WhitePatchPattern.Moon: "a white tailtip, ears, and paws",
  WhitePatchPattern.Phantom: "a patch of white fur over one eye",
  WhitePatchPattern.Karpati: "a white nose, tail, ears, and paws",
  WhitePatchPattern.Powder: "dusted white fur on their face and back",
  WhitePatchPattern.Smokey: "white speckles"
}

PELT_COLOUR_TEXT = {
  PeltColour.White: "white",
  PeltColour.PaleGrey: "light grey",
  PeltColour.Silver: "silver",
  PeltColour.Grey: "blue",
  PeltColour.DarkGrey: "dark grey",
  PeltColour.Ghost: "grey",
  PeltColour.Black: "black",
  PeltColour.Cream: "cream",
  PeltColour.PaleGinger: "pale ginger",
  PeltColour.Golden: "golden",
  PeltColour.Ginger: "ginger",
  PeltColour.DarkGinger: "flame-coloured",
  PeltColour.Sienna: "dark ginger",
  PeltColour.LightBrown: "pale",
  PeltColour.Lilac: "rosy grey",
  PeltColour.Brown: "light brown",
  PeltColour.GoldenBrown: "golden-brown",
  PeltColour.DarkBrown: "brown",
  PeltColour.Chocolate: "dark brown"
}

PELT_PATTERN_TEXT = {
  ScreenName.Profile: {
    PeltPattern.SingleColour: "solid",
    PeltPattern.Tabby: "tabby",
    PeltPattern.Marbled: "marbled tabby",
    PeltPattern.Rosette: "rosette",
    PeltPattern.Smoke: "smoke",
    PeltPattern.Ticked: "ticked",
    PeltPattern.Speckled: "speckled",
    PeltPattern.Bengal: "bengal tabby",
    PeltPattern.Mackerel: "mackerel tabby",
    PeltPattern.Classic: "classic tabby",
    PeltPattern.Sokoke: "sokoke tabby",
    PeltPattern.Agouti: "agouti",
    PeltPattern.SingleStripe: "dorsal stripe",
    PeltPattern.Masked: "masked tabby"
  },
  ScreenName.Allegiances: {
    PeltPattern.SingleColour: {
      "before_colour": "",
      "after_colour": "",
      "after_gender": ""
    },
    PeltPattern.Tabby: {
      "before_colour": "",
      "after_colour": "tabby",
      "after_gender": ""
    },
    PeltPattern.Speckled: {
      "before_colour": "speckled",
      "after_colour": "",
      "after_gender": ""
    },
    PeltPattern.Bengal: {
      "before_colour": "unusually-dappled",
      "after_colour": "",
      "after_gender": ""
    },
    PeltPattern.Marbled: {
      "before_colour": "",
      "after_colour": "tabby",
      "after_gender": ""
    },
    PeltPattern.Ticked: {
      "before_colour": "",
      "after_colour": "",
      "after_gender": "with darker flecks"
    },
    PeltPattern.Smoke: {
      "before_colour": "smoky",
      "after_colour": "",
      "after_gender": ""
    },
    PeltPattern.Mackerel: {
      "before_colour": "",
      "after_colour": "tabby",
      "after_gender": ""
    },
    PeltPattern.Classic: {
      "before_colour": "",
      "after_colour": "tabby",
      "after_gender": ""
    },
    PeltPattern.Agouti: {
      "before_colour": "",
      "after_colour": "tabby",
      "after_gender": ""
    },
    PeltPattern.SingleStripe: {
      "before_colour": "",
      "after_colour": "",
      "after_gender": "with a darker stripe running down {PRONOUN/main/poss} back"
    },
    PeltPattern.Rosette: {
      "before_colour": "unusually-spotted",
      "after_colour": "",
      "after_gender": ""
    },
    PeltPattern.Sokoke: {
      "before_colour": "",
      "after_colour": "tabby",
      "after_gender": ""
    },
    PeltPattern.Masked: {
      "before_colour": "masked",
      "after_colour": "tabby",
      "after_gender": ""
    }
  }
}

EYE_COLOUR_TEXT = {
  # Yellow eyes - high pigmentation
  EyeColour.Yellow: "yellow",
  EyeColour.PaleYellow: "pale yellow",
  EyeColour.Amber: "amber",
  EyeColour.Orange: "orange",
  EyeColour.Gold: "gold",
  EyeColour.Copper: "copper",
  EyeColour.Bronze: "bronze",

  # Green eyes - medium pigmentation
  EyeColour.GreenYellow: "green-yellow",
  EyeColour.PaleGreen: "pale green",
  EyeColour.Hazel: "hazel",
  EyeColour.Green: "green",
  EyeColour.Sage: "sage",
  EyeColour.Emerald: "emerald",
  EyeColour.SunlitIce: "sunlit ice",

  # Blue eyes - low pigmentation
  EyeColour.Blue: "blue",
  EyeColour.DarkBlue: "dark blue",
  EyeColour.Cyan: "cyan",
  EyeColour.HeatherBlue: "heather blue",
  EyeColour.Cobalt: "cobalt",
  EyeColour.PaleBlue: "pale blue",

  EyeColour.Grey: "grey",
  EyeColour.Silver: "silver",
}

SCAR_TEXT = {
  ScarCategory: {
    ScarCategory.Burn: " with burn scarring",
    ScarCategory.Frostbite: " with frostbite scarring",
  },
  ScarPelt: [
    (ScarPelt.ScratchEye, " with a scar over one eye"),
    (ScarPelt.NoLeftEar, " missing one ear"),
    (ScarPelt.NoRightEar, " missing one ear"),
    (ScarPelt.NoEars, " missing both ears"),
    (ScarPelt.TornLeftEar, " with a torn ear"),
    (ScarPelt.TornRightEar, " with a torn ear"),
    (ScarPelt.NoPaw, " with a missing paw"),
    (ScarPelt.NoTail, " without a tail"),
    (ScarPelt.HalfTail, " with half a tail"),
  ]
}