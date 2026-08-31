from random import randint
from collections import Counter
def d6():
    return randint(1,6)

def gr(count:int, prior:list, tp = None):
    priority_map = {num: index for index, num in enumerate(prior)}

    gr_gen = [(d6(),d6()) for _ in range(count)]
    match tp:
        case None:
            gr_list = gr_gen
        case 'A':
            gr_list = [i if (1 in i) or (2 in i) else d6() for i in gr_gen]
        case 'B':
            gr_list = [i if (3 in i) or (4 in i) else d6() for i in gr_gen]
        case 'C':
            gr_list = [i if (5 in i) or (6 in i) else d6() for i in gr_gen]
    
    redraw = [i for i in gr_list if type(i) == int]
    choice = [i for i in gr_list if type(i) == tuple]
    
    
    result = [min(t, key=priority_map.get) for t in choice] + redraw
    print(result)
    res = dict(Counter(result))
    ct = [0,0,0,0,0,0]
    for key in res.keys():
        ct[key-1] = res[key]
    rt = f'成長 {count}次 順序 {prior}\n' + \
    f'靈巧: {ct[0]}\n' + \
    f'敏捷: {ct[1]}\n' + \
    f'力量: {ct[2]}\n' + \
    f'生命: {ct[3]}\n' + \
    f'智力: {ct[4]}\n' + \
    f'精神: {ct[5]}\n'
    if tp:
        rt += f'使用勇者之證: {tp}'
    return rt




