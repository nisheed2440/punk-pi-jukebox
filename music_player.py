"""
Music Player
Handles music playback using pygame
"""
import pygame
import logging
from typing import List, Optional, Callable
from music_library import Song

logger = logging.getLogger(__name__)


class MusicPlayer:
    """Manages music playback"""
    
    def __init__(self):
        """Initialize music player"""
        pygame.mixer.init()
        self.current_playlist: List[Song] = []
        self.current_index: int = -1
        self.is_playing: bool = False
        self.volume: float = 0.7
        self.on_song_change: Optional[Callable] = None
        
        pygame.mixer.music.set_volume(self.volume)
        
        # Set up end event
        self.SONG_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.SONG_END)
        
        logger.info("Music player initialized")
    
    def load_playlist(self, songs: List[Song]):
        """
        Load a new playlist
        
        Args:
            songs: List of Song objects to play
        """
        self.stop()
        self.current_playlist = songs
        self.current_index = -1
        logger.info(f"Loaded playlist with {len(songs)} songs")
    
    def play(self, index: int = 0):
        """
        Start playing from specified index
        
        Args:
            index: Index in playlist to start from (default: 0)
        """
        if not self.current_playlist:
            logger.warning("No playlist loaded")
            return
        
        if index < 0 or index >= len(self.current_playlist):
            logger.warning(f"Invalid playlist index: {index}")
            return
        
        self.current_index = index
        song = self.current_playlist[self.current_index]
        
        try:
            pygame.mixer.music.load(song.path)
            pygame.mixer.music.play()
            self.is_playing = True
            logger.info(f"Playing: {song.name}")
            
            if self.on_song_change:
                self.on_song_change(song, self.current_index)
        
        except Exception as e:
            logger.error(f"Error playing song {song.name}: {e}")
            # Try next song
            self.next()
    
    def pause(self):
        """Pause playback"""
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            logger.info("Playback paused")
    
    def unpause(self):
        """Resume playback"""
        if not self.is_playing and self.current_index >= 0:
            pygame.mixer.music.unpause()
            self.is_playing = True
            logger.info("Playback resumed")
    
    def stop(self):
        """Stop playback"""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.current_index = -1
        logger.info("Playback stopped")
    
    def next(self):
        """Play next song in playlist"""
        if not self.current_playlist:
            return
        
        next_index = self.current_index + 1
        
        if next_index >= len(self.current_playlist):
            # Loop back to start
            next_index = 0
        
        self.play(next_index)
    
    def previous(self):
        """Play previous song in playlist"""
        if not self.current_playlist:
            return
        
        prev_index = self.current_index - 1
        
        if prev_index < 0:
            # Loop to end
            prev_index = len(self.current_playlist) - 1
        
        self.play(prev_index)
    
    def set_volume(self, volume: float):
        """
        Set playback volume
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
        logger.info(f"Volume set to {self.volume}")
    
    def get_current_song(self) -> Optional[Song]:
        """Get currently playing song"""
        if 0 <= self.current_index < len(self.current_playlist):
            return self.current_playlist[self.current_index]
        return None
    
    def handle_song_end(self):
        """Handle end of song event - automatically play next"""
        if self.is_playing:
            logger.info("Song ended, playing next")
            self.next()

