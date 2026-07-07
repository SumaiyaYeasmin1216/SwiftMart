#!/bin/bash

# Image Search Testing Guide
# This script demonstrates how to manually test the search functionality

echo "🔍 AI Image Search Testing Methods"
echo "=================================="

# Method 1: Check backend health
echo "1️⃣  Backend Health Check:"
curl -s http://localhost:8000/health | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'✅ Status: {data[\"status\"]}')
print(f'📊 CLIP Model: {data[\"services\"][\"clip_model\"]}')
print(f'🗄️  Database: {data[\"services\"][\"firestore\"]}')
print(f'☁️  Storage: {data[\"services\"][\"cloudinary\"]}')
"

echo ""
echo "2️⃣  Current Database Contents:"
curl -s http://localhost:8000/images | python3 -c "
import sys, json
data = json.load(sys.stdin)
total = data['data']['total']
print(f'📊 Total Images: {total}')
for i, img in enumerate(data['data']['images'][:5], 1):
    title = img['metadata'].get('title', 'Untitled')
    category = img['metadata'].get('category', 'No category')
    print(f'   {i}. {title} ({category})')
if total > 5:
    print(f'   ... and {total-5} more images')
"

echo ""
echo "3️⃣  Search Test Methods:"
echo "   A) Use your Flutter app (recommended)"
echo "   B) Run: python3 test_search.py"
echo "   C) Manual cURL (example below):"

echo ""
echo "Manual Search Example:"
echo "# Create a test image and search with it"
echo "curl -X POST http://localhost:8000/search \\"
echo "  -F 'image=@your_image.jpg' \\"
echo "  | python3 -c \""
echo "import sys, json"
echo "data = json.load(sys.stdin)"
echo "results = data['data']['results']"
echo "print(f'Found {len(results)} similar images:')"
echo "for i, r in enumerate(results[:3], 1):"
echo "    score = r['similarity_score'] * 100"
echo "    title = r['metadata'].get('title', 'Untitled')"
echo "    print(f'  {i}. {title} - {score:.1f}% similar')"
echo "\""

echo ""
echo "4️⃣  Upload New Test Image:"
echo "curl -X POST http://localhost:8000/upload \\"
echo "  -F 'image=@your_product.jpg' \\"
echo "  -F 'title=My Product Name' \\"
echo "  -F 'category=shoes'"

echo ""
echo "🎯 Recommended: Use your Flutter app for the best experience!"
echo "   Your app automatically handles image capture, upload, and search display."
