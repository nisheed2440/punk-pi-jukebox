# Quick Start Guide

## For Raspberry Pi Users

### 1. Initial Setup (One-time)

```bash
# Navigate to project directory
cd ~/jukebox

# For Pi Zero 2 W - use lite version (more stable)
chmod +x setup_lite.sh
./setup_lite.sh

# For Pi 3/4/5 - use regular version
chmod +x setup.sh
./setup.sh
```

**⚠️ Pi Zero 2 W Users:**
- Use `setup_lite.sh` (not setup.sh)
- Ensure you have a **5V 3A power supply** or Pi will reboot!
- Takes 45-60 minutes to complete
- Be patient during pygame installation (20+ minutes)

**If Pi keeps rebooting:**
```bash
# Check power supply (most common issue)
vcgencmd get_throttled

# If output is not 0x0, you have power problems!
# See POWER_ISSUES.md for solutions
```

### 2. Enable SPI (Required for RFID)

```bash
sudo raspi-config
```

Navigate to: **Interface Options** → **SPI** → **Enable**

Then reboot:
```bash
sudo reboot
```

### 3. Add Music

1. Create a folder structure like this:

```
music/
└── <your_nfc_tag_id>/
    └── 01_artist_name/
        └── 01_album_name/
            ├── albumart.png
            └── 01_song_name.mp3
```

2. To get your NFC tag ID:
   - Run the app
   - Click ⚙️ (gear icon)
   - Click "Read NFC Mode"
   - Tap your NFC tag
   - Note the ID shown

### 4. Run the Jukebox

```bash
source venv/bin/activate
python jukebox_app.py
```

## Testing Without Hardware

You can test the app on any computer (Mac, Linux, Windows):

```bash
# Setup
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pygame pillow

# Run (RFID will be in mock mode)
python jukebox_app.py
```

## Common Tasks

### Update Music Library

Just add new folders/files to the `music` directory, then:
- Open debug menu (⚙️)
- Click "Rescan Music Library"

### Configure Stop NFC Tag

1. Open debug menu (⚙️)
2. Click "Configure Stop NFC"
3. Tap the NFC tag you want to use
4. Click "Save Configuration"

### Change Music Library Location

1. Open debug menu (⚙️)
2. Update "Music Library Path"
3. Click "Save Configuration"

## Troubleshooting

### "No module named 'RPi'"

This is normal on non-Raspberry Pi systems. The app will run in mock mode.

### "Permission denied" for GPIO/SPI

```bash
sudo usermod -a -G gpio,spi $USER
sudo reboot
```

### No sound

```bash
# Check audio output
amixer cget numid=3

# Set to headphone jack (1), HDMI (2), or auto (0)
amixer cset numid=3 1
```

### RFID not reading

1. Check SPI is enabled: `lsmod | grep spi`
2. Check wiring connections
3. Try different NFC tag (must be MIFARE compatible)

## Auto-Start on Boot

```bash
# Create systemd service
sudo nano /etc/systemd/system/jukebox.service

# Add content (see README.md for details)

# Enable service
sudo systemctl enable jukebox.service
sudo systemctl start jukebox.service
```

## File Structure Quick Reference

```
jukebox/
├── jukebox_app.py          # Main app - run this
├── setup.sh                # Setup script
├── requirements.txt        # Dependencies
├── README.md              # Full documentation
├── QUICKSTART.md          # This file
├── venv/                  # Virtual environment (created by setup)
├── music/                 # Your music library
│   └── <nfc_id>/
│       └── <seq>_artist/
│           └── <seq>_album/
│               ├── albumart.png
│               └── <seq>_song.mp3
└── config.json           # App settings (auto-created)
```

## Need Help?

See the full [README.md](README.md) for detailed documentation.

