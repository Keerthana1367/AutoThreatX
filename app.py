import streamlit as st
import json
from db import get_all_surface_goals, get_tree

st.set_page_config(layout="wide")
st.title("Automotive Cybersecurity Attack Tree")
st.caption("CVSS is shown only for atomic attack steps")

# ---------------- Load surface goals ----------------
surface_goals = get_all_surface_goals()
if not surface_goals:
    st.error("No attack trees found in database")
    st.stop()

goal = st.selectbox("Select Surface Goal", surface_goals)

tree_doc = get_tree(goal)
if not tree_doc:
    st.error("Selected attack tree not found")
    st.stop()

# If your DB returns wrapper doc, unwrap tree
tree = tree_doc["tree"] if "tree" in tree_doc else tree_doc

# ---------------- Collect atomic CVSS nodes ----------------
def collect_atomic_nodes(node, result):
    if node.get("is_atomic") and node.get("cvss"):
        result.append({
            "Attack Step": node["goal"],
            "CVSS Base Score": node["cvss"]["base_score"]
        })
    for c in node.get("children", []):
        collect_atomic_nodes(c, result)


atomic_nodes = []
collect_atomic_nodes(tree, atomic_nodes)

# ---------------- Sidebar: CVSS View ----------------
st.sidebar.header("Atomic Attacks (CVSS)")

if atomic_nodes:
    st.sidebar.dataframe(atomic_nodes, use_container_width=True)
else:
    st.sidebar.info("No atomic nodes with CVSS found")

# ---------------- Render D3 Tree ----------------
tree_json = json.dumps(tree).replace("</", "<\\/")

with open("visualize.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace("{{TREE_DATA}}", tree_json)

st.components.v1.html(
    html,
    height=2500,
    scrolling=True
)
