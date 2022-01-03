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

def add_au_rules(dic):
	new = {}
	for f, t in dic.items():
		if len(t) > 1 and t.endswith("a") and not t.endswith('aa'):
			new_from = f + 'pv'
			new_to = t[:-1] + 'au'
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

def add_t_before_rules(dic):
	new = {}
	for f, t in dic.items():
		if t[-1] in "aieou":
			new_from = 'O' + f
			new_to = 't' + t
			new[new_from] = new_to
	return {**new, **dic}

def add_ssh_before_rules(dic):
	new = {}
	for f, t in dic.items():
		if t[-1] in "aieou":
			new_from = ']' + f
			new_to = '"s' + t
			new[new_from] = new_to
	return {**new, **dic}

def add_s_before_rules(dic):
	new = {}
	for f, t in dic.items():
		if t[-1] in "aieou":
			new_from = '_' + f
			new_to = 's' + t
			new[new_from] = new_to
	return {**new, **dic}

repl = {
	'@°':		'ka',
	'B"':		'ga',
	'E"':		'ca',
	'G"':		'ja',
	'N"':		'.na',
	'd':		'"sra',
	'e"':		'tra',
	'ﬂ"':		'nna',
	'}œ"':		'hma',
	'◊O"':		'kta',
	'_O"':		'sta',
	'SO"':		'nta',
	'O"':		'ta',
	'P"':		'tha',
	'SQ':		'nda',
	'Q':		'da',
	'_"':		'sa',
	'—"':		'tna',
	'S"':		'na',
	'_\\"':		'sva',
	'\\"':		'va',
	'V"':		'bra',
	'W"':		'bha',
	'X"':		'ma',
	'\\Y"':		'vya',
	'Y\\"':		'yva',
	'_OY"':		'stya',
	'SY"':		'nya',
	'_Y"':		'sya',
	'Y"':		'ya',
	'Z':		'ra',
	']"':		'"sa',
	'[':		'la',
	'c"':		'j~na',
	'T"}':		'pra',
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
	'qwe':		'qwe'
}
repl = add_virama_rules(repl)
repl = add_long_a_rules(repl)
repl = add_u_rules(repl)
repl = add_long_u_rules(repl)
repl = add_o_rules(repl)
repl = add_au_rules(repl)
repl = add_i_rules(repl)
repl = add_long_i_rules(repl)
repl = add_e_rules(repl)
repl = add_ai_rules(repl)
repl = add_t_before_rules(repl)
repl = add_r_before_rules(repl)
repl = add_ssh_before_rules(repl)
repl = add_s_before_rules(repl)
repl = add_unchanging_letters(repl)

# avoid replicating these special rules to "aa", "ii", halant etc
repl['&'] = '.a'
repl['·°'] = 'ruu'
repl['ë'] = '‘'; # U+2018 left single quotation mark
repl['í'] = '’'; # U+2019 right single quotation mark
repl['Ïp'] = 'aa';
repl['Ï'] = 'a';
repl['$'] = '|';
repl['#'] = '.h';
repl['Ú'] = 'i';
repl['ñ'] = '—';

repl_for_letter = {}

for k, v in repl.items():
	if k[0] in repl_for_letter:
		repl_for_letter[k[0]][k] = v
	else:
		repl_for_letter[k[0]] = {k: v}

def decodeline(line):
	res = ''

	while line:
		continue2 = False
		if line[0] in repl_for_letter:
			for repl_from, repl_to in repl_for_letter[line[0]].items():
				if line.startswith(repl_from):
					res += repl_to
					line = line[len(repl_from):]
					continue2 = True
					break
		if continue2:
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

	main(args);

	#main(args)
