.PHONY: FORCE

# we use bash for <(cmd) argument to diff
SHELL := bash
TESTS := 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24

test: sample/p113.txt FORCE
	@test/test-line p113 ${TESTS}

sample/p113.txt: sample/p113.pdf
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
