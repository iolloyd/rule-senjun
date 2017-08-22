import os
import sys
import MySQLdb
from MySQLdb.cursors import DictCursor
from helpers import slugify

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


def get_labels():
    q = "select id, name from labels"
    return [(x['id'], x['name'].replace(' ', '_')) for x in query(q)]


def get_items_labels(store_id):
    q = """
    SELECT i.id id, c.name name, c.type c_name
    FROM bloomingdales_items i 
         JOIN categories c 
           ON i.categoryId = c.id AND i.storeId = {} 
    """.format(store_id)
    return [{'id': x['id'],
             'name': slugify(x['name']),
             'label': slugify(x['c_name'])
             } for x in query(q)]


def get_matching_rules():
    q = "SELECT label, matches FROM label_matches"
    return [{'label': x['label'], 
             'matches': x['matches'].split(',') 
            } for x in query(q)]
