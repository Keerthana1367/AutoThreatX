import streamlit as st
import json
from db import get_all_surface_goals, get_tree

st.set_page_config(layout="wide")
st.title("Automotive Cybersecurity Attack Tree")

surface_goals = get_all_surface_goals()
if not surface_goals:
    st.error("No trees in DB")
    st.stop()

goal = st.selectbox("Select Surface Goal", surface_goals)
tree = get_tree(goal)

tree_json = json.dumps(tree).replace("</", "<\\/")

with open("visualize.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace("{{TREE_DATA}}", tree_json)
st.components.v1.html(html, height=2500, scrolling=True)
