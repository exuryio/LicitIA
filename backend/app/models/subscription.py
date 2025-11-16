"""Subscription model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Numeric, DateTime, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import Base


class Subscription(Base):
    """Subscription model for companies that want to receive tender alerts."""
    
    __tablename__ = "subscriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(String(255), nullable=False)
    contact_name = Column(String(255), nullable=False)
    contact_email = Column(String(255), nullable=False, index=True)
    whatsapp_number = Column(String(50), nullable=False)
    active = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    min_amount = Column(Numeric(18, 2), nullable=True)
    max_amount = Column(Numeric(18, 2), nullable=True)
    departments = Column(JSON, nullable=True)  # List of department names
    only_relevant = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<Subscription(id={self.id}, company={self.company_name}, email={self.contact_email})>"

