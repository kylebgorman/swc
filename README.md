swc.py: Threaded .wav file length counter
========================================

This program is named after the venerable UNIX classic `wc`; "s" stands for either "sound" or "second", depending on which you prefer. Given a list of files, it computes the summed length (in hours, minutes, and seconds) of the files using Python's `wave` module, where length is the number of frames divided by the framerate. 

While this task is relatively simple (it could be done using `soxi -Td`), what is special about this is that I use Python threading to accomplish the task. The only part that is likely to release the GIL (and therefore get a benefit from threading) is when `wave.read` does IO, but my tests suggest it's a good deal faster than `soxi` in many cases. 

    $ grep -c  processor /proc/cpuinfo 
    4
    $ time soxi -Td ~/Data/English8k/*.wav
    16:09:16.36

    real    0m46.807s
    user    0m1.884s
    sys     0m3.092s
    $ time ./swc.py "~/Data/English8k/*.wav"
    16:09:16.36

    real    0m9.203s
    user    0m7.800s
    sys 0m4.752s

That said, it may simply be that `soxi` is not optimized for this task. And, it should be noted, `soxi` appears to be able to cache its results, whereas this program is not.

* Threading is implemented by making each task an instance of a `threading.Thread` subclass,
* A `Queue.Queue` is used to keep track of what needs to be done
* `multiprocessing.cpu_count` is used to determine the optimal number of threads

The code here is provided mostly as a demo (see code for license), though I use it in my own (acoustic phonetics) research.
