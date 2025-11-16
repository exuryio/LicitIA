#!/usr/bin/env python3
"""Simple test script to verify SECOP II connection."""
from datetime import datetime, timedelta
from app.services.secop_client import fetch_recent_tenders
from app.core.logging import setup_logging
from app.config import settings

setup_logging()

print("=" * 80)
print("🧪 SECOP II CONNECTION TEST")
print("=" * 80)
print()
print(f"Dataset ID: {settings.SECOP_DATASET_ID}")
print(f"App Token: {'✅ Set' if settings.SECOP_APP_TOKEN else '❌ Not set'}")
print()

# Test with last 7 days
since_date = datetime.now() - timedelta(days=7)
print(f"📅 Fetching tenders since: {since_date.strftime('%Y-%m-%d')}")
print()
print("⏳ This may take a moment...")
print()

try:
    tenders = fetch_recent_tenders(since_date)
    
    print()
    print("=" * 80)
    print(f"✅ SUCCESS! Fetched {len(tenders)} tenders")
    print("=" * 80)
    print()
    
    if tenders:
        print("📋 Sample tenders:")
        print()
        for i, t in enumerate(tenders[:5], 1):
            print(f"{i}. {t.entity_name[:60]}")
            print(f"   ID: {t.external_id}")
            print(f"   Department: {t.department or 'N/A'}")
            if t.amount and t.amount > 0:
                print(f"   Amount: ${t.amount:,.2f} COP")
            else:
                print(f"   Amount: N/A")
            if t.publication_date:
                print(f"   Published: {t.publication_date.strftime('%Y-%m-%d')}")
            else:
                print(f"   Published: N/A")
            print(f"   State: {t.state}")
            print()
        
        if len(tenders) > 5:
            print(f"... and {len(tenders) - 5} more tenders")
            print()
        
        print("=" * 80)
        print("✅ Automatic detection is working correctly!")
        print("=" * 80)
    else:
        print("⚠️  No tenders found in the last 7 days.")
        print("   This is normal if there are no new tenders published recently.")
        print("   Try testing with a longer date range (e.g., 30 days).")
        print()
        
except Exception as e:
    print()
    print("=" * 80)
    print("❌ ERROR")
    print("=" * 80)
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

