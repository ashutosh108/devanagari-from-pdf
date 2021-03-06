#!/bin/env python3
import argparse
import re

# 'Literal' and derived classes are only used in chars array below. They are
# used to denote type of each entry so we can easily filter them by type.

# char to be replaced by literal string as given, not other handling required.
# e.g. digits, '.', etc
class CharType:
	def __init__(self, str):
		self.str = str

class Literal(CharType):
	pass

# represents char which denotes complete syllable which can optionally be
# appended with some trailing chars
class Syllable(CharType):
	pass

# represents vowel which is to replace whatever trailing vowel we have already
# "vowel which is the right half of simple syllable"
# e.g. -ii or -aa
class RightVowel(CharType):
	pass

# consonant to be added on the right, but before vowels
# e.g. -r
class RightCons(CharType):
	pass

# this char code is appended on the right, but 'r' must be added *in front* of
# the syllable
class RightFrontalR(CharType):
	pass

# like RightFrontalR but also add .m to the end
class RightFrontalRAndTailM(CharType):
	pass

# char code happens in the beginning of syllable, but represents '-i' to be
# appended to the syllable.  Only 'i', but it comes in three different codes
# for three different arc lenghts.
class LeftVowel(CharType):
	pass

# not a real space, but a spacing character used by original layout program to
# adjust characters properly. We simply ignore them at the end of each
# syllable.
# e.g. '>'
class Spacing(CharType):
	pass

# 'left half os syllable, a consonant'
# e.g. kh-
class LeftCons(CharType):
	pass

# complete vowel when it stands separately
# e.g. 'a' or 'i'
class Vowel(CharType):
	pass

# potential replacements (all codepoints extracted  from /ToUnicode objects in PDF files_:
chars = {
	'\u000a':			Literal('\n'),			# newline
	'\u000c':			Literal('\f'),			# formfeed (new page)
	'\u0020':			Literal(' '),			# space
	'\u0022':			RightVowel('a'),		# " vertical bar completing most syllables
	'\u0023':			Literal('.h'),			# #
	'\u0024':			Literal('|'),			# $
	'\u0025':			RightVowel('.rr'),		# %
	'\u0026':			Literal('.a'),			# &
	'\u0027':			Literal('[???]'),		# '
	'\u0028':			Literal('('),			# (
	'\u0029':			Literal(')'),			# )
	'\u002a':			Literal('*'),			# *
	'\u002b':			Literal('+'),			# +
	'\u002c':			Literal(','),			# ,
	'\u002d':			Literal('-'),			# -
	'\u002e':			Literal('.'),			# .
	'\u002f':			Literal('[???]'),		# /
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
	'\u003a':			Literal('[???]'),		# :
	'\u003b':			Literal(';'),			# ;
	'\u003c':			LeftVowel('i'),			# <
	'\u003d':			Literal('='),			# =
	'\u003e':			Spacing(''),			# >	(spacing)
	'\u003f':			Literal('?'),			# ?
	'\u0040':			Syllable('ka'),			# @
	'\u0041':			LeftCons('kh'),			# A
	'\u0042':			LeftCons('g'),			# B
	'\u0043':			LeftCons('gh'),			# C
	'\u0044':			Syllable('"na'),		# D
	'\u0045':			LeftCons('c'),			# E
	'\u0046':			Syllable('cha'),		# F
	'\u0047':			LeftCons('j'),			# G
	'\u0048':			LeftCons('jh'),			# H
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
	'\u0065':			LeftCons('tr'),			# e
	'\u0066':			LeftCons('tt'),			# f
	'\u0067':			Literal('.o'),			# g OM (AUM)
	'\u0068':			Vowel('.r'),			# h U+0069 6a 6c might be .rr .l .ll?
	'\u0069':			Literal('[???]'),		# i
	'\u006a':			Literal('[???]'),		# j
	'\u006b':			Literal('[???]'),		# k
	'\u006c':			RightVowel('u'),		# l what is different from  s?
	'\u006d':			RightVowel('uu'),		# m what is different from t?
	'\u006e':			RightCons('n'),			# n	appears e.g. after '"' in pna
	'\u006f':			RightVowel(''),			# o virama. Kind of cheaty to declare it as a 'RightVowel' bit it works
	'\u0070':			RightVowel('aa'),		# p
	'\u0071':			LeftVowel('i'),			# q
	'\u0072':			RightVowel('ii'),		# r what is different from \u00ee?
	'\u0073':			RightVowel('u'),		# s what is different from l?
	'\u0074':			RightVowel('uu'),		# t what is different from m?
	'\u0075':			RightVowel('e'),		# u becomes part of -o as 'pu'
	'\u0076':			RightVowel('ai'),		# v becomes part of -au as 'pv'
	'\u0077':			RightVowel('.r'),		# w 78 and 79 might be -.rr and -.l or -.l and -.ll
	'\u0078':			Literal('[???]'),		# x
	'\u0079':			Literal('~m'),			# y Chandra-bindu
	'\u007a':			Syllable('.m'),			# z
	'\u007b':			RightFrontalR('r'),		# { hook above line. adds r to the beginning of syllable
	'\u007c':			RightFrontalRAndTailM('r-.m'),	# | hook above + dot. adds r to the beginning and .m to the end
	'\u007d':			RightCons('r'),			# } line from center to left-bottom
	'\u007e':			RightCons('r'),			# ~ caret below character (used for -r in syllables not ending with bar)
	'\u00a0':			LeftCons('pt'),			# NBSP
	'\u00a2':			Literal('[???]'),		# ??
	'\u00a3':			Literal('[???]'),		# ??
	'\u00a7':			Literal('[???]'),		# ??
	'\u00a8':			Syllable('dbha'),		# ??
	'\u00a9':			Syllable('dda'),		# ??
	'\u00ac':			Literal('[???]'),		# ??
	'\u00ae':			Syllable('dba'),		# ??
	'\u00af':			RightCons('r'),			# ??
	'\u00b0':			Spacing(''),			# ?? (spacing e.g. after ka, ruu)
	'\u00b1':			Syllable('kla'),		# ??
	'\u00b4':			Syllable('ddha'),		# ??
	'\u00b5':			Syllable('"nkta'),		# ??
	'\u00b7':			Syllable('ruu'),		# ??
	'\u00bb':			Syllable('kka'),		# ??
	'\u00c0':			Syllable('.t.tha'),		# ??
	'\u00c1':			Syllable('dra'),		# ??
	'\u00c2':			Syllable('hya'),		# ??
	'\u00c4':			LeftCons('~nj'),		# ??
	'\u00c5':			LeftCons('~nc'),		# ??
	'\u00c6':			Syllable('stra'),		# ??
	'\u00c7':			LeftCons('cc'),			# ??
	'\u00c8':			Syllable('.thya'),		# ?? (.ttha? unlikely)
	'\u00c9':			LeftCons('jj'),			# ??
	'\u00cb':			Syllable('.tya'),		# ??
	'\u00cc':			Vowel('u'),				# ?? ?
	'\u00cd':			Syllable('.dya'),		# ??
	'\u00cf':			Vowel('a'),				# ??
	'\u00d1':			Syllable('lla'),		# ??
	'\u00d3':			Vowel('uu'),			# ?? ?
	'\u00d4':			Vowel('e'),				# ??
	'\u00d5':			Syllable('.s.ta'),		# ??
	'\u00d6':			Syllable('hna'),		# ??
	'\u00d8':			Syllable('dgha'),		# ??
	'\u00da':			Vowel('i'),				# ??
	'\u00dc':			Syllable('h.na'),		# ??
	'\u00e0':			Syllable('hva'),		# ??
	'\u00e1':			Syllable('hla'),		# ??
	'\u00e3':			Syllable('"nkha'),		# ??
	'\u00e4':			Syllable('"nka'),		# ??
	'\u00e5':			Syllable('"nga'),		# ??
	'\u00e6':			Syllable('sra'),		# ??
	'\u00e7':			Syllable('"ngha'),		# ??
	'\u00e8':			Syllable('"nk.sa'),		# ??
	'\u00e9':			Syllable('"nma'),		# ??
	'\u00eb':			Literal('\u2018'), 		# U+2018 left single quotation mark
	'\u00ec':			LeftVowel('i'),			# ??
	'\u00ed':			Literal('\u2019'),		# U+2019 right single quotation mark
	'\u00ee':			RightVowel('ii'),		# ?? what is different from 'r'?
	'\u00f1':			Literal('\u2014'),		# ?? ???, em-dash
	'\u00f2':			Syllable('kta'),		# ??
	'\u00f3':			Literal('\u2015'),		# ?? ???, horizontal bar (dash longer than em dash)
	'\u00f4':			Syllable('.t.ta'),		# ??
	'\u00f5':			Syllable('.d.da'),		# ??
	'\u00f7':			LeftCons('str'),		# ?? as in stryeva
	'\u00f9':			Syllable('dya'),		# ??
	'\u00fb':			Syllable('dga'),		# ??
	'\u00fc':			Syllable('dva'),		# ??
	'\u00ff':			LeftCons('ch'),			# ??
	'\u0152':			Syllable('.s.tha'),		# ??
	'\u0153':			LeftCons('hm'),			# ??
	'\u02c6':			Literal(','),			# ?? ?
	'\u02c7':			Literal('.'),			# ??
	'\u02dc':			RightCons('ya'),		# ??
	'\u2013':			LeftCons('gn'),			# ???
	'\u2014':			LeftCons('tn'),			# ???
	'\u201a':			Syllable('h.r'),		# ???
	'\u201c':			LeftCons('kt'),			# ???
	'\u201e':			Syllable('hra'),		# ???
	'\u2021':			Syllable('ru'),			# ???
	'\u2026':			Syllable('kva'),		# ???
	'\u2030':			Syllable('pla'),		# ???
	'\u203a':			Literal('[???]'),		# ???
	'\u2044':			LeftCons('l'),			# ???
	'\u2122':			Syllable('d.r'),		# ??? ?
	'\u2206':			LeftCons('"sc'),		# ???
	'\u2248':			LeftCons('"sn'),		# ???
	'\u221a':			Syllable('sna'),		# ???
	'\u221e':			Syllable('dbra'),		# ??? ?
	'\u2260':			Syllable('dma'),		# ???
	'\u2264':			Syllable('"nkra'),		# ???
	'\u2265':			Syllable('"ngra'),		# ???
	'\u25ca':			LeftCons('k'),			# ???
	'\ufb02':			LeftCons('nn'),			# ???
}

# Create separate associative arrays for each character type. e.g. all
# Vowel('') go to vowels[].
for code, syl in chars.items():
	array_name = type(syl).__name__.lower() + 's'
	if array_name not in globals():
		globals()[array_name] = {}
	globals()[array_name][code] = syl.str
	
start_chars = syllables | leftconss | literals | vowels

# return ([:consonant:]*)([:vowel:]?)
# assuming that there might be many consonants, but not more than one vowel.
def split_vowel(str):
	# Make sure we have two non-optional groups. Then empty groups would return
	# as '' (as we want), not as None
	r = re.compile(r'^(.*?)((?:a|aa|i|ii|u|uu|e|ai|o|au|\.r|\.rr|\.l|\.ll)?)$')
	m = r.match(str)
	if m:
		return m.groups()
	return str

def test_cons_vowel(str, cons, vwls):
	res = split_vowel(str)
	if res != (cons, vwls):
		raise Exception('%s split into %s, not (%s, %s)' % (str, res, cons, vwls))

# quick internal sanity checks
test_cons_vowel('ba', 'b', 'a')
test_cons_vowel('raa', 'r', 'aa')
test_cons_vowel('k.r', 'k', '.r')
test_cons_vowel('c', 'c', '')

def replace_vowel(str, newvowel):
	conss, oldvowel = split_vowel(str)
	return conss + newvowel

def handle_i_modifier(i_modifier, repl_to):
	if i_modifier:
		repl_to = replace_vowel(repl_to, 'i')
	i_modifier = False
	return i_modifier, repl_to

def add_before_last_vowel(what, syllable):
	conss, vowel = split_vowel(syllable)
	return conss + what + vowel

def handle_trailing_vowels_and_r(line, repl_to):
	while line:
		c = line[0]
		conss, oldvowel = split_vowel(repl_to)
		if c in rightvowels:
			newvowel = rightvowels[c]
			if oldvowel == 'aa' and newvowel == 'e':
				newvowel = 'o'
			elif oldvowel == 'aa' and newvowel == 'ai':
				newvowel = 'au'
			repl_to = conss + newvowel
		# add frontal "r" as in rvi, rva
		elif c in rightfrontalrs:
			# however, 'ii' is written as combination of 'i' and 'r hook'
			if repl_to == 'i':
				repl_to = 'ii'
			else:
				repl_to = 'r' + repl_to
		# add trailing "r" as in grii, gra
		elif c in rightconss:
			repl_to = add_before_last_vowel(rightconss[c], repl_to)
		# Generally, leftcons means start of a new syllable. However, if we
		# don't yet have complete syllable (i.e. oldvowel is '' so far), we
		# should consider leftcons-es part of our syllable.
		elif oldvowel == '' and c in leftconss:
			repl_to += leftconss[c]
		# Same for syllables[]
		elif oldvowel == '' and c in syllables:
			repl_to += syllables[c]
		# r-...-.m as combined as a single char
		elif c in rightfrontalrandtailms:
			repl_to = 'r' + repl_to + '.m'
		elif c in spacings:
			pass
		else:
			break
		line = line[1:]
	return line, repl_to

# swap and cleanup some letters on input to compensate weird spacing
def fix_common_letter_spacing_problems(line):
	# for some reason, pdftotext wants to move m- ('X') character before -e
	# ('u') while also adding space. It is probably because 'u' include quite a
	# step backwards. Try to fix it manually.
	line = line.replace('Xu ', 'uX')

	# naamnaiva: v- moves before -ai, fix it
	# S"pX"n\v "
	# S"pX"nv\"
	line = line.replace('\\v ', 'v\\')
	line = line.replace('\\u ', 'u\\')

	# ojastejodyutidhara.h: -r moves before -u, fix it
	# ??puG"_O"uG"pu??<s O"R"Z#
	# ??puG"_O"uG"pu??s<O"R"Z#
	line = line.replace('<s ', 's<')

	# viitamohairiti: -i moves before -ai, fix it
	# \"rO"X"pu`qv Z<O"
	# \"rO"X"pu`vqZ<O"
	line = line.replace('qv ', 'vq')
	line = line.replace('qu ', 'uq')

	# vyaapnoti: -i moves before -e (which is used as part of -o here)
	# \Y"pT"np<u O"
	# \Y"pT"npu<O"
	line = line.replace('<u ', 'u<')

	#vedairvi: -i moved before -ai
	#\"uQ<v \"{
	#\"uQ<v\"{
	line = line.replace('<v ', 'v<')

	# sarvadu.s.tanibarha.naaya: -u moved after .s.t, -i moved, spaces added.
	# We fix this, but it looks really custom. Would be nice to figure out a
	# more generic change.
	#_"\"{Q??l <> S"V"`{N"pY"
	#_"\"{Ql??<>S"V"`{N"pY"
	line = line.replace('\u00d5l ', 'l\u00d5')
	line = line.replace('<> ', '><')

	# striipu.msayorhari.h: s- moved before .m, -i before r-
	#??rT"s_z "Y"pu`q{ Z#
	#??rT"sz_"Y"pu`{qZ#
	line = line.replace('_z ', 'z_')
	line = line.replace('q{ ', '{q')

	#caturmmuurtti"scaturbaahu-
	#E"O"sXX"t<{ f"{???"O"sV"p{`-l
	#E"O"sXX"t{<f"{???"O"sV"p{`l-
	line = line.replace('<{ ', '{<')
	line = line.replace('-l', 'l-')

	return line

def decodeline(line):
	res = ''
	# collect additional parts of final syllable until we see syllable completion
	consonants_before_syllable = ''
	# since -i is written before the syllable, flag it as necessary
	i_modifier = False

	line = fix_common_letter_spacing_problems(line)

	while line:
		if line[0] in start_chars:
			repl_from = line[0]
			repl_to = start_chars[repl_from]
			line = line[1:]

			line, repl_to = handle_trailing_vowels_and_r(line, repl_to)
			i_modifier, repl_to = handle_i_modifier(i_modifier, repl_to)

			res += consonants_before_syllable + repl_to
			consonants_before_syllable = ''
		elif line[0] in leftconss:
			consonants_before_syllable += leftconss[line[0]]
			line = line[1:]
		elif line[0] in leftvowels:
			i_modifier = True
			line = line[1:]
		# could not find any known prefix, escape next char
		else:
			res += "[" + line[0] + "]"
			line = line[1:]
	return res

macroman_to_utf8_table = [
# 8x
'\u00c4', '\u00c5', '\u00c7', '\u00c9', '\u00d1', '\u00d6', '\u00dc', '\u00e1',
'\u00e0', '\u00e2', '\u00e4', '\u00e3', '\u00e5', '\u00e7', '\u00e9', '\u00e8',
# 9x
'\u00ea', '\u00eb', '\u00ed', '\u00ec', '\u00ee', '\u00ef', '\u00f1', '\u00f3',
'\u00f2', '\u00f4', '\u00f6', '\u00f5', '\u00fa', '\u00f9', '\u00fb', '\u00fc',
# Ax
'\u2020', '\u00b0', '\u00a2', '\u00a3', '\u00a7', '\u2022', '\u00b6', '\u00df',
'\u00ae', '\u00a9', '\u2122', '\u00b4', '\u00a8', '\u2260', '\u00c6', '\u00d8',
# Bx
'\u221e', '\u00b1', '\u2264', '\u2265', '\u00a5', '\u00b5', '\u2202', '\u2211',
'\u220f', '\u03c0', '\u222b', '\u00aa', '\u00ba', '\u03a9', '\u00e6', '\u00f8',
# Cx
'\u00bf', '\u00a1', '\u00ac', '\u221a', '\u0192', '\u2248', '\u2206', '\u00ab',
'\u00bb', '\u2026', '\u00a0', '\u00c0', '\u00c3', '\u00d5', '\u0152', '\u0153',
# Dx
'\u2013', '\u2014', '\u201c', '\u201d', '\u2018', '\u2019', '\u00f7', '\u25ca',
'\u00ff', '\u0178', '\u2044', '\u20ac', '\u2039', '\u203a', '\ufb01', '\ufb02',
# Ex
'\u2021', '\u00b7', '\u201a', '\u201e', '\u2030', '\u00c2', '\u00ca', '\u00c1',
'\u00cb', '\u00c8', '\u00cd', '\u00ce', '\u00cf', '\u00cc', '\u00d3', '\u00d4',
# Fx
'\uf8ff', '\u00d2', '\u00da', '\u00db', '\u00d9', '\u0131', '\u02c6', '\u02dc',
'\u00af', '\u02d8', '\u02d9', '\u02da', '\u00b8', '\u02dd', '\u02db', '\u02c7',
]
def macroman_to_utf8_char(c):
	if ord(c) >= 0x80 and ord(c) <= 0xff:
		return macroman_to_utf8_table[ord(c)-0x80]
	return c

def fix_macroman_encoded_string(line):
	return ''.join([macroman_to_utf8_char(c) for c in line])

def main(args):
	for line in args.infile:
		if args.verbose:
			print(line, end='')
		if args.macroman:
			line = fix_macroman_encoded_string(line)
			if args.verbose:
				print('same decoded from macroman:')
				print(line, end='')
		print(decodeline(line), end='')

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description=
			'Decode Devanagari text after pdftotext (from poppler-utils)')
	parser.add_argument('-v', '--verbose', help='print each input line before it\'s decoded version',
			action='store_true')
	parser.add_argument('-m', '--macroman', help='assume Mac OS Roman encoding instead of usual UTF-8 (useful for some PDF files with fonts without /ToUnicode tables)',
			action='store_true')
	parser.add_argument(
		"infile",
		type=argparse.FileType('r'),
		help="source .txt output from pdftotext")
	args = parser.parse_args()

	main(args)
