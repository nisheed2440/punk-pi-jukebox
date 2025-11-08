# Project Structure

## Directory Tree

```
py-3/  (jukebox project root)
│
├── Core Application Files
│   ├── jukebox_app.py          # Main application entry point
│   ├── rfid_reader.py          # RFID/NFC reader wrapper
│   ├── music_library.py        # Music library scanner and manager
│   ├── music_player.py         # Pygame music player
│   └── config_manager.py       # Configuration management
│
├── Setup & Installation
│   ├── setup.sh                # Automated setup script
│   ├── install_service.sh      # Systemd service installer
│   ├── jukebox.service.example # Systemd service template
│   ├── requirements.txt        # Python dependencies
│   └── test_setup.py          # Installation verification script
│
├── Documentation
│   ├── README.md              # Complete documentation
│   ├── QUICKSTART.md          # Quick start guide
│   └── STRUCTURE.md           # This file
│
├── Assets
│   ├── fallback_albumart.png  # Default album art image
│   └── create_fallback_art.py # Script to generate fallback art
│
├── Configuration (auto-generated)
│   └── config.json            # App settings (created on first run)
│
├── Music Library
│   └── music/                 # Music files directory
│       ├── README.md          # Music library guide
│       └── <nfc_id>/          # Playlist directories (you create these)
│           └── <seq>_<artist>/
│               └── <seq>_<album>/
│                   ├── albumart.png
│                   └── <seq>_<song>.mp3
│
├── Python Virtual Environment
│   └── venv/                  # Virtual environment (created by setup)
│
└── Version Control
    ├── .git/                  # Git repository
    └── .gitignore            # Git ignore rules
```

## File Descriptions

### Core Application Files

| File | Purpose | Key Features |
|------|---------|--------------|
| `jukebox_app.py` | Main application | Tkinter GUI, NFC polling, event handling |
| `rfid_reader.py` | RFID interface | MFRC522 wrapper, mock mode for testing |
| `music_library.py` | Music management | Library scanning, playlist organization |
| `music_player.py` | Audio playback | Pygame mixer, playlist control |
| `config_manager.py` | Settings | JSON config, NFC mappings |

### Setup Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `setup.sh` | One-time setup | `./setup.sh` |
| `install_service.sh` | Auto-start config | `./install_service.sh` |
| `test_setup.py` | Verify installation | `python test_setup.py` |

### Music Library Structure

```
music/
└── 123456789/                    # NFC tag ID
    ├── 01_daft_punk/             # Artist (seq 01)
    │   ├── 01_discovery/         # Album (seq 01)
    │   │   ├── albumart.png      # Album cover (600x600+ recommended)
    │   │   ├── 01_one_more_time.mp3
    │   │   ├── 02_aerodynamic.mp3
    │   │   └── 03_digital_love.mp3
    │   └── 02_random_access_memories/
    │       ├── albumart.png
    │       └── 01_get_lucky.mp3
    └── 02_justice/               # Another artist (seq 02)
        └── 01_cross/
            ├── albumart.png
            ├── 01_genesis.mp3
            └── 02_let_there_be_light.mp3
```

**Naming Convention:**
- NFC ID: Exact tag ID (e.g., `123456789`)
- Artist: `<seq>_<name>` (e.g., `01_daft_punk`)
- Album: `<seq>_<name>` (e.g., `01_discovery`)
- Song: `<seq>_<name>.<ext>` (e.g., `01_one_more_time.mp3`)

**Rules:**
- Use lowercase with underscores
- Use leading zeros (01, 02, ..., 10, 11, ...)
- Supported formats: MP3, WAV, OGG, FLAC, M4A
- Album art must be named `albumart.png`

## Configuration File

`config.json` is auto-generated with these settings:

```json
{
  "music_library_path": "music",     // Path to music library
  "stop_nfc_id": "987654321",        // NFC tag to stop playback
  "volume": 0.7,                     // Volume (0.0 to 1.0)
  "nfc_mappings": {},                // Reserved for future use
  "debug_mode": false                // Debug flag
}
```

## Data Flow

```
NFC Tag Tapped
     ↓
RFID Reader (rfid_reader.py)
     ↓
Jukebox App (jukebox_app.py)
     ↓
Music Library (music_library.py) ← Scans folder structure
     ↓
Music Player (music_player.py) ← Loads playlist
     ↓
Pygame Mixer ← Plays audio
     ↓
UI Updates ← Shows album art + song info
```

## UI Components

```
┌─────────────────────────────────────────┐
│ ⚙ (Debug Menu)                         │  ← Debug icon (top-left)
│                                         │
│                                         │
│         [Album Art Display]             │  ← Album cover image
│                                         │
│                                         │
│    ─────────────────────────────        │
│         Song Title                      │  ← Song info overlay
│         Artist Name                     │     (on top of album art)
│         Album Name                      │
│    ─────────────────────────────        │
└─────────────────────────────────────────┘
```

### Debug Menu Features

- **Read NFC Mode**: Display tag IDs without playing
- **Configure Stop NFC**: Set stop-playback tag
- **Music Library Path**: Change library location
- **Rescan Library**: Reload music database
- **Save Configuration**: Persist settings

## Hardware Setup

### MFRC522 to Raspberry Pi

```
MFRC522        Raspberry Pi
───────        ────────────
SDA      →     GPIO 8  (Pin 24)
SCK      →     GPIO 11 (Pin 23)
MOSI     →     GPIO 10 (Pin 19)
MISO     →     GPIO 9  (Pin 21)
IRQ      →     (not connected)
GND      →     GND     (Pin 6)
RST      →     GPIO 25 (Pin 22)
3.3V     →     3.3V    (Pin 1)
```

## Dependencies

### Python Packages
- `pygame` - Audio playback
- `pillow` (PIL) - Image processing
- `mfrc522` - RFID reader
- `spidev` - SPI communication
- `RPi.GPIO` - GPIO control (Raspberry Pi only)

### System Requirements
- Python 3.7+
- SPI enabled (Raspberry Pi)
- Audio output configured
- Display (800x480 recommended)

## Common Operations

### Get NFC Tag ID
1. Run app: `python jukebox_app.py`
2. Click ⚙ → "Read NFC Mode"
3. Tap NFC tag
4. Note the displayed ID

### Add New Playlist
1. Create folder: `music/<nfc_tag_id>/`
2. Add music following structure
3. Open debug menu → "Rescan Library"

### Configure Stop Tag
1. Open debug menu
2. Click "Configure Stop NFC"
3. Tap desired NFC tag
4. Click "Save Configuration"

### Auto-start on Boot
```bash
./install_service.sh
sudo systemctl start jukebox.service
```

## Troubleshooting

### Check Installation
```bash
python test_setup.py
```

### View Logs (if running as service)
```bash
journalctl -u jukebox.service -f
```

### Manual Run (with logs)
```bash
python jukebox_app.py
```

## Extending the App

### Add New Audio Format
Edit `music_library.py`, line ~161:
```python
if not filename.lower().endswith(('.mp3', '.wav', '.ogg', '.flac', '.m4a', '.aac')):
```

### Change UI Size
Edit `jukebox_app.py`, line ~38:
```python
self.root.geometry("800x480")  # Change dimensions
```

### Customize Album Art Size
Edit `jukebox_app.py`, line ~399:
```python
img.thumbnail((800, 480), Image.Resampling.LANCZOS)  # Change size
```

## License

MIT License - Free to use and modify.

