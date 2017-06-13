import sys
import redis
import itertools
from functools import reduce
from db import get_items, get_items_labels, get_labels
from redis_conn import r

def combos(lst):
    out = [] 
    for L in range(0, len(lst)+1):
        for subset in itertools.permutations(lst, L):
            out.append(subset)

    out = [x for x in out if x]
    return [':'.join(x) for x in list(set(out))]


def add_match(left, rights): 
    for right in rights:
        left = sorted(left.split(':'))
        left = ':'.join(left)
        r.sadd('match:{}'.format(left), right)
        r.sadd('match:{}'.format(right), left)


def get_matching(labels, matches):
    matching = [matches[x] for x in matches if x in labels][0]
    print('matching rules', matching)
    labels = ['label:{}'.format(x) for x in matching]
    matches = [r.smembers(x) for x in labels]
    matches = [clean(list(x)) for x in matches]
    matches = [y for x in matches for y in x]

    return matches


def clean(lst):
    return [x.decode('utf-8') for x in lst]


def get_members(key):
    keys = ':'.join(sorted(key.split(':')))
    keys = 'label:{}'.format(keys)
    members = clean(r.smembers(keys))
    return members


def get_outfit_type(labels, keys):
    labels = ['label:{}'.format(x) for x in labels]
    x = r.sunion(labels)
    x = clean(x)
    return list(set(x).intersection(set(keys)))


def get_outfit_items(id, matches):
    labels = clean(list(r.smembers('item:{}'.format(id))))
    keys = get_matching(labels, matches)

    return {
        "top": get_outfit_type(['top'], keys),
        "bottom": get_outfit_type(['jean', 'trouser', 'skirt'], keys),
        "shoes": get_outfit_type(['heels', 'heel', 'boots'], keys), 
        "bag": get_outfit_type(['bag', 'clutch', 'purse', 'wallet'], keys) 
    }


def store_items_labels(labels):
    for x in labels:
        id, label = x['id'], x['label']
        r.sadd('item:{}'.format(id), label)
        r.sadd('label:{}'.format(label), id)
        for y in combos(label.split('_')):
            r.sadd('item:{}'.format(id), y)
            r.sadd('label:{}'.format(y), id)


def store_matches(matches):
    for key, match in matches.items():
        add_match(key, match) 


def init():
    r.flushdb()
    items_labels = get_items_labels()
    store_items_labels(items_labels)
    store_matches(matches)


def normalize_keys(keys):
    keys = [':'.join(sorted(key.split(':'))) for key in keys]
    return keys

def get_item(item):
    return {'shoes': get_items(item['shoes']),
            'bag': get_items(item['bag']),
            'top': get_items(item['bottom']),
            'bottom': get_items(item['top'])
            }

if __name__ == '__main__':
    item_id = sys.argv[1]
    if not item_id:
        print('You need to provide an item_id')
        exit(1)

    matches = {'boyfriend:jean': ['button:down:shirt'], 
               'button:down:shirt': ['boyfriend:jean', 'clutch:bag', 'heels'],
               'black:tank:top': ['moto:jacket'],
               'moto:jacket': ['black:tank:top'],
               'skinny:jean': ['v-neck:sweater'],
               'v-neck:sweater': ['skinny:jean']
               }

    # init()
    x = get_outfit_items(sys.argv[1], matches)
    x = get_item(x)
    print(x)
    
