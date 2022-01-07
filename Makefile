.PHONY: FORCE

# we use bash for <(cmd) argument to diff
SHELL := bash
PAGES := p005 p113 p115
#LINES := 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33
FRAGMENTS := f001 f002
VERBOSE := 0

test: $(patsubst %, sample/%.txt, ${PAGES}) FORCE
	@VERBOSE=${VERBOSE} test/test-line "${PAGES}" "${LINES}" "${FRAGMENTS}"

sample/%.txt: sample/%.pdf
	pdftotext -layout -nopgbrk $<

sample/decoded-p%.pdf: sample/p%.pdf
	qpdf --qdf "$<" "$@"

sample/p%.pdf: sample/vi1000\ -\ govindAcArya\ [san].pdf
	pdfseparate -f $(patsubst sample/p%.pdf,%,$@) -l $(patsubst sample/p%.pdf,%,$@) "$<" $@

go-%: sample/decoded-p%.pdf
	fix-qdf $< > sample/tmp.pdf
	xdg-open sample/tmp.pdf

clean:
	rm -f sample/p[0-9][0-9][0-9].txt sample/p[0-9][0-9][0-9].pdf sample/decoded-p[0-9][0-9][0-9].pdf sample/tmp.pdf sample/vi*.txt
