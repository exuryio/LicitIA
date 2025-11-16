"""Tender ingestion service - fetches, stores, classifies, and notifies."""
from datetime import datetime, timedelta
from app.core.db import SessionLocal
from app.core.logging import get_logger
from app.models.tender import Tender, TenderSource
from app.models.subscription import Subscription
from app.services.secop_client import fetch_recent_tenders
from app.services.classification import classify_tender_relevance
from app.services.notifications import send_email_alert, send_whatsapp_alert

logger = get_logger(__name__)


def fetch_and_store_new_tenders() -> None:
    """
    Main background job: fetch new tenders, classify, and send notifications.
    
    This function is called periodically by the scheduler.
    """
    db = SessionLocal()
    try:
        logger.info("Starting tender fetch job")
        
        # Determine since_timestamp: use the most recent tender's publication_date,
        # or default to 7 days ago if no tenders exist
        last_tender = db.query(Tender).order_by(Tender.publication_date.desc()).first()
        if last_tender and last_tender.publication_date:
            since_timestamp = last_tender.publication_date
        else:
            since_timestamp = datetime.utcnow() - timedelta(days=7)
        
        logger.info(f"Fetching tenders since {since_timestamp}")
        
        # Fetch from SECOP with filters for interventoría vial
        # Strategy 1: Filter by UNSPSC code 81101500 (Ingeniería Civil y Arquitectura)
        # Strategy 2: Also search by keywords as backup
        
        all_tenders = []
        seen_ids = set()
        
        # First, fetch by UNSPSC code (most precise filter)
        logger.info("Fetching tenders with UNSPSC code 81101500 (Ingeniería Civil y Arquitectura)")
        unspsc_tenders = fetch_recent_tenders(
            since_timestamp=since_timestamp,
            unspsc_code="81101500",
        )
        for tender in unspsc_tenders:
            if tender.external_id not in seen_ids:
                seen_ids.add(tender.external_id)
                all_tenders.append(tender)
        
        logger.info(f"Found {len(unspsc_tenders)} tenders with UNSPSC 81101500")
        
        # Also search by keywords to catch any missed tenders
        keywords = ["interventoría", "interventoria", "vial", "vías", "vias", "carretera", "malla vial"]
        logger.info("Also searching by keywords for interventoría vial")
        
        for keyword in keywords:
            tenders = fetch_recent_tenders(
                since_timestamp=since_timestamp,
                keyword_filter=keyword,
            )
            for tender in tenders:
                if tender.external_id not in seen_ids:
                    seen_ids.add(tender.external_id)
                    all_tenders.append(tender)
        
        secop_tenders = all_tenders
        logger.info(f"Found {len(secop_tenders)} unique tenders (UNSPSC + keywords)")
        
        new_tenders = []
        updated_count = 0
        
        for secop_tender in secop_tenders:
            try:
                # Check if tender already exists
                existing = db.query(Tender).filter(
                    Tender.external_id == secop_tender.external_id
                ).first()
                
                if existing:
                    # Update basic fields (but skip classification if already done)
                    existing.entity_name = secop_tender.entity_name
                    existing.object_text = secop_tender.object_text
                    existing.department = secop_tender.department
                    existing.municipality = secop_tender.municipality
                    existing.amount = secop_tender.amount
                    existing.publication_date = secop_tender.publication_date
                    existing.closing_date = secop_tender.closing_date
                    existing.state = secop_tender.state
                    existing.process_url = secop_tender.process_url
                    existing.updated_at = datetime.utcnow()
                    updated_count += 1
                    continue
                
                # Create new tender
                new_tender = Tender(
                    external_id=secop_tender.external_id,
                    source=TenderSource(secop_tender.source),
                    entity_name=secop_tender.entity_name,
                    object_text=secop_tender.object_text,
                    department=secop_tender.department,
                    municipality=secop_tender.municipality,
                    amount=secop_tender.amount,
                    publication_date=secop_tender.publication_date,
                    closing_date=secop_tender.closing_date,
                    state=secop_tender.state,
                    process_url=secop_tender.process_url,
                    contract_type=secop_tender.contract_type,
                    contract_modality=secop_tender.contract_modality,
                    is_relevant_interventoria_vial=False,  # Will be updated by classification
                )
                
                db.add(new_tender)
                new_tenders.append(new_tender)
            
            except Exception as e:
                logger.error(f"Error processing tender {secop_tender.external_id}: {e}")
                continue
        
        # Commit new tenders first
        db.commit()
        
        logger.info(f"Stored {len(new_tenders)} new tenders, updated {updated_count} existing")
        
        # Classify new tenders
        relevant_tenders = []
        for tender in new_tenders:
            try:
                # Refresh from DB to get the ID
                db.refresh(tender)
                
                # Classify
                classification = classify_tender_relevance(
                    tender.object_text,
                    tender.entity_name,
                )
                
                tender.relevance_score = classification["relevance_score"]
                tender.is_relevant_interventoria_vial = classification["is_relevant"]
                
                if classification["is_relevant"]:
                    relevant_tenders.append(tender)
            
            except Exception as e:
                logger.error(f"Error classifying tender {tender.id}: {e}")
                continue
        
        # Commit classification results
        db.commit()
        
        logger.info(f"Classified {len(new_tenders)} tenders, {len(relevant_tenders)} relevant")
        
        # Send notifications for relevant tenders
        for tender in relevant_tenders:
            try:
                # Find matching subscriptions
                subscriptions = db.query(Subscription).filter(
                    Subscription.active == True
                ).all()
                
                for subscription in subscriptions:
                    # Apply subscription filters
                    if subscription.only_relevant and not tender.is_relevant_interventoria_vial:
                        continue
                    
                    if subscription.min_amount and tender.amount:
                        if tender.amount < subscription.min_amount:
                            continue
                    
                    if subscription.max_amount and tender.amount:
                        if tender.amount > subscription.max_amount:
                            continue
                    
                    if subscription.departments:
                        if tender.department not in subscription.departments:
                            continue
                    
                    # Send notifications
                    send_email_alert(subscription, tender)
                    send_whatsapp_alert(subscription, tender)
            
            except Exception as e:
                logger.error(f"Error sending notifications for tender {tender.id}: {e}")
                continue
        
        logger.info("Tender fetch job completed successfully")
    
    except Exception as e:
        logger.error(f"Error in fetch_and_store_new_tenders: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()

