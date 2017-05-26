import redis

def combos_aux(active, tail, a):
    if (not active) and (not tail):
        return
    if not tail:
        a.append(active)
    else:
        combos_aux(active + [tail[0]], tail[1:], a)
        combos_aux(active, tail[1:], a)
    return a

def combos(lst):
    return combos_aux([], lst, [])

def get_labels(id):
    return [x for x in items if x[0] == id][0][1:]

def setFromTuple(tup):
    return [set(x.split(':')) for x in tup]

def getValidMatches(labels, matches):
    labelsSet = set(labels)
    matchesSets = [setFromTuple(x) for x in matches]
    validMatches = [x for x in matchesSets if labelsSet in x]
    result = [x for x in validMatches[0] if not x == labelsSet]
    return result

def add_match(r, labels_str, matches):
    labels = labels_str.split(':')
    match_combos = combos(labels)
    match_combos = [":".join(x) for x in match_combos]
    [r.sadd('m_:{}'.format(match), *matches) for match in match_combos]
    [r.sadd('m_:{}'.format(match), labels_str) for match in matches]

def get_outfit_for(r, id):
    labels_to_match = r.hget('items', id)
    decoded = 'm_:{}'.format(labels_to_match.decode('utf-8'))
    matching_labels = [x.decode('utf-8') for x in r.smembers(decoded)]
    matching_items = [r.smembers('labels:{}'.format(x)) for x in matching_labels]
    matching_items = [y for x in matching_items for y in x]
    matching_items = [x.decode('utf-8') for x in matching_items]
    return matching_items
    print(matching_items)

