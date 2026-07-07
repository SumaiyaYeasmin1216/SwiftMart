#!/usr/bin/env python3
"""
Simple script to add a 'clothing' category to Firestore to match the image search products.
"""

import firebase_admin
from firebase_admin import credentials, firestore
import json
import os
from datetime import datetime

def add_clothing_category():
    """Add a clothing category to Firestore"""
    try:
        # Path to service account key
        cred_path = "/Users/hemal/Downloads/Git/ecommerce_admin/image_search_backend_python/swift-26949-00fcd2344ea7.json"
        
        if not os.path.exists(cred_path):
            print(f"❌ Service account file not found: {cred_path}")
            return
        
        # Initialize Firebase Admin
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        
        # Get Firestore client
        db = firestore.client()
        
        # Check if category already exists
        doc_ref = db.collection('Categories').document('clothing')
        doc = doc_ref.get()
        
        if doc.exists:
            print("✅ Category 'clothing' already exists!")
            print(f"Category data: {doc.to_dict()}")
            return
        
        # Add the clothing category
        category_data = {
            'Name': 'Clothing',
            'Image': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=500&h=500&fit=crop',
            'isFeatured': True,
            'ParentId': '',
            'CreateAt': datetime.now(),
            'UpdateAt': datetime.now()
        }
        
        doc_ref.set(category_data)
        print("✅ Successfully added 'clothing' category to Firestore!")
        print(f"Category data: {category_data}")
        
    except Exception as e:
        print(f"❌ Error adding clothing category: {e}")

if __name__ == "__main__":
    print("🚀 Adding clothing category to Firestore...")
    add_clothing_category()
    print("✅ Done!")
