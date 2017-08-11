import sys
import json
from redis_lib.query import get_outfits


def outfits(ids):
    result = get_outfits(ids)
    return [a for b in result for a in b]


if __name__ == '__main__':
    """Test load data using test/load.sh.

    run by the following command:
        python3 cli_outfit.py 112 223
    """
    ids = sys.argv[1:]
    print(ids)
    results = outfits(ids)
    print(results)
