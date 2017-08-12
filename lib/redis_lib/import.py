import os
import sys
import MySQLdb
import redis
r = redis.Redis(host='localhost', port=6379, db=0) 
from MySQLdb.cursors import DictCursor

db = MySQLdb.connect(user=os.environ['EWEAR_DB_USER'], 
                     passwd=os.environ['EWEAR_DB_PWD'],
                     db=os.environ['EWEAR_DB_NAME'],
                     cursorclass=DictCursor)
c = db.cursor()


def _query(conn):
    def aux(q):
        c.execute(q)
        return c.fetchall()
    return aux 

query = _query(db.cursor())

def get_matching_rules():
    q = "SELECT label, matches FROM label_matches"
    return [{'label': x['label'], 
             'matches': x['matches'].split(',') 
            } for x in query(q)]


def get_labels():
    q = "SELECT id, NAME FROM labels"
    return [{'id': x['id'],
             'name': x['NAME']
            } for x in query(q)]


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


def add_rule(rule):
    for match in rule['matches']:
        r.sadd('rules:{}'.format(rule['label']), match)
        for part in rule['label'].split(':'):
            r.sadd('rules:{}'.format(part), match)


def add_item(label):
    r.sadd('item:{}'.format(label['id']), label['name'])
    r.sadd('label:{}'.format(label['name']), 'item:{}'.format(label['id']))
    

def store_rules():
    rules = [x for x in get_matching_rules() if not x['matches'] == ['']]
    for x in rules:
        add_rule(x)


def store_labels():
    labels = [x for x in get_labels() if not x['name'] == '']
    for x in labels:
        add_item(x)


def import_to_redis():
    store_rules() 
    store_labels()

if __name__ == '__main__':
    import_to_redis()

