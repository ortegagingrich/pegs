ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

SRC_FOLDER=$(ROOT_DIR)/src


.phony: install
install:
	python setup.py install


.phony: uninstall
uninstall:
	python setup.py uninstall


.phony: clobber
clobber:
	find . -name "*.pyc" -exec rm -rf {} \;

.phony: run
run:
	python $(SRC_FOLDER)/main.py

.phony: line_count
line_count:
	find . -name '*.py' -or -wholename '*/bin/*' | xargs wc -l
