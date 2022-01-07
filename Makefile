.PHONY: FORCE

# we use bash for <(cmd) argument to diff
SHELL := bash
TESTS := p113
#LINES := 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33
VERBOSE := 0

test: sample/p113.txt FORCE
	@VERBOSE=${VERBOSE} test/test-line "${TESTS}" "${LINES}"

sample/%.txt: sample/%.pdf
	pdftotext -layout -nopgbrk $<

all: p113-decoded.pdf p114-decoded.pdf

sample/p%-decoded.pdf: sample/p%.pdf
	qpdf --qdf "$<" "$@"

sample/p113.pdf: sample/vi1000\ -\ govindAcArya\ [san].pdf
	pdfseparate -f $(patsubst sample/p%.pdf,%,$@) -l $(patsubst sample/p%.pdf,%,$@) "$<" $@

sample/p114.pdf: sample/vi1000\ -\ govindAcArya\ [san].pdf
	pdfseparate -f $(patsubst sample/p%.pdf,%,$@) -l $(patsubst sample/p%.pdf,%,$@) "$<" $@

go: sample/p113-decoded.pdf
	fix-qdf sample/p113-decoded.pdf > sample/p113-decoded-.pdf
	xdg-open sample/p113-decoded-.pdf

clean:
	rm -f sample/p113.txt sample/p114.{txt,pdf} sample/p113-decoded{,-}.pdf
