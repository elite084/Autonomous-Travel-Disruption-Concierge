from pydantic import BaseModel
from typing import List, Optional

class DisruptionEvent(BaseModel):
    trip_id: str
    flight_number: str
    disruption_type: str  # e.g., "Cancelled", "Delayed"
    reason: str
    user_automation_preference: int = 90  # Threshold out of 100

class RecoveryOption(BaseModel):
    option_id: str
    flight_details: str
    hotel_details: str
    benefits_applied: List[str]
    policy_compliant: bool
    jrs_score: int = 0
    confidence_level: int = 0

class RecoveryResponse(BaseModel):
    trip_id: str
    status: str
    selected_plan: Optional[RecoveryOption]
    requires_user_approval: bool