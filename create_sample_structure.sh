#!/bin/bash
# Create sample music directory structure for testing

echo "Creating sample music directory structure..."
echo ""

# Sample NFC ID
NFC_ID="sample_123456"

# Create directory structure
mkdir -p "music/${NFC_ID}/01_sample_artist/01_sample_album"
mkdir -p "music/${NFC_ID}/02_another_artist/01_first_album"
mkdir -p "music/${NFC_ID}/02_another_artist/02_second_album"

echo "✓ Created directory structure"

# Create README files in each album
cat > "music/${NFC_ID}/01_sample_artist/01_sample_album/README.txt" << EOF
Sample Album Structure

Add your MP3 files here with this naming pattern:
- 01_song_name.mp3
- 02_another_song.mp3
- 03_third_song.mp3
etc.

Also add an albumart.png file (600x600px or larger recommended).
EOF

cat > "music/${NFC_ID}/02_another_artist/01_first_album/README.txt" << EOF
Add your music files here following the naming convention:
<seq>_<song_name>.mp3

Example:
- 01_robot_rock.mp3
- 02_technologic.mp3

Don't forget albumart.png!
EOF

cat > "music/${NFC_ID}/02_another_artist/02_second_album/README.txt" << EOF
Album folder structure:
- albumart.png (required for album art display)
- 01_song_one.mp3
- 02_song_two.mp3
- etc.
EOF

echo "✓ Created README files in albums"

# Create a sample tree structure document
cat > "music/${NFC_ID}/STRUCTURE.txt" << EOF
Music Library Structure for NFC ID: ${NFC_ID}

${NFC_ID}/
├── 01_sample_artist/
│   └── 01_sample_album/
│       ├── albumart.png (add your album art here)
│       ├── 01_song_name.mp3 (add your songs)
│       ├── 02_another_song.mp3
│       └── ...
│
└── 02_another_artist/
    ├── 01_first_album/
    │   ├── albumart.png
    │   └── songs...
    │
    └── 02_second_album/
        ├── albumart.png
        └── songs...

To use this playlist:
1. Add your MP3 files following the naming convention
2. Add albumart.png in each album folder
3. Get your actual NFC tag ID by running the app in "Read NFC Mode"
4. Rename this folder from "sample_123456" to your actual NFC tag ID
5. Tap the NFC tag to play!
EOF

echo "✓ Created structure documentation"
echo ""
echo "Sample structure created at: music/${NFC_ID}/"
echo ""
echo "Next steps:"
echo "  1. Add your MP3 files to the album folders"
echo "  2. Add albumart.png files (600x600px+ recommended)"
echo "  3. Use 'Read NFC Mode' to get your actual NFC tag ID"
echo "  4. Rename the folder to match your NFC tag ID"
echo "  5. Rescan the library in the app"
echo ""
echo "Example file names:"
echo "  - 01_robot_rock.mp3"
echo "  - 02_around_the_world.mp3"
echo "  - 03_harder_better_faster_stronger.mp3"
echo ""

