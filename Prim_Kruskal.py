import streamlit as st
import networkx as nx

st.title("Graph Visualizer – Step 3 (MST)")

G = nx.Graph()
edges = [
    (0,1,4),(0,2,3),(1,2,1),(1,3,2),(2,3,4),(3,4,2)
]

for u,v,w in edges:
    G.add_edge(u,v,weight=w)

if st.button("Prim"):
    mst = nx.minimum_spanning_tree(G, algorithm="prim")
    st.write("Prim MST:", list(mst.edges(data=True)))

if st.button("Kruskal"):
    mst = nx.minimum_spanning_tree(G, algorithm="kruskal")
    st.write("Kruskal MST:", list(mst.edges(data=True)))
