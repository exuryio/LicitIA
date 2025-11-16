"""OpenAI-based relevance classification for tenders."""
import json
from typing import Dict, Optional
from openai import OpenAI
from app.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Initialize OpenAI client
openai_client = None
if settings.OPENAI_API_KEY:
    openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)


def classify_tender_relevance(object_text: str, entity_name: Optional[str] = None) -> Dict[str, any]:
    """
    Classify if a tender is relevant for road supervision (interventoría vial).
    
    Args:
        object_text: The tender object description
        entity_name: Optional entity name for context
        
    Returns:
        Dict with 'is_relevant' (bool) and 'relevance_score' (float 0-1)
    """
    # Fallback result
    default_result = {
        "is_relevant": False,
        "relevance_score": 0.0,
    }
    
    # If OpenAI is not configured, use keyword fallback
    if not openai_client:
        logger.warning("OpenAI client not configured, using keyword fallback")
        return _keyword_fallback(object_text, entity_name)
    
    try:
        # Build prompt
        prompt_text = f"""Objeto del proceso: {object_text}"""
        if entity_name:
            prompt_text += f"\nEntidad: {entity_name}"
        
        system_prompt = """Eres un clasificador de licitaciones públicas colombianas. 
Tu tarea es determinar si una licitación corresponde a "interventoría de vías" (supervisión de obras viales, carreteras, malla vial).

Responde ÚNICAMENTE en formato JSON válido con esta estructura exacta:
{
  "is_relevant": true o false,
  "relevance_score": un número entre 0.0 y 1.0
}

Donde:
- is_relevant: true si la licitación es claramente de interventoría vial, false en caso contrario
- relevance_score: 0.0 a 1.0 indicando qué tan relevante es (1.0 = muy relevante, 0.0 = no relevante)

Solo considera relevante si se trata específicamente de supervisión, interventoría, o control de calidad de obras viales/carreteras."""
        
        response = openai_client.chat.completions.create(
            model=settings.OPENAI_MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_text},
            ],
            temperature=0.1,
            max_tokens=200,
        )
        
        content = response.choices[0].message.content.strip()
        
        # Try to parse JSON response
        # Sometimes OpenAI wraps JSON in markdown code blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        result = json.loads(content)
        
        # Validate result structure
        if "is_relevant" not in result or "relevance_score" not in result:
            logger.warning("OpenAI response missing required fields, using fallback")
            return _keyword_fallback(object_text, entity_name)
        
        # Ensure types are correct
        result["is_relevant"] = bool(result["is_relevant"])
        result["relevance_score"] = float(result.get("relevance_score", 0.0))
        result["relevance_score"] = max(0.0, min(1.0, result["relevance_score"]))
        
        return result
    
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to parse OpenAI JSON response: {e}, using fallback")
        return _keyword_fallback(object_text, entity_name)
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}, using fallback")
        return _keyword_fallback(object_text, entity_name)


def _keyword_fallback(object_text: str, entity_name: Optional[str] = None) -> Dict[str, any]:
    """
    Fallback keyword-based classification.
    
    Returns:
        Dict with 'is_relevant' and 'relevance_score'
    """
    text_lower = (object_text or "").lower()
    if entity_name:
        text_lower += " " + entity_name.lower()
    
    # Keywords that indicate road supervision
    relevant_keywords = [
        "interventoría",
        "interventoria",
        "vial",
        "vías",
        "vias",
        "carretera",
        "malla vial",
        "supervisión de vías",
        "supervision de vias",
        "obra vial",
        "infraestructura vial",
    ]
    
    # Check for keyword matches
    matches = sum(1 for keyword in relevant_keywords if keyword in text_lower)
    
    if matches > 0:
        # Score based on number of matches (capped at 0.8 for fallback)
        score = min(0.8, 0.3 + (matches * 0.1))
        return {
            "is_relevant": True,
            "relevance_score": score,
        }
    
    return {
        "is_relevant": False,
        "relevance_score": 0.0,
    }

