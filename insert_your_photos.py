#!/usr/bin/env python3
import os
import random
from PIL import Image
import shutil

IMG_DIR = os.path.join(os.path.dirname(__file__), 'img')

# Get all JPG files in img directory
jpg_files = [f for f in os.listdir(IMG_DIR) if f.lower().endswith(('.jpg', '.jpeg'))]

print(f"พบรูป {len(jpg_files)} ชุด: {jpg_files}")

if len(jpg_files) < 12:
    print(f"⚠️ มีแค่ {len(jpg_files)} รูป ต้องการ 12 รูป")
    # สุ่มได้ทั้งในจำนวนที่มี
    needed = 12
else:
    needed = 12
    # สุ่มเลือก 12 รูป
    selected = random.sample(jpg_files, min(12, len(jpg_files)))
    jpg_files = selected

# Delete old gallery and fact PNG files
for i in range(6):
    for prefix in ['gallery', 'fact']:
        old_file = os.path.join(IMG_DIR, f'{prefix}_{i}.png')
        if os.path.exists(old_file):
            os.remove(old_file)
            print(f"ลบ {prefix}_{i}.png")

# Resize JPG files to gallery/fact format
print("\nสุ่มใส่รูป...")

# Create gallery images
for i in range(6):
    if i < len(jpg_files):
        src_file = os.path.join(IMG_DIR, jpg_files[i])
    else:
        # ถ้าไม่มีรูปพอ ให้เลือกซ้ำแบบสุ่ม
        src_file = os.path.join(IMG_DIR, random.choice(jpg_files))
    
    try:
        img = Image.open(src_file)
        # Resize to 300x300
        img = img.resize((300, 300), Image.Resampling.LANCZOS)
        dst_file = os.path.join(IMG_DIR, f'gallery_{i}.png')
        img.save(dst_file, 'PNG')
        print(f"✓ gallery_{i}.png ← {os.path.basename(src_file)}")
    except Exception as e:
        print(f"❌ ผิดพลาด gallery_{i}: {e}")

# Create fact images
for i in range(6):
    if (i + 6) < len(jpg_files):
        src_file = os.path.join(IMG_DIR, jpg_files[i + 6])
    else:
        # ถ้าไม่มีรูปพอ ให้เลือกซ้ำแบบสุ่ม
        src_file = os.path.join(IMG_DIR, random.choice(jpg_files))
    
    try:
        img = Image.open(src_file)
        # Resize to 300x300
        img = img.resize((300, 300), Image.Resampling.LANCZOS)
        dst_file = os.path.join(IMG_DIR, f'fact_{i}.png')
        img.save(dst_file, 'PNG')
        print(f"✓ fact_{i}.png ← {os.path.basename(src_file)}")
    except Exception as e:
        print(f"❌ ผิดพลาด fact_{i}: {e}")

print("\n✅ สุ่มใส่รูปเสร็จ! ลองเปิด http://127.0.0.1:8000 ดูนะ 💕")
