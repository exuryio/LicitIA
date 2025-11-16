"""Subscription Pydantic schemas."""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class SubscriptionCreate(BaseModel):
    """Schema for creating a subscription."""
    company_name: str
    contact_name: str
    contact_email: EmailStr
    whatsapp_number: str
    min_amount: Optional[Decimal] = None
    max_amount: Optional[Decimal] = None
    departments: Optional[List[str]] = None
    only_relevant: bool = True


class SubscriptionUpdate(BaseModel):
    """Schema for updating a subscription."""
    company_name: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    whatsapp_number: Optional[str] = None
    active: Optional[bool] = None
    min_amount: Optional[Decimal] = None
    max_amount: Optional[Decimal] = None
    departments: Optional[List[str]] = None
    only_relevant: Optional[bool] = None


class SubscriptionResponse(BaseModel):
    """Subscription response schema."""
    id: UUID
    company_name: str
    contact_name: str
    contact_email: str
    whatsapp_number: str
    active: bool
    created_at: datetime
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    departments: Optional[List[str]] = None
    only_relevant: bool
    
    class Config:
        from_attributes = True

