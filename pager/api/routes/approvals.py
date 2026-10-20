from fastapi import APIRouter, HTTPException

from pager.storage.schemas import DecisionIn

router = APIRouter(tags=["approvals"])


@router.post("/actions/{action_id}/decision")
def decide(action_id: str, body: DecisionIn) -> None:
    """Reserved for the approval gate. The body is validated now; execution comes next."""
    raise HTTPException(
        status_code=501,
        detail={"code": "not_ready", "message": "Approval decisions are not wired yet.", "action_id": action_id, "decision": body.decision},
    )
