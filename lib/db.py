import os
import sys
import MySQLdb
from MySQLdb.cursors import DictCursor
from helpers import slugify

db = MySQLdb.connect(user=os.environ['EWEAR_DB_USER'], 
                     passwd=os.environ['EWEAR_DB_PWD'],
                     db='ewear',
                     cursorclass=DictCursor)
c = db.cursor()

base_url = 'https://s3.amazonaws.com/everywearcom/items/{}_thumb.jpg'

def query(q):
    c.execute(q)
    return c.fetchall()


def get_tags():
    return [x for x in query('select id, slug from tags')]


def get_labels():
    q = "select id, name from labels"
    return [(x['id'], x['name'].replace(' ', '_')) for x in query(q)]


def get_images(ids):
    q = """
    SELECT 
        i.id,
        min(im.imageName) url
    FROM
        (select id from bloomingdales_items where id in ({})) i,
        images im
    WHERE i.id = im.itemId
    GROUP BY i.id
    """
    results = {} 
    ids = [y for x in ids for y in x]
    ids = [x for x in ids if not x == []]
    if not ids:
        return None
    qry = q.format(','.join(map(str, ids)))
    results = query(qry)

    return [x for x in results]


def replace_values(dict_like, str):
    result = {}
    for x in dict_like:
        result[x] = [str.format(x['url'][:-4]) for x in dict_like[x]]

    return result


def get_items(item_list):
    """base_url = 'https://s3.amazonaws.com/everywearcom/items/{}_web_chat.jpg'
    """
    if not item_list:
        return []
    ids = ','.join(item_list) 
    q = """
    SELECT i.id, replace(im.imageName, '.jpg', '') imageName
    FROM bloomingdales_items i 
    JOIN images im on i.id = im.itemId 
    WHERE i.id in ({})
    """.format(ids)

    print(q)
    return [x for x in query(q)]


def get_basics():
    q = """
    select b.*, im.imageName imageName
    from basics b
    join images im on b.id = im.itemId
    """
    return [x for x in query(q)]

def get_items_labels():
    q = """
    SELECT i.id id, c.name name, c.type c_name
    FROM bloomingdales_items i 
         JOIN categories c 
           ON i.categoryId = c.id 
          AND i.storeId = 25
    """
    return [{'id': x['id'],
             'name': slugify(x['name']),
             'label': slugify(x['c_name'])
             } for x in query(q)]

