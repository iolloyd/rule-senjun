import sys
import itertools
import redis

r = redis.Redis(host='localhost', port=6379, db=0) 


def cartesian(*t):
    t = sorted(t, key=len, reverse=True)
    t = [x for x in t if not x == []]
    return [list(x) for x in product(*t)]


def clean(lst):
    return [x.decode('utf-8') for x in lst]


def get_outfits(ids):
    """In redis, we manually set relations. For each of the 'rules', we
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
        //  [1 2 3   5 6], 
        //    [2 3 4 5] 
        //    [2   4 5 6 7 8] 
        //  = [2 3   5]
    """
    items = ['item:{}'.format(item_id) for item_id in ids]
    labels = list(itertools.chain([get_labels(item_id) for item_id in items]))
    label_rules = [x.replace('label:', 'rules:') for y in labels for x in y]
    list_of_rules = clean(r.smembers('rules:list'))
    matching_rule_keys = [x for x in list_of_rules if x in label_rules]
    rules_to_labels = [x.replace('rules:', 'label:') for x in list_of_rules]
    matching_ids = [clean(r.smembers(x)) for x in rules_to_labels]
    return labels


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
        labels = [x for x in labels]
        x = r.sunion(labels)
        x = clean(x)
        return list(set(x).intersection(set(keys)))
    except:
        print(sys.exc_info)


def get_outfit_items(id):
    labels = [clean(list(r.smembers('item:{}'.format(id))))]
    print('labels', labels)
    keys = get_matching(labels)
    result = {
        "top": has_label(['topunder', 'topover'], keys),
        "bottom": has_label(['jean', 'trouser', 'skirt'], keys),
        "shoes": has_label(['heels', 'heel', 'boots'], keys), 
        "bag": has_label(['bag', 'clutch', 'purse', 'wallet'], keys) 
    }

    return get_outfits(result)


