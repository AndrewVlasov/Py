l = []
n = int(input('сколько чисел?'))
for i in range(n):
    x = int(input('введите число'))
    l.append(x)
if l.index(0) >= 0:
    k = 0
    s = 0
    for i in range(l.index(0)):
        k = l[i] + k
    l.insert(l.index(0), k)
    for i in range(l.index(0), len(l)):
        s = l[i] + s
    l.insert(l.index(0)+1, s)

    print(l.index(0))

print(*l)
