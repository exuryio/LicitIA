#!/usr/bin/env python3
"""Test script to demonstrate filtering tenders for interventoría vial."""
from datetime import datetime, timedelta
from app.services.secop_client import fetch_recent_tenders
from app.core.logging import setup_logging

setup_logging()

print("=" * 80)
print("🔍 TESTING FILTERS FOR INTERVENTORÍA VIAL")
print("=" * 80)
print()

# Test 1: Keyword filter for "interventoría" or "vial"
print("TEST 1: Searching for 'interventoría' or 'vial' keywords")
print("-" * 80)
since_date = datetime(2020, 1, 1)  # Start from 2020

# Try different keyword combinations
keywords_to_try = ["interventoría", "vial", "vías", "carretera", "malla vial"]

for keyword in keywords_to_try:
    print(f"\n🔍 Searching for: '{keyword}'")
    tenders = fetch_recent_tenders(
        since_timestamp=since_date,
        keyword_filter=keyword
    )
    print(f"   Found: {len(tenders)} tenders")
    if tenders:
        print(f"   Sample: {tenders[0].entity_name[:50]}...")
        break

print()
print("=" * 80)
print("TEST 2: Department filter (e.g., Cundinamarca)")
print("-" * 80)
tenders = fetch_recent_tenders(
    since_timestamp=since_date,
    department_filter="Cundinamarca"
)
print(f"Found: {len(tenders)} tenders in Cundinamarca")

print()
print("=" * 80)
print("TEST 3: Combined filters (keyword + department)")
print("-" * 80)
tenders = fetch_recent_tenders(
    since_timestamp=since_date,
    keyword_filter="vial",
    department_filter="Cundinamarca"
)
print(f"Found: {len(tenders)} tenders matching 'vial' in Cundinamarca")

print()
print("=" * 80)
print("💡 RECOMMENDED FILTERS FOR INTERVENTORÍA VIAL:")
print("=" * 80)
print()
print("1. KEYWORD FILTERS (most important):")
print("   - 'interventoría' OR 'interventoria'")
print("   - 'vial' OR 'vías' OR 'vias'")
print("   - 'carretera'")
print("   - 'malla vial'")
print("   - 'supervisión de vías'")
print()
print("2. LOCATION FILTERS:")
print("   - Specific departments (departamento_entidad)")
print("   - Specific cities (ciudad_entidad)")
print()
print("3. AMOUNT FILTERS:")
print("   - Minimum amount (min_amount)")
print("   - Maximum amount (max_amount)")
print()
print("4. DATE FILTER:")
print("   - Only recent tenders (since_timestamp)")
print()

