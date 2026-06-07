# validation_rules.py

from models.attacknode import AttackNode


def rule_single_goal(node: AttackNode) -> bool:
    """
    Node must represent a single attacker goal.
    """
    bad_keywords = [" and ", " or ", "/", ","]
    goal_lower = node.goal.lower()
    return not any(k in goal_lower for k in bad_keywords)


def rule_goal_oriented(node: AttackNode) -> bool:
    """
    Node must describe an attacker goal, not a tool or defense.
    """
    forbidden = [
        "tool", "exploit", "patch", "firewall",
        "ids", "ips", "mitigation", "defense"
    ]
    goal_lower = node.goal.lower()
    return not any(f in goal_lower for f in forbidden)


def rule_smaller_than_parent(node: AttackNode, parent: AttackNode) -> bool:
    """
    Child node must be more specific than parent.
    """
    return len(node.goal) > len(parent.goal)


def rule_automotive_relevant(node: AttackNode) -> bool:
    """
    Node must be relevant to automotive cybersecurity.
    """
    automotive_terms = [
        "can", "ecu", "vehicle", "automotive",
        "telematics", "adas", "infotainment",
        "v2x", "sensor", "gateway"
    ]
    goal_lower = node.goal.lower()
    return any(term in goal_lower for term in automotive_terms)
