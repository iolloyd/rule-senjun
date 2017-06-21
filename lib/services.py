import json
from bottle import route, run, response
from os.path import basename, dirname, realpath
from redis_store import get_outfit_items, get_outfits
from db import (get_basics, 
                get_items, 
                get_items_labels, 
                get_images
                )


def items_with_images(id):
    items = get_outfit_items(id)
    items_with_images = get_images(items)


def items(id):
    items = items_with_images(id)

    return json.dumps(items_with_images)


def basics():
    items = [(x['id'], x['imageName']) for x in get_basics()]
    return json.dumps(items)


def outfits(id):
    item_outfits = get_outfit_items(id)
    return item_outfits[:10]

