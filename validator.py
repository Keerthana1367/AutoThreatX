from models.attacknode import AttackNode, CVSSv3
from validation_rules import *
from cvss import calculate_base_score


def validate_node(node: AttackNode, parent: AttackNode) -> AttackNode:
    score = 0

    # ---------------- VALIDATION RULES ----------------
    if rule_single_goal(node):
        score += 1

    if rule_goal_oriented(node):
        score += 1

    if rule_more_specific_than_parent(node, parent):
        score += 1

    if rule_automotive_relevant(node):
        score += 1

    node.validation_score = score
    node.approved = score >= 3

    # Do not decide atomicity too early
    if node.level < 2:
        return node

    # ---------------- ATOMIC + CVSS ----------------
    if node.approved and rule_atomic_stop(node):
        node.is_atomic = True
        node.atomic_reason = "Single concrete attacker action"

        # CVSS is assigned ONLY for atomic nodes
        metrics = {
            "AV": "N",   # Network
            "AC": "L",   # Low complexity
            "PR": "N",   # No privileges
            "UI": "N",   # No user interaction
            "C": "H",    # High confidentiality impact
            "I": "H",    # High integrity impact
            "A": "H",    # High availability impact
        }

        base_score = calculate_base_score(metrics)

        node.cvss = CVSSv3(
            attack_vector=metrics["AV"],
            attack_complexity=metrics["AC"],
            privileges_required=metrics["PR"],
            user_interaction=metrics["UI"],
            scope="U",
            confidentiality=metrics["C"],
            integrity=metrics["I"],
            availability=metrics["A"],
            base_score=base_score,
        )

    # ---------------- SAFETY CHECK ----------------
    if not rule_cvss_only_for_atomic(node):
        raise ValueError("CVSS assigned to non-atomic node")

    return node
