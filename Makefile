.PHONY: clean reinstall test all

all: reinstall test

clean:
	-pip uninstall scs
	$(RM) -rf *.so *.egg-info *.pyc cython/scs.c dist build *.c

reinstall: clean
	pip install -e .

test:
	nosetests -vs
