import pandas as pd

def parse_numbered_list(text: str) -> list[str]:
    lines = []
    for l in text.splitlines():
        l = l.strip()
        if len(l) > 2 and l[0].isdigit() and l[1] == ".":
            lines.append(l.split(".", 1)[1].strip())
    return lines

def export_to_excel(tree_dict: dict, filename: str):
    """
    Export the attack tree to an Excel file with a professional structure.
    """
    rows = []

    def _flatten(node, parent_goal=None, path=""):
        current_goal = node.get("goal", "N/A")
        full_path = f"{path} > {current_goal}" if path else current_goal
        
        rows.append({
            "Depth": node.get("level"),
            "Node Type": node.get("node_type", "").replace("_", " ").title(),
            "Parent": parent_goal,
            "Goal": current_goal,
            "CVSS Score": node.get("cvss", 0.0),
            "CVSS Vector": node.get("cvss_vector", "N/A"),
            "Feasibility": node.get("feasibility", "Medium"),
            "Quality Score": f"{node.get('validation_score', 0)}/4",
            "Hierarchy Path": full_path
        })
        
        for child in node.get("children", []):
            _flatten(child, current_goal, full_path)

    _flatten(tree_dict)
    df = pd.DataFrame(rows)
    
    # Sort by Depth to maintain logical flow
    df = df.sort_values(by=["Depth"])
    
    df.to_excel(filename, index=False)
    print(f"📊 Professional Excel report exported: {filename}")
