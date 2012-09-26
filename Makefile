PREFIX=/usr/local
CFLAGS=-O2

TARGET=swc
WRAPPERS=$(TARGET)_wrap.c $(TARGET).py
PYLIBS=build/

all: $(TARGET) $(PYLIBS)
install: installc installpy

$(TARGET):
	$(CC) $(CFLAGS) -o $(TARGET) swc.c -lc -lm -lsndfile

$(WRAPPERS): 
	swig -python -threads $(TARGET).i

$(PYLIBS): $(WRAPPERS)
	python setup.py build

installc: $(TARGET)
	install $(TARGET) $(PREFIX)/bin

installpy: $(PYLIBS)
	python setup.py install

clean:
	$(RM) -r $(TARGET) $(WRAPPERS) $(PYLIBS)

test: $(TARGET)
	curl -O http://facstaff.bloomu.edu/jtomlins/Sounds/king.wav
	echo "Soxi output: `soxi -d king.wav`"
	echo "C output: `./swc king.wav`"
	rm king.wav
