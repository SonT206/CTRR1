import streamlit as st
import networkx as nx

st.title("Graph Visualizer – Step 4 (Euler)")

G = nx.Graph()
edges = [(0,1),(1,2),(2,0),(2,3),(3,0)]
G.add_edges_from(edges)

if nx.is_eulerian(G):
    st.success("Euler Cycle exists")
    st.write(list(nx.eulerian_circuit(G)))
elif nx.has_eulerian_path(G):
    st.warning("Euler Path exists")
    st.write(list(nx.eulerian_path(G)))
else:
    st.error("No Euler Path or Cycle")
