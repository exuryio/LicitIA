#!/usr/bin/env python3
"""View tenders with UNSPSC code 81101500 in a readable format."""
from datetime import datetime, timedelta
from app.services.secop_client import fetch_recent_tenders
from app.core.logging import setup_logging

setup_logging()

print("=" * 100)
print("📋 TENDERS WITH UNSPSC 81101500 - INGENIERÍA CIVIL Y ARQUITECTURA")
print("=" * 100)
print()

# Fetch tenders
since_date = datetime(2020, 1, 1)
print(f"🔍 Fetching tenders with UNSPSC 81101500...")
print()

tenders = fetch_recent_tenders(
    since_timestamp=since_date,
    unspsc_code="81101500"
)

print()
print("=" * 100)
print(f"✅ FOUND {len(tenders)} TENDERS")
print("=" * 100)
print()

if tenders:
    for i, tender in enumerate(tenders, 1):
        print(f"\n{'='*100}")
        print(f"TENDER #{i} of {len(tenders)}")
        print(f"{'='*100}")
        print()
        print(f"🆔 PROCESS ID: {tender.external_id}")
        print(f"🏢 ENTITY: {tender.entity_name}")
        print(f"📍 DEPARTMENT: {tender.department or 'N/A'}")
        print(f"📍 MUNICIPALITY: {tender.municipality or 'N/A'}")
        
        if tender.amount and tender.amount > 0:
            print(f"💰 AMOUNT: ${tender.amount:,.2f} COP")
        else:
            print(f"💰 AMOUNT: N/A")
        
        if tender.publication_date:
            print(f"📅 PUBLICATION DATE: {tender.publication_date.strftime('%Y-%m-%d')}")
        else:
            print(f"📅 PUBLICATION DATE: N/A")
        
        if tender.closing_date:
            print(f"📅 CLOSING DATE: {tender.closing_date.strftime('%Y-%m-%d')}")
        else:
            print(f"📅 CLOSING DATE: N/A")
        
        print(f"📊 STATE: {tender.state}")
        print(f"🔗 PROCESS URL: {tender.process_url}")
        print()
        print("📄 DESCRIPTION / OBJECT:")
        print("-" * 100)
        print(tender.object_text)
        print()
        
        # Ask if user wants to continue after every 5 tenders
        if i % 5 == 0 and i < len(tenders):
            print(f"\n... Showing {i} of {len(tenders)} tenders. Continue? (Press Enter)")
            input()
    
    print()
    print("=" * 100)
    print(f"✅ TOTAL: {len(tenders)} tenders displayed")
    print("=" * 100)
else:
    print("⚠️  No tenders found")

