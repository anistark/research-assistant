#!/usr/bin/env python3
"""
Upload sample data from data/sample_chunks.json to the research assistant API
"""

import requests
import json
import sys
from dotenv import load_dotenv
import os

load_dotenv()

def load_sample_chunks_from_file(filename="data/sample_chunks.json"):
    """Load sample chunks from JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Sample data file not found: {filename}")
        print("Please ensure sample_chunks.json exists in the data/ directory")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {filename}: {e}")
        return []

def upload_sample_data(base_url=None):
    """Upload sample chunks to the API"""
    
    if base_url is None:
        port = os.getenv('PORT', 8000)
        base_url = f"http://localhost:{port}"
    
    sample_chunks = load_sample_chunks_from_file()
    if not sample_chunks:
        return False
    
    print(f"📁 Loaded {len(sample_chunks)} chunks from data/sample_chunks.json")
    
    upload_payload = {
        "chunks": sample_chunks,
        "schema_version": "1.0"
    }
    
    try:
        response = requests.put(
            f"{base_url}/api/upload",
            json=upload_payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 202:
            print("✅ Successfully uploaded sample data!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Upload failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API.")
        print(f"   Expected API URL: {base_url}")
        return False
    except Exception as e:
        print(f"❌ Upload failed: {str(e)}")
        return False

def test_search(base_url=None):
    """Test the similarity search functionality"""
    
    if base_url is None:
        port = os.getenv('PORT', 8000)
        base_url = f"http://localhost:{port}"
    
    test_queries = [
        "What is mucuna and how does it grow?",
        "How to grow velvet bean with maize?", 
        "What is the Transformer architecture?",
        "Attention mechanisms in neural networks",
        "Soil fertility and green manure",
        "Machine translation with neural networks"
    ]
    
    print("\n🔍 Testing search functionality...")
    
    for query in test_queries:
        try:
            response = requests.post(
                f"{base_url}/api/similarity_search",
                json={"query": query, "k": 3, "min_score": 0.1},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                results = response.json()
                print(f"\nQuery: '{query}'")
                print(f"Found {len(results['results'])} results")
                
                for i, result in enumerate(results['results'][:2]):
                    score = result['score'] * 100
                    print(f"  {i+1}. Score: {score:.1f}% - {result['text'][:100]}...")
            else:
                print(f"Search failed for '{query}': {response.status_code}")
                
        except Exception as e:
            print(f"Search error for '{query}': {str(e)}")

if __name__ == "__main__":
    print("🚀 Research Assistant Data Upload Tool")
    print("=" * 50)
    
    port = os.getenv('PORT', 8000)
    api_url = f"http://localhost:{port}"
    
    try:
        response = requests.get(api_url)
        print("✅ API server is running")
    except:
        print("❌ API server not accessible.")
        sys.exit(1)
    
    if upload_sample_data():
        test_search()
        
        print("\n✅ Setup complete!")
    else:
        print("❌ Setup failed. Check the error messages above.")
        sys.exit(1)
