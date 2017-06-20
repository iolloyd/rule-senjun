def test(expected, actual):
    exp = expected
    act = actual
    if not exp == act:
        print('expected', exp)
        print('actual', act)
    else:
        print('OK')
