def add_match(left, rights): 
    for right in rights:
        left = sorted(left.split(':'))
        left = ':'.join(left)
        r.sadd('match:{}'.format(left), right)
        r.sadd('match:{}'.format(right), left)


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


