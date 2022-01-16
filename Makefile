# Makefile for devanagari-pdf-decoder
#
# Commonly used targets:
#
# make test
#    (it's a default target)
#    Run generally stable tests, optionally customized by setting FRAGMENTS, PAGES, LINES and VERBOSE
#    make PAGES='p113 uc-p002l'
#       only run tests for these pages
#    make FRAGMENTS=f003 VERBOSE=1
#       only test this fragment (see test/f*.txt), and print the fragment
#       before decoding
#    make PAGES='p113' LINES=3
#       only compare results for third line of corresponding test

# make sample/p006.qdf
#    Prepare the 'QDF' version of a given page for vi1000 (useful to see the
#    actual Tf and Tj commands along with font encoding details)

# make sample/uc-p006.qdf
#    Prepare the 'QDF' version of a given page for Upani.sat Candrikaa (

# make go-uc-p006
#    fix sample/uc-p006.qdf after editing, run standard PDF viewer on it. It is
#    useful to try and change given .qdf file to see what exactly changes in
#    actual on-screen output in PDF viewer.
#
#    Commonly used tricks (run go-.... after corresponding edits)
#       <0002>Tf => <00020202020202>Tf
#       duplicate some specific char (02) to see what it corresponds to.

.PHONY: FORCE

# we use bash for <(cmd) argument to diff
SHELL := bash
DEFAULT_FRAGMENTS := f001 \
	f002 \
	f003 \
	f004 \
	f005 \
	f006 \
	f007 \
	f008 \
	f009 \
	f010 \
	f011 \
	f012 \
	f013 \
	f014 \
	f015 \
	f016 \
	f017 \
	f018 \
	f019 \
	f020 \
	f021 \
	f022
DEFAULT_PAGES := p005 p113 p115 uc-p002
#LINES := 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33
VERBOSE := 0

ifndef PAGES
ifndef FRAGMENTS
PAGES := ${DEFAULT_PAGES}
FRAGMENTS := ${DEFAULT_FRAGMENTS}
endif
endif

test: $(patsubst %, sample/%.txt, ${PAGES}) FORCE
	@VERBOSE=${VERBOSE} test/test-line "${PAGES}" "${LINES}" "${FRAGMENTS}"

sample/%l.txt: sample/%.pdf
	WIDTH=$$(pdfinfo "$<" | awk 'match($$0, "Page size: *([0-9]+)[^0-9]+([0-9]+)", m) { print m[2] }'); \
	echo width: $$WIDTH; \
	HALFWIDTH=$$((WIDTH/2)); \
	pdftotext -layout -W $$HALFWIDTH -H 10000 "$<" "$@"

sample/%r.txt: sample/%.pdf
	WIDTH=$$(pdfinfo "$<" | awk 'match($$0, "Page size: *([0-9]+)[^0-9]+([0-9]+)", m) { print m[2] }'); \
	echo width: $$WIDTH; \
	HALFWIDTH=$$((WIDTH/2)); \
	pdftotext -layout -W $$HALFWIDTH -H 10000 -x $$HALFWIDTH "$<" "$@"

sample/%.txt: sample/%.pdf
	pdftotext -layout -nopgbrk "$<"

sample/%-split.txt: sample/%.pdf
	WIDTH=$$(pdfinfo "$<" | awk 'match($$0, "Page size: *([0-9]+)[^0-9]+([0-9]+)", m) { print m[2] }'); \
	echo width: $$WIDTH; \
	PAGES=$$(pdfinfo "$<" |awk '/Pages:/{print $$2}'); \
	echo pages: $$PAGES; \
	HALFWIDTH=$$((WIDTH/2)); \
	for ((i=1;i<=$$PAGES;i++)); do \
		pdftotext -f $$i -l $$i -layout -W $$HALFWIDTH -H 10000 "$<" -; \
		pdftotext -f $$i -l $$i -layout -W $$HALFWIDTH -H 10000 -x $$HALFWIDTH "$<" -; \
	done > "$@"

sample/%.qdf: sample/%.pdf
	qpdf --qdf "$<" "$@"

sample/p%.pdf: sample/vi1000\ -\ govindAcArya\ [san].pdf
	pdfseparate -f $(patsubst sample/p%.pdf,%,$@) -l $(patsubst sample/p%.pdf,%,$@) "$<" $@

sample/uc-p%.pdf: sample/UpanishathChandrikaPart1.pdf
	pdfseparate -f $(patsubst sample/uc-p%.pdf,%,$@) -l $(patsubst sample/uc-p%.pdf,%,$@) "$<" "$@"

go-%: sample/%.qdf
	fix-qdf "$<" > sample/tmp.pdf
	xdg-open sample/tmp.pdf

sample/uc-%-decoded.txt: sample/uc-%.txt
	src/decode-shree-devanagari.py -m "$<" > $@

sample/%-decoded.txt: sample/%.txt
	src/decode-shree-devanagari.py "$<" > $@

clean:
	rm -f sample/p[0-9][0-9][0-9].txt sample/p[0-9][0-9][0-9].pdf sample/*.qdf sample/tmp.pdf sample/vi*.txt sample/uc-p*.{pdf,txt} sample/Up*.txt

qdf: sample/vi1000\ -\ govindAcArya\ [san].qdf
