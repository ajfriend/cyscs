.PHONY: clean reinstall test all

all: reinstall test

clean:
	-pip uninstall scs
	$(RM) -rf *.egg-info scs/*.pyc *.pyc dist build scs/*.c scs/*.so scs/__pycache__ .cache/ test/__pycache__

reinstall: clean
	pip install -e .

# can run -vs, where s makes it not capture output
test:
	py.test test -vs
