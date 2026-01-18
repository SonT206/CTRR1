import matplotlib
matplotlib.use("Agg")

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import time

# =========================
# BFS
# =========================
def bfs(graph, start):
    visited = set()
    order = []
    q = deque([start])
    visited.add(start)

    while q:
        u = q.popleft()
        order.append(u)
        for v in graph[u]:
            if v not in visited:
                visited.add(v)
                q.append(v)
    return order

# =========================
# DFS
# =========================
def dfs(graph, start):
    visited = set()
    order = []

    def _dfs(u):
        visited.add(u)
        order.append(u)
        for v in graph[u]:
            if v not in visited:
                _dfs(v)

    _dfs(start)
    return order

# =========================
# Bipartite
# =========================
def is_bipartite(graph):
    color = {}
    for node in graph:
        if node not in color:
            q = deque([node])
            color[node] = 0
            while q:
                u = q.popleft()
                for v in graph[u]:
                    if v not in color:
                        color[v] = 1 - color[u]
                        q.append(v)
                    elif color[v] == color[u]:
                        return False, {}
    return True, color

# =========================
# Ford–Fulkerson (Animated)
# =========================
def ford_fulkerson_steps(G, s, t):
    flow = {e: 0 for e in G.edges}
    steps = []

    def bfs_path():
        parent = {}
        visited = {s}
        q = deque([s])
        while q:
            u = q.popleft()
            for v in G.successors(u):
                if v not in visited and G[u][v]["capacity"] - flow[(u, v)] > 0:
                    visited.add(v)
                    parent[v] = u
                    q.append(v)
        return parent if t in visited else None

    while True:
        parent = bfs_path()
        if not parent:
            break

        path = []
        v = t
        bottleneck = float("inf")
        while v != s:
            u = parent[v]
            bottleneck = min(bottleneck, G[u][v]["capacity"] - flow[(u, v)])
            path.append((u, v))
            v = u
        path.reverse()

        for e in path:
            flow[e] += bottleneck

        steps.append((path.copy(), dict(flow)))

    return steps

# =========================
# Streamlit UI
# =========================
st.set_page_config(layout="wide")
st.title("🎯 Trực quan Thuật toán Đồ thị")

algorithm = st.sidebar.selectbox(
    "Chọn thuật toán",
    ["BFS", "DFS", "Bipartite", "Ford–Fulkerson (Max Flow)"]
)

# =========================
# Graph input
# =========================
st.sidebar.markdown("### Danh sách cạnh (u v capacity)")
edges_input = st.sidebar.text_area(
    "Ví dụ:\nA B 10\nA C 5\nB C 15\nB D 10\nC D 10",
    height=150
)

# Parse graph
G = nx.DiGraph()
graph_simple = {}

for line in edges_input.splitlines():
    parts = line.split()
    if len(parts) >= 2:
        u, v = parts[0], parts[1]
        graph_simple.setdefault(u, []).append(v)
        graph_simple.setdefault(v, [])
        if len(parts) == 3:
            cap = int(parts[2])
            G.add_edge(u, v, capacity=cap)
        else:
            G.add_edge(u, v, capacity=1)

# =========================
# Run algorithms
# =========================
if algorithm in ["BFS", "DFS"]:
    start = st.sidebar.text_input("Đỉnh bắt đầu", "A")
    if st.sidebar.button("▶ Chạy"):
        if start in graph_simple:
            order = bfs(graph_simple, start) if algorithm == "BFS" else dfs(graph_simple, start)
            st.success(f"Thứ tự duyệt: {order}")

elif algorithm == "Bipartite":
    if st.sidebar.button("▶ Kiểm tra"):
        ok, color = is_bipartite(graph_simple)
        st.success("Đồ thị hai phía" if ok else "Không phải đồ thị hai phía")

elif algorithm == "Ford–Fulkerson (Max Flow)":
    s = st.sidebar.text_input("Nguồn", "A")
    t = st.sidebar.text_input("Đích", "D")

    if st.sidebar.button("▶ Chạy"):
        steps = ford_fulkerson_steps(G, s, t)
        pos = nx.spring_layout(G)

        for i, (path, flow) in enumerate(steps):
            plt.figure()
            nx.draw(G, pos, with_labels=True, node_color="lightblue")
            nx.draw_networkx_edges(G, pos, edgelist=path, edge_color="red", width=3)
            st.pyplot(plt)
            st.write(f"Bước {i+1}: tăng luồng {path}")
            time.sleep(0.8)
