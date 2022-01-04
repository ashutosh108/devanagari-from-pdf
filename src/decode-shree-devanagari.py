#!/bin/env python3
import argparse

def add_unchanging_letters(dic):
	letters_as_they_are = "0123456789()- .,\n\f"
	new = {}
	for c in letters_as_they_are:
		new[c] = c
	return {**new, **dic}

def add_virama_rules(dic):
	new = {}
	for f, t in dic.items():
		if len(t) > 1 and t.endswith('a') and not t.endswith('aa'):
			new_from = f + 'o'
			new_to = t[:-1]
			new[new_from] = new_to
	return {**new, **dic}

repl = {
	'@w\u00b0':			'k.r',
	'@z\u00b0':			'ka.m',
	'@\u00b0':			'ka',
	'A"':				'kha',
	'B"':				'ga',
	'E"':				'ca',
	'G"':				'ja',
	'M':				'.dha', # always 'M>' but '>' is just spacing
	'N"':				'.na',
	'O"':				'ta',
	'P"':				'tha',
	'Q':				'da',
	'R"':				'dha',
	'S"':				'na',
	'T"n':				'pna',
	'T"':				'pa',
	'V"':				'ba',
	'W"':				'bha',
	'X"':				'ma',
	'Y"':				'ya',
	'Z':				'ra',
	'[':				'la',
	'\\"':				'va',
	']"':				'"sa',
	'^"':				'.sa',
	'_"':				'sa',
	'`':				'ha',
	'b"':				'k.sa',
	'c"':				'j~na',
	'd':				'"sra',
	'e"':				'tra',
	'z':				'.m',
	'\u00a0"':			'pta',
	'\u00b4':			'ddha',
	'\u00c2':			'hya',
	'\u00c5"':			'~nca',
	'\u00c7"':			'cca',
	'\u00c9"':			'jja',
	'\u00d5':			'.s.ta',
	'\u00e4':			'"nka',
	'\u00e6':			'sra',
	'\u00f2z\u00b0':	'kta.m',
	'\u00f9':			'dya',
	'\u00fc':			'dva',
	'\u0153"':			'hma',
	'\u2014"':			'tna',
	'\u201a':			'h.r',
	'\u2206"':			'"sca',
	'\ufb02"':			'nna',
}
repl = add_virama_rules(repl)
repl = add_unchanging_letters(repl)

# avoid replicating these special rules to "aa", "ii", halant etc
repl['#'] = '.h'
repl['$'] = '|'
repl['&'] = '.a'
repl['\u00b7\u00b0'] = 'ruu'
repl['\u00cc'] = 'u';
repl['\u00cfp'] = 'aa'
repl['\u00cf'] = 'a'
repl['\u00d4'] = 'e'
repl['\u00da{'] = 'ii'
repl['\u00da'] = 'i'
repl['\u00eb'] = '\u2018' # U+2018 left single quotation mark
repl['\u00ed'] = '\u2019' # U+2019 right single quotation mark
repl['\u00f1'] = '—'
repl['\u2021'] = 'ru'

# letters modifying the following syllable
repl_prefix = {
	'\u25ca':	'k',
}
for k, v in repl.items():
	if len(k)==2 and k[1] == '"':
		if not (len(v) > 1 and v[-1] == 'a'):
			raise Exception("wrong replacement pair found: '%s' => '%s' pattern ends on '\"', but replacement doesn't end on 'a'" % (k, v))
		repl_prefix[k[0]] = v[:-1]

# trailing vowels lookup. Must be longest-first among matching prefixes since
# first match wins and we want the longest one among the two entries to win.
# e.g. 'pv' must go before 'p'.

repl_trailing = {
	'l':	'u',
	'pu':	'o',
	'pv':	'au',
	'p':	'aa',
	'r':	'ii',
	's':	'u',
	't':	'uu',
	'u':	'e',
	'v':	'ai',
	'w':	'.r',
}

# optimization: group all entries by first char of it's key to make linear
# search shorter.
repl_for_letter = {}
for k, v in repl.items():
	if k[0] in repl_for_letter:
		repl_for_letter[k[0]][k] = v
	else:
		repl_for_letter[k[0]] = {k: v}

def handle_i_modifier(i_modifier, repl_to):
	if i_modifier:
		if repl_to.endswith('a') and len(repl_to) > 1 and repl_to[-2] in "tdhmknyvpljbcsr":
			repl_to = repl_to[:-1] + 'i'
		else:
			raise Exception("i modifier before unsupported replacement: '%s' => '%s'" % (repl_from, repl_to))
	i_modifier = False
	return i_modifier, repl_to

def add_before_last_vowel(what, syllable):
	vowels=''
	while syllable[-1:] in "aeiou":
		vowels += syllable[-1:]
		syllable = syllable[:-1]
	return syllable + what + vowels

def handle_trailing_vowels_and_r(line, repl_to):
	while True:
		got3 = line[0:3] in repl_trailing
		got2 = line[0:2] in repl_trailing
		if got3 or got2 or line[0:1] in repl_trailing:
			from_trailing = line[0:3] if got3 else line[0:2] if got2 else line[0:1]
			if not repl_to[-1] in "ai":
				repl_to = "[WARNING: '%s' modifier after a syllable ending not on 'a': %s]" % (from_trailing, repl_to) + repl_to
			repl_to = repl_to[:-1] + repl_trailing[from_trailing]
			# special case: add 'r' *before* the syllable
			if from_trailing[-1] == '{':
				repl_to = 'r' + repl_to
			line = line[len(from_trailing):]
		# add frontal "r" as in rvi, rva
		elif line[0:1] == '{':
			repl_to = 'r' + repl_to
			line = line[1:]
		# add trailing "r" as in grii, gra
		elif line[0:1] == '}':
			repl_to = add_before_last_vowel('r', repl_to)
			line = line[1:]
		# r-...-.m as combined as a single char
		elif line[0:1] == '|':
			repl_to = 'r' + repl_to + '.m'
			line = line[1:]
		# used as spacing after e.g. .s.t or .dha
		elif line[0:1] == '>':
			line = line[1:]
		else:
			break
	return line, repl_to

def decodeline(line):
	res = ''
	# collect additional parts of final syllable until we see syllable completion
	add_consonants_before_syllable = ''
	# since -i is written before the syllable, flag it as necessary
	i_modifier = False

	while line:
		continue2 = False
		if line[0] in repl_for_letter:
			for repl_from, repl_to in repl_for_letter[line[0]].items():
				if line.startswith(repl_from):
					line = line[len(repl_from):]
					i_modifier, repl_to = handle_i_modifier(i_modifier, repl_to)
					line, repl_to = handle_trailing_vowels_and_r(line, repl_to)
					res += add_consonants_before_syllable + repl_to
					add_consonants_before_syllable = ''
					continue2 = True
					break
		if continue2:
			continue
		if line[0:1] in repl_prefix:
			add_consonants_before_syllable += repl_prefix[line[0]]
			line = line[1:]
			continue
		if line[0:1] == '<' or line[0:1] == 'q' or line[0:1] == 'ì':
			i_modifier = True
			line = line[1:]
			continue
		# could not find any known prefix, escape next char
		res += "[" + line[0] + "]"
		line = line[1:]
	return res

def main(args):
	for line in args.infile:
		print(decodeline(line), end='')

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description=
			'Decode Devanagari text after pdftotext (from poppler-utils)')
	parser.add_argument(
		"infile",
		type=argparse.FileType('r'),
		help="source .txt output from pdftotext")
	args = parser.parse_args()

	main(args)
