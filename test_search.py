#!/usr/bin/env python3
"""
Test script for AI Image Search API
This script demonstrates how to interact with the main.py backend for testing search functionality.
"""

import requests
import json
import base64
import io
from PIL import Image, ImageDraw, ImageFont
import os

# Backend configuration
BACKEND_URL = "http://localhost:8000"

def create_test_image(text, color, size=(400, 400)):
    """Create a simple test image with text for testing purposes"""
    # Create a new image with specified color
    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a font, fall back to default if not available
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position to center it
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
    
    # Draw white text with black outline for better visibility
    outline_color = "black" if color != "black" else "white"
    text_color = "white" if color != "white" else "black"
    
    # Draw outline
    for dx in [-2, -1, 0, 1, 2]:
        for dy in [-2, -1, 0, 1, 2]:
            if dx != 0 or dy != 0:
                draw.text((position[0] + dx, position[1] + dy), text, font=font, fill=outline_color)
    
    # Draw main text
    draw.text(position, text, font=font, fill=text_color)
    
    return img

def save_image_as_bytes(img, format='JPEG'):
    """Convert PIL image to bytes"""
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=format, quality=95)
    return img_byte_arr.getvalue()

def test_backend_health():
    """Test if the backend is running and healthy"""
    print("🏥 Testing backend health...")
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend is healthy!")
            print(f"   - CLIP Model: {data['services']['clip_model']}")
            print(f"   - Firestore: {data['services']['firestore']}")
            print(f"   - Cloudinary: {data['services']['cloudinary']}")
            return True
        else:
            print(f"❌ Backend unhealthy: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False

def test_upload_image(image_bytes, filename, title, category):
    """Test uploading an image to the backend"""
    print(f"📤 Uploading test image: {filename}")
    try:
        files = {'image': (filename, image_bytes, 'image/jpeg')}
        data = {'title': title, 'category': category}
        
        response = requests.post(f"{BACKEND_URL}/upload", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Upload successful! ID: {result['data']['id']}")
            return result['data']['id']
        else:
            print(f"❌ Upload failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return None

def test_search_image(image_bytes, filename):
    """Test searching with an image"""
    print(f"🔍 Searching with image: {filename}")
    try:
        files = {'image': (filename, image_bytes, 'image/jpeg')}
        
        response = requests.post(f"{BACKEND_URL}/search", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Search successful!")
            
            if result['data']['results']:
                print(f"   Found {len(result['data']['results'])} similar images:")
                for i, match in enumerate(result['data']['results'], 1):
                    similarity = match['similarity_score'] * 100
                    title = match['metadata'].get('title', 'Untitled')
                    category = match['metadata'].get('category', 'No category')
                    print(f"   {i}. {title} ({category}) - {similarity:.1f}% similar")
            else:
                print("   No similar images found")
            
            return result
        else:
            print(f"❌ Search failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Search error: {e}")
        return None

def test_list_images():
    """Test listing all images in the database"""
    print("📋 Listing all images in database...")
    try:
        response = requests.get(f"{BACKEND_URL}/images")
        
        if response.status_code == 200:
            result = response.json()
            images = result['data']['images']
            total = result['data']['total']
            
            print(f"✅ Found {total} images in database:")
            for i, img in enumerate(images, 1):
                title = img['metadata'].get('title', 'Untitled')
                category = img['metadata'].get('category', 'No category')
                print(f"   {i}. {title} ({category}) - ID: {img['id'][:8]}...")
            
            return images
        else:
            print(f"❌ List failed: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"❌ List error: {e}")
        return []

def main():
    print("🧪 AI Image Search Test Suite")
    print("=" * 50)
    
    # Test 1: Check backend health
    if not test_backend_health():
        return
    
    print("\n" + "=" * 50)
    
    # Test 2: List current images
    current_images = test_list_images()
    
    print("\n" + "=" * 50)
    
    # Test 3: Create and upload test images
    print("🎨 Creating test product images...")
    
    test_products = [
        {"text": "Nike Sneakers", "color": "red", "title": "Nike Air Max", "category": "shoes"},
        {"text": "Apple Watch", "color": "blue", "title": "Apple Watch Series 9", "category": "watches"},
        {"text": "Denim Jacket", "color": "darkblue", "title": "Levi's Denim Jacket", "category": "clothing"},
        {"text": "Leather Bag", "color": "brown", "title": "Luxury Leather Handbag", "category": "accessories"},
        {"text": "Running Shoes", "color": "green", "title": "Adidas Ultraboost", "category": "shoes"},
    ]
    
    uploaded_ids = []
    for product in test_products:
        # Create test image
        img = create_test_image(product["text"], product["color"])
        img_bytes = save_image_as_bytes(img)
        filename = f"{product['text'].lower().replace(' ', '_')}.jpg"
        
        # Upload to backend
        image_id = test_upload_image(img_bytes, filename, product["title"], product["category"])
        if image_id:
            uploaded_ids.append(image_id)
    
    print(f"\n✅ Uploaded {len(uploaded_ids)} test images!")
    
    print("\n" + "=" * 50)
    
    # Test 4: Search with similar images
    print("🔍 Testing search functionality...")
    
    # Create a search image similar to one we uploaded
    search_img = create_test_image("Athletic Shoes", "red")  # Similar to Nike Sneakers
    search_bytes = save_image_as_bytes(search_img)
    
    result = test_search_image(search_bytes, "search_shoes.jpg")
    
    print("\n" + "=" * 50)
    
    # Test 5: Search with different category
    print("🔍 Testing cross-category search...")
    
    # Create a watch-like search image
    watch_img = create_test_image("Smart Watch", "blue")  # Similar to Apple Watch
    watch_bytes = save_image_as_bytes(watch_img)
    
    result2 = test_search_image(watch_bytes, "search_watch.jpg")
    
    print("\n" + "=" * 50)
    
    # Test 6: Final database state
    print("📊 Final database state:")
    final_images = test_list_images()
    
    print(f"\n🎉 Test complete! Database now has {len(final_images)} images.")
    print("\n💡 Your Flutter app should now return relevant results!")
    print("   Try uploading a red shoe image - it should match the Nike Sneakers")
    print("   Try uploading a blue watch image - it should match the Apple Watch")

if __name__ == "__main__":
    # Check if PIL is available
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("❌ PIL (Pillow) not installed. Installing...")
        import subprocess
        subprocess.check_call(["pip3", "install", "pillow"])
        from PIL import Image, ImageDraw, ImageFont
    
    main()
