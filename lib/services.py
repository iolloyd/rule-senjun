from bottle import route, run, response
from os.path import basename, dirname, realpath
from db import get_basics, get_items, get_items_labels, get_images
from redis_store import get_outfit_items
import json


def items(id):
    items = get_outfit_items(id)
    items_with_images = get_images(items)

    return json.dumps(items_with_images)


def basics():
    items = [(x['id'], x['imageName']) for x in get_basics()]

    return json.dumps(items)


