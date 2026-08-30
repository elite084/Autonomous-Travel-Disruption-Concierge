from fastapi import FastAPI, HTTPException
from models import DisruptionEvent, RecoveryResponse, RecoveryOption
from agents import aegis_orchestrator

app = FastAPI(title="Aegis Backend API", description="Autonomous Journey Recovery[cite: 1]")

@app.post("/api/v1/disruption/detect", response_model=RecoveryResponse)
async def handle_disruption(event: DisruptionEvent):
    """
    Endpoint triggered when a travel disruption is detected.[cite: 1]
    Launches the Multi-Agent AI System.[cite: 1]
    """
    try:
        # Initialize state for LangGraph
        initial_state = {
            "trip_id": event.trip_id,
            "disruption": event.dict(),
            "candidate_flights": [],
            "candidate_hotels": [],
            "benefits_evaluated": [],
            "policy_checked": False,
            "preferences_applied": False,
            "recovery_plans": [],
            "best_plan": {},
            "requires_approval": False
        }

        # Execute LangGraph Orchestrator[cite: 1]
        final_state = aegis_orchestrator.invoke(initial_state)

        best_plan = final_state.get("best_plan", {})
        
        selected_option = RecoveryOption(
            option_id=best_plan.get("option_id", "unknown"),
            flight_details=best_plan.get("flight_details", "unknown"),
            hotel_details=best_plan.get("hotel_details", "unknown"),
            benefits_applied=best_plan.get("benefits_applied", []),
            policy_compliant=best_plan.get("policy_compliant", False),
            jrs_score=best_plan.get("jrs_score", 0),
            confidence_level=best_plan.get("confidence_level", 0)
        )

        return RecoveryResponse(
            trip_id=event.trip_id,
            status="Recovery Plan Generated",
            selected_plan=selected_option,
            requires_user_approval=final_state["requires_approval"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))