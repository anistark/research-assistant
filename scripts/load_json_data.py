#!/usr/bin/env python3
"""
Load sample data from data/sample_chunks.json to the research assistant API
"""

import requests
import json
import sys
import os
from pathlib import Path

backend_src = Path(__file__).parent.parent / "backend" / "src"
sys.path.insert(0, str(backend_src))

from dotenv import load_dotenv

backend_env = Path(__file__).parent.parent / "backend" / ".env"
load_dotenv(backend_env)


def load_from_json_file(filename="../data/sample_chunks.json", base_url=None):
    """Load chunks from JSON file and upload to API"""

    script_dir = Path(__file__).parent
    data_file = script_dir / filename

    if base_url is None:
        port = os.getenv("PORT", 8000)
        base_url = f"http://localhost:{port}"

    if not data_file.exists():
        print(f"❌ File {data_file} not found!")
        print("Please ensure the sample data exists at data/sample_chunks.json")
        return False

    try:
        with open(filename, "r", encoding="utf-8") as f:
            chunks = json.load(f)

        print(f"📁 Loaded {len(chunks)} chunks from {filename}")

        upload_payload = {"chunks": chunks, "schema_version": "1.0"}

        response = requests.put(
            f"{base_url}/api/upload",
            json=upload_payload,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 202:
            print("✅ Successfully uploaded data from JSON file!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Upload failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API.")
        print(f"   Expected API URL: {base_url}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def verify_upload(base_url=None):
    """Verify the data was uploaded correctly"""
    if base_url is None:
        port = os.getenv("PORT", 8000)
        base_url = f"http://localhost:{port}"

    try:
        response = requests.get(f"{base_url}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"\n📊 Database now contains {stats['total_chunks']} chunks")

            print("\n📚 Available documents:")
            papers = stats.get("top_referenced_papers", [])
            for paper in papers[:5]:
                print(f"  • {paper['source_doc_id']} ({paper['journal']})")

        print(f"\n🔍 Testing search functionality...")
        search_response = requests.post(
            f"{base_url}/api/similarity_search",
            json={"query": "velvet bean cultivation", "k": 3, "min_score": 0.1},
        )

        if search_response.status_code == 200:
            results = search_response.json()
            found = len(results.get("results", []))
            print(
                f"✅ Search test successful: found {found} results for 'velvet bean cultivation'"
            )
        else:
            print("❌ Search test failed")

    except Exception as e:
        print(f"❌ Verification failed: {e}")


if __name__ == "__main__":
    print("🚀 Research Assistant JSON Data Loader")
    print("=" * 50)

    port = os.getenv("PORT", 8000)
    api_url = f"http://localhost:{port}"

    try:
        response = requests.get(api_url)
        print("✅ API server is running")
    except:
        print("❌ API server not accessible")
        sys.exit(1)

    if load_from_json_file():
        verify_upload()

        print("\n✅ Setup complete!")
    else:
        print("❌ Setup failed. Check the error messages above.")
        sys.exit(1)
