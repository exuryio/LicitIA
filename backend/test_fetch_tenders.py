"""Test script to fetch and store tenders from SECOP II."""
from datetime import datetime, timedelta
from app.services.secop_client import fetch_recent_tenders
from app.core.logging import setup_logging

setup_logging()

def test_fetch_tenders():
    """Test fetching tenders from SECOP II."""
    
    print("🧪 Testing tender fetch from SECOP II...")
    print()
    
    # Fetch tenders from last 365 days (dataset has historical data)
    # Note: Adjust this based on when you want to start fetching from
    since_date = datetime.utcnow() - timedelta(days=365)
    print(f"📅 Fetching tenders since: {since_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        tenders = fetch_recent_tenders(since_date)
        
        print(f"✅ Successfully fetched {len(tenders)} tenders")
        print()
        
        if tenders:
            print("📋 Sample tenders:")
            print()
            for i, tender in enumerate(tenders[:5], 1):
                print(f"{i}. {tender.entity_name}")
                print(f"   ID: {tender.external_id}")
                print(f"   Departamento: {tender.department or 'N/A'}")
                print(f"   Monto: ${tender.amount:,.2f} COP" if tender.amount else "   Monto: N/A")
                print(f"   Fecha publicación: {tender.publication_date.strftime('%Y-%m-%d') if tender.publication_date else 'N/A'}")
                print(f"   URL: {tender.process_url}")
                print()
        else:
            print("⚠️  No tenders found in the specified date range")
            print("   Try adjusting the date range or check your SECOP_DATASET_ID")
        
        print("=" * 80)
        print("✅ Test completed!")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error fetching tenders: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_fetch_tenders()

