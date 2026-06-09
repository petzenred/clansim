# settings.py - Comprised on the original 'clansettings.json' and 'gamesettings.json'.

"""
    WARNING: This file is NOT where settings are stored. You're looking for '`'settings.txt'`' in the saves folder.
        Edit this file if you want to change your settings instead.

    It's where the text used to display the settings in the game are stored.
"""

CLAN_SETTINGS: dict = {
    ".": [
        "WARNING: This file is NOT where your settings are stored.",
        "This file is only used to display the settings in the game.",
        "The file you are looking for is 'settings.txt' in your saves folder.",
        "If you want to change your settings, edit that file instead.",
        "FORMAT:",
        {
            "group": {
                "setting name": [
                    "display name",
                    "tooltip",
                    "default",
                    [
                        "nested setting",
                        "enabled value"
                    ]
                ]
            }
        }
    ],
    "general": {
        "autosave": [
            "Automatically save every five moons",
            "Automatically save every five moons.",
            False
        ],
        "disasters": [
            "Allow mass extinction events",
            "This may result in up to 1/3rd of your Clan dying in one moon.",
            False
        ],
        "showxp": [
            "Show exact XP and nutrition status",
            "Will turn 'experience: proficient' into 'experience: proficient (151)'; and 'nutrition: full' into 'nutrition: full (70)'.",
            False
        ],
        "random med cat": [
            "Allow medicine cats to be randomly selected on patrol",
            "Medicine cats can be selected with the patrol buttons +1, +3,+6.",
            True
        ],
        "fading": [
            "Allow dead cats to fade away",
            "After 202 moons, dead cats will be unloaded, and saved separately. No family relations will be lost.",
            True
        ],
        "save_faded_copy": [
            "Save a complete copy of faded cats information",
            "A complete copy of faded cat save info will be saved in plain-text.",
            False
        ],
        "backgrounds": [
            "Enable Clan page background",
            "Even with this off, the camp you choose will still affect the events you encounter.",
            True
        ],
        "moons and seasons": [
            "Show moons and seasons widget",
            "Displays Clan age and current Clan season on several screens.",
            False
        ]
    },
    "role": {
        "deputy": [
            "Allow leaders to automatically choose a new deputy",
            "The Warrior Code rules will be taken into account when choosing a deputy.",
            False
        ],
        "12_moon_graduation": [
            "Disable experience-based apprentice graduation",
            "All apprentices will graduate at 12 moons.",
            False
        ],
        "retirement": [
            "Cats will never retire due to a permanent condition",
            "When this setting is off, cats with permanent conditions will choose whether or not they want to retire.",
            False
        ],
        "become_mediator": [
            "Allow warriors and elders to choose to become mediators",
            "Warriors and elders will have a chance to become mediators upon timeskip.",
            False
        ]
    },
    "relation": {
        "affair": [
            "Allow cats to breed with cats that aren't their mates",
            "This will allow mated and unmated cats to have kits with other cats they are not mated with. This includes, but is not limited to, affairs/cheating.",
            False
        ],
        "same sex birth": [
            "Pregnancy ignores biology",
            "Allow all cats to get pregnant despite their gender and all couples to birth kittens despite same-sex status.",
            False
        ],
        "same sex adoption": [
            "Increase same-sex adoption",
            "If same-sex birth is disabled, this option greatly increases the chances of same-sex couples adopting.",
            True,
            [
                "same sex birth",
                False
            ]
        ],
        "single parentage": [
            "Allow cats to have kittens with an unknown second parent",
            "Allow cats to have kittens with an unknown second biological parent. The cat will be listed as the only biological parent.",
            False
        ],
        "romantic with former mentor": [
            "Allow romantic interactions with former mentors",
            "Allows mentors and the cats they trained to be romantic after they become warriors.",
            True
        ],
        "first cousin mates": [
            "Allow first cousins to be mates and have romantic interactions",
            "Allows cats with the same grandparents but different parents to become mates.",
            False
        ]
    },
    "freshkill_tactics":{
        "by-status":[
            "by-status",
            "The Clan will be fed according their status and within the status by age.",
            True
        ],
        "younger first":[
            "younger first",
            "The Clan will be fed according to their age only.",
            False
        ],
        "less nutrition first":[
            "less nutrition first",
            "First the cats with the lowest nutrition will be fed, afterwards the Clan will be fed according to their status.",
            False
        ],
        "hunter first":[
            "hunter first",
            "Firstly the cats with a hunter skill will be fed, afterwards the Clan will be fed according to their status.",
            False
        ],
        "sick/injured first":[
            "sick/injured first",
            "Firstly the sick and injured cats will be fed, afterwards the Clan will be fed according to their status.",
            False
        ],
        "more experience first":[
            "high EXP first",
            "The Clan will be fed according their experience, highest one first.",
            False
        ],
        "ration prey":[
            "ration prey",
            "Healthy warriors will only eat half of the food they need, even if there is enough for the Clan.",
            False
        ]
    },
    "clan_focus":{
        "business as usual":[
            "Business As Usual",
            "The Clan has no specific focus and won't get any bonuses.",
            True,
            "usual_focus",
            "#usual_focus_button"
        ],
        "hunting":[
            "Feeding the Clan",
            "The Clan will focus on hunting, each working warrior (including deputy and leader) and each working apprentice will gather additional prey on each moonskip.",
            False,
            "hunting_focus",
            "#hunting_focus_button"
        ],
        "herb gathering":[
            "Assisting with Herb Gathering",
            "The Clan will focus on herb gathering, each medicine cat and medicine cat apprentice will gather additional herbs on each moonskip due to extra help from the warriors.",
            False,
            "herb_focus",
            "#herb_focus_button"
        ],
        "threaten outsiders": [
            "Threatening Outsiders",
            "The relationship with cats outside of the Clan decreases due to intentionally threatening behavior from your warriors.",
            False,
            "threaten_focus",
            "#threaten_focus_button"
        ],
        "seek outsiders": [
            "Entreating with Outsiders",
            "The relationship with cats outside of the Clan increases as your warriors make efforts to sow seeds of friendship.",
            False,
            "entreat_focus",
            "#entreat_focus_button"
        ],
        "rest and recover":[
            "Resting and Recovering",
            "The Clan will take more care and time in their tasks and therefore the rate of injuries, illnesses and outbreaks will be reduced.",
            False,
            "rest_focus",
            "#rest_focus_button"
        ],
        "sabotage other clans": [
            "Sabotaging Other Clans",
            "Your mediators and warriors work together to undermine the other Clans. Only available if you have a working mediator. Selecting this will also allow you to choose which Clans you target.",
            False,
            "sabotage_focus",
            "#sabotage_focus_button"
        ],
        "aid other clans": [
            "Helping Other Clans",
            "Your mediator and warriors work together to help the other Clans with whatever they need. Only available if you have a working mediator. Selecting this will also allow you to choose which Clans you target.",
            False,
            "help_focus",
            "#help_focus_button"
        ],
        "raid other clans": [
            "Raiding Other Clans",
            "Your warriors begin crossing borders for resources. Prey and herbs will greatly increase each moonskip, but injuries and illnesses will increase and the relationship with other Clans decrease. You will be able to choose which Clans you target.",
            False,
            "raid_focus",
            "#raid_focus_button"
        ],
        "hoarding":[
            "Hoarding Resources",
            "Your warriors begin stockpiling as many resources as they can get their paws on, regardless of their own safety. Prey and herbs will increase each moonskip, but injuries and illnesses will also increase.",
            False,
            "hoard_focus",
            "#hoard_focus_button"
        ]
    },
    "..": "these are special. they do not have a display name or a tooltip",
    "__other": {
        "show dead relation": [
            False,
            True
        ],
        "show empty relation": [
            False,
            True
        ],
        "favourite sub tab": [
            None,
            "life events",
            "user notes"
        ],
        "den labels": [
            True,
            False
        ],
        "show fav": [
            False,
            True
        ]
    }
}


GAME_SETTINGS: dict = {
    ".": [
        "WARNING: This file is NOT where your settings are stored.",
        "This file is only used to display the settings in the game.",
        "The file you are looking for is 'settings.json' in your saves folder.",
        "If you want to change your settings, edit that file instead.",
        "FORMAT:",
        {
            "group": {
                "setting name": [
                    "display name",
                    "tooltip",
                    "default"
                ]
            }
        }
    ],
    "general": {
        "dark mode": [
            "Dark mode",
            "Camp backgrounds will match with the mode: nighttime for dark mode and daytime for light mode.",
            False
        ],
        "fullscreen scaling": [
            "Ignore fullscreen scaling rules",
            "If enabled, fullscreen will display as large as possible (toggle fullscreen to update). This may include visual artifacts.",
            False
        ],
        "no sprite antialiasing": [
            "Disable sprite antialiasing",
            "If enabled, sprites and patrol art will no longer be antialiased (\"blurry\"/\"smooth\") when in fullscreen.",
            False
        ],
        "custom cursor": [
            "Custom cursor",
            "The cursor will be replaced with a cat paw. The cursor is currently unfinished and is prone to crashing.",
            False
        ],
        "keybinds": [
            "Keybinds",
            "Enables certain keybinds to be used throughout the menus for quick navigation.",
            False
        ],
        "shaders": [
            "Enable Shaders",
            "This will add a shading layer onto the cat sprites.",
            False
        ],
        "gore": [
            "Allow mild gore and blood in patrol artwork",
            "Mild gore and blood will be allowed in the artwork displayed alongside patrols.",
            False
        ],
        "discord": [
            "Enable Discord integration",
            "Discord will show info about your Clan, including your Clan name",
            False
        ],
        "check_for_updates": [
            "Check for updates",
            "Automatically checks for updates on startup",
            True
        ],
        "show_changelog": [
            "Display changelog on startup",
            "Shows the changelog of the latest release on startup",
            True
        ],
        "special_dates": [
            "Allow special date events",
            "Certain changes may be made to the game on special days such as April Fools",
            True
        ],
        "random relation": [
            "Randomize relationship values when creating Clan",
            "Clan founder cats will start the game with established relationships.",
            True
        ],
        "they them default": [
            "Use they/them as default pronouns",
            "If this setting is on new cats will generate with they/them pronouns, regardless of gender.",
            False
        ]
    },
    "..": "these are special. they do not have a display name or a tooltip",
    "__other": {
        "language": [
            "en",
            "es",
            "de"
        ],
        "text size": [
            "0",
            "1",
            "2"
        ],
        "fullscreen": [
            False,
            True
        ],
        "music_volume": [
            100
        ],
        "sound_volume": [
            100
        ],
        "audio_mute": [
            False,
            True
        ]
    }
}
