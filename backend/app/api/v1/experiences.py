"""Company Experience API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import tempfile
import os

from app.core.db import get_db
from app.models.company_experience import CompanyExperience
from app.schemas.company_experience import (
    CompanyExperienceCreate,
    CompanyExperienceResponse,
    CompanyExperienceListResponse,
    ExcelImportResponse
)
from app.services.excel_import import import_experiences_from_excel
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/experiences", response_model=CompanyExperienceResponse, status_code=201)
async def create_experience(
    experience: CompanyExperienceCreate,
    db: Session = Depends(get_db),
):
    """Create a new company experience."""
    from app.services.experience_matching import extract_keywords
    import json
    
    # Extract keywords
    keywords = extract_keywords(experience.project_description)
    keywords_json = json.dumps(keywords) if keywords else None
    
    db_experience = CompanyExperience(
        **experience.model_dump(),
        keywords=keywords_json
    )
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    
    # Parse keywords for response
    response_data = CompanyExperienceResponse.model_validate(db_experience)
    if db_experience.keywords:
        response_data.keywords = json.loads(db_experience.keywords)
    
    return response_data


@router.get("/experiences", response_model=CompanyExperienceListResponse)
async def list_experiences(
    company_name: Optional[str] = Query(None, description="Filter by company name"),
    limit: int = Query(100, ge=1, le=1000, description="Number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db),
):
    """List company experiences."""
    query = db.query(CompanyExperience)
    
    if company_name:
        query = query.filter(CompanyExperience.company_name.ilike(f"%{company_name}%"))
    
    total = query.count()
    # Handle None completion_date for ordering
    from sqlalchemy import case
    experiences = query.order_by(
        case((CompanyExperience.completion_date.is_(None), 1), else_=0),
        CompanyExperience.completion_date.desc()
    ).offset(offset).limit(limit).all()
    
    # Parse keywords for response
    import json
    items = []
    for exp in experiences:
        # Create a dict from the model, parse keywords, then validate
        exp_dict = {
            "id": exp.id,
            "company_name": exp.company_name,
            "contract_number": exp.contract_number,
            "project_description": exp.project_description,
            "contracting_entity": exp.contracting_entity,
            "completion_date": exp.completion_date,
            "amount": float(exp.amount) if exp.amount else None,
            "category": exp.category,
            "engineering_area": exp.engineering_area,
            "keywords": json.loads(exp.keywords) if exp.keywords else None,
            "created_at": exp.created_at,
            "updated_at": exp.updated_at,
        }
        exp_data = CompanyExperienceResponse.model_validate(exp_dict)
        items.append(exp_data)
    
    return CompanyExperienceListResponse(items=items, total=total)


@router.get("/experiences/{experience_id}", response_model=CompanyExperienceResponse)
async def get_experience(
    experience_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a single experience by ID."""
    experience = db.query(CompanyExperience).filter(CompanyExperience.id == experience_id).first()
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    
    import json
    # Create a dict from the model, parse keywords, then validate
    exp_dict = {
        "id": experience.id,
        "company_name": experience.company_name,
        "contract_number": experience.contract_number,
        "project_description": experience.project_description,
        "contracting_entity": experience.contracting_entity,
        "completion_date": experience.completion_date,
        "amount": float(experience.amount) if experience.amount else None,
        "category": experience.category,
        "engineering_area": experience.engineering_area,
        "keywords": json.loads(experience.keywords) if experience.keywords else None,
        "created_at": experience.created_at,
        "updated_at": experience.updated_at,
    }
    response_data = CompanyExperienceResponse.model_validate(exp_dict)
    return response_data


@router.post("/experiences/import", response_model=ExcelImportResponse)
async def import_experiences(
    file: UploadFile = File(..., description="Excel file with company experiences"),
    company_name: str = Query("BEC", description="Company name (defaults to BEC)"),
    db: Session = Depends(get_db),
):
    """
    Import company experiences from Excel file.
    
    Expected columns:
    - EMPRESA
    - CONTRATO No.
    - OBRA (required)
    - ENTIDAD CONTRATANTE
    - FECHA FINALIZACIÓN
    - VALOR ACTUAL
    - CATEGORÍA
    - ÁREA DE LA INGENIERÍA CIVIL
    """
    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="File must be an Excel file (.xlsx or .xls)")
    
    # Save uploaded file to temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
        try:
            # Read file content
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
            
            # Import experiences
            imported, errors = import_experiences_from_excel(tmp_file_path, company_name)
            
            if errors:
                message = f"Imported {imported} experiences with {len(errors)} errors"
            else:
                message = f"Successfully imported {imported} experiences"
            
            return ExcelImportResponse(
                imported=imported,
                errors=errors,
                message=message
            )
        
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)


@router.delete("/experiences/{experience_id}", status_code=204)
async def delete_experience(
    experience_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete an experience."""
    experience = db.query(CompanyExperience).filter(CompanyExperience.id == experience_id).first()
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    
    db.delete(experience)
    db.commit()
    return None

