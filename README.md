swc.py: Threaded .wav file length counter
========================================

This program is named after the venerable UNIX classic `wc`; "s" stands for either "sound" or "second", depending on which you prefer. Given a list of files, it computes the summed length (in hours, minutes, and seconds) of the files.

The code here is provided mostly as a demo of linking C and Python with sWIG, though I use it in my own (acoustic phonetics) research.

A pecularity of the binary `swc` is that it uses glob internally. So if the following happens:

    $ swc wav/*.wav 
    -bash: /usr/local/bin/swc: Argument list too long

This will work:

    $ swc 'wav/*.wav'
    FILL ME IN

This surely has some bad consequences, but not ones that come up normally.

How to install:
---------------

You will need SWIG and the libsndfile headers. Once you have them, issue:

    make; sudo make install
