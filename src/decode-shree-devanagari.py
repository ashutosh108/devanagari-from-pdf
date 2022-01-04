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
	'@z°':		'ka.m',
	'@°':		'ka',
	'@w°':		'k.r',
	'A"':		'kha',
	'òz°':		'kta.m',
	'B"':		'ga',
	'E"':		'ca',
	'G"':		'ja',
	'N"':		'.na',
	'd':		'"sra',
	'e"':		'tra',
	'ﬂ"':		'nna',
	'œ"':		'hma',
	'Â':		'hya',
	'O"':		'ta',
	'P"':		'tha',
	'Q':		'da',
	'´':		'ddha',
	'ü':		'dva',
	'_"':		'sa',
	'—"':		'tna',
	'S"':		'na',
	'\\"':		'va',
	'V"':		'ba',
	'W"':		'bha',
	'X"':		'ma',
	'Y"':		'ya',
	'Z':		'ra',
	']"':		'"sa',
	'[':		'la',
	'c"':		'j~na',
	'T"n':		'pna',
	'T"':		'pa',
	'^"':		'.sa',
	'ù':		'dya',
	'b"':		'k.sa',
	'z':		'.m',
	'Õ>':		'.s.ta',
	'Ç"':		'cca',
	'∆"':		'"sca',
	'R"':		'dha',
	'ä':		'"nka',
	'Å"':		'~nca',
	'`':		'ha',
	'qwe':		'qwe'
}
repl = add_virama_rules(repl)
repl = add_unchanging_letters(repl)

# avoid replicating these special rules to "aa", "ii", halant etc
repl['&'] = '.a'
repl['·°'] = 'ruu'
repl['‡'] = 'ru'
repl['ë'] = '‘'; # U+2018 left single quotation mark
repl['í'] = '’'; # U+2019 right single quotation mark
repl['Ïp'] = 'aa';
repl['Ï'] = 'a';
repl['Ô'] = 'e';
repl['$'] = '|';
repl['#'] = '.h';
repl['Ú{'] = 'ii';
repl['Ú'] = 'i';
repl['ñ'] = '—';

# letters modifying the following syllable
repl_prefix = {
	'O':	't',
	']':	'"s',
	'_':	's',
	'S':	'n',
	'X':	'm',
	'\\':	'v',
	'Y':	'y',
	'E':	'c',
	'◊':	'k'
}

# trailing letters lookup. Must be longest-first among matching prefixes since
# first match wins and we want the longest one among the two entries to win.
# Almost every entry is duplicated with it's "prefix r" version. Later We test
# if the last symbol of the key is '{' to add 'r' in front of syllable.
#
# '{' (r-before-syllable) is a special case because it doesn't need
# corresponding "short a" entry
#
# '}' means *trailing* r

repl_trailing = {
	'pu{':	'o',
	'pu':	'o',
	'pv{':	'au',
	'pv':	'au',
	'p{':	'aa',
	'p':	'aa',
	'v{':	'ai',
	'v':	'ai',
	'r{':	'ii',
	'r':	'ii',
	's{':	'u',
	's':	'u',
	'l':	'u',
	't{':	'uu',
	't':	'uu',
	'u{':	'e',
	'u':	'e',
	'{':	'a',
	'}r':	'rii',
	'}':	'ra',
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

def handle_trailing_vowels_and_r(line, repl_to):
	got3 = line[0:3] in repl_trailing
	got2 = line[0:2] in repl_trailing
	if got3 or got2 or line[0:1] in repl_trailing:
		from_trailing = line[0:3] if got3 else line[0:2] if got2 else line[0:1]
		if repl_to.endswith('a'):
			repl_to = repl_to[:-1] + repl_trailing[from_trailing]
			# special case: add 'r' *before* the syllable
			if from_trailing[-1] == '{':
				repl_to = 'r' + repl_to
			line = line[len(from_trailing):]
		else:
			raise Exception("'%s' modifier after a syllable ending not on 'a': %s" % (from_trailing, repl_to))
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
		if line[0] in repl_prefix:
			add_consonants_before_syllable += repl_prefix[line[0]]
			line = line[1:]
			continue
		if line[0] == '<' or line[0] == 'q':
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
