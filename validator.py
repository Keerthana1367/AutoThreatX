from models.attacknode import AttackNode


def validate_node(node: AttackNode, parent: AttackNode) -> AttackNode:
    score = 0
    g = node.goal.lower()

    # Rule 1: single goal (no chaining)
    if " and " not in g:
        score += 1

    # Rule 2: reasonable length (avoid narratives)
    if len(node.goal) < 120:
        score += 1

    # Rule 3: hierarchy correctness
    if node.level > parent.level:
        score += 1

    # Rule 4: automotive relevance
    if parent.node_type in ["surface_goal", "attack_vector"]:
        score += 1
    else:
        if any(x in g for x in ["vehicle", "can", "ecu", "automotive", "firmware", "gateway"]):
            score += 1

    node.validation_score = score
    node.approved = score >= 2
    return node
