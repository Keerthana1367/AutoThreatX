import json
from models.attacknode import AttackNode
from generator import generate_children
from db import get_tree, save_tree


def expand_tree(node: AttackNode, max_depth: int | None = None):
    """
    Recursively expand attack tree.
    Expansion stops ONLY at atomic nodes.
    max_depth is an optional safety guard.
    """

    # Primary stop: semantic atomicity
    if node.is_atomic:
        return

    # Secondary stop: safety guard (optional)
    if max_depth is not None and node.level >= max_depth:
        return

    children = generate_children(node)
    node.children.extend(children)

    for c in children:
        expand_tree(c, max_depth)


def generate_attack_tree(surface_goal: str, max_depth: int | None = None) -> dict:
    """
    Generate an attack tree for a single surface goal.
    Tree grows until atomic boundaries are reached.
    """

    # Defensive check (optional, safe)
    if isinstance(surface_goal, list):
        surface_goal = surface_goal[0] if surface_goal else ""

    # Level 0: Surface Goal
    root = AttackNode(
        goal=surface_goal,
        level=0,
        node_type="surface_goal"
    )

    # Level 1: Attack Vectors
    vectors = generate_children(root)
    root.children.extend(vectors)

    # Recursive expansion
    for v in vectors:
        expand_tree(v, max_depth)

    return root.to_dict()


if __name__ == "__main__":

    SURFACE_GOAL = "Throttle Control System Compromise"

    existing = get_tree(SURFACE_GOAL)

    if existing:
        print("✅ Existing tree found\n")
        print(json.dumps(existing, indent=2))
    else:
        print("⚙️ Generating attack tree (semantic-driven)...\n")

        # max_depth=None → pure semantic expansion
        # You can set max_depth=7 if you want a safety cap
        tree = generate_attack_tree(
            SURFACE_GOAL,
            max_depth=None
        )

        save_tree(SURFACE_GOAL, tree)
        print("💾 Tree saved successfully\n")
        print(json.dumps(tree, indent=2))
