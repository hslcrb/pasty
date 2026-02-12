#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create Frutiger Aero background assets
"""
from PIL import Image, ImageDraw
import os

def create_frutiger_background():
    """Create a Frutiger Aero style gradient background"""
    os.makedirs("assets", exist_ok=True)
    
    # Create 1920x1080 background
    width, height = 1920, 1080
    img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(img)
    
    # Frutiger Aero style gradient (sky blue to white)
    for y in range(height):
        ratio = y / height
        # Sky blue to light blue gradient
        r = int(135 + (255 - 135) * ratio)
        g = int(206 + (255 - 206) * ratio)  
        b = int(250 + (255 - 250) * ratio * 0.5)
        a = int(255 * 0.7)  # 70% opacity
        color = (r, g, b, a)
        draw.line([(0, y), (width, y)], fill=color)
    
    img.save("assets/background.png", "PNG")
    print("Created Frutiger Aero background")

def create_app_icon():
    """Create a simple Pasty icon"""
    os.makedirs("assets", exist_ok=True)
    
    # Create 256x256 icon
    size = 256
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Blue circle with white "P"
    draw.ellipse([10, 10, size-10, size-10], fill=(70, 130, 180, 255))
    
    # Simple "P" (approximation with rectangles)
    # Vertical bar
    draw.rectangle([80, 60, 110, 200], fill=(255, 255, 255, 255))
    # Top arc
    draw.ellipse([100, 60, 180, 140], fill=(255, 255, 255, 255))
    draw.ellipse([115, 75, 165, 125], fill=(70, 130, 180, 255))
    
    # Save as PNG and ICO
    img.save("assets/icon.png", "PNG")
    
    # Create ICO with multiple sizes
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    icons = [img.resize(s, Image.Resampling.LANCZOS) for s in sizes]
    icons[0].save("assets/icon.ico", format="ICO", sizes=[(i.width, i.height) for i in icons])
    
    print("Created app icon")

if __name__ == "__main__":
    create_frutiger_background()
    create_app_icon()
