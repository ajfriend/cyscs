.PHONY: clean reinstall test all sdist

all: reinstall test

clean:
	-pip uninstall cyscs
	$(RM) -rf *.egg-info cyscs/*.pyc *.pyc dist build cyscs/*.c cyscs/*.so cyscs/__pycache__ .cache/ test/__pycache__ __pycache__ test/*.pyc test/__pycache__

reinstall: clean
	python setup.py install --cython

# can run -vs, where s makes it not capture output
# the -l flag will print out a list of local variables with their corresponding values when a test fails
test:
	py.test --pyargs cyscs -l

sdist:
	python setup.py sdist --cython
	# the line below unpacks the sdist (i was wanting to inspect it manually)
	#tar -zxvf dist/cyscs-*.tar.gz -C dist/

wheel:
	python setup.py bdist_wheel --cython
	# install in virtualenv with pip install dist/scs-1.1.8-....whl