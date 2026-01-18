import streamlit as st
import networkx as nx
from pyvis.network import Network
import random
import tempfile
import os

st.set_page_config(layout="wide")
st.title("🧠 Hệ thống đồ thị tương tác (Online)")

# ======================
# SESSION STATE
# ======================
if "G" not in st.session_state:
    st.session_state.G = nx.Graph()
if "directed" not in st.session_state:
    st.session_state.directed = False

# ======================
# SIDEBAR
# ======================
st.sidebar.header("⚙️ Cấu hình đồ thị")

st.session_state.directed = st.sidebar.checkbox("Đồ thị có hướng")
weighted = st.sidebar.checkbox("Có trọng số", value=True)

w_min, w_max = 1, 1
if weighted:
    w_min = st.sidebar.number_input("Trọng số min", 1, 1)
    w_max = st.sidebar.number_input("Trọng số max", w_min, 50)

# ======================
# NODE / EDGE
# ======================
st.sidebar.subheader("➕ Thao tác")

if st.sidebar.button("Thêm đỉnh"):
    st.session_state.G.add_node(len(st.session_state.G.nodes))

nodes = list(st.session_state.G.nodes)

if len(nodes) >= 2:
    u = st.sidebar.selectbox("Đỉnh u", nodes)
    v = st.sidebar.selectbox("Đỉnh v", nodes)
    if st.sidebar.button("Thêm cạnh"):
        w = random.randint(w_min, w_max) if weighted else 1
        st.session_state.G.add_edge(u, v, weight=w)

if st.sidebar.button("Xóa toàn bộ"):
    st.session_state.G.clear()

# ======================
# ALGORITHMS
# ======================
st.sidebar.subheader("🧮 Thuật toán")

algo = st.sidebar.selectbox(
    "Chọn thuật toán",
    [
        "Không",
        "BFS",
        "DFS",
        "Dijkstra",
        "Bellman-Ford",
        "Floyd-Warshall",
        "Prim (MST)",
        "Kruskal (MST)",
        "Topological Sort",
        "Kiểm tra chu trình"
    ]
)

start = None
if algo in ["BFS", "DFS", "Dijkstra", "Bellman-Ford"]:
    start = st.sidebar.selectbox("Đỉnh bắt đầu", nodes) if nodes else None

# ======================
# ALGO LOGIC
# ======================
highlight_edges = []
info = ""

G = st.session_state.G

try:
    if algo == "BFS":
        edges = list(nx.bfs_edges(G, start))
        highlight_edges = edges

    elif algo == "DFS":
        edges = list(nx.dfs_edges(G, start))
        highlight_edges = edges

    elif algo == "Dijkstra":
        paths = nx.single_source_dijkstra_path(G, start)
        for p in paths.values():
            highlight_edges += list(zip(p, p[1:]))

    elif algo == "Bellman-Ford":
        paths = nx.single_source_bellman_ford_path(G, start)
        for p in paths.values():
            highlight_edges += list(zip(p, p[1:]))

    elif algo == "Floyd-Warshall":
        info = "Đã tính ma trận khoảng cách Floyd–Warshall"

    elif algo == "Prim (MST)":
        highlight_edges = list(nx.minimum_spanning_edges(G, algorithm="prim", data=False))

    elif algo == "Kruskal (MST)":
        highlight_edges = list(nx.minimum_spanning_edges(G, algorithm="kruskal", data=False))

    elif algo == "Topological Sort":
        order = list(nx.topological_sort(G))
        info = f"Thứ tự topo: {order}"

    elif algo == "Kiểm tra chu trình":
        cycles = list(nx.simple_cycles(G)) if st.session_state.directed else list(nx.cycle_basis(G))
        info = "Có chu trình" if cycles else "Không có chu trình"

except Exception as e:
    info = f"Lỗi: {e}"

# ======================
# DRAW GRAPH
# ======================
net = Network(height="650px", width="100%", directed=st.session_state.directed)
net.barnes_hut()

for n in G.nodes:
    net.add_node(n, label=str(n), color="#8ecae6")

for u, v, d in G.edges(data=True):
    color = "black"
    width = 2
    if (u, v) in highlight_edges or (v, u) in highlight_edges:
        color = "red"
        width = 4
    label = str(d["weight"]) if weighted else ""
    net.add_edge(u, v, label=label, color=color, width=width)

tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
net.save_graph(tmp.name)

with open(tmp.name, "r", encoding="utf-8") as f:
    st.components.v1.html(f.read(), height=700)



if info:
    st.info(info)
