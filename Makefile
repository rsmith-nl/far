# file: Makefile
# vim:fileencoding=utf-8:fdm=marker:ft=make
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-03-03 21:56:24 +0100
# Last modified: 2018-03-04 00:06:53 +0100
.PHONY: try help

help::
	@echo "Available commands:"
	@echo "  make run -- lauch find and replace."
	@echo "  make test -- create test tree."
	@echo "  make clean -- remove test tree."

run::
	python3 far.py


test::
	mkdir -p test/gnarf test/bar test/baz
	for f in a.txt b.dat c.bin d.foo foo.txt; \
	do \
		touch test/gnarf/$$f test/bar/$$f test/baz/$$f ; \
	done

clean::
	rm -rf test
