import sys
import json
from services import (items as api_items, 
                      basics as api_basics,
                      outfits as api_outfits,
                      outfits_with_images as api_outfits_with_images
                      )

def items(id, *args):
    return api_items(id)


def basics(*args):
    return api_basics()


def outfits(id, *args):
    return json.dumps(api_outfits(id))


def outfits_with_images(id, *args):
    result = api_outfits_with_images(id)
    return json.dumps(result)


if __name__ == '__main__':
    def _handle_command(cmd, *args):
        try:
            return globals()[cmd](*args)
        except KeyError:
            print('Unknown command:', cmd)

    def _handle_error(choice):
        msgs = {
            'nocmd': 'Missing command. You must provide one',
        }
        try:
            print(msgs[choice])
            exit(1)
        except:
            print('Unknown command')
            exit(1)

    if len(sys.argv) < 1:
        _handle_error('nocmd')

    cmd = sys.argv[1]
    result = _handle_command(cmd, *sys.argv[2:])
    print(result)
