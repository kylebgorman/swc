#!/usr/bin/env python

import os

from Queue import Queue
from threading import Thread

## HELPERS TO DETERMINE NUMBER OF THREADS TO USE

def _ncpu():
    """
    Determine the number of CPUs. Heuristics taken from a StackOverflow thread.
    """
    # Python 2.6
    try: 
        from multiprocessing import cpu_count
        return cpu_count()
    except (ImportError, NotImplementedError):
        pass
    # POSIX
    try: 
        return int(os.sysconf('SC_NPROCESSORS_ONLN'))
    except (AttributeError, ValueError):
        pass
    # Windows
    try:
        return int(os.environ['NUMBER_OF_PROCESSORS'])
    except (KeyError, ValueError):
        pass
    # Jython
    try:
        from java.lang import Runtime
        return Runtime.getRuntime().availableProcessors()
    except (KeyError, ValueError):
        pass


## now compute this number once for the module
_number_of_cpus = _ncpu()


class Mapper(Thread):
    """
    Generic mapper thread
    """
    def __init__(self, mapper, tomap, mapped):
        # start a thread
        Thread.__init__(self)
        # instance variables
        self.mapper = mapper
        self.tomap = tomap
        self.mapped = mapped


    def run(self):
        while True:
            # apply mapper and put results into the out queue
            self.mapped.put(self.mapper(self.tomap.get()))
            # signal completion
            self.tomap.task_done()


class Reducer(Thread):
    """
    Generic reducer thread
    """
    def __init__(self, reducer, mapped, factory=float):
        # start a thread
        Thread.__init__(self)
        # instance variables
        self.reducer = reducer
        self.mapped = mapped
        self.result = factory()


    def run(self):
        while True:
            # apply reducer
            self.result = self.reducer(self.result, self.mapped.get())
            # signal completion
            self.mapped.task_done()


class ThreadM(object):
    """
    Class representing a mapper thread pool. Standard usage looks like:

    >>> from operator import add
    >>> m = ThreadM(len)
    >>> for line in open('/usr/share/dict/words', 'r'):
    ...     m.put(line.rstrip())
    >>> m.join()
    >>> print reduce(add, m)
    839677

    The default value for n, the number of threads, assumes the mapping 
    function is CPU-bound. If it's IO-bound, feel free to set it much higher
    """

    def __init__(self, mapper, inputvals=None, n=None):
        # choose size of thread pool (= n)
        if n < 1: # which also means undefined
            n = _number_of_cpus * 2
        # make queues
        self.tomap  = Queue()
        self.mapped = Queue()
        # make mapping thread pool
        for i in xrange(n):
            m = Mapper(mapper, self.tomap, self.mapped)
            m.daemon = True
            m.start()
        # populate input queue if iterable is given
        if inputvals:
            for val in inputvals:
                self.put(val)


    def __iter__(self):
        """
        Returns mapped values. Most often used after calling the join() 
        instance method.
        """
        while self.mapped.qsize():
            yield self.mapped.get()
            self.mapped.task_done()


    def join(self):
        """
        Waits for mapping queue to complete. 
        """
        self.tomap.join()


    def put(self, val):
        """
        Adds a value to the mapping queue
        
        val: value to add to the queue
        """
        self.tomap.put(val)


class ThreadMR(object):
    """
    Class representing a mapper-reducer thread pool. Standard usage looks like:

    >>> from operator import add
    >>> mr = ThreadMR(len, add, factory=int)
    >>> for line in open('/usr/share/dict/words', 'r'):
    ...     mr.put(line.rstrip())
    >>> print mr.join()
    839677
    """

    def __init__(self, mapper, reducer, inputvals=None, n=None, factory=float):
        """ 
        Creates a threaded map-reducer    

        mapper: one-place (hopefully C-based) mapping function
        reducer: one-place (hopefully C-based) reducing function
        inputvals: optional iterable of keys to map
        n: optional number of cores
        """
        # choose size of thread pool (= n)
        if n < 1: # which also means undefined
            n = _number_of_cpus
        # make queues
        self.tomap  = Queue()
        self.mapped = Queue()
        # make mapping thread pool
        for i in xrange(n):
            m = Mapper(mapper, self.tomap, self.mapped)
            m.daemon = True
            m.start()
        # make a single reducing thread
        self.r = Reducer(reducer, self.mapped, factory)
        self.r.daemon = True
        self.r.start()
        # populate input queue if iterable is given
        if inputvals:
            for val in inputvals:
                self.put(val)


    # internals etc.

    def put(self, val):
        """
        Adds a value to the mapping queue
        
        val: value to add to the queue
        """
        self.tomap.put(val)

    
    def join(self):
        """
        Waits for mapping queue to complete. Waits for reducing queue to 
        finish. Optionally, returns result value
        """
        self.tomap.join()
        self.mapped.join()
        return self.r.result


if __name__ == '__main__':
    import doctest
    doctest.testmod()
