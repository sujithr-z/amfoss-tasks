import sys

def solve():
    a = sys.stdin.read().split()
    if not a:
        return
    
    t = int(a[0])
    out = []
    idx = 1
    
    for _ in range(t):
        n = int(a[idx])
        idx += 1
        
        l = []
        for i in range(n):
            k = int(a[idx + i])
            while l and l[-1] > k:
                k += l.pop()
            l.append(k)
            
        idx += n
        out.append(str(max(l)))
        
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    solve()