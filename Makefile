.PHONY: FORCE

# we use bash for <(cmd) argument to diff
SHELL := bash
TESTS := p113 p115
#LINES := 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33
VERBOSE := 0

test: $(patsubst %, sample/%.txt, ${TESTS}) FORCE
	@VERBOSE=${VERBOSE} test/test-line "${TESTS}" "${LINES}"

sample/%.txt: sample/%.pdf
	pdftotext -layout -nopgbrk $<

all: p113-decoded.pdf p114-decoded.pdf

sample/p%-decoded.pdf: sample/p%.pdf
	qpdf --qdf "$<" "$@"

sample/p%.pdf: sample/vi1000\ -\ govindAcArya\ [san].pdf
	pdfseparate -f $(patsubst sample/p%.pdf,%,$@) -l $(patsubst sample/p%.pdf,%,$@) "$<" $@

go-%: sample/p%-decoded.pdf
	fix-qdf $< > sample/tmp.pdf
	xdg-open sample/tmp.pdf

clean:
	rm -f sample/p[0-9][0-9][0-9].txt sample/p11[6-9].pdf sample/p[0-9][0-9][0-9]-decoded.pdf sample/tmp.pdf
