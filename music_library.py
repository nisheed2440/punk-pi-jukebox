"""
Music Library Manager
Scans and organizes music files based on folder structure
"""
import os
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Song:
    """Represents a song"""
    path: str
    filename: str
    seq_no: int
    name: str


@dataclass
class Album:
    """Represents an album"""
    path: str
    seq_no: int
    name: str
    songs: List[Song]
    album_art: Optional[str] = None


@dataclass
class Artist:
    """Represents an artist"""
    path: str
    seq_no: int
    name: str
    albums: List[Album]


@dataclass
class Playlist:
    """Represents a playlist (NFC ID mapping)"""
    nfc_id: str
    path: str
    artists: List[Artist]


class MusicLibrary:
    """Manages music library and playlist organization"""
    
    def __init__(self, library_path="music"):
        """
        Initialize music library
        
        Args:
            library_path: Root path to music library
        """
        self.library_path = library_path
        self.playlists: Dict[str, Playlist] = {}
        
        # Create music directory if it doesn't exist
        if not os.path.exists(library_path):
            os.makedirs(library_path)
            logger.info(f"Created music library directory: {library_path}")
    
    def scan_library(self):
        """Scan music library and build playlist index"""
        self.playlists = {}
        
        if not os.path.exists(self.library_path):
            logger.warning(f"Music library path does not exist: {self.library_path}")
            return
        
        # Scan for NFC ID directories
        try:
            for nfc_id in os.listdir(self.library_path):
                nfc_path = os.path.join(self.library_path, nfc_id)
                
                if not os.path.isdir(nfc_path):
                    continue
                
                playlist = self._scan_playlist(nfc_id, nfc_path)
                if playlist:
                    self.playlists[nfc_id] = playlist
                    logger.info(f"Loaded playlist for NFC ID: {nfc_id}")
        
        except Exception as e:
            logger.error(f"Error scanning music library: {e}")
        
        logger.info(f"Music library scan complete. Found {len(self.playlists)} playlists")
    
    def _scan_playlist(self, nfc_id: str, path: str) -> Optional[Playlist]:
        """Scan a playlist directory"""
        artists = []
        
        try:
            for artist_dir in sorted(os.listdir(path)):
                artist_path = os.path.join(path, artist_dir)
                
                if not os.path.isdir(artist_path):
                    continue
                
                artist = self._scan_artist(artist_dir, artist_path)
                if artist:
                    artists.append(artist)
        
        except Exception as e:
            logger.error(f"Error scanning playlist {nfc_id}: {e}")
            return None
        
        if artists:
            return Playlist(nfc_id=nfc_id, path=path, artists=artists)
        return None
    
    def _scan_artist(self, dirname: str, path: str) -> Optional[Artist]:
        """Scan an artist directory"""
        # Parse directory name: <seq_no>_<artist_name>
        try:
            parts = dirname.split('_', 1)
            if len(parts) != 2:
                logger.warning(f"Invalid artist directory name: {dirname}")
                return None
            
            seq_no = int(parts[0])
            name = parts[1].replace('_', ' ').title()
        except ValueError:
            logger.warning(f"Invalid artist directory name: {dirname}")
            return None
        
        albums = []
        
        try:
            for album_dir in sorted(os.listdir(path)):
                album_path = os.path.join(path, album_dir)
                
                if not os.path.isdir(album_path):
                    continue
                
                album = self._scan_album(album_dir, album_path)
                if album:
                    albums.append(album)
        
        except Exception as e:
            logger.error(f"Error scanning artist {dirname}: {e}")
            return None
        
        if albums:
            return Artist(path=path, seq_no=seq_no, name=name, albums=albums)
        return None
    
    def _scan_album(self, dirname: str, path: str) -> Optional[Album]:
        """Scan an album directory"""
        # Parse directory name: <seq_no>_<album_name>
        try:
            parts = dirname.split('_', 1)
            if len(parts) != 2:
                logger.warning(f"Invalid album directory name: {dirname}")
                return None
            
            seq_no = int(parts[0])
            name = parts[1].replace('_', ' ').title()
        except ValueError:
            logger.warning(f"Invalid album directory name: {dirname}")
            return None
        
        songs = []
        album_art = None
        
        # Look for album art
        album_art_path = os.path.join(path, "albumart.png")
        if os.path.exists(album_art_path):
            album_art = album_art_path
        
        try:
            for filename in sorted(os.listdir(path)):
                file_path = os.path.join(path, filename)
                
                if not os.path.isfile(file_path):
                    continue
                
                # Check if it's a music file
                if not filename.lower().endswith(('.mp3', '.wav', '.ogg', '.flac', '.m4a')):
                    continue
                
                song = self._parse_song(filename, file_path)
                if song:
                    songs.append(song)
        
        except Exception as e:
            logger.error(f"Error scanning album {dirname}: {e}")
            return None
        
        if songs:
            return Album(
                path=path,
                seq_no=seq_no,
                name=name,
                songs=songs,
                album_art=album_art
            )
        return None
    
    def _parse_song(self, filename: str, path: str) -> Optional[Song]:
        """Parse a song file"""
        # Parse filename: <seq_no>_<song_name>.ext
        try:
            name_without_ext = os.path.splitext(filename)[0]
            parts = name_without_ext.split('_', 1)
            
            if len(parts) != 2:
                logger.warning(f"Invalid song filename: {filename}")
                return None
            
            seq_no = int(parts[0])
            name = parts[1].replace('_', ' ').title()
            
            return Song(path=path, filename=filename, seq_no=seq_no, name=name)
        
        except ValueError:
            logger.warning(f"Invalid song filename: {filename}")
            return None
    
    def get_playlist(self, nfc_id: str) -> Optional[Playlist]:
        """Get playlist by NFC ID"""
        return self.playlists.get(nfc_id)
    
    def get_all_songs(self, nfc_id: str) -> List[Song]:
        """Get all songs in a playlist in order"""
        playlist = self.get_playlist(nfc_id)
        if not playlist:
            return []
        
        all_songs = []
        for artist in sorted(playlist.artists, key=lambda a: a.seq_no):
            for album in sorted(artist.albums, key=lambda a: a.seq_no):
                for song in sorted(album.songs, key=lambda s: s.seq_no):
                    all_songs.append(song)
        
        return all_songs
    
    def get_song_info(self, song: Song, playlist: Playlist) -> dict:
        """Get detailed information about a song including artist and album"""
        for artist in playlist.artists:
            for album in artist.albums:
                if song in album.songs:
                    return {
                        'song': song.name,
                        'artist': artist.name,
                        'album': album.name,
                        'album_art': album.album_art
                    }
        return {
            'song': song.name,
            'artist': 'Unknown',
            'album': 'Unknown',
            'album_art': None
        }

