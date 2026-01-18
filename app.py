import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import time

# ===== IMPORT CÁC THUẬT TOÁN =====
from BFS_DFS_Bipartite import bfs, dfs, is_bipartite
from Dijkstra import dijkstra
from Prim_Kruskal import prim, kruskal
from Euler import euler_path
from Ford_Fulkerson_Animated import ford_fulkerson_steps

# ===== CONFIG =====
st.set_page_config(layout="wide")
st.title("🧠 Ứng dụng Trực quan Thuật toán Đồ thị")

# ===== SESSION STATE =====
if "graph" not in st.session_state:
    st.session_state.graph = nx.DiGraph()

if "ff_steps" not in st.session_state:
    st.session_state.ff_steps = []
    st.session_state.ff_index = 0

# ===== SIDEBAR =====
st.sidebar.header("⚙️ Thuật toán")

algo = st.sidebar.selectbox(
    "Chọn thuật toán",
    [
        "BFS",
        "DFS",
        "Đường đi ngắn nhất (Dijkstra)",
        "Kiểm tra đồ thị 2 phía",
        "Prim (MST)",
        "Kruskal (MST)",
        "Euler (Chu trình / Đường đi)",
        "Ford–Fulkerson (Max Flow)"
    ]
)

start = st.sidebar.text_input("Đỉnh bắt đầu", "0")
end = st.sidebar.text_input("Đỉnh kết thúc / Đích", "3")

run = st.sidebar.button("▶ Chạy thuật toán")
next_step = st.sidebar.button("⏭ Bước tiếp (Ford)")

# ===== SAMPLE GRAPH (CÓ THỂ THAY BẰNG ĐỒ THỊ TƯƠNG TÁC SAU) =====
G = st.session_state.graph
if G.number_of_nodes() == 0:
    edges = [
        ("0", "1", 10),
        ("0", "2", 5),
        ("1", "2", 15),
        ("1", "3", 10),
        ("2", "3", 10)
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=w, capacity=w)

# ===== VẼ ĐỒ THỊ =====
def draw_graph(highlight_edges=None, highlight_nodes=None):
    pos = nx.spring_layout(G, seed=42)
    edge_colors = []
    for u, v in G.edges():
        if highlight_edges and (u, v) in highlight_edges:
            edge_colors.append("red")
        else:
            edge_colors.append("gray")

    node_colors = []
    for n in G.nodes():
        if highlight_nodes and n in highlight_nodes:
            node_colors.append("orange")
        else:
            node_colors.append("lightblue")

    plt.figure(figsize=(7, 5))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=node_colors,
        edge_color=edge_colors,
        node_size=1500,
        arrows=True
    )

    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    st.pyplot(plt)
    plt.clf()

# ===== MAIN LOGIC =====
if run:

    if algo == "BFS":
        order = bfs(G, start)
        draw_graph(highlight_nodes=order)
        st.success(f"BFS Order: {order}")

    elif algo == "DFS":
        order = dfs(G, start)
        draw_graph(highlight_nodes=order)
        st.success(f"DFS Order: {order}")

    elif algo == "Đường đi ngắn nhất (Dijkstra)":
        dist, path = dijkstra(G, start, end)
        draw_graph(highlight_edges=list(zip(path, path[1:])))
        st.success(f"Khoảng cách: {dist}")
        st.write("Đường đi:", " → ".join(path))

    elif algo == "Kiểm tra đồ thị 2 phía":
        ok, part = is_bipartite(G)
        if ok:
            st.success("✅ Đồ thị là 2 phía")
        else:
            st.error("❌ Đồ thị KHÔNG phải 2 phía")

    elif algo == "Prim (MST)":
        mst = prim(G)
        draw_graph(highlight_edges=mst)
        st.success("Cây khung nhỏ nhất (Prim)")

    elif algo == "Kruskal (MST)":
        mst = kruskal(G)
        draw_graph(highlight_edges=mst)
        st.success("Cây khung nhỏ nhất (Kruskal)")

    elif algo == "Euler (Chu trình / Đường đi)":
        path = euler_path(G)
        draw_graph(highlight_nodes=path)
        st.success(" → ".join(path))

    elif algo == "Ford–Fulkerson (Max Flow)":
        graph_dict = {}
        for u, v, data in G.edges(data=True):
            graph_dict.setdefault(u, {})
            graph_dict[u][v] = data.get("capacity", 1)

        st.session_state.ff_steps = ford_fulkerson_steps(
            graph_dict, start, end
        )
        st.session_state.ff_index = 0

        st.success("Đã khởi tạo Ford–Fulkerson, nhấn 'Bước tiếp'")

# ===== FORD – STEP BY STEP =====
if algo == "Ford–Fulkerson (Max Flow)" and next_step:
    if st.session_state.ff_index < len(st.session_state.ff_steps):
        step = st.session_state.ff_steps[st.session_state.ff_index]
        draw_graph(highlight_edges=step["path"])
        st.info(
            f"Bước {st.session_state.ff_index + 1} – Tăng luồng: {step['flow']}"
        )
        st.session_state.ff_index += 1
    else:
        st.success("✅ Đã đạt luồng cực đại")
