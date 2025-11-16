#!/usr/bin/env python3
"""Test filtering by UNSPSC code 81101500 - Ingeniería Civil y Arquitectura."""
from datetime import datetime, timedelta
from app.services.secop_client import fetch_recent_tenders
from app.core.logging import setup_logging

setup_logging()

print("=" * 80)
print("🔍 TESTING: Filter by UNSPSC Code 81101500")
print("   (Ingeniería Civil y Arquitectura)")
print("=" * 80)
print()

# Test with UNSPSC code
unspsc_code = "81101500"
since_date = datetime(2020, 1, 1)

print(f"📅 Searching for tenders since: {since_date.strftime('%Y-%m-%d')}")
print(f"🔑 UNSPSC Code: {unspsc_code} (Ingeniería Civil y Arquitectura)")
print()
print("⏳ Fetching...")
print()

try:
    tenders = fetch_recent_tenders(
        since_timestamp=since_date,
        unspsc_code=unspsc_code
    )
    
    print()
    print("=" * 80)
    
    if tenders:
        print(f"✅ FOUND {len(tenders)} TENDERS with UNSPSC {unspsc_code}!")
        print("=" * 80)
        print()
        
        # Show first few tenders
        for i, tender in enumerate(tenders[:5], 1):
            print(f"📋 TENDER #{i}:")
            print("-" * 80)
            print(f"🆔 Process ID: {tender.external_id}")
            print(f"🏢 Entity: {tender.entity_name}")
            print(f"📍 Department: {tender.department or 'N/A'}")
            print(f"💰 Amount: ${tender.amount:,.2f} COP" if tender.amount and tender.amount > 0 else "💰 Amount: N/A")
            print(f"📅 Published: {tender.publication_date.strftime('%Y-%m-%d') if tender.publication_date else 'N/A'}")
            print(f"📊 State: {tender.state}")
            print(f"🔗 URL: {tender.process_url}")
            print()
            print("📄 Description:")
            print(tender.object_text[:200] + ("..." if len(tender.object_text) > 200 else ""))
            print()
        
        if len(tenders) > 5:
            print(f"... and {len(tenders) - 5} more tenders")
            print()
        
        print("=" * 80)
        print("✅ SUCCESS! You can filter by UNSPSC code 81101500!")
        print("=" * 80)
    else:
        print("⚠️  No tenders found with UNSPSC code 81101500")
        print("=" * 80)
        print()
        print("This could mean:")
        print("  - The code format might be different in the dataset")
        print("  - Try checking what category codes are actually used")
        print("  - The code might be stored with a prefix (e.g., 'V1.81101500')")
        
except Exception as e:
    print()
    print("=" * 80)
    print("❌ ERROR")
    print("=" * 80)
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

