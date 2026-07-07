#!/usr/bin/env python3
"""
Quick test to check if products exist with specific SKUs in Firestore
"""

import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase Admin SDK
cred_path = 'image_search_backend_python/swift-26949-00fcd2344ea7.json'
if not os.path.exists(cred_path):
    print(f"❌ Credential file not found: {cred_path}")
    exit(1)

cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

db = firestore.client()

# Test SKUs from image search results
test_skus = ['SKU-96591', 'SKU-29206']

print("🔍 Testing if products exist for these SKUs:")
print("-" * 50)

for sku in test_skus:
    print(f"\n🏷️  Checking SKU: {sku}")
    
    # Query Products collection by Sku field
    products = db.collection('Products').where('Sku', '==', sku).limit(1).get()
    
    if products:
        product = products[0]
        product_data = product.to_dict()
        print(f"✅ Found product!")
        print(f"   📄 Document ID: {product.id}")
        print(f"   🏷️  SKU: {product_data.get('Sku', 'N/A')}")
        print(f"   📝 Title: {product_data.get('Title', 'N/A')}")
        print(f"   🏪 Category: {product_data.get('CategoryId', 'N/A')}")
    else:
        print(f"❌ No product found with SKU: {sku}")

print("\n" + "="*50)
print("🔍 Let's also check all products in the database:")

all_products = db.collection('Products').limit(10).get()
print(f"📊 Total products found: {len(all_products)}")

if all_products:
    print("\n📋 First few products:")
    for i, product in enumerate(all_products[:5]):
        product_data = product.to_dict()
        print(f"   {i+1}. SKU: {product_data.get('Sku', 'NO-SKU')} | Title: {product_data.get('Title', 'NO-TITLE')}")
else:
    print("❌ No products found in the database!")
