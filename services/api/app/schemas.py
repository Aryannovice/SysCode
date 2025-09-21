from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from enum import Enum

class ComponentType(str, Enum):
    DATABASE = "database"
    CACHE = "cache"
    LOAD_BALANCER = "load_balancer"
    API_GATEWAY = "api_gateway"
    MICROSERVICE = "microservice"
    MESSAGE_QUEUE = "message_queue"
    CDN = "cdn"
    SEARCH_ENGINE = "search_engine"

class DesignRequest(BaseModel):
    problem_statement: str
    requirements: List[str]
    scale_requirements: Optional[Dict[str, str]] = {}
    constraints: Optional[List[str]] = []

class DesignComponent(BaseModel):
    type: ComponentType
    name: str
    description: str
    rationale: str
    alternatives: List[str] = []

class DesignResponse(BaseModel):
    design_id: str
    analysis: str
    suggestions: List[str]
    components: List[DesignComponent]
    estimated_complexity: str

class FeedbackRequest(BaseModel):
    component_type: ComponentType
    component_details: Dict[str, Any]
    user_rationale: Optional[str] = ""
