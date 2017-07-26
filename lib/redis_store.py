import sys
import redis
import itertools
from functools import reduce
from db import get_items, get_items_labels, get_labels
from redis_conn import r
from helpers import combos, cartesian


def add_match(left, rights): 
    for right in rights:
        left = sorted(left.split(':'))
        left = ':'.join(left)
        r.sadd('match:{}'.format(left), right)
        r.sadd('match:{}'.format(right), left)


def get_matching(labels, matches):
    try:
        matching = [matches[x] for x in matches if x in labels]
        if not matching:
            return []

        labels = ['label:{}'.format(x) for x in matching[0]]
        matches = [r.smembers(x) for x in labels] 
        matches = [clean(list(x)) for x in matches]
        matches = [y for x in matches for y in x]

        return matches
    except:
        print(sys.exc_info)


def clean(lst):
    return [x.decode('utf-8') for x in lst]


def get_members(key):
    keys = ':'.join(sorted(key.split(':')))
    keys = 'label:{}'.format(keys)
    members = clean(r.smembers(keys))
    return members


def get_outfit_type(labels, keys):
    try:
        labels = ['label:{}'.format(x) for x in labels]
        x = r.sunion(labels)
        x = clean(x)
        return list(set(x).intersection(set(keys)))
    except:
        print(sys.exc_info)


def get_outfit_items(ids):
    matches = get_matches()
    labelsLists = [clean(list(r.smembers('item:{}'.format(id))))
                   for id in ids]
    labels = [x for xs in labelsLists for x in xs]
    try:
        keys = get_matching(labels, matches)
    except:
        print(sys.exc_info)

    result = {
        "top": get_outfit_type(['topunder', 'topover'], keys),
        "bottom": get_outfit_type(['jean', 'trouser', 'skirt'], keys),
        "shoes": get_outfit_type(['heels', 'heel', 'boots'], keys), 
        "bag": get_outfit_type(['bag', 'clutch', 'purse', 'wallet'], keys) 
    }

    return get_outfits(result)


def get_outfits(outfit_items):
    vals = [outfit_items[x] 
            for x in outfit_items 
            if not outfit_items[x] == []
            ]
    return cartesian(*vals)


def store_items_labels(labels):
    for x in labels:
        id, name, label = x['id'], x['name'], x['label']
        r.sadd('item:{}'.format(id), name)
        r.sadd('label:{}'.format(name), id)
        r.sadd('item:{}'.format(id), label)
        r.sadd('label:{}'.format(label), id)

        for y in combos(name.split('_')):
            r.sadd('item:{}'.format(id), y)
            r.sadd('label:{}'.format(y), id)

        for y in combos(label.split('_')):
            r.sadd('item:{}'.format(id), y)
            r.sadd('label:{}'.format(y), id)


def store_matches(matches):
    for key, match in matches.items():
        add_match(key, match) 


def normalize_keys(keys):
    keys = [':'.join(sorted(key.split(':'))) for key in keys]
    return keys


def get_item(item):
    return {'shoes': get_items(item['shoes']),
            'bag': get_items(item['bag']),
            'top': get_items(item['bottom']),
            'bottom': get_items(item['top'])
            }


def get_matches():
    return {'boyfriend:jean': ['button:down:shirt'], 
            'button:down:shirt': ['boyfriend:jean', 'clutch:bag', 'heels'],
            'black:tank:top': ['moto:jacket'],
            'moto:jacket': ['black:tank:top'],
            'skinny:jean': ['v-neck:sweater'],
            'v-neck:sweater': ['skinny:jean'],
            'red:shoe': ['black:blazer', 'black:jean'],
            'pencil:skirt': ['button:down:shirt:solid', 'dark:neutral:shoe',
                             'bag:medium:neutral']
            }


def init():
    r.flushdb()
    items_labels = get_items_labels()
    print(items_labels)
    store_items_labels(items_labels)


if __name__ == '__main__':
    init()
