from typing import List, Optional
from pydantic import BaseModel, Field
import uuid


class AttackNode(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    goal: str
    level: int
    node_type: str                 # REQUIRED
    parent_id: Optional[str] = None

    validation_score: int = 0
    approved: bool = False
    
    cvss: float = 0.0
    cvss_vector: str = "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N"
    feasibility: str = "Medium"
    impact: str = "Medium"

    children: List["AttackNode"] = Field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "goal": self.goal,
            "level": self.level,
            "node_type": self.node_type,
            "parent_id": self.parent_id,
            "validation_score": self.validation_score,
            "approved": self.approved,
            "cvss": self.cvss,
            "cvss_vector": self.cvss_vector,
            "feasibility": self.feasibility,
            "impact": self.impact,
            "children": [child.to_dict() for child in self.children],
        }

    class Config:
        validate_assignment = True


AttackNode.update_forward_refs()
