import redis
from db import get_items_labels, get_labels
from redis_conn import r

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

def setFromTuple(tup):
    return [set(x.split(':')) for x in tup]

def getValidMatches(labels, matches):
    labelsSet = set(labels)
    matchesSets = [setFromTuple(x) for x in matches]
    validMatches = [x for x in matchesSets if labelsSet in x]
    result = [x for x in validMatches[0] if not x == labelsSet]
    return result

def add_match(r, label, matches):
    print('*')
    print(matches)
    print('*')
    for matching_label in matches:
        r.sadd('match:{}'.format(label), matching_label)

def get_outfit_for(r, id):
    labels_to_match = r.smembers('items:{}:labels'.format(id))
    print(labels_to_match)
    decoded = [x.decode('utf-8') for x in labels_to_match]
    decoded = [x for x in decoded if x != [':']]
    matching_labels = [x.decode('utf-8') for x in r.smembers(decoded)]
    matching_items = [r.smembers('labels:{}'.format(x)) for x in matching_labels]
    matching_items = [y for x in matching_items for y in x]
    matching_items = [x.decode('utf-8') for x in matching_items]
    return matching_items

def store_items_labels(r, items_labels):
    for item_id, item_labels in items_labels:
        for label in item_labels.split(':'):
            r.sadd('item:{}:labels'.format(item_id), label)

def store_labels(r, labels):
    for id, label in labels:
        r.hmset('labels', {id: label})
        r.sadd('label_{}'.format(label), id)

def store_matches(r, matches):
    for key, match in matches.items():
        print('matching ', key, ' to ', match) 
        add_match(r, key, match) 

if __name__ == '__main__':
    matches = {
        'top': 'bottom',
        'jeans:high': 'top:cropped',
        'bottom:blue': 'top:blue',
        'blue': 'blue'
    }
    items_labels = get_items_labels()
    store_items_labels(r, items_labels)
    store_matches(r, matches)
    """
    x = get_outfit_for(r, 29299)
    print(x)
    """
