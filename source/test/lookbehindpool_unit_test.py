import os.path, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from lookbehindpool import LookBehindPool


class PoolItem:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def write(self, value):
        self._value = value


def test_capacity():
    pool = LookBehindPool(10, lambda: PoolItem(0))
    assert(pool.capacity == 10)


def test_writing():
    pool = LookBehindPool(10, lambda: PoolItem(0))
    assert(len(pool._pool) == 10)
    pool.update(lambda item: item.write(1))
    assert(pool.current.value == 1)
    pool.update(lambda item: item.write(2))
    assert(pool.current.value == 2)
    assert(pool[1].value == 1)


def test_rollover():
    pool = LookBehindPool(3)
    assert(pool._current_position == 0)
    pool.assign(1)
    assert(pool._current_position == 1)
    assert(pool.current == 1)
    pool.assign(2)
    assert(pool._current_position == 2)
    assert(pool.current == 2)
    pool.assign(3)
    assert(pool._current_position == 0)
    assert(pool.current == 3)
    assert(pool.previous == 2)


def test_read_back():
    pool = LookBehindPool(20, lambda: PoolItem(0))
    for i in range(10):
        pool.update(lambda item: item.write(i))

    result = list(pool.read_back(5, lambda item: item.value))
    assert(len(result) == 5)
    assert(result[0] == 9)
    assert (result[4] == 5)
