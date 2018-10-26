def binomial(n, k):
    if 0 <= k <= n:
        num = 1
        div = 1
        for t in range(min(k, n - k)):
            num *= n
            div *= (t + 1)
            n -= 1
        return num // div
    else:
        return 0

from random import choice
def decimation(n='Lea',m='Fred'):
    return choice(['Lucas','Guillaume','Renaud','Jeremy','Claire','Mimoune','Caps','Cedric', n, m])

