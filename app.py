import streamlit as st
import json
from db import get_tree
from main import generate_attack_tree
# pyright: reportUndefinedVariable=false

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AutoThreat-X | Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR PREMIUM LOOK ---
st.markdown("""
<style>
    /* Main Background & Text */
    .stApp {
        background-color: #0b0f19;
        color: #e0e6ed;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #00d4ff !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }
    
    /* Neon Glow for the Main Title */
    .main-title {
        font-size: 3rem;
        font-weight: 900;
        background: -webkit-linear-gradient(45deg, #00d4ff, #d33682);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        color: #ff4b4b !important;
        text-shadow: 0px 0px 10px rgba(255, 75, 75, 0.3);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #00d4ff 0%, #007bff 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.6);
        color: white;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("### System Status")
    st.markdown("- **Engine**: Groq LLaMA 3.1\n- **DB**: MongoDB Atlas\n- **Scoring**: CVSS v3.1")

# --- MAIN CONTENT ---
st.markdown('<div class="main-title"> AutoThreat-X</div>', unsafe_allow_html=True)
st.caption("Automotive Cybersecurity Threat Validator & Attack Tree Generator")
st.markdown("---")

# Main Input
st.markdown("### Threat Modeling Target")
SURFACE_GOAL = st.text_input(
    "Enter the target ECU or subsystem to model:",
    "Remote Keyless Entry (RKE) System Hacking"
)
st.markdown("---")

# Fetch Tree
doc = get_tree(SURFACE_GOAL)

if not doc:
    st.warning(f"⚠️ No existing threat model found for **{SURFACE_GOAL}** in the database.")
    st.info("Click below to initialize the AI engine and generate a comprehensive attack tree.")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button(f" Generate Threat Model for '{SURFACE_GOAL}'"):
            with st.spinner(" AI Engine compiling attack vectors... This may take a few minutes..."):
                tree_json = generate_attack_tree(SURFACE_GOAL)
                st.success(" Threat Model generated successfully!")
                doc = {"tree": tree_json}
        else:
            st.stop()
else:
    st.success(f" Threat Model loaded for **{SURFACE_GOAL}**")

# If we get here, we have the tree
tree_json = doc["tree"]

# --- CALCULATE METRICS ---
def get_metrics(node):
    stats = {"total": 1, "high": 0, "max_cvss": 0.0}
    cvss = float(node.get("cvss", 0))
    if cvss > stats["max_cvss"]: stats["max_cvss"] = cvss
    if cvss >= 7.0: stats["high"] += 1
        
    for child in node.get("children", []):
        child_stats = get_metrics(child)
        stats["total"] += child_stats["total"]
        stats["high"] += child_stats["high"]
        if child_stats["max_cvss"] > stats["max_cvss"]:
            stats["max_cvss"] = child_stats["max_cvss"]
    return stats

metrics = get_metrics(tree_json)

# --- DASHBOARD METRICS ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Nodes Generated", metrics["total"])
m2.metric("Max CVSS Score", f"{metrics['max_cvss']:.1f}")
m3.metric("High Severity Alerts (CVSS 7+)", metrics["high"])
m4.metric("Validation Status", "Verified ")

st.markdown("---")
st.markdown("### Interactive Attack Tree")

# --- VISUALIZATION ---
tree_str = json.dumps(tree_json)

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  body {{
    background-color: transparent;
    color: #fafafa;
    font-family: 'Inter', sans-serif;
    margin: 0;
    overflow: hidden;
  }}
  .node rect {{
    cursor: pointer;
    stroke: #333;
    stroke-width: 1px;
    rx: 8;
    ry: 8;
    transition: all 0.3s;
  }}
  .node rect:hover {{
    stroke: #00d4ff;
    stroke-width: 2px;
    filter: drop-shadow(0 0 8px rgba(0,212,255,0.8));
  }}
  .node text {{
    font: 12px 'Inter', sans-serif;
    font-weight: 600;
    fill: #ffffff;
    pointer-events: none;
    text-anchor: middle;
  }}
  .link {{
    fill: none;
    stroke: #00d4ff;
    stroke-opacity: 0.3;
    stroke-width: 2px;
  }}
  #details {{
    position: fixed;
    top: 20px;
    right: 20px;
    width: 320px;
    background: rgba(17, 24, 39, 0.95);
    border: 1px solid #1f2937;
    border-left: 4px solid #00d4ff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    backdrop-filter: blur(10px);
    z-index: 1000;
  }}
  .badge {{
    display: inline-block;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 10px;
    letter-spacing: 1px;
  }}
  .cvss-high {{ background: #ff4b4b; color: white; box-shadow: 0 0 10px rgba(255,75,75,0.5); }}
  .cvss-med {{ background: #ffa421; color: black; box-shadow: 0 0 10px rgba(255,164,33,0.5); }}
  .cvss-low {{ background: #00d4ff; color: black; box-shadow: 0 0 10px rgba(0,212,255,0.5); }}
  
  h3 {{ margin-top: 0; color: #00d4ff; font-size: 16px; border-bottom: 1px solid #1f2937; padding-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }}
  p {{ margin: 8px 0; font-size: 14px; line-height: 1.4; color: #d1d5db; }}
  b {{ color: #f3f4f6; }}
</style>
</head>
<body>

<div id="details">
  <h3>Node Diagnostics</h3>
  <p>Select a node to inspect threat metrics and intelligence.</p>
</div>

<script>
const data = {tree_str};

const width = window.innerWidth;
const height = window.innerHeight;

const svg = d3.select("body")
  .append("svg")
  .attr("width", width)
  .attr("height", height)
  .call(d3.zoom().on("zoom", (event) => {{
    main_g.attr("transform", event.transform);
  }}))
  .append("g");

const main_g = svg.append("g")
  .attr("transform", "translate(" + width/2 + ", 50) scale(0.8)");

const nodeWidth = 200;
const nodeHeight = 55;

const treeLayout = d3.tree().nodeSize([nodeWidth + 30, 140]);
const root = d3.hierarchy(data, d => d.children);

root.x0 = 0;
root.y0 = 0;

const nodeColors = {{
  "surface_goal": "#00d4ff",
  "attack_vector": "#ffa421",
  "method": "#ff4b4b",
  "technique": "#d33682",
  "sub_technique": "#6c71c4",
  "atomic_attack": "#2ecc71"
}};

update(root);

function update(source) {{
  const treeData = treeLayout(root);
  const nodes = treeData.descendants();
  const links = treeData.links();

  nodes.forEach(d => d.y = d.depth * 160);

  const node = main_g.selectAll('g.node')
    .data(nodes, d => d.id || (d.id = Math.random()));

  const nodeEnter = node.enter().append('g')
    .attr('class', 'node')
    .attr("transform", d => `translate(${{source.x0}},${{source.y0}})`)
    .on('click', (event, d) => {{
       showDetails(d.data);
       if (d.children || d._children) {{
         toggleNode(d);
         update(d);
       }}
    }});

  nodeEnter.append('rect')
    .attr('width', nodeWidth)
    .attr('height', nodeHeight)
    .attr('x', -nodeWidth / 2)
    .attr('y', -nodeHeight / 2)
    .style("fill", d => nodeColors[d.data.node_type] || "#1f2937")
    .style("fill-opacity", 0.95)
    .style("stroke", d => d._children ? "#ffffff" : "#4b5563")
    .style("stroke-width", d => d._children ? "2px" : "1px");

  nodeEnter.append('text')
    .attr("dy", "0.35em")
    .text(d => {{
      const goal = d.data.goal;
      return goal.length > 25 ? goal.substring(0, 22) + "..." : goal;
    }});

  const nodeUpdate = nodeEnter.merge(node);
  nodeUpdate.transition().duration(500)
    .attr("transform", d => `translate(${{d.x}},${{d.y}})`);

  nodeUpdate.select('rect')
    .style("stroke", d => d._children ? "#ffffff" : "#4b5563")
    .style("stroke-width", d => d._children ? "2px" : "1px");

  const nodeExit = node.exit().transition().duration(500)
    .attr("transform", d => `translate(${{source.x}},${{source.y}})`)
    .remove();

  const link = main_g.selectAll('path.link')
    .data(links, d => d.target.id);

  const linkEnter = link.enter().insert('path', "g")
    .attr("class", "link")
    .attr("d", d3.linkVertical()
      .x(d => source.x0)
      .y(d => source.y0)
    );

  linkEnter.merge(link).transition().duration(500)
    .attr("d", d3.linkVertical()
      .x(d => d.x)
      .y(d => d.y)
    );

  link.exit().transition().duration(500)
    .attr("d", d3.linkVertical()
      .x(d => source.x)
      .y(d => source.y)
    )
    .remove();

  nodes.forEach(d => {{ d.x0 = d.x; d.y0 = d.y; }});
}}

function toggleNode(d) {{
  if (d.children) {{ d._children = d.children; d.children = null; }}
  else {{ d.children = d._children; d._children = null; }}
}}

function showDetails(d) {{
  const panel = document.getElementById('details');
  const cvss = d.cvss || 0.0;
  const cvssClass = cvss >= 7 ? 'cvss-high' : (cvss >= 4 ? 'cvss-med' : 'cvss-low');
  
  panel.innerHTML = `
    <h3>${{d.node_type.replace('_', ' ').toUpperCase()}}</h3>
    <div class="badge ${{cvssClass}}">CVSS ${{cvss}}</div>
    <p><b>Goal:</b> ${{d.goal}}</p>
    <p><b>Vector:</b> <code style="font-size: 11px; color: #00d4ff; word-break: break-all;">${{d.cvss_vector || 'N/A'}}</code></p>
    <p><b>Feasibility:</b> <span style="color: ${{d.feasibility === 'High' ? '#ff4b4b' : (d.feasibility === 'Low' ? '#00d4ff' : '#ffa421')}}">${{d.feasibility || 'Medium'}}</span></p>
    <p><b>Validation Score:</b> ${{d.validation_score || 0}}/4</p>
  `;
}}
</script>
</body>
</html>
"""

st.components.v1.html(html, height=800, scrolling=True)
