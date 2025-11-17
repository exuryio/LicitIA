"""Experience matching service - matches tenders against company experiences."""
import json
import re
from typing import List, Dict, Optional, Tuple
from app.models.tender import Tender
from app.models.company_experience import CompanyExperience
from app.core.logging import get_logger

logger = get_logger(__name__)

# Matching weights (sum should be ~1.0)
WEIGHTS = {
    "keyword": 0.50,  # Keywords from project description
    "amount": 0.25,   # Amount similarity
    "entity": 0.15,   # Entity name similarity
    "category": 0.10, # Category/engineering area match
}

# Minimum match threshold
MIN_MATCH_THRESHOLD = 0.60


def extract_keywords(text: str) -> List[str]:
    """
    Extract relevant keywords from text for matching.
    
    Focuses on interventoría-related terms and technical keywords.
    """
    if not text:
        return []
    
    text_lower = text.lower()
    
    # Common interventoría-related keywords
    interventoria_keywords = [
        "interventoría", "interventoria", "supervisión", "supervision",
        "vial", "vías", "vias", "carretera", "malla vial",
        "obra", "obras", "construcción", "construccion",
        "mantenimiento", "mejoramiento", "rehabilitación", "rehabilitacion",
        "diseño", "diseno", "estudio", "estudios",
        "técnica", "tecnica", "administrativa", "ambiental",
        "puente", "puentes", "infraestructura",
    ]
    
    # Extract words that match our keywords
    words = re.findall(r'\b\w+\b', text_lower)
    keywords = [word for word in words if word in interventoria_keywords]
    
    # Also extract significant words (length > 5, not common stop words)
    stop_words = {"para", "del", "los", "las", "con", "por", "que", "una", "uno"}
    significant_words = [
        word for word in words 
        if len(word) > 5 and word not in stop_words and word not in keywords
    ]
    
    # Combine and deduplicate
    all_keywords = list(set(keywords + significant_words[:10]))  # Limit significant words
    
    return all_keywords


def calculate_keyword_score(tender_text: str, experience_keywords: List[str]) -> float:
    """
    Calculate keyword matching score between tender and experience.
    
    Returns score between 0.0 and 1.0.
    """
    if not experience_keywords:
        return 0.0
    
    tender_lower = tender_text.lower()
    
    # Count matches
    matches = sum(1 for keyword in experience_keywords if keyword in tender_lower)
    
    if matches == 0:
        return 0.0
    
    # Score based on percentage of keywords matched
    match_ratio = matches / len(experience_keywords)
    
    # Boost score if multiple matches (exponential)
    if matches >= 3:
        return min(1.0, match_ratio * 1.3)
    elif matches >= 2:
        return min(1.0, match_ratio * 1.2)
    
    return match_ratio


def calculate_amount_score(tender_amount: Optional[float], experience_amount: Optional[float]) -> float:
    """
    Calculate amount similarity score.
    
    Returns score between 0.0 and 1.0.
    """
    if not tender_amount or not experience_amount:
        return 0.5  # Neutral score if either is missing
    
    # Calculate ratio
    if experience_amount == 0:
        return 0.5
    
    ratio = tender_amount / experience_amount
    
    # Score based on how close the amounts are
    if 0.5 <= ratio <= 2.0:  # Within 2x range
        return 1.0
    elif 0.25 <= ratio <= 4.0:  # Within 4x range
        return 0.8
    elif 0.1 <= ratio <= 10.0:  # Within 10x range
        return 0.6
    else:
        return 0.3


def calculate_entity_score(tender_entity: str, experience_entity: Optional[str]) -> float:
    """
    Calculate entity name similarity score.
    
    Returns score between 0.0 and 1.0.
    """
    if not experience_entity:
        return 0.5  # Neutral if no experience entity
    
    tender_lower = tender_entity.lower()
    experience_lower = experience_entity.lower()
    
    # Exact match
    if tender_lower == experience_lower:
        return 1.0
    
    # Partial match (entity name contains or is contained)
    if tender_lower in experience_lower or experience_lower in tender_lower:
        return 0.7
    
    # Word overlap
    tender_words = set(tender_lower.split())
    experience_words = set(experience_lower.split())
    common_words = tender_words.intersection(experience_words)
    
    if len(common_words) > 0:
        return 0.4
    
    return 0.0


def calculate_category_score(tender: Tender, experience: CompanyExperience) -> float:
    """
    Calculate category/engineering area match score.
    
    Returns score between 0.0 and 1.0.
    """
    # If experience has engineering_area, check if it matches tender keywords
    if experience.engineering_area:
        area_lower = experience.engineering_area.lower()
        tender_text = (tender.object_text or "").lower()
        
        # Check for key terms in engineering area
        if "vial" in area_lower or "vias" in area_lower or "carretera" in area_lower:
            if any(term in tender_text for term in ["vial", "vias", "carretera", "malla"]):
                return 1.0
        
        if "construccion" in area_lower or "obra" in area_lower:
            if any(term in tender_text for term in ["obra", "construccion", "construcción"]):
                return 0.8
    
    # Category match - check if experience category matches tender keywords
    # No longer depends on is_relevant_interventoria_vial - matching is based on actual experience
    if experience.category and "interventoría" in experience.category.lower():
        # Check if tender text contains interventoría-related keywords
        tender_text = (tender.object_text or "").lower()
        if any(term in tender_text for term in ["interventoría", "interventoria", "supervisión", "supervision"]):
            return 1.0
    
    return 0.5  # Neutral if no specific match


def match_tender_against_experiences(
    tender: Tender,
    experiences: List[CompanyExperience],
    min_score: float = MIN_MATCH_THRESHOLD
) -> Tuple[float, List[Dict]]:
    """
    Match a tender against company experiences.
    
    Args:
        tender: The tender to match
        experiences: List of company experiences
        min_score: Minimum score to consider a match
        
    Returns:
        Tuple of (best_match_score, list_of_matching_experiences)
    """
    if not experiences:
        return 0.0, []
    
    matches = []
    
    for experience in experiences:
        # Calculate individual scores
        keyword_score = calculate_keyword_score(
            tender.object_text or "",
            json.loads(experience.keywords) if experience.keywords else []
        )
        
        amount_score = calculate_amount_score(
            float(tender.amount) if tender.amount else None,
            float(experience.amount) if experience.amount else None
        )
        
        entity_score = calculate_entity_score(
            tender.entity_name or "",
            experience.contracting_entity
        )
        
        category_score = calculate_category_score(tender, experience)
        
        # Calculate weighted total score
        total_score = (
            WEIGHTS["keyword"] * keyword_score +
            WEIGHTS["amount"] * amount_score +
            WEIGHTS["entity"] * entity_score +
            WEIGHTS["category"] * category_score
        )
        
        # Only include if above threshold
        if total_score >= min_score:
            matches.append({
                "experience_id": str(experience.id),
                "project_description": experience.project_description[:100] + "..." if len(experience.project_description) > 100 else experience.project_description,
                "contracting_entity": experience.contracting_entity,
                "amount": float(experience.amount) if experience.amount else None,
                "score": round(total_score, 3),
                "scores": {
                    "keyword": round(keyword_score, 3),
                    "amount": round(amount_score, 3),
                    "entity": round(entity_score, 3),
                    "category": round(category_score, 3),
                }
            })
    
    # Sort by score descending
    matches.sort(key=lambda x: x["score"], reverse=True)
    
    # Return best score and top matches (limit to 5)
    best_score = matches[0]["score"] if matches else 0.0
    top_matches = matches[:5]
    
    return best_score, top_matches


def match_all_tenders_against_experiences(
    tenders: List[Tender],
    experiences: List[CompanyExperience],
    min_score: float = MIN_MATCH_THRESHOLD
) -> Dict[str, Tuple[float, List[Dict]]]:
    """
    Match multiple tenders against experiences.
    
    Returns a dictionary mapping tender_id to (score, matches).
    """
    results = {}
    
    for tender in tenders:
        score, matches = match_tender_against_experiences(tender, experiences, min_score)
        results[str(tender.id)] = (score, matches)
    
    return results

