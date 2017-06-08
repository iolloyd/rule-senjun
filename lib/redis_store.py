import sys
import redis
import itertools
from functools import reduce
from db import get_items_labels, get_labels
from redis_conn import r

def combos(lst):
    out = []
    for L in range(0, len(stuff)+1):
        for subset in itertools.permutations(stuff, L):
            out.append(subset)


def add_match(left, rights): 
    for right in rights:
        left = sorted(left.split(':'))
        left = ':'.join(left)
        r.sadd('match:{}'.format(left), right)
        r.sadd('match:{}'.format(right), left)


def get_matching(labels):
    keys = ['match:{}'.format(x) for x in labels]
    keys = [x.decode('utf-8') for x in r.sinter(*keys)]
    keys = [':'.join(sorted(x.split(':'))) for x in keys]
    return keys


def clean(lst):
    return [x.decode('utf-8') for x in lst]

def get_members(key):
    keys = ':'.join(sorted(key.split(':')))
    keys = 'label:{}'.format(keys)
    print('>', keys)
    members = clean(r.smembers(keys))
    print(members)
    return members


def get_outfit_type(label, keys):
    keys = ['label:{}'.format(x) for x in keys]
    lbl = 'label:{}'.format(label)
    ks = [clean(r.sinter(x, lbl)) for x in keys] 
    ks = [x for x in ks if x != []] 
    return reduce(lambda x, y: x + y, ks, [])


def get_outfit_for(id):
    labels = clean(list(r.smembers('item:{}'.format(id))))
    print('labels', labels)
    keys = get_matching(labels)
    print('keys', keys)

    all = [get_members(x) for x in keys]
    all = reduce(lambda x, y: x + y, all)
    print('all', all)

    return {
        'top': get_outfit_type('top', keys),
        'bottom': get_outfit_type('bottom', keys),
        'shoes': get_outfit_type('shoe', keys), 
        'bag': get_outfit_type('bag', keys) 
    }


def maybe(lst):
    return lst and lst[0] or False

def store_items_labels(labels):
    for id, label in labels:
        label = sorted(label)
        label = ':'.join(label)
        r.sadd('item:{}'.format(id), label)
        r.sadd('label:{}'.format(label), id)


def store_matches(matches):
    for key, match in matches.items():
        add_match(key, match) 


def init():
    items_labels = get_items_labels()
    store_items_labels(items_labels)
    store_matches(matches)


def normalize_keys(keys):
    keys = [':'.join(sorted(key.split(':'))) for key in keys]
    return keys


def load_test_items():
    items = {
        123: ['top:crop'],
        124: ['clutch:bag'],
        125: ['vneck:sweater:top'],
        126: ['skinny:jean:bottom'],
        127: ['coat:top'],
        128: ['bottom:blazer'],
        129: ['solid:skirt:pencil:bottom']
    }

    for k, vs in items.items():
        for item in items:
            keys = normalize_keys(items[item])
            for k in keys:
                r.sadd('item:{}'.format(k), item)
                r.sadd('item:{}'.format(item), k)
                r.sadd('label:{}'.format(k), item)
                r.sadd('label:{}'.format(item), k)
                for kk in k.split(':'):
                    r.sadd('label:{}'.format(kk), item)


def test_init():
    r.flushdb()
    load_test_items()
    store_matches(matches)

if __name__ == '__main__':
    item_id = sys.argv[1]
    if not item_id:
        print('You need to provide an item_id')
        exit(1)

    matches = {
        'blazer:top': ['leather:bottom', 'cami', 'top:tshirt', 'flare:jean:bottom',
                   'leather:skinny:bottom', 'button_down:shirt:top', 
                   'skinny:jean:bottom', 'straightleg:trouser:bottom',],

        'bodycon:dress:top': ['utility:jacket:top', 'blazer:top',
                          'leather:jacket:top', ],

        'boots:shoe': ['utility:jacket:top', 'skinny:jean:bottom', ],

        'bucket:bag': ['solid:pencil:skirt:bottom', 'utility:jacket:top',
                       'cami:top', 'skinny:jean:bottom', ],

        'bulk:coat:top': ['straight_leg:trouser:bottom', 'solid:pencil:skirt',
                          'skinny:jean:bottom', 'longsleeve:blouse:top',
                          'vneck:sweater:top', 'buttondown:shirt:top',
                          'tshirt:top', 'bottom:boyfriend:jean',
                          'flare:jean:bottom', 'cami:bottom',
                          'leather:skinny:bottom', 'aline:skirt:bottom', ],

        'buttondown:shirt': ['solid:pencil:skirt', 'straightleg:trouser',
                             'aline:skirt:bottom', 
                             'leather:skinny', 'skinny:jean', 'boyfriend:jean', ],

        'clutch:bag': ['boyfriend:jean', 'vneck:sweater', 'aline:skirt:bottom',
                       'skinny:jean', 'cami', 'coat:top', ], 

        'crop:top': ['solid:pencil:skirt:bottom', 'utility:jacket:top',
                     'leather:skinny:bottom',
                     'straightleg:trouser:bottom', 'boyfriend:jean:bottom',
                     'aline:skirt:bottom',
                     'skinny:jean:bottom', 'blazer:bottom', ],

        'earrings': ['cardigan', 'cami', ],

        'daytime:dress': ['cardigan', 'blazer', 'coat:top', 'leather:jacket', 'utility:jacket', ],

        'evening:gown:top': ['leather:jacket:top', 'blazer:top', ],

        'heels': ['boyfriend:jean', 'skinny:jean', 'solid:pencil:skirt',
                  'aline:skirt:bottom', 'flare:jean', 't-shirt',
                  'straight:leg:trouser', 'long:sleeve:blouse',],

        'maxi:dress': ['utility:jacket', 'leather:jacket', 'blazer', 'cardigan',],

        'satchel:bag': ['buttondown:shirt', 'cardigan', 'flare:jean', 'cutoff:shorts', 'cami', 'utility:jacket',
                        'longsleeve:blouse', 'vneck:sweater', 'tshirt', 'boyfriend:jean', 'skinny:jean', 'solid:pencil:skirt',
                        'aline:skirt:bottom', 'leather:jacket', 'coat:top', 'cardigan', 'leather:skinny', ],

        'sheath:dress': ['blazer', 'utility:jacket', 'cardigan',
                         'leather:jacket', 'coat:top', ],

        'shift:dress': ['vneck:sweater', 'cardigan', 'leather:jacket',
                        'coat:top', 'utility:jacket', ], 

        'shortsleeve:blouse': ['skinny:jean', 'cutoff:shorts', 'solid:pencil:skirt', 'blazer',
                               'leather:skinny', 'aline:skirt:bottom', ],

        'test:one': ['test:top', 'test:bottom', 'test:shoe', 'test:bag', ]
    }

    test_init()
    x = get_outfit_for(sys.argv[1])

    for y in x:
        print(y, len(x[y]), x[y])

