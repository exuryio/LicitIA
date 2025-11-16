"""Subscription API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.db import get_db
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse

router = APIRouter()


@router.post("/subscriptions", response_model=SubscriptionResponse, status_code=201)
async def create_subscription(
    subscription: SubscriptionCreate,
    db: Session = Depends(get_db),
):
    """Create a new subscription."""
    db_subscription = Subscription(**subscription.model_dump())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return SubscriptionResponse.model_validate(db_subscription)


@router.get("/subscriptions", response_model=List[SubscriptionResponse])
async def list_subscriptions(
    db: Session = Depends(get_db),
):
    """List all subscriptions."""
    subscriptions = db.query(Subscription).order_by(Subscription.created_at.desc()).all()
    return [SubscriptionResponse.model_validate(s) for s in subscriptions]


@router.get("/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
async def get_subscription(
    subscription_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a single subscription by ID."""
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return SubscriptionResponse.model_validate(subscription)


@router.patch("/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
async def update_subscription(
    subscription_id: UUID,
    subscription_update: SubscriptionUpdate,
    db: Session = Depends(get_db),
):
    """Update a subscription."""
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    # Update only provided fields
    update_data = subscription_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(subscription, field, value)
    
    db.commit()
    db.refresh(subscription)
    return SubscriptionResponse.model_validate(subscription)

