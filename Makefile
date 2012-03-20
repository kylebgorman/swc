TARGET=swc
PREFIX=/usr/local
CFLAGS=-s -O3

all: c py 
install: installc installpy

c: 
	$(CC) $(CFLAGS) -o $(TARGET) swc.c -lc -lm -lsndfile

py:
	swig -threads -python swc.i
	python setup.py build
	echo \#\!/usr/bin/env python > TEMP
	cat swc.py >> TEMP
	mv TEMP swc.py
	chmod +x swc.py

installc: $(TARGET)
	install $(TARGET) $(PREFIX)/bin

installpy: $(TARGET)
	python setup.py install
	install swc.py threadanything.py $(PREFIX)/bin

clean:
	python setup.py clean
	rm -rf build/ $(TARGET) swc.py *.pyc *_wrap.c

test: $(TARGET)
	curl -O http://facstaff.bloomu.edu/jtomlins/Sounds/king.wav
	echo "Soxi output: `soxi -d king.wav`"
	echo "C output: `./swc king.wav`"
	echo "Python output: `python swc.py king.wav`"
	rm king.wav
