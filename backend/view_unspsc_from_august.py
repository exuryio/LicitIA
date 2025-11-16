#!/usr/bin/env python3
"""View tenders with UNSPSC 81101500 from August 1, 2025 until today."""
from datetime import datetime
from app.services.secop_client import fetch_recent_tenders
from app.core.logging import setup_logging

setup_logging()

print("=" * 100)
print("📋 TENDERS WITH UNSPSC 81101500")
print("   Fecha de publicación desde: 01/08/2025 hasta hoy")
print("=" * 100)
print()

# Date range: August 1, 2025 to today
start_date = datetime(2025, 8, 1)  # August 1, 2025
end_date = datetime.now()

print(f"📅 Fecha de publicación desde: {start_date.strftime('%d/%m/%Y')}")
print(f"📅 Hasta: {end_date.strftime('%d/%m/%Y')}")
print(f"🔑 UNSPSC Code: 81101500 (Ingeniería Civil y Arquitectura)")
print()
print("⏳ Fetching tenders from SECOP II...")
print()

try:
    # Fetch tenders with UNSPSC code and date filter
    tenders = fetch_recent_tenders(
        since_timestamp=start_date,
        unspsc_code="81101500"
    )
    
    # Additional filter by end date (in memory, since we can only do >= in $where)
    filtered_tenders = []
    for tender in tenders:
        if tender.publication_date:
            if start_date <= tender.publication_date <= end_date:
                filtered_tenders.append(tender)
        # If no date but within reasonable range, include it
        elif not tender.publication_date:
            # Include tenders without dates (they might be recent)
            filtered_tenders.append(tender)
    
    print()
    print("=" * 100)
    print(f"✅ FOUND {len(filtered_tenders)} TENDERS")
    print("=" * 100)
    print()
    
    if filtered_tenders:
        # Sort by publication date (newest first)
        filtered_tenders.sort(
            key=lambda x: x.publication_date if x.publication_date else datetime.min, 
            reverse=True
        )
        
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
                print(f"📅 FECHA DE PUBLICACIÓN: {tender.publication_date.strftime('%d/%m/%Y')}")
            else:
                print(f"📅 FECHA DE PUBLICACIÓN: N/A (sin fecha en el dataset)")
            
            if tender.closing_date:
                print(f"📅 FECHA DE CIERRE: {tender.closing_date.strftime('%d/%m/%Y')}")
            else:
                print(f"📅 FECHA DE CIERRE: N/A")
            
            print(f"📊 ESTADO: {tender.state}")
            print(f"🔗 URL DEL PROCESO: {tender.process_url}")
            print()
            print("📄 DESCRIPCIÓN / OBJETO:")
            print("-" * 100)
            print(tender.object_text[:400] + ("..." if len(tender.object_text) > 400 else ""))
            print()
            
            # Pause every 10 tenders
            if i % 10 == 0 and i < len(filtered_tenders):
                print(f"\n... Mostrando {i} de {len(filtered_tenders)} licitaciones. Presiona Enter para continuar...")
                try:
                    input()
                except:
                    pass
        
        print()
        print("=" * 100)
        print(f"✅ TOTAL: {len(filtered_tenders)} licitaciones mostradas")
        print("=" * 100)
        
        # Statistics
        with_dates = [t for t in filtered_tenders if t.publication_date]
        print()
        print("📊 ESTADÍSTICAS:")
        print(f"   • Total licitaciones: {len(filtered_tenders)}")
        print(f"   • Con fecha de publicación: {len(with_dates)}")
        print(f"   • Sin fecha de publicación: {len(filtered_tenders) - len(with_dates)}")
        
    else:
        print("⚠️  No se encontraron licitaciones en este rango de fechas")
        print()
        print("💡 Posibles razones:")
        print("   - No hay licitaciones con UNSPSC 81101500 publicadas desde agosto 2025")
        print("   - Las fechas pueden no estar disponibles en el dataset")
        print("   - Intenta ajustar el rango de fechas")
        
except Exception as e:
    print()
    print("=" * 100)
    print("❌ ERROR")
    print("=" * 100)
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

