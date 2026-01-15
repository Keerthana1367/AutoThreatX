from models.attacknode import AttackNode
from validator import validate_node
from llm.llm_client import call_llm
from config import LEVEL_CONFIG


def parse_numbered_list(text: str) -> list[str]:
    return [
        l.split(".", 1)[1].strip()
        for l in text.splitlines()
        if l.strip() and l[0].isdigit() and "." in l
    ]


def generate_children(parent: AttackNode) -> list[AttackNode]:
    if parent.is_atomic:
        return []

    if parent.node_type not in LEVEL_CONFIG:
        return []

    cfg = LEVEL_CONFIG[parent.node_type]

    prompt = f"""
Generate {cfg['min']} to {cfg['max']} DISTINCT {cfg['child_type']} goals
for automotive cybersecurity.

Parent goal:
"{parent.goal}"

Rules:
- Single attacker goal
- No tools, exploits, or defenses
- No implementation details
- Output ONLY a numbered list
"""

    items = parse_numbered_list(call_llm(prompt))
    children = []

    for text in items:
        node = AttackNode(
            goal=text,
            level=parent.level + 1,
            node_type=cfg["child_type"],
            parent_id=parent.id
        )

        node = validate_node(node, parent)
        if node.approved:
            children.append(node)

    return children
