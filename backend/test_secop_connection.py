"""Test script to inspect SECOP II dataset and verify connection."""
import requests
import json
from datetime import datetime, timedelta
from app.config import settings
from app.core.logging import setup_logging

setup_logging()

def test_secop_connection():
    """Test connection to SECOP II and inspect dataset structure."""
    
    if not settings.SECOP_DATASET_ID:
        print("❌ ERROR: SECOP_DATASET_ID not configured in .env")
        print("Please set SECOP_DATASET_ID in your .env file")
        return
    
    base_url = f"{settings.SECOP_BASE_URL}/{settings.SECOP_DATASET_ID}.json"
    
    print(f"🔍 Testing connection to SECOP II...")
    print(f"📡 URL: {base_url}")
    print(f"🔑 App Token: {'✅ Set' if settings.SECOP_APP_TOKEN else '❌ Not set (optional)'}")
    print()
    
    # Try to fetch a few records to inspect structure
    params = {
        "$limit": 5,
        "$order": "fecha_de_publicacion_del DESC",
    }
    
    headers = {}
    if settings.SECOP_APP_TOKEN:
        headers["X-App-Token"] = settings.SECOP_APP_TOKEN
    
    try:
        print("📥 Fetching sample records...")
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if not data:
            print("⚠️  No data returned. Check your DATASET_ID.")
            return
        
        print(f"✅ Successfully fetched {len(data)} sample records")
        print()
        print("=" * 80)
        print("📋 DATASET STRUCTURE ANALYSIS")
        print("=" * 80)
        print()
        
        # Analyze first record to see all available fields
        if data:
            first_record = data[0]
            print("📊 Available fields in the dataset:")
            print()
            for key, value in first_record.items():
                value_preview = str(value)[:100] if value else "null"
                if len(value_preview) > 100:
                    value_preview += "..."
                print(f"  • {key:40s} = {value_preview}")
            print()
            print("=" * 80)
            print("🔍 FIELD MAPPING SUGGESTIONS")
            print("=" * 80)
            print()
            
            # Try to identify common fields
            field_mapping = {}
            
            # Look for process number/ID
            for key in first_record.keys():
                key_lower = key.lower()
                if any(term in key_lower for term in ["numero", "numero_del_proceso", "id_proceso", "codigo"]):
                    if "proceso" in key_lower or "numero" in key_lower:
                        field_mapping["external_id"] = key
                        print(f"  ✅ external_id (process number): '{key}'")
                        break
            
            # Look for entity name
            for key in first_record.keys():
                key_lower = key.lower()
                if any(term in key_lower for term in ["entidad", "nombre_entidad", "institucion"]):
                    field_mapping["entity_name"] = key
                    print(f"  ✅ entity_name: '{key}'")
                    break
            
            # Look for object text
            for key in first_record.keys():
                key_lower = key.lower()
                if any(term in key_lower for term in ["objeto", "objeto_del_proceso", "descripcion"]):
                    field_mapping["object_text"] = key
                    print(f"  ✅ object_text: '{key}'")
                    break
            
            # Look for publication date
            for key in first_record.keys():
                key_lower = key.lower()
                if any(term in key_lower for term in ["fecha_publicacion", "fecha_de_publicacion", "publicacion"]):
                    field_mapping["publication_date"] = key
                    print(f"  ✅ publication_date: '{key}'")
                    break
            
            # Look for closing date
            for key in first_record.keys():
                key_lower = key.lower()
                if any(term in key_lower for term in ["fecha_cierre", "fecha_de_cierre", "cierre"]):
                    field_mapping["closing_date"] = key
                    print(f"  ✅ closing_date: '{key}'")
                    break
            
            # Look for amount
            for key in first_record.keys():
                key_lower = key.lower()
                if any(term in key_lower for term in ["valor", "presupuesto", "monto", "cuantia"]):
                    field_mapping["amount"] = key
                    print(f"  ✅ amount: '{key}'")
                    break
            
            # Look for department
            for key in first_record.keys():
                key_lower = key.lower()
                if "departamento" in key_lower:
                    field_mapping["department"] = key
                    print(f"  ✅ department: '{key}'")
                    break
            
            # Look for municipality
            for key in first_record.keys():
                key_lower = key.lower()
                if "municipio" in key_lower:
                    field_mapping["municipality"] = key
                    print(f"  ✅ municipality: '{key}'")
                    break
            
            # Look for state
            for key in first_record.keys():
                key_lower = key.lower()
                if any(term in key_lower for term in ["estado", "estado_del_proceso", "estado_proceso"]):
                    field_mapping["state"] = key
                    print(f"  ✅ state: '{key}'")
                    break
            
            # Look for URL
            for key in first_record.keys():
                key_lower = key.lower()
                if any(term in key_lower for term in ["url", "enlace", "link", "proceso"]):
                    if "url" in key_lower or "enlace" in key_lower:
                        field_mapping["process_url"] = key
                        print(f"  ✅ process_url: '{key}'")
                        break
            
            print()
            print("=" * 80)
            print("📝 SAMPLE RECORD (First tender)")
            print("=" * 80)
            print(json.dumps(first_record, indent=2, ensure_ascii=False, default=str))
            print()
            
            # Test date filtering
            print("=" * 80)
            print("🧪 TESTING DATE FILTER")
            print("=" * 80)
            print()
            
            test_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            date_field = field_mapping.get("publication_date", "fecha_de_publicacion_del")
            
            test_params = {
                "$limit": 1,
                "$where": f"{date_field} >= '{test_date}'",
            }
            
            print(f"Testing filter: {date_field} >= '{test_date}'")
            test_response = requests.get(base_url, params=test_params, headers=headers, timeout=30)
            
            if test_response.status_code == 200:
                test_data = test_response.json()
                print(f"✅ Date filter works! Found {len(test_data)} records in last 30 days")
            else:
                print(f"⚠️  Date filter test returned status {test_response.status_code}")
                print(f"Response: {test_response.text[:200]}")
            
            print()
            print("=" * 80)
            print("✅ Connection test completed!")
            print("=" * 80)
            print()
            print("📌 Next steps:")
            print("  1. Review the field mappings above")
            print("  2. Update secop_client.py with the correct field names")
            print("  3. Test the fetch_recent_tenders function")
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to SECOP API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text[:500]}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_secop_connection()

