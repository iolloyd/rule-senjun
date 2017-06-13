import MySQLdb
from MySQLdb.cursors import DictCursor
from helpers import slugify

db = MySQLdb.connect(user='root', 
                     passwd='root', 
                     db='ewear',
                     cursorclass=DictCursor)
c = db.cursor()

def query(q):
    c.execute(q)
    return c.fetchall()

def get_tags():
    return [x for x in query('select id, slug from tags')]

def get_labels():
    q = "select id, name from labels"
    return [(x['id'], x['name'].replace(' ', '_')) for x in query(q)]

def get_items(item_list):
    if not item_list:
        return []
    ids = ','.join(item_list) 
    q = "select * from items where id in ({})".format(ids)
    print(q)

    return [x for x in query(q)]

def get_items_labels():
    q = """
    SELECT i.id, 
           c.name c_name
    FROM items i 
         JOIN categories c 
           ON i.categoryId = c.id 
          AND i.storeId = 25
    """
    return [{'id': x['id'], 
             'label': slugify(x['c_name'])
             } for x in query(q)]
