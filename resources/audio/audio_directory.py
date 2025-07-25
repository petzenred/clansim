# audio_directory.py - An index of what sound/music should play when.

from definitions import *

__all__ = ['MUSIC_PLAYLISTS', 'SOUND_INDEX']

MUSIC_PLAYLISTS: dict = {
    MAIN_MENU_SCREENS_KEY: ["Forest_Ambiance_1.mp3"],
    CREATION_SCREENS_KEY: ["Clangen_Generations_441khz.mp3"],
    Biome.Beach: ["Beach_Ambiance_1.mp3", "Beach_Ambiance_2.mp3"],
    Biome.Desert: ["Desert_Ambiance_1.mp3"],
    Biome.Forest: ["Forest_Ambiance_1.mp3"],
    Biome.Mountain: ["Mountain_Ambiance_1.mp3", "Mountain_Ambiance_2.mp3"],
    Biome.Plains: ["Plains_Ambiance_1.mp3", "Plains_Ambiance_2.mp3"],
    Biome.Wetlands: ["Wetlands_Ambiance_1.mp3"],
    Biome.Twolegplace: [],
}

SOUND_INDEX: dict = {
    "button_press": ["Button_Click_4.mp3"],
    "button_hover": ["Button_Hover_3.mp3"],
    "page_flip": ["Page_Flip_1.mp3","Page_Flip_2.mp3","Page_Flip_3.mp3","Page_Flip_4.mp3","Page_Flip_5.mp3"],
    "dice_roll": ["Dice_Roll_1.mp3","Dice_Roll_2.mp3","Dice_Roll_3.mp3","Dice_Roll_4.mp3",
                  "Dice_Roll_5.mp3","Dice_Roll_6.mp3","Dice_Roll_7.mp3"],
    "save": ["Save_Button.mp3"],
    "timeskip": ["Timeskip_Button.mp3"],
    "antagonize": ["Antagonize_Button.mp3"]
}