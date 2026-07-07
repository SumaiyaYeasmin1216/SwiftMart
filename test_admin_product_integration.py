#!/usr/bin/env python3
"""
Test Admin Product Integration with AI Search

This script demonstrates the complete workflow:
1. Admin uploads a product with images (simulated)
2. Product images are automatically indexed in AI search backend
3. User searches with similar image and finds the product
4. User navigates to the product detail page

Run this test to verify the integration is working.
"""

import requests
import json
import time

# Configuration
BACKEND_URL = "http://localhost:8000"
SAMPLE_PRODUCT_DATA = {
    "product_id": "test-product-123",
    "name": "Nike Air Max Sneakers",
    "price": 129.99,
    "description": "Premium athletic sneakers with excellent cushioning"
}

# Sample product image URLs (using some existing Cloudinary URLs for testing)
SAMPLE_PRODUCT_IMAGES = [
    "https://res.cloudinary.com/dx9kx8j5t/image/upload/v1725027569/image_search_uploads/0f1d8c6f-7b5e-4c8e-b7a3-1c9f2c8d3e4f.jpg",
    "https://res.cloudinary.com/dx9kx8j5t/image/upload/v1725027568/image_search_uploads/8f2e9c7a-3d6e-4b9f-a8c5-2e0f3d7a9b8c.jpg",
]

def test_product_image_indexing():
    """Test the new /api/index_image endpoint"""
    print("\n🧪 Testing Product Image Indexing")
    print("="*50)
    
    for i, image_url in enumerate(SAMPLE_PRODUCT_IMAGES):
        print(f"📸 Indexing image {i+1}: {image_url[:60]}...")
        
        # Send request to index product image
        response = requests.post(f"{BACKEND_URL}/api/index_image", json={
            "product_id": SAMPLE_PRODUCT_DATA["product_id"],
            "image_url": image_url
        })
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"✅ Indexed successfully: {result['data']['document_id']}")
        else:
            print(f"❌ Failed to index: {response.status_code} - {response.text}")
            
        time.sleep(1)  # Small delay between requests
    
def test_search_integration():
    """Test searching and verify product_id is returned"""
    print("\n🔍 Testing Search Integration")
    print("="*50)
    
    # Use one of the indexed images as search query (simulate user uploading similar image)
    search_image_url = SAMPLE_PRODUCT_IMAGES[0]
    
    print(f"🖼️  Searching with image: {search_image_url[:60]}...")
    
    # Download the image for search
    img_response = requests.get(search_image_url)
    if img_response.status_code != 200:
        print("❌ Failed to download search image")
        return
    
    # Send search request
    files = {"image": ("test_image.jpg", img_response.content, "image/jpeg")}
    search_response = requests.post(f"{BACKEND_URL}/search", files=files)
    
    if search_response.status_code == 200:
        results = search_response.json()
        print(f"📊 Search returned {len(results['data']['results'])} results")
        
        for i, result in enumerate(results['data']['results'][:3]):  # Show top 3
            score = result.get('similarity_score', 0) * 100
            product_id = result.get('product_id', 'None')
            print(f"  {i+1}. Similarity: {score:.1f}% | Product ID: {product_id}")
            
            if product_id == SAMPLE_PRODUCT_DATA["product_id"]:
                print(f"     🎯 Found our test product! Navigation would work.")
    else:
        print(f"❌ Search failed: {search_response.status_code}")

def check_backend_health():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Backend is healthy: {health}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False

def main():
    """Run the complete integration test"""
    print("🚀 AI Search + Admin Product Integration Test")
    print("="*60)
    
    # Check backend
    if not check_backend_health():
        print("\n💡 Make sure to start the backend first:")
        print("   cd image_search_backend_python && python3 main.py")
        return
    
    # Test product indexing
    test_product_image_indexing()
    
    # Wait a bit for indexing to complete
    print("\n⏳ Waiting for indexing to complete...")
    time.sleep(3)
    
    # Test search
    test_search_integration()
    
    print("\n" + "="*60)
    print("🎉 Integration test completed!")
    print("\n📱 Flutter App Workflow:")
    print("   1. Admin uploads product → Images auto-indexed")
    print("   2. User searches image → Gets results with product_id")
    print("   3. User taps result → Navigates to product details")
    print("\n🔗 Key Integration Points:")
    print("   • ProductRepository._syncProductImagesWithSearchBackend()")
    print("   • Backend /api/index_image endpoint")  
    print("   • Search results include product_id for navigation")

if __name__ == "__main__":
    main()
