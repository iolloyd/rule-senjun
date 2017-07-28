from itertools import permutations, product


def combos(lst):
    out = [] 
    for L in range(0, len(lst)+1):
        for subset in permutations(lst, L):
            out.append(subset)
    out = [x for x in out if x]
    return [':'.join(x) for x in list(set(out))]


def cartesian(*t):
    t = sorted(t, key=len, reverse=True)
    t = [x for x in t if not x == []]
    return [list(x) for x in product(*t)]


def filtered_combos(lsts):
    seen = set() 
    combos = []
    for x in lsts:
        to_check = [(x[i], x[i+1]) for i in range(0, len(x)-2)]
        to_check += [(x[i], x[i+2]) for i in range(0, len(x)-2)]
        to_check += [(x[i+1], x[i+2]) for i in range(0, len(x)-2)]
        match = [x for x in to_check if x in seen]
        if not match: 
            combos.append(x)
            for x in to_check: seen.add(x)
    return sorted(combos)


