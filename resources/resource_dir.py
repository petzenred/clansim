# resource_dir.py

from enum import Enum, StrEnum

_RESOURCES_PATH: str = "resources/"

class Resource(StrEnum):
    """ Keeps track of the different resource dictionaries the game can load from files. """

    Herbs = _RESOURCES_PATH + "dicts/herb_info.json"
    ClanSymbol = _RESOURCES_PATH + "dicts/clan_symbol_sprite_data.yaml"
    Backstories = _RESOURCES_PATH + "dicts/backstories.json"
    TraitRanges = _RESOURCES_PATH + "dicts/traits/trait_ranges.json"

    @property
    def path(self):
        return self.value
