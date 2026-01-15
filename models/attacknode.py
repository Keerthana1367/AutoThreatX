from typing import List, Optional
from pydantic import BaseModel, Field
import uuid


class CVSSv3(BaseModel):
    attack_vector: str
    attack_complexity: str
    privileges_required: str
    user_interaction: str
    scope: str
    confidentiality: str
    integrity: str
    availability: str
    base_score: Optional[float] = None


class AttackNode(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    goal: str
    level: int
    node_type: str
    parent_id: Optional[str] = None

    # atomicity
    is_atomic: bool = False
    atomic_reason: Optional[str] = None
    attacker_role: Optional[str] = None

    # validation
    validation_score: int = 0
    approved: bool = False

    # risk
    cvss: Optional[CVSSv3] = None

    children: List["AttackNode"] = Field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "goal": self.goal,
            "level": self.level,
            "node_type": self.node_type,
            "parent_id": self.parent_id,
            "is_atomic": self.is_atomic,
            "atomic_reason": self.atomic_reason,
            "attacker_role": self.attacker_role,
            "validation_score": self.validation_score,
            "approved": self.approved,
            "cvss": self.cvss.dict() if self.cvss else None,
            "children": [c.to_dict() for c in self.children],
        }

    class Config:
        validate_assignment = True


AttackNode.update_forward_refs()
