import sys
input = sys.stdin.readline
from collections import deque

N, P = map(int, input().split())

graph = [[] for _ in range(N+1)]
capacity  = [[0]*(N+1) for _ in range(N+1)]
flow = [[0]*(N+1) for _ in range(N+1)]

for _ in range(P):
    sv, nv = map(int, input().split())
    graph[sv].append(nv)
    graph[nv].append(sv)
    capacity[sv][nv] = 1

def BFS(source, sink, visited):
    q = deque()
    q.append(source)
    while q and visited[sink] == -1:
        sv = q.popleft()
        for nv in graph[sv]:
            if visited[sink] == -1 and capacity[sv][nv] - flow[sv][nv] > 0:
                q.append(nv)
                visited[nv] = sv
                if nv == sink:
                    return True
    return False

def edmonds_karp(source, sink):
    ans = 0
    while True:
        visited = [-1]*(N+1)
        if not BFS(source, sink, visited):
            return ans
        j = sink
        while j != source:
            i = visited[j]
            flow[i][j] += 1
            flow[j][i] -= 1
            j = i
        ans += 1
print(edmonds_karp(1, 2))