N = int(input())
A = list(map(int, input().split()))
cnt = [0 for _ in range(N)]
for i in range(N):
    cnt[A[i]-1] += 1
S = 0
for i in range(N):
    S += cnt[i]*(cnt[i]-1)/2
for i in range(N):
    if cnt[A[i]-1] == 1:
        print(int(S))
    else:
        print(int(S+(3-2*cnt[A[i]-1])/2))
