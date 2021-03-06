import json
import sys
import itertools 
import math
import redis
from functools import reduce

r = redis.Redis(host='localhost', port=6379, db=0) 

def cyclic(lst, count):
    if len(lst) >= count:
        return lst
    buffer = lst[:]
    while (len(buffer) < count):
        buffer = buffer + lst
    return buffer[:count]

def combos_aux(active, tail, a):
    if (not active) and (not tail):
        return
    if not tail:
        a.append(active)
    else:
        combos_aux(active + [tail[0]], tail[1:], a)
        combos_aux(active, tail[1:], a)
    return a


def combos(*lsts):
    return combos_aux([], lsts, [])


def fill(lst, count):
    c = len(lst)
    if (c >= count):
        return lst
    return lst + [lst[-1]] * (count - c)


def matched_outfits(*t):
    longest = reduce(max, [len(x) for x in t])
    t = map(lambda x, y=longest: cyclic(x, y), t)
    return list(zip(*t))


def clean(lst):
    return [x.decode('utf-8') for x in lst]


def outfits_from_ids(ids):
    tops = has_label(['label:top'], ids)
    bottoms = has_label(['label:skirt'], ids)
    heels = has_label(['label:heel'], ids)
    return matched_outfits(tops, bottoms, heels)


def contains_label(label, item_id):
    return label in r.smembers('item:{}'.format(item_id))

def all_have_label(label, lst):
    matches = [x for x in lst if contains_label(label, x)]
    return len(matches) == lst


def filtered_outfits(outfits, filter_labels):
    for label in filter_labels:
        outfits = [x for x in outfits if all_have_label(label, x)]
    return outfits


def get_outfits(ids, filters=None):
    """
        In redis, we manually set relations. For each of the 'rules', we
        add the key as a member of the set 'rules:list'.
        example:
        rules:fluffy:boots => label:fluffy:top label:fluffy:coat label: furry:hat
        rules:leather:top  => label:sexy:boots label:leather:jeans
        rules:list => rules:fluffy:boots rules:leather:top
        1. For each id, fetch the labels it has. 
        // item:453 = ['label:sexy:boots']
        2. Find any rules that have a key that matches. 
        // rules:sexy:boots = ['label:leather:jeans', 'label:leather:top']
        3. Find item ids that have those labels. 
        // label:leather:jeans = [223, 227, 229] 
        // label:leather:top = [112, 133, 144]
        4. Find the ids that exist in all the results.
        //  [1 2 3 _ 5 6 _ _], 
        //  [_ 2 3 4 5 _ _ _] 
        //  [_ 2 _ 4 5 6 7 8] 
        // =[_ 2 _ _ 5 _ _ _]
    """
    items = ['item:{}'.format(item_id) for item_id in ids]
    labels = list(map(get_labels, items))
    labels = list(reduce(set.intersection, map(set, labels)))
    labels = ['label:{}'.format(x) for x in labels]
    label_rules = [x.replace('label:', 'rules:') for x in labels]
    matching = [clean(r.smembers(x)) for x in label_rules]
    m_rules = [x for y in matching for x in y]
    m_rules = [x.split(':') for x in m_rules]
    m_rules = [x for y in m_rules for x in y]
    m_labels = ['label:{}'.format(x) for x in m_rules]
    ids = [clean(r.smembers(x)) for x in m_labels]
    ids = [x for y in ids for x in y] 
    ids = ["item:{}".format(x.replace('item:', '')) for x in ids]
    outfits = outfits_from_ids(ids)
    if (filters):
        outfits = filtered_outfits(outfits, filters)

    return outfits


def get_labels(item_id):
    labels = clean(r.smembers(item_id))
    return labels


def get_matching(labels):
    matches = get_match_rules()
    labels = [x for y in labels for x in y]
    try:
        matching = [matches[x] for x in matches if x in labels]
        if not matching:
            return []

        matches = [r.smembers(x) for x in matching[0]] 
        matches = [clean(list(x)) for x in matches]
        matches = [y for x in matches for y in x]
        return matches
    except:
        print(sys.exc_info)


def has_label(labels, keys):
    try:
        x = r.sunion(labels)
        x = clean(x)
        return list(set(x).intersection(set(keys)))
    except:
        print(sys.exc_info)


if __name__ == '__main__':
    args = sys.argv[1:]
    ids = [x for x in args if not x.startswith('-')]
    filters = [x.replace('-', '') for x in args if x.startswith('-')]
    outfits = get_outfits(ids, filters)
    outfits = json.dumps(outfits)
    print(outfits)
