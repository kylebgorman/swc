/* Copyright (c) 2012 Kyle Gorman
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to 
 * deal in the Software without restriction, including without limitation the 
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
 *
 * swc.i: SWIG file for Python module
 * Kyle Gorman
 */

%module swc %{
#define SWIG_FILE_WITH_INIT
#include "swc.h"
%}

float sndfile_length(char[]);

%pythoncode %{

def SWC(path):
    # get Python path
    f = path if isinstance(path, str) else path.name
    val = sndfile_length(f)
    if val == -1: raise ValueError('Error reading file {0}\n'.format(f))
    return val

if __name__ == '__main__':

    from sys import argv
    from math import fmod
    from glob import iglob
    from operator import add

    from threadanything import ThreadM

    # check usage
    if len(argv) < 2:
        exit('USAGE: ./swc.py FILE1 [FILE2 ...]')
    
    # make mapper
    m = ThreadM(SWC)

    # load it up
    for arg in argv[1:]:
        for path in iglob(arg):
            m.put(path)

    # sum up (but not using datetime, which is totally terrible)
    m.join()
    seconds = reduce(add, m)
    hours = int(seconds // 3600)
    seconds = fmod(seconds, 3600.)
    minutes = int(seconds // 60)
    seconds = fmod(seconds, 60.)
    print '{0}:{1:02}:{2:02.04}'.format(hours, minutes, seconds)
%}
