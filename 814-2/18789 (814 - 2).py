import random
import os
from copy import deepcopy
import sys
from tqdm import tqdm
import pickle
sys.setrecursionlimit(10**8)

os.chdir('814-2/')

def bisect_left_desc(arr, x):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < x:
            hi = mid
        else:
            lo = mid + 1
    return lo

class Game:
    def __init__(self, DB=[], DB_score=[]):
        if not DB:
            self.DB = [[[random.randint(0, 9) for _ in range(14)] for _ in range(8)] for _ in range(60)]
            self.DB_score = [self.score_metric(self.DB[x]) for x in range(60)]
            _sorted = sorted(zip(self.DB_score, self.DB), reverse=True)
            self.DB_score, self.DB = map(list, zip(*_sorted))
        else:
            self.DB = DB
            self.DB_score = [self.score_metric(DB[i]) for i in range(60)]
    def preset(self):
        # iter: [mutate_max, permute_iter, deep_permute_iter]
        # score_calc => is_apply = False
        is_apply = False
        if is_apply: return [1, 1, 1]
        else: return [5, 100, 10]
    def score_metric(self, table):
        return self.score_calculator(table)

    def mutate(self, table, table_score, max_change_number):
        # 한 개의 숫자를 랜덤하게 뽑아서 그 숫자를 0~9 까지 중 성적 값이 가장 높은 숫자로 바꿔주기
        change_number = random.randint(1, max_change_number) #max_change_number
        next_table = deepcopy(table)
        
        for _ in range(change_number):
            idx = random.randint(0, 111)
            y = idx % 8 
            x = idx // 8
            next_table[y][x] = random.randint(0, 9)
        mu_score = self.score_metric(next_table)
        dscore = mu_score - table_score 
        if dscore > 0:
            return next_table, mu_score
        return table, table_score
    
    def permute(self, table, table_score, iteration):
        # number 만큼의 숫자끼리 바꾸기 (ex. 모든 1 => 2 모든 2 => 1)
        next_table = deepcopy(table)
        for _ in range(iteration):
            
            permutation = random.sample(range(10), 2)
            a = permutation[0]
            b = permutation[1]
            for y in range(8):
                for x in range(14):
                    if next_table[y][x] == a:
                        next_table[y][x] = b
                    elif next_table[y][x] == b:
                        next_table[y][x] = a
            
            # Simulated Annealing의 유무에 따라 테이블의 변경 정하기
            pscore = self.score_metric(next_table)
            dscore = pscore - table_score
        
            if dscore > 0:
                return next_table, pscore
        if dscore == 0:
            return next_table, pscore
        return table, table_score
    def deep_permute(self, table, table_score, iteration):
        # number 만큼의 숫자끼리 바꾸기 (ex. 모든 1 => 2 모든 2 => 1)
        next_table = deepcopy(table)
        
        for _ in range(iteration):
            permutation = random.sample(range(10), 10)
            for y in range(8):
                for x in range(14):
                    next_table[y][x] = permutation[next_table[y][x]]
            
            # Simulated Annealing의 유무에 따라 테이블의 변경 정하기
            dpscore = self.score_metric(next_table)
            dscore = dpscore - table_score
            
            if dscore > 0:
                return next_table, dpscore
        if dscore == 0:
            return next_table, dpscore
        return table, table_score
    
    def simulated_annealing(self, max_iter=100):
        mutate_max, permute_iter, deep_permute_iter = self.preset()
        # 점수에 따른 가중치를 부여해서 랜덤으로 선택한 표에 대해, mutation을 가하고,
        # 점수가 높아졌다면 변이된 표를 저장, 점수가 같다면 이전 표를 덮어씌운다.
        for iter in tqdm(range(max_iter)):
            table_idx = random.choices(range(60), weights=self.DB_score, k=1)[0]
            current_table, current_table_score = self.DB[table_idx], self.DB_score[table_idx]
            if random.random() < 0.8:
                next_table, next_table_score = self.mutate(current_table, current_table_score, mutate_max)
            elif random.random() < 0.9:
                next_table, next_table_score = self.permute(current_table, current_table_score, permute_iter)
            else:
                next_table, next_table_score = self.deep_permute(current_table, current_table_score, deep_permute_iter)
            
            # 기존 DB 보다 못하다면 배제
            if next_table_score < self.DB_score[-1]:
                continue
            # 기존 DB의 한 테이블과 점수가 같다면 대체
            elif next_table_score in self.DB_score:
                exist_idx = self.DB_score.index(next_table_score)
                self.DB[exist_idx] = next_table
                
            # 기존 DB에 없는 remarkable한 점수일 경우 추가
            else:
                idx_to_insert = bisect_left_desc(self.DB_score, next_table_score)
                self.DB.insert(idx_to_insert, next_table); self.DB.pop()
                self.DB_score.insert(idx_to_insert, next_table_score); self.DB_score.pop()
             
    def score_calculator(self, table, n=1, score=1):
        search_pos = []
        next_pos = []
        dy = [-1, -1, -1, 0, 0, 1, 1, 1]
        dx = [-1, 0, 1, -1, 1, -1, 0, 1]
        if n == 9999:
            return score
        reversed = str(n)[::-1]
        if not reversed.startswith('0') and int(reversed) < n:
            return self.score_calculator(table, n+1, score+1)
        # BASE CASE: 시작할 숫자를 찾기
        for y in range(8):
            for x in range(14):
                if int(str(n)[0]) == table[y][x]:
                    # 찾고자하는 값의 마지막 인덱스일경우: n에 1을 더함으로 다음 숫자 분석
                    if len(str(n)) == 1:
                        return self.score_calculator(table, n+1, score+1)
                    # 다음 자릿수가 남은 경우: i에 1을 더함으로 해당 점수의 다음 인덱스 분석
                    else:
                        if [y, x] not in search_pos:
                            search_pos.append([y, x])
        
        # CONTINUOUS CASE: 현재 위치에서 이어지는 숫자를 찾기
        for i in range(1, len(str(n))):
            next_pos = []
            for current_pos in list(search_pos):
                current_y, current_x = current_pos
                next_n = int(str(n)[i])
                for direction in range(8):
                    # 범위 안에 다음 위치를 찾기
                    next_y = current_y + dy[direction]
                    next_x = current_x + dx[direction]
                    if 0 <= next_y < 8 and 0 <= next_x < 14:
                        # 찾고자하는 값이 맞다면
                        if next_n == table[next_y][next_x]:
                            # 찾고자하는 값의 마지막 인덱스일경우: n에 1을 더함으로 다음 숫자 분석
                            if [next_y, next_x] not in next_pos:
                                next_pos.append([next_y, next_x])
            if not next_pos:
                break
            search_pos = next_pos
            
        # 마지막 숫자로 가는 방향이 존재하는 경우
        if next_pos:
            return self.score_calculator(table, n+1, score+1)
        # 마지막 숫자로 가는 방향이 존재하지 않을 경우
        return self.score_calculator(table, n+1, score)
    
    def score_calculator2(self, table, n=1):
        search_pos = []
        next_pos = []
        dy = [-1, -1, -1, 0, 0, 1, 1, 1]
        dx = [-1, 0, 1, -1, 1, -1, 0, 1]
        
        if n == 10000:
            return 9999
        reversed = str(n)[::-1]
        if not reversed.startswith('0') and int(reversed) < n:
            return self.score_calculator(table, n+1)
        # BASE CASE: 시작할 숫자를 찾기
        for y in range(8):
            for x in range(14):
                if int(str(n)[0]) == table[y][x]:
                    # 찾고자하는 값의 마지막 인덱스일경우: n에 1을 더함으로 다음 숫자 분석
                    if len(str(n)) == 1:
                        return self.score_calculator2(table, n+1)
                    # 다음 자릿수가 남은 경우: i에 1을 더함으로 해당 점수의 다음 인덱스 분석
                    else:
                        if [y, x] not in search_pos:
                            search_pos.append([y, x])
        
        # CONTINUOUS CASE: 현재 위치에서 이어지는 숫자를 찾기
        for i in range(1, len(str(n))):
            next_pos = []
            for current_pos in list(search_pos):
                current_y, current_x = current_pos
                next_n = int(str(n)[i])
                for direction in range(8):
                    # 범위 안에 다음 위치를 찾기
                    next_y = current_y + dy[direction]
                    next_x = current_x + dx[direction]
                    if 0 <= next_y < 8 and 0 <= next_x < 14:
                        # 찾고자하는 값이 맞다면
                        if next_n == table[next_y][next_x]:
                            # 찾고자하는 값의 마지막 인덱스일경우: n에 1을 더함으로 다음 숫자 분석
                            if [next_y, next_x] not in next_pos:
                                next_pos.append([next_y, next_x])
            if not next_pos:
                break
            search_pos = next_pos
            
        # 마지막 숫자로 가는 방향이 존재하는 경우
        if next_pos:
            return self.score_calculator2(table, n+1)
        # 마지막 숫자로 가는 방향이 존재하지 않을 경우
        return n-1
    
    def print_table(self, table):
        for y in range(8):
            print(*table[y], sep = "")
            
def main():
    iteration = 0
    
    if os.path.isfile('DB.pickle'):
        print("**PICKLE FILE LOADAED**")
        with open('DB.pickle', 'rb') as f:
            DB = pickle.load(f)
        with open('DB_score.pickle', 'rb') as f:
            DB_score = pickle.load(f)
        game = Game(DB, DB_score)
    else:
        print("**NEW DB CREATED**")
        game = Game()
    try:
        while True:
            game.simulated_annealing()
            iteration += 100
            print("iteration:",iteration)
            print("하위 20개의 점수:", *game.DB_score[-20:])
            print("상위 10개의 점수:", *game.DB_score[:10])
            if iteration % 10000 == 0:
                with open('DB.pickle', 'wb') as f:
                    pickle.dump(game.DB, f)
                with open('DB_score.pickle', 'wb') as f:
                    pickle.dump(game.DB_score, f)        
    except KeyboardInterrupt:
        print(game.DB_score)
        game.print_table(game.DB[0])
        with open('DB.pickle', 'wb') as f:
            pickle.dump(game.DB, f)
        with open('DB_score.pickle', 'wb') as f:
            pickle.dump(game.DB_score, f)
        
if __name__ == '__main__':
    main()