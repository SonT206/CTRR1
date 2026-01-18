import streamlit as st
import networkx as nx
import random

st.set_page_config(layout="wide")
st.title("Graph Visualizer – Step 2 (Shortest Path)")

weighted = st.checkbox("Weighted Graph", value=True)

G = nx.Graph()
node_count = st.number_input("Number of nodes", 2, 10, 5)

for i in range(node_count):
    G.add_node(i)

st.write("Edges")
edges = []
for i in range(node_count - 1):
    w = random.randint(1, 10) if weighted else 1
    G.add_edge(i, i + 1, weight=w)
    edges.append((i, i + 1, w))

st.write("Edge List:", edges)

start = st.selectbox("Start", G.nodes)
end = st.selectbox("End", G.nodes)

if st.button("Shortest Path"):
    if weighted:
        path = nx.dijkstra_path(G, start, end)
        cost = nx.dijkstra_path_length(G, start, end)
    else:
        path = nx.shortest_path(G, start, end)
        cost = len(path) - 1

    st.success(f"Path: {path}")
    st.info(f"Cost: {cost}")
