# [ ] for screens
`scripts/_red/screens/[ ]`

- [ ] figure out why buttons aren't showing up

The ClanGen code refers to `bgs`/`backgrounds` and `screens`. Both seem to be `pygame.Surface` objects?
- [ ] differentiate between a Background, a Platform, a Screen, and a Surface
 - **Background**: what all other UI elements are layered on top of. There are three options: the main menu background, 
a Clan's camp, or a single solid colour (brown), the exact shade of which depends on if the game is in Light or Dark 
mode.
 - **Platform**: what a cat's sprite is set on top of in their profile screens.
 - **Screen**: TODO
 - **Surface**: TODO

- [ ] separate a *Screen* (`pygame.Screen`), 
- a *Page* (classes which inherit from 
      `scripts._red.pages.red_base_page.RedBaseScreen`), and 
- a *Surface*
  - **Screens**: objects which inherit from `pygame.Screen`
  - **Surface**: objects of the class `pygame.Surface`
  - **Page**: `scripts._red.pages.red_base_page.RedBaseScreen`
  - **Window**: objects whose class inherits from `pygame_gui.elements.UIWindow` or `pygame_gui.windows.UIMessageWindow`
- "MainSettings" -> "GameSettings"

- [ ] implement `ScreenManager` class
  - [x] add methods from `AllScreens` class at `scripts.screens/all_screens.py`
    - [ ] delete the original
  - [x] add methods from `scripts/game_structure/screen_settings.py`
    - [ ] delete the original
  - [x] add methods from `scripts/screens/screens_core/screens_core.py`
    - [ ] delete the original
  - [ ] set `active_clan_camp` and `active_clan_prefix` when the `game` object changes `active_clan_prefix`
- [ ] update popup windows (`scripts/game_structure/windows.py`)
  - [ ] `"cur_screen"`
- [ ] replace print() debugging statements with the logger
- when switching themes
  - I'm changing it so switching themes rebuilds `pygame.Surface` objects, instead of surfaces being built for 
all themes ahead of time and stored, when logically speaking once someone has picked light/dark mode they won't 
change it most playthroughs
  - [ ] `screen_manager.build_camp_bg_surfaces()`
  - [ ] make the loading screen run
- [x] update `scripts/ui/generate_box.py`
- [x] update `scripts/ui/generate_button.py`
- [x] update `scripts/ui/generate_screen_scale_json.py`
  - no changes needed
- [ ] update `scripts/ui/icon.py`
  - move the contents (a single `enum` class) to `definitions.py` and delete the file
- [x] update `scripts/ui/ui_elements.py`
- [x] update `scripts/ui/ui_manager.py`
  - no changes needed
- [ ] update screen classes
- [ ] replace strings with enums where possible
  - [ ] find all calls to `str.casefold()`
  - [ ] replace `scripts.cat.enums.CatAgeEnum` with an enum in `definitions`
    - [x] find and replace
    - [ ] not a StrEnum, but instead tuples of the age ranges?
- `Profile` screen
  - Buttons
    - Previous Cat
    - Next Cat
    - `Back` which takes the player to the `Camp`, `CatList`, or `Events` screen, depending
    - Inspection (magnifying glass icon)
      - Include customize cat button on the `InspectSprite` screen
  - Blurbs, top to bottom
    - Left side
      - gender
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
      - relations
        - subtabs: family tree, adoption, see relationships, choose mate
      - roles
        - subtabs: manage roles, change mentor
      - edits (used to be *personal*)
        - dropdown: change name, trans your gender, specify gender, cat toggles
      - personal (used to be *history*, which is now a subtab)
        - subtabs: history, skills, notes
          - **history** is the cat's timeline
          - **skills** lists the cat's skills and XP
          - [ ] use icons to differentiate between notes, history, and skills
          - [ ] differentiate between the open tab, the closed tabs, and hovering over a closed tab
          - can 
    - Bottom row: 
      - conditions
      - faith
      - accessories
        - base this off the `LifeGen-FullGen` accessories tab
      - dangerous
        - subtabs: exile cat, kill cat, destroy accessory
        - should be in the bottom right because there's nothing else there on the `Profile` screen you would click on
- [ ] update screen names in other scripts
  - [ ] `/scripts/game_structure/audio.py`

## Debugging

- [ ] training patrols aren't selectable
- [ ] ClanEventsScreen calls change_screen() twice
- [ ] ClanMembersScreen calls change_screen() twice
- [ ] MainMenuScreen calls queueing music twice
- [ ] change names for sub screens to match large screens
- [ ] remove the dens dropdown, since it's redundant with the `ClanCamp` screen
  - potentially keep it on Clan menu screens that aren't the `ClanCamp` screen, e.g. keep it on the `CatList` screen
- [ ] when using the back button from the `Profile` screen, you could want the `Events` screen, the `Camp` screen, or 
the `CatList` screen. bBut you can't use `screen_manager.last_screen_name` because if you go `Events` -> `Profile` 
-> `Relationships` -> `Profile`, then hit the back button, you want the `Events` page, not the Relationships page.
- [x] rename screens for clarity
  - [x] StartScreen -> MainMenuScreen
  - [x] SettingsScreen -> GameSettingsScreen
  - [x] MakeClanScreen -> NewClanScreen
  - SwitchClanScreen -> (unchanged)
  - [x] ClanScreen -> ClanCampScreen
  - [x] AllegiancesScreen -> ClanAllegiancesScreen
  - ClanSettingsScreen -> (unchanged)
  - [x] EventsScreen -> ClanEventsScreen
  - [x] ListScreen -> ClanMembersScreen
  - [x] PatrolScreen -> ClanPatrolScreen
  - ProfileScreen -> (unchanged)
  - [x] CeremonyScreen -> ProfileCeremonyScreen
  - [x] ChangeGenderScreen -> ProfileGenderScreen
  - [x] ChooseAdoptiveParentScreen -> ProfileAdoptScreen
  - [x] ChooseMateScreen -> ProfileMateScreen
  - [x] ChooseMentorScreen -> ProfileMentorScreen
  - [x] FamilyTreeScreen -> ProfileFamilyScreen
  - [x] RelationshipScreen -> ProfileRelationshipsScreen
  - [x] RoleScreen -> ProfileRoleScreen
  - [x] SpriteInspectScreen -> ProfileInspectScreen
  - [x] MediationScreen -> ProfileMediationScreen
  - [x] LeaderDenScreen -> DenLeaderScreen
  - [x] MedDenScreen -> DenHealerScreen
  - [x] WarriorDenScreen -> DenWarriorScreen
  - [x] ClearingScreen -> DenFreshkillScreen

## New features

- [ ] add the ability to choose from multiple accessories, like in LifeGen
- [ ] Add `faith` tab to the Profile screen.
  - [ ] get rid of skills blurb, and put it in its own tab too?
  - [ ] maybe put the skills and background + history in the same tab as the notes?
- `scripts.ui.ui_elements.UICatListDisplay` screen
  - [ ] switch to scrolling up and down instead of pages
