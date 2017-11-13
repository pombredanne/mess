import sys
from datetime import datetime as dt
import threading

IS_PY2 = sys.version_info < (3, 0)

if IS_PY2:
    from Queue import Queue
else:
    from queue import Queue

import time

# Threading class
#################


class Worker(threading.Thread):
    """ Execute tasks from given queue """
    def __init__(self, tasks):
        threading.Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                print("%s || [ERROR] %s") % (now, e)
            finally:
                self.tasks.task_done()


class ThreadPool:
    """ Pool of threads consuming from queue """

    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def map(self, func, arg_list):
        for args in arg_list:
            self.add_task(func, args)

    def wait_completion(self):
        self.tasks.join()
