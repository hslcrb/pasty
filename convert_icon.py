#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Process user's icon to ICO format
"""
from PIL import Image
import os

def process_user_icon():
    """Convert user's icon to ICO with multiple sizes"""
    icon_path = "assets/icon_source.png"
    output_ico = "assets/icon.ico"
    
    if not os.path.exists(icon_path):
        print(f"Icon not found: {icon_path}")
        return
    
    # Load image
    img = Image.open(icon_path).convert("RGBA")
    
    # Create multiple sizes for ICO
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    icons = []
    for size in sizes:
        resized = img.resize(size, Image.Resampling.LANCZOS)
        icons.append(resized)
    
    # Save as ICO
    icons[0].save(output_ico, format="ICO", sizes=[(icon.width, icon.height) for icon in icons])
    print(f"User icon saved as: {output_ico}")
    
    # Also save PNG version
    img.save("assets/icon.png", "PNG")
    print("Icon PNG saved")

if __name__ == "__main__":
    process_user_icon()
