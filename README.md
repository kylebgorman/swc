swc.py: Threaded .wav file length counter
========================================

This program is named after the venerable UNIX classic `wc`; "s" stands for 
either "sound" or "second", depending on which you prefer. Given a list of 
files, it computes the summed length (in hours, minutes, and seconds) of the 
files.

The code here is provided mostly as a demo (see LICENSE), though I use it in 
my own (acoustic phonetics) research.

How to install:
---------------

You will need SWIG and the libsndfile headers. Once you have them, issue:

    make; sudo make install
