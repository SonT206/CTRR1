import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

from lib.Ford_Fulkerson_Animated import ford_fulkerson_steps

st.set_page_config(layout="wide")
st.title("🔷 Chương trình Đồ thị Tương tác")

# -----------------------------
# Session state
# -----------------------------
if "graph" not in st.session_state:
    st.session_state.graph = nx.DiGraph()

if "ff_steps" not in st.session_state:
    st.session_state.ff_steps = []
    st.session_state.ff_index = 0
    st.session_state.ff_maxflow = 0

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("⚙ Thuật toán")

algo = st.sidebar.selectbox(
    "Chọn thuật toán",
    ["Ford–Fulkerson (Max Flow)"]
)

source = st.sidebar.text_input("Đỉnh nguồn")
sink = st.sidebar.text_input("Đỉnh đích")

if st.sidebar.button("▶ Chạy Ford–Fulkerson"):
    if source and sink:
        G = st.session_state.graph
        if source in G.nodes and sink in G.nodes:
            max_flow, steps = ford_fulkerson_steps(G, source, sink)
            st.session_state.ff_steps = steps
            st.session_state.ff_index = 0
            st.session_state.ff_maxflow = max_flow
        else:
            st.warning("Nguồn hoặc đích không tồn tại!")

if st.sidebar.button("⏭ Bước tiếp"):
    if st.session_state.ff_index < len(st.session_state.ff_steps) - 1:
        st.session_state.ff_index += 1

# -----------------------------
# Hiển thị đồ thị
# -----------------------------
net = Network(height="600px", width="100%", directed=True)

G = st.session_state.graph

for n in G.nodes:
    net.add_node(n, label=str(n))

# Nếu đang animation Ford
highlight_edges = []
flow_info = {}

if st.session_state.ff_steps:
    step = st.session_state.ff_steps[st.session_state.ff_index]
    highlight_edges = step["path"]
    flow_info = step["flow_state"]

for u, v, data in G.edges(data=True):
    label = str(data.get("weight", 1))
    color = "black"
    width = 2

    if (u, v) in highlight_edges:
        color = "red"
        width = 5

    if (u, v) in flow_info:
        label = f"{flow_info[(u,v)]}/{data.get('weight',1)}"

    net.add_edge(u, v, label=label, color=color, width=width)

net.set_options("""
{
  "physics": {
    "enabled": true,
    "solver": "forceAtlas2Based"
  },
  "interaction": {
    "dragNodes": true,
    "multiselect": true
  }
}
""")

html = net.generate_html()
components.html(html, height=620)

# -----------------------------
# Thông tin luồng
# -----------------------------
if st.session_state.ff_steps:
    st.success(f"💧 Luồng cực đại = {st.session_state.ff_maxflow}")
    st.info(
        f"Bước {st.session_state.ff_index+1} / {len(st.session_state.ff_steps)}"
    )
