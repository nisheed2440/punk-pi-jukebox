#!/usr/bin/env python3
"""
Test script to verify jukebox installation
"""
import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing module imports...")
    
    tests = [
        ("tkinter", "Tkinter (GUI)"),
        ("pygame", "Pygame (Audio)"),
        ("PIL", "Pillow (Images)"),
    ]
    
    optional_tests = [
        ("mfrc522", "MFRC522 (RFID)"),
        ("RPi.GPIO", "RPi.GPIO"),
    ]
    
    passed = 0
    failed = 0
    
    for module, name in tests:
        try:
            __import__(module)
            print(f"  ✓ {name}")
            passed += 1
        except ImportError as e:
            print(f"  ✗ {name}: {e}")
            failed += 1
    
    print("\nOptional modules (for Raspberry Pi):")
    for module, name in optional_tests:
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ⚠ {name} (not available - this is OK on non-Pi systems)")
    
    return failed == 0


def test_project_structure():
    """Test if project structure is correct"""
    print("\n" + "="*50)
    print("Testing project structure...")
    
    required_files = [
        "jukebox_app.py",
        "rfid_reader.py",
        "music_library.py",
        "music_player.py",
        "config_manager.py",
        "requirements.txt",
        "setup.sh",
        "README.md",
        "fallback_albumart.png"
    ]
    
    required_dirs = [
        "music"
    ]
    
    passed = 0
    failed = 0
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
            passed += 1
        else:
            print(f"  ✗ {file} (missing)")
            failed += 1
    
    for dir in required_dirs:
        if os.path.isdir(dir):
            print(f"  ✓ {dir}/")
            passed += 1
        else:
            print(f"  ✗ {dir}/ (missing)")
            failed += 1
    
    return failed == 0


def test_music_library():
    """Test music library structure"""
    print("\n" + "="*50)
    print("Testing music library...")
    
    music_dir = "music"
    
    if not os.path.exists(music_dir):
        print("  ✗ Music directory not found")
        return False
    
    # Look for any NFC ID directories
    nfc_dirs = [d for d in os.listdir(music_dir) 
                if os.path.isdir(os.path.join(music_dir, d)) 
                and d != "__pycache__"]
    
    if not nfc_dirs:
        print(f"  ⚠ No music playlists found in {music_dir}/")
        print(f"    Add your music following this structure:")
        print(f"    {music_dir}/<nfc_id>/<seq>_artist/<seq>_album/<seq>_song.mp3")
        return True
    
    print(f"  ✓ Found {len(nfc_dirs)} playlist(s)")
    
    for nfc_id in nfc_dirs[:3]:  # Show first 3
        print(f"    - {nfc_id}")
        
        nfc_path = os.path.join(music_dir, nfc_id)
        artists = [d for d in os.listdir(nfc_path) 
                   if os.path.isdir(os.path.join(nfc_path, d))]
        
        if artists:
            print(f"      └─ {len(artists)} artist(s)")
    
    if len(nfc_dirs) > 3:
        print(f"    ... and {len(nfc_dirs) - 3} more")
    
    return True


def test_pygame():
    """Test pygame initialization"""
    print("\n" + "="*50)
    print("Testing pygame...")
    
    try:
        import pygame
        pygame.mixer.init()
        print("  ✓ Pygame mixer initialized")
        pygame.quit()
        return True
    except Exception as e:
        print(f"  ✗ Pygame test failed: {e}")
        return False


def test_config():
    """Test config file"""
    print("\n" + "="*50)
    print("Testing configuration...")
    
    if os.path.exists("config.json"):
        print("  ✓ config.json exists")
        
        try:
            import json
            with open("config.json", "r") as f:
                config = json.load(f)
            print(f"  ✓ Config loaded successfully")
            print(f"    - Music library: {config.get('music_library_path')}")
            print(f"    - Stop NFC ID: {config.get('stop_nfc_id', 'Not set')}")
            return True
        except Exception as e:
            print(f"  ✗ Error reading config: {e}")
            return False
    else:
        print("  ⚠ config.json not found (will be created on first run)")
        return True


def main():
    """Run all tests"""
    print("="*50)
    print("Jukebox Installation Test")
    print("="*50)
    print()
    
    # Check Python version
    print(f"Python version: {sys.version}")
    print()
    
    results = []
    
    results.append(("Module Imports", test_imports()))
    results.append(("Project Structure", test_project_structure()))
    results.append(("Music Library", test_music_library()))
    results.append(("Pygame", test_pygame()))
    results.append(("Configuration", test_config()))
    
    # Summary
    print("\n" + "="*50)
    print("Test Summary")
    print("="*50)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "="*50)
    if all_passed:
        print("✓ All tests passed!")
        print("\nYou can now run the jukebox:")
        print("  python jukebox_app.py")
    else:
        print("⚠ Some tests failed")
        print("\nPlease check the errors above and:")
        print("  1. Make sure you ran ./setup.sh")
        print("  2. Activate virtual environment: source venv/bin/activate")
        print("  3. Install dependencies: pip install -r requirements.txt")
    print("="*50)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

