# Raspberry Pi Zero 2 W - Power and Stability Issues

## Problem: Pi Reboots During Setup

If your Raspberry Pi Zero 2 W keeps rebooting during `setup.sh`, this is usually caused by:

1. **Insufficient Power Supply** (most common)
2. **System Overload** (too many packages installing at once)
3. **Overheating**
4. **Corrupted SD Card**

## Solutions

### 1. Use Proper Power Supply (CRITICAL) ⚡

**Pi Zero 2 W Requirements:**
- Minimum: 5V @ 2.5A (12.5W)
- Recommended: 5V @ 3A (15W) official Raspberry Pi power supply
- Use USB-C cable rated for power delivery

**Check Your Setup:**
```bash
# Check for undervoltage warnings
vcgencmd get_throttled
```

If output is not `throttled=0x0`, you have power issues!

**Undervoltage Codes:**
- `0x50000` = Undervoltage occurred
- `0x50005` = Undervoltage + currently throttled

**Fix:**
- Use official Raspberry Pi power supply
- Use shorter, thicker USB cable
- Avoid using computer USB ports
- Don't power through a USB hub

### 2. Use Lightweight Setup Script

The Pi Zero 2 W is slow and can be overwhelmed by installing many packages at once.

**Use the lite version:**

```bash
chmod +x setup_lite.sh
./setup_lite.sh
```

This script:
- Installs packages ONE at a time
- Adds pauses between installations
- Uses `--no-cache-dir` to reduce memory usage
- Takes 30-60 minutes but is more stable

### 3. Manual Installation (Most Reliable)

If automated scripts keep failing, install manually:

#### Step 1: Install System Dependencies

```bash
# Update first
sudo apt-get update
sleep 5

# Install one by one
sudo apt-get install -y python3-dev
sudo apt-get install -y python3-pip
sudo apt-get install -y libsdl2-dev
sleep 10  # Wait between heavy packages
sudo apt-get install -y libsdl2-mixer-dev
sleep 10
sudo apt-get install -y libsdl2-image-dev
sleep 10
sudo apt-get install -y libsdl2-ttf-dev
sleep 10

# Lighter packages
sudo apt-get install -y libfreetype6-dev libportmidi-dev
sudo apt-get install -y libjpeg-dev zlib1g-dev libpng-dev
```

#### Step 2: Create Virtual Environment

```bash
cd ~/jukebox
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Python Packages (SLOWLY)

```bash
# Upgrade pip
pip install --upgrade pip --no-cache-dir

# Install one by one with pauses
pip install pillow==10.1.0 --no-cache-dir
sleep 60  # Wait 1 minute

# Pygame takes FOREVER on Pi Zero 2 W (15-30 minutes!)
# Make sure you have good power supply
pip install pygame==2.5.2 --no-cache-dir
sleep 60

pip install mfrc522==0.0.7 --no-cache-dir
sleep 30

pip install spidev==3.6 --no-cache-dir
sleep 30

pip install RPi.GPIO==0.7.1 --no-cache-dir
```

#### Step 4: Finish Setup

```bash
# Create directories
mkdir -p music

# Generate album art
python create_fallback_art.py

# Create config
cat > config.json << 'EOF'
{
  "music_library_path": "music",
  "stop_nfc_id": null,
  "volume": 0.7,
  "nfc_mappings": {},
  "debug_mode": false
}
EOF
```

### 4. Increase Swap Space

The Pi Zero 2 W only has 512MB RAM. Increase swap:

```bash
# Stop swap
sudo dphys-swapfile swapoff

# Edit config
sudo nano /etc/dphys-swapfile
# Change: CONF_SWAPSIZE=100
# To:     CONF_SWAPSIZE=1024

# Restart swap
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

Then try setup again.

### 5. Cool Down and Monitor

```bash
# Check temperature
vcgencmd measure_temp

# If over 70°C, add cooling or wait
```

Add heatsinks or small fan if needed.

### 6. Use Pre-built Packages

Instead of compiling pygame from source, use pre-built wheels:

```bash
source venv/bin/activate

# Try pre-built wheel
pip install pygame --no-cache-dir --prefer-binary
```

Or use system package:

```bash
# Install system pygame
sudo apt-get install -y python3-pygame

# Create venv with system packages
python3 -m venv --system-site-packages venv
```

### 7. Run Setup Over SSH (Not Desktop)

If running desktop environment:

```bash
# Stop desktop to free memory
sudo systemctl stop lightdm

# Run setup
./setup_lite.sh

# Restart desktop
sudo systemctl start lightdm
```

Or better - run entirely over SSH with no desktop loaded.

### 8. Check SD Card

```bash
# Check for errors
sudo fsck -f /dev/mmcblk0p2

# Check disk space
df -h
```

Make sure you have at least 2GB free.

## Recommended Setup Process for Pi Zero 2 W

1. **Use official 5V 3A power supply**
2. **Enable SSH, disable desktop** (run headless during setup)
3. **Increase swap to 1GB**
4. **Run `setup_lite.sh`** (not regular setup.sh)
5. **Be patient** - pygame compilation takes 20-30 minutes
6. **Monitor temperature** - add cooling if needed
7. **Don't use the Pi during installation**

## Alternative: Cross-Compile on Faster Pi

If you have a Pi 4 or Pi 5:

1. Set up on faster Pi first
2. Copy the entire `venv` directory to Pi Zero 2 W
3. Much faster than compiling on Zero 2 W

```bash
# On Pi 4
cd ~/jukebox
./setup.sh

# Copy to Zero 2 W
scp -r ~/jukebox pi@zero2w.local:~/

# On Zero 2 W
cd ~/jukebox
source venv/bin/activate
python jukebox_app.py
```

## Monitoring Power During Setup

Install helpful tools:

```bash
sudo apt-get install -y stress cpufrequtils

# Monitor during setup
watch -n 1 'vcgencmd measure_temp && vcgencmd get_throttled && vcgencmd measure_clock arm'
```

## Still Crashing?

If all else fails, use pre-installed system packages:

```bash
# Install everything from apt
sudo apt-get install -y \
    python3-pygame \
    python3-pil \
    python3-spidev \
    python3-rpi.gpio

# Install only mfrc522 via pip
python3 -m venv --system-site-packages venv
source venv/bin/activate
pip install mfrc522 --no-cache-dir
```

This avoids all compilation but may have older package versions.

## Expected Install Times on Pi Zero 2 W

- System dependencies: 10-15 minutes
- Virtual environment: 1 minute
- Pillow: 3-5 minutes
- **Pygame: 20-30 minutes** ⚠️ (longest part)
- Other packages: 2-3 minutes each

**Total: 45-60 minutes with good power supply**

If it crashes before 30 minutes, it's almost certainly a power issue!

## Hardware Checklist

- [ ] Official Raspberry Pi 5V 3A power supply
- [ ] Short, thick USB-C cable (no thin charging cables)
- [ ] Heatsink or fan (optional but recommended)
- [ ] Quality SD card (SanDisk, Samsung - not cheap brands)
- [ ] Not powering anything else from the Pi during setup

Fix power first - everything else depends on it! ⚡

