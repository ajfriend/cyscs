.PHONY: clean reinstall test all

all: reinstall test

clean:
	-pip uninstall scs
	$(RM) -rf src/*.egg-info src/*.pyc *.pyc dist build src/*.c src/*.so

reinstall: clean
	pip install -e .

test:
	nosetests -vs
