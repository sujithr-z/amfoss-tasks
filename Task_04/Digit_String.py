import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    t = int(input_data[0])
    out = []
    
    for i in range(1, t + 1):
        a = input_data[i]
        n = len(a)
        
        tot = a.count('1') + a.count('3')
        k = tot
        l = 0
        m = 0
        
        for char in a:
            if char == '2':
                l += 1
            elif char == '1' or char == '3':
                m += 1
            
            kept = l + (tot - m)
            if kept > k:
                k = kept
        
        out.append(str(n - k))
        
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    solve()