import random
from os import chdir, path
from sympy import sympify

chdir(path.dirname(path.abspath(__file__)))

# gonna abandon!
def dn(n) -> int:
    return random.randint(1,n)

def d6() -> int: 
    return random.randint(1,6)

def d66() -> int:
    a = d6()
    b = d6()
    return str(int(str(a)+str(b)))

def nd6(n):
    ls= [d6() for _ in range(n)]
    total = sum(ls)
    phs = '+'.join(map(str, ls))

    return f'{total}[{phs}]', total

def ndm(n:int, m:int):
    ls = [random.randint(1,m) for _ in range(n)]
    total = sum(ls)
    phs = '+'.join(map(str, ls))
    return f'{total}[{phs}]', total


def ndmplus(n:int, m:int, plus = 0):
    ls = [random.randint(1,m) for _ in range(n)]
    total = sum(ls) + plus
    phs = '+'.join(map(str, ls))
    return f'{n}d{m}+{plus}:[{phs}]+{plus} > **{total}**', total

def xndmplus(comm:str):
    ls = comm.split('+')
    plus = []
    dice = []
    for l in ls:
        if 'd' in l:
            dice.append(l)
        else:
            try:
                plus.append(int(l))
            except:
                pass
    
    plsum = sum(plus)

    phr = []
    total = 0

    for d in dice:
        try:
            l = [int(t) for t in d.split('d')]
            if l[0] > 100:
                raise ValueError
            if l[1] > 10000:
                raise ValueError
            if type(l[0])!= int and type[l[1]] != int:
                raise TypeError
            ph, to = ndm(l[0],l[1])
            phr.append(ph)
            total += to
        except Exception as e:
            print('Bad dice roll.')
            return None
    
    return f'{comm}: {'+'.join(phr)} + {plsum} > **{total+plsum}**'

def eval_eq(eq):
    return sympify(eq)



if __name__ == '__main__':
    for i in range(40):
        print(d66())