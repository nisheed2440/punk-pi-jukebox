"""
RFID Reader Module for MFRC522
Handles NFC tag reading on Raspberry Pi
"""
import logging

logger = logging.getLogger(__name__)

try:
    from mfrc522 import SimpleMFRC522
    import RPi.GPIO as GPIO
    RFID_AVAILABLE = True
except ImportError:
    RFID_AVAILABLE = False
    logger.warning("RFID libraries not available. Running in mock mode.")


class RFIDReader:
    """Wrapper for MFRC522 RFID reader"""
    
    def __init__(self, mock_mode=False):
        """
        Initialize RFID reader
        
        Args:
            mock_mode: If True, use mock reader for testing without hardware
        """
        self.mock_mode = mock_mode or not RFID_AVAILABLE
        self.reader = None
        
        if not self.mock_mode:
            try:
                self.reader = SimpleMFRC522()
                logger.info("RFID reader initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize RFID reader: {e}")
                logger.info("Falling back to mock mode")
                self.mock_mode = True
    
    def read_id(self, timeout=None):
        """
        Read NFC tag ID
        
        Args:
            timeout: Optional timeout in seconds (not implemented for SimpleMFRC522)
            
        Returns:
            str: Tag ID as string, or None if no tag detected
        """
        if self.mock_mode:
            # Mock mode for testing without hardware
            logger.info("Mock mode: Simulating NFC read")
            return None
        
        try:
            id, text = self.reader.read_no_block()
            if id:
                tag_id = str(id)
                logger.info(f"NFC tag detected: {tag_id}")
                return tag_id
            return None
        except Exception as e:
            logger.error(f"Error reading NFC tag: {e}")
            return None
    
    def read_id_blocking(self):
        """
        Read NFC tag ID (blocking until tag is detected)
        
        Returns:
            str: Tag ID as string
        """
        if self.mock_mode:
            logger.info("Mock mode: Cannot block for NFC read")
            return "mock_tag_123456"
        
        try:
            id, text = self.reader.read()
            tag_id = str(id)
            logger.info(f"NFC tag detected (blocking): {tag_id}")
            return tag_id
        except Exception as e:
            logger.error(f"Error reading NFC tag: {e}")
            return None
    
    def cleanup(self):
        """Clean up GPIO resources"""
        if not self.mock_mode and RFID_AVAILABLE:
            try:
                GPIO.cleanup()
                logger.info("GPIO cleanup completed")
            except Exception as e:
                logger.error(f"Error during GPIO cleanup: {e}")

