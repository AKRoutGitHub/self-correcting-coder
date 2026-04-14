from typing import TypedDict, Optional

class AgentState(TypedDict):
    task: str
    code: str
    error: Optional[str]
    iterations: int