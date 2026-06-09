# New Text Formatting for ClanSim

All text to be replaced must be surrounded by brackets.



## Filters

If you don't want to specify any part of a filter (e.g. if there are no tags, or no specific camp conditions required) 
then you don't need to include it (or you can set it to ~, which will be read as None).

```yaml
filter:
    tags: ~ # list of string tags
    location: # where is the event happening?
      is_camp: false
      biome:
        allowed: ~ # List of strings corresponding to members of definitions.Biome.
        disallowed: ~ # List of strings corresponding to members of definitions.Biome.
    cats:
        # !LIMITATION! The main cat must always be from the player's Clan.
        main: # `main` is the cat code for this cat.
          AND: # All of these conditions must be true; if trait and rank are both given, the main cat will be chosen from cats with the required trait AND the required rank.
            trait: ~ # List of personality trait strings.
            rank: ~ # List of strings corresponding to members and properties of definitions.Rank.
            age: ~ # TODO this filter doesn't work yet, sorry
          OR: # Only one of these conditions must be true; if trait and rank are both given, the main cat will be chosen from cats with the required trait OR the required rank OR with both.
            trait: ~ # List of personality trait strings.
            rank: ~ # List of strings corresponding to members and properties of definitions.Rank.
            age: ~ # TODO this filter doesn't work yet, sorry
          NOR: # None of these conditions can be true; if trait and rank are both given, the main cat will be chosen from cats who don't have a listed personality trait AND who don't have any of the listed ranks.
            trait: ~ # List of personality trait strings.
            rank: ~ # List of strings corresponding to members and properties of definitions.Rank.
            age: ~ # TODO this filter doesn't work yet, sorry
        cat1: # `cat1` is the cat code for this cat.
          AND: # All of these conditions must be true; if trait and rank are both given, the main cat will be chosen from cats with the required trait AND the required rank.
            trait: ~ # List of personality trait strings.
            rank: ~ # List of strings corresponding to members and properties of definitions.Rank.
            age: ~ # TODO this filter doesn't work yet, sorry
            main_clan: ~ # Boolean: is this cat from the same Clan as the main cat?
            rel: ~ # TODO this filter doesn't work yet, sorry
          OR: # Only one of these conditions must be true; if trait and rank are both given, the main cat will be chosen from cats with the required trait OR the required rank OR with both.
            trait: ~ # List of personality trait strings.
            rank: ~ # List of strings corresponding to members and properties of definitions.Rank.
            age: ~ # TODO this filter doesn't work yet, sorry
            main_clan: ~ # Boolean: is this cat from the same Clan as the main cat?
            rel: ~ # TODO this filter doesn't work yet, sorry
          NOR: # None of these conditions can be true; if trait and rank are both given, the main cat will be chosen from cats who don't have a listed personality trait AND who don't have any of the listed ranks.
            trait: ~ # List of personality trait strings.
            rank: ~ # List of strings corresponding to members and properties of definitions.Rank.
            age: ~ # TODO this filter doesn't work yet, sorry
            main_clan: ~ # Boolean: is this cat from the same Clan as the main cat?
            rel: ~# TODO this filter doesn't work yet, sorry
```

## New codes

- `{CAT/main}` prints the main cat's name.
  - `{CAT/cat/rel.child}` prints the name of a random one of `cat`'s children.
  - `{CAT/cat/rel.mate}` prints the name of a random, current mate of `cat`, dead or alive. Note that if a mate dies, sometimes it will take a cat a while to move on, and until they do the dead cat is still listed as their mate.
  - `{CAT/cat/rel.mate/live}` prints the name of a random, living, current mate of `cat`.
  - `{CAT/cat/rel.mate_prev}` prints the name of a random cat who `cat` was previously involved with, dead or alive.
  - `{CAT/cat/rel.mate_ever/dead/unknownresidence}` prints the name of a random mate of `cat`, current or previous, who is dead and not in StarClan or the Dark Forest.
  - `{CAT/cat/rel.mate/darkforest}` prints the name of a random, current mate of `cat` who is in the Dark Forest. At the moment, only dead cats can be in the Dark Forest, but in a hypothetical Brambleclaw situation that wouldn't be the case.
- `{PRONOUN/main/object}` prints 
- `{VERB/cat/continue/continues}` depends on the `Pronoun` **class's** `conju` member.
- `{}`

### CAT
All cats in an event have a **cat code**, made of letters and numbers (please keep them brief!) The cat code is 
unique to that cat within an event, and used everywhere that cat is referred to.
- **Two cat codes can't refer to the same cat.** If a cat fits more than one filter, but is selected for the first,
that cat *can't be chosen for the second filter*. If no valid cats remain for the second filter, the filter will 
just fail (which is handled differently depending on whether it's a filter for an event, for a backstory, etc.) so 
**you should try to put the most specific filters first.**

The tag structure goes:
1. `CAT`
2. Cat code : who are we talking about here?
3. Filter for cats who have a specific relationship to the cat referred to by `cat_code`.
   - `rel.mate` : fetches the cat's current mates, alive and dead, in any Clan, with any rank, etc.
   - `rel.mate_prev` : fetches the cat's previous mates, alive and dead, in any Clan, with any rank, etc.
   - `rel.mate_ever` : fetches the cat's current and previous mates, alive and dead, in any Clan, with any rank, etc, you get the idea.
   - `rel.child` : fetches the cat's children, biological and adopted.
   - `rel.parent` : fetches the cat's parents, biological and adopted.
   - `rel.sibling` : fetches the cat's siblings, including those born before and after the cat.
   - `rel.littermate` : fetches the cat's littermates.
   - `rel.mentor` : fetches the cat's current or last mentor.
   - `rel.prev_mentor` : fetches the cat's previous mentors (excluding their last mentor if the cat is no longer 
   - an apprentice).
   - `rel.apprentice` : fetches the cat's current apprentice.
   - If you want the cat's leader, deputy, medicine cat, mediator, or a random Clanmate, you should add another 
   cat code and filter for it there.
   - `rank` : fetches the cat's rank.
   - `pelt` : fetches the cat's pelt.
4. If the previous filter fetched a cat, you can filter for cats with certain statuses.
   - `dead` : Probably self-explanatory.
     - Further sub-filter where you can specify `.../dead/starclan`, `.../dead/darkforest`, or `.../dead/unknownresidence`
   - `live` : Probably self-explanatory. The filter will also catch `alive` and `living`.
   - `emo.pos` : fetches only cats who the cat had a positive relationship with.
   - `emo.neg` : fetches only those who the cat had a negative relationship with.
If the previous filter fetched a cat's pelt, you can filter for certain aspects of the pelt.
   - `colour`
   - `tortie_colour`
   - `length`

### CLAN
The tag structure goes:
1. `CLAN`
2. Whose Clan is this? If you don't provide a third argument, only the prefix of the Clan's name will be returned.
   - You can use `cat.cat_code`, e.g. `cat.main` to get the Clan name for a specific cat.
      - i.e. `main`, `other_clan_patrol_leader`
   - You can use `clan.main`, `clan.other`, or `clan.clan_id`
     - i.e. if the main 
3. Further specification. One of:
    - `leader` : returns the name of the current leader of the Clan specified in (2).
    - `deputy` : returns the name of the current deputy of the Clan specified in (2).
    - `medicine` : returns the name of a random medicine cat or medicine cat apprentice from the Clan specified in (2).
    - `mediator` : returns the name of a random mediator or mediator apprentice from the Clan specified in (2).
    - `biome` : returns the biome where the specified Clan's camp is.


**Example:** Say the player Clan is ThunderClan [^]. Using filters, we've assigned the cat code `tc_cat` to a randomly
chosen cat from ThunderClan. Each specification would give:
    - `{CLAN/clan.main}` -> "Thunder"
    - `{CLAN/cat.sunbeam/leader}` -> "Squirrelstar".
    - `{CLAN/cat.sunbeam/deputy}` -> "Ivypool".
    - `{CLAN/cat.sunbeam/medicine}` -> one of "Jayfeather", "Alderheart".
        - There isn't a medicine cat apprentice in ThunderClan right now, but if there was, they would also be a 
potential pull here. If you want to specify a fully-fledged medicine cat, and not an apprentice (or vice versa) use a 
new cat code and filter for one.
    - `{CLAN/sunbeam/mediator}` -> this will only return "Tree" although if ThunderClan had multiple mediators, 
there would be an equal chance of it being any of them.
    - `{CLAN/sunbeam/biome}` -> "forest".
    - If the third argument returns the same cat asking for it (e.g. `{CLAN/cat.squirrelstar/leader}` 
still returns `Squirrelstar`)

**Example:** The player Clan is still ThunderClan. Say we want to list the leaders of all the other Clans around the 
lake. In this case, it probably makes more sense to use a filter to save one cat from each Clan to 

[^] As of the book *Thunder*.

### PRONOUN
The tag structure goes: 
1. `PRONOUN`
2. The cat's code (e.g. `main`).
3. The tense of the pronoun. One of: 
   - `object` = him/her/them
   - `subject` = he/she/they
   - `poss` (possessive) = his/her/their
   - `inposs` (inpossessive) = his/hers/theirs
   - `self` (himself/herself/themself)


### CONJU
This replaces `VERB`.

The tag structure goes: 
Example: `{CONJU/cat/continue/continues}`

In `Cat.pronoun`, one option is `conju`, which dictates which of the options after `cat` will be used. From the default
pronouns:
- 'they' has a `conju` value of 1, and so would use 'continue' -> 'they continue"
- 'he' and 'she' have `conju` values of 2, and so would use 'continues' -> 'he continues', 'she continues'


## Examples

### Example 1
Let's say we want to write an event where an apprentice has a dream that they think contained an omen. The text in this
event describes the excited apprentice describing their dream to a medicine cat and a skeptical onlooker.

The apprentice is `main` (technically `main` could be any of the three cats, but I think in this case the main cat 
being the apprentice makes the most sense). The medicine cat will be `medicine` and the skeptic will be `skeptic`.

The most basic filter we could buid that would still work looks like this:

```yaml
filter:
    cats:
        main:
          AND:
            rank: 
              - apprentice
        medicine:
          AND:
            rank:
              - medicine cat
        skeptic: ~
```

However, at this point, `medicine` could be any medicine cat, alive or dead, and from any Clan. `skeptic` could be 
literally any cat who has ever existed in the save file who isn't `main` or `medicine`! Let's make their identities a 
bit more specific. First of all, we want both `medicine` and `skeptic` to be from the apprentice's Clan, because why 
else would they be around for the apprentice to speak to when they first wake up from the dream?

```yaml
medicine:
  AND:
    rank:
      - medicine cat
    main_clan: true
skeptic:
  AND:
    main_clan: true
```

Then we decide we want to give the skeptic a reason for not believing `main` when they talk about their dream. Maybe 
the skeptic is generally dismissive, which we'll represent with their having the `cold` personality trait. Or maybe the 
skeptic is a medicine cat themself, and doesn't quite believe that a non-medicine cat would be sent an omen; we'll 
specify that they can be a medicine cat or a medicine cat apprentice. Finally, we don't need the skeptic to be cold AND 
a medicine cat - both would be fine, but only one of the conditions would do.

```yaml
skeptic:
  AND:
    main_clan: true
  OR:
    trait:
      - cold
    rank:
      - medicine cat
      - medicine cat apprentice
```

We decide that we don't want this event to be used by cats who live in the Mountainous biome, because rocks suck. We 
add this to the filter:
```yaml
biome:
  NOR:
    - mountainous
```

The final filter looks like this:

```yaml
filter:
  biome:
    NOR:
      - mountainous
  cats:
    main:
      AND:
        rank: 
          - apprentice
    medicine:
      AND:
        rank:
          - medicine cat
        main_clan: true
    skeptic:
      AND:
        main_clan: true
      OR:
        trait:
          - cold
        rank:
          - medicine cat
          - medicine cat apprentice
```

Text: `{CAT/medicine} listens patiently as {CAT/main} describes {PRONOUN/main/poss} dream. "And then I saw {OMEN/sight/biome}!" {PRONOUN/main/subject/CAP} breathlessly {CONJU/main/continue/continues}. {CAT/skeptic} rolls {PRONOUN/skeptic/poss} eyes.`

Situation 1: 
- The main cat is Bugpaw, a NightClan warrior apprentice who uses they/them pronouns.
- `medicine` is Firepelt, a NightClan medicine cat who uses she/her pronouns.
- `skeptic` is Grayshell, a NightClan elder who has a cold personality and uses he/him pronouns.
- The NightClan camp is in the Beach biome.
-> `Firepelt listens patiently as Bugpaw describes their dream. "And then I saw a shell shining with the colors of the water!" They breathlessly continue. Grayshell rolls his eyes.`

Situation 2: 
- The main cat is Lionpaw, a DayClan mediator apprentice who uses she/her pronouns.
- `medicine` is Goldstreak, a DayClan medicine cat who uses she/her pronouns.
- `skeptic` is Breezepaw, a DayClan medicine cat apprentice who has an adventurous personality and uses they/them pronouns.
  - Note that whether Breezepaw's mentor is Goldstreak or another medicine cat doesn't matter.
- The DayClan camp is in the Plains biome.
-> `Goldstreak listens patiently as Lionpaw describes her dream. "And then I saw a single burnt stalk of grass!" She breathlessly continues. Breezepaw rolls their eyes.`

Situation 3: 
- The main cat is Moonpaw, a ThunderClan medicine cat apprentice who uses she/her pronouns.
- `medicine` is Alderheart, a ThunderClan medicine cat who uses he/him pronouns.
- `skeptic` is Jayfeather, a ThunderClan medicine cat who has a grumpy personality and uses he/him pronouns.
- The ThunderClan camp is in the Forest biome.
-> `Alderheart listens patiently as Moonpaw describes her dream. "And then I saw a perfect walnut!" She breathlessly continues. Jayfeather rolls his eyes.`

## TODO
- Add a condition where a random number is generated and one of several random options is chosen. E.g., for **Example 1**, have a way to select omens that use sight or hearing, and replace the word "saw" with "heard" depending on how it turns out.
- Allow nesting brackets
  - E.g. an omen where the main cat sees somthing happening to their Clan leader: `{OMEN/sight/{CLAN/main/leader}}` -> `Fireheart saw an omen of Bluestar's pawprints being washed away by a flood`
  - E.g. an omen where the main cat sees somthing happening to their mate: `{OMEN/sight/{CAT/main/rel.mate}}` -> `Leafstar saw an omen of Billystorm's pawprints being washed away by a flood`