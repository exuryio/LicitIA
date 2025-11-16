#!/usr/bin/env python3
"""View tenders with UNSPSC 81101500 filtered by date range."""
from datetime import datetime, timedelta
from app.services.secop_client import fetch_recent_tenders
from app.core.logging import setup_logging

setup_logging()

print("=" * 100)
print("📋 TENDERS WITH UNSPSC 81101500 - FILTERED BY DATE")
print("=" * 100)
print()

# Date range: August 2024 to today
# Note: Change the year/month below if you need a different range
# If you meant August 2025, change to: datetime(2025, 8, 1)
start_date = datetime(2024, 8, 1)  # August 1, 2024
end_date = datetime.now()

# You can also customize the dates here:
# start_date = datetime(2025, 8, 1)  # For August 2025
# end_date = datetime.now()

print(f"📅 Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
print(f"🔑 UNSPSC Code: 81101500 (Ingeniería Civil y Arquitectura)")
print()
print("⏳ Fetching tenders...")
print()

try:
    # Fetch all tenders with UNSPSC code (we'll filter by date after)
    all_tenders = fetch_recent_tenders(
        since_timestamp=start_date,
        unspsc_code="81101500"
    )
    
    # Filter by date range (publication date)
    filtered_tenders = []
    tenders_without_dates = []
    
    for tender in all_tenders:
        if tender.publication_date:
            if start_date <= tender.publication_date <= end_date:
                filtered_tenders.append(tender)
        else:
            # Keep track of tenders without dates
            tenders_without_dates.append(tender)
    
    # If no tenders with dates in range, show message
    if not filtered_tenders and tenders_without_dates:
        print(f"⚠️  Note: {len(tenders_without_dates)} tenders found but they don't have publication dates")
        print(f"   Showing all {len(all_tenders)} tenders (including those without dates)")
        print()
        filtered_tenders = all_tenders  # Show all if no dates match
    
    print()
    print("=" * 100)
    print(f"✅ FOUND {len(filtered_tenders)} TENDERS")
    print(f"   (Out of {len(all_tenders)} total with UNSPSC 81101500)")
    print("=" * 100)
    print()
    
    if filtered_tenders:
        # Sort by publication date (newest first)
        filtered_tenders.sort(key=lambda x: x.publication_date if x.publication_date else datetime.min, reverse=True)
        
        for i, tender in enumerate(filtered_tenders, 1):
            print(f"\n{'='*100}")
            print(f"TENDER #{i} of {len(filtered_tenders)}")
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
            print(tender.object_text[:300] + ("..." if len(tender.object_text) > 300 else ""))
            print()
            
            # Show every 5 tenders
            if i % 5 == 0 and i < len(filtered_tenders):
                print(f"\n... Showing {i} of {len(filtered_tenders)} tenders. Press Enter to continue...")
                try:
                    input()
                except:
                    pass
        
        print()
        print("=" * 100)
        print(f"✅ TOTAL: {len(filtered_tenders)} tenders displayed")
        print("=" * 100)
        
        # Summary
        print()
        print("📊 SUMMARY:")
        print(f"   • Total tenders found: {len(filtered_tenders)}")
        if filtered_tenders:
            with_dates = sum(1 for t in filtered_tenders if t.publication_date)
            print(f"   • Tenders with publication dates: {with_dates}")
            print(f"   • Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    else:
        print("⚠️  No tenders found in this date range")
        print()
        print("💡 Try:")
        print("   - Adjusting the date range")
        print("   - Checking if tenders have publication dates")
        print("   - Some tenders might not have dates in the dataset")
        
except Exception as e:
    print()
    print("=" * 100)
    print("❌ ERROR")
    print("=" * 100)
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

