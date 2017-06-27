from itertools import product, groupby

def slugify(x):
    return x.replace(' ', '_').lower()

def combos(lst):
    out = [] 
    for L in range(0, len(lst)+1):
        for subset in itertools.permutations(lst, L):
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


if __name__ == '__main__':
    data = [['a1', 'a2', 'a3' ],
            ['b1', 'b2', 'b3', 'b4'],
            ['c1', 'c2', 'c3'],
            ]

    prod = cartesian(*data)
    x = filtered_combos(prod)
    for a in x:
        print(a)
