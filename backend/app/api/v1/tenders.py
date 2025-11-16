"""Tender API endpoints."""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from uuid import UUID

from app.core.db import get_db
from app.models.tender import Tender
from app.schemas.tender import TenderResponse, TenderListResponse

router = APIRouter()


@router.get("/tenders", response_model=TenderListResponse)
async def list_tenders(
    is_relevant: bool = Query(True, description="Filter by relevance"),
    department: Optional[str] = Query(None, description="Filter by department"),
    contract_type: Optional[str] = Query(None, description="Filter by contract type (Tipo de contrato)"),
    contract_modality: Optional[str] = Query(None, description="Filter by contract modality (Modalidad de contratación)"),
    date_from: Optional[date] = Query(None, description="Filter by publication date from"),
    date_to: Optional[date] = Query(None, description="Filter by publication date to"),
    limit: int = Query(50, ge=1, le=100, description="Number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db),
):
    """List tenders with optional filters."""
    query = db.query(Tender)
    
    # Apply filters
    if is_relevant:
        query = query.filter(Tender.is_relevant_interventoria_vial == True)
    
    if department:
        query = query.filter(Tender.department.ilike(f"%{department}%"))
    
    if contract_type:
        query = query.filter(Tender.contract_type.ilike(f"%{contract_type}%"))
    
    if contract_modality:
        query = query.filter(Tender.contract_modality.ilike(f"%{contract_modality}%"))
    
    if date_from:
        query = query.filter(Tender.publication_date >= date_from)
    
    if date_to:
        query = query.filter(Tender.publication_date <= date_to)
    
    # Get total count
    total = query.count()
    
    # Apply pagination and ordering
    tenders = query.order_by(Tender.publication_date.desc()).offset(offset).limit(limit).all()
    
    return TenderListResponse(
        items=[TenderResponse.model_validate(t) for t in tenders],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/tenders/{tender_id}", response_model=TenderResponse)
async def get_tender(
    tender_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a single tender by ID."""
    tender = db.query(Tender).filter(Tender.id == tender_id).first()
    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found")
    return TenderResponse.model_validate(tender)

