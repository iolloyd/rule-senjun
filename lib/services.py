import json
from math import floor 
from bottle import route, run, response
from os.path import basename, dirname, realpath
from redis_store import get_outfit_items, get_outfits
from helpers import filtered_combos
from db import (get_basics, get_items, get_items_labels, get_images)

base_url = 'https://s3.amazonaws.com/everywearcom/items/{}_thumb.jpg'

def items(idList):
    items = get_outfit_items(idList)
    return items


def basics():
    items = [(x['id'], x['imageName']) 
             for x in get_basics()
            ]
    return json.dumps(items)


def outfits(idList):
    item_outfits = get_outfit_items(idList)
    item_outfits = [x for x in sorted(item_outfits[:400]) if len(x) == 3]
    return filtered_combos(item_outfits)


def _get_image_path(url): 
    return base_url.format(url.replace('.jpg', ''))


def _get_image_path_list(id_and_url_list):
    return [{'id': x['id'], 
             'url': _get_image_path(x['url'])} 
            for x in id_and_url_list
            ]
