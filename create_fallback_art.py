"""
Script to create fallback album art using pygame
"""
import sys

try:
    import pygame
    
    print("Creating fallback album art with pygame...")
    pygame.init()
    
    # Create surface
    surface = pygame.Surface((600, 600))
    surface.fill((26, 26, 26))  # Dark background #1a1a1a
    
    # Draw music note shape
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

except ImportError:
    print("❌ pygame not installed yet")
    print("   Run setup script first, or manually install: pip install pygame")
    sys.exit(1)

except Exception as e:
    print(f"❌ Error creating fallback art: {e}")
    print("   The app will work without it - just won't show default album art")
    print("   Add albumart.png files to your music album folders instead")
    sys.exit(1)

