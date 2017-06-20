import itertools

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
    return [list(x) for x in itertools.product(*t)]

