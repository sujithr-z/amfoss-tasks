import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    t = int(input_data[0])
    out = []
    idx = 1
    
    for _ in range(t):
        n = int(input_data[idx])
        c = int(input_data[idx+1])
        idx += 2
        
        a = [int(x) for x in input_data[idx:idx+n]]
        idx += n
        b = [int(x) for x in input_data[idx:idx+n]]
        idx += n
        
        k = 0
        v = True
        for i in range(n):
            if a[i] >= b[i]:
                k += a[i] - b[i]
            else:
                v = False
                break
        
        if not v:
            k = 10**18
            
        a.sort()
        b.sort()
        
        l = c
        v = True
        for i in range(n):
            if a[i] >= b[i]:
                l += a[i] - b[i]
            else:
                v = False
                break
                
        if not v:
            l = 10**18
            
        ans = k if k < l else l
        
        if ans >= 10**18:
            out.append("-1")
        else:
            out.append(str(ans))
            
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    solve()