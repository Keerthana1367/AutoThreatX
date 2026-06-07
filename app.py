import streamlit as st
import json
from db import get_tree
# pyright: reportUndefinedVariable=false


st.set_page_config(layout="wide")
st.title("Atomic Automotive Cyber Attack Tree")

SURFACE_GOAL = st.text_input(
    "Surface Goal",
    "Remote Keyless Entry (RKE) System Hacking"
)

doc = get_tree(SURFACE_GOAL)

if not doc:
    st.error("No attack tree found in MongoDB.")
    st.stop()

tree_json = doc["tree"]

tree_str = json.dumps(tree_json)

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  body {{
    background-color: #0e1117;
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
  }}
  .node text {{
    font: 11px 'Inter', sans-serif;
    fill: #e0e0e0;
    pointer-events: none;
    text-anchor: middle;
  }}
  .link {{
    fill: none;
    stroke: #4a4a4a;
    stroke-opacity: 0.5;
    stroke-width: 1.5px;
  }}
  #details {{
    position: fixed;
    top: 20px;
    right: 20px;
    width: 320px;
    background: rgba(25, 25, 25, 0.95);
    border: 1px solid #333;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    backdrop-filter: blur(8px);
    z-index: 1000;
  }}
  .badge {{
    display: inline-block;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 10px;
  }}
  .cvss-high {{ background: #ff4b4b; color: white; }}
  .cvss-med {{ background: #ffa421; color: black; }}
  .cvss-low {{ background: #00d4ff; color: black; }}
  
  h3 {{ margin-top: 0; color: #00d4ff; font-size: 16px; border-bottom: 1px solid #333; padding-bottom: 8px; }}
  p {{ margin: 8px 0; font-size: 14px; line-height: 1.4; color: #bbb; }}
  b {{ color: #eee; }}
</style>
</head>
<body>

<div id="details">
  <h3>Node Details</h3>
  <p>Select a node to see threat metrics.</p>
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
  .attr("transform", "translate(" + width/2 + ", 100) scale(0.8)");

const nodeWidth = 180;
const nodeHeight = 50;

const treeLayout = d3.tree().nodeSize([nodeWidth + 20, 120]);
const root = d3.hierarchy(data, d => d.children);

root.x0 = 0;
root.y0 = 0;

const nodeColors = {{
  "surface_goal": "#00d4ff",
  "attack_vector": "#ffa421",
  "method": "#ff4b4b",
  "technique": "#d33682",
  "sub_technique": "#6c71c4"
}};

update(root);

function update(source) {{
  const treeData = treeLayout(root);
  const nodes = treeData.descendants();
  const links = treeData.links();

  nodes.forEach(d => d.y = d.depth * 150);

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
    .style("fill", d => nodeColors[d.data.node_type] || "#2c3e50")
    .style("fill-opacity", 0.9)
    .style("stroke", d => d._children ? "#fff" : "#333")
    .style("stroke-width", d => d._children ? "3px" : "1px");

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
    .style("stroke", d => d._children ? "#fff" : "#333")
    .style("stroke-width", d => d._children ? "3px" : "1px");

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
    <p><b>Vector:</b> <code style="font-size: 10px; word-break: break-all;">${{d.cvss_vector || 'N/A'}}</code></p>
    <p><b>Feasibility:</b> <span style="color: ${{d.feasibility === 'High' ? '#7199FF' : '#ff4b4b'}}">${{d.feasibility || 'Medium'}}</span></p>
    <p><b>Score:</b> ${{d.validation_score || 0}}/4</p>
  `;
}}
</script>
</body>
</html>
"""

st.components.v1.html(html, height=1600, scrolling=True)
