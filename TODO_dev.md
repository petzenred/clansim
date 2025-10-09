# TODO_dev

A technical list of things that need doing. If you aren't a developer, you're probably looking for `TODO.md`.


## Uncategorized
- game = `scripts.game_structure.game_essentials.Game()`
- [ ] implement `FadedCat`, a subclass of Cat
  - Cats should have a can/can't have kits toggle. If your camp is in a Twolegplace, one disaster is that a bunch of
  humans come and TNR a bunch of your cats, and don't let newborns, kits, and elders go.
  - with new relationship and event systems, sometimes cats will tell other cats stories about dead cats they had a
  strong relationship with OR who had high fame, or who they heard about through a story. This prevents that cat
  from fading
- [ ] implement `Relationship`
    - don't forget: `raise NotImplementedError(f"Relationships aren't implemented yet, so you can't filter for 
  emotional relationships between cats yet. Sorry!")`
- replace strings with enums where possible
    - [ ] find all calls to `str.casefold()`
    - [x] replace `scripts.cat.enums.CatAgeEnum` with an enum in `definitions`
    - [ ] replace current `Age` StrEnum, but instead tuples of the age ranges
- [ ] all classes use either "Handler" or "Manager"
- [ ] new button on main menu - "convert ClanGen save"
- [ ] for sprites-related pelt aspects, instead of strings, be an IntEnum that contains where they are on a sprite 
sheet
- [ ] include this in SaveManager or ConversionManager
    # fix 'old' history save bugs
    if type(self.mentor_influence["trait"]) is type(None):
      self.mentor_influence["trait"] = {}
    if type(self.mentor_influence["skill"]) is type(None):
      self.mentor_influence["skill"] = {}
    if "mentor" in self.mentor_influence:
      del self.mentor_influence["mentor"]
- [ ] separate pregnancy from the list of ailments in Conditions
- [ ] Easter egg cats (`GameConfig.easter_eggs`)
  - Sunnyfall
  - Moonkitti
  - Murphy (cat genetics fella)
  - Bo (Autumnleaf)
  - Nick (Softheart)
  - Aloy (Leafpelt)
  - Freddie (Tigershine)
  - Artie (Mistpool)
  - Marlowe (Badgerheart)
  - Disco (Discostep)
- [ ] Seperate a backstory into how a cat was born (`BackstoryBirth`), and how a cat joined their Clan 
(`BackstoryCircumstance`).

  
## Track cats and Clans
- keeps track of all cats: living, dead, and faded
- keeps track of all Clans: extant, destroyed, and forgotten
- keeps track of relationships between Clans and Clan reputation
- [x] `CatTracker` class
  - [x] tests
- [ ] keep track of nursing queens and which Clan they are currently a member of


## Saving and loading files
- [ ] `IOManager` class
  - [ ] tests
- [ ] `SaveManager` class
  - [ ] tests
- [ ] what do saves look like?
- [ ] create a `save` method in `game`
- things you can save and load separately
  - Clans, cats, and Clan settings are saved together
  - general game settings
  - sound game settings
- [ ] sequence: the game boots up TODO rework this
  - in `main.py`
    2. [ ] check for downloaded updates
    3. [ ] set version info
    1. [ ] logging setup
    4. [ ] pygame setup
    5. [ ] 
    6. [x] the `game` object creates a `SaveManager` object
    7. [x] load game settings (general and sound)
    8. [ ] load the data from the save file referred to by `currentclan.txt` if possible
    9. [ ] 
- [ ] sequence: the player switches save files (player Clans)
  1. [ ] get valid and invalid save files
  2. [ ] show that information to player
  3. [ ] the player selects the name of a valid save file (e.g. `ThunderClan`)
  4. [ ] the player clicks a button which reads `Load this Clan`
  5. [ ] load that save file and automatically send the player back to the main menu
- [ ] save sequence: general game settings
- [ ] load sequence: general game settings
- [ ] save sequence: sound game settings
- [ ] load sequence: sound game settings
- [ ] save sequence: game
  1. [ ] save cat lists
  2. [ ] save Clan info
- [ ] load sequence: game (`game.load_active_clan_save_file`)
  1. [x] create a new `CatTracker` object in `game`
  2. [x] load Clan settings in `conf`
  3. [ ] load the Clan details
    - [x] load game details: the current time, save and game versions, the last cat ID used, and the afterlife guides
    - [x] create the `RedClan` object for the player's Clan
    - [x] create the `RedClan` object for outsiders
    - [x] create the `RedClan` object for warrior Clans other than the player's
    - [ ] create `Camp` object for the player's Clan
  4. [ ] 


## Configuration and settings
- [-] split the `Settings` class into `GameSettings` and `ClanSettings`
- [ ] `GameConfig` class 
- [ ] `CatConfig` class 
- [ ] `RelationshipConfig` class 
- [ ] `ClanConfig` class 
  -  [ ] refactor how the freshkill prioritization is saved
- [ ] `EventConfig` class 
- [ ] `PreyConfig` class 
- [ ] `RankConfig` class 
  - move `Rank` priority lists from `definitions` to here
- [ ] `BiomeConfig` class 
- [ ] `ConfSettManager` class
- [ ] settings should only be retrieved with `game.get_config_value`, not `game._game_config`
- [ ] settings should only be retrieved with `game.get_setting_value`, not `game._settings`
  - [ ] implement `game.get_setting_value`
- [ ] NEW: it would be fun if there was a setting to randomly have cats from the books show up, or even to have one 
of the Clans from the books show up. Only ever one at a time though!
- [ ] NEW: `HelpingHand` settings which changes event occurrence probability depending on your Clan's state
    - setting: helping hand
        - preypile: if low, more likely to get events where you get lots of prey and less likely to get events where 
      new cats join your Clan
        - num_cats: if very low, more likely to get events where new cats join your Clan
        - herbstore: if low, more likely to get events where your medicine cats collect extra herbs
        - sick_cats: medicine cat patrols are more likely to collect herbs that you need (but still only if they're 
      in season)
- [ ] NEW: `RealisticPregnancies` setting
  - [ ] miscarriages
  - [ ] torties need a tortie parent OR a ginger-base and a black-base parent
  - [ ] if a cat has no white, they can't have blue eyes
  - [ ] female cats are more likely to be tortie than male cats
  - [ ] ginger-base female cats can't have black-base sons, and black-base female cats can't have ginger-base sons


## Events and History
- [ ] `Filter` class
  - [elements of filter](/resources/lang/en/_Red/new_text_formatting.md)
    - [ ] `tags` - a list of string tags
    - [ ] `biome`: subkeys are `allowed` and `disallowed`, both of which contain strings that should correspond to 
    members of the `Biome` class
    - [ ] `location`: contains keys related to where the event is happening. Includes `biome`, which has the subkeys 
    `allowed` and `disallowed`, both of which contain strings that should correspond to members of the `Biome` class;
    and it contains a boolean, `is_camp`.
    - [ ] TODO add the ability to filter for cats with specific skills + skill experience + aggregate experience
  - [ ] TODO add ability to filter for Clan settings and game settings, or should that be a tag thing?
  - [ ] doesn't care if an empty tag is missing or read as None
- unify event text replacements
    - [ ] Patrol.process_text
    - [ ] DisasterEvents.handle_disasters
- [x] new section for `RedCat.History`: attachments
  - current and previous mate(s)
  - current and previous apprentice(s)
  - current and previous mentor(s)
  - current litter and parents
- [ ] update event formatting to new standard
- [ ] `scripts.events.perform_ceremonies`
- [x] `RedCondition` class
- [ ] should there be `injury` and `illness` events or `minor condition` and `major condition` events?
- [ ] `BaseEvent` class
- [ ] ongoing events - pregnancies, apprenticeship? probably not its own class
- categorize these events
  - [ ] adoption
  - [ ] finding kittens
- [ ] `HistoryEvent` class
  - [ ] birth
  - [ ] death
  - [ ] murder
  - [ ] Clan change - note that because Outsiders and StarClan/the DF are considered Clans, this covers every change
  - [ ] rank change
  - [ ] mentor change
  - [ ] disasters
    - cats are caught and spayed by Twolegs
  - [ ] leader ceremony
- [ ] `MoonEvent` class
  - [ ] pregnancy
  - [ ] leader den event
  - [ ] warriors' den event
  - [ ] mediation event
  - [ ] illness outbreak
  - [ ] relationship change
- [ ] `PatrolEvent` class
- [ ] NEW: implement secret events
- events to change
    - [ ] "Lakestar, wanting to help keep her Clanmates in shape and ready for anything, woke Mottlednose, 
  Scalekit, Freezekit, and Dovespeckle up early for morning stretches. (negative effect)"
      - Don't pick kits to do this - only warriors and warrior apprentices.
    - [ ] "Leopardwhisker doesn't even hesitate before splitting from the patrol to check on the source of the noise. 
    He quickly regrets his impulsivity, however, when an angry raccoon bursts from the bush! Leopardwhisker 
    gets quite the scare, but thankfully the raccoon only wanted to get away from him and quickly runs off 
    back into the undergrowth."
      - This event lowers the Clan's relationship with outsiders - it shouldn't.
      - Also, shouldn't "implusivity" be "impulsiveness"?

### Patrols
- [ ] If patrol_id isn't unique, check the patrol hashes against each other. If they're different, generate a 
new patrol_id


## Utility
- Methods in `scripts.utility` that need to have the Cat class passed to them should be somewhere else
- move some functions out of `scripts.utility`
    - [ ] change_clan_reputation
    - [ ] change_clan_relations
    - [ ] change_relationship_values
    - [ ] get_leader_life_notice
    - [ ] get_alive_status_cats
    - [ ] get_warring_clan
- Put in `definitions.py`
    - [ ] `resources.audio.audio_directory`
    - [ ] `resources.dicts.events.reformat_events`

### Debug mode
- [ ] `main.py` "CHECK AND SET DEBUG MODE" section
- [ ] `scripts.debug_console`
- [ ] `scripts.debug_menu`
- [ ] `scripts.debug_commands`
- [ ] `logger.debug` level

### Logging
- [ ]debug mode: logger.debug + {# from scripts.debug_menu import debugmode 
from scripts.debug_console import debug_mode}


## RedClan class
- [ ] implement the `Camp` class to keep track of herbs, freshkill, etc.
- [ ] when a cat changes Clans, where is that updated?
  - [ ] child class `FadedClan`
  - [ ] child class `DestroyedClan`
- [ ] change attribute `instructor` and `demon` to `afterlife_guide_sc` and `afterlife_guide_df`
- [ ] when will a cat join a `RedClan` object Clan?
  - [ ] when a non-kitten cat is created (e.g. at the beginning of the game, or in a patrol event)
  - [ ] when a kitten is created at the beginning of the game
  - [ ] when a kitten is found, with or without a parent
  - [ ] when a cat joins after leaving a different `RedClan` object Clan
- [ ] when will a cat leave a `RedClan` object Clan?
  - [ ] when they die
  - [ ] when they leave to join a different `RedClan` object Clan
- [ ] when a living cat switches Clans
  - [ ] changes to the `RedCat` object
    - [ ] update `RedCat.history.attachments.curr_clan_prefix`
    - [ ] update `RedCat.history.attachments.prev_clan_prefixes`
  - [ ] changes to the old Clan's `RedClan` object
    - [ ] update `RedClan.clan_cats`
    - [ ] update `RedClan.clan_cats_by_rank`
  - [ ] changes to the new Clan's `RedClan` object
    - [ ] update `RedClan.clan_cats`
    - [ ] update `RedClan.clan_cats_by_rank`
  - [ ] changes to the `CatTracker` object
    - [ ] if the cat is a nursing queen, update `CatTracker` and switch their kits' Clan
    - [ ] if the cat is a healer, update `CatTracker` if they are or are not becoming a healer
- [ ] NEW: more Clan settings
  - [ ] `canon_restraints`: overall toggle and individual toggles
    - [ ] if possible, leaders who automatically choose deputies will only choose deputies who have had apprentices
    - [ ] healers can't have mates or kits
    - [ ] automatic negative opinion modifier for code breakers and cats with HalfClan backstories
      - note that some Clan flavours remove the HalfClan opinion penalty, the healer relationships restriction, etc.
  - [ ] `num_moon_interactions_per_cat`: int
  - [ ] `relationship_modifier`: int
      - This is a number that is automatically added to the relationship of all cats in the same Clan with each other.
      For example, it would be 5 for ThunderClan since being ThunderClan cats would make two cats more inclined
      toward each other; for the 'Clan' that contains kittypets, or the 'Clan' that contains loners and rogues, it
      would be 0, since every two random loners don't have connections to one another.
  - [ ] `opinion_of_clan`: dict
      - Each Clan has an opinion of others, not a relationship with them. Events can raise and lower these, depending
       on the side - e.g. if SkyClan finds a litter of ShadowClan kits and returns them, then ShadowClan's opinion of
       SkyClan will increase because of gratitude, but maybe SkyClan's opinion of ShadowClan will decrease because of
       how irresponsible this event made them seem


### MoonHandler class
Calls methods that take care of the things that happen when you hit the `Timeskip (go forward one moon)` button.
- [ ] 

### Camps
- [ ] `Camp` class
- [x] implement an enum for each camp `CampKey`
- [ ] den locations for each camp background
- [ ] keep track of freshkill
- [ ] keep track of the healer's den
  - [ ] herb stockpile
  - [ ] how many healers does the Clan need right now?
  - [ ] which cats are in the healer's den - e.g. cats with some, but not all, conditions


## RedCat class
- [ ] `FadedCat` child class
  - [ ] Cats should have a can/can't have kits toggle. If your camp is in a Twolegplace, one disaster is that a 
  bunch of humans come and TNR a bunch of your cats, and don't let newborns, kits, and elders go.
  - [ ] With new relationship and event systems, sometimes cats will tell other cats stories about dead cats 
  they had a strong relationship with OR who had high fame, or who they heard about through a story. This 
  prevents that cat from fading.
- [x] method to create a `RedCat`
- [ ] pregnancies should generate kits the moon that they're born
- [ ] what method is called:
  - [ ] when a cat changes ranks during a moon event `RedCat.change_rank`
  - [ ] when a cat changes ranks because of the player `RedCat.change_rank`
  - [ ] when a cat dies because of the player `RedCat.change_rank`
  - [ ] when a cat dies because during a moon event `RedCat.kill`
  - [ ] when a cat dies on patrol `RedCat.kill`
  - [ ] when a cat changes Clans because of the player (e.g. exile, searching for them) `RedCat.change_clan`
  - [ ] when a cat changes Clans during a moon event `RedCat.change_clan`
  - [ ] when a cat changes Clans on patrol `RedCat.change_clan`
- [ ] when will a cat change ranks?
  - [ ] kit -> apprentice
  - [ ] graduation
  - [ ] warrior <-> mediator <-> healer <-> queen
  - [ ] promotion to deputy, leader
  - [ ] demotion from deputy
  - [ ] when they become a loner, rogue, or kittypet
- what method is called:
  - [ ] when a cat changes ranks during a moon event `RedCat.change_rank`
  - [ ] when a cat changes ranks because of the player `RedCat.change_rank`
  - [ ] when a cat dies because of the player `RedCat.change_rank`
  - [ ] when a cat dies because during a moon event `RedCat.kill`
  - [ ] when a cat dies on patrol `RedCat.kill`
  - [ ] when a cat changes Clans because of the player (e.g. exile, searching for them) `RedCat.change_clan`
  - [ ] when a cat changes Clans during a moon event `RedCat.change_clan`
  - [ ] when a cat changes Clans on patrol `RedCat.change_clan`
- [ ] implement `RedCat.change_rank`
- [ ] implement `RedCat.kill`
- [ ] implement `RedCat.change_clan`
- [ ] update save files and how they're parsed
- [ ] update how the `CatTracker` tracks nursing queens
- [ ] When switching Clans:
  1. [ ] check all save files (what folder names exist?)
     - [ ] don't forget to handle the case of there being zero (valid) save files
     - [ ] if a save file isn't valid(has a malformed `XClan.json/yaml` file, or none) display it as grayed out in the
`SwitchClans` screen
  2. [ ] the player picks a save file
  3. [ ] create CatTracker object
  4. [x] load Clan settings
  5. [ ] create Clan objects for all Clans in the save
     - [ ] camp file
        - [ ] herb supply
        - [ ] freshkill pile
  6. [ ] load cats in the Clans one by one
  7. [ ] load conditions
  8. [ ] load relationships
  9. [ ] load ongoing events
- [ ] Have a button on the main menu that says "convert saves"
- NEW: hidden trait(s?) or hook(s?) that affect the cat's thoughts. E.g. if a cat's hidden trait is "gossip", thoughts
tagged with "gossip" will appear for them more often


## Skills
- use only one Skill class
    - [ ] scripts.cat.skills.CatSkills
    - [ ] scripts.cat.skills.Skill
- [ ] combine the multiple enums for the same thing - SkillPath, HiddenSkillEnum, SkillTypeFlag, Skill, and CatSkills
  - [ ] DataClass Skill
  - [ ] Enum CatSkill

### Pelts
- combine multiple white patch patterns, like `LifeGen-GeneMod` can


## Names
- [ ] prefix and suffix can't be from the same source
- [ ] legacy naming
- [ ] named after white patches


## Personality
- Can change throughout a cat's life, it just changes progressively less the older a cat gets.


## Text handling and conversions
- TextHandler class
- ConversionManager class
  - [ ] Move Pelt conversion stuff into the load save, not in the Pelt class itself.
  - event_analyzer.py
- [ ] {CLAN/m_c}, {CLAN/r_c}, {CLAN/c_n}, {CLAN/o_c_n}


## UI
- [ ] training patrols aren't selectable
- [ ] replace strings with enums where possible
  - [ ] find all calls to `str.casefold()`
  - [ ] replace `scripts.cat.enums.CatAgeEnum` with an enum in `definitions`
    - [x] find and replace
    - [ ] not a StrEnum, but instead tuples of the age ranges?
- Screen text to fix
  - [ ] "Verbenafoot, Ivypuddle, and Stagshade had a nice talk, while eating.
  screens.relationships.neutral_postscript"
  - [ ] "Piperswoop, Stagshade, and Bluestripe took a sunbath and had a little 
  small talk.screens.relationships.neutral_postscript"
  - [ ] "screens.mediator.already_workedThis pair has already been mediated this moon."
- [ ] Add `faith` tab to the Profile screen.
  - [ ] Get rid of skills blurb, and put it in its own tab too?
  - [ ] Maybe put the skills and background + history in the same tab as the notes?
- `Cat List` screen
  - [ ] switch to scrolling up and down instead of pages
- `Profile` screen
  - Buttons
    - Previous Cat
    - Next Cat
    - Camp, Cat List, or Events depending on where the (replaces Back)
    - Inspection (magnifying glass icon)
      - Include customize cat button on this screen
  - Blurbs, top to bottom
    - Left side
      - gender alignment
      - eye colour
      - brief pelt description
      - fur length
      - age (in moons) and age category (kitten, adolescent, etc.)
    - Right side
      - rank
      - personality
      - nutrition
      - flavour string
  - Tabs, left to right
    - Top row
      - personal
        - subtabs: history, skills, notes
        - TODO use icons to differentiate between notes, history, and skills
        - TODO differentiate between the open tab, the closed tabs, and hovering over a closed tab
      - relations
        - subtabs: family tree, adoption, see relationships, choose mate
      - roles
        - subtabs: manage roles, change mentor
      - edits
        - subtabs: change name, trans your gender, specify gender, cat toggles
    - Bottom row: 
      - dangerous
        - subtabs: exile cat, kill cat, destroy accessory
      - conditions
      - faith


# Planned features

## Game map
- [ ] Terrain class
  - [ ] To generate a map, ask: how big the map should be, what the largest body of water nearby is: determines 
  the likelihood of each biome, from most to least.
    - Ocean -> Potential biomes are Beach, Plains, Wetlands, Mountain, Forest, Desert
    - Lake -> Potential biomes are Forest, Mountain, Plains, Desert, Beach, Wetlands
    - River -> Potential biomes are Wetlands, Plains, Desert, Forest, Mountain, Beach
  - [ ] All maps will have at least one Twolegplace.
  - [ ] Where to converse with the afterlife of your choosing.
    - default: Moonplace
    - Biome.Beach: Mooncove
    - Biome.Desert: Moonpool - It's an oasis
    - Biome.Forest: Moonhollow - In the densest part of the forest, where a sudden clearing in a dense forest with 
    no trees, where the moonlight shines so brightly it temporarily blinds cats who enter from the surrounding 
    forest too suddenly.
    - Biome.Mountain: Moonpeak
    - Biome.Plains: Moonfalls - In a hollow in the plains, one end of the hollow is gradual while the other
    is a cliff. A stream that runs through the plains ends here in a small waterfall, with a pool beneath 
    shallow enough for a healer cat to lie down in it and fall asleep under the spray of the waterfall to 
    connect with their ancestors.
    - Biome.Wetland: Moongrove
    - Biome.Twolegplace: Moonstone - The top of a public art piece in a small public park. The art piece is a 
    mirrored sculpture, which the cats must climb up to the top of, where a round shape in the sculpture provides 
    a place where they can sleep. The surface is hard and cold, so the cats assume it's made of stone.
- [ ] Pick your Clan camp's square first, and from then on it's cheaper to get more territory tiles of the same biome 
as your camp then of other biomes.
  - Also, maybe there's a ranking of biomes that makes it so (e.g.) (Beach - Wetland) < (Beach - Mountain)


## Flavour
- Clan flavour 
  - Not explicitly displayed anywhere; it just affects some events and thoughts.
  - A Clan gets two flavour categories, then a value for each.
    - **decoration_category:** pale summer flowers, bright spring flowers, shells from the river, shells 
    from the ocean, Twoleg trash, bird feathers
    - **position_category:** Storyteller (Starteller? Preserves Clan history), Singer (same as Storyteller? Skald)?, 
    Code Enforcer (), Greenkeeper (a gardener; makes it easier for your healer to get herbs)
    - **rules_category:** healers can have mates and kits, remove HalfClan backstory's negative opinion modifier
      - Only available if the `canon_limitations` Clan setting is set to `True`.
    - The Clan flavour categories and choices can change depending on events and the cats in the Clan.
  - Clans have naming themes. Or maybe each leader has preferred naming themes? Or both?
- [ ] Flavour strings for cats go on the cat's profile page, where backstory and skills are currently.
- [ ] Skills are either moved to their own tabs or to a subtab in the same tab where notes live on the 
profile screen.
- [ ] Clan background
  - When you have finished generating your Clan, a Clan background is chosen randomly and displayed on a screen
  with the title "INTO THE FOREST" alongside your Clan's symbol. 
    - Or "INTO THE FOREST" is the button you hit?
    - Options:
      - an entirely new Clan formed by cats looking for mutual safety (like in Dawn of the Clans)
      - a Clan that was destroyed recently and is being reformed
      - an ancient Clan that is being reformed (like SkyClan)
      - a Clan where StarClan guided all or most of the cats to form the Clan
      - a Clan where StarClan guided only the leader, medicine cat, or both to form the Clan
- [ ] 


## Storylines
- [ ] Storyline class
- Inspired by events that currently exist
  - [ ] "After a particularly controversial decision, {CLAN/main/leader}'s leadership is called into 
  question. Camp is  filled with whisperings about whether they're really fit to be the head of {CLAN/main}Clan."
- Inspired by backstories that currently exist
  - [ ] ClansHealerOther: "{CAT/main} was once a healer in another Clan."
    - Did they leave willing? As an exile? Because their clan was destroyed? Why?
    - Maybe add some more backstories to specify
- Inspired by nothing in particular
  - [ ] If the Clan's guide is from one afterlife, and the leader believes deeply in the other, get a new guide
  - [ ] If a cat is exiled, and they have a bloodthirsty/sensitive child, make it so the child might decide 
  to follow them into exile (Tawnypaw-style) because they feel judged
- [ ] 


## More kinds of events
LeadCeremony = "lead_ceremony" # TODO implement LeadCeremony class
DepCeremony = "dep_ceremony" # TODO implement DepCeremony class
    # cat_age: int - age of the cat when they became deputy
    # clan: Clan - which Clan the cat became the deputy of
    # leader: Cat - the leader who made the cat their deputy
AppCeremony = "app_ceremony" # TODO implement AppCeremony class
    # apprentice: Cat - which cat became an apprentice
    # mentor: Cat - which cat became a mentor
GradCeremony = "grad_ceremony" # TODO implement GradCeremonyEvent class
    # cat_age: int - age of the cat when their apprenticeship ended
    # honor: str - what the cat was honored for
    # influence_trait: ?? - how the cat's mentor influenced their personality
    # influence_skills: ?? - how the cat's mentor influenced their skills
ClanFoundation = "clan_found" # TODO implement ClanFoundation class
    # season: Season - the season when the Clan was founded
ClanDisband = "clan_disband" # TODO implement ClanDisband class
    # season: Season - the season when the Clan was disbanded