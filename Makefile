

all: build

build: setup
	@echo "Building [sic] scripts"
	make -C scripts
	@echo "Building third party bits"
	make -C third-party build


setup:
	@echo "Setting up the [sic] repo"
	git submodule init
	git submodule update


.PHONY: all clean build develop setup dep-check
