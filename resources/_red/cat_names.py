# cat_names.py - Names that cats can have. This is a Python file, not a YAML file, to
#                   prevent initialization errors in the RedName class.

########################################################################################################################
# Imports
########################################################################################################################

from definitions import (
    Rank,
    Biome, EyeColour, PeltColour, PeltPattern, RedSkill, TortiePatches, WhitePatches, Season,
)


########################################################################################################################
# Constants
########################################################################################################################

SPECIAL_NAMES: str = "special_ranks_and_suffixes"

OTHER: dict = {
    "blacklist": ["silverpelt",  # this is the Clans' name for the night sky
                  "greenleaf",  # this is the Clans' name for summer
                  "leaffall",  # this is the Clans' name for autumn
                  "leafbare", # this is the Clans' name for winter
                  "newleaf", # this is the Clan's name for spring
                  "blackface",
                  "brownface",
                  "molesting",
                  "pancakeface",
                  "redface",
                  "wetback",
                  "yellowbone",
                  "yellowface",],
    SPECIAL_NAMES: {
      Rank.Leader: "star",
      Rank.MediatorApp: "paw",
      Rank.HealerApp: "paw",
      Rank.WarriorApp: "paw",
      Rank.QueenApp: "paw",
      Rank.Kit: "kit",},
    "animal_parts": ["Addax", "Adder", "Albatross", "Alligator", "Alpaca", "Ant", "Antelope", "Aphid", "Avocet",
                     "Axolotl",

                     "Badger", "Barracuda", "Bass", "Bat", "Bear", "Beaver", "Bee", "Beetle", "Beluga", "Bird",
                     "Bison", "Bittern", "Boar", "Buck", "Buffalo", "Bug", "Bumble", "Butterfly",

                     "Camel", "Canary", "Caracal", "Caribou", "Carp", "Caterpillar", "Chaffinch", "Chamois",
                     "Cheetah", "Chick", "Cicada", "Civet", "Clam", "Coati", "Cobra", "Cod", "Condor", "Coral",
                     "Cormorant", "Cougar", "Cow", "Coyote", "Crab", "Crane", "Crayfish", "Crocodile", "Crow",
                     "Cub", "Cuckoo", "Curlew", "Cygnet",

                     "Darner", "Deer", "Dingo", "Doe", "Dog", "Dolphin", "Dove", "Duck",

                     "Eagle", "Egret", "Elk", "Ermine", "Ewe",

                     "Falcon", "Fawn", "Fennec", "Ferret", "Finch", "Fish", "Fox", "Frog",

                     "Gander", "Gannet", "Gar", "Gazelle", "Goat", "Goose", "Gosling", "Grackle", "Grayling", "Grebe",

                     "Grouse", "Gull", "Guppy",

                     "Hare", "Harrier", "Hawk", "Heron", "Hornet", "Horse", "Hound",

                     "Ibis",

                     "Jackal", "Jackdaw", "Jackrabbit", "Jay", "Jellyfish", "Jerboa", "Junco",

                     "Kestrel", "Kingfisher", "Kite",

                     "Lamb", "Lark", "Leopard", "Lion", "Lizard", "Loach", "Locust", "Lynx",

                     "Magpie", "Mamba", "Mantis", "Marlin", "Marten", "Meerkat", "Midge", "Mink", "Minnow",
                     "Mite", "Mole", "Monkey", "Moorhen", "Moose", "Mosquito", "Moth", "Mouse",

                     "Newt", "Nightingale",

                     "Octopus", "Orca", "Oriole", "Oryx", "Osprey", "Otter", "Owl",

                     "Panther", "Parrot", "Partridge", "Pelican", "Perch", "Pheasant", "Pig", "Pigeon", "Pike",
                     "Pipit", "Pronghorn", "Python",

                     "Quail",

                     "Rabbit", "Raccoon", "Ram", "Rat", "Raven", "Roach", "Robin",

                     "Sable", "Salamander", "Salmon", "Sardine", "Scorpion", "Seabass", "Seagull", "Serpent",
                     "Shark", "Sheep", "Shrew", "Shrike", "Skink", "Skunk", "Slug", "Snail", "Snake", "Sparrow",
                     "Spider", "Spoonbill", "Squid", "Squirrel", "Stag", "Starling", "Stoat", "Stork", "Swallow",
                     "Swan",

                     # taipans are a kind of snake that lives in desert
                     "Tadpole", "Taipan", "Tarantula", "Thrush", "Tiger", "Toad", "Tortoise", "Trout", "Turtle",
                     "Viper", "Vixen", "Vole", "Vulture",
                     "Warbler", "Wasp", "Weasel", "Weevil", "Whale", "Wolf", "Wolverine", "Worm", "Wren",
                     "Yak",

                     # SUFFIXES
                     "badger", "bat", "bear", "bee", "beetle", "bird", "bug", "bumble",
                     "cricket",
                     "deer",
                     "eagle", "elk",
                     "falcon", "fawn", "fish", "fox",
                     "goose",
                     "hare", "hawk", "horse",
                     "jay",
                     "kestrel", "kite",
                     "lamb", "leopard", "lion",
                     "minnow", "moth", "mouse",
                     "newt",
                     "ram", "raven", "roach",
                     "scorpion", "sheep", "snake", "spider", "squid", "swan",
                     "thrush", "tiger", "turtle", ],
    # TODO plant parts
}

OUTSIDERS: dict = {
    Rank.Kittypet: [
    "Agent Smith", "Ah", "Ah ha", "Alaska", "Apple Cider", "Apple Pencil", "Aphrodite", "Archimedes", "Aquarius",
    "Antares", "Anubis", "Aries", "Armageddon", "Arcturus", "Artificer", "Artemis", "Asgore", "Asriel", "Atlas",
    "Award Winning Smile", "Azimuth", "Azula", "Azurite",

    "Baba Yaga", "Baby Dog", "Bacchus", "Backflip", "Bacon", "Bagel", "Baja Blast", "Baobei", "Baojin", "Baphomet",
    "Bastet", "Beanie", "Beanie Baby", "Beef Stroganoff", "Beesechurger", "Beatle", "Bellafide", "Bellatrix",
    "Bellibolt", "Beowulf", "Berlioz", "Betelgeuse", "Bibimbap", "Bidoof", "Big Mac", "Big Man", "Big Papa Huge Time",
    "Bill Bailey", "Biscuits B. Bakin", "Biscuit", "Bismuth", "Black Widow", "Blahaj", "Blade", "Blinky Stubbins",
    "Blitzo", "Bob-omb", "Bohr Model", "Bok Choy", "Bologna", "Brandy", "Brandywine", "Boots", "Brick", "Brioche",
    "Broccoli", "Brooklyn", "Brother Dubious", "Burgermeister", "Burger Master", "Burning Skies", "Business Frog",
    "Bustopher Jones",

    "Cake", "Calamari", "Call of Greatness", "Call of the Void", "Calorimetry", "Crunchwrap", "Cyndaquil",
    "Cocoa", "Cupid", "Cocoa Puff", "Cookie", "Covalent", "Covalent Bond", "Confetti", "Canned Beans",
    "Constructive Criticism", "Coffee", "Cola", "Colby Jack", "Colin Robinson", "Cinnabon", "Circe", "Clicker",
    "Chiquito", "Cleffa", "Clawdette", "Canned Tuna", "Churro", "Chocolate", "Chocolate Chip", "Chocolate Pudding",
    "Choccie", "Choo-Choo", "Chorizo", "Cherubi", "Chikorita", "Chief", "Cannelloni", "Cannoli", "Chef",
    "Chekhov's Gun", "Chekov", "Cheesecake", "Cheesepuff", "Cheeto", "Cheeto Puff", "Cheetoman", "Captain",
    "Captain Curly", "Car Alarm", "Cheese Beast", "Cashmere", "Capricorn", "Cracked Earth",

    "Dust Bunny", "Dusty Cuddles", "Deep Dish Pizza", "Danger Dave", "Deimos", "Deino", "Dakrai", "Daisy Mae",
    "Duke", "Distinguished Gentleman", "Duchess", "Dr. Strange", "Double Trouble", "Doctor Who", "Doofenshmirtz",
    "Demeter", "Dimitrescu",

    "Egypt", "Ender Dragon", "Etoile", "Europa", "Espeon", "Espresso", "Espurr", "Electron", "Electronegativity",
    "Evilface", "Exothermic", "Exothermic Reaction", "Extra Cuddles", "Endless Reflections", "Endothermic", "Enthalpy",
    "Entropy", "Endothermic Reaction",

    "Fennekin", "First Generation iPod", "Fridge", "Fuecoco", "Furby", "Fuzz Lightyear", "Frita", "Failnaught",
    "Frito", "French", "Fruity Pebble", "Frumpkin", "French Fry", "Freya", "Fireball", "Five Pebbles", "Formal",
    "Formality", "Four Needles", "Foghettaboutit", "Fran Bow", "Formal Charge", "Firecracker", "Fairy", "Fax Machine",
    "Fairytale",

    "Gigabyte", "Gimli", "Growlithe", "Grunkle Stan", "Gold Foil Experiment", "Goomy", "Goryo", "Gouda", "Gourmand",
    "Good Sir", "Gnocchi", "Gilded Lily", "Gemelli", "Gemini", "General Erasmus Dickinson", "Ganiru", "Guacamole",

    "Hocus Pocus", "Heat Capacity", "Hot Sauce", "Habanero", "Habibi", "Helios", "Heisenberg", "Hercules", "Harlequin",
    "Hatsune Miku", "Halcyon", "Haiku", "Hale-Bopp", "Halloween",

    "Itsy Bitsy", "Inspector", "Iron Man", "Ice Cube", "Ice Spice", "Icecube", "Icee", "Ion", "Ionic Compound",

    "Jeep Wrangler", "Jirachi", "Jolly Rancher", "Jelly Jam",
    "Jennyanydots", "Jigsaw", "Jiminy Cricket", "Jellylorum", "Jellybean", "Jake Gyllenpaws", "Jaylen", "Jelly",

    "Kitty", "Kitty Cat", "Kombucha", "Klondike", "Kitty Softpaws", "Kid Cat", "Kagamine Len", "Kagamine Rin",
    "Kelloggs", "Ketchup", "Ketsl", "Kettlingur",

    "Luchasaurus", "Lucifur", "Lugnut", "Luxio", "Luci-Purr", "Lunchbox", "Lilleplutt", "Limiting Reactant",
    "Little Baby", "Little Caesar", "Little Ghost", "Little Guy", "Little Lady", "Little Man", "Little My",
    "Little Nicky", "Little One", "Lil Baby", "Lemon Boy", "Lawn Mower", "Lady Figment", "Lady Liberty",

    "Mudkip", "Meowzart", "Meowyman", "Molly", "McFlurry", "McLovin", "Man With All The Answers", "McChicken",
    "Microwave", "Mr. Anderson", "Mr. Kitty", "Mr. Kitty Whiskers", "Mr. Midnight", "Mr. Mistoffolees", "Mr. Mustard",
    "Mr. Oreo", "Mr. President", "Mr. Princess", "Mr. Sir", "Mr. Whiskers", "Mr. Wigglebottom", "Mitochondria",
    "Miss Marple", "Molly Murder Mittens", "Missile Launcher", "Mitzy Moo Moo", "Midnight Goddess", "Mitsubishi",
    "Milky Way", "Meow-Meow", "Milhouse", "Mercedes", "Metal", "Metalloid", "Meowth", "Maleficent", "Magikarp",

    "Neptune", "Neapolitan", "Nephrite", "Nidorina", "Neuron", "Ninetales", "Ninja", "Nintendo", "Nintendo DS",
    "Nintendo Switch", "Neuroscientist", "Neutron", "Nefertiti", "Nebula", "Napkin",

    "Oshawott", "Obi Wan", "Oberon", "Old Deuteronomy", "Oopsy Dazey", "Octet", "Octet Rule", "Old Man Sam",

    "Porsche", "Pot Roast", "Pouncival", "Princess", "Pringle", "Private Eye", "Pong", "Pongo", "President",
    "President Blanket", "Ponyboy", "Pork Belly", "Porkchop", "Procyon",
    "Polyatomic", "Polyatomic Ion", "Polaris", "Pepperjack", "Pistol Star", "Ping Pong", "Pachirisu", "Pisces",
    "Pixel", "Pinkie Pie", "Plot Twist", "Playstation", "Pizza Place", "Pawmi", "Plague", "Plato", "Peter Pan",
    "Pharah", "Phasmo", "Pina Colada", "Peter Parker", "Pichu", "Pavlova", "Peeta",
    "Perrserker", "Peanut Butter", "Pequeno", "Perdito", "Peridot", "Periodic Table", "Periodic Trend",
    "Peanut Wigglebutt", "Padparadscha", "Paimon", "Pudding",

    "Queso Ruby", "Quantum Mechanics", "Quarter Pounder", "Quartermaster",
    "Rorschach", "Rick Astley", "Raptor", "Rum", "Riolu", "Ringo Starr", "Righteous Bread Pudding", "Rivulet",
    "Reeses Puff", "Refrigerator", "Rarity", "Rapunzel", "Ramattra", "Roomba",

    "Sherbet", "Shrimp Fried Rice", "Silvally", "Slushie", "Smoothie", "Smores",
    "Smile", "Sugar Plum", "Smiley", "Soos", "Symphony", "Sashimi", "Sagittarius", "Sage Marro",
    "Snickers", "Sweet Creature", "Sweet Leon", "Sweet Marmalade", "Stink Mink", "Stinkbutt", "Sotast", "Stardust",
    "Solanum", "Soleil", "Solstice", "Sriracha", "Sonic", "Snoots", "Sprigatito", "Soda Pop", "Snotlout", "Sophie",
    "Sorbet", "Sofanthiel", "Snom", "Sneakers", "Snufkin", "Snuggles", "Soap Bubbles", "Soccer Ball", "Snuttig",
    "Smarty Pants", "Shinx", "Shortbread", "Slurpuff", "Skrunkly", "Skitty", "Sapphire", "Sarabi", "Seven Of Nine",
    "Skittles", "Serengeti", "Scorpio", "Skyrim", "Scholar", "Sans", "Sangria",

    "Tabasco", "Taco Bell", "Toffee", "Torchic", "Tribble", "Trouble Nuggets", "Totoro", "Toph", "Tamagotchi",
    "Tractor", "Torque", "Toyota", "Toulouse", "Toxel", "Taillow", "Toastee", "Terabyte", "Triscuit",
    "Tomato Soup", "Titania", "Top Hat", "Tetris", "Tofu", "Togepi", "Thumbelina", "Tetromino", "Tnoy Karaxis",
    "Todd Howard", "Tin Man", "The Doctor", "The Garlic Lord", "Thermodynamics", "Times New Roman", "Timid Ninja",
    "The Narrator", "Tardis", "Teacup", "Synth", "Tabbytha", "Tantomile", "T-rex", "Tumblebrutus", "Twinkle Lights",

    "Umbreon", "Uncle Butter", "Undyne",

    "Void", "Void Walker", "Volkswagen", "Voltage", "Void Worm", "Vega", "Velociraptor", "Virgo", "Van Pelt", "Vaxx",
    "Valence Electron", "Victini",

    "Wagyu", "Waffle", "Warren Peace", "Wasabi", "Whiz Kid", "Wiggity Wacks", "Wigglebutt", "Wiggog Yrath", "Wizard",
    "Wolfe",

    "Yeet", "Yeeted", "Yippee", "Yokai", "Yoonmin", "Yooted",

    "Zekrom", "Zendaya", "Zenith", "Zenyatta", "Zion", "Zeraora", "Zorua",
],
    Rank.Loner: [
    "Abby", "Abigail", "Abuko", "Abyss", "Acacia", "Ace", "Adaliz", "Adam", "Admiral", "Adora", "Aether", "Agatha",
    "Agnes", "Aidan", "Aiden", "Akila", "Akilah", "Alastair", "Alba", "Albedo", "Albert", "Alberto", "Alcina", "Alcor",
    "Alcyone", "Aldrich", "Alec", "Alex", "Alexa", "Alfie", "Alfred", "Alfredo", "Algernon", "Alice", "Alien", "Alma",
    "Alonzo", "Alphonse", "Alphys", "Altair", "Alvin", "Amanda", "Amani", "Amaretto", "Amari", "Amaya", "Amber",
    "Amelia", "Amethyst", "Amigo", "Amir", "Amity", "Amongus", "Amor", "Amy", "Ana", "Anais", "Ananya", "Andrew",
    "Andromeda", "Angel", "Anita", "Anju", "Ankha", "Anya", "Apex", "Apple", "April", "Apu", "Arch", "Archibald",
    "Archie", "Ari", "Ariel", "Armin", "Arroyo", "Arusha", "Ashe", "Askari", "Aspen", "Astrid", "Atticus", "Aubrey",
    "August", "Augustus", "Aurora", "Ava", "Avellana", "Avery", "Axel", "Azizi",

    "Baby", "Badru", "Bagheera", "Bahati", "Baihu", "Bailey", "Baisel", "Barbatuques", "Baldie", "Baldwin", "Baliyo",
    "Baloo", "Bamboo", "Bandit", "Banshee", "Banzai", "Barbie", "Barker", "Barnaby", "Basil", "Bastion", "Bean",
    "Beetle", "Beans", "Beau", "Beauty", "Bebe", "Bede", "Bell", "Bella", "Belle", "Bellini", "Ben", "Benito",
    "Bennett", "Benny", "Bentley", "Beth", "Bethany", "Betsy", "Beverly", "Bianca", "Bibelot", "Bigwig", "Bill",
    "Billy", "Bingo", "Bingsu", "Binx", "Birb", "Bird of Paradise", "Birdie", "Bitey", "Bitnara", "Bixbite", "Bixby",
    "Blair", "Blaire", "Blanche", "Blavingad", "Bliklotep", "Blinky", "Blu", "Bluebell", "Bluebird", "Bluey", "Bob",
    "Boba", "Bobby", "Bokshiri", "Bolt", "Bombalurina", "Bombon", "Bonbon", "Bongo", "Boni", "Bonkers", "Bonnie",
    "Bonny", "Boo", "Boobear", "Booker", "Bren", "Brian", "Broom", "Bruce", "Bruno", "Brutus", "Bub", "Buchito",
    "Buddy", "Buffy", "Bugbear", "Bulgogi", "Bullwinkle", "Bumblebee", "Bun", "Bunga", "Bunny", "Burger", "Burm",
    "Buttercup", "Buttermilk", "Butternut", "Butters", "Butterscotch", "Byeol",

    "Caakiri", "Cadence", "Cady", "Caesar", "Callie", "Calliope", "Callisto", "Calvin", "Calypso", "Camilo",
    "Camouflage", "Campion", "Candi", "Candy", "Canela", "Canopus", "Capella", "Cappuccino", "Caramel", "Cardamom",
    "Cardboard", "Carlotta", "Carmen", "Carmin", "Carolina", "Caroline", "Carrie", "Casper", "Cassandra", "Cassidy",
    "Castor", "Cat", "Catalina", "Catie", "Catrick", "Catty", "Cauliflower", "Cayenne", "Cece", "Cecelia", "Celebi",
    "Celeste", "Celia", "Centauri", "Centipede", "Cerberus", "Ceres", "Chai", "Chance", "Chanel", "Chansey",
    "Chanterelle", "Chaos", "Chara", "Charcoal", "Chari", "Chariklo", "Charles", "Charlie", "Charlotte", "Charm",
    "Charon", "Chase", "Chayanne", "Checkers", "Cheddar", "Cheerio", "Cheese", "Cherry", "Cherub", "Cheshire",
    "Chester", "Chevre", "Chewie", "Chewy", "Chiaki", "Chibi", "Chica", "Chicco", "Chickpea", "Chihiro", "Chiku",
    "Chip", "Chispa", "Chloe", "Chris", "Chrissy", "Chub", "Cielo", "Cilantro", "Cinder", "Cinderblock", "Cirrus",
    "Civet", "Clementine", "Cleo", "Cleopatra", "Clifford", "Cloe", "Cloud", "Clover", "Clyde", "Coal", "Cobweb",
    "Cody", "Comet", "Comfy", "Conan", "Concrete", "Conk Crete", "Connie", "Cooper", "Coquito", "Coral", "Corazon",
    "Coriander", "Coricopat", "Corn", "Cosmo", "Courage", "Cowbell", "Cowboy", "Cozy", "Crab", "Cracker", "Cream",
    "Crema", "Crescent", "Crispy", "Crow", "Crumpet", "Crunchy", "Crystal", "Cubby", "Cullen", "Cupcake", "Curry",
    "Cutie", "Cybele", "Cyprus",

    "Daisuke", "Dakari", "Dakota", "Dali", "Daliah", "Dambi", "Dan", "Danbi", "Danchu", "Dandelion", "Dapper",
    "Darcy", "Darling", "Dasik", "Dave", "Dayo", "Dean", "Deirdre", "Deli", "Delilah", "Della", "Destiny", "Dewey",
    "Diablo", "Diallo", "Diamond", "Diana", "Diesel", "Digiorno", "Dinah", "Dino", "Diona", "Dipole", "Dipper",
    "Dirk", "Disco", "Diva", "Dixie", "Dizzy", "Djungelskog", "Dmitri", "Dobie", "Doc", "Dog", "Doja", "Dolly",
    "Domingo", "Dominic", "Domino", "Donald", "Donut", "Donuts", "Doodle", "Dori", "Dorian", "Dorothy", "Dova",
    "Draco", "Dragon", "Dragonfly", "Draugr", "Dreamy", "Ducky", "Dude", "Dulce", "Dumpling", "Dumpster", "Dune",
    "Dunnock", "Dwarf", "Dysnomia",

    "Eclipse", "Ed", "Eda", "Eddie", "Eden", "Edgar", "Edward", "Eepy", "Eevee", "Egg", "Einar", "Elden", "Eli",
    "Elijah", "Elio", "Ellie", "Elliot", "Elton", "Elvis", "Ember", "Emeline", "Emerald", "Emi", "Emilio", "Emma",
    "Emmet", "Emy", "Enchilada", "End", "Endless", "Enoki", "Envy", "Erebus", "Erica", "Eris", "Esker", "Esme",
    "Esther", "Eva", "Evangeline", "Eve", "Evelyn", "Everest", "Evie", "Ezra", "Fable", "Faizah", "Fallow", "Famine",
    "Fang", "Fauna", "Fawn", "Feather", "Feldspar", "Felicette", "Felicity", "Felix", "Feliz", "Fern", "Fernanda",
    "Ferret", "Ferry", "Feta", "Fig", "Figaro", "Filou", "Finch", "Finnian", "Firefly", "Fish", "Fisher", "Fishleg",
    "Fishtail", "Fiver", "Flabby", "Flamenco", "Flopper", "Flower", "Fluffy", "Flurry", "Flutie", "Fork", "Foxtrot",
    "Fran", "Frank", "Frankie", "Frannie", "Franny", "Fred", "Freddy", "Free", "Friend", "Frisk", "Frog", "Froggy",
    "Fry", "Frye", "Fudge", "Fuli", "Fuzzbo", "Fuzziwig",

    "Gabriel", "Gala", "Galahad", "Gamble", "Ganymede", "Garfield", "Gargoyle", "Garnet", "Gato", "Gayle", "Genji",
    "Geode", "George", "Ghost", "Gibby", "Gible", "Ginger", "Gingersnap", "Gir", "Girly Pop", "Gizmo", "Glameow",
    "Glass", "Glory", "Gluttony", "Gobi", "Godzilla", "Gofrette", "Goldfish", "Goose", "Grace", "Grain", "Grandpa",
    "Grass", "Grasshopper", "Grave", "Gravy", "Greed", "Gremlin", "Gretchen", "Grizabella", "Grizzly", "Guillermo",
    "Guinness", "Gumbo", "Gumi", "Gunnar", "Guppy", "Gus", "Gust", "Gustavo", "Guzma", "Gwendoline", "Gwyndolin",
    "Gwynn", "Gyoza", "Habika", "Hadar", "Haku", "Halmey", "Ham", "Hamburger", "Hamlet", "Hantu", "Hanzo",
    "Harmony", "Haru", "Harvest", "Harvey", "Havoc", "Hawkbit", "Hawkeye", "Haymitch", "Hazel", "Heathcliff",
    "Heather", "Hehe", "Heli", "Helix", "Henry", "Herbert", "Herc", "Hero", "Hershey", "Hex", "Hiccup", "Hickory",
    "Highness", "Hilbert", "Himiko", "Hiyoko", "Hlao", "Hobbes", "Hobohime", "Holly", "Honda", "Honeydew",
    "Honeysuckle", "Hop", "Hopper", "Horizon", "Hotdog", "Howdy", "Howler", "Hubert", "Hughie", "Hulk", "Human",
    "Humphrey", "Hunter", "Husker", "Hydra", "Hyeri", "Ice", "Iggy", "Igor", "Ike", "Ikea", "Illari", "Indi",
    "Indigo", "Iniko", "Insect", "Io", "Ipsy", "Isabel", "Isabella", "Isabelle", "Isaiah", "Izzy", "Jaakko", "Jack",
    "Jackal", "Jackie", "Jacko", "Jacques", "Jade", "Jae", "Jaffa", "Jaiden", "Jakada", "Jake", "Jalebi", "Jambo",
    "James", "Jamilah", "Janis", "Jasmine", "Jason", "Jasper", "Jattelik", "Jattematt", "Jaxon", "Jay", "Jemila",
    "Jenny", "Jerry", "Jesse", "Jessica", "Jessie", "Jester", "Jet", "Jethro", "Jetta", "Jewel", "Jewels", "Jim",
    "Jimmy", "Jinn", "Jinx", "Jitters", "Joanne", "John", "Johnny", "Joker", "Jolly", "Jonas", "Joob", "Jose",
    "Joy", "Jozi", "Jubie", "Judas", "Jude", "Judy", "Julie", "Juliet", "June", "Junkrat", "Juno", "Jupiter",

    "KD", "Kabuki", "Kaede", "Kai", "Kaia", "Kaito", "Kaizo", "Kale", "Kaleb", "Kamari", "Kamau", "Karen", "Kariba",
    "Karkinos", "Karma", "Kasha", "Kasi", "Kate", "Katjie", "Katniss", "Katy", "Keanu", "Keiko", "Kellas", "Ken",
    "Kendra", "Kenny", "Kenya", "Kepler", "Kerberos", "Kermit", "Kerry", "Kevin", "Keyboard", "Keziah", "Kianna",
    "Kiara", "Kibble", "Kiki", "Kimani", "Kimberly", "Kimchi", "King", "Kingston", "Kion", "Kip", "Kipling", "Kirby",
    "Kiriko", "Kisha", "Kismet", "Kivu", "Kiwi", "Klee", "Knorrig", "Knox", "Koala", "Koba", "Koda", "Kodi", "Kodiak",
    "Koi", "Kokichi", "Kokomi", "Kokum", "Komaru", "Kong", "Kovu", "Kramig", "Kudu", "Kuma", "Kuromi", "Kushi", "Kyle",
    "Kyoko", "Kyu",

    "L", "Laburnum", "Lacy", "Lady", "Ladybug", "Laika", "Laila", "Lakota", "Laksha", "Laku", "Lapis", "Laranjito",
    "Larch", "Larimar", "Lark", "Laszlo", "Latte", "Lavender", "Lawrence", "Lazarus", "Lazuli", "Leche", "Lee", "Leif",
    "Lemmy", "Lemon", "Leo", "Leon", "Leonardo", "Lester", "Levi", "Leviathan", "Levon", "Lex", "Li Shang", "Libra",
    "Lilac", "Lilith", "Lily", "Linden", "Lindsey", "Linguine", "Linzhi", "Lionel", "Litten", "Livlig", "Loaf", "Lobo",
    "Lobster", "Loca", "Lodesh", "Loki", "Lola", "Lollipop", "Lolly", "Lonardo", "London", "Loona", "Lora", "Lorado",
    "Louie", "Louis", "Lovebug", "Loyalty", "Luca", "Lucia", "Luciel", "Lucio", "Lucky", "Lucy", "Luigi", "Luke",
    "Lulu", "Lumi", "Lumine", "Luna", "Lupo", "Luz", "Lychee", "Lydia", "Lynzi", "Lyric",

    "Mabel", "Mac", "Macaroon", "Macavity", "Maddy", "Madi", "Madoka", "Maeve", "Maggie", "Magic", "Maiko", "Maize",
    "Majesty", "Makalu", "Makena", "Makini", "Mako", "Makoto", "Makula", "Makwa", "Malachite", "Mali", "Malia",
    "Malik", "Malika", "Mama", "Mamba", "Manda", "Mange", "Mango", "Mangosteen", "Mani", "Maomao", "Marathon",
    "Marble", "Marcel", "Marceline", "Marcy", "Mare", "Mareep", "Maria", "Marie", "Marina", "Mario", "Mariposa",
    "Mark", "Marlow", "Marny", "Mars", "Marshal", "Marshmallow", "Martha", "Martini", "Marula", "Mason", "Matador",
    "Matcha", "Mathias", "Matilda", "Mauga", "Maverick", "Mawuli", "Max", "Maxie", "May", "Maya", "Mazu", "Meatloaf",
    "Meatlug", "Medusa", "Meeka", "Megabyte", "Megan", "Meilin", "Meimei", "Melanie", "Melba", "Melody", "Melon",
    "Melona", "Memories Lost", "Mera", "Mercury", "Mercy", "Merengue", "Merlot", "Merry", "Mew", "Mia", "Miau",
    "Michelle", "Michi", "Mick", "Mieke", "Mikhail", "Mikumi", "Miles", "Milkshake", "Millie", "Milo", "Milque",
    "Mimas", "Mimi", "Mimikyu", "Mimzy", "Minette", "Minha", "Mini", "Minna", "Minnie", "Mint", "Minty", "Mira",
    "Miranda", "Miriam", "Miso", "Misty", "Mitaine", "Mitski", "Mittens", "Mitzi", "Miyun", "Mizan", "Mizar", "Mizu",
    "Mocha", "Mochi", "Moira", "Mojito", "Mojo", "Mollie", "Momo", "Monika", "Monster", "Monte", "Monzi", "Moo",
    "Moomin", "Moon", "Mop", "Mora", "Morb", "Morbius", "Mordred", "Morel", "Morpeko", "Morphius", "Morrhar", "Morty",
    "Mosaic", "Mosi", "Mowgli", "Moxie", "Mooncake", "Mozzarella", "Mucha", "Mufasa", "Muffet", "Muffy", "Mullido",
    "Mumbai", "Mungojerrie", "Munkustrap", "Murder", "Mushroom", "Mustard", "Myko", "Myler", "Mystic",

    "Nabi", "Nadia", "Nadir", "Nadja", "Nagi", "Nagito", "Nakala", "Nakeena", "Nala", "Namielle", "Namu", "Nandor",
    "Naomi", "Nari", "Neel", "Neil", "Nemo", "Neo", "Neobiani", "Ness", "Nessie", "Nevaeh", "Neytiri", "Nezuko",
    "Nibblenephim", "Nibbles", "Nibbly", "Nick", "Nightcat", "Nightmare", "Nikki", "Nile", "Niles", "Nimbus", "Nine",
    "Nirav", "Nirvana", "Nisha", "Nissan", "Nitro", "Nittany", "Niu", "Nix", "Nixie", "Noche", "Noelle", "Noir",
    "Noodle", "Noodlefly", "Nook", "Nori", "Norm", "Norman", "Nottingham", "Nova", "Nucleus", "Nugget", "Nuggets",
    "Nuka", "Nuri", "Nuru", "Nutella", "Nutmeg", "Nymph", "Nyx",

    "O'Leary", "Oakley", "Oapie", "Obsidian", "Octavia", "October", "Odetta", "Oleander", "Olga", "Oliva", "Oliver",
    "Ollie", "Omelet", "Omen", "Onion", "Onyx", "Oops", "Opal", "Ophelia", "Orbital", "Orchard", "Oregano", "Oreo",
    "Orion", "Orisa", "Oryx", "Orzo", "Oscar", "Oscypek", "Osiris", "Otto", "Outlaw", "Outsider", "Owen", "Ox",

    "Pablo", "Paella", "Pallas", "Paloma", "Pancake", "Pancho", "Panda", "Pandora", "Pango", "Pangur", "Panini",
    "Panko", "Paprika", "Papyrus", "Paquito", "Para", "Parhelion", "Pasha", "Pasta", "Patches", "Patience", "Paul",
    "Paulina", "Peach", "Peanut", "Pear", "Pearl", "Pecan", "Pekhult", "Peko", "Penny", "Peony", "Pepita", "Pepper",
    "Pepsi", "Periwinkle", "Perry", "Pesto", "Peter", "Petya", "Phantom", "Phoenix", "Photon", "Pichi", "Pickles",
    "Pierogi", "Pierre", "Pietro", "Piggy", "Pigment", "Pikachu", "Pillow", "Pineapple", "Ping", "Pinkie", "Pip",
    "Piper", "Pipkin", "Pippin", "Pipsqueak", "Pixie", "Pizza", "Plumeria", "Pluto", "Pochito", "Pocket", "Poe",
    "Poem", "Pokey", "Poki", "Pokotho", "Polka", "Polly", "Pompompurin", "Potato", "Prickle", "Pride", "Proton",
    "Puddles", "Pumba", "Pumpernickel", "Pumpkin", "Punchy", "Punk", "Purdy", "Purri", "Purry", "Pushee", "Puzzle",

    "Qilian", "Quagmire", "Quake", "Quartz", "Quasar", "Qubo", "Queen", "Queenie", "Queeny", "Querida", "Quesadilla",
    "Queso", "Quest", "Quickie", "Quimby", "Quince", "Quincy", "Quinn", "Quino", "Quinzee",

    "Rabiah", "Radar", "Rafael", "Rafiki", "Raja", "Ramble", "Ramen", "Ramon", "Randy", "Rani", "Rat", "Ratau",
    "Ratoo", "Rattle", "Raven", "Ravioli", "Ray", "Raymond", "Razzle", "Reaper", "Rebel", "Reese", "Regina", "Ren",
    "Renata", "Rhea", "Rhianna", "Rhubarb", "Ribosome", "Ricardo", "Rice", "Rico", "Ricotta", "Rigatoni", "Rigel",
    "Riley", "Ringo", "Rio", "Riot", "Ripley", "Risa", "River", "Riya", "Rizz", "Roald", "Robbie", "Robert", "Rocket",
    "Rodeo", "Rolo", "Roman", "Romeo", "Rooster", "Rori", "Rory", "Rosanna", "Rose", "Roselie", "Rosewood", "Rowan",
    "Rubber Duck", "Ruby", "Rudolph", "Rudy", "Rue", "Ruffnut", "Rufus", "Rukiya", "Rum Tum Tugger", "Rumpleteazer",
    "Runt", "Russel", "Rusty", "Ruthie", "Ryos",

    "Sable", "Sachiko", "Sadie", "Sadiki", "Saeko", "Safari", "Saffron", "Safi", "Sagwa", "Sahara", "Sahel", "Saidah",
    "Sailor", "Saint", "Sakari", "Saki", "Sakura", "Salem", "Salmon", "Salsa", "Salt", "Salvage", "Sam", "Samantha",
    "Sambusa", "Samus", "Sand", "Sanai", "Sandwich", "Sandy", "Santana", "Sarafina", "Sanyu", "Sarah", "Sarek",
    "Sarge", "Sarki", "Sasha", "Sassy", "Saturn", "Sausage", "Savannah", "Savvy", "Scampi", "Scarecrow", "Scavenger",
    "Schmidt", "Scotch", "Scotty", "Scout", "Scribble", "Scrooge", "Scrungle", "Seamus", "Sega", "Sekhmet", "Selkie",
    "Selkirk", "Seok", "Seoli", "Seoul", "Seraph", "Serenity", "Sergei", "Sergio", "Seri", "Seven", "Shaka", "Shamash",
    "Shampoo", "Shamwow", "Shani", "Shanty", "Shari", "Shay", "Shenzi", "Shep", "Sherb", "Sherman", "Shilin", "Shiloh",
    "Shimmer", "Shino", "Shiver", "Shrimp", "Shukura", "Shuri", "Shuvai", "Siri", "Sillabub", "Silly", "Silva",
    "Silver", "Silvia", "Sim", "Simba", "Simon", "Simone", "Siren", "Siri", "Sirius", "Skimbleshanks", "Skylar",
    "Slinky", "Sloane", "Sloth", "Slug", "Smoke", "Smoky", "Snaggles", "Snek", "Snook", "Snowball", "Snowbell", "Soap",
    "Socks", "Sofa", "Sofrito", "Sol", "Sona", "Sonata", "Sonnet", "Sookie", "Sooty", "Soren", "Soup", "Sox", "Spam",
    "Sparkle", "Sparky", "Spatula", "Speedwell", "Spicy", "Spinach", "Spinel", "Spock", "Spooky", "Spoon", "Spore",
    "Spots", "Squeak", "Stan", "Stanley", "Star", "Starfish", "Stargazer", "Starry", "Static", "Steak", "Stella",
    "Steve", "Steven", "Stinky", "Stitches", "Stolas", "Story", "Strawberry", "Stripes", "Stuffie", "Styx", "Subaru",
    "Sucrose", "Sueno", "Sugar", "Suhailah", "Summit", "Sundae", "Sunflower", "Sungrazer", "Sunny", "Sunset",
    "Survivor", "Sushi", "Suya", "Swansea", "Sweet", "Sweetie", "Sybil", "Sylvana", "Sylveon", "Sylvester",

    "Tabatha", "Tabby", "Taco", "Taffy", "Tahini", "Tahir", "Taihu", "Talia", "Tamale", "Tammy", "Tangerine", "Tango",
    "Tangy", "Tara", "Taro", "Tasha", "Tatiana", "Taurus", "Tay", "Tayo", "Tazama", "Techno", "Teddie", "Teddy",
    "Tempest", "Tempo", "Tesla", "Tesora", "Teufel", "Theo", "Theodore", "Theta", "Thoko", "Thor", "Thuban", "Thyme",
    "Tia", "Tiana", "Tigger", "Tikka", "Tilin", "Tim Tam", "Timmy", "Timon", "Tinka", "Tinky", "Tiny", "Tipsy",
    "Titan", "Toast", "Toby", "Todd", "Tom", "Tomato", "Toni", "Tonka", "Toothless", "Topaz", "Topi", "Toriel", "Toro",
    "Tortellini", "Tortilla", "Tracer", "Traveler", "Treasure", "Trick", "Trinity", "Trinket", "Trip", "Triton",
    "Trixie", "Trouble", "Troublemaker", "Truffle", "Trumpet", "Tucker", "Tuffnut", "Tumble", "Tumo", "Turbo",
    "Twiggy", "Twilight", "Twister", "Twix", "Two Sprouts", "Tyler", "Tyson",

    "Uba", "Ula", "Ulyssa", "Umbriel", "Union", "Uriel", "Ursala",

    "Valente", "Valentina", "Valentino", "Vanessa", "Vanilla", "Vasco", "Venti", "Venture", "Venus", "Veronica",
    "Vervain", "Vesper", "Vesta", "Via", "Victor", "Victoria", "Vida", "Viktor", "Vinnie", "Vinyl", "Violet", "Vivian",
    "Vivienne", "Vox", "Vulpix",

    "Wade", "Wally", "Walnut", "Walter", "Wanda", "Wanderer", "War", "Webby", "Wednesday", "Wendy", "Weston",
    "Whiskers", "Whiskey", "Whisper", "Whitney", "Wiggly", "Wilbur", "Willow", "Windy", "Winry", "Winston", "Wishbone",
    "Wisp", "Wisteria", "Wolf", "Wolfgang", "Wolverine", "Wonder", "Worm", "Wrath",

    "X'ek", "Xelle", "Xhosa", "Xiao", "Xola",

    "Yaoyao", "Yazhu", "Yen", "Yeobo", "Yeza", "Yinuo", "Yogurt", "Yoshi", "Yote", "Yuca", "Yuka", "Yuki", "Yumeko",
    "Yusuke", "Yuzu", "Yvaine",

    "Zach", "Zachary", "Zahra", "Zambezi", "Zambia", "Zaniah", "Zari", "Zariah", "Zarya", "Zazu", "Zebra", "Zelda",
    "Zell", "Zephyr", "Zikomo", "Zim", "Zira", "Ziti", "Zoe", "Zoomie", "Zorro", "Zuberi", "Zuko", "Zuma", "Zuna",
    "Zuva",
],
# tribe_names: list = ["Chasing Wind", "Looks to the Moon", "Looks to the Sky", "Meadow of Two Worlds",
#                      "Plentiful Leaves", "Singing Gray Bird", "Six Grains of Gravel", "Sunny Meadow",
#                      "Watches the Path", "Listens to the Wind", ]
}

# curlews are shorebirds
PREFIXES: dict = {
    None: [
        "Adder", "Alder", "Ant", "Antler", "Aphid", "Apple", "Apricot", "Arch", "Aspen", "Aster",

        "Badger", "Barley", "Basil", "Bass", "Bay", "Beam", "Bear", "Beaver", "Bee", "Beech", "Beetle", "Berry", "Big",
        "Billow", "Birch", "Bird", "Bite", "Bitter", "Bittern", "Bliss", "Blizzard", "Bloom", "Blossom", "Blotch",
        "Bluebell", "Bluff", "Bog", "Borage", "Bough", "Boulder", "Bounce", "Bracken", "Bramble", "Brave", "Breeze",
        "Briar", "Bright", "Brindle", "Bristle", "Broken", "Brook", "Brush", "Bubbling", "Bud", "Bug", "Bumble",
        "Burdock", "Burr", "Burrow", "Bush", "Butterfly", "Buzzard",

        "Carnation", "Carp", "Caterpillar", "Cave", "Cedar", "Chaffinch", "Chasing", "Cherry", "Chervil", "Chestnut",
        "Chirp", "Chive", "Cicada", "Claw", "Clay", "Clear", "Cliff", "Clover", "Comfrey", "Condor", "Cone", "Conifer",
        "Conker", "Copse", "Cougar", "Coyote", "Crag", "Crane", "Creek", "Cress", "Crest", "Crested", "Cricket",
        "Crooked", "Crouch", "Curl", "Curlew", "Curly", "Current", "Cypress",

        "Dahlia", "Daisy", "Dancing", "Dapple", "Dappled", "Dart", "Dash", "Dawn", "Day", "Dazzle", "Dew", "Dog",
        "Down", "Downy", "Dream", "Drift", "Drizzle", "Droplet", "Dry", "Duck", "Dusk",

        "Eagle", "Echo", "Edelweiss", "Eel", "Egret", "Elder", "Elm", "Ermine",

        "Faith", "Falcon", "Fallow", "Fawn", "Feather", "Fennel", "Fern", "Ferret", "Fickle", "Fidget", "Fierce", "Fin",
        "Finch", "Fir", "Fish", "Flail", "Flash", "Flax", "Fleck", "Fleet", "Flicker", "Flight", "Flint", "Flip",
        "Flit", "Float", "Flood", "Flower", "Fluff", "Fluffy", "Flutter", "Fly", "Fog", "Foggy", "Freckle", "Fringe",
        "Frog", "Frond", "Fruit", "Fumble", "Furled", "Furze", "Fuzz", "Fuzzy",
        # "Fallen", "Falling",

        "Gale", "Gander", "Gardenia", "Garlic", "Gentle", "Gill", "Glade", "Goose", "Gorge", "Gorse", "Grass", "Gravel",
        "Grouse", "Gull", "Guppy", "Gust",

        "Hail", "Half", "Hare", "Hatch", "Haven", "Hawk", "Hay", "Hazel", "Hazy", "Heart", "Heath", "Heavy", "Hemlock",
        "Heron", "Hill", "Hollow", "Holly", "Honey", "Hoot", "Hop", "Hope", "Hornet", "Hound", "Howl", "Hush",
        "Hyacinth",

        "Iris", "Ivy",

        "Jackdaw", "Jagged", "Jay", "Jumble", "Jump", "Junco", "Juniper",

        "Kestrel", "Kink", "Kite",

        "Lake", "Larch", "Lark", "Laurel", "Lavender", "Leaf", "Leap", "Leopard", "Lichen", "Light", "Lightning",
        "Lilac", "Lily", "Lion", "Little", "Lizard", "Locust", "Long", "Lotus", "Loud", "Low", "Luck", "Lupine", "Lynx",

        "Mallow", "Mantis", "Maple", "Marigold", "Marsh", "Meadow", "Midge", "Milk", "Milkweed", "Mink", "Minnow",
        "Mistle", "Mite", "Mole", "Moon", "Moor", "Morning", "Moss", "Mossy", "Moth", "Mottle", "Mottled", "Mouse",
        "Mumble", "Murk", "Myrtle",

        "Nectar", "Needle", "Nettle", "Newt", "Nightingale", "Nimble", "Nut",

        "Oak", "Oat", "Odd", "One", "Oriole", "Osprey",

        "Pansy", "Panther", "Parsley", "Partridge", "Patch", "Patchouli", "Peak", "Pear", "Peat", "Perch", "Petal",
        "Petunia", "Pheasant", "Pigeon", "Pike", "Pine", "Piper", "Plover", "Plum", "Pod", "Pond", "Pool", "Pop",
        "Poppy", "Posy", "Pounce", "Prance", "Prickle", "Prim", "Primrose", "Puddle", "Python",

        "Quail", "Quick", "Quiet", "Quill", "Quiver",

        "Rabbit", "Raccoon", "Ragged", "Rain", "Rainbow", "Rat", "Rattle", "Raven", "Reed", "Ridge", "Rift", "Rindle",
        "Ripple", "River", "Roach", "Roar", "Rook", "Root", "Rose", "Rosy", "Rowan", "Rubble", "Runnel", "Running",
        "Rush", "Rustle", "Rye",

        "Sable", "Sapling", "Scorch", "Scratch", "Seed", "Serpent", "Shard", "Sharp", "Shell", "Shimmer", "Shine",
        "Shining", "Shivering", "Short", "Shrew", "Shrub", "Shy", "Silent", "Silk", "Silky", "Silt", "Skip", "Sky",
        "Slate", "Sleek", "Sleepy", "Sleet", "Slight", "Slip", "Sloe", "Slope", "Slumber", "Small", "Snail", "Snake",
        "Snap", "Sneeze", "Snip", "Snowy", "Soft", "Song", "Sorrel", "Spark", "Sparrow", "Speckle", "Spider", "Spike",
        "Splash", "Splinter", "Spore", "Spot", "Spotted", "Spring", "Sprout", "Spruce", "Squirrel", "Starling", "Stem",
        "Stoat", "Stork", "Streak", "Stream", "Stretch", "Strike", "Stripe", "Stumpy", "Sunny", "Swallow", "Swamp",
        "Swarm", "Sweet", "Swift", "Sycamore",

        "Tadpole", "Tall", "Talon", "Tangle", "Tansy", "Tawny", "Tempest", "Thistle", "Thorn", "Thrift", "Thrush",
        "Thunder", "Thyme", "Tiger", "Timber", "Tiny", "Toad", "Torn", "Tremble", "Trickle", "Trout", "Tuft", "Tulip",
        "Tumble", "Turtle",

        "Valley", "Vine", "Vixen",

        "Wasp", "Weasel", "Web", "Weed", "Weevil", "Wet", "Wheat", "Whimsy", "Whirl", "Whisker", "Whisper",
        "Whispering", "Whistle", "Whorl", "Wild", "Willow", "Wind", "Wing", "Wish", "Wisteria", "Wolf", "Wolverine",
        "Wood", "Worm", "Wren",

        "Yarrow", "Yew",

        "Zinnia", ],
    Biome: {
        # These names are based on environments globally, not just in the UK.
        Biome.Beach: [

            # names based on * flora

            # names based on # fauna
            # mammals
            # birds
            # bugs
            # reptiles + amphibians
            # fish

            # names based on places in *

            # names based on weather in *

            # names based on other *-related stuff

            # "Delta", "Dolphin", "Gull", "Jellyfish", "Pearl", "Pool", "Ripple", "Sand", "Scale", "Shimmer", "Wave",
            # Timberfur, the RiverClan deputy before Oakheart
            "Albatross", "Algae", "Anchovy", "Anemone", "Avocet",
            "Barnacle", "Barracuda", "Bass", "Beluga", "Breeze", "Brine",
            "Clam", "Coast", "Coati", "Coconut", "Cod", "Conch", "Coral", "Cove", "Crab", "Curlew", "Current",
            "Dolphin", "Drip", "Drop", "Dune",
            "Eel",
            "Fin", "Flounder", "Flow", "Frond", "Foam",
            "Gannet", "Gull", "Gust", "Gusty",
            "Hermit",
            "Kelp", "Kestrel",
            "Lagoon", "Lake",
            "Marlin", "Monkey",
            "Nacre",
            "Ocean", "Octopus", "Orca",
            "Paddle", "Palm", "Parrot", "Pearl", "Pearly", "Pelican", "Piper", "Pool",
            "Reef", "Ripple",
            "Sago", "Salmon", "Salt", "Sand", "Sandy", "Sardine", "Scale", "Sea", "Seabass", "Seagull", "Shark",
            "Shell", "Shimmer", "Shore", "Slug", "Snail", "Splash", "Squid",
            "Thrift", "Tidal", "Tide", "Timber", "Torrent", "Turtle",
            "Wave", "Whale",
        ],
        Biome.Desert: [

            # names based on * flora

            # names based on # fauna
            # mammals
            # birds
            # bugs
            # reptiles + amphibians
            # fish

            # names based on places in *

            # names based on weather in *

            # names based on other *-related stuff

            # "Rye",
            "Acacia", "Addax", "Agave", "Aloe", "Antelope", "Arid",
            "Barren", "Blaze", "Blister", "Brittle", "Burn", "Buzzard",
            "Cactus", "Camel", "Canyon", "Caracal", "Cheetah", "Cliff", "Coati", "Cobra", "Condor", "Coyote",
            "Day", "Desert", "Dingo", "Drought", "Dry", "Dune", "Dust", "Dusty",
            "Fang", "Fennec", "Fly",
            "Gazelle", "Gully", "Gust", "Gusty",
            "Heat", "Hot",
            "Jackal", "Jackrabbit", "Jerboa",
            "Kestrel",
            "Lion", "Lizard",
            "Mamba", "Meerkat", "Mesa", "Mirage", "Moon",
            "Needle", "Night",
            "Oasis", "Oryx",
            "Pear", "Poison", "Prickle",
            "Quartz",
            "Rattle",
            "Salt", "Scorch", "Scorpion", "Scrub", "Skull", "Smolder", "Snake", "Spider", "Sun",
            "Taipan",
            "Venom", "Viper", "Vulture",
            "Water", "Wax",
            "Yucca",
        ],
        Biome.Forest: [
            # "Branch", "Fern", "Moss", "Oak", "Robin", "Squirrel", "Twig",

            # names based on forest flora
            # "Elder" after Ferncloud's brother Elderkit. It's a kind of tree
            "Alder", "Apple", "Aspen", "Bay", "Beech", "Birch", "Cedar", "Chestnut", "Elder", "Elm", "Fir",
            "Hickory", "Holly", "Magnolia", "Maple", "Oak", "Pine", "Spruce", "Walnut",
            "Azalea", "Berry", "Bramble", "Crocus", "Daffodil", "Fern", "Hazel", "Mistle", "Morel",
            "Moss", "Mossy", "Mushroom", "Myrtle", "Nettle", "Poppy", "Rose", "Violet", "Yarrow",

            # names based on forest fauna
            # mammals
            "Badger", "Bat", "Bear", "Boar", "Buck", "Civet", "Coati", "Cub", "Deer", "Doe", "Elk",
            "Fawn", "Fox", "Marten", "Mole", "Moose", "Mouse", "Skunk", "Shrew", "Squirrel", "Stag", "Vole", "Weasel",
            "Wolf",
            # birds
            "Grouse", "Finch", "Kestrel", "Lark", "Mistle", "Owl", "Pigeon",
            "Quail", "Robin", "Rook", "Sparrow", "Swallow", "Thrush",
            "Robin", "Shrike", "Sparrow", "Thrush", "Wren",
            # bugs
            "Ant", "Bee", "Beetle", "Hornet", "Moth",
            # reptiles + amphibians
            "Adder",
            # fish

            # names based on places in forests
            "Canopy", "Creek", "Grove",

            # names based on weather in forests
            "Mist", "Misty",

            # names based on other forest-related stuff
            "Acorn", "Antler", "Bark", "Branch", "Cone", "Forest", "Frond", "Honey", "Leaf", "Log", "Nut", "Root",
            "Sap", "Sprig", "Stick", "Stump", "Thicket", "Thistle", "Thorn", "Timber", "Tree", "Twig", "Wood",
        ],
        Biome.Mountain: [
            # "Alpaca", "Chamois", "Cliff", "Eagle", "Echo", "Whisper",
            # "Alpine", "Fall", "Mica", "Pinnacle", "Prickle", "Shard", "Steppe", "Volcano",

            # names based on mountain flora
            "Alder", "Apple", "Aspen", "Birch", "Cherry", "Conifer", "Fir",
            "Larch", "Maple", "Oak", "Pear", "Pine", "Plum", "Poplar", "Spruce", "Willow",
            "Briar", "Bush", "Chervil", "Crocus", "Daisy", "Edelweiss", "Fern", "Heather", "Juniper",
            "Laurel", "Lichen", "Lily", "Moss", "Mossy", "Myrtle", "Nettle", "Parsley", "Poppy", "Tulip",

            # names based on mountain fauna
            # "Leopard" because those live on mountains, even if the cats in game likely won't run into them there
            "Alpaca", "Antler", "Bear", "Caribou", "Cougar", "Cub", "Deer", "Doe", "Elk", "Fawn", "Fox",
            "Goat", "Hare", "Leopard", "Lynx", "Marmot", "Panther", "Rabbit", "Ram", "Sheep", "Stag", "Wolf", "Yak",
            "Ant", "Bee", "Cicada", "Cricket", "Moth", "Spider",
            "Bird", "Eagle", "Egret", "Falcon", "Hawk", "Jay", "Junco", "Raven", "Sparrow", "Thrush", "Owl", "Vulture",
            "Warbler", "Wren", "Pipit",
            "Frog", "Newt", "Salamander", "Snake", "Toad",
            "Bass", "Grayling", "Trout",

            # names based on places in mountains
            # TODO add Fall, Falling, Falls? as in waterfalls
            "Abyss", "Bluff", "Brook", "Cave", "Canyon", "Cavern", "Chasm", "Cliff", "Crag", "Creek",
            "Lake", "Meadow", "Mountain", "Peak", "River", "Slope", "Spire", "Stream", "Summit",

            # names based on weather in mountains
            # "Drift" as in a snow drift
            "Avalanche", "Blizzard", "Cloud", "Cloudy", "Drift", "Fog", "Frigid", "Gale", "Gust", "Gusty",
            "Hail", "Ice", "Mist", "Misty", "Rain", "Snow", "Storm",

            # names based on stone
            "Basalt", "Boulder", "Flint", "Granite", "Gravel", "Quartz", "Pebble", "Rock", "Rocky", "Salt", "Shale",
            "Stone",

            # names based on other mountain-related stuff
            # "Cone" as in pinecone
            # "Honey" because there are several species of bee which only live on mountains
            "Cone", "Echo", "High", "Honey", "Howl", "Sky", "Shrub", "Whisper", "Whistle",
        ],
        Biome.Plains: [
            # "Barley", "Breeze", "Cow", "Field", "Grass", "Heather", "Poppy", "Rye", "Wheat", "Willow",

            # names based on plains flora
            "Hickory",  "Willow",

            "Anise", "Barley", "Bracken", "Chive", "Clover", "Daffodil", "Dandelion",
            "Furze", "Gorse", "Grass", "Heather",
            "Oat", "Peony", "Poppy",
            "Rye", "Sage", "Sedge", "Sorrel",
            "Verbena", "Wheat", "Yarrow",

            # names based on plains fauna
            "Bird", "Bison", "Buffalo", "Coati", "Cow", "Elk", "Ewe", "Gopher", "Hare", "Horse", "Kestrel",
            "Lamb", "Pig", "Pronghorn", "Rabbit", "Sheep",

            "Chicken", "Crow", "Cuckoo", "Curlew", "Dove", "Hawk", "Grebe", "Grouse",
            "Lark", "Owl", "Pheasant", "Piper", "Pipit", "Quail", "Robin", "Shrike", "Sparrow", "Stork",

            "Ant", "Bee", "Bug", "Butterfly", "Tarantula",

            "Frog", "Salamander", "Snake", "Toad",

            # names based on places in the plains
            "Burrow", "Copse", "Ditch", "Field", "Hill", "Hollow", "Meadow", "Prairie", "Tunnel",

            # names based on weather in the plains
            "Breeze", "Cloud", "Fog", "Gust", "Gusty", "Mist", "Wind",

            # names based on other plains-related stuff
            "Chalk", "Dawn", "Feather", "Flutter",
            "Moon", "Moor", "Morning", "Pollen", "Prickle",
            "Roan", "Rustle", "Sand", "Set", "Sky", "Swift", "Swish",
            "Wool", "Woolly",
        ],
        Biome.Twolegplace: [
            # names based on * flora

            # names based on # fauna
            # mammals
            "Dog", "Rabbit", "Raccoon", "Rat",
            # birds
            "Chickadee", "Crow", "Kestrel", "Pigeon", "Raven", "Robin", "Starling",
            # bugs
            "Beetle", "Roach",
            # reptiles + amphibians
            # fish
            "Koi",

            # names based on places in *

            # names based on weather in *

            # names based on other *-related stuff
            "Brick", "Stone", "Trash", "Wood",
        ],
        Biome.Wetlands: [
            # "Axolotl", "Bog", "Mosquito", "Reed", "Stork",
            # "Creep" replaced Creeper, which I understand is a plant, but I have a wolf in me and it's a Minecraft zoomer
            # not sure about "Dogwood"
            # tamaracks are a species of larch tree, they're very common in swamps

            # names based on wetland flora
            # "Cotton" as in cottonwood
            "Ash", "Azalea", "Bay", "Birch", "Cedar", "Cotton", "Cypress", "Dogwood", "Elder", "Fir", "Hickory",
            "Larch", "Magnolia", "Mangrove", "Maple", "Pine", "Spruce", "Tamarack", "Willow",
            "Algae", "Bullrush", "Creep", "Daffodil", "Fern", "Hyacinth", "Iris", "Ivy", "Lichen", "Lily", "Lotus",
            "Marigold", "Moss", "Mossy", "Reed", "Rose", "Rush",

            # names based on wetland fauna
            # mammals
            "Bat", "Bear", "Beaver", "Civet", "Coati", "Otter", "Skunk",
            # birds
            "Bittern", "Cormorant", "Crane", "Cuckoo", "Cygnet", "Duck", "Egret", "Gander", "Goose", "Gosling",
            "Grackle", "Grebe", "Harrier", "Heron", "Ibis", "Kingfisher", "Mallard", "Plover", "Sparrow", "Spoonbill",
            "Stork", "Swan", "Swallow", "Owl",
            # bugs
            "Bee", "Beetle", "Bug", "Crayfish", "Darner", "Fly", "Mosquito", "Slug", "Snail", "Spider", "Wasp", "Worm",
            # reptiles + amphibians
            "Alligator", "Crocodile", "Frog", "Newt", "Salamander", "Skink", "Snake", "Tadpole", "Toad", "Tortoise",
            "Turtle",
            # fish
            "Gar", "Eel", "Fish",

            # names based on places in wetlands
            "Bayou", "Bog", "Creek", "Marsh", "Pond", "Pool", "River", "Shore", "Stream", "Swamp",

            # names based on weather in wetlands
            "Mist", "Misty", "Rain",

            # names based on other wetland-related stuff
            "Clay",
            "Fallow",
            "Log",
            "Mire", "Mud", "Murk",
            "Peat",
            "Ripple",
            "Salt", "Shade", "Skip", "Splash", "Sun",
            "Timber",
            "Vine",
            "Wade", "Web", "Weed", "Wet", "Wood",
        ],
    },
    EyeColour: {
        EyeColour.Amber: ["Amber", "Blaze", "Fire", "Flame", "Gold", "Honey", "Pumpkin", "Sap", "Scorch", "Sun", ],
        EyeColour.Blue: [
            # "Blue",
            "Blue", "Borage", "Cold", "Frost", "Frosty", "Ice", "Icicle", "Lake", "Rime", "Sky", "Water",
        ],
        EyeColour.Cobalt: [
            # "Blue",
            "Blue", "Frost", "Frosty", "Ice", "Icy", "Lake", "Rime", "Sky", "Water",
        ],
        EyeColour.Copper: ["Amber", "Brown", "Cinnamon", "Copper", "Fire", "Red",],
        EyeColour.Cyan: ["Blue", "Cold", "Frost", "Ice", "Rapid", "Rime", "River", "Sky", "Storm",],
        EyeColour.DarkBlue: [
            # "Blue",
            "Berry", "Blue", "Cobalt", "Dark", "Deep", "Lake", "Night", "Rain", "River", "Sky", "Storm", "Water",
        ],
        EyeColour.Emerald: [
            # "Green",
            "Emerald", "Green", "Nettle", "Pine", "Shine", "Weed",
        ],
        EyeColour.Gold: ["Amber", "Gold", "Golden", "Honey", "Sap", "Sun", "Yellow",],
        EyeColour.Green: [
            # "Green",
            "Algae", "Aloe", "Clover", "Fern", "Green", "Holly", "Jade", "Olive", "Nettle", "Tree", "Weed",
        ],
        EyeColour.GreenYellow: ["Daisy", "Gold", "Grass", "Green", "Hazel", "Nectar", "Nettle", "Sand", "Sandy", "Tawny", "Weed", "Yellow",],
        EyeColour.Grey: ["Gray", "Heather", "Moon", "Rain", "Ripple", "Silver", "Stone", "Storm",],
        EyeColour.Hazel: [
            # "Hazel",
            "Almond", "Daisy", "Gold", "Hazel", "Sand", "Tawny",
        ],
        EyeColour.HeatherBlue: ["Borage", "Blue", "Heather", "Juniper", "Lavender", "Lilac", "Rosemary", "Violet", "Wisteria",],
        EyeColour.Orange: ["Amber", "Blaze", "Ember", "Fire", "Flame", "Honey", "Orange", "Pumpkin", "Red", "Sun",],
        EyeColour.PaleBlue: [
            # "Blue",
            "Blue", "Cloud", "Day", "Pale", "Rime", "Ripple", "River", "Sky",
        ],
        EyeColour.PaleGreen: [
            # "Lime",
            "Agave", "Fern", "Green", "Mint", "Nectar", "Nettle", "Olive", "Pale", "Stem", "Weed",
        ],
        EyeColour.PaleYellow: ["Daisy", "Gold", "Light", "Pale", "Sun", "Yellow",],
        EyeColour.Sage: ["Bush", "Clove", "Green", "Leaf", "Nectar", "Olive", "Sage", "Weed",],
        EyeColour.Silver: [
            # "Silver",
            "Gray", "Feather", "Light", "Moon", "Pale", "Rain", "Silver", "Stone", "Storm",
        ],
        EyeColour.SunlitIce: [
            # I added "Mouse" because Rock described Mousefur's eyes as 'the colour of sunlit ice' one time
            "Dawn", "Dusk", "Frost", "Glow", "Ice", "Icy", "Mouse", "Odd", "Sun",
        ],
        EyeColour.Yellow: ["Daisy", "Day", "Honey", "Lemon", "Light", "Moon", "Sun", "Yellow",],
    },
    PeltColour: {
        PeltColour.Black: [
            # "Black", "Black", "Dark", "Night",
            "Bat", "Bear", "Black", "Burnt",
            "Char", "Charred", "Chickadee", "Cinder", "Coal", "Crow",
            "Dark", "Dusk",
            "Ebony", "Evening",
            "Flint",
            "Ghost", "Grackle",
            "Holly",
            "Ink", "Inky",
            "Kelp",
            "Midnight", "Mulberry", "Murk",
            "Night",
            "Pepper", "Pitch",
            "Raven", "Rose",
            "Sable", "Scorch", "Shade", "Shaded", "Shadow", "Squirrel", "Storm",
        ],
        PeltColour.Brown: [
            # "Auburn",
            "Adder", "Alder",
            "Bear", "Bracken", "Bramble", "Branch", "Brown", "Burnet",
            "Dark", "Deer", "Doe", "Dog", "Duck", "Dust", "Dusty",
            "Elder",
            "Fawn", "Fennel",
            "Hazel",
            "Log",
            "Marten", "Mouse", "Mud",
            "Nut",
            "Oak", "Ochre", "Otter", "Owl",
            "Reed", "Robin", "Root", "Russet",
            "Shade", "Shadow", "Spider", "Stag",
            "Thrush", "Tree", "Twig", "Twilight",
            "Umber",
            "Vole",
            "Weasel",
        ],
        PeltColour.Chocolate: [
            # "Auburn", "Brown", "Dark", "Mud", "Umber",
            "Bear", "Bramble", "Branch", "Brown", "Burnet",
            "Dark", "Dust",
            "Hickory",
            "Loach", "Log",
            "Mud", "Mushroom",
            "Night",
            "Oak", "Otter", "Owl",
            "Reed", "Robin", "Rowan", "Russet",
            "Shade", "Shadow",
            "Thicket", "Thistle", "Thorn", "Thrush", "Twig",
        ],
        PeltColour.Cream: [
            # "Cream", "Milk", "Pale", "Robin", "Violet",
            "Alder", "Apple",
            "Bone", "Branch", "Bright",
            "Cream",
            "Daisy", "Dandelion", "Dawn", "Day",
            "Egg",
            "Fallow", "Fawn", "Fennel", "Foxglove", # foxglove is poison; why would a cat do this one?
            "Honey",
            "Ivory",
            "Jasmine",
            "Light", "Lovage",
            "Morel", "Morning", "Mushroom",
            "Nectar",
            "Orchid",
            "Pale", "Peach", "Phlox",
            "Sand", "Sandy", "Shine", "Snapdragon", "Spindle", "Straw", "Sun", "Sunny",
            "Veil", "Verbena", "Vervain",
            "Warm",
            "Yellow",
        ],
        PeltColour.DarkBrown: [
            "Alder", "Auburn",
            "Bear", "Branch", "Brown", "Burnet",
            "Dark", "Deer", "Dust",
            "Elder",
            "Gopher",
            "Hickory",
            "Loach", "Log",
            "Mud", "Mushroom",
            "Night",
            "Oak", "Otter", "Owl",
            "Reed", "Robin", "Rowan",
            "Shade", "Shadow", "Spider", "Splash", "Stag",
            "Thicket", "Thrush", "Tree", "Twig",
        ],
        PeltColour.DarkGinger: [
            "Alder", "Apple", "Auburn",
            "Berry", "Burn", "Burnet", "Burnt",
            "Cinnamon", "Copper",
            "Dark", "Dawn",
            "Ember",
            "Fire", "Flame", "Flash", "Fox",
            "Ginger",
            "Holly",
            "Lyre",
            # "Nectar",
            "Oak", "Ochre", "Oleander", "Orange",
            "Pumpkin",
            "Red", "Robin", "Rowan", "Russet", "Rust",
            "Scarlet", "Shade", "Spark", "Spider", "Sorrel",
            # "Tawny",
            "Thunder",
            # "Warm",
        ],
        PeltColour.DarkGrey: [
            # "Ashy",
            "Ash", "Ashen",
            "Bat", "Bleak", "Boulder",
            "Cinder", "Cloud", "Cloudy", "Crow",
            "Dark",
            "Flint", "Frog",
            "Gray",
            # "Magpie",
            "Mist", "Misty",
            "Night",
            "Pebble", "Pigeon", "Plume",
            "Rain", "Rat", "Raven", "Rock",
            "Scorch", "Shade", "Shadow", "Smoke", "Smokey", "Spider", "Splash", "Squirrel", "Stone", "Storm",
            "Twilight",
            "Warbler", "Wisp",
        ],
        PeltColour.Ghost: [
            # "Ebony", "Shaded",
            "Bat", "Black", "Bleak",
            "Char", "Charred", "Cinder", "Cloud", "Cloudy", "Crow",
            "Dark",
            "Fade", "Faded",
            "Ghost", "Gray",
            "Magpie", "Midnight",
            "Night",
            "Pepper",
            "Raven",
            "Sable", "Scorch", "Shade", "Shadow", "Silver", "Spider", "Storm",
            "Violet",
        ],
        PeltColour.Ginger: [
            # "Larkspur",
            "Alder", "Amber", "Apple", "Auburn",
            "Berry", "Blaze", "Burn", "Burnt",
            "Dawn",
            "Ember",
            "Fallow", "Fire", "Flame", "Flare", "Flash", "Fox",
            "Ginger", "Gorse",
            "Lion", "Light", "Lyre",
            "Marigold",
            "Nectar",
            "Ochre", "Orange",
            "Primrose", "Pumpkin",
            "Robin", "Rose", "Rowan", "Rust", "Rusty",
            "Shine", "Snake", "Sorrel", "Spark", "Straw", "Sun", "Sunny",
            "Tawny", "Tiger",
            "Warm",
        ],
        PeltColour.Golden: [
            "Amber", "Apple", "Auburn",
            "Berry", "Buttercup",
            "Canary", "Chick",
            "Daffodil", "Dandelion", "Dawn", "Day",
            "Fennel", "Fig", "Flash",
            "Glint", "Gold", "Golden",
            "Honey",
            # "Light",
            "Lightning", "Lion",
            "Marigold",
            "Nectar",
            "Peach",
            "Saffron", "Shine", "Straw", "Sun", "Sunny",
            "Tawny", "Thrush", "Thunder",
            "Warm",
            "Yellow",
        ],
        PeltColour.GoldenBrown: [
            # "Brown", "Fawn", "Lion", "Ochre", "Thrasher",
            "Alder", "Auburn",
            "Branch", "Brown", "Burnet",
            "Cougar",
            "Dandelion", "Deer", "Doe", "Dust", "Dusty",
            "Elder",
            "Hazel",
            "Kite",
            "Lark", "Log",
            "Mouse", "Mud",
            "Nectar",
            "Oak", "Otter", "Owl",
            "Robin", "Root", "Russet",
            "Shade", "Shadow", "Stag",
            "Thicket", "Thorn", "Thrush", "Tree", "Twig",
            "Umber",
            "Vole",
            "Wind",
        ],
        PeltColour.Grey: [
            "Ash", "Ashen",
            "Bleak", "Boulder",
            "Cinder", "Cloud", "Cloudy", "Cold",
            "Dove",
            "Fish", "Fog", "Frog",
            "Gray", "Gull",
            "Ivy", # after Ivypool!
            "Lyre",
            "Mist", "Misty", "Mouse",
            "Pebble", "Pigeon", "Plume",
            "Rain", "Rat", "Rime", "Rock",
            "Shade", "Shadow", "Shrike", "Smoke", "Smoky", "Soot", "Spider", "Splash", "Stone", "Storm",
            "Teasel", "Thrush", "Toad", "Tree", "Trout",
            "Wisp",
        ],
        PeltColour.LightBrown: [
            # "Adder", "Bark", "Robin", "Thrush",
            "Beech", "Branch", "Bright", "Brown",
            "Cougar",
            "Dawn", "Dust", "Dusty",
            "Eagle",
            "Glow",
            "Hawk", "Hazel",
            "Lark", "Light", "Lightning",
            "Mouse", "Mud",
            "Pale", "Puma",
            "Root",
            "Sand", "Sandy", "Scrub", "Soft", "Sweet",
            "Tawny", "Toad", "Tree",
            "Velvet", "Vole",
            "Warm",
        ],
        PeltColour.Lilac: [
            "Branch", "Bright",
            "Dawn", "Dust", "Dusty",
            "Fish", "Frog",
            "Ghost",
            "Hazel", "Heather",
            "Lavender", "Light", "Lilac",
            "Mint", "Mouse", "Mud",
            "Nectar",
            "Pale",
            "Robin",
            "Sand", "Sandy", "Scrub", "Spider",
            "Violet", "Vole",
            "Warm",
        ],
        PeltColour.PaleGinger: [
            # "Ginger", "Ochre", "Orange", "Violet",
            "Alder", "Auburn",
            "Berry", "Bright",
            "Cosmos",
            "Daisy", "Dandelion", "Dawn", "Day",
            "Egg",
            "Fallow", "Fawn", "Fennel", "Foxglove",
            "Honey",
            "Ivory",
            "Jasmine",
            "Light", "Lovage",
            "Morel", "Morning", "Mushroom",
            "Nectar",
            "Orchid",
            "Pale", "Peach", "Phlox",
            "Sand", "Sandy", "Shine", "Snapdragon", "Spindle", "Straw", "Sun", "Sunny",
            "Tawny",
            "Veil", "Verbena", "Vervain",
            "Warm",
            "Yellow",
        ],
        PeltColour.PaleGrey: [
            "Ash", "Azalea",
            "Breeze", "Bright",
            "Chill", "Clear", "Cloud", "Cloudy", "Cold", "Cotton",
            "Dove", "Down",
            "Foam", "Fog", "Freeze", "Fringe", "Frog", "Frost", "Frozen",
            "Gray",
            "Hail", "Haze", "Heather",
            "Ice", "Icicle", "Icy", "Ivy", # "Ivy" after Ivypool!
            "Light",
            "Mint", "Mistle", "Moon", "Mouse",
            "Nectar",
            "Pale", "Pebble", "Pipit",
            "Rime", "Rock",
            "Silver", "Sky", "Stone", "Storm", "Stream",
            "Thicket", "Tuft",
        ],
        PeltColour.Sienna: [
            # "Fuschia", "Ginger", "Red", "Robin", "Violet",
            "Alder", "Apple", "Auburn",
            "Berry", "Burn", "Burnet", "Burnt",
            "Cinnamon", "Copper",
            "Dusk",
            "Ember",
            "Fire", "Flame", "Fox",
            "Ginger",
            "Holly",
            "Lyre",
            # "Nectar",
            "Ochre", "Oleander", "Orange",
            "Red", "Robin", "Rowan", "Russet", "Rust", "Rusty",
            "Scarlet", "Shade", "Sorrel", "Spark", "Squirrel", "Sun", "Sunset",
            # "Tawny",
            "Vixen",
        ],
        PeltColour.Silver:[
            # "Silver", "Silver",
            "Air",
            "Bleak", "Blizzard", "Blue", "Borage",
            "Cloud", "Cloudy", "Cold", "Crocus",
            "Ermine", "Feather", "Fish", "Flurry", "Freeze", "Fringe", "Frost", "Frozen",
            "Glint", "Gossamer", "Gray", "Gull",
            "Heather",
            "Ice", "Icy",
            "Lilac",
            "Minnow", "Mint", "Mist", "Mistle", "Moon",
            "Nectar",
            "Pale", "Pebble", "Pike",
            "Rain", "Rime", "River", "Rock", "Rue",
            "Scale", "Shatter", "Silver", "Snap", "Stoat", "Stone",
            "Thicket",
            "Vine",
            "Wave",
        ],
        PeltColour.White:[
            # "White",
            "Air",
            "Blizzard", "Bone", "Bright",
            "Chalk", "Chervil", "Chill", "Cloud", "Cloudy", "Cold", "Cotton",
            "Dove",
            "Egg",
            "Flurry", "Foam", "Freeze", "Fringe", "Frost", "Frozen",
            "Ghost",
            "Hail", "Hawthorn",
            "Ibis", "Ice", "Icicle", "Icy",
            "Laurel", "Light",
            "Milk", "Moon",
            "Nectar",
            "Pale", "Privet",
            "Rime",
            "Salt", "Sky", "Snake", "Snow", "Snowy", "Swan",
            "White", "Wisp",
        ],
    },
    # TODO fill out more PeltPatterns
    PeltPattern: {
        PeltPattern.Agouti: ["Stripe", ],
        PeltPattern.Bengal: ["Tiger", ],
        PeltPattern.Classic: ["Breeze", "Wind", ],
        PeltPattern.Mackerel: ["Tiger", ],
        PeltPattern.Marbled: ["Breeze", "Storm", "Wind", ],
        PeltPattern.Masked: ["Mask", "Raccoon", ],
        PeltPattern.Rosette: ["Rose", ],
        PeltPattern.SingleStripe: ["Stripe", ],
        PeltPattern.Smoke: ["Plum", "Smoke", "Smudge", ],
        PeltPattern.Sokoke: ["Smudge", ],
        PeltPattern.SolidColour: [],
        PeltPattern.Speckled: ["Leopard", ],
        PeltPattern.Tabby: ["Tiger", ],
        PeltPattern.Ticked: ["Freckle", "Spot", "Spotted", ],
    },
    # TODO make it so that kits can be named after something related to the season they were born in
    Season: {
        Season.Spring: [
            "Breeze", "Bloom", "Blossom", "Bird", "Bud", "Gentle", "Hope", "Rain", "Robin", "Storm",
        ],
        Season.Summer: [
            "Flower", "Leaf", "Petal", "Sun",
        ],
        Season.Autumn: [
            # "Fall" as in leaf-fall
            "Breeze", "Chill", "Fall", "Wind",
        ],
        Season.Winter: [
            "Blizzard", "Cold", "Frost", "Hope", "Ice", "Snow",
        ],
    },
    # TODO fill out more TortiePatches
    # TODO add "Roan" to tortie and white patches
    TortiePatches: {
        # "Brindle", "Dapple", "Freckle", "Mottle", "Leaf", "Shell", "Turtle",
        TortiePatches.Bandana: [
            "Smudge", "Wolf",
        ],
        TortiePatches.Blanket: [
            "Shell", "Turtle",
        ],
        TortiePatches.Brindle: [
            "Brindle", "Mottle",
        ],
        TortiePatches.Chimera: [
            "Moon",
        ],
        TortiePatches.Daub: [
            "Slash",
        ],
        TortiePatches.Dapplenight: [
            "Shell", "Turtle",
        ],
        TortiePatches.Freckled: [
            "Freckle", "Speckle", "Spot", "Spotted",
        ],
        TortiePatches.Mask: [
            "Mask", "Raccoon", "Smudge",
        ],
        TortiePatches.Oriole: [
            "Shell", "Turtle",
        ],
        TortiePatches.Paige: [
            "Shell", "Patch",
        ],
        TortiePatches.PacMan: [
            "Shell", "Patch",
        ],
        TortiePatches.Robin: [
            "Robin",
        ],
        TortiePatches.Safi: [
            # TODO
        ],
        TortiePatches.Shiloh: [
            # this is what the character Leafshade looks like
            "Brindle", "Dapple", "Freckle", "Leaf", "Maple", "Mottle",
        ],
        TortiePatches.Smudged: [
            # this is what the character Leafshade looks like
            "Blossom", "Petal",
        ],
    },
    WhitePatches: {
        WhitePatches.Appaloosa: [
            "Dapple", "Fleck", "Freckle", "Mottle", "Speckle", "Spot", "Spotted",
        ],
        WhitePatches.BackSpot: [
            "One", "Spot", "Turtle",
        ],
        WhitePatches.Beard: [
            "Patch",
        ],
        WhitePatches.Blackstar: [
            # TODO make a token so that this will end up with the name Colourfoot depending on the cat's colour
            "Dew", "Snow", "Snowy", "White",
        ],
        WhitePatches.Broken: [
            # "Frost", "Ice", "Snow", "White",
            "Spotted",
        ],
        WhitePatches.Buddy: [
            "Spot",
        ],
        WhitePatches.Bullseye: [
            "Ring",
        ],
        WhitePatches.Buster: [
            "Cow", "Ripple",
        ],
        WhitePatches.Cake: [
            "Cow", "Patch",
        ],
        WhitePatches.ChestSpeck: [
            "Snow", "Spot", "White",
        ],
        WhitePatches.Coat: [
            "Frost", "Ice", "Snow", "White",
        ],
        WhitePatches.Cow: [
            "Cow", "Patch", "Splash", "Whirl", "Whorl",
        ],
        WhitePatches.CowTwo: [
            "Cow", "Patch", "Rain", "Splash",
        ],
        WhitePatches.Curved: [
            "Curve", "Moon", "Swirl", "Whorl",
        ],
        WhitePatches.EyeBags: [
            "Tip",
        ],
        WhitePatches.FadeSpots: [ # TODO maybe also include FadeBelly?
            "Frost",
        ],
        WhitePatches.Farofa: [
            "Deer", "Fawn", "Patch", "Stag",
        ],
        WhitePatches.BlazeChestPawsContinuous: [ # "fcone"
            "Frosted",
        ],
        WhitePatches.BlazeChestPawsBroken: [ # "fctwo"
            "Frosted",
        ],
        WhitePatches.Finn: [
            "Fade", "Ring",
        ],
        WhitePatches.Freckles: [
            "Dapple", "Freckle", "Leopard", "Spot", "Spotted",
        ],
        WhitePatches.Glass: [
            "Blizzard", "Frosted", "Storm", "Whirl", "Whorl",
        ],
        WhitePatches.Goatee: [
            "Snow", "White",
        ],
        WhitePatches.HalfFace: [
            "Half", "White",
        ],
        WhitePatches.Hawkblaze: [
            "Hawk", "Eagle", "Falcon",
        ],
        WhitePatches.Kropka: [
            "Tip",
        ],
        WhitePatches.Lightsong: [
            "Light",
        ],
        WhitePatches.Little: [
            "Tip",
        ],
        WhitePatches.MinkPoint: [
            "Haze", "Seal",
        ],
        WhitePatches.Miss: [
            "Swirl",
        ],
        WhitePatches.OneEar: [
            "Light", "Snow", "White",
        ],
        WhitePatches.Owl: [
            "Hoot", "Owl",
        ],
        WhitePatches.Painted: [
            "Blossom", "Leopard", "Spot", "Spotted",
        ],
        WhitePatches.Pebble: [
            "Patch", "Pebble", "Spot",
        ],
        WhitePatches.Pebbleshine: [
            "Blizzard", "Dapple", "Dappled", "Freckle", "Leopard", "Pebble", "Spot", "Spotted",
        ],
        WhitePatches.Petal: [
            # "Aster", "Daisy", "Flower", "Rose",
            "Patch", "Petal", "Spot", "Two", "White",
        ],
        WhitePatches.Ragdoll: [
            "Raccoon",
        ],
        WhitePatches.Ravenpaw: [
            "Raven", "Tip",
        ],
        WhitePatches.ReversePants: [
            "High", "Top",
        ],
        WhitePatches.Rosina: [
            # "Half" for the half of the face
            # "Ring" for rings on the tail
            "Half", "Ring",
        ],
        WhitePatches.Savannah: [
            "Frost",
        ],
        WhitePatches.SealPoint: [
            "Seal",
        ],
        WhitePatches.ShibaInu: [
            "Dog", "Hound",
        ],
        WhitePatches.Skunk: [
            "Skunk", "Badger",
        ],
        WhitePatches.Sparrow: [
            # "Hawk", "Thrush",
            "Bird", "Feather", "Half", "Sparrow",
        ],
        WhitePatches.TailTip: [
            "Tip",
        ],
        WhitePatches.TailTwo: [
            "Snow", "Snowy",
        ],
        WhitePatches.Tip: [
            "Tip",
        ],
        WhitePatches.Wrap: [
            "Half", "White",
        ],
        WhitePatches.WoodPecker: [
            "Needle", "Tiger",
        ],
    },
}

SUFFIXES: dict = {
    None: [
        # "claw" x5; "foot" x4; "fur" x10; "heart" x7; "pelt" x10; "rise" x1; "tail" x6; "tooth" x5; "tuft" x4; "whisker" x5;
        # "lightning"
        "arch", "ash", "aster",

        "back", "badger", "bark", "bat", "beak", "beam", "bee", "beetle", "bellow", "belly", "berry", "billow", "bird",
        "bite", "blaze", "blink", "bloom", "blossom", "blotch", "blur", "bone", "bounce", "bracken", "bramble",
        "branch", "break", "breeze", "briar", "bright", "brook", "bubble", "bud", "bumble", "burn", "burr", "burst",
        "bush", "buzz",

        "call", "catcher", "chase", "chaser", "chasm", "chest", "chill", "chirp", "chomp", "cinder", "clash", "claw",
        "cloud", "clover", "crackle", "crash", "crawl", "creek", "crest", "cry", "curl", "current",

        "daisy", "dance", "dapple", "dart", "dash", "dawn", "daze", "dazzle", "dew", "dream", "drift", "drizzle",
        "drop", "dusk", "dust",

        "eagle", "ear", "ears", "echo", "egg", "ember", "eye", "eyes",

        "face", "falcon", "fall", "fang", "feather", "fern", "fin", "fire", "fish", "flake", "flame", "flare", "flash",
        "fleck", "flick", "flicker", "flight", "flip", "flit", "flood", "flow", "flower", "fluff", "fog", "foot",
        "fox", "freeze", "frost", "fruit", "fur", "fuzz",

        "gale", "gaze", "ghost", "glare", "gleam", "glide", "glint", "glow", "goose", "gorse", "grass", "growl",

        "hail", "hare", "haven", "hawk", "haze", "heart", "heather", "hiss", "hollow", "holly", "honey", "hope",
        "howl", "husk",

        "ice", "iris", "ivy",

        "jaw", "jay", "joy", "jumble", "jump",

        "kestrel", "kick", "kite", "knoll",

        "lake", "larch", "laurel", "leaf", "leap", "leg", "leopard", "light", "lightning", "lilac", "lily", "lion",
        "lotus",

        "mallow", "mane", "mark", "mask", "meadow", "mimic", "minnow", "mist", "moon", "moor", "moss", "moth",
        "mouse", "munch", "murk", "muzzle",

        "needle", "nest", "nettle", "newt", "nibble", "night", "nip", "noise", "nose", "nudge", "nut",

        "pad", "patch", "path", "peak", "pelt", "petal", "plume", "pond", "pool", "poppy", "pounce", "prance",
        "prickle", "puddle", "purr",

        "quill", "quiver",

        "rain", "rapid", "raven", "reed", "rip", "ripple", "rise", "river", "roach", "roar", "rock", "root", "rose",
        "rumble", "rump", "run", "runner", "rush", "rustle",

        "scar", "scratch", "screech", "seed", "seeker", "shade", "shadow", "shard", "shell", "shimmer", "shine",
        "shiver", "shock", "shriek", "sight", "silk", "skip", "skitter", "sky", "slash", "slip", "snap", "snarl",
        "snout", "snow", "soar", "song", "spark", "speck", "speckle", "spider", "spike", "spirit", "splash",
        "splinter", "spore", "spot", "spots", "spring", "sprout", "stalk", "stem", "step", "sting", "stone", "storm",
        "streak", "stream", "strike", "stripe", "sun", "swarm", "swipe", "swoop",

        "tail", "talon", "tangle", "thistle", "thorn", "thrift", "throat", "thrush", "thud", "thunder", "tiger",
        "timber", "toe", "tooth", "trail", "tree", "trot", "tuft", "tumble", "twist",

        "valley",

        "watcher", "water", "wave", "web", "whisker", "whisper", "whistle", "willow", "wind", "wing", "wish", "wisp",

        "zoom",
    ],
    Biome: {
        Biome.Beach: [
            # "fish" because Sunfish was a RiverClan warrior
            # "tide" x1
            "coast", "coral", "cove", "current",
            "drip", "drop",
            "fin", "fish", "flood", "foam",
            "gill",
            "ocean",
            "pearl", "pool",
            "ripple",
            "sand", "sea", "shell", "shimmer", "shine", "shore", "splash", "squid", "stream", "surf",
            "tide", "torrent",
            "water", "wave",
        ],
        Biome.Desert: [
            "aloe",
            "bite",
            "canyon",
            "dune", "dust",
            "fang", "fly",
            "needle",
            "prickle",
            "rattle",
            "sand", "scorpion", "snake",
            "sun", "tooth", "wind",
        ],
        Biome.Forest: [
            # "dapple",
            "acorn", "antler",
            "beak", "bear", "branch", "briar",
            "clove", "cone",
            "deer",
            "fawn", "fern", "flight", "fog", "frond",
            "glade", "grove",
            "moss",
            "sap", "shade",
            "thicket", "twig",
            "wood",
        ],
        Biome.Mountain: [
            "briar",
            "cave", "caw", "cliff", "crag", "cricket",
            "drop",
            "eagle", "echo",
            "fall", "flight", "frost",
            "goat",
            "horn",
            "jay",
            "leap", "lichen",
            "mound",
            "peak", "point",
            "quake",
            "ram",
            "shard", "shatter", "sky", "steep", "stone", "summit",
            "wing", "whisper", "whistle",
        ],
        Biome.Plains: [
            "bee", "breeze", "briar", "brush", "bull", "burrow",
            "elk",
            "field", "flight", "flutter",
            "horse",
            "lamb",
            "meadow",
            "oat",
            "pollen",
            "runner",
            "sheep", "swish",
            "tunnel",
            "wool",
        ],
        Biome.Wetlands: [
            # "fish" because Sunfish was a RiverClan warrior
            "briar", "bog", "bug",
            "creek", "croak",
            "duck",
            "fish", "flood",
            "glow",
            "lily",
            "mire", "moss", "mud",
            "ripple", "root",
            "skipper", "song", "splash", "stream", "swamp",
            "turtle",
            "wade", "wave", "wing",
        ],
    },
    PeltPattern: {
        PeltPattern.Agouti: [
            "back", "fur", "pelt",
        ],
        PeltPattern.Bengal: [
            "dapple", "fleck", "freckle", "patch", "ripple", "speck", "speckle", "spot", "spots", "tiger",
        ],
        PeltPattern.Classic: [
            # "stripe" x1
            "blotch", "feather", "fern", "leaf", "patch", "stripe", "swirl", "whorl",
        ],
        PeltPattern.Mackerel: [
            # "stripe" x1
            "feather", "fern", "leaf", "stripe",
        ],
        PeltPattern.Marbled: [
            # "stripe" x1
            "feather", "leaf", "ripple", "shade", "stripe", "swirl", "whirl", "whorl",
        ],
        PeltPattern.Masked: [
            # "mask" x1
            "mask", "shade", "stripe", ],
        PeltPattern.Rosette: [
            # "dapple" x1
            "dapple", "fleck", "freckle", "leopard", "ripple", "speckle", "spots",
        ],
        PeltPattern.SingleStripe: [
            # "shadow",
            "stem", "streak", "stripe",
        ],
        PeltPattern.Smoke: [
            "dawn", "dusk", "fade", "ghost", "shade", "smoke",
        ],
        PeltPattern.Sokoke: [
            # "stripe" x1
            "feather", "fern", "leaf", "stripe", "swirl", "whorl",
        ],
        PeltPattern.Speckled: [
            "dapple", "fleck", "freckle", "mottle", "speck", "speckle", "spot",
        ],
        PeltPattern.Tabby: [
            # "stripe" x1
            "feather", "leaf", "shade", "stripe", "swirl",
        ],
        PeltPattern.Ticked: [
            "freckle", "pelt", "speckle", "spots",
        ],
    },
    RedSkill: {
        RedSkill.StarClan: ["moon", "night", "sight", "silver", ], # "silver" because Silverpelt
        RedSkill.DarkForest: ["claw", "fang", "snarl", "talon", "tangle", ],
        RedSkill.Clairvoyance: ["sight", ],

        RedSkill.Teaching: ["heart", ],
        RedSkill.CampKeeping: ["heart", ],
        RedSkill.Fighting: ["blaze", "claw", "fang", "heart", "lion", ],
        RedSkill.Mediation: ["heart", "light", ],
        RedSkill.KitSitting: ["heart", ],
        RedSkill.Herbalism: ["fern", "leaf", ],
        RedSkill.Interpretation: ["sight", ],

        RedSkill.Fishing: ["catch", ],
        RedSkill.Stalking: ["catch", "crawl", "creep", "hunt", "nose", "shadow", ],
        RedSkill.Ambushing: ["catch", "feather", "flight", "jump", "leap", ],
        RedSkill.Scavenging: ["creep", "hunt", "nose", "shadow", ],

        RedSkill.Swimming: ["creek", "fin", "fish", "river", "stream", "tide", ],
        RedSkill.Running: ["leg", "run", "runner", "wind", ],
        RedSkill.Climbing: ["climb", "leap", "peak", ],
        RedSkill.Navigating: ["hunt", "path", "step", ],

        RedSkill.Comforting: ["heart", "feather", ],
        RedSkill.Speaking: [],
        RedSkill.Reasoning: ["sight", ],
        RedSkill.Observation: ["sight", ],
        RedSkill.Storytelling: ["song", ],
        RedSkill.History: ["song", ],
    },
    # TODO add tortie patch suffixes
    TortiePatches: {
        #  Calico: ["dapple", "patch", "stripe", ], # "patch" x1
        #  Tortie: ["dapple", "speckle", "spot", ], # "dapple" x1
        #  TwoColour: ["patch", "splash", "spot", "spots", "swan", ], # "patch" x1
    },
    WhitePatches: {
        WhitePatches.Appaloosa: ["dapple", "mottle", "spot", "spots", ],
        WhitePatches.Apron: ["ear", "tail", ],
        WhitePatches.Blackstar: ["feet", "foot", "step", ],
        WhitePatches.Bleached: ["frost", ],
        WhitePatches.Blossomstep: ["step", ],
        WhitePatches.Boots: ["foot", "leg", ],
        WhitePatches.Broken: ["dapple", "frost", "spots", ],
        WhitePatches.CapSaddle: ["patch", "splash", ],
        WhitePatches.ChestSpeck: ["freeze", "snow", "spot", ],
        WhitePatches.Cow: ["spots", "swirl", "whirl", "whorl", ],
        WhitePatches.CowTwo: ["rain", "ripple", "splash", "spot", "whirl", "whorl", ],
        WhitePatches.Curved: ["feather", "swirl", "wing", "whirl", "whorl", ],
        WhitePatches.Dapplepaw: ["spot", "spots", ],
        # TODO add FadeBelly?
        WhitePatches.FadeSpots: ["frost", ],
        WhitePatches.Freckles: ["dapple", "spots", ],
        WhitePatches.Front: ["muzzle", "nose", ],
        WhitePatches.HalfFace: ["frost", "mottle", ],
        WhitePatches.HalfWhite: ["stripe", ],
        WhitePatches.Hawkblaze: ["blaze", "wing", ],
        WhitePatches.Heart: ["ear", "heart", "tail", ],
        WhitePatches.HeartTwo: ["heart", "spot", ],
        WhitePatches.Kropka: ["tip", ],
        WhitePatches.Lightsong: ["back", "frost", "ice", "song", "splash", ],
        WhitePatches.MinkPoint: ["haze", ],
        WhitePatches.Miss: ["swirl", ],
        WhitePatches.Moon: ["frost", "swirl", ],
        WhitePatches.Moorish: ["face", "tail", ],
        WhitePatches.OneEar: ["ear", ],
        WhitePatches.Pebbleshine: ["light", "shine", ],
        WhitePatches.Petal: ["blossom", "flower", "petal", ],
        WhitePatches.Powder: ["dapple", "haze", "mottle", "spots", ],
        WhitePatches.Sammy: ["heart", ],
        WhitePatches.Savannah: ["frost", ],
        WhitePatches.Smokey: ["mottle", ],
        WhitePatches.Tail: ["tail", ],
        WhitePatches.TailTwo: ["tail", ],
        WhitePatches.Unders: ["feet", "leg", ],
        WhitePatches.Van: ["ear", "spots", "tail", ],
        WhitePatches.Vest: ["splash", ],
        WhitePatches.Vitiligo: ["dapple", "haze", "mottle", "spots", ],
        WhitePatches.VitiligoTwo: ["dapple", "mottle", "spots", ],
        WhitePatches.Wings: ["splash", "wing", ],
    },
}
