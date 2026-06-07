import json
from models.attacknode import AttackNode
from generator import generate_children
from db import get_tree, save_tree
from utils import export_to_excel
import re


def expand_tree(node: AttackNode, max_depth: int):
    """
    Recursively expand the attack tree up to max_depth.
    """
    if node.level >= max_depth:
        return

    children = generate_children(node)
    node.children.extend(children)

    for child in children:
        expand_tree(child, max_depth)


if __name__ == "__main__":

    SURFACE_GOAL = "Remote Keyless Entry (RKE) System Hacking"
    FORCE_REGENERATE = True  # Set to True to bypass cache and refresh CVSS scores

    # 🔍 1. Check MongoDB first
    existing = None
    if not FORCE_REGENERATE:
        try:
            existing = get_tree(SURFACE_GOAL)
        except Exception as e:
            print(f"⚠️  Database connection failed: {e}. Proceeding with local generation...\n")

    if existing:
        print("✅ Loaded attack tree from MongoDB\n")
        tree_json = existing["tree"]
        
        # 📊 Export to Excel
        safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", SURFACE_GOAL)
        export_to_excel(tree_json, f"attack_tree_{safe_name}.xlsx")
        
        print(json.dumps(tree_json, indent=2))
        exit(0)

    print("⚙️ No existing tree found. Generating new attack tree...\n")

    # 🌳 2. Level 0 — Surface Goal
    surface_goal = AttackNode(
        goal=SURFACE_GOAL,
        level=0,
        node_type="surface_goal"
    )

    # 🌿 3. Level 1 — Attack Vectors
    attack_vectors = generate_children(surface_goal)
    surface_goal.children.extend(attack_vectors)

    # 🌲 4. Expand deeper (Methods → Techniques → Atomic)
    for vector in attack_vectors:
        expand_tree(vector, max_depth=4)

    # 📦 5. Convert to JSON
    tree_json = surface_goal.to_dict()

    # 💾 6. Save to MongoDB
    try:
        save_tree(SURFACE_GOAL, tree_json)
    except Exception as e:
        print(f"⚠️  Failed to save to database: {e}")

    # 📊 7. Export to Excel
    safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", SURFACE_GOAL)
    export_to_excel(tree_json, f"attack_tree_{safe_name}.xlsx")

    print("✅ Attack tree generated locally\n")
    print(json.dumps(tree_json, indent=2))
