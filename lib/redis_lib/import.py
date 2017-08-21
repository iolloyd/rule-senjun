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
    return [{'label': x['label'].lower(), 
             'matches': [s.lower() for s in x['matches'].split(',')]
            } for x in query(q)]


def get_labels():
    q = "SELECT id, NAME FROM labels"
    return [{'id': x['id'],
             'name': x['NAME'].lower()
            } for x in query(q)]


def add_match(left, rights): 
    for right in rights:
        left = sorted(left.split(':'))
        left = ':'.join(left)
        r.sadd('match:{}'.format(left), right)
        r.sadd('match:{}'.format(right), left)


def add_rule(rule):
    label = rule['label']
    print('add rule: label', label)
    for match in rule['matches']:
        r.sadd('rules:{}'.format(label), match)
        for part in label.split(':'):
            print('add rule for part', part, match)
            r.sadd('rules:{}'.format(part), match)


def add_item(label):
    print('adding item', label['id'], label['name'])
    r.sadd('item:{}'.format(label['id']), label['name'])
    print('adding label member to ', label['name'], label['id'])
    r.sadd('label:{}'.format(label['name']), 'item:{}'.format(label['id']))
    

def store_rules():
    print('storing rules')
    rules = (x for x in get_matching_rules() if not x['matches'] == [''])
    for x in rules:
        add_rule(x)


def store_labels():
    print('storing labels')
    labels = (x for x in get_labels() if not x['name'] == '')
    for x in labels:
        add_item(x)


if __name__ == '__main__':
    store_rules() 
    store_labels()

