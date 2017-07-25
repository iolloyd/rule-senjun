import json
from math import floor 
from bottle import route, run, response
from os.path import basename, dirname, realpath
from redis_store import get_outfit_items, get_outfits
from helpers import filtered_combos
from db import (get_basics, 
                get_items, 
                get_items_labels, 
                get_images
                )

base_url = 'https://s3.amazonaws.com/everywearcom/items/{}_thumb.jpg'

def items_with_images(id):
    items = get_outfit_items(id)
    return get_images(items)



def items(id):
    items = items_with_images(id)

    return json.dumps(items_with_images)


def basics():
    items = [(x['id'], x['imageName']) for x in get_basics()]

    return json.dumps(items)


def outfits(idList):
    results = set() 
    for x in get_outfit_items(id):
        results.add(x)
    item_outfits = []
    for x in range(1, 400):
        item_outfits.append(results.pop())
    item_outfits = [x for x in sorted(item_outfits[:400]) if len(x) == 3]

    return filtered_combos(item_outfits)

def outfits_with_images(ids):
    item_outfits = outfits(idList)
    result = [get_images(x) for x in item_outfits]
    result = [_get_image_path_list(x) for x in result]
    result = [x for x in result if len(x) == 3]

    return result


def _get_image_path(url): 
    return base_url.format(url.replace('.jpg', ''))


def _get_image_path_list(id_and_url_list):
    return [{'id': x['id'], 
             'url': _get_image_path(x['url'])} 
            for x in id_and_url_list
            ]


if __name__ == '__main__':
    for x in outfits_with_images(27939):
        print([_x['id'] for _x in x])
