#!/bin/env python3
import argparse

def add_unchanging_letters(dic):
	letters_as_they_are = "0123456789()- .\n\f"
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

def add_long_a_rules(dic):
	new = {}
	for f, t in dic.items():
		if len(t) > 1 and t.endswith('a') and not t.endswith('aa'):
			new_from = f + 'p'
			new_to = t + 'a'
			new[new_from] = new_to
	return {**new, **dic}

def add_long_u_rules(dic):
	new = {}
	for f, t in dic.items():
		if len(t) > 1 and t.endswith('a') and not t.endswith('aa'):
			new_from = f + 't'
			new_to = t[:-1] + 'uu'
			new[new_from] = new_to
	return {**new, **dic}

def add_u_rules(dic):
	new = {}
	for f, t in dic.items():
		if len(t) > 1 and t.endswith('a') and not t.endswith('aa'):
			new_from = f + 's'
			new_to = t[:-1] + 'u'
			new[new_from] = new_to
	return {**new, **dic}

def add_i_rules(dic):
	new = {}
	for f, t in dic.items():
		if len(t) > 1 and t.endswith("a") and not t.endswith('aa'):
			new_from = '<' + f
			new_to = t[:-1] + 'i'
			new[new_from] = new_to
	return {**new, **dic}

def add_long_i_rules(dic):
	new = {}
	for f, t in dic.items():
		if len(t) > 1 and t.endswith("a") and not t.endswith('aa'):
			new_from = f + 'r'
			new_to = t[:-1] + 'ii'
			new[new_from] = new_to
	return {**new, **dic}

def add_o_rules(dic):
	new = {}
	for f, t in dic.items():
		if len(t) > 1 and t.endswith("a") and not t.endswith('aa'):
			new_from = f + 'pu'
			new_to = t[:-1] + 'o'
			new[new_from] = new_to
	return {**new, **dic}

def add_e_rules(dic):
	new = {}
	for f, t in dic.items():
		if len(t) > 1 and t.endswith("a") and not t.endswith('aa'):
			new_from = f + 'u'
			new_to = t[:-1] + 'e'
			new[new_from] = new_to
	return {**new, **dic}

def add_ai_rules(dic):
	new = {}
	for f, t in dic.items():
		if len(t) > 1 and t.endswith("a") and not t.endswith('aa'):
			new_from = f + 'v'
			new_to = t[:-1] + 'ai'
			new[new_from] = new_to
	return {**new, **dic}

def add_r_before_rules(dic):
	new = {}
	for f, t in dic.items():
		if len(t) > 1 and t[-1:] in "aiuoe":
			new_from = f + '{'
			new_to = 'r' + t
			new[new_from] = new_to
	return {**new, **dic}

def decodeline(line):
	repl = {
		'$':		'|',
		'B"':		'ga',
		'd':		'"sra',
		'e"':		'tra',
		'ﬂ"':		'nna',
		'#':		'.h',
		'Ï':		'a',
		'Ú':		'i',
		'ñ':		'—',
		'}œ"':		'hma',
		'◊O"':		'kta',
		'_O"':		'sta',
		'O"':		'ta',
		'<O"':		'ti',
		'O_"':		'tsa',
		'O\\"':		'tva',
		'Q':		'da',
		'_"':		'sa',
		'S"':		'na',
		'\\"':		'va',
		'V"':		'bra',
		'<\\"':		'vi',
		'W"':		'bha',
		'<W"':		'bhi',
		'OX"':		'tma',
		'X"':		'ma',
		'\\Y"':		'vya',
		'Y\\"':		'yva',
		'_OY"':		'stya',
		'SY"':		'nya',
		'Y"':		'ya',
		'Z':		'ra',
		'@°':		'ka',
		']"':		'"sa',
		'[':		'la',
		'c"':		'j~na',
		'T"':		'pa',
		'^"':		'.sa',
		'ù':		'dya',
		'b"':		'k.sa',
		'z':		'.m',
		'Õ>':		'.s.ta',
		'N"':		'.na',
		'Ç"':		'cca',
		'G"':		'ja',
		'qwe':		'qwe'
	}
	repl = add_unchanging_letters(repl)
	repl = add_virama_rules(repl)
	repl = add_long_a_rules(repl)
	repl = add_u_rules(repl)
	repl = add_long_u_rules(repl)
	repl = add_o_rules(repl)
	repl = add_i_rules(repl)
	repl = add_long_i_rules(repl)
	repl = add_e_rules(repl)
	repl = add_ai_rules(repl)
	repl = add_r_before_rules(repl)

	# avoid replicating these special rules to "aa", "ii", halant etc
	repl['&'] = '.a'
	repl['·°'] = 'ruu'

	res = ''


	class ContinueLine(Exception):
		pass

	while len(line) != 0:
		try:
			for repl_from, repl_to in repl.items():
				if line.startswith(repl_from):
					res += repl_to
					line = line[len(repl_from):]
					raise ContinueLine
			# could not find any known prefix, escape next char
			res += "[" + line[0] + "]"
			line = line[1:]
		except ContinueLine:
			continue
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

	main(args);

	#main(args)
