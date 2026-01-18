import streamlit as st
import networkx as nx
from pyvis.network import Network
import tempfile
import json

st.set_page_config(layout="wide")
st.title("Graph Visualizer – Step 1 (BFS, DFS, Bipartite)")

# ---------------- GRAPH STATE ----------------
if "nodes" not in st.session_state:
    st.session_state.nodes = []
    st.session_state.edges = []
    st.session_state.node_id = 0

# ---------------- PYVIS GRAPH ----------------
def render_graph():
    net = Network(height="600px", width="100%", directed=False)
    net.toggle_physics(False)

    for n in st.session_state.nodes:
        net.add_node(n["id"], label=str(n["id"]))

    for e in st.session_state.edges:
        net.add_edge(e["from"], e["to"])

    net.set_options("""
    {
      "interaction": { "hover": true },
      "manipulation": {
        "enabled": true,
        "addNode": true,
        "addEdge": true,
        "deleteNode": true,
        "deleteEdge": true
      }
    }
    """)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    net.save_graph(tmp.name)
    st.components.v1.html(open(tmp.name, encoding="utf-8").read(), height=620)

# ---------------- BUILD NX GRAPH ----------------
def build_graph():
    G = nx.Graph()
    for n in st.session_state.nodes:
        G.add_node(n["id"])
    for e in st.session_state.edges:
        G.add_edge(e["from"], e["to"])
    return G

# ---------------- BFS ----------------
def bfs(G, start):
    visited = []
    queue = [start]
    seen = set()

    while queue:
        u = queue.pop(0)
        if u not in seen:
            seen.add(u)
            visited.append(u)
            queue.extend(G.neighbors(u))
    return visited

# ---------------- DFS ----------------
def dfs(G, start):
    visited = []
    stack = [start]
    seen = set()

    while stack:
        u = stack.pop()
        if u not in seen:
            seen.add(u)
            visited.append(u)
            stack.extend(G.neighbors(u))
    return visited

# ---------------- UI ----------------
left, right = st.columns([3, 2])

with left:
    st.subheader("Interactive Graph")
    render_graph()

with right:
    st.subheader("Algorithms")

    if st.button("Add Node"):
        st.session_state.nodes.append({"id": st.session_state.node_id})
        st.session_state.node_id += 1

    if len(st.session_state.nodes) > 0:
        start = st.selectbox("Start Vertex", [n["id"] for n in st.session_state.nodes])

        if st.button("Run BFS"):
            G = build_graph()
            st.write("BFS Order:", bfs(G, start))

        if st.button("Run DFS"):
            G = build_graph()
            st.write("DFS Order:", dfs(G, start))

        if st.button("Check Bipartite"):
            G = build_graph()
            st.write("Is Bipartite:", nx.is_bipartite(G))

    st.subheader("Adjacency List")
    G = build_graph()
    for n in G.nodes:
        st.write(f"{n}: {list(G.neighbors(n))}")
