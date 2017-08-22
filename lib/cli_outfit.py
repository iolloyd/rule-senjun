import sys
import json
from redis_lib.query import get_outfits


if __name__ == '__main__':
    """Test load data using test/load.sh.

    run by the following command:
        python3 cli_outfit.py 112 223
    """
    ids = sys.argv[1:]
    results = get_outfits(ids)
    [print(x) for x in results]
