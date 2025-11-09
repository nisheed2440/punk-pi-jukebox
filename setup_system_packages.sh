#!/bin/bash
# Setup using ONLY system packages - fastest and most reliable for Pi Zero 2 W
# No compilation required!

echo "========================================="
echo "Jukebox Setup (System Packages Only)"
echo "========================================="
echo ""
echo "This method uses pre-built Debian packages"
echo "No compilation = faster, more reliable"
echo "Perfect for Pi Zero 2 W"
echo ""

# Check if running on Raspberry Pi
if [ -f /sys/firmware/devicetree/base/model ]; then
    echo "✓ Running on Raspberry Pi"
    IS_RPI=true
else
    echo "⚠ Not running on Raspberry Pi"
    IS_RPI=false
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"
echo ""

# Update package list
echo "Updating package list..."
sudo apt-get update
echo ""

# Install ALL dependencies from system packages
echo "Installing system packages..."
echo "This is much faster than compiling!"
echo ""

sudo apt-get install -y \
    python3-pygame \
    python3-spidev \
    python3-rpi.gpio \
    python3-pip \
    python3-venv

if [ $? -ne 0 ]; then
    echo "✗ Failed to install system packages"
    exit 1
fi

echo "✓ System packages installed"
echo ""

# Create virtual environment with system packages
echo "Creating virtual environment (with system packages access)..."
python3 -m venv --system-site-packages venv

if [ $? -ne 0 ]; then
    echo "✗ Failed to create virtual environment"
    exit 1
fi

echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --no-cache-dir
echo ""

# Only install packages not available from apt
echo "Installing mfrc522 (not in apt repositories)..."
pip install mfrc522==0.0.7 --no-cache-dir

if [ $? -ne 0 ]; then
    echo "✗ Failed to install mfrc522"
    exit 1
fi

echo "✓ mfrc522 installed"
echo ""

# Create music directory
echo "Creating music directory structure..."
mkdir -p music
mkdir -p music/example_nfc_id/01_example_artist/01_example_album
echo "✓ Music directory created"
echo ""

# Generate fallback album art
echo "Generating fallback album art..."
python create_fallback_art.py

if [ $? -ne 0 ]; then
    echo "⚠ Fallback art generation failed"
    echo "  The app will work without it"
fi
echo ""

# Create initial config
echo "Creating initial configuration..."
cat > config.json << EOF
{
  "music_library_path": "music",
  "stop_nfc_id": null,
  "volume": 0.7,
  "nfc_mappings": {},
  "debug_mode": false
}
EOF

echo "✓ Configuration file created"
echo ""

# Check SPI on Raspberry Pi
if [ "$IS_RPI" = true ]; then
    echo "Checking SPI configuration..."
    
    if lsmod | grep -q spi_bcm2835; then
        echo "✓ SPI is enabled"
    else
        echo "⚠ SPI is not enabled!"
        echo "  Enable SPI with: sudo raspi-config"
        echo "  Navigate to: Interface Options -> SPI -> Enable"
        echo "  Then reboot: sudo reboot"
    fi
fi

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Installation method: System packages (no compilation)"
echo "Total time: ~2-5 minutes (much faster!)"
echo ""
echo "Installed:"
echo "  ✓ pygame (from apt)"
echo "  ✓ spidev (from apt)"
echo "  ✓ RPi.GPIO (from apt)"
echo "  ✓ mfrc522 (from pip)"
echo ""
echo "To run the jukebox:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the app: python jukebox_app.py"
echo ""
echo "See README.md for more details."
echo ""

