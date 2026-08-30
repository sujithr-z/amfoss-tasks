import sys

def solve():
    a = sys.stdin.read().split()
    out = []
    for x in a[1:]:
        out.append(str(10**len(x) + 1))
    sys.stdout.write('\n'.join(out) + '\n')

solve()