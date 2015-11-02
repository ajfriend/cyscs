.PHONY: clean reinstall test all sdist

all: reinstall test

clean:
	-pip uninstall scs
	$(RM) -rf *.egg-info scs/*.pyc *.pyc dist build scs/*.c scs/*.so scs/__pycache__ .cache/ test/__pycache__ __pycache__

reinstall: clean
	pip install -e .

# can run -vs, where s makes it not capture output
# the -l flag will print out a list of local variables with their corresponding values when a test fails
test:
	py.test test -vl

sdist: clean
	python setup.py sdist
	tar -zxvf dist/scs-1.1.8.tar.gz -C dist/