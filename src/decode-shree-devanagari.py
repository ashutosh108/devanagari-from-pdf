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

class Literal:
	def __init__(self, str):
		self.str = str

class Syllable(Literal):
	pass

class RightVowel(Literal):
	pass

class RightCons(Literal):
	pass

class RightTail(Literal):
	pass

class RightFrontalR(Literal):
	pass

class RightFrontalRAndTailM(Literal):
	pass

class LeftVowel(Literal):
	pass

class Space(Literal):
	pass

class LeftCons(Literal):
	pass

class Vowel(Literal):
	pass

class Virama(Literal):
	pass

a = Literal('a')
b = Syllable('sa')

# potential replacements (all codepoints extracted  from /ToUnicode objects in PDF files_:
chars = {
	'\u000a':			Literal('\n'),			# newline
	'\u000c':			Literal('\f'),			# formfeed (new page)
	'\u0020':			Literal(' '),			# space
	'\u0022':			RightVowel('a'),		# " vertical bar completing most syllables
	'\u0023':			Syllable('.h'),			# #
	'\u0024':			Literal('|'),			# $
	'\u0025':			RightVowel('.rr'),		# %
	'\u0026':			Literal('.a'),			# &
	'\u0028':			Literal('('),			# (
	'\u0029':			Literal(')'),			# )
	'\u002a':			Literal('*'),			# *
	'\u002b':			Literal('+'),			# +
	'\u002c':			Literal(','),			# ,
	'\u002d':			Literal('-'),			# -
	'\u002e':			Literal('.'),			# .
	'\u0030':			Literal('0'),			# 0
	'\u0031':			Literal('1'),			# 1
	'\u0032':			Literal('2'),			# 2
	'\u0033':			Literal('3'),			# 3
	'\u0034':			Literal('4'),			# 4
	'\u0035':			Literal('5'),			# 5
	'\u0036':			Literal('6'),			# 6
	'\u0037':			Literal('7'),			# 7
	'\u0038':			Literal('8'),			# 8
	'\u0039':			Literal('9'),			# 9
	'\u003b':			Literal(';'),			# ;
	'\u003c':			LeftVowel('i'),			# <
	'\u003e':			Space(''),				# >	(spacing)
	'\u003f':			Literal('?'),			# ?
	'\u0040':			Syllable('ka'),			# @
	'\u0041':			LeftCons('kh'),			# A
	'\u0042':			LeftCons('g'),			# B
	'\u0043':			LeftCons('gh'),			# C
	'\u0044':			Syllable('"n'),			# D
	'\u0045':			LeftCons('c'),			# E
	'\u0046':			Syllable('cha'),		# F
	'\u0047':			LeftCons('j'),			# G
	'\u0049':			LeftCons('~n'),			# I
	'\u004a':			Syllable('.ta'),		# J
	'\u004b':			Syllable('.tha'),		# K
	'\u004c':			Syllable('.da'),		# L
	'\u004d':			Syllable('.dha'),		# M
	'\u004e':			LeftCons('.n'),			# N
	'\u004f':			LeftCons('t'),			# O
	'\u0050':			LeftCons('th'),			# P
	'\u0051':			Syllable('da'),			# Q
	'\u0052':			LeftCons('dh'),			# R
	'\u0053':			LeftCons('n'),			# S
	'\u0054':			LeftCons('p'),			# T
	'\u0055':			Syllable('pha'),		# U
	'\u0056':			LeftCons('b'),			# V
	'\u0057':			LeftCons('bh'),			# W
	'\u0058':			LeftCons('m'),			# X
	'\u0059':			LeftCons('y'),			# Y
	'\u005a':			Syllable('ra'),			# Z
	'\u005b':			Syllable('la'),			# [
	'\u005c':			LeftCons('v'),			# \
	'\u005d':			LeftCons('"s'),			# ]
	'\u005e':			LeftCons('.s'),			# ^
	'\u005f':			LeftCons('s'),			# _
	'\u0060':			Syllable('ha'),			# `
	'\u0061':			Syllable('.la'),		# a
	'\u0062':			LeftCons('k.s'),		# b
	'\u0063':			LeftCons('j~n'),		# c
	'\u0064':			Syllable('"sra'),		# d
	'\u0065':			LeftCons('tr'),		# e
	'\u0066':			LeftCons('tt'),		# f
	'\u0068':			Vowel('.r'),			# h U+0069 6a 6c might be .rr .l .ll?
	'\u006c':			RightVowel('u'),		# l what is different from  s?
	'\u006d':			RightVowel('uu'),		# m what is different from t?
	'\u006e':			RightCons('n'),			# n	appears e.g. after '"' in pna
	'\u006f':			Virama('_'),			# o virama.
	'\u0070':			RightVowel('aa'),		# p
	'\u0071':			LeftVowel('i'),			# q
	'\u0072':			RightVowel('ii'),		# r what is different from \u00ee?
	'\u0073':			RightVowel('u'),		# s what is different from l?
	'\u0074':			RightVowel('uu'),		# t what is different from m?
	'\u0075':			RightVowel('e'),		# u becomes part of -o as 'pu'
	'\u0076':			RightVowel('ai'),		# v becomes part of -au as 'pv'
	'\u0077':			RightVowel('.r'),		# w 78 and 79 might be -.rr and -.l or -.l and -.ll
	'\u007a':			Syllable('.m'),			# z
	'\u007b':			RightFrontalR('r'),		# { hook above line. adds r to the beginning of syllable
	'\u007c':			RightFrontalRAndTailM('r-.m'),	# | hook above + dot. adds r to the beginning and .m to the end
	'\u007d':			RightCons('-r'),		# } line from center to left-bottom
	'\u007e':			RightCons('-r'),		# ~ caret below character (used for -r in syllables not ending with bar)
	'\u00a0':			LeftCons('pt-'),		# NBSP
	'\u00a8':			Syllable('dbha'),		# ¨
	'\u00a9':			Syllable('dda'),		# ©
	'\u00ae':			Syllable('dba'),		# ®
	'\u00b0':			Space(''),				# ° (spacing e.g. after ka, ruu)
	'\u00b1':			Syllable('kla'),		# ±
	'\u00b4':			Syllable('ddha'),		# ´
	'\u00b5':			Syllable('"nkta'),		# µ
	'\u00b7':			Syllable('ruu'),		# ·
	'\u00bb':			Syllable('kka'),		# »
	'\u00c1':			Syllable('dra'),		# Á
	'\u00c2':			Syllable('hya'),		# Â
	'\u00c4':			LeftCons('~nj-'),		# Ä
	'\u00c5':			LeftCons('~nc-'),		# Å
	'\u00c6':			Syllable('stra'),		# Æ
	'\u00c7':			LeftCons('cc-'),		# Ç
	'\u00c8':			Syllable('.thya'),		# È (.ttha? unlikely)
	'\u00c9':			LeftCons('jj-'),		# É
	'\u00cb':			Syllable('.tya'),		# Ë
	'\u00cc':			Vowel('u'),				# Ì ?
	'\u00cf':			Vowel('a'),				# Ï
	'\u00d1':			Syllable('lla'),		# Ñ
	'\u00d3':			Vowel('uu'),			# Ó ?
	'\u00d4':			Vowel('e'),				# Ô
	'\u00d5':			Syllable('.s.ta'),		# Õ
	'\u00d6':			Syllable('hna'),		# Ö
	'\u00da':			Vowel('i'),				# Ú
	'\u00dc':			Syllable('h.na'),		# Ü
	'\u00e0':			Syllable('hva'),		# à
	'\u00e1':			Syllable('hla'),		# á
	'\u00e3':			Syllable('"nkha'),		# ã
	'\u00e4':			Syllable('"nka'),		# ä
	'\u00e5':			Syllable('"nga'),		# å
	'\u00e6':			Syllable('sra'),		# æ
	'\u00e7':			Syllable('"ngha'),		# ç
	'\u00e8':			Syllable('"nk.sa'),		# è
	'\u00e9':			Syllable('"nma'),		# é
	'\u00eb':			Literal('\u2018'), 		# U+2018 left single quotation mark
	'\u00ec':			LeftVowel('i'),			# ì
	'\u00ed':			Literal('\u2019'),		# U+2019 right single quotation mark
	'\u00ee':			RightVowel('-ii'),		# î what is different from 'r'?
	'\u00f1':			Literal('\u2013'),		# ñ –, en-dash
	'\u00f2':			Syllable('kta'),		# ò
	'\u00f3':			Literal('\u2014'),		# ó —, em-dash
	'\u00f9':			Syllable('dya'),		# ù
	'\u00fb':			Syllable('dga'),		# û
	'\u00fc':			Syllable('dva'),		# ü
	'\u00ff':			LeftCons('ch-'),		# ÿ
	'\u0152':			Syllable('.s.tha'),		# Œ
	'\u0153':			LeftCons('hm-'),		# œ
	'\u02c6':			RightCons('-n'),		# ˆ ?
	'\u02dc':			RightCons('-ya'),		# ˜
	'\u2013':			LeftCons('gn-'),		# –
	'\u2014':			LeftCons('tn-'),		# —
	'\u201a':			Syllable('h.r'),		# ‚
	'\u201c':			LeftCons('kt-'),		# “
	'\u201e':			Syllable('hra'),		# „
	'\u2021':			Syllable('ru'),			# ‡
	'\u2026':			Syllable('kva'),		# …
	'\u2044':			LeftCons('l-'),			# ⁄
	'\u2122':			Syllable('d.r'),		# ™ ?
	'\u2206':			LeftCons('"sc-'),		# ∆
	'\u221a':			Syllable('sna'),		# √
	'\u221e':			Syllable('dbra'),		# ∞ ?
	'\u2260':			Syllable('dma'),		# ≠
	'\u2264':			Syllable('"nkra'),		# ≤
	'\u2265':			Syllable('"ngra'),		# ≥
	'\u25ca':			LeftCons('k-'),			# ◊
	'\ufb02':			LeftCons('nn-'),		# ﬂ
}

spacing_chars = [c for c in chars if isinstance(chars[c], Space) ]

repl = {
	'@':				'ka',
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
	'\u00f2z':			'kta.m',
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
	while line:
		c = line[0]
		if c in repl_trailing:
			repl_to = repl_to[:-1] + repl_trailing[c]
			if repl_to.endswith('ae'):
				repl_to = repl_to[:-2] + 'o'
			elif repl_to.endswith('aai'):
				repl_to = repl_to[:-3] + 'au'
		# add frontal "r" as in rvi, rva
		elif c == '{':
			repl_to = 'r' + repl_to
		# add trailing "r" as in grii, gra
		elif c == '}':
			repl_to = add_before_last_vowel('r', repl_to)
		# r-...-.m as combined as a single char
		elif c == '|':
			repl_to = 'r' + repl_to + '.m'
		elif c in spacing_chars:
			pass
		else:
			break
		line = line[1:]
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
