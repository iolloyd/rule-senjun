def cyclic(lst, count):
    if len(lst) >= count:
        return lst
    buffer = lst[:]
    while (len(buffer) < count):
        buffer = buffer + lst
    return buffer[:count]


if __name__ == "__main__":
    x = [2, 4, 7]

    assert(cyclic(x, 2) == [2, 4, 7])
    assert(cyclic(x, 4) == [2, 4, 7, 2])
    assert(cyclic(x, 8) == [2, 4, 7, 2, 4, 7, 2, 4])

