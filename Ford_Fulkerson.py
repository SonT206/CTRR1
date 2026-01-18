import networkx as nx

def ford_fulkerson_steps(G, source, sink):
    """
    Trả về:
    - max_flow: giá trị luồng cực đại
    - steps: danh sách từng bước animation
      mỗi bước = {
          'path': [(u,v), ...],
          'flow_added': x,
          'flow_state': {(u,v): f}
      }
    """

    # Tạo residual graph
    R = nx.DiGraph()
    for u, v, data in G.edges(data=True):
        cap = data.get("weight", 1)
        R.add_edge(u, v, capacity=cap)
        R.add_edge(v, u, capacity=0)

    flow = {}
    steps = []
    max_flow = 0

    def bfs():
        parent = {source: None}
        queue = [source]
        while queue:
            u = queue.pop(0)
            for v in R.successors(u):
                if v not in parent and R[u][v]["capacity"] > 0:
                    parent[v] = u
                    if v == sink:
                        path = []
                        cur = v
                        bottleneck = float("inf")
                        while parent[cur] is not None:
                            p = parent[cur]
                            bottleneck = min(bottleneck, R[p][cur]["capacity"])
                            path.append((p, cur))
                            cur = p
                        return path[::-1], bottleneck
                    queue.append(v)
        return None, 0

    while True:
        path, bottleneck = bfs()
        if not path:
            break

        max_flow += bottleneck

        for u, v in path:
            R[u][v]["capacity"] -= bottleneck
            R[v][u]["capacity"] += bottleneck
            flow[(u, v)] = flow.get((u, v), 0) + bottleneck

        steps.append({
            "path": path,
            "flow_added": bottleneck,
            "flow_state": flow.copy()
        })

    return max_flow, steps
