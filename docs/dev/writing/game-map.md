# Game Map

It's a 10x10 tilemap. Each tile has:
- a biome


| Terrain     | Biome       | Adjacent Tiles                                              | Camp        | ClanGen Biome |
|-------------|-------------|-------------------------------------------------------------|-------------|---------------|
| Ruins       | Twolegplace | 0 Twolegplace<br>at least 5 mountains                       | ruins       | mountainous   |
| Twolegplace | Twolegplace | any                                                         | n/a         | n/a           |
| Ocean       | Water       | exactly 3 land tiles<br>water otherwise                     | n/a         | n/a           |
| River       | Water       | at least 3 land<br> at least 2 water                        | n/a         | n/a           |
| Lake        | Water       | at most 3 water<br>land otherwise                           | n/a         | n/a           |
| Beach       | Sand        | exactly 3 water<br>land otherwise                           | beach       | beach         |
| Tidal Cave  | Sand        | at least 1 beach<br>at least 2 mountain<br>at least 3 water | tidal cave  | beach         |
| Desert      | Sand        | at least 4 sand<br>land otherwise                           | desert      | plains        |
| Plains      | Grass       | at least 3 grass<br>at most 2 water                         | grasslands  | plains        |
| Wastelands  | Grass       | at least 2 Twolegplace<br>at least 4 grass                  | wastelands  | plains        |
| Quarry      | Mountain    | at least 1 Twolegplace<br>at least 3 mountain               | quarry      | mountainous   |
| Fjord       | Mountain    | exactly 3 water<br>exactly 5 mountain                       | fjord       | mountainous   |
| Rocky Slope | Mountain    | 0 water<br>at least 3 mountain<br>at least 3 forest         | rocky slope | mountainous   |
| Cliff       | Mountain    | 0 water<br>at least 3 mountain<br>at least 3 grass          | cliff       | mountainous   |
| Lakeside    | Trees       | at most 3 water<br>forest otherwise                         | lake        | forest        |
| Oak         | Trees       | forest or grass                                             | classic     | forest        |
| Pine        | Trees       | forest or mountain                                          | gully       | forest        |
| Taiga       | Trees       | 0 water<br>only mountain or forest                          | taiga       | forest        |
| Grotto      | Trees       | 0 trees                                                     | grotto      | forest        |
| Marsh       | Wetland     | exactly 3 or 5 water<br>mostly grass otherwise              |             | wetland       |
| Swamp       | Wetland     | exactly 3 or 5 water<br>mostly trees otherwise              |             | wetland       |
| Floodplain  | Wetland     | exactly 3 or 5 water<br>mostly sand otherwise               |             | wetland       |
|             | Wetland     |                                                             |             |               |


## Generation

1 generate water
2 line water with sand, but do not replace mountains
3 randomly place Twolegplaces, but do not place more than 2 and do not replace water

| Terrain     | Allowed Adjacent Terrain              | Required Adjacent Terrain |
|-------------|---------------------------------------|---------------------------|
| Water       | Grass, Mountain, Sand, Trees, Wetland |                           |
| Sand        | Grass, Water, Wetland                 |                           |
| Grass       | Mountain, Sand, Trees, Water, Wetland |                           |
| Mountain    | Grass, Trees, Water                   |                           |
| Wetland     | Grass, Sand, Trees                    | Water, Wetland            |
| Trees       |                                       |                           |
| Twolegplace | Twolegplace, Any                      |                           |

For every tile, there's an 80% chance of the next tile having the same terrain.
For every non-water tile, there's a 10% chance of Twolegplace terrain, a 




- beach
- forest
- mountain
- plains

- desert
- wetlands
