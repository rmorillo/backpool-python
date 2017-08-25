from lookbehindpool import LookBehindPool
from threading import Thread
from queue import Queue

class LookBehindSafely:
    def __init__(self, unsafe_pool, update_lambda=None):
        self._unsafe_pool = unsafe_pool
        self._update_lambda = update_lambda
        self._queue = Queue()        
        self._is_update_mode = update_lambda is not None
        self._queue_worker = None
        self._enabled = False

    def start(self):
        self._queue_worker = Thread(target=self.queue_reader_loop, args=())
        self._queue_worker.setDaemon(True)
        self._enabled = True
        self._queue_worker.start()

    def empty_up_queue(self):
        queue = self._queue
        while not queue.empty():
            self._update_lambda(queue.get(), self._unsafe_pool._pool[self._unsafe_pool._current_position])            
        
    def queue_reader_loop(self):
        while self._enabled:
            if self._is_update_mode:
                self.empty_up_queue()
                
    def queue_assign(self, value):
        self._queue.put(value)

    def stop(self):
        self._enabled = False

    
    
