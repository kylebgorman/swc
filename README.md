swc.py: Threaded .wav file length counter
========================================

This program is named after the venerable UNIX classic `wc`; "s" stands for either "sound" or "second", depending on which you prefer. Given a list of files, it computes the summed length (in hours, minutes, and seconds) of the files using Python's `wave` module, where length is the number of frames divided by the framerate. 

While this task is relatively simple (it could be done using `soxi`, what is special about this is that I use Python threading to accomplish the task. The only part that is likely to release the GIL (and therefore get a benefit from threading) is when `wave.read` does IO, but overall it certainly feels fast. A few interesting features:

* Threading is implemented by making each task an instance of a `threading.Thread` subclass,
* A `Queue.Queue` is used to keep track of what needs to be done
* `multiprocessing.cpu_count` is used to determine the optimal number of threads

The code here is provided mostly as a demo (see code for license), though I use it in my own (acoustic phonetics) research.
