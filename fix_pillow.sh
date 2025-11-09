#!/bin/bash
# Quick fix for Pillow installation issues on Pi Zero 2 W

echo "========================================="
echo "Pillow Installation Fix"
echo "========================================="
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run ./setup_lite.sh first"
    exit 1
fi

echo "Installing additional image library dependencies..."
sudo apt-get update
sudo apt-get install -y \
    python3-pil \
    libjpeg-dev \
    libpng-dev \
    libtiff5-dev \
    libopenjp2-7-dev \
    liblcms2-dev \
    libwebp-dev \
    libharfbuzz-dev \
    libfribidi-dev

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Attempting to install Pillow..."

# Try latest version
echo "Trying Pillow 10.1.0..."
pip install --no-cache-dir pillow==10.1.0

if [ $? -eq 0 ]; then
    echo "✓ Pillow 10.1.0 installed successfully!"
else
    echo "Failed, trying older version..."
    
    # Try older version
    echo "Trying Pillow 9.5.0..."
    pip install --no-cache-dir pillow==9.5.0
    
    if [ $? -eq 0 ]; then
        echo "✓ Pillow 9.5.0 installed successfully!"
    else
        echo "Failed, trying system package approach..."
        
        # Use system package with venv
        deactivate
        rm -rf venv
        python3 -m venv --system-site-packages venv
        source venv/bin/activate
        
        echo "✓ Using system Pillow package"
    fi
fi

echo ""
echo "Testing Pillow installation..."
python3 -c "from PIL import Image; print('✓ Pillow is working! Version:', Image.__version__)"

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================="
    echo "✅ Pillow is now working!"
    echo "========================================="
    echo ""
    echo "Generating fallback album art..."
    python create_fallback_art.py
    
    if [ $? -eq 0 ]; then
        echo "✓ Fallback album art created"
    else
        echo "Creating simple fallback..."
        # Create a simple black file as fallback
        python3 << 'PYEOF'
from PIL import Image, ImageDraw

img = Image.new('RGB', (600, 600), color='#1a1a1a')
draw = ImageDraw.Draw(img)
draw.rectangle([150, 250, 450, 350], fill='#333333', outline='#666666', width=3)
img.save('fallback_albumart.png')
print("✓ Simple fallback created")
PYEOF
    fi
    
    echo ""
    echo "You can now continue with setup or run the app!"
else
    echo ""
    echo "========================================="
    echo "❌ Pillow installation failed"
    echo "========================================="
    echo ""
    echo "This is likely due to:"
    echo "1. Insufficient power supply"
    echo "2. Low memory"
    echo "3. Build tools missing"
    echo ""
    echo "Try:"
    echo "1. Check power: vcgencmd get_throttled"
    echo "2. Increase swap space (see POWER_ISSUES.md)"
    echo "3. Reboot and try again"
    exit 1
fi

