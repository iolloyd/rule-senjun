import redis
from lib.engine import add_match, get_outfit_for

def init_redis(host='localhost', port=6379, db=0):
    r = redis.Redis(host=host, port=port, db=db)
    r.flushdb()
    return r

def load_items(r, items_labels):
    """An item is structured like:
    123: 'x:y:z'
    """
    for key, labels in items_labels.items():
        r.hmset('items', {key: labels})
        r.sadd('labels:{}'.format(labels), key)

def load_matches(r, matches):
    [add_match(r, key, matches) for key, matches in matches.items()]

items = {
    1: 'a:b:c', 2: 'a:c:e', 3: 'a:b:e', 4: 'd:e:f',
    5: 'd:e:g', 6: 'g:j:k', 7: 'a:b:c', 8: 'a:b:e'
}

matches = {
    'a:b:c': ['a:b:e', 'd:e:f'],
    'a:c:e': ['d:e:g'],
    'a:b:e': ['g:j:k']
}

r = init_redis()
load_items(r, items)
load_matches(r, matches)

actual = set(get_outfit_for(r, 1))
expected = {'3', '4', '8'}
assert actual == expected

actual = set(get_outfit_for(r, 2))
expected = {'5'}
assert actual == expected

actual = set(get_outfit_for(r, 6))
expected = {'3', '8'}
assert actual == expected
