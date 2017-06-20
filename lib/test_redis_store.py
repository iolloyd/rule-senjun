from testit import test
from redis_store import get_outfits

if __name__ == '__main__':
    expected = [[1,3], [1,4], [2,3], [2,4]]
    actual = get_outfits({
        'top': [1,2],
        'bottom': [],
        'shoes': [3,4]
    })
    test(sorted(expected), sorted(actual))
