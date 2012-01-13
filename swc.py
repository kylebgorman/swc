#!/usr/bin/env python
# Copyright (c) 2012 Kyle Gorman 
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
# swc.py: count hours, seconds, minutes of wave files
# Kyle Gorman <kylebgorman@gmail.com>

import wave

from sys import argv
from glob import iglob
from Queue import Queue
from math import fsum, fmod
from threading import Thread
from multiprocessing import cpu_count
from os.path import expanduser, expandvars


class SoxiThread(Thread):
    """
    Class where each instance is a call to soxi -d
    """

    def __init__(self, paths, results):
        # start a thread
        Thread.__init__(self)
        # the paths
        self.paths = paths
        # the place to put the results
        self.results = results


    def run(self):
        while True:
            ## GIL released -- I think
            w = wave.open(self.paths.get(), 'r')
            ## GIL acquired -- I think
            # compute length
            self.results.append(w.getnframes() / float(w.getframerate()))
            # signal completion
            self.paths.task_done()


if __name__ == '__main__':

    # usage check
    if len(argv) < 2: 
        exit('Error.\nUSAGE: ./swc.py FILE1 [FILE2 ...]')

    # create queue and length list
    paths = Queue()
    results = []

    # create pool of threads
    for i in xrange(cpu_count()):
        t = SoxiThread(paths, results)
        t.setDaemon(True)
        t.start()

    # populate queue
    for arg in argv[1:]:
        for path in iglob(expanduser(expandvars(arg))):
            paths.put(path)

    # wait until processing is done
    paths.join()

    # sum up (not using datetime, which is the worst module ever)
    seconds = fsum(results)
    hours = int(seconds // 3600)
    seconds = fmod(seconds, 3600.)
    minutes = int(seconds // 60)
    seconds = fmod(seconds, 60.)
    print '{0}:{1:02}:{2:02.04}'.format(hours, minutes, seconds)
