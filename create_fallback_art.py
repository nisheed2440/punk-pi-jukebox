"""
Script to create fallback album art
"""
from PIL import Image, ImageDraw, ImageFont

# Create a simple gradient image
img = Image.new('RGB', (600, 600), color='#1a1a1a')
draw = ImageDraw.Draw(img)

# Draw a music note symbol
draw.ellipse([200, 250, 400, 450], fill='#333333', outline='#666666', width=3)
draw.rectangle([350, 200, 390, 370], fill='#333333', outline='#666666', width=3)
draw.ellipse([330, 170, 410, 220], fill='#333333', outline='#666666', width=3)

# Add text
try:
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
except:
    font = ImageFont.load_default()

text = "No Album Art"
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
text_x = (600 - text_width) // 2
text_y = 500

draw.text((text_x, text_y), text, fill='#666666', font=font)

# Save
img.save('fallback_albumart.png')
print("Fallback album art created: fallback_albumart.png")

