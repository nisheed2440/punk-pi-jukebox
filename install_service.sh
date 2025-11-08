#!/bin/bash
# Install systemd service for auto-start

SERVICE_FILE="jukebox.service"
SERVICE_PATH="/etc/systemd/system/$SERVICE_FILE"

echo "Installing Jukebox systemd service..."

# Check if service file exists
if [ ! -f "jukebox.service.example" ]; then
    echo "Error: jukebox.service.example not found"
    exit 1
fi

# Update paths in service file based on current directory
CURRENT_DIR=$(pwd)
sed "s|/home/pi/jukebox|$CURRENT_DIR|g" jukebox.service.example > /tmp/jukebox.service

# Update user if not pi
CURRENT_USER=$(whoami)
sed -i.bak "s|User=pi|User=$CURRENT_USER|g" /tmp/jukebox.service

# Copy to systemd
echo "Installing service file to $SERVICE_PATH"
sudo cp /tmp/jukebox.service $SERVICE_PATH

# Set permissions
sudo chmod 644 $SERVICE_PATH

# Reload systemd
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Enable service
echo "Enabling jukebox service..."
sudo systemctl enable jukebox.service

echo ""
echo "Service installed successfully!"
echo ""
echo "Commands:"
echo "  Start:   sudo systemctl start jukebox.service"
echo "  Stop:    sudo systemctl stop jukebox.service"
echo "  Status:  sudo systemctl status jukebox.service"
echo "  Logs:    journalctl -u jukebox.service -f"
echo ""
echo "To start on next boot: Service is already enabled"
echo "To start now: sudo systemctl start jukebox.service"
echo ""

# Clean up
rm /tmp/jukebox.service /tmp/jukebox.service.bak 2>/dev/null

