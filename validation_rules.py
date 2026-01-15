from models.attacknode import AttackNode


def rule_single_goal(node: AttackNode) -> bool:
    return not any(x in node.goal.lower() for x in [" and ", " or "])


def rule_goal_oriented(node: AttackNode) -> bool:
    forbidden = [
        "tool", "exploit", "patch", "firewall", "ids", "ips",
        "payload", "shellcode", "buffer", "offset", "memory"
    ]
    return not any(f in node.goal.lower() for f in forbidden)


def rule_more_specific_than_parent(node: AttackNode, parent: AttackNode) -> bool:
    return len(set(node.goal.lower().split()) -
               set(parent.goal.lower().split())) > 0


def rule_automotive_relevant(node: AttackNode) -> bool:
    keywords = [
        "can", "ecu", "vehicle", "telematics", "infotainment",
        "gateway", "obd", "adas", "firmware", "bus"
    ]
    return any(k in node.goal.lower() for k in keywords)


# -------- ATOMIC BOUNDARIES --------

def rule_single_action(node: AttackNode) -> bool:
    verbs = ["send", "inject", "replay", "modify", "upload", "bypass", "spoof", "forge"]
    return sum(1 for v in verbs if v in node.goal.lower()) <= 1


def rule_no_implementation_detail(node: AttackNode) -> bool:
    forbidden = ["byte", "bit", "stack", "heap", "opcode", "assembly"]
    return not any(f in node.goal.lower() for f in forbidden)


def rule_risk_scorable(node: AttackNode) -> bool:
    abstract = ["compromise", "attack", "manipulate"]
    return not any(a in node.goal.lower() for a in abstract)


def rule_atomic_stop(node: AttackNode) -> bool:
    return (
        rule_single_goal(node)
        and rule_single_action(node)
        and rule_no_implementation_detail(node)
        and rule_risk_scorable(node)
    )


def rule_cvss_only_for_atomic(node: AttackNode) -> bool:
    return node.cvss is None or node.is_atomic
