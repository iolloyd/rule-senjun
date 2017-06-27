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
    return sorted([list(x) for x in product(*t, repeat=1)])


def filtered_combos(lst):
    seen = [] 
    results = []
    for y in lst:
        for x in y:
            print(x)
            # keys = [frozenset([x[0], x[1]]), frozenset([x[0], x[2]]), frozenset([x[1], x[2]])]
            # matches = [x for x in set(seen) if x in keys] 
            if not matches:
                results.append(x)
            for k in keys:
                seen.append(k) 

    return results


if __name__ == '__main__':
    data = [['a1', 'a2', 'a3'],
            ['b1', 'b2', 'b3'],
            ['c1', 'c2', 'c3']]

    prod = cartesian(*data)
    x = filtered_combos(prod)
    print(x)
