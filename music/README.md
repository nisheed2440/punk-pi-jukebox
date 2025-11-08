# Music Library

Place your music files here following this structure:

```
music/
├── <NFC_ID>/
│   ├── <seq>_<artist_name>/
│   │   ├── <seq>_<album_name>/
│   │   │   ├── albumart.png
│   │   │   ├── <seq>_<song_name>.mp3
│   │   │   └── ...
│   │   └── ...
│   └── ...
└── ...
```

## Example Structure

```
music/
├── 123456789/
│   ├── 01_daft_punk/
│   │   ├── 01_discovery/
│   │   │   ├── albumart.png
│   │   │   ├── 01_one_more_time.mp3
│   │   │   ├── 02_aerodynamic.mp3
│   │   │   └── 03_digital_love.mp3
│   │   └── 02_random_access_memories/
│   │       ├── albumart.png
│   │       └── 01_get_lucky.mp3
│   └── 02_justice/
│       └── 01_cross/
│           ├── albumart.png
│           └── 01_genesis.mp3
└── 987654321/
    └── 01_queen/
        └── 01_greatest_hits/
            ├── albumart.png
            ├── 01_bohemian_rhapsody.mp3
            └── 02_we_will_rock_you.mp3
```

## Naming Rules

1. **NFC ID folders**: Use the exact NFC tag ID (numbers)
2. **Artist folders**: `<seq>_<artist_name_in_lowercase_with_underscores>`
   - Example: `01_daft_punk`, `02_justice`
3. **Album folders**: `<seq>_<album_name_in_lowercase_with_underscores>`
   - Example: `01_discovery`, `02_random_access_memories`
4. **Song files**: `<seq>_<song_name_in_lowercase_with_underscores>.mp3`
   - Example: `01_one_more_time.mp3`, `02_aerodynamic.mp3`
5. **Album art**: Must be named exactly `albumart.png` in each album folder

## Getting NFC IDs

1. Run the jukebox app
2. Click the ⚙️ debug icon
3. Click "Read NFC Mode"
4. Tap your NFC tag
5. The ID will be displayed - use this as your folder name

## Tips

- Use leading zeros in sequence numbers for proper sorting (01, 02, 03, etc.)
- Keep names in lowercase with underscores replacing spaces
- Supported formats: MP3, WAV, OGG, FLAC, M4A
- Album art should be PNG format, recommended size: 600x600px or larger
- One NFC tag can have multiple artists, albums, and songs

