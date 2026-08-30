from typing import TypedDict, List
from langgraph.graph import StateGraph, END
import random

# Define the state for the LangGraph orchestrator
class JourneyState(TypedDict):
    trip_id: str
    disruption: dict
    candidate_flights: List[dict]
    candidate_hotels: List[dict]
    benefits_evaluated: List[dict]
    policy_checked: bool
    preferences_applied: bool
    recovery_plans: List[dict]
    best_plan: dict
    requires_approval: bool

def flight_agent(state: JourneyState) -> JourneyState:
    """Evaluates available flight recovery options.[cite: 1]"""
    # Mocking Amadeus API response[cite: 1]
    state["candidate_flights"] = [
        {"id": "f1", "airline": "Preferred Air", "delay_mins": 120, "cost": 0, "risk_of_delay": "Low"},
        {"id": "f2", "airline": "Alt Air", "delay_mins": 60, "cost": 150, "risk_of_delay": "Medium"}
    ]
    return state

def hotel_agent(state: JourneyState) -> JourneyState:
    """Manages hotel updates and coordination.[cite: 1]"""
    # Mocking Hotel Booking API response[cite: 1]
    state["candidate_hotels"] = [
        {"id": "h1", "action": "Keep Reservation", "cost": 0},
        {"id": "h2", "action": "Late Check-in Approved", "cost": 20}
    ]
    return state

def benefits_agent(state: JourneyState) -> JourneyState:
    """Evaluates travel benefits like lounge access.[cite: 1]"""
    state["benefits_evaluated"] = [
        {"flight_id": "f1", "benefits": ["Lounge Access Included"]},
        {"flight_id": "f2", "benefits": []}
    ]
    return state

def policy_agent(state: JourneyState) -> JourneyState:
    """Validates options against travel policies.[cite: 1]"""
    state["policy_checked"] = True
    return state

def preference_agent(state: JourneyState) -> JourneyState:
    """Applies user preferences using the Digital Traveler Twin.[cite: 1]"""
    state["preferences_applied"] = True
    return state

def jrs_engine(state: JourneyState) -> JourneyState:
    """
    Calculates the Journey Recovery Score based on:
    - Arrival delay[cite: 1]
    - Total recovery cost[cite: 1]
    - Traveler preferences[cite: 1]
    - Loyalty benefit utilization[cite: 1]
    - Risk of further disruption[cite: 1]
    """
    plans = []
    for flight in state["candidate_flights"]:
        # Mocking the JRS algorithm weights
        base_score = 100
        delay_penalty = flight["delay_mins"] * 0.2
        cost_penalty = flight["cost"] * 0.1
        
        # Check benefits
        benefit_bonus = 10 if any(b["flight_id"] == flight["id"] and b["benefits"] for b in state["benefits_evaluated"]) else 0
        
        risk_penalty = 15 if flight["risk_of_delay"] == "Medium" else 0
        
        jrs = int(base_score - delay_penalty - cost_penalty + benefit_bonus - risk_penalty)
        
        # Mock confidence level calculation
        confidence = jrs - random.randint(0, 10)
        
        plans.append({
            "option_id": f"plan_{flight['id']}",
            "flight_details": flight["airline"],
            "hotel_details": "Updated",
            "benefits_applied": ["Lounge Access"] if benefit_bonus > 0 else [],
            "policy_compliant": state["policy_checked"],
            "jrs_score": jrs,
            "confidence_level": confidence
        })
    
    state["recovery_plans"] = plans
    # Select plan with highest score[cite: 1]
    state["best_plan"] = max(plans, key=lambda x: x["jrs_score"])
    
    # Confidence Threshold Check[cite: 1]
    user_threshold = state["disruption"].get("user_automation_preference", 90)
    state["requires_approval"] = state["best_plan"]["confidence_level"] < user_threshold
    
    return state

# Build the LangGraph workflow
workflow = StateGraph(JourneyState)

workflow.add_node("flight_agent", flight_agent)
workflow.add_node("hotel_agent", hotel_agent)
workflow.add_node("benefits_agent", benefits_agent)
workflow.add_node("policy_agent", policy_agent)
workflow.add_node("preference_agent", preference_agent)
workflow.add_node("jrs_engine", jrs_engine)

workflow.set_entry_point("flight_agent")
workflow.add_edge("flight_agent", "hotel_agent")
workflow.add_edge("hotel_agent", "benefits_agent")
workflow.add_edge("benefits_agent", "policy_agent")
workflow.add_edge("policy_agent", "preference_agent")
workflow.add_edge("preference_agent", "jrs_engine")
workflow.add_edge("jrs_engine", END)

aegis_orchestrator = workflow.compile()