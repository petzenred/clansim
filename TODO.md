# TODO

- [ ] different languages
- [ ] move logging to its own file
- [ ] move loading to its own file and separate when it happens so Clan info is loaded when the ClanScreen is
- [ ] handle ClanGen and ClanSim changelogs
- [ ] name: Whitetoe

## Cat generation
- [ ] change how naming works

## Biomes
- [ ] add playlists for new biomes (wetlands, Twolegplace, )

## Clan creation

Game mode and gameplay settings
- Settings which are **NOT** available after Clan creation
  - Game mode (Classic Mode/Expanded Mode)
    - The explanations for each game mode are tooltips, not displayed to the right of the selection.

## Skills
- [ ] split HUNTER and FIGHTER into biome-specific variants
- [ ] add new hidden skills for being from different clans
- [ ] differentiate the CLAIRVOYANT, OMEN, PROPHET, and STAR skills

## Events
- new events 
	- [ ] kidnap kits from another clan
		- [ ] make clan relations worse, if they get caught
		- [ ] whether they get caught or not -> other clan's temper aspect 'aggression' goes up by 2
		- [ ] Can be ordered by clan leader, or done by an individual cat's choice
		- [ ] can be a secret
  - [ ] other clan asks for freshkill
- storylines
    - [ ] prophecy storyline
        - [ ] must have a non-medicine cat skill 3 >= skill.STAR or a medicine cat with at least one of the following 
      skills: STAR, PROPHET, OMEN, CLAIRVOYANT
    - [ ] search for a cat who went missing
    - [ ] search for a cat who was kidnapped by Twolegs
      - [ ] the cat might come back spayed/neutered


## Interactions
Every moon, each cat picks another cat and then generates an interaction depending on both cats' personalities, 
reputations, tags, and their relationship to one another.


## Leadership decisions
- [ ] ask other clans for freshkill
- [ ] ask other clans for herbs


## Reputation
scripts/cat/history.py

Cats will have a new, visible stat: their reputation, calculated as the average of how each cat in their own Clan feels 
about them. My current plan for this stat is to use it in automatic leader succession decisions (see the relevant 
section below), but please feel free to suggest other uses for it as well!

Additionally, cats can gain reputation tags based on their personal history - the results of random events they took 
part in, decisions they've made, their lineage, etc. Most tags will add or remove custom patrol events and/or 
relationship interactions. However, some tags can affect leadership succession.

| Tag        | Description                                                                                        |
|------------|----------------------------------------------------------------------------------------------------|
| scorned    | This cat has done something truly heinous, and everycat knows about it.                            |
| shunned    | This cat has acted questionably in the past, and will have to work to earn their clanmates' trust. |
| valorous   | This cat has endangered their life for the sake of the Clan.                                       |
| celebrated | This cat's name is known in every Clan and will be remembered for generations to come.             |


scripts/cat/history.py


### Reputation tags

- **Scorned**: This cat has done something truly heinous in the past, and every cat knows about it.
	- Earn this tag by murdering a kit, a clanmate without reason, or a mediator ([how mediators work](#mediators) is 
  changed).
	- Earn this tag by attacking a medicine cat patrol from any Clan.
	- Cats with this tag might be thrown out of their Clan depending on the leader's personality and relationship to 
  them.
	- Cats with this tag will [never be considered an option for deputy](#leadership-decisions), and if a deputy earns 
  this tag they will always be demoted to warrior.
	- ***TODO*** What happens if a leader earns this tag?
- **Shunned**: This cat has acted questionably in the past, and will have to work to earn their clanmates' trust.
	- Earn this tag by leading a patrol and making a decision that gets cats killed.
	- Cats with this tag will *most likely* [not be considered an option for deputy](#leadership-decisions).
- **Valorous**: This cat has endangered their life for the sake of the Clan.
	- Cats can earn this tag by endangering their life for the sake of their clanmates.
- **Celebrated**: This cat's name is known in every Clan and will be remembered for generations to come.
	- This cat is the Firestar of this Clan.
	- This tag should be essentially impossible to get - I want to make sure that cats who get this tag are already 
  especially memorable.


Note that how your Clan views some acts might change depending on your Clan's temper and, if another Clan is 
involved, your Clan's relationship to the other Clan. For example, say the WindClan warrior Mudclaw starts a 
skirmish with a ThunderClan patrol and kills a ThunderClan cat.

Clan relationship	WindClan temper		Result
Allies				high social			Mudclaw will gain the *shunned* tag for putting the Clan in danger by angering an ally and bordering Clan.
Allies				high aggression		Mudclaw's clanmates have a random chance to lose trust in him because he did not act in the Clan's best interest. One day, I'd like this to be determined by personality instead of random chance.
					neutral-low social	

Neutral				aggression > social	Mudclaw's clanmates have a random chance to gain respect for him.
Neutral				social > aggression	Mudclaw's clanmates have a random chance to lose respect for/trust in him.

Enemies				whatever			Mudclaw will gain the *valorous* tag if the cat he killed was the other Clan's deputy or leader. His clanmates will have a random chance to gain respect for/trust in him.


## Patrols
- new patrols
	- [ ] medicine cats going to the medicine cat gathering to talk to StarClan
- [ ] cats who go on any patrol alone can go missing, allowing them to be searched for


## Visuals
- [ ] separate cats' inner ear color and nose color
- [ ] add non-white patches - e.g. Marlowe and Aloy's chin patches


## Sounds
- [ ] Only have one noise for button hovering - randomly playing one of six sounds makes it seem like this only works some of the time
- [ ] Only have one noise for button presses - randomly playing one of five sounds makes it seem like this only works some of the time
- [ ] No music plays on cat screen
- [ ] What's the difference between MusicManager.audio_disabled_f and MusicManager.muted_f?


## Settings
- [ ] Add settings keys to `definitions.py` and use them everywhere

# BACKLOG

- [ ] This task is postponed

# DONE

- [x] This task is done #prio1
- [-] This task has been declined