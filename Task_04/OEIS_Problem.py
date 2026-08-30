p = []

for x in range(2, 110000):
    if all(x % i for i in range(2, int(x**.5) + 1)):
        p.append(x)

for _ in range(int(input())):
    n = int(input())
    print(p[0], *[p[i-1]*p[i] for i in range(1, n-1)], p[n-2])