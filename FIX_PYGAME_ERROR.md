# Fix Pygame SDL2 Installation Error

## Problem

You're seeing this error when running setup.sh:

```
/bin/sh: 1: sdl2-config: not found
IndexError: list index out of range
ERROR: Failed to build 'pygame' when getting requirements to build wheel
```

## Solution

Pygame requires SDL2 system libraries to be installed BEFORE you can install the Python package.

### Quick Fix

Run this script which installs all required system dependencies:

```bash
cd ~/jukebox
./install_dependencies.sh
```

Then try setup again:

```bash
./setup.sh
```

### Manual Fix

If you prefer to install manually:

```bash
# Update package list
sudo apt-get update

# Install SDL2 and related libraries
sudo apt-get install -y \
    python3-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libportmidi-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev

# Now install pygame
source venv/bin/activate
pip install pygame
```

## What Each Library Does

- **libsdl2-dev** - Core SDL2 library (Simple DirectMedia Layer)
- **libsdl2-image-dev** - Image loading (PNG, JPG, etc.)
- **libsdl2-mixer-dev** - Audio mixing (music playback)
- **libsdl2-ttf-dev** - TrueType font rendering
- **libfreetype6-dev** - Font rendering support
- **libportmidi-dev** - MIDI support
- **libjpeg-dev, libpng-dev, zlib1g-dev** - Image format support

## After Installing Dependencies

Continue with the normal setup:

```bash
cd ~/jukebox

# If venv doesn't exist yet
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

## Verification

To verify pygame installed correctly:

```bash
source venv/bin/activate
python3 -c "import pygame; print('Pygame version:', pygame.version.ver)"
```

Should output something like:
```
Pygame version: 2.5.2
```

## Alternative: Use System Pygame (Not Recommended)

If you still have issues, you can use the system-installed pygame:

```bash
# Install system pygame
sudo apt-get install -y python3-pygame

# Create venv with access to system packages
python3 -m venv --system-site-packages venv
source venv/bin/activate
```

**Note:** This is not recommended as it may have version conflicts.

## Still Having Issues?

1. Make sure you ran `sudo apt-get update` first
2. Check your Raspberry Pi OS is up to date: `sudo apt upgrade -y`
3. Make sure you have enough disk space: `df -h`
4. Check Python version: `python3 --version` (should be 3.7+)

## Common Issues

### "Unable to locate package libsdl2-dev"

Your package list may be outdated:
```bash
sudo apt-get update
sudo apt-get upgrade
```

### "E: Could not get lock /var/lib/dpkg/lock"

Another package manager is running. Wait for it to finish or reboot:
```bash
sudo reboot
```

### "Permission denied"

Make sure scripts are executable:
```bash
chmod +x setup.sh
chmod +x install_dependencies.sh
```

---

**Updated:** The latest version of setup.sh now automatically installs these dependencies!

Just run `./setup.sh` and it will handle everything.

