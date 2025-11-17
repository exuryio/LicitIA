"""Tender Pydantic schemas."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
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
    apertura_estado: Optional[str] = None  # Estado de apertura: "Abierto" o "Cerrado"
    process_url: str
    contract_type: Optional[str] = None
    contract_modality: Optional[str] = None
    relevance_score: Optional[float] = None
    is_relevant_interventoria_vial: bool
    # Experience matching
    experience_match_score: Optional[float] = Field(None, description="Match score against company experiences (0-1)")
    matching_experiences: Optional[List[dict]] = Field(None, description="List of matching experiences")
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TenderListResponse(BaseModel):
    """Paginated tender list response."""
    items: List[TenderResponse]
    total: int
    limit: int
    offset: int
