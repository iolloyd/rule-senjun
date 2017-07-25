import bottle
from bottle import (
        route, 
        run, 
        response
        )
from subprocess import (
        PIPE, 
        run as subrun
        )
from os.path import (
        basename, 
        dirname, 
        realpath
        )
from db import (
        get_basics, 
        get_items, 
        get_items_labels, 
        get_images
        )
from redis_store import get_outfit_items
from services import (
        items as api_items, 
        basics as api_basics
        )
import json


def enable_cors(fn):
    def _aux(*args, **kwargs):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
        response.headers['Content-Type'] = 'application/json'
        if bottle.request.method != 'OPTIONS':
            return fn(*args, **kwargs)

    return _aux


def show(data):
    return json.dumps(data, default=str)


@route('/items/<id>/matches', method=['GET', 'OPTIONS'])
@enable_cors
def get_items(id):
    return items(id)


@route('/basics', method=['GET', 'OPTIONS'])
@enable_cors
def basics():
    return show(get_basics())


run(host='localhost', port=3003)
