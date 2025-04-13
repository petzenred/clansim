import random
from typing import Optional

import pygame
import pygame_gui

from definitions import *
from resources.audio.audio_directory import (MUSIC_PLAYLISTS, SOUND_INDEX)
from scripts.game_structure.game_essentials import game
import scripts.game_structure.ui_elements as ui_elements

import logging

logger = logging.getLogger(__name__)


class MusicManager:
    playlists: dict = MUSIC_PLAYLISTS
    current_playlist: list
    current_track: Optional[str]
    queued_track: Optional[str]

    number_of_tracks: int
    volume: float = game.settings["music_volume"] / 100

    muted_f: bool
    audio_disabled_f: bool

    def __init__(self):
        self.current_playlist = []
        self.number_of_tracks = len(self.current_playlist)
        self.muted_f = False
        self.audio_disabled_f = False
        self.current_track = None
        self.queued_track = None
        return

    def external_music_start(self):
        """ Plays the currently queued track then queues the next track.

        Visible to other modules.
        """
        if not self.queued_track:
            logger.warning("no track queued")
            return

        self._play_track(self.queued_track)
        self._queue_track()

    def check_music(self, screen: str):
        """ Checks if playlist currently playing is appropriate for the given screen, and changes the playlist if
        needed.
        Visible to other modules.
        :param screen: key for the current game screen
        """
        if self.muted_f or self.audio_disabled_f:
            return

        playable_biome: str = self._check_biome_playlist()
        logger.debug(f"playable_biome={playable_biome}")

        logger.debug(f"Screen = {screen}")

        if (    # main menu screens
                screen in MAIN_MENU_SCREENS
                and self.current_playlist != self.playlists[MAIN_MENU_SCREENS_KEY]
        ):
            new_playlist = self.playlists[MAIN_MENU_SCREENS_KEY]
        elif (  # clan creation screens
                screen in CREATION_SCREENS
                and self.current_playlist != self.playlists[CREATION_SCREENS_KEY]
        ):
            new_playlist = self.playlists[CREATION_SCREENS_KEY]
        # else:   # other screens
        elif (  # other screens
                screen not in MAIN_MENU_SCREENS
                and screen not in CREATION_SCREENS
        ):
            new_playlist = self.playlists[playable_biome]

        # Fade out current track and start playing the new one
        self._fade_out_music()
        self._load_playlist(new_playlist)

    def mute_music(self):
        """Pauses current music track.
        Visible to other modules.
        """
        self.muted_f = True
        if not self.audio_disabled_f:
            pygame.mixer.music.pause()

    def unmute_music(self, screen: str):
        """ Unpauses current music track, then double checks if the track is appropriate for the screen before changing
        if necessary.
        Visible to other modules.
        :param screen: key for the current game screen
        """
        if self.audio_disabled_f:
            try:
                pygame.mixer.init()
                sound_manager._load_sounds()
                self.audio_disabled_f = False
                self.muted_f = False
            except pygame.error:
                self.muted_f = True
                return False
        else:
            self.muted_f = False
        pygame.mixer.music.unpause()
        self.check_music(screen)
        return True

    def change_volume(self, new_volume: int):
        """ Changes the volume.
        Visible to other modules.
        :param new_volume: should be between 0 and 100
        """
        # make sure given volume is between 0 and 100
        if new_volume > 100:
            new_volume = 100
        if new_volume < 0:
            new_volume = 0

        # convert to a float and change volume accordingly
        self.volume = new_volume / 100
        game.settings["music_volume"] = new_volume
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(self.volume)

    def _fade_out_music(self, fadeout: int = 2000):
        """ Fades the music out.
        :param fadeout: fadeout length in milliseconds  | Default = 2
        """
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(fadeout)

    def _check_biome_playlist(self) -> str:
        """ Finds the active clan's biome and returns the appropriate playlist. """
        biome_playlist_key: str = BIOME_FOREST
        try:
            biome = game.clan.biome
            logger.debug(f"Current biome: {biome}")
            if biome in self.playlists:
                logger.debug(f"Found playlist for {biome} biome")
                if self.playlists[biome]:
                    biome_playlist_key = biome
                    logger.debug(f"Biome playlist for {biome} is {len(biome_playlist_key)} songs long")
            else:
                logger.debug(f"Could not find {biome} in playlists: {self.playlists.keys()}")
        except AttributeError:
            pass
        logger.debug(f"Queueing biome playlist: {biome_playlist_key}")
        return biome_playlist_key

    def _load_playlist(self, playlist: list[str]):
        """ Loads and plays random file from playlist, queues up next track
        set loops to -1 to loop the chosen file
        setting loops to number above zero will play the track that number of times before playing the queued track
        """
        self.current_playlist = playlist
        self.queued_track = None  # clear queue

        self.number_of_tracks = len(self.current_playlist)

        self._queue_track()

    def _queue_track(self):
        """ Queues up the next music track.

         The next track is chosen randomly from the current playlist but WILL NOT be the current track.
        """
        #  if playlist is empty or has a single track, don't attempt queueing
        if self.number_of_tracks == 0:
            return

        # otherwise we pick a new track and queue it
        if self.current_track and self.number_of_tracks > 1:
            playlist_copy = self.current_playlist.copy()
            logger.debug(f"Playlist: {playlist_copy}, removing track: {self.current_track}")
            playlist_copy.remove(self.current_track)  # don't want to repeat current track, so we take it out
            options = playlist_copy
            logger.debug(f"Final list: {options}")
        else:
            options = self.current_playlist

        try:
            self.queued_track = random.choice(options)
            logger.debug(f"Queueing music: current track is {self.current_track}, new track is {self.queued_track}")
        except IndexError:
            logger.warning("Playlist is empty")
            self.queued_track = None

    def _play_track(self, track, loops=0):
        """ Plays the given track and sets volume.

        set loops to -1 to loop the chosen file
        setting loops to number above zero will play the track that number of times before playing the queued track
        """
        self.current_track = track
        pygame.mixer.music.load(MUSIC_PATH + self.current_track)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(loops, fade_ms=1000)


music_manager = MusicManager()


class _SoundManager:
    volume: float = game.settings["sound_volume"] / 100

    def __init__(self):
        self.pressed = None
        logger.debug(f"UI Sounds volume: {self.volume}")

        self._load_sounds()

    def _load_sounds(self):
        logger.debug(f"_SoundManager._load_sounds")
        self.sounds = {}
        sound_data = SOUND_INDEX
        for sound in sound_data:
            try:
                self.sounds[sound] = []
                for path in sound_data[sound]:
                    self.sounds[sound].append(
                        pygame.mixer.Sound(SOUNDS_PATH + path)
                    )

                for each in self.sounds[sound]:
                    pygame.mixer.Sound.set_volume(each, self.volume)
            except:
                logger.exception("Failed to load sound")

    def handle_sound_events(self, sound_event: pygame.event):
        """
        assigns universal sound effects to event.type objects
        SHOULD NOT BE USED FOR INDIVIDUAL UNIQUE BUTTON SOUNDS
        UIImageButtons have a sound_id parameter for assigning unique sounds to individual buttons
        :param sound_event: the event that is taking place
        """
        if self.pressed == sound_event.ui_element:
            pass  # Don't play a sound from a button twice
        else:
            self.pressed = sound_event.ui_element

            # If hovering over the leader den decision to antagonize a different clan, play its unique sound on hover.
            if sound_event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
                if sound_event.ui_element.__class__ not in [ui_elements.CatButton, ui_elements.UISpriteButton]:
                    self._play_sound("button_hover")
                # if sound_event.ui_element.sound_id == "negative_interaction":

            if sound_event.type == pygame_gui.UI_BUTTON_START_PRESS:
                self._play_sound("button_press", sound_event.ui_element)

    def _play_sound(self, sound_key: str = None, button: ui_elements = None):
        """ Plays UI sounds.

        If a button is passed which has a sound_id, then that sound will be played.

        plays the given sound, if an ImageButton is passed through then the sound_id of the ImageButton will be
        used instead
        """
        if music_manager.muted_f or music_manager.audio_disabled_f:
            return

        if button and hasattr(button, "sound_id"):
            try:
                if button.sound_id is not None:
                    sound_key = button.sound_id
            except AttributeError:
                logger.exception(f"That ui_element has no sound_id.")

        try:
            random_sound = random.choice(self.sounds[sound_key])
            logger.debug(f"Playing sound: {sound_key}:{random_sound}")
            pygame.mixer.Sound.play(random_sound)
        except KeyError:
            logger.exception(f"Could not find sound {sound_key}")
        self.pressed = None

    def change_volume(self, new_volume: int):
        """ Changes the volume, int given should be between 0 and 100. """
        # make sure given volume is between 0 and 100
        if new_volume > 100:
            new_volume = 100
        if new_volume < 0:
            new_volume = 0

        # convert to a float and change volume accordingly
        self.volume = new_volume / 100
        game.settings["sound_volume"] = new_volume
        for sound in self.sounds:
            for each in self.sounds[sound]:
                pygame.mixer.Sound.set_volume(each, self.volume)


sound_manager = _SoundManager()
