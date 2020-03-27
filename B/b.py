S = input()
N = len(S)
flg = True
i = 0
while i <= (N-3)/2:
    if S[i]!=S[int((N-3)/2-i)]:
        flg = False
    i += 1
i = N-1
while i >= (N+1)/2:
    if S[i]!=S[int((3*N-1)/2-i)]:
        flg = False
    i -= 1
i = 0
while i <= N-1:
    if S[i]!=S[N-1-i]:
        flg = False
    i += 1
if flg:
    print('Yes')
else:
    print('No')
