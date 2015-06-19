import re
import codecs
import random

# file containing lexicon
lex = codecs.open("/Users/student/Documents/lexicon.txt", encoding="utf-8", mode="r+")

# file containing recorded sentences
rec = codecs.open("/Users/student/Documents/textcpy.txt", encoding="utf-8", mode="r+")

# output file for phone count
f = codecs.open("/Users/student/Documents/phone_count_m.txt", encoding="utf-8", mode="w+")

# output file for romanized hokkien
m = codecs.open("/Users/student/Documents/hokkien_romanization.txt", encoding="utf-8", mode="w+")

# counter for number of phones
count = {}# {'i': 0.0, 'ei': 0.0, 'uh': 0.0, 'o': 0.0, 'ai': 0.0, 'ia': 0.0, 'ioo': 0.0, 'ua': 0.0, 'ui': 0.0, 'iau': 0.0, 'u': 0.0, 'e': 0.0, 'ah': 0.0, 'oh': 0.0, 'au': 0.0, 'io': 0.0, 'iu': 0.0, 'ue': 0.0, 'uai': 0.0, 'p': 0.0, 'b': 0.0, 't': 0.0, 'k': 0.0, 'q': 0.0, 'h': 0.0, 'm': 0.0, 'ng': 0.0, 's': 0.0, 'ts': 0.0, 'dz': 0.0, 'ph': 0.0, 'th': 0.0, 'kh': 0.0, 'n': 0.0, 'tsh': 0.0, 'l': 0.0, 'g': 0.0, 'j': 0.0, 'd': 0.0, '_': 0.0}

# counter for number of triphones
count_tri = {}
""" for x in count.keys():
	for y in count.keys():
		for z in count.keys():
			temp = x + y + z
			count_tri[temp] = 0
"""

# list of words in lexicon (in Chinese characters) mapped to phone
char_list = {}

# words which have unknown pronunciation
unknown_words = []

# number of phones in sentences
rec_total = 0.0

# number of triphones in sentences
rec_total_tri = 0.0

giant_string = ""

for line in lex:
	# col = re.split(",", line)
	col = re.split(" ", line, 1)

	# strip nonalphabetical characters and make them lower case
	col[1] = re.sub("[^a-zA-Z /]+", "", col[1])
	# col[1].lower()
	print col[0]
	print col[1]
	char_list[col[0]] = col[1]

	# alternate pronunciations
	"""word = []
	c = 0
	pron = re.split("/", col[1])
	for p in pron:
		word.append([])
		x = re.split(" ", p)
		for s in x:
			if not len(s) == 0 and not s.isspace():
				word[c].append(s)
		c += 1

	# characters/phrase
	# col[2] = re.sub("[a-zA-Z1-9,./':;?]()", "", col[2])
	li = []
	pron2 = re.split("/", col[0])
	li.append(word)
	li.append(pron2)
	col[2] = re.sub("[a-zA-Z1-9 ]", "", col[2])
	chars = re.split(u"\uFF0F", col[2])
	chars_unq = []
	for char in chars:
		if not len(char) == 0 and not char.isspace():
			chars_unq.append(char)
			print char
			char_list[char] = li"""

# sort dict keys by descending length of string
key = char_list.keys()
key.sort()
key.sort(key=len, reverse=True)
for k in key:
	if k.isspace() or len(k) == 0:
		key.remove(k)


def count_p(phones, num, occ):
	# count phones
	global count
	global rec_total
	for phone in phones:
		if phone in count.keys():
			count[phone] += 1.0 / float(num) * occ
			rec_total += 1.0 / float(num) * occ
		else:
			count[phone] = 1.0 / float(num) * occ
			rec_total += 1.0 / float(num) * occ


def count_trip(phones, num):
	# count triphones
	global count_tri
	global rec_total_tri
	if len(phones) != 0:
		left_phone = "_"
		curr_phone = phones[0]
		right_phone = "_"

		counter = 1
		while curr_phone != "_":
			if len(phones) > counter:
				right_phone = phones[counter]
			else:
				right_phone = "_"

			tri = left_phone + curr_phone + right_phone
			count_tri[tri] += 1.0 / float(num)
			rec_total_tri += 1.0 / float(num)
			left_phone = curr_phone
			curr_phone = right_phone
			counter += 1


def missing_words(string):
	# search for unknown words
	global unknown_words
	string = re.sub("[a-zA-Z1-9]", "", string)
	for char in string:
		if char not in unknown_words:
			unknown_words.append(char)

for line in rec:

	# replace known phrases
	# rand_pron = random.choice(char_list[word][1])
	# line = re.sub(word, rand_pron + " ", line)
	cpy = re.split(" ", line, 1)
	cpy[1] = re.sub(" ", "", cpy[1])
	giant_string += cpy[1]
	# index = 0
	""" word = []
	while index != len(cpy[1]):
		end = len(cpy[1]) - 1
		sstring = cpy[1][index:end]
		while end != index and sstring not in char_list.keys():
			end -= 1
			sstring = cpy[1][index:end]
		if end == index:
			index += 1
		else:
			print sstring
			count_p(char_list[sstring], 1, 1)
			index = end + 1
		# count phones and triphones
		for w in char_list[word][0]:
			x = len(char_list[word][0])
			count_p(w, x)
			count_trip(w, x)
		"""
	# count_p(char_list[word], 1, a[1])
			# rand_pron = random.choice(char_list[word][1])
			# line = re.sub(word, rand_pron + " ", line)
	# print word
	#missing_words(line)
	#m.write(line)
print giant_string

for word in key:
	print word
	a = re.subn(word, char_list[word], giant_string)
	giant_string = a[0]
	w = re.split(" ", char_list[word])
	count_p(w, 1, a[1])

# sorted order
f.write("Phone count in sorted order (descending):\n")
sort_count = []
for phone in count.keys():
	sort_count.append([count[phone], phone])
for li in sorted(sort_count, reverse=True):
	f.write(str(round(li[0],2)))
	f.write(u"\u0009")
	f.write(str(round(li[0] / rec_total * 100, 1)))
	f.write(u"\u0009")
	x = unicode(li[1])
	f.write(x)
	f.write(u"\u0009")
	f.write("\n")


# sorted order for triphones
f.write("Triphone count in sorted order (descending):\n")
sort_count_tri = []
for phone in count_tri.keys():
	if count_tri[phone] != 0:
		sort_count_tri.append([count_tri[phone], phone])
for li in sorted(sort_count_tri, reverse=True):
	f.write(str(round(li[0],2)))
	f.write(u"\u0009")
	f.write(str(round(li[0] / rec_total_tri * 100, 1)))
	f.write(u"\u0009")
	x = unicode(li[1])
	f.write(x)
	f.write(u"\u0009")
	f.write("\n")

"""
f.write("Unknown words:\n")
f.write(str(len(unknown_words)))
for word in range(0, len(unknown_words)):
	f.write(unknown_words[word] + "\n")"""
