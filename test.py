import redis
from lib.redis_store import add_match, get_outfit_for
from lib.db import get_labels as get_db_labels, get_tags

def load_items(r, items_labels):
    """An item is structured like:
    123: 'x:y:z'
    """
    for key, labels in items_labels.items():
        r.hmset('items', {key: labels})
        r.sadd('labels:{}'.format(labels), key)

def load_matches(r, matches):
    [add_match(r, key, matches) 
     for key, matches in matches.items()]

items = {
    1: 'a:b:c', 2: 'a:c:e', 3: 'a:b:e', 4: 'd:e:f',
    5: 'd:e:g', 6: 'g:j:k', 7: 'a:b:c', 8: 'a:b:e'
}

matches = {
    'top': ['bottom',],
    'jeans:high': ['top:cropped',]
}
