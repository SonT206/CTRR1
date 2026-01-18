import streamlit as st
import networkx as nx
from pyvis.network import Network
import json

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Trình tạo đồ thị tương tác",
    layout="wide"
)

# =============================
# SESSION STATE
# =============================
if "graph" not in st.session_state:
    st.session_state.graph = nx.Graph()

if "directed" not in st.session_state:
    st.session_state.directed = False

if "steps" not in st.session_state:
    st.session_state.steps = []

if "step_index" not in st.session_state:
    st.session_state.step_index = 0

# =============================
# SIDEBAR UI (GIỐNG HÌNH MẪU)
# =============================
with st.sidebar:
    st.markdown("## 🛠️ Công cụ đồ thị")

    st.session_state.directed = st.checkbox("Đồ thị có hướng")

    if st.session_state.directed:
        st.session_state.graph = nx.DiGraph(st.session_state.graph)
    else:
        st.session_state.graph = nx.Graph(st.session_state.graph)

    st.divider()
    st.markdown("### 🔹 Thuật toán cơ bản")

    start = st.text_input("Đỉnh bắt đầu")
    end = st.text_input("Đỉnh kết thúc")

    if st.button("BFS"):
        if start in st.session_state.graph:
            order = list(nx.bfs_tree(st.session_state.graph, start))
            st.session_state.steps = order
            st.session_state.step_index = 0

    if st.button("DFS"):
        if start in st.session_state.graph:
            order = list(nx.dfs_preorder_nodes(st.session_state.graph, start))
            st.session_state.steps = order
            st.session_state.step_index = 0

    if st.button("Đường đi ngắn nhất"):
        if start in st.session_state.graph and end in st.session_state.graph:
            path = nx.shortest_path(st.session_state.graph, start, end)
            st.session_state.steps = path
            st.session_state.step_index = 0

    st.divider()
    st.markdown("### 🔸 Thuật toán nâng cao")

    if st.button("Prim (MST)"):
        mst = nx.minimum_spanning_tree(st.session_state.graph, algorithm="prim")
        st.session_state.steps = list(mst.edges())
        st.session_state.step_index = 0

    if st.button("Kruskal (MST)"):
        mst = nx.minimum_spanning_tree(st.session_state.graph, algorithm="kruskal")
        st.session_state.steps = list(mst.edges())
        st.session_state.step_index = 0

    if st.button("Ford–Fulkerson"):
        if isinstance(st.session_state.graph, nx.DiGraph):
            flow = nx.maximum_flow(st.session_state.graph, start, end)
            st.session_state.steps = list(flow[1].keys())
            st.session_state.step_index = 0
        else:
            st.warning("Ford–Fulkerson cần đồ thị có hướng")

    if st.button("Euler (Hierholzer)"):
        if nx.is_eulerian(st.session_state.graph):
            path = list(nx.eulerian_circuit(st.session_state.graph))
            st.session_state.steps = path
            st.session_state.step_index = 0
        else:
            st.warning("Đồ thị không Euler")

    st.divider()
    st.markdown("### 🎞️ Điều khiển Animation")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("◀"):
            st.session_state.step_index = max(0, st.session_state.step_index - 1)
    with col2:
        if st.button("▶"):
            st.session_state.step_index = min(len(st.session_state.steps) - 1, st.session_state.step_index + 1)
    with col3:
        if st.button("Reset"):
            st.session_state.step_index = 0

    st.divider()
    if st.button("🗑️ Xóa đồ thị"):
        st.session_state.graph.clear()
        st.session_state.steps = []
        st.session_state.step_index = 0

# =============================
# BUILD PYVIS GRAPH
# =============================
net = Network(
    height="760px",
    width="100%",
    directed=st.session_state.directed,
    bgcolor="#ffffff"
)

active = set()
if st.session_state.steps:
    s = st.session_state.steps[: st.session_state.step_index + 1]
    for x in s:
        if isinstance(x, tuple):
            active.update(x)
        else:
            active.add(x)

for n in st.session_state.graph.nodes():
    net.add_node(
        n,
        label=str(n),
        color="#ff6666" if n in active else "#97c2fc"
    )

for u, v in st.session_state.graph.edges():
    net.add_edge(
        u, v,
        color="red" if (u in active and v in active) else "black"
    )

net.set_options("""
var options = {
  interaction: { hover: true },
  manipulation: {
    enabled: true,
    addNode: function (data, callback) {
      data.label = data.id;
      callback(data);
    },
    addEdge: function (data, callback) {
      if (data.from === data.to) return;
      callback(data);
    },
    deleteNode: true,
    deleteEdge: true
  },
  physics: { enabled: false }
}
""")

html = net.generate_html()
st.components.v1.html(html, height=780)
