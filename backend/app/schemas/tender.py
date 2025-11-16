"""Tender Pydantic schemas."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID


class TenderResponse(BaseModel):
    """Tender response schema."""
    id: UUID
    external_id: str
    source: str
    entity_name: str
    object_text: str
    department: Optional[str] = None
    municipality: Optional[str] = None
    amount: Optional[float] = None
    publication_date: Optional[datetime] = None
    closing_date: Optional[datetime] = None
    state: str
    process_url: str
    contract_type: Optional[str] = None
    contract_modality: Optional[str] = None
    relevance_score: Optional[float] = None
    is_relevant_interventoria_vial: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TenderListResponse(BaseModel):
    """Paginated tender list response."""
    items: list[TenderResponse]
    total: int
    limit: int
    offset: int

