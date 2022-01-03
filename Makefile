.PHONY: FORCE

# we use bash for <(cmd) argument to diff
SHELL := bash

test: sample/p113.txt FORCE
	@test/test-line 1 p113
	@test/test-line 2 p113
	@test/test-line 3 p113
	@test/test-line 4 p113
	@test/test-line 5 p113
	@test/test-line 6 p113

sample/p113.txt: sample/p113.pdf
	pdftotext -layout -nopgbrk $<

all: p113-decoded.pdf p114-decoded.pdf

sample/p%-decoded.pdf: sample/p%.pdf
	qpdf --qdf "$<" "$@"

sample/p113.pdf: sample/vi1000\ -\ govindAcArya\ [san].pdf
	pdfseparate -f $(patsubst sample/p%.pdf,%,$@) -l $(patsubst sample/p%.pdf,%,$@) "$<" $@

p114.pdf: vi1000\ -\ govindAcArya\ [san].pdf
	pdfseparate -f $(patsubst sample/p%.pdf,%,$@) -l $(patsubst sample/p%.pdf,%,$@) "$<" $@

go: sample/p113-decoded.pdf
	fix-qdf sample/p113-decoded.pdf > sample/p113-decoded-.pdf
	xdg-open sample/p113-decoded-.pdf
