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
        # 불가능
    return False
            
N = 5; M = 4
matchedX = [-1]*N
matchedY = [-1]*M
graph = [[0, 1, 2], [2], [0, 3], [0, 3], [1]]

for i in range(N):
    visited = [False]*N
    dfs(i)
    print(i)