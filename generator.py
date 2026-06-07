import json
import re
import time
from llm.llm_client import call_llm
from models.attacknode import AttackNode
from validator import validate_node
from utils import parse_numbered_list

LEVEL_CONFIG = {
    "surface_goal": {
        "child": "attack_vector",
        "prompt": """
Generate HIGH-LEVEL attack vectors that represent broad pathways
to achieve the attacker goal.

Attack vectors are:
- entry pathways (physical, wireless, supply-chain, insider, backend)
- NOT specific exploits
- NOT atomic actions
"""
    },

    "attack_vector": {
        "child": "method",
        "prompt": "Generate HIGH-LEVEL attack methods used within this attack vector."
    },

    "method": {
        "child": "technique",
        "prompt": "Generate concrete attack techniques for this attack method."
    },

    "technique": {
        "child": "sub_technique",
        "prompt": "Refine this technique into more specific sub-techniques."
    },

    "sub_technique": {
        "child": "procedure",
        "prompt": "Generate attacker procedures describing ordered actions."
    },

    "procedure": {
        "child": "atomic",
        "prompt": "Generate ATOMIC attacker actions that cannot be decomposed further."
    }
}



def generate_children(parent: AttackNode, min_n=1, max_n=3) -> list[AttackNode]:
    time.sleep(1.2)  # Rate limit spacing
    if parent.node_type not in LEVEL_CONFIG:
        return []

    cfg = LEVEL_CONFIG[parent.node_type]

    prompt = f"""
{cfg['prompt']}

Parent node:
"{parent.goal}"

Return the output as a JSON LIST of objects. 
Each object MUST have:
- "goal": description of the {cfg['child']}
- "cvss": estimated CVSS 3.1 score (float)
- "vector": estimated CVSS 3.1 vector string
- "feasibility": estimated feasibility (Easy, Medium, High)

Example:
[
  {{"goal": "...", "cvss": 7.5, "vector": "CVSS:3.1/...", "feasibility": "Medium"}},
  ...
]
"""

    response = call_llm(prompt)
    try:
        # Clean potential markdown
        cleaned = re.sub(r"^```[a-z]*\n?", "", response.strip(), flags=re.MULTILINE)
        cleaned = re.sub(r"```$", "", cleaned.strip())
        items = json.loads(cleaned)
    except:
        # Fallback to crude parsing if LLM fails JSON
        items = [{"goal": goal} for goal in parse_numbered_list(response)]

    children = []
    for item in items[:max_n]:
        goal_text = item.get("goal", "Unknown")
        node = AttackNode(
            goal=goal_text,
            level=parent.level + 1,
            node_type=cfg["child"],
            parent_id=parent.id,
            cvss=item.get("cvss", 0.0),
            cvss_vector=item.get("vector", "N/A"),
            feasibility=item.get("feasibility", "Medium")
        )

        node = validate_node(node, parent)

        if node.approved:
            children.append(node)

    return children
