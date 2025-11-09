# Raspberry Pi Jukebox

A Python-based jukebox application for Raspberry Pi Zero 2 W with NFC/RFID support using MFRC522 reader.

## Features

- 🎵 Play music from NFC tags
- 📁 Organized music library by playlist/artist/album
- 🖼️ Album art display with song info overlay
- ⚙️ Debug menu for NFC configuration
- 🛑 Special NFC tag to stop music playback
- 🔄 Automatic playlist progression
- 🎨 Beautiful Tkinter GUI

## Hardware Requirements

- Raspberry Pi Zero 2 W (or any Raspberry Pi)
- MFRC522 RFID/NFC Reader
- NFC tags (MIFARE Classic or compatible)
- Display (720x720 recommended, HDMI or DSI)
- Speakers or audio output

## MFRC522 Wiring

Connect the MFRC522 to your Raspberry Pi as follows:

| MFRC522 Pin | Raspberry Pi Pin |
|-------------|------------------|
| SDA         | GPIO 8 (Pin 24)  |
| SCK         | GPIO 11 (Pin 23) |
| MOSI        | GPIO 10 (Pin 19) |
| MISO        | GPIO 9 (Pin 21)  |
| IRQ         | Not connected    |
| GND         | GND (Pin 6)      |
| RST         | GPIO 25 (Pin 22) |
| 3.3V        | 3.3V (Pin 1)     |

## Installation

### 1. Enable SPI on Raspberry Pi

```bash
sudo raspi-config
# Navigate to: Interface Options -> SPI -> Enable
sudo reboot
```

### 2. Clone and Setup

```bash
cd ~
git clone <your-repo-url> jukebox
cd jukebox

# For Pi Zero 2 W - use lite version (slower but more stable)
./setup_lite.sh

# For Pi 3/4/5 - use regular version
./setup.sh
```

**⚠️ Important for Pi Zero 2 W:**
- Use official 5V 3A power supply (insufficient power causes reboots!)
- Setup takes 45-60 minutes
- See `POWER_ISSUES.md` if you experience crashes

**Or manually:**

```bash
# Install system dependencies first
./install_dependencies.sh

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

### 3. Set Up Music Library

Create your music library following this structure:

```
music/
├── <NFC_ID_1>/
│   ├── 01_artist_name/
│   │   ├── 01_album_name/
│   │   │   ├── albumart.png
│   │   │   ├── 01_song_name.mp3
│   │   │   ├── 02_another_song.mp3
│   │   │   └── ...
│   │   └── 02_another_album/
│   │       └── ...
│   └── 02_another_artist/
│       └── ...
├── <NFC_ID_2>/
│   └── ...
```

**Example:**
```
music/
├── 123456789/
│   ├── 01_daft_punk/
│   │   ├── 01_discovery/
│   │   │   ├── albumart.png
│   │   │   ├── 01_one_more_time.mp3
│   │   │   ├── 02_aerodynamic.mp3
│   │   │   └── 03_digital_love.mp3
│   │   └── 02_random_access_memories/
│   │       ├── albumart.png
│   │       └── 01_get_lucky.mp3
│   └── 02_justice/
│       └── 01_cross/
│           ├── albumart.png
│           └── 01_genesis.mp3
```

**Naming Convention:**
- NFC ID folders: Use the exact NFC tag ID
- Artist folders: `<seq_no>_<artist_name>` (e.g., `01_daft_punk`)
- Album folders: `<seq_no>_<album_name>` (e.g., `01_discovery`)
- Song files: `<seq_no>_<song_name>.mp3` (e.g., `01_robot_rock.mp3`)
- Album art: `albumart.png` in each album folder

## Usage

### Running the App

```bash
cd ~/jukebox
source venv/bin/activate
python jukebox_app.py
```

### Auto-start on Boot (Optional)

Create a systemd service:

```bash
sudo nano /etc/systemd/system/jukebox.service
```

Add the following content:

```ini
[Unit]
Description=Jukebox App
After=multi-user.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/jukebox
Environment="DISPLAY=:0"
ExecStart=/home/pi/jukebox/venv/bin/python /home/pi/jukebox/jukebox_app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable jukebox.service
sudo systemctl start jukebox.service
```

### Debug Menu

Click the ⚙️ icon in the top-left corner to access the debug menu:

- **Read NFC Mode**: Display NFC tag IDs without playing music
- **Configure Stop NFC**: Set up a special NFC tag to stop playback
- **Music Library Path**: Change the music library location
- **Rescan Library**: Reload the music library
- **Save Configuration**: Save all settings

### Configuration

The app stores configuration in `config.json`:

```json
{
  "music_library_path": "music",
  "stop_nfc_id": "987654321",
  "volume": 0.7,
  "nfc_mappings": {},
  "debug_mode": false
}
```

## Supported Audio Formats

- MP3 (.mp3)
- WAV (.wav)
- OGG (.ogg)
- FLAC (.flac)
- M4A (.m4a)

## Troubleshooting

### Pygame Installation Fails (SDL2 Error)

If you get an error about `sdl2-config` not found:

```bash
# Install SDL2 dependencies
./install_dependencies.sh
```

Or manually:
```bash
sudo apt-get update
sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
```

Then try again:
```bash
source venv/bin/activate
pip install pygame
```

### RFID Reader Not Working

1. Check SPI is enabled:
   ```bash
   lsmod | grep spi
   ```

2. Check wiring connections

3. Test RFID reader:
   ```bash
   python -c "from mfrc522 import SimpleMFRC522; reader = SimpleMFRC522(); print('Tap NFC tag...'); print(reader.read())"
   ```

### No Audio Output

1. Check audio configuration:
   ```bash
   sudo raspi-config
   # System Options -> Audio -> Select audio output
   ```

2. Test audio:
   ```bash
   speaker-test -t wav
   ```

### Permission Issues

```bash
sudo usermod -a -G gpio,spi pi
sudo reboot
```

## Development

### Running in Mock Mode (without RFID hardware)

The app automatically detects if it's running on a Raspberry Pi. On other systems, it runs in mock mode.

### Creating Fallback Album Art

```bash
python create_fallback_art.py
```

## Project Structure

```
.
├── jukebox_app.py          # Main application
├── rfid_reader.py          # RFID/NFC reader interface
├── music_library.py        # Music library manager
├── music_player.py         # Pygame music player
├── config_manager.py       # Configuration management
├── create_fallback_art.py  # Generate fallback album art
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore            # Git ignore rules
├── fallback_albumart.png # Default album art
├── config.json           # App configuration (created on first run)
└── music/                # Music library folder
```

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Built with Python, Tkinter, and Pygame
- MFRC522 library for RFID support
- Designed for Raspberry Pi

