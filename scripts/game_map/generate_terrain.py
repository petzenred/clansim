# generate_terrain.py
from enum import Enum
from random import choice


class Terrain(Enum):
    """The terrain class.

    Format for values is ("tile character",["allowed","adjacent","tiles"],["required","adjacent","tiles"])
    """
    GRASS = ("w",["GRASS","MOUNTAIN","SAND","TREES","WATER","WETLAND"],[])
    MOUNTAIN = ("M",["GRASS", "MOUNTAIN", "TREES", "WATER"],[])
    SAND = ("=",["GRASS","SAND","WATER","WETLAND"],[])
    TREES = ("A",["GRASS",""],[])
    # TWOLEGPLACE = ("22",[],[])
    WATER = ("~",[],[])
    WETLAND = ("o",["GRASS", "SAND", "TREES"],["WATER","WETLAND"])
        


def _generate_game_map(game_map_size: int) -> str:
    tile_options: list = list(Terrain.__members__.keys())
    _map = ""
    for x in range(game_map_size):
        for y in range(game_map_size):
            _map += Terrain.__members__[choice(tile_options)].value[0]
    return _map


def _get_adjacent_terrains(tile: Terrain):
    return choice(tile.value)


def _test():
    _print_map = '\n'
    _game_map_size_i = 10
    game_map = _generate_game_map(_game_map_size_i)
    print(len(game_map))
    for y in range(_game_map_size_i):
        for x in range(_game_map_size_i):
            print(f"{x},{y},{y + (x*_game_map_size_i)}")
            terrain = game_map[y + (x*_game_map_size_i)]
            _print_map += terrain*3
        _print_map += '\n'
    print(_print_map)
    return


_test()
