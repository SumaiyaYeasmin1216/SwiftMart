#!/usr/bin/env python3
"""
Script to populate the image search database with actual product images.

This script helps you add real product images to your database so that
the AI image search can find relevant matches when users upload photos.
"""

import requests
import json
import os
from pathlib import Path

# Backend URL
BACKEND_URL = "http://localhost:8000"

def upload_image(image_path, title=None, category=None):
    """Upload a single image to the database"""
    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            files = {'image': (os.path.basename(image_path), f, 'image/jpeg')}
            data = {}
            if title:
                data['title'] = title
            if category:
                data['category'] = category
            
            response = requests.post(f"{BACKEND_URL}/upload", files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Uploaded: {os.path.basename(image_path)} -> ID: {result['data']['image_id']}")
                return True
            else:
                print(f"❌ Failed to upload {image_path}: {response.text}")
                return False
    except Exception as e:
        print(f"❌ Error uploading {image_path}: {e}")
        return False

def main():
    print("🚀 Product Image Database Populator")
    print("=" * 50)
    
    # Check if backend is running
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        if response.status_code != 200:
            print("❌ Backend not responding. Make sure it's running on http://localhost:8000")
            return
    except Exception:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:8000")
        return
    
    print("✅ Backend is running!")
    
    # Look for product images in common directories
    image_dirs = [
        Path("assets/products"),
        Path("assets/images"), 
        Path("lib/assets/products"),
        Path("lib/assets/images"),
        Path("products"),
        Path("images")
    ]
    
    found_images = []
    for img_dir in image_dirs:
        if img_dir.exists():
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.webp']:
                found_images.extend(img_dir.glob(ext))
    
    if not found_images:
        print("\n📁 No product images found in standard directories.")
        print("\n💡 To add product images:")
        print("1. Create a 'products' folder in this directory")
        print("2. Add your product images (sneakers, watches, clothes, etc.)")
        print("3. Run this script again")
        print("\nOr manually upload images using:")
        print(f"curl -X POST {BACKEND_URL}/upload -F 'image=@your_image.jpg' -F 'title=Product Name' -F 'category=sneakers'")
        return
    
    print(f"\n📸 Found {len(found_images)} images to upload:")
    
    uploaded = 0
    for img_path in found_images:
        # Try to guess category and title from filename
        filename = img_path.stem
        category = None
        title = filename.replace('_', ' ').replace('-', ' ').title()
        
        # Simple category detection based on filename
        filename_lower = filename.lower()
        if any(word in filename_lower for word in ['sneaker', 'shoe', 'nike', 'adidas', 'boot']):
            category = 'shoes'
        elif any(word in filename_lower for word in ['watch', 'rolex', 'time', 'clock']):
            category = 'watches' 
        elif any(word in filename_lower for word in ['shirt', 'tshirt', 't-shirt', 'hoodie', 'jacket']):
            category = 'clothing'
        elif any(word in filename_lower for word in ['bag', 'backpack', 'purse', 'wallet']):
            category = 'accessories'
        
        if upload_image(str(img_path), title, category):
            uploaded += 1
    
    print(f"\n🎉 Successfully uploaded {uploaded} images!")
    
    # Show current database status
    try:
        response = requests.get(f"{BACKEND_URL}/images")
        if response.status_code == 200:
            data = response.json()
            total = data['data']['total']
            print(f"📊 Database now contains {total} images total")
        
    except Exception:
        print("📊 Could not retrieve database statistics")

if __name__ == "__main__":
    main()
