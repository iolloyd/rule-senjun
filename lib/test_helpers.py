from testit import test
from helpers import combos, cartesian

if __name__ == '__main__':
    expected = [[1,3], [1,4], [2,3], [2,4]]
    actual = cartesian([1,2], [3,4])
    test(expected, actual)

    expected = sorted(set(['1:2', '1', '2:1', '2']))
    actual = sorted(set(combos(['1','2'])))
    test(expected, actual)
