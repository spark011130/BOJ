def dfs(x):
    visited[x] = True
    for y in graph[x]:
        # y노드가 아직 매칭이 되지 않은 경우, x와 이어주기
        if matchedY[y] == -1:
            matchedY[y] = x
            matchedX[x] = y
            return True
        # y노드가 매칭되어있으면, y노드랑 매칭된 어느 x노드가 다른 y노드랑 매칭이 가능한지 알아보기
        # 추가 조건: Y가 0번째 인덱스를 가진 X랑 매칭하려고 할 경우, 포기하기 (0번째 x의 이어짐은 절대적으로)
        elif not matchedY[y] == 0  and not visited[matchedY[y]] and dfs(matchedY[y]):
            matchedY[y] = x
            matchedX[x] = y
            return True
        # 불가능
    return False

# 소수 테이블 만들기: 에라스토테네스의 체
n = 3000
table = [False, False] + [True]*(n-1)
for i in range(2, n+1):
    if table[i]:
        for j in range(2*i, n+1, i):
            table[j] = False

N = int(input())
A = list(map(int, input().split()))
graph = [[] for _ in range(N)]
for i in range(N):
    for j in range(N):
        if i != j and table[A[i]+A[j]] == True:
            graph[i].append(j)
ans = []
for y in graph[0]:
    matchedX = [-1]*N
    matchedY = [-1]*N
    matchedX[0] = y
    matchedY[y] = 0
    
    for i in range(1, N):
        visited = [False]*N
        dfs(i)
    
    if -1 not in matchedX:
        ans.append(A[y])

if ans:    
    print(*sorted(ans))
else:
    print(-1)