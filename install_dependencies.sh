#!/bin/bash
# Install system dependencies for Raspberry Pi Jukebox
# Run this if setup.sh fails or you need to reinstall dependencies

echo "========================================="
echo "Installing System Dependencies"
echo "========================================="
echo ""
echo "This will install libraries required for:"
echo "  - Pygame (SDL2)"
echo "  - Pillow (image processing)"
echo "  - MFRC522 (SPI/GPIO)"
echo ""

# Update package list
echo "Updating package list..."
sudo apt-get update

echo ""
echo "Installing Python development packages..."
sudo apt-get install -y \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-venv

echo ""
echo "Installing SDL2 libraries (required for pygame)..."
sudo apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libportmidi-dev

echo ""
echo "Installing image processing libraries..."
sudo apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libtiff-dev

echo ""
echo "Installing SPI and GPIO libraries (for RFID)..."
sudo apt-get install -y \
    python3-spidev \
    python3-rpi.gpio

echo ""
echo "Installing audio libraries..."
sudo apt-get install -y \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev

echo ""
echo "========================================="
echo "System dependencies installed!"
echo "========================================="
echo ""
echo "Now you can install Python packages:"
echo "  source venv/bin/activate"
echo "  pip install -r requirements.txt"
echo ""
echo "Or run the full setup:"
echo "  ./setup.sh"
echo ""

