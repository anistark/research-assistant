#!/usr/bin/env python3
"""
Comprehensive API testing script for the Research Assistant
"""

import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = f"http://localhost:{os.getenv('PORT', 8000)}"

def test_api_health():
    """Test basic API connectivity"""
    print("🔍 Testing API health...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ API is healthy")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        return False

def test_upload():
    """Test the upload endpoint"""
    print("\n📤 Testing upload endpoint...")
    
    test_chunk = {
        "id": "test_chunk_001",
        "source_doc_id": "test_document.pdf",
        "chunk_index": 1,
        "section_heading": "Test Section",
        "doi": "10.1000/test.2023.001",
        "journal": "Test Journal",
        "publish_year": 2023,
        "usage_count": 0,
        "attributes": ["Testing", "API"],
        "link": "https://example.com/test",
        "text": "This is a test chunk for API validation. It contains sample text to verify the upload and embedding process works correctly."
    }
    
    payload = {
        "chunks": [test_chunk],
        "schema_version": "1.0"
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/api/upload",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 202:
            print("✅ Upload successful")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False

def test_similarity_search():
    """Test similarity search endpoint"""
    print("\n🔍 Testing similarity search...")
    
    test_queries = [
        {
            "query": "velvet bean cultivation practices",
            "k": 5,
            "min_score": 0.1
        },
        {
            "query": "Transformer attention mechanism",
            "k": 3,
            "min_score": 0.2
        },
        {
            "query": "intercropping mucuna with maize",
            "k": 10,
            "min_score": 0.15
        },
        {
            "query": "neural network sequence modeling",
            "k": 5,
            "min_score": 0.2
        }
    ]
    
    for i, search_req in enumerate(test_queries):
        print(f"\n  Query {i+1}: '{search_req['query']}'")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/similarity_search",
                json=search_req,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                results = response.json()
                found = len(results.get('results', []))
                print(f"    ✅ Found {found} results")
                
                if found > 0:
                    top_result = results['results'][0]
                    score = top_result['score'] * 100
                    text_preview = top_result['text'][:80] + "..."
                    print(f"    📄 Top match: {score:.1f}% - {text_preview}")
                    print(f"    📚 Source: {top_result['metadata']['source_doc_id']}")
            else:
                print(f"    ❌ Search failed: {response.status_code}")
                print(f"    Response: {response.text}")
        except Exception as e:
            print(f"    ❌ Search error: {e}")

def test_get_journal():
    """Test journal retrieval endpoint"""
    print("\n📖 Testing journal retrieval...")
    
    journal_ids = [
        "extension_brief_mucuna.pdf",
        "1706.03762v7.pdf", 
        "nonexistent_journal.pdf"
    ]
    
    for journal_id in journal_ids:
        print(f"\n  Getting journal: {journal_id}")
        
        try:
            response = requests.get(f"{BASE_URL}/api/{journal_id}")
            
            if response.status_code == 200:
                data = response.json()
                chunk_count = len(data.get('chunks', []))
                print(f"    ✅ Found {chunk_count} chunks")
            elif response.status_code == 404:
                print(f"    ℹ️  Journal not found: # {journal_id}")
            else:
                print(f"    ❌ Retrieval failed: {response.status_code}")
        except Exception as e:
            print(f"    ❌ Retrieval error: {e}")

def test_stats():
    """Test statistics endpoint"""
    print("\n📊 Testing statistics endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/stats")
        
        if response.status_code == 200:
            stats = response.json()
            print("✅ Statistics retrieved successfully")
            print(f"  📈 Total chunks: {stats.get('total_chunks', 0)}")
            
            top_papers = stats.get('top_referenced_papers', [])
            print(f"  🏆 Top papers tracked: {len(top_papers)}")
            
            if top_papers:
                print("  📚 Most referenced:")
                for i, paper in enumerate(top_papers[:3]):
                    usage = paper.get('total_usage', 0)
                    title = paper.get('source_doc_id', 'Unknown')
                    print(f"    {i+1}. {title} ({usage} references)")
        else:
            print(f"❌ Stats failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Stats error: {e}")

def run_performance_test():
    """Basic performance testing"""
    print("\n⚡ Running performance tests...")
    
    search_times = []
    
    for i in range(5):
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/similarity_search",
                json={"query": f"test query {i}", "k": 5, "min_score": 0.1},
                headers={"Content-Type": "application/json"}
            )
            
            end_time = time.time()
            search_time = end_time - start_time
            search_times.append(search_time)
            
            if response.status_code == 200:
                print(f"  🔍 Search {i+1}: {search_time:.3f}s")
            else:
                print(f"  ❌ Search {i+1} failed")
        except Exception as e:
            print(f"  ❌ Search {i+1} error: {e}")
    
    if search_times:
        avg_time = sum(search_times) / len(search_times)
        print(f"\n📊 Average search time: {avg_time:.3f}s")
        print(f"📊 Min/Max: {min(search_times):.3f}s / {max(search_times):.3f}s")

def main():
    """Run comprehensive API tests"""
    print("🧪 Research Assistant API Test Suite")
    print("=" * 50)
    
    tests = [
        ("API Health", test_api_health),
        ("Upload", test_upload),
        ("Similarity Search", test_similarity_search),
        ("Journal Retrieval", test_get_journal),
        ("Statistics", test_stats),
        ("Performance", run_performance_test)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result is not False:
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print(f"\n🎯 Test Summary: {passed}/{total} tests completed")
    
    if passed == total:
        print("🎉 All tests passed! API is functioning correctly.")
    else:
        print("⚠️  Some tests failed.")

if __name__ == "__main__":
    main()
