#!/bin/bash
# Lightweight setup script for Raspberry Pi Zero 2 W
# Installs dependencies one at a time to avoid overwhelming the system

echo "========================================="
echo "Jukebox Lite Setup (Pi Zero 2 W)"
echo "========================================="
echo ""
echo "This script is optimized for low-power devices"
echo "It will install packages slowly to avoid crashes"
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

# Function to install package with retry
install_package() {
    local package=$1
    echo "Installing $package..."
    sudo apt-get install -y "$package"
    if [ $? -eq 0 ]; then
        echo "  ✓ $package installed"
        sleep 2  # Brief pause between installations
        return 0
    else
        echo "  ✗ Failed to install $package"
        return 1
    fi
}

# Update package list (do this only once)
echo ""
echo "Updating package list..."
sudo apt-get update
echo "✓ Package list updated"
sleep 3

# Install system dependencies ONE AT A TIME
echo ""
echo "Installing system dependencies (this will take a while)..."
echo "Progress will be slow to prevent system overload"
echo ""

# Core Python packages
install_package "python3-dev"
install_package "python3-pip"
install_package "python3-setuptools"

# SDL2 packages (these are the heavy ones)
echo ""
echo "Installing SDL2 libraries (may take 5-10 minutes)..."
install_package "libsdl2-dev"
sleep 5
install_package "libsdl2-image-dev"
sleep 5
install_package "libsdl2-mixer-dev"
sleep 5
install_package "libsdl2-ttf-dev"
sleep 5

# Other dependencies
install_package "libfreetype6-dev"
install_package "libportmidi-dev"
install_package "libjpeg-dev"
install_package "zlib1g-dev"
install_package "libpng-dev"

# Additional Pillow dependencies
install_package "libtiff5-dev"
install_package "libopenjp2-7-dev"
install_package "liblcms2-dev"
install_package "libwebp-dev"

echo ""
echo "✓ System dependencies installed"

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

# Upgrade pip (slowly)
echo ""
echo "Upgrading pip..."
pip install --upgrade pip --no-cache-dir
sleep 5

# Install Python packages ONE AT A TIME
echo ""
echo "Installing Python packages..."
echo ""
echo "Installing pygame (this is the slowest - may take 20+ minutes)..."
echo "Please be patient, the Pi Zero 2 W is slow at compiling..."
pip install pygame==2.5.2 --no-cache-dir

if [ $? -ne 0 ]; then
    echo "❌ pygame installation failed!"
    echo "   pygame is required for the jukebox"
    exit 1
fi
echo "✓ pygame installed"
sleep 10

echo ""
echo "Installing mfrc522..."
pip install mfrc522==0.0.7 --no-cache-dir
sleep 5

echo "Installing spidev..."
pip install spidev==3.6 --no-cache-dir
sleep 5

echo "Installing RPi.GPIO..."
pip install RPi.GPIO==0.7.1 --no-cache-dir
sleep 5

echo ""
echo "✓ Python packages installed"

# Create music directory
echo ""
echo "Creating music directory structure..."
mkdir -p music
mkdir -p music/example_nfc_id/01_example_artist/01_example_album
echo "✓ Music directory created"

# Generate fallback album art
echo ""
echo "Generating fallback album art..."
python create_fallback_art.py

if [ $? -ne 0 ]; then
    echo "⚠ Fallback art generation failed (Pillow issue)"
    echo "  Creating simple fallback image instead..."
    # Create a simple black PNG as fallback
    if command -v convert &> /dev/null; then
        convert -size 600x600 xc:black -pointsize 40 -fill gray \
                -gravity center -annotate +0+0 "No Album Art" \
                fallback_albumart.png
        echo "✓ Created basic fallback image"
    else
        echo "  Skipping fallback art - will use solid color"
    fi
fi

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
echo "See README.md for more details."
echo ""

