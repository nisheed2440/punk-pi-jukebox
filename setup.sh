#!/bin/bash
# Setup script for Jukebox app

echo "========================================="
echo "Jukebox Setup Script"
echo "========================================="
echo ""

# Check if running on Raspberry Pi
if [ -f /sys/firmware/devicetree/base/model ]; then
    echo "✓ Running on Raspberry Pi"
    IS_RPI=true
else
    echo "⚠ Not running on Raspberry Pi - some features may not work"
    IS_RPI=false
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "✗ Failed to create virtual environment"
    exit 1
fi

echo "✓ Virtual environment created"

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "✗ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"

# Create music directory
echo ""
echo "Creating music directory structure..."
mkdir -p music

# Create example playlist structure
mkdir -p music/example_nfc_id/01_example_artist/01_example_album
echo "✓ Example music directory created at: music/example_nfc_id/"

# Generate fallback album art
echo ""
echo "Generating fallback album art..."
python create_fallback_art.py

# Create initial config
echo ""
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

# Check SPI on Raspberry Pi
if [ "$IS_RPI" = true ]; then
    echo ""
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
echo "To run the jukebox:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the app: python jukebox_app.py"
echo ""
echo "Add your music to the 'music' folder following the structure:"
echo "  music/<NFC_ID>/<seq>_<artist>/<seq>_<album>/<seq>_<song>.mp3"
echo ""
echo "See README.md for more details."
echo ""

