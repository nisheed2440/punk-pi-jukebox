# Getting Started with Raspberry Pi Jukebox

This guide will walk you through setting up your jukebox from scratch.

## 📋 Prerequisites

### Hardware
- ✅ Raspberry Pi Zero 2 W (or any Raspberry Pi)
- ✅ MFRC522 RFID/NFC Reader module
- ✅ NFC tags (MIFARE Classic or compatible)
- ✅ MicroSD card (8GB+ recommended)
- ✅ Display (HDMI/DSI connected)
- ✅ Speakers or headphones
- ✅ Power supply

### Optional
- Jumper wires for MFRC522 connection
- Case for the project
- Buttons for physical controls (future enhancement)

## 🔌 Step 1: Hardware Setup

### Connect MFRC522 to Raspberry Pi

```
MFRC522 Pin    →    Raspberry Pi Pin
─────────────────────────────────────
SDA            →    GPIO 8  (Pin 24)
SCK            →    GPIO 11 (Pin 23)
MOSI           →    GPIO 10 (Pin 19)
MISO           →    GPIO 9  (Pin 21)
IRQ            →    Not connected
GND            →    GND     (Pin 6)
RST            →    GPIO 25 (Pin 22)
3.3V           →    3.3V    (Pin 1)
```

**Important:** 
- Never connect MFRC522 to 5V - it will damage the module!
- Use 3.3V only
- Double-check connections before powering on

## 💻 Step 2: Raspberry Pi OS Setup

### Enable SPI Interface

```bash
sudo raspi-config
```

Navigate: **Interface Options** → **SPI** → **Enable** → **Finish**

Reboot:
```bash
sudo reboot
```

### Update System

```bash
sudo apt update
sudo apt upgrade -y
```

### Install Dependencies

```bash
sudo apt install -y python3-pip python3-venv git
```

## 📥 Step 3: Install Jukebox

### Clone/Transfer Project

If using git:
```bash
cd ~
git clone <your-repo-url> jukebox
cd jukebox
```

Or if you have the files locally:
```bash
cd ~
mkdir jukebox
# Transfer files to ~/jukebox
cd jukebox
```

### Run Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create Python virtual environment
- Install all dependencies
- Create music directory structure
- Generate fallback album art
- Create default configuration

## 🎵 Step 4: Add Your Music

### Method 1: Using the Sample Structure Script

```bash
./create_sample_structure.sh
```

This creates a template structure. Then:
1. Navigate to `music/sample_123456/`
2. Add your MP3 files following the naming convention
3. Add `albumart.png` files to each album folder
4. Rename the folder to your actual NFC tag ID (see next section)

### Method 2: Manual Structure

Create this structure:

```
music/
└── <YOUR_NFC_TAG_ID>/
    └── 01_artist_name/
        └── 01_album_name/
            ├── albumart.png
            ├── 01_song_one.mp3
            ├── 02_song_two.mp3
            └── 03_song_three.mp3
```

**File Naming Rules:**
- Artists: `01_daft_punk`, `02_justice` (lowercase, underscores)
- Albums: `01_discovery`, `02_cross`
- Songs: `01_one_more_time.mp3`, `02_aerodynamic.mp3`
- Album art: Must be named exactly `albumart.png`

## 🏷️ Step 5: Get Your NFC Tag IDs

### Start the App

```bash
source venv/bin/activate
python jukebox_app.py
```

### Read NFC Tags

1. Click the **⚙️** (gear icon) in top-left corner
2. Click **"Read NFC Mode"** button
3. Tap each NFC tag on the reader
4. Note the ID displayed
5. Click **"Stop Read Mode"** when done

### Rename Your Music Folders

Rename your music folders to match the NFC tag IDs:

```bash
mv music/sample_123456 music/123456789012
```

Where `123456789012` is your actual NFC tag ID.

## 🎮 Step 6: Test the Jukebox

### Rescan Music Library

1. Open debug menu (⚙️)
2. Click **"Rescan Music Library"**
3. Check that it finds your playlists

### Play Music

1. Tap an NFC tag on the reader
2. Music should start playing!
3. Album art should display
4. Song info should show at bottom

## ⚙️ Step 7: Configure (Optional)

### Set Up Stop NFC Tag

If you want a special tag to stop playback:

1. Open debug menu (⚙️)
2. Click **"Configure Stop NFC"**
3. Tap the NFC tag you want to use
4. Click **"Save Configuration"**

### Adjust Settings

In debug menu:
- Change music library path if needed
- Test different configurations
- Save settings when done

## 🚀 Step 8: Auto-Start on Boot (Optional)

To make the jukebox start automatically:

```bash
./install_service.sh
```

Then:
```bash
sudo systemctl start jukebox.service
sudo systemctl status jukebox.service
```

To view logs:
```bash
journalctl -u jukebox.service -f
```

To stop auto-start:
```bash
sudo systemctl disable jukebox.service
```

## ✅ Step 9: Verify Installation

Run the test script:

```bash
python test_setup.py
```

This checks:
- ✓ All Python modules installed
- ✓ Project structure correct
- ✓ Music library readable
- ✓ Pygame working
- ✓ Configuration valid

## 📖 Quick Reference

### Running the App

```bash
cd ~/jukebox
source venv/bin/activate
python jukebox_app.py
```

### Adding New Music

1. Add files to `music/<nfc_id>/` folders
2. Open debug menu
3. Click "Rescan Music Library"
4. Tap NFC tag to play

### Stopping the App

- Press Ctrl+C in terminal
- Or close the window

### Updating the App

```bash
git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

## 🐛 Troubleshooting

### RFID Not Working

Check SPI:
```bash
lsmod | grep spi
```

Should show: `spi_bcm2835`

Check wiring:
```bash
python3 << EOF
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
print("Tap NFC tag...")
print(reader.read())
EOF
```

### No Sound

Set audio output:
```bash
sudo raspi-config
# System Options → Audio → Select output
```

Test audio:
```bash
speaker-test -t wav -c 2
```

### Permission Errors

```bash
sudo usermod -a -G gpio,spi,audio $USER
sudo reboot
```

### App Crashes

Check logs:
```bash
python jukebox_app.py
# Watch for error messages
```

Or if running as service:
```bash
journalctl -u jukebox.service -n 50
```

### Music Not Loading

1. Check file names follow convention
2. Check folder structure is correct
3. Try "Rescan Music Library"
4. Check permissions: `ls -la music/`

## 📚 Documentation

- **README.md** - Complete documentation
- **QUICKSTART.md** - Quick reference guide
- **STRUCTURE.md** - Project architecture
- **music/README.md** - Music library guide
- **GETTING_STARTED.md** - This file

## 🎯 Next Steps

### Enhance Your Jukebox

1. **Add More Music**
   - Organize by genre, mood, or artist
   - Create different NFC tags for different playlists

2. **Customize the UI**
   - Edit `jukebox_app.py` to change colors, fonts, layout
   - Add custom backgrounds or themes

3. **Physical Enclosure**
   - Design a case for the Raspberry Pi and RFID reader
   - Add physical buttons (future enhancement)

4. **Advanced Features** (You can extend)
   - Shuffle mode
   - Repeat mode
   - Volume control buttons
   - Current playlist view
   - Search functionality

## 💡 Tips

- **Album Art**: Use 600x600px or larger PNG images for best quality
- **File Names**: Keep them simple and consistent
- **Organization**: Group similar music under the same NFC tag
- **Testing**: Use "Read NFC Mode" to verify tags before adding music
- **Backup**: Keep a backup of your music library and config.json

## 🤝 Support

If you run into issues:

1. Check the troubleshooting section above
2. Read the full README.md
3. Run `python test_setup.py` to diagnose issues
4. Check file permissions and ownership
5. Verify RFID reader is working with a test script

## 🎉 Enjoy Your Jukebox!

You're all set! Tap an NFC tag and enjoy your music.

---

**Project Files Summary:**
- `jukebox_app.py` - Main application
- `setup.sh` - Initial setup
- `test_setup.py` - Verify installation
- `create_sample_structure.sh` - Create example folders
- `install_service.sh` - Enable auto-start

**Happy listening! 🎵**

