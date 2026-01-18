from collections import deque
import time

def ford_fulkerson_steps(graph, source, sink):
    """
    graph: dict {u: {v: capacity}}
    return: list of steps (path, flow)
    """

    steps = []
    residual = {}

    # Tạo đồ thị dư
    for u in graph:
        residual[u] = {}
        for v in graph[u]:
            residual[u][v] = graph[u][v]
            if v not in residual:
                residual[v] = {}
            if u not in residual[v]:
                residual[v][u] = 0

    def bfs():
        parent = {source: None}
        queue = deque([source])

        while queue:
            u = queue.popleft()
            for v in residual[u]:
                if v not in parent and residual[u][v] > 0:
                    parent[v] = u
                    if v == sink:
                        path = []
                        cur = sink
                        flow = float('inf')
                        while parent[cur] is not None:
                            flow = min(flow, residual[parent[cur]][cur])
                            path.append((parent[cur], cur))
                            cur = parent[cur]
                        path.reverse()
                        return path, flow
                    queue.append(v)
        return None, 0

    while True:
        path, flow = bfs()
        if not path:
            break

        for u, v in path:
            residual[u][v] -= flow
            residual[v][u] += flow

        steps.append({
            "path": path,
            "flow": flow
        })

    return steps
