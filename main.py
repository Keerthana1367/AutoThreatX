import json
import argparse
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


def generate_attack_tree(surface_goal_name: str, max_depth: int = 4, force_regenerate: bool = False):
    # 🔍 1. Check MongoDB first
    existing = None
    if not force_regenerate:
        try:
            existing = get_tree(surface_goal_name)
        except Exception as e:
            print(f"⚠️  Database connection failed: {e}. Proceeding with local generation...\n")

    if existing:
        print("✅ Loaded attack tree from MongoDB\n")
        tree_json = existing["tree"]
        
        # 📊 Export to Excel
        safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", surface_goal_name)
        export_to_excel(tree_json, f"attack_tree_{safe_name}.xlsx")
        
        return tree_json

    print(f"⚙️ No existing tree found for '{surface_goal_name}'. Generating new attack tree...\n")

    # 🌳 2. Level 0 — Surface Goal
    surface_goal = AttackNode(
        goal=surface_goal_name,
        level=0,
        node_type="surface_goal"
    )

    # 🌿 3. Level 1 — Attack Vectors
    attack_vectors = generate_children(surface_goal)
    surface_goal.children.extend(attack_vectors)

    # 🌲 4. Expand deeper (Methods → Techniques → Atomic)
    for vector in attack_vectors:
        expand_tree(vector, max_depth=max_depth)

    # 📦 5. Convert to JSON
    tree_json = surface_goal.to_dict()

    # 💾 6. Save to MongoDB
    try:
        save_tree(surface_goal_name, tree_json)
    except Exception as e:
        print(f"⚠️  Failed to save to database: {e}")

    # 📊 7. Export to Excel
    safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", surface_goal_name)
    export_to_excel(tree_json, f"attack_tree_{safe_name}.xlsx")

    print("✅ Attack tree generated locally\n")
    return tree_json


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an attack tree for a given surface goal.")
    parser.add_argument("goal", nargs="?", default="Remote Keyless Entry (RKE) System Hacking", help="The surface goal to generate the attack tree for.")
    parser.add_argument("--force", action="store_true", help="Force regenerate the attack tree even if it exists in the database.")
    parser.add_argument("--depth", type=int, default=4, help="Maximum depth of the attack tree.")
    args = parser.parse_args()

    tree = generate_attack_tree(args.goal, max_depth=args.depth, force_regenerate=args.force)
    print(json.dumps(tree, indent=2))
