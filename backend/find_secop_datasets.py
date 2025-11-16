"""Script to help find SECOP II datasets on datos.gov.co."""
import requests
import json
from typing import List, Dict

def search_secop_datasets(query: str = "SECOP II") -> List[Dict]:
    """
    Search for SECOP datasets on datos.gov.co.
    
    Note: This uses the Socrata API search endpoint.
    """
    # Socrata search endpoint for datos.gov.co
    search_url = "https://www.datos.gov.co/api/search"
    
    params = {
        "q": query,
        "limit": 20,
    }
    
    try:
        print(f"🔍 Searching for datasets matching: '{query}'")
        print()
        
        response = requests.get(search_url, params=params, timeout=30)
        response.raise_for_status()
        
        results = response.json()
        
        if "results" in results:
            datasets = results["results"]
            print(f"✅ Found {len(datasets)} datasets")
            print()
            print("=" * 80)
            print("📋 SECOP II DATASETS FOUND:")
            print("=" * 80)
            print()
            
            for i, dataset in enumerate(datasets, 1):
                resource_id = dataset.get("resource", {}).get("id", "N/A")
                name = dataset.get("resource", {}).get("name", "Unknown")
                description = dataset.get("resource", {}).get("description", "")[:200]
                
                print(f"{i}. {name}")
                print(f"   📌 Dataset ID: {resource_id}")
                if description:
                    print(f"   📝 Description: {description}...")
                print()
            
            return datasets
        else:
            print("⚠️  No results found or unexpected response format")
            print(f"Response: {json.dumps(results, indent=2)[:500]}")
            return []
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error searching datasets: {e}")
        return []
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return []


def list_popular_secop_datasets():
    """List some common SECOP dataset search terms."""
    print("=" * 80)
    print("🔍 COMMON SECOP DATASET SEARCH TERMS")
    print("=" * 80)
    print()
    print("Try searching for:")
    print("  1. 'SECOP II'")
    print("  2. 'SECOP 2'")
    print("  3. 'procesos de contratación'")
    print("  4. 'licitaciones públicas'")
    print("  5. 'contratación pública'")
    print()
    print("=" * 80)
    print()


if __name__ == "__main__":
    print("=" * 80)
    print("🔍 SECOP II DATASET FINDER")
    print("=" * 80)
    print()
    print("This script helps you find SECOP II datasets on datos.gov.co")
    print()
    
    # Show common search terms
    list_popular_secop_datasets()
    
    # Try searching for SECOP II
    datasets = search_secop_datasets("SECOP II")
    
    if not datasets:
        print()
        print("💡 TIP: If no results, try:")
        print("   1. Go directly to https://www.datos.gov.co/")
        print("   2. Search manually in the browser")
        print("   3. Look for 'SECOP' or 'Contratación Pública' categories")
        print()
    
    print("=" * 80)
    print("📝 NEXT STEPS:")
    print("=" * 80)
    print()
    print("1. Copy one of the Dataset IDs shown above")
    print("2. Add it to your .env file:")
    print("   SECOP_DATASET_ID=your-dataset-id-here")
    print("3. Run: python test_secop_connection.py")
    print()

