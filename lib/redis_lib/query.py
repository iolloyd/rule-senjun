import sys
import itertools 
import math
import redis
from functools import reduce

r = redis.Redis(host='localhost', port=6379, db=0) 

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
    t = map(lambda x, y=longest: fill(x, y), t)
    return list(zip(*t))

def clean(lst):
    return [x.decode('utf-8') for x in lst]


def outfits_from_ids(ids):
    tops = has_label(['label:top'], ids)
    bottoms = has_label(['label:skirt'], ids)
    heels = has_label(['label:heel'], ids)
    return matched_outfits(tops, bottoms, heels)


def get_outfits(ids):
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
    return outfits_from_ids(ids)


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


def get_outfit_items(ids):
    pass


if __name__ == '__main__':
    outfits = get_outfits(sys.argv[1:])
