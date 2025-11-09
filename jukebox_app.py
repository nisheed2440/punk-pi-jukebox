"""
Jukebox App - Main Application
Tkinter-based GUI for Raspberry Pi jukebox with NFC support
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pygame
import logging
import os
import threading
from typing import Optional

# Try to import PIL/Pillow, fall back to pygame for image loading
try:
    from PIL import Image, ImageTk
    PILLOW_AVAILABLE = True
    logger = logging.getLogger(__name__)
    logger.info("Using PIL/Pillow for image processing")
except ImportError:
    PILLOW_AVAILABLE = False
    Image = None
    ImageTk = None
    logger = logging.getLogger(__name__)
    logger.warning("PIL/Pillow not available, using pygame for images")

from rfid_reader import RFIDReader
from music_library import MusicLibrary, Song
from music_player import MusicPlayer
from config_manager import ConfigManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class JukeboxApp:
    """Main Jukebox Application"""
    
    def __init__(self, root, mock_rfid=False):
        """
        Initialize jukebox app
        
        Args:
            root: Tkinter root window
            mock_rfid: Use mock RFID reader for testing
        """
        self.root = root
        self.root.title("Jukebox")
        self.root.geometry("720x720")
        self.root.configure(bg='black')
        
        # Make fullscreen (comment out for testing)
        # self.root.attributes('-fullscreen', True)
        
        # Initialize components
        self.config = ConfigManager()
        self.rfid_reader = RFIDReader(mock_mode=mock_rfid)
        self.music_library = MusicLibrary(self.config.get_music_library_path())
        self.music_player = MusicPlayer()
        
        # Set up music player callback
        self.music_player.on_song_change = self.on_song_change
        
        # State
        self.current_playlist = None
        self.debug_mode = False
        self.rfid_read_mode = False
        self.stop_nfc_config_mode = False
        
        # UI components
        self.album_art_label = None
        self.info_frame = None
        self.song_label = None
        self.artist_label = None
        self.album_label = None
        self.debug_button = None
        self.debug_window = None
        
        # Load fallback image
        self.fallback_image = None
        self.load_fallback_image()
        
        # Build UI
        self.build_ui()
        
        # Scan music library
        self.music_library.scan_library()
        
        # Start RFID polling
        self.poll_rfid()
        
        # Start pygame event loop
        self.check_pygame_events()
        
        logger.info("Jukebox app initialized")
    
    def load_fallback_image(self):
        """Load or create fallback album art"""
        fallback_path = "fallback_albumart.png"
        
        if PILLOW_AVAILABLE:
            # Use PIL/Pillow if available
            if os.path.exists(fallback_path):
                try:
                    self.fallback_image = Image.open(fallback_path)
                    logger.info("Loaded fallback album art")
                    return
                except Exception as e:
                    logger.error(f"Error loading fallback image: {e}")
            
            # Create a simple fallback image
            try:
                img = Image.new('RGB', (400, 400), color='#1a1a1a')
                img.save(fallback_path)
                self.fallback_image = img
                logger.info("Created fallback album art")
            except Exception as e:
                logger.error(f"Error creating fallback image: {e}")
        else:
            # Use pygame to create fallback
            try:
                if os.path.exists(fallback_path):
                    # Try to load with pygame
                    pygame_img = pygame.image.load(fallback_path)
                    self.fallback_image = pygame_img
                    logger.info("Loaded fallback album art (pygame)")
                else:
                    # Create with pygame
                    surface = pygame.Surface((400, 400))
                    surface.fill((26, 26, 26))
                    pygame.image.save(surface, fallback_path)
                    self.fallback_image = surface
                    logger.info("Created fallback album art (pygame)")
            except Exception as e:
                logger.error(f"Error with fallback image: {e}")
                self.fallback_image = None
    
    def build_ui(self):
        """Build main UI"""
        # Main container
        main_frame = tk.Frame(self.root, bg='black')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Album art display
        self.album_art_label = tk.Label(main_frame, bg='black')
        self.album_art_label.pack(fill=tk.BOTH, expand=True)
        
        # Info overlay frame (on top of album art)
        self.info_frame = tk.Frame(main_frame, bg='black', bd=0)
        self.info_frame.place(relx=0.5, rely=0.85, anchor='center')
        
        # Song info labels
        self.song_label = tk.Label(
            self.info_frame,
            text="",
            font=('Helvetica', 24, 'bold'),
            fg='white',
            bg='black'
        )
        self.song_label.pack()
        
        self.artist_label = tk.Label(
            self.info_frame,
            text="",
            font=('Helvetica', 18),
            fg='#cccccc',
            bg='black'
        )
        self.artist_label.pack()
        
        self.album_label = tk.Label(
            self.info_frame,
            text="",
            font=('Helvetica', 16),
            fg='#999999',
            bg='black'
        )
        self.album_label.pack()
        
        # Debug button (small icon in corner)
        self.debug_button = tk.Button(
            self.root,
            text="⚙",
            font=('Helvetica', 16),
            command=self.toggle_debug_window,
            bg='#333333',
            fg='white',
            bd=0,
            width=3,
            height=1
        )
        self.debug_button.place(x=10, y=10)
        
        # Show fallback image initially
        self.display_album_art(None)
    
    def toggle_debug_window(self):
        """Toggle debug window"""
        if self.debug_window and self.debug_window.winfo_exists():
            self.debug_window.destroy()
            self.debug_window = None
        else:
            self.show_debug_window()
    
    def show_debug_window(self):
        """Show debug configuration window"""
        self.debug_window = tk.Toplevel(self.root)
        self.debug_window.title("Debug Menu")
        self.debug_window.geometry("400x500")
        self.debug_window.configure(bg='#2a2a2a')
        
        # Title
        title_label = tk.Label(
            self.debug_window,
            text="Debug Menu",
            font=('Helvetica', 20, 'bold'),
            fg='white',
            bg='#2a2a2a'
        )
        title_label.pack(pady=20)
        
        # RFID Read Mode button
        read_rfid_btn = tk.Button(
            self.debug_window,
            text="Read NFC Mode" if not self.rfid_read_mode else "Stop Read Mode",
            font=('Helvetica', 14),
            command=self.toggle_rfid_read_mode,
            bg='#4CAF50' if not self.rfid_read_mode else '#f44336',
            fg='white',
            width=20,
            height=2
        )
        read_rfid_btn.pack(pady=10)
        
        # RFID display
        self.rfid_display = tk.Label(
            self.debug_window,
            text="Waiting for NFC...",
            font=('Helvetica', 12),
            fg='yellow',
            bg='#2a2a2a',
            wraplength=350
        )
        self.rfid_display.pack(pady=10)
        
        # Configure Stop NFC button
        stop_nfc_btn = tk.Button(
            self.debug_window,
            text="Configure Stop NFC",
            font=('Helvetica', 14),
            command=self.configure_stop_nfc,
            bg='#ff9800',
            fg='white',
            width=20,
            height=2
        )
        stop_nfc_btn.pack(pady=10)
        
        # Current stop NFC display
        stop_nfc_text = f"Stop NFC ID: {self.config.get('stop_nfc_id', 'Not set')}"
        stop_nfc_label = tk.Label(
            self.debug_window,
            text=stop_nfc_text,
            font=('Helvetica', 10),
            fg='white',
            bg='#2a2a2a'
        )
        stop_nfc_label.pack(pady=5)
        
        # Music library path
        tk.Label(
            self.debug_window,
            text="Music Library Path:",
            font=('Helvetica', 12),
            fg='white',
            bg='#2a2a2a'
        ).pack(pady=(20, 5))
        
        path_frame = tk.Frame(self.debug_window, bg='#2a2a2a')
        path_frame.pack(pady=5)
        
        self.path_entry = tk.Entry(path_frame, width=25, font=('Helvetica', 10))
        self.path_entry.insert(0, self.config.get_music_library_path())
        self.path_entry.pack(side=tk.LEFT, padx=5)
        
        browse_btn = tk.Button(
            path_frame,
            text="Browse",
            command=self.browse_music_path,
            bg='#555',
            fg='white'
        )
        browse_btn.pack(side=tk.LEFT)
        
        # Rescan library button
        rescan_btn = tk.Button(
            self.debug_window,
            text="Rescan Music Library",
            font=('Helvetica', 12),
            command=self.rescan_library,
            bg='#2196F3',
            fg='white',
            width=20
        )
        rescan_btn.pack(pady=10)
        
        # Save button
        save_btn = tk.Button(
            self.debug_window,
            text="Save Configuration",
            font=('Helvetica', 14, 'bold'),
            command=self.save_configuration,
            bg='#4CAF50',
            fg='white',
            width=20,
            height=2
        )
        save_btn.pack(pady=20)
        
        # Close button
        close_btn = tk.Button(
            self.debug_window,
            text="Close",
            font=('Helvetica', 12),
            command=self.debug_window.destroy,
            bg='#666',
            fg='white',
            width=20
        )
        close_btn.pack(pady=10)
    
    def toggle_rfid_read_mode(self):
        """Toggle RFID read mode"""
        self.rfid_read_mode = not self.rfid_read_mode
        
        if self.rfid_read_mode:
            # Stop music if playing
            self.music_player.stop()
            self.update_display("", "", "")
            logger.info("Entered RFID read mode")
        else:
            if self.debug_window and self.debug_window.winfo_exists():
                self.rfid_display.config(text="Waiting for NFC...")
            logger.info("Exited RFID read mode")
        
        # Update button text if debug window is open
        if self.debug_window and self.debug_window.winfo_exists():
            for widget in self.debug_window.winfo_children():
                if isinstance(widget, tk.Button) and "Read" in widget.cget("text"):
                    widget.config(
                        text="Stop Read Mode" if self.rfid_read_mode else "Read NFC Mode",
                        bg='#f44336' if self.rfid_read_mode else '#4CAF50'
                    )
    
    def configure_stop_nfc(self):
        """Configure stop NFC ID"""
        self.stop_nfc_config_mode = True
        self.music_player.stop()
        
        messagebox.showinfo(
            "Configure Stop NFC",
            "Tap the NFC tag you want to use as the stop command."
        )
        
        logger.info("Waiting for stop NFC configuration...")
    
    def browse_music_path(self):
        """Browse for music library path"""
        path = filedialog.askdirectory(
            title="Select Music Library Folder",
            initialdir=self.config.get_music_library_path()
        )
        
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)
    
    def rescan_library(self):
        """Rescan music library"""
        logger.info("Rescanning music library...")
        self.music_library.scan_library()
        messagebox.showinfo("Library Scan", f"Found {len(self.music_library.playlists)} playlists")
    
    def save_configuration(self):
        """Save configuration"""
        # Update music library path
        new_path = self.path_entry.get()
        if new_path != self.config.get_music_library_path():
            self.config.set_music_library_path(new_path)
            self.music_library.library_path = new_path
            self.rescan_library()
        
        # Save config
        if self.config.save():
            messagebox.showinfo("Success", "Configuration saved successfully!")
        else:
            messagebox.showerror("Error", "Failed to save configuration")
    
    def poll_rfid(self):
        """Poll RFID reader for new tags"""
        def read_rfid():
            nfc_id = self.rfid_reader.read_id()
            
            if nfc_id:
                self.root.after(0, lambda: self.handle_nfc_tag(nfc_id))
        
        # Run in separate thread to avoid blocking UI
        thread = threading.Thread(target=read_rfid, daemon=True)
        thread.start()
        
        # Poll every 500ms
        self.root.after(500, self.poll_rfid)
    
    def handle_nfc_tag(self, nfc_id: str):
        """Handle NFC tag detection"""
        logger.info(f"NFC tag detected: {nfc_id}")
        
        # If in stop NFC config mode
        if self.stop_nfc_config_mode:
            self.config.set_stop_nfc_id(nfc_id)
            self.stop_nfc_config_mode = False
            messagebox.showinfo(
                "Stop NFC Configured",
                f"Stop NFC ID set to: {nfc_id}"
            )
            return
        
        # If in RFID read mode
        if self.rfid_read_mode:
            if self.debug_window and self.debug_window.winfo_exists():
                self.rfid_display.config(text=f"NFC ID: {nfc_id}")
            return
        
        # Check if it's the stop command
        if self.config.is_stop_nfc(nfc_id):
            logger.info("Stop NFC detected")
            self.music_player.stop()
            self.update_display("Music Stopped", "", "")
            self.display_album_art(None)
            return
        
        # Load and play playlist
        playlist = self.music_library.get_playlist(nfc_id)
        
        if playlist:
            logger.info(f"Loading playlist for NFC ID: {nfc_id}")
            songs = self.music_library.get_all_songs(nfc_id)
            
            if songs:
                self.current_playlist = playlist
                self.music_player.load_playlist(songs)
                self.music_player.play(0)
            else:
                logger.warning(f"No songs found in playlist: {nfc_id}")
                self.update_display("No Songs Found", "", "")
        else:
            logger.warning(f"No playlist found for NFC ID: {nfc_id}")
            self.update_display("Unknown NFC Tag", f"ID: {nfc_id}", "")
    
    def on_song_change(self, song: Song, index: int):
        """Callback when song changes"""
        if not self.current_playlist:
            return
        
        # Get song info
        info = self.music_library.get_song_info(song, self.current_playlist)
        
        # Update display
        self.update_display(
            info['song'],
            info['artist'],
            info['album']
        )
        
        # Update album art
        self.display_album_art(info['album_art'])
        
        logger.info(f"Now playing: {info['artist']} - {info['song']}")
    
    def update_display(self, song: str, artist: str, album: str):
        """Update song info display"""
        self.song_label.config(text=song)
        self.artist_label.config(text=artist)
        self.album_label.config(text=album)
    
    def display_album_art(self, image_path: Optional[str]):
        """Display album art"""
        try:
            if PILLOW_AVAILABLE:
                # Use PIL/Pillow method
                if image_path and os.path.exists(image_path):
                    img = Image.open(image_path)
                else:
                    img = self.fallback_image
                
                if img:
                    # Resize to fit window while maintaining aspect ratio
                    img.thumbnail((720, 720), Image.Resampling.LANCZOS)
                    
                    # Convert to PhotoImage
                    photo = ImageTk.PhotoImage(img)
                    
                    # Update label
                    self.album_art_label.config(image=photo)
                    self.album_art_label.image = photo  # Keep a reference
            else:
                # Use pygame method
                if image_path and os.path.exists(image_path):
                    try:
                        pygame_img = pygame.image.load(image_path)
                    except:
                        pygame_img = self.fallback_image
                else:
                    pygame_img = self.fallback_image
                
                if pygame_img:
                    # Scale pygame surface to fit window
                    size = pygame_img.get_size()
                    scale_factor = min(720/size[0], 720/size[1])
                    new_size = (int(size[0]*scale_factor), int(size[1]*scale_factor))
                    scaled_img = pygame.transform.scale(pygame_img, new_size)
                    
                    # Convert pygame surface to PhotoImage via PPM
                    img_str = pygame.image.tostring(scaled_img, 'RGB')
                    w, h = scaled_img.get_size()
                    
                    # Create PPM format image data
                    ppm = f'P6 {w} {h} 255 '.encode() + img_str
                    
                    # Create PhotoImage from PPM data
                    photo = tk.PhotoImage(width=w, height=h, data=ppm, format='PPM')
                    
                    # Update label
                    self.album_art_label.config(image=photo)
                    self.album_art_label.image = photo  # Keep a reference
        
        except Exception as e:
            logger.error(f"Error displaying album art: {e}")
            # Show solid color as last resort
            self.album_art_label.config(bg='#1a1a1a')
    
    def check_pygame_events(self):
        """Check for pygame events (song end)"""
        for event in pygame.event.get():
            if event.type == self.music_player.SONG_END:
                self.music_player.handle_song_end()
        
        # Check every 100ms
        self.root.after(100, self.check_pygame_events)
    
    def cleanup(self):
        """Clean up resources"""
        logger.info("Cleaning up...")
        self.music_player.stop()
        self.rfid_reader.cleanup()
        pygame.quit()


def main():
    """Main entry point"""
    root = tk.Tk()
    
    # Check if running on Raspberry Pi
    mock_rfid = not os.path.exists('/sys/firmware/devicetree/base/model')
    
    app = JukeboxApp(root, mock_rfid=mock_rfid)
    
    # Handle window close
    def on_closing():
        app.cleanup()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start main loop
    root.mainloop()


if __name__ == "__main__":
    main()

