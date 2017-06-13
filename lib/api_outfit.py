from bottle import route, run, response
from subprocess import PIPE, run
from os.path import basename, dirname, realpath

@route('/outfits/<id>')
def index(id):
    base = realpath(__file__)
    cmd = ["/usr/local/bin/python3", 
           "/Users/lloyd/projects/rules/lib/redis_store.py", 
           id]
    result = run(cmd, 
                 stdout=PIPE, 
                 stderr=PIPE, 
                 universal_newlines=True) 

    return result.stdout

run(host='localhost', port=3300)
