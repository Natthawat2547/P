#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os
import random

# Create img directory
IMG_DIR = os.path.join(os.path.dirname(__file__), 'img')
os.makedirs(IMG_DIR, exist_ok=True)

# Colors for gradient
COLORS = [
    [(255, 107, 157), (196, 69, 105)],   # pink
    [(255, 165, 2), (255, 183, 3)],      # orange
    [(255, 0, 110), (214, 40, 40)],      # red
    [(251, 86, 7), (255, 0, 110)],       # hot
    [(131, 56, 236), (181, 23, 158)],    # purple
    [(58, 134, 255), (131, 56, 236)]     # blue
]

EMOJI_GALLERY = ['🎂', '🌹', '🎪', '🏖️', '🍽️', '🎭']
EMOJI_FACT = ['😊', '💕', '✨', '🌟', '👑', '🎀']

def create_gradient_image(width, height, color1, color2, emoji=None, number=None):
    """สร้างรูปที่มี gradient และ emoji หรือ number"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Draw gradient
    for y in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * y / height)
        g = int(color1[1] + (color2[1] - color1[1]) * y / height)
        b = int(color1[2] + (color2[2] - color1[2]) * y / height)
        draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b))
    
    # Add text (emoji or number) in center
    try:
        font = ImageFont.load_default()
        text = emoji if emoji else str(number)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        draw.text((x, y), text, fill='white', font=font)
    except:
        pass
    
    return img

# Create gallery images
print("สร้างรูป gallery...")
for i in range(6):
    color = COLORS[i]
    emoji = EMOJI_GALLERY[i]
    img = create_gradient_image(300, 300, color[0], color[1], emoji=emoji)
    filepath = os.path.join(IMG_DIR, f'gallery_{i}.png')
    img.save(filepath)
    print(f"✓ บันทึก gallery_{i}.png")

# Create fact images
print("\nสร้างรูป fact...")
for i in range(6):
    color = COLORS[i]
    number = i + 1
    # Reverse gradient สำหรับ fact
    img = create_gradient_image(300, 300, color[1], color[0], number=number)
    filepath = os.path.join(IMG_DIR, f'fact_{i}.png')
    img.save(filepath)
    print(f"✓ บันทึก fact_{i}.png")

print(f"\n✅ สร้างรูป 12 ชุดเสร็จ ใน {IMG_DIR}")
