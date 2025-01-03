# x => y
def dfs(x):
    visited[x] = True
    for y in graph[x]:
        # y노드가 아직 매칭이 되지 않은 경우, x와 이어주기
        if matchedY[y] == -1:
            matchedY[y] = x
            matchedX[x] = y
            return True
        # y노드가 매칭되어있으면, y노드랑 매칭된 어느 x노드가 다른 y노드랑 매칭이 가능한지 알아보기
        elif not visited[matchedY[y]] and dfs(matchedY[y]):
            matchedY[y] = x
            matchedX[x] = y
            return True
    return False

N, M = map(int, input().split())
matchedX = [-1]*N
matchedY = [-1]*M
graph = []
for _ in range(N):
    temp = list(map(int, input().split()))[1:]
    for i in range(len(temp)):
        temp[i] -= 1
    graph.append(temp)
ans = 0 
for i in range(N):
    visited = [False]*N
    for _ in range(2):
        if dfs(i):
            ans += 1
print(ans)