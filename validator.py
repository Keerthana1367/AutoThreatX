from models.attacknode import AttackNode
from validation_rules import *


def validate_node(node: AttackNode, parent: AttackNode) -> AttackNode:
    score = 0

    if rule_single_goal(node): score += 1
    if rule_goal_oriented(node): score += 1
    if rule_more_specific_than_parent(node, parent): score += 1
    if rule_automotive_relevant(node): score += 1

    node.validation_score = score
    node.approved = score >= 3

    if node.level < 2:
     return node


    if node.approved and rule_atomic_stop(node):
        node.is_atomic = True
        node.atomic_reason = "Atomic decision boundary satisfied"

    if not rule_cvss_only_for_atomic(node):
        raise ValueError("CVSS on non-atomic node")

    return node
