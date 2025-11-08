#!/bin/bash
# Diagnostic script for Raspberry Pi health check
# Helps identify power, temperature, and system issues

echo "========================================="
echo "Raspberry Pi Health Check"
echo "========================================="
echo ""

# Check if on Raspberry Pi
if [ ! -f /sys/firmware/devicetree/base/model ]; then
    echo "❌ Not running on a Raspberry Pi"
    exit 1
fi

# Show Pi model
echo "📱 Device Information:"
cat /sys/firmware/devicetree/base/model
echo ""
echo ""

# Check temperature
echo "🌡️  Temperature:"
TEMP=$(vcgencmd measure_temp | cut -d= -f2)
TEMP_NUM=$(echo $TEMP | cut -d"'" -f1)
echo "  Current: $TEMP"
if (( $(echo "$TEMP_NUM > 70" | bc -l) )); then
    echo "  ⚠️  WARNING: Temperature is high! Add cooling."
elif (( $(echo "$TEMP_NUM > 80" | bc -l) )); then
    echo "  ❌ CRITICAL: Temperature too high! System will throttle!"
else
    echo "  ✅ Temperature is good"
fi
echo ""

# Check voltage/throttling (MOST IMPORTANT)
echo "⚡ Power Supply Status:"
THROTTLED=$(vcgencmd get_throttled)
echo "  Raw status: $THROTTLED"
echo ""

THROTTLE_HEX=$(echo $THROTTLED | cut -d= -f2)

if [ "$THROTTLE_HEX" = "0x0" ]; then
    echo "  ✅ Power supply is good - no issues detected"
else
    echo "  ❌ POWER ISSUES DETECTED!"
    echo ""
    echo "  Throttle flags: $THROTTLE_HEX"
    echo ""
    echo "  Meaning:"
    
    # Decode throttle bits
    case $THROTTLE_HEX in
        *"50000"*|*"50005"*)
            echo "  - Undervoltage detected (bit 16)"
            echo "  - System was throttled due to low voltage"
            ;;
        *"50001"*)
            echo "  - Currently under-voltage!"
            ;;
        *"20000"*|*"20002"*)
            echo "  - ARM frequency capped occurred"
            ;;
        *"40000"*|*"40004"*)
            echo "  - Throttling occurred"
            ;;
    esac
    
    echo ""
    echo "  🔧 FIX: Use official Raspberry Pi 5V 3A power supply!"
    echo "      Current supply is insufficient."
fi
echo ""

# Check CPU frequency
echo "⚡ CPU Status:"
FREQ=$(vcgencmd measure_clock arm | cut -d= -f2)
FREQ_MHZ=$((FREQ / 1000000))
echo "  Current frequency: ${FREQ_MHZ} MHz"

if [ "$FREQ_MHZ" -lt 800 ]; then
    echo "  ⚠️  CPU is throttled (should be 1000 MHz for Pi Zero 2 W)"
else
    echo "  ✅ CPU running at normal speed"
fi
echo ""

# Check memory
echo "💾 Memory Status:"
free -h
echo ""

AVAILABLE=$(free -m | awk 'NR==2{print $7}')
if [ "$AVAILABLE" -lt 100 ]; then
    echo "  ⚠️  Low memory available (${AVAILABLE}MB)"
    echo "     Consider increasing swap space"
else
    echo "  ✅ Memory looks okay"
fi
echo ""

# Check swap
echo "💿 Swap Space:"
SWAP=$(free -m | awk 'NR==3{print $2}')
echo "  Total swap: ${SWAP}MB"
if [ "$SWAP" -lt 512 ]; then
    echo "  ⚠️  Swap is small - recommend 1024MB for Pi Zero 2 W"
    echo ""
    echo "  To increase swap:"
    echo "    sudo dphys-swapfile swapoff"
    echo "    sudo nano /etc/dphys-swapfile"
    echo "    # Change CONF_SWAPSIZE=100 to CONF_SWAPSIZE=1024"
    echo "    sudo dphys-swapfile setup"
    echo "    sudo dphys-swapfile swapon"
else
    echo "  ✅ Swap space is adequate"
fi
echo ""

# Check disk space
echo "💽 Disk Space:"
df -h /
echo ""

AVAILABLE_GB=$(df -BG / | awk 'NR==2{print $4}' | sed 's/G//')
if [ "$AVAILABLE_GB" -lt 2 ]; then
    echo "  ⚠️  Low disk space (${AVAILABLE_GB}GB available)"
    echo "     Need at least 2GB free for installation"
else
    echo "  ✅ Disk space is adequate"
fi
echo ""

# Check if SPI is enabled
echo "📡 SPI Status (for RFID):"
if lsmod | grep -q spi_bcm2835; then
    echo "  ✅ SPI is enabled"
else
    echo "  ❌ SPI is NOT enabled"
    echo "     Enable with: sudo raspi-config"
    echo "     Navigate to: Interface Options -> SPI -> Enable"
fi
echo ""

# System load
echo "📊 System Load:"
uptime
echo ""

LOAD=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
if (( $(echo "$LOAD > 2.0" | bc -l) )); then
    echo "  ⚠️  System is under heavy load"
else
    echo "  ✅ System load is normal"
fi
echo ""

# Summary and recommendations
echo "========================================="
echo "📋 Summary and Recommendations"
echo "========================================="
echo ""

# Check for critical issues
CRITICAL=0
if [ "$THROTTLE_HEX" != "0x0" ]; then
    echo "❌ CRITICAL: Fix power supply first!"
    echo "   Use official Raspberry Pi 5V 3A power supply"
    echo "   Short, thick USB cable (not thin charging cables)"
    echo ""
    CRITICAL=1
fi

if (( $(echo "$TEMP_NUM > 75" | bc -l) )); then
    echo "⚠️  WARNING: High temperature detected"
    echo "   Add heatsink or small fan"
    echo "   Ensure good ventilation"
    echo ""
    CRITICAL=1
fi

if [ "$AVAILABLE" -lt 100 ]; then
    echo "⚠️  WARNING: Low memory"
    echo "   Close unnecessary programs"
    echo "   Consider increasing swap space"
    echo ""
fi

if [ "$CRITICAL" -eq 0 ]; then
    echo "✅ System looks healthy!"
    echo ""
    echo "Safe to proceed with installation."
    echo "Use: ./setup_lite.sh"
else
    echo "⚠️  Fix issues above before running setup"
    echo ""
    echo "Most common fix: Better power supply!"
fi
echo ""

echo "For detailed help, see: POWER_ISSUES.md"
echo "========================================="

