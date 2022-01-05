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

# potential replacements (all codepoints extracted  from /ToUnicode objects in PDF files_:
chars = {
	'\u0020':			' ',		# space
	'\u0022':			'-a',		# " vertical bar completing most syllables
	'\u0023':			'.h',		# #
	'\u0024':			'|',		# $
	'\u0025':			'-.rr',		# %
	'\u0026':			'.a',		# &
	'\u0028':			'(',		# (
	'\u0029':			')',		# )
	'\u002a':			'*',		# *
	'\u002b':			'+',		# +
	'\u002c':			',',		# ,
	'\u002d':			'-',		# -
	'\u002e':			'.',		# .
	'\u0030':			'0',		# 0
	'\u0031':			'1',		# 1
	'\u0032':			'2',		# 2
	'\u0033':			'3',		# 3
	'\u0034':			'4',		# 4
	'\u0035':			'5',		# 5
	'\u0036':			'6',		# 6
	'\u0037':			'7',		# 7
	'\u0038':			'8',		# 8
	'\u0039':			'9',		# 9
	'\u003b':			';',		# ;
	'\u003c':			'i-',		# <
	'\u003e':			'',			# >	(spacing)
	'\u003f':			'?',		# ?
	'\u0040':			'ka',		# @
	'\u0041':			'kh-',		# A
	'\u0042':			'g-',		# B
	'\u0043':			'gh-',		# C
	'\u0044':			'"n',		# D
	'\u0045':			'c-',		# E
	'\u0046':			'cha',		# F
	'\u0047':			'j-',		# G
	'\u0049':			'~n-',		# I
	'\u004a':			'.ta',		# J
	'\u004b':			'.tha',		# K
	'\u004c':			'.da',		# L
	'\u004d':			'.dha',		# M
	'\u004e':			'.n-',		# N
	'\u004f':			't-',		# O
	'\u0050':			'th-',		# P
	'\u0051':			'da',		# Q
	'\u0052':			'dh-',		# R
	'\u0053':			'n-',		# S
	'\u0054':			'p-',		# T
	'\u0055':			'pha',		# U
	'\u0056':			'b-',		# V
	'\u0057':			'bh-',		# W
	'\u0058':			'm-',		# X
	'\u0059':			'y-',		# Y
	'\u005a':			'ra',		# Z
	'\u005b':			'la',		# [
	'\u005c':			'v-',		# \
	'\u005d':			'"s-',		# ]
	'\u005e':			'.s-',		# ^
	'\u005f':			's-',		# _
	'\u0060':			'ha',		# `
	'\u0061':			'.la',		# a
	'\u0062':			'k.s-',		# b
	'\u0063':			'j~n-',		# c
	'\u0064':			'"sra',		# d
	'\u0065':			'tr-',		# e
	'\u0066':			'tt-',		# f
	'\u0068':			'.r',		# h U+0069 6a 6c might be .rr .l .ll?
	'\u006c':			'-u',		# l what is different from  s?
	'\u006d':			'-uu',		# m what is different from t?
	'\u006e':			'-n',		# n	appears e.g. after '"' in pna
	'\u006f':			'-_',		# o virama.
	'\u0070':			'-aa',		# p
	'\u0071':			'i-',		# q
	'\u0072':			'-ii',		# r what is different from \u00ee?
	'\u0073':			'-u',		# s what is different from l?
	'\u0074':			'-uu',		# t what is different from m?
	'\u0075':			'-e',		# u becomes part of -o as 'pu'
	'\u0076':			'-ai',		# v becomes part of -au as 'pv'
	'\u0077':			'-.r',		# w
	'\u0078':			'-.rr',		# x ? (a guess; not seen yet)
	'\u0079':			'-.l',		# y ? (a guess; not seen yet)
	'\u007a':			'-.m',		# z
	'\u007b':			'r-',		# { hook above line. adds r to the beginning of syllable
	'\u007c':			'r-.m',		# | hook above + dot. adds r to the beginning and .m to the end
	'\u007d':			'-r',		# } line from center to left-bottom
	'\u007e':			'-r',		# ~ caret below character (used for -r in syllables not ending with bar)
	'\u00a0':			'pt-',		# NBSP
	'\u00a8':			'dbha',		# ¨
	'\u00a9':			'dda',		# ©
	'\u00ae':			'dba',		# ®
	'\u00b0':			'',			# ° (spacing e.g. after ka, ruu)
	'\u00b1':			'kla',		# ±
	'\u00b4':			'ddha',		# ´
	'\u00b5':			'"nkta',	# µ
	'\u00b7':			'ruu',		# ·
	'\u00bb':			'kka',		# »
	'\u00c1':			'dra',		# Á
	'\u00c2':			'hya',		# Â
	'\u00c4':			'~nj-',		# Ä
	'\u00c5':			'~nc-',		# Å
	'\u00c6':			'stra',		# Æ
	'\u00c7':			'cc-',		# Ç
	'\u00c8':			'.thya',	# È (.ttha? unlikely)
	'\u00c9':			'jj-',		# É
	'\u00cb':			'.tya',		# Ë
	'\u00cc':			'u',		# Ì ?
	'\u00cf':			'a',		# Ï
	'\u00d1':			'lla',		# Ñ
	'\u00d3':			'uu',		# Ó ?
	'\u00d4':			'e',		# Ô
	'\u00d5':			'.s.ta',	# Õ
	'\u00d6':			'hna',		# Ö
	'\u00da':			'i',		# Ú
	'\u00dc':			'h.na',		# Ü
	'\u00e0':			'hva',		# à
	'\u00e1':			'hla',		# á
	'\u00e3':			'"nkha',	# ã
	'\u00e4':			'"nka',		# ä
	'\u00e5':			'"nga',		# å
	'\u00e6':			'sra',		# æ
	'\u00e7':			'"ngha',	# ç
	'\u00e8':			'"nk.sa',	# è
	'\u00e9':			'"nma',		# é
	'\u00eb':			'-n',		# ë ?
	'\u00ec':			'i-',		# ì
	'\u00ed':			'[???]',	# í -n turned to up-right?
	'\u00ee':			'-ii',		# î what is different from 'r'?
	'\u00f1':			'\u2013',	# ñ –, en-dash
	'\u00f2':			'kta',		# ò
	'\u00f3':			'\u2014',	# ó —, em-dash
	'\u00f9':			'dya',		# ù
	'\u00fb':			'dga',		# û
	'\u00fc':			'dva',		# ü
	'\u00ff':			'ch-',		# ÿ
	'\u0152':			'.s.tha',	# Œ
	'\u0153':			'hm-',		# œ
	'\u02c6':			'-n',		# ˆ ?
	'\u02dc':			'-ya',		# ˜
	'\u2013':			'gn-',		# –
	'\u2014':			'tn-',		# —
	'\u201a':			'h.r',		# ‚
	'\u201c':			'kt-',		# “
	'\u201e':			'hra',		# „
	'\u2021':			'ru',		# ‡
	'\u2026':			'kva',		# …
	'\u2044':			'l-',		# ⁄
	'\u2122':			'd.r',		# ™ ?
	'\u2206':			'"sc-',		# ∆
	'\u221a':			'sna',		# √
	'\u221e':			'dbra',		# ∞ ?
	'\u2260':			'dma',		# ≠
	'\u2264':			'"nkra',	# ≤
	'\u2265':			'"ngra',	# ≥
	'\u25ca':			'k-',		# ◊
	'\ufb02':			'nn-',		# ﬂ
}

repl = {
	'@w':				'k.r',
	'@z':				'ka.m',
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
repl['\u00b7'] = 'ruu'
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
repl['\u00b0'] = '' # spacing after e.g. 'ka'

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
		if line[0:1] == '<' or line[0:1] == 'q' or line[0:1] == '\u00ec':
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
