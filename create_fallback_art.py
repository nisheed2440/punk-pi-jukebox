"""
Script to create fallback album art
Tries multiple methods from heavyweight to lightweight
"""
import sys

# Method 1: Try PIL/Pillow (if available)
try:
    from PIL import Image, ImageDraw, ImageFont
    
    print("Using PIL/Pillow to create fallback art...")
    img = Image.new('RGB', (600, 600), color='#1a1a1a')
    draw = ImageDraw.Draw(img)
    
    # Draw a music note symbol
    draw.ellipse([200, 250, 400, 450], fill='#333333', outline='#666666', width=3)
    draw.rectangle([350, 200, 390, 370], fill='#333333', outline='#666666', width=3)
    draw.ellipse([330, 170, 410, 220], fill='#333333', outline='#666666', width=3)
    
    # Add text
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    text = "No Album Art"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (600 - text_width) // 2
    text_y = 500
    
    draw.text((text_x, text_y), text, fill='#666666', font=font)
    img.save('fallback_albumart.png')
    print("✓ Fallback album art created: fallback_albumart.png")
    sys.exit(0)

except ImportError:
    print("PIL/Pillow not available, trying alternative methods...")

# Method 2: Try using pygame (already a dependency)
try:
    import pygame
    
    print("Using pygame to create fallback art...")
    pygame.init()
    
    # Create surface
    surface = pygame.Surface((600, 600))
    surface.fill((26, 26, 26))  # #1a1a1a
    
    # Draw music note shape (simplified)
    pygame.draw.circle(surface, (51, 51, 51), (300, 350), 100, 3)
    pygame.draw.rect(surface, (51, 51, 51), (370, 200, 40, 170), 3)
    pygame.draw.circle(surface, (51, 51, 51), (370, 195), 40, 3)
    
    # Add text
    font = pygame.font.Font(None, 48)
    text = font.render("No Album Art", True, (102, 102, 102))
    text_rect = text.get_rect(center=(300, 520))
    surface.blit(text, text_rect)
    
    # Save
    pygame.image.save(surface, 'fallback_albumart.png')
    pygame.quit()
    
    print("✓ Fallback album art created: fallback_albumart.png")
    sys.exit(0)

except Exception as e:
    print(f"pygame method failed: {e}")

# Method 3: Create a minimal PNG manually (no dependencies!)
try:
    import struct
    import zlib
    
    print("Creating minimal PNG without external libraries...")
    
    # Create a simple 600x600 dark gray PNG
    width, height = 600, 600
    
    def create_minimal_png():
        # PNG signature
        png_signature = b'\x89PNG\r\n\x1a\n'
        
        # IHDR chunk
        ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
        ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data)
        ihdr = struct.pack('>I', len(ihdr_data)) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)
        
        # IDAT chunk - image data (dark gray pixels)
        raw_data = b''
        for y in range(height):
            raw_data += b'\x00'  # Filter type
            for x in range(width):
                raw_data += b'\x1a\x1a\x1a'  # RGB #1a1a1a
        
        compressed_data = zlib.compress(raw_data, 9)
        idat_crc = zlib.crc32(b'IDAT' + compressed_data)
        idat = struct.pack('>I', len(compressed_data)) + b'IDAT' + compressed_data + struct.pack('>I', idat_crc)
        
        # IEND chunk
        iend_crc = zlib.crc32(b'IEND')
        iend = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)
        
        return png_signature + ihdr + idat + iend
    
    with open('fallback_albumart.png', 'wb') as f:
        f.write(create_minimal_png())
    
    print("✓ Minimal fallback PNG created (no dependencies)")
    sys.exit(0)

except Exception as e:
    print(f"Minimal PNG creation failed: {e}")

# Method 4: Last resort - just create a dummy file or skip
print("⚠️  Could not create fallback image")
print("   The app will work without it - just won't show default album art")
print("   Add albumart.png files to your music album folders instead")
sys.exit(1)

