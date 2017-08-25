from lookbehindpool import LookBehindPool, SafePoolTransit

import time

class PoolItem:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def write(self, value):
        self._value = value


def test_dummy():
    source_pool = LookBehindPool(10, lambda: PoolItem(0))
    target_pool = LookBehindPool(10, lambda: PoolItem(0))    
    
    safe_pool = SafePoolTransit(source_pool, target_pool, lambda source, target: target.write(source.value))
    #SafeFanInTransit()
    #SafeFanOutTransit()
    safe_pool.start()

    bookmark = target_pool.bookmark
    source_pool.update(lambda item: item.write(0))
    #safe_pool.queue_assign(buffer.current)
    time.sleep(0.1) # give it some time to transit
    safe_pool.stop()    

    if bookmark.is_stale:
        for pool_item in bookmark.keep_up():
            assert(pool_item.value)    
    
    
