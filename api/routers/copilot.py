from fastapi import APIRouter
from pydantic import BaseModel

from copilot.procurement_copilot import ask_copilot

router = APIRouter(
    prefix="/copilot",
    tags=["Copilot"]
)


class CopilotRequest(BaseModel):

    question: str
    context: str


@router.post("/")
def copilot(request: CopilotRequest):

    answer = ask_copilot(
        request.question,
        request.context
    )

    return {
        "answer": answer
    }