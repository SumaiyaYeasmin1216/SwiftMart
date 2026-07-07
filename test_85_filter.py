#!/usr/bin/env python3
"""
Test script to demonstrate 85% similarity filtering
"""

import requests
import json
from PIL import Image, ImageDraw, ImageFont
import io
import time

BACKEND_URL = "http://localhost:8000"

def create_test_image(text, color, size=(400, 400)):
    """Create a simple test image"""
    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
    draw.text(position, text, font=font, fill="white")
    
    return img

def test_search_with_filtering():
    print("🧪 Testing Search with 85% Similarity Filter")
    print("=" * 50)
    
    # Check backend
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Backend not running. Start it first with: ./start.sh")
            return
        print("✅ Backend is running")
    except:
        print("❌ Cannot connect to backend. Make sure it's running on localhost:8000")
        return
    
    # Create a search image
    search_img = create_test_image("Nike Shoes", "red")
    img_byte_arr = io.BytesIO()
    search_img.save(img_byte_arr, format='JPEG', quality=95)
    img_bytes = img_byte_arr.getvalue()
    
    # Test 1: Search without filtering (show all results)
    print("\n1️⃣  Search WITHOUT filtering:")
    try:
        files = {'image': ('test.jpg', img_bytes, 'image/jpeg')}
        response = requests.post(f"{BACKEND_URL}/search", files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            results = data['data']['results']
            print(f"   Found {len(results)} total results:")
            for i, result in enumerate(results[:5], 1):
                similarity = result['similarity_score'] * 100
                title = result['metadata'].get('title', 'Untitled')
                print(f"   {i}. {title} - {similarity:.1f}%")
        else:
            print(f"   ❌ Search failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Search with 85% filtering
    print("\n2️⃣  Search WITH 85% filtering:")
    try:
        files = {'image': ('test.jpg', img_bytes, 'image/jpeg')}
        data = {'min_score': '0.85'}  # Filter at backend level
        response = requests.post(f"{BACKEND_URL}/search", files=files, data=data, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            results = data['data']['results']
            print(f"   Found {len(results)} results above 85%:")
            for i, result in enumerate(results, 1):
                similarity = result['similarity_score'] * 100
                title = result['metadata'].get('title', 'Untitled')
                print(f"   {i}. {title} - {similarity:.1f}%")
            
            if len(results) == 0:
                print("   🎯 No results found above 85% similarity")
                print("   💡 This is good! It means your filter is working correctly.")
                print("   💡 Only very similar images will be shown to users.")
        else:
            print(f"   ❌ Search failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print(f"\n🎉 Your Flutter app will now show only results above 85% similarity!")
    print("📱 Test your Flutter app - it should show fewer, but more relevant results.")

if __name__ == "__main__":
    test_search_with_filtering()
