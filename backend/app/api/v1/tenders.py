"""Tender API endpoints."""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date, datetime
from uuid import UUID

from app.core.db import get_db
from app.models.tender import Tender
from app.models.company_experience import CompanyExperience
from app.schemas.tender import TenderResponse, TenderListResponse
from app.services.experience_matching import match_tender_against_experiences, MIN_MATCH_THRESHOLD

router = APIRouter()


@router.get("/tenders", response_model=TenderListResponse)
async def list_tenders(
    department: Optional[str] = Query(None, description="Filter by department"),
    contract_type: Optional[str] = Query(None, description="Filter by contract type (Tipo de contrato)"),
    contract_modality: Optional[str] = Query(None, description="Filter by contract modality (Modalidad de contratación)"),
    date_from: Optional[date] = Query(None, description="Filter by publication date from"),
    date_to: Optional[date] = Query(None, description="Filter by publication date to"),
    match_experience: bool = Query(False, description="Only show tenders matching company experiences"),
    min_match_score: float = Query(MIN_MATCH_THRESHOLD, ge=0.0, le=1.0, description="Minimum match score (0-1)"),
    company_name: Optional[str] = Query(None, description="Company name for experience matching"),
    limit: int = Query(50, ge=1, le=1000, description="Number of results (higher limit allowed for experience matching)"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db),
):
    """List tenders with optional filters and experience matching."""
    query = db.query(Tender)
    
    # Apply filters (relevance filter removed - experience matching is the main feature)
    
    if department:
        # Search in both department and municipality fields
        # This allows users to search for cities (municipios) as well as departments
        query = query.filter(
            (Tender.department.ilike(f"%{department}%")) |
            (Tender.municipality.ilike(f"%{department}%"))
        )
    
    if contract_type:
        query = query.filter(Tender.contract_type.ilike(f"%{contract_type}%"))
    
    if contract_modality:
        query = query.filter(Tender.contract_modality.ilike(f"%{contract_modality}%"))
    
    if date_from:
        query = query.filter(Tender.publication_date >= date_from)
    
    if date_to:
        query = query.filter(Tender.publication_date <= date_to)
    
    # Experience matching setup
    experiences = []
    if match_experience or company_name:
        exp_query = db.query(CompanyExperience)
        if company_name:
            exp_query = exp_query.filter(CompanyExperience.company_name.ilike(f"%{company_name}%"))
        experiences = exp_query.all()
    
    # If matching is required, we need to match ALL tenders first, then paginate
    if match_experience and experiences:
        # Get ALL tenders (no pagination yet) for matching
        # Order by publication_date DESC, with NULL values last
        all_tenders = query.order_by(
            Tender.publication_date.desc().nulls_last()
        ).all()
        
        # Match and filter all tenders
        matched_items = []
        for tender in all_tenders:
            match_score, matching_experiences = match_tender_against_experiences(
                tender, experiences, min_score=min_match_score
            )
            
            # Only include if matches threshold
            if match_score >= min_match_score:
                tender_response = TenderResponse.model_validate(tender)
                tender_response.experience_match_score = match_score
                tender_response.matching_experiences = matching_experiences if matching_experiences else None
                matched_items.append(tender_response)
        
        # Sort by publication date (most recent first), then by match score as secondary criteria
        # Handle None dates by putting them at the end
        # Use a tuple where first element is 0 for None dates (so they sort last when reverse=True)
        # and 1 for dates (so they sort first)
        matched_items.sort(
            key=lambda x: (
                0 if x.publication_date is None else 1,  # Put None dates last
                x.publication_date if x.publication_date is not None else datetime.min,
                x.experience_match_score or 0.0
            ),
            reverse=True
        )
        
        # Now apply pagination to matched results
        total = len(matched_items)
        items = matched_items[offset:offset + limit]
        
    else:
        # Normal flow: paginate first, then match (for display purposes only)
        # Order by publication_date DESC, with NULL values last
        total = query.count()
        tenders = query.order_by(
            Tender.publication_date.desc().nulls_last()
        ).offset(offset).limit(limit).all()
        
        # Build response with match scores (optional, for display)
        items = []
        for tender in tenders:
            tender_response = TenderResponse.model_validate(tender)
            
            if experiences:
                match_score, matching_experiences = match_tender_against_experiences(
                    tender, experiences, min_score=min_match_score
                )
                tender_response.experience_match_score = match_score if match_score > 0 else None
                tender_response.matching_experiences = matching_experiences if matching_experiences else None
            
            items.append(tender_response)
    
    return TenderListResponse(
        items=items,
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/tenders/{tender_id}", response_model=TenderResponse)
async def get_tender(
    tender_id: UUID,
    company_name: Optional[str] = Query(None, description="Company name for experience matching"),
    db: Session = Depends(get_db),
):
    """Get a single tender by ID with optional experience matching."""
    tender = db.query(Tender).filter(Tender.id == tender_id).first()
    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found")
    
    tender_response = TenderResponse.model_validate(tender)
    
    # Add experience matching if company_name provided
    if company_name:
        experiences = db.query(CompanyExperience).filter(
            CompanyExperience.company_name.ilike(f"%{company_name}%")
        ).all()
        
        if experiences:
            match_score, matching_experiences = match_tender_against_experiences(
                tender, experiences, min_score=MIN_MATCH_THRESHOLD
            )
            tender_response.experience_match_score = match_score if match_score > 0 else None
            tender_response.matching_experiences = matching_experiences if matching_experiences else None
    
    return tender_response

