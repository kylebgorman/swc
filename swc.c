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
 * swc.c: C functions
 * Kyle Gorman
 */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#include <sndfile.h> // http://www.mega-nerd.com/libsndfile

// Get sound file length in seconds
float sndfile_length(char path[]) {
    // open
    SF_INFO info;
    SNDFILE* source = sf_open(path, SFM_READ, &info);
    // quick check for validity
    if (source == NULL || info.sections < 1) return -1.;
    // compute
    float seconds = info.frames / (float) info.samplerate;
    // close
    sf_close(source);
    // return
    return seconds;
}

// Main method
int main(int argc, char* argv[]) {
    char usage[] = "USAGE: swc FILE1 [FILE2...]\n";

    // check for ags
    if (argc < 2) {
        fprintf(stderr, usage);
        exit(EXIT_FAILURE);
    }

    // compute
    int i = 1;
    float seconds = 0.;
    for (/* i = 1 */; i < argc; i++) {
        float val = sndfile_length(argv[i]);
        if (val == -1.) {
            fprintf(stderr, "Error reading file %s\n", argv[i]);
            exit(EXIT_FAILURE);
        }
        seconds += val;
    }

    // print
    int hours = (int) (seconds / 3600.);
    seconds = fmod(seconds, 3600.);
    int minutes = (int) (seconds / 60.);
    seconds = fmod(seconds, 60.);
    printf("%d:%02d:%02.02f\n", hours, minutes, seconds);

    // leave
    exit(EXIT_SUCCESS);
}
