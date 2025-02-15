# ClanSim Planned Features
The ClanGen systems for traits, skills, and relationships are reused in their entirety. I use them in new ways, and add 
new features to the relationship system, but nothing will be removed anywhere. 

!!! todo "TODO" [Clan Generation/Claim territory](#claim-territory)

!!! todo "TODO" [Clan Generation/Choose Clan camp](#choose-clan-camp)

!!! todo "TODO" [find a FullGen link](#overpopulation)


## Clan territories
There is now a tiled game map where each square is either claimed by a specific Clan or is explicitly neutral area 
(e.g. for communicating with StarClan and/or holding Gatherings). 

- Your Clan needs to regularly patrol their territory (especially squares that are Clan borders!).

## Biomes
ClanGen has a partially-implemented [terrain system](/docs/dev/writing/clangen-biomes.md). I've included these 
categorizations in this mod. Each tile in the map has a terrain, which effects which patrol events happen there.

### Hunting
The hunting skill has been broken up into biome-specific variants. 

| Biome       | Skill   |
|-------------|---------|
| Beach       | Fishing |
| Desert      |         |
| Forest      |         |
| Mountainous |         |
| Plains      |         |
| Wetlands    |         |





## Reputation
Cats will have a new, visible stat: their reputation, calculated as the average of how each cat in their own Clan feels 
about them. My current plan for this stat is to use it in 
[automatic leader succession decisions](#leadership-succession), but please feel free to suggest other uses for it as 
well!

Additionally, cats can gain reputation tags based on their personal history - the results of random events they took 
part in, decisions they've made, their lineage, etc. Tags will add or remove custom patrol events and/or relationship 
interactions. However, some tags can also affect leadership succession.

| Tag        | Description                                                                                        | Example                 |
|------------|----------------------------------------------------------------------------------------------------|-------------------------|
| scorned    | This cat has done something truly heinous, and everycat knows about it.                            | Scourge, Tigerclaw/star |
| shunned    | This cat has acted questionably in the past, and will have to work to earn their clanmates' trust. | Dark Forest trainees    |
| valorous   | This cat has endangered their life for the sake of the Clan.                                       | Brambleclaw, Alderheart |
| celebrated | This cat's name is known in every Clan and will be remembered for generations to come.             | Firestar                |

Note that how your Clan views some acts might change depending on your Clan's
[temper](/docs/dev/writing/leaders-den-events#player_clan_temper-liststr) and, if another Clan is involved, your Clan's 
relationship to the other Clan.


## Patrol overhaul
This is going to be the most obvious, and probably the most consequential, change to gameplay.

### Hunting + border patrols


- The longer a tile in your territory goes without being patrolled, the more likely it becomes that the next time a cat 
passes through it, a dangerous event will happen.
- Each cat now has some amount of stamina (related to their experience and age), and each square they pass through 
will take up some amount of their monthly (moonly?) energy. Patrols will now have to be managed much more mindfully.
- Each tile has a specific [terrain](/docs/dev/writing/#clangen-biomes), which influences which events can happen in it and which skills cats need to 
succeed at fights and hunts happening there.
- Patrolling Clan borders more often can raise your Clan's 
['aggresion' temper aspect](/docs/dev/writing/leaders-den-events#player_clan_temper-liststr).

### Medicine cat patrols
Cats will specifically seek out herbs that are relevant to any current medical problems in the Clan. 

### Training patrols
If successful, these are guaranteed to result in a mentor's skills or personality influencing their apprentice.

### 'Search For' action
Allows your Clan to search for cats who disappeared, were kidnapped by Twolegs, etc. This used to be a leadership 
decision, but I think it makes more sense here.


## Relationships and interactions

### Leadership succession
If the setting for Clan leaders choosing their own deputies is left on, there is a new system for how deputies are 
decided. 
The factors a leader will consider when choosing a deputy are:
- How much the leader trusts a candidate.
- How much the leader likes a candidate.
- How much the leader respects a candidate.
- How high the cat's reputation is among the Clan.

How each factor is weighted depends on the current leader’s personality. E.g. responsible leaders completely disregard 
their personal like for a cat and weigh respect, trust, and reputation equally; charismatic leaders place a heavier 
weight on popular opinion; loving leaders place a higher weight on their personal like; etc.


## Other Clans
- Now populated with actual cats, who your cats can interact with! Although not a full Clan of them because I don’t 
want to make lag.
    - Leaders and deputies of all Clans are simulated, as well as at least 1 medicine cat per Clan. 
- Inter-Clan romances might result in one cat moving to a new Clan. This does mean that your cats might move to be with 
a loved one! If so, the cat who left your Clan will continue to be simulated and has a chance to return, if their 
Clan is willing to take them back.
	- If their mate dies or they break up, the cat who left your Clan might try to get back into your Clan. If they 
don't, or if they fail, they will become a loner.
- Other clans will start wars to claim your territory.
	
	




## Clan Generation
Titledrop heyo!!

Seriously though when you hit ‘New Game’ there’s some stuff new to ClanSim. Below is a compare/contrast table for 
creating new Clans in ClanGen and ClanSim.

| Step | ClanGen             | ClanSim                                                |
|------|---------------------|--------------------------------------------------------|
| 1    | Set game mode       | Set game mode and gameplay settings                    |
| 2    | Name the Clan       | Claim territory                                        |
| 3    | Pick leader         | Choose Clan camp location                              |
| 4    | Pick deputy         | Name the Clan and choose icon                          |
| 5    | Pick medicine cat   | Pick or build leader                                   |
| 6    | Pick 4-7 other cats | Pick or build deputy, or leave choice up to the leader |
| 7    | Choose Clan camp    | Pick or build medicine cat                             |
| 8    | Choose Clan icon    | Pick or build 4-7 other cats                           |

### Game mode and gameplay settings
Settings which are **NOT** available after Clan creation
- game mode (Classic Mode/Expanded Mode)
- randomize relationship values when creating Clan
  - This setting is also available from the main menu's Settings, but here it can be turned on/off for individual Clans.
- use naming conventions for your Clan
  - Did I steal this idea directly from Dwarf Fortress? Yes I did. Am I sorry at all? No I’m not.
  - All names in the game have been sorted in categories based on vibes, and if you like you can restrict which ones 
your Clan will randomly select from.
  - See [this file](/resources/dicts/names/names.json) for the name categories
- choose the number of Clans present in your game (or leave it to chance)
  - Due to other Clans being generated in greater detail, and a map needing to be generated for the game, this is 
mainly a lag prevention feature.
  - There is a hard cap of 4 other Clans (so 5 Clans total, including your own).
- name the other Clans and choose their icons (or leave it to chance)
  - Are you going for a playthrough with a specific feeling? Make sure the other Clans' names don't harsh your vibe.

### Claim territory

### Choose Clan camp
You need to pick a square in your Clan's territory to be your camp.

Settings which are available after Clan creation
- allow mild gore and blood in patrol artwork
  - This setting is also available from the main menu's Settings, but here it can be turned on/off for individual Clans.
- everything available in the Settings menu inside the game (sorted into general, relation, and role)

### Name your Clan and choose icon
Combine two separate steps, since a Clan's name and icon are linked.

There is now an option to enforce your Clan's first leader having the same name as the Clan itself, Dawn of the 
Clans-style. This can go either way - you can name your Clan now and have the leader's name changed in the next step, 
or whatever the leader's name in the next step ends up being will retroactively be filled in here, and a suitable icon 
chosen using the same logic as if you had hit 'random'.

### Picking random cats vs. building cats
Generating random cats and picking from them works exactly like it did in ClanGen.
Building a Clan lets you design each individual cat, because surely I can't be the only person who's wanted an easy way 
to create a Clan made of cats I know IRL.



## Storylines
- Events which can be triggered only by cats who have already triggered other events.
- Now, prophecies received from StarClan can have consequences in your game!
- Make searches for missing cats more detailed.


## Inclusions from other mods

### Overpopulation
This is one of the biggest problems with ordinary ClanGen, so I'm planning a few features to tackle it.
- if kittens don't thrive, they will not survive to apprenticehood
  - based on similar feature from [FullGen]()
  - having more medicine cats and kit sitters/queens will reduce the likelihood of kittens not thriving


### [GeneMod](https://github.com/Chinch-Bug/clangen-genemod.git)

- Optional toggle that lets you use realistic cat genetics! I might not be able to include customizable cats if this 
toggle is on, though, just because of how complicated that would get.


## Other random stuff

### Mediators
- The mediator is no longer an in-Clan position - it’s an external cat who your Clan can appeal to for inter-Clan 
relationship help. This is more reflective of the position in the books and is a less broken game mechanic.
	- If a cat in your Clan wants to become a mediator, they leave your control. Therefore, you will be asked before 
this happens.

### Save files
- Import saves from JSON files.
- Import ClanGen Clans to play them as-is in ClanSim.
	- You will need to manually set changed (hunter/fighter skills) and new (reputation) values for each cat.

### Visual changes
- The relationships tab of the Events screen now uses arrows instead of a scroll bar to reduce rendering lag.
	- I'm not the only person who had this issue with larger Clans, right?
- On the ClanCampScreen, a pile of freshkill appears near the `clearing` button that dynamically reflects how much 
freshkill your Clan has.

### The Warrior Code
I'm not sure that I want to implement this at all. However, I think it might be interesting to implement a system where 
a leader event is added (with VERY high difficulty) in which your Clan's leader advocates for a change to the warrior 
code - e.g. allowing cats to change Clans to follow loved ones. Whatever the current warrior code dictates would affect 
how different actions are seen by other cats, and maybe I could add some tags that relate to this system - e.g. 
traditionalist, progressive, etc.

