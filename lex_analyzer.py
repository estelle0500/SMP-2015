import re
import codecs
import random

# file containing lexicon
lex = codecs.open("/Users/student/Documents/lexicon.txt", encoding="utf-8", mode="r+")

# file containing recorded sentences
rec = codecs.open("/Users/student/Downloads/prompts.txt", encoding="utf-8", mode="r+")

# output file for phone count
f = codecs.open("/Users/student/Documents/phone_count.txt", encoding="utf-8", mode="w+")

# output file for romanized hokkien
m = codecs.open("/Users/student/Documents/hokkien_romanization.txt", encoding="utf-8", mode="w+")

# output file for missing words
z = codecs.open("/Users/student/Documents/missing_words.txt", encoding="utf-8", mode="w+")

# counter for number of phones
count = {}# {'i': 0.0, 'ei': 0.0, 'uh': 0.0, 'o': 0.0, 'ai': 0.0, 'ia': 0.0, 'ioo': 0.0, 'ua': 0.0, 'ui': 0.0, 'iau': 0.0, 'u': 0.0, 'e': 0.0, 'ah': 0.0, 'oh': 0.0, 'au': 0.0, 'io': 0.0, 'iu': 0.0, 'ue': 0.0, 'uai': 0.0, 'p': 0.0, 'b': 0.0, 't': 0.0, 'k': 0.0, 'q': 0.0, 'h': 0.0, 'm': 0.0, 'ng': 0.0, 's': 0.0, 'ts': 0.0, 'dz': 0.0, 'ph': 0.0, 'th': 0.0, 'kh': 0.0, 'n': 0.0, 'tsh': 0.0, 'l': 0.0, 'g': 0.0, 'j': 0.0, 'd': 0.0, '_': 0.0}

# counter for number of triphones
count_tri = {}

# list of words in lexicon (in Chinese characters) mapped to phone
char_list = {}

# words which have unknown pronunciation
unknown_words = []

# number of phones in sentences
rec_total = 0.0

# number of triphones in sentences
rec_total_tri = 0.0

giant_string = ""

curr_rand = ""

for line in lex:
	col = re.split(",", line)
	# col = re.split(" ", line, 1)

	# strip nonalphabetical characters and make them lower case
	col[1] = re.sub("[^a-zA-Z /]+", "", col[1])
	# col[1].lower()
	#print col[0]
	#print col[1]
	#char_list[col[0]] = col[1]

	# alternate pronunciations
	word = []
	pron = re.split("/", col[1])
	c = 0
	for p in pron:
		word.append([])

		# split into phones
		x = re.split(" ", p)
		for s in x:
			if not len(s) == 0 and not s.isspace():
				word[c].append(s)
		c += 1

	# characters/phrase
	col[2] = re.sub("[a-zA-Z1-9,./':;?() ]", "", col[2])
	li = []
	pron2 = re.split("/", col[0])
	li.append(word)
	li.append(pron2)

	# multiple chinese phrases mapped to same hokkien phrase
	chars = re.split(u"\uFF0F", col[2])
	for char in chars:
		if not len(char) == 0 and not char.isspace():
			#print char
			char_list[char] = li

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


def count_trip(phones, num, occ):
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
			if tri in count_tri.keys():
				count_tri[tri] += 1.0 / float(num) * occ
			else:
				count_tri[tri] = 1.0 / float(num) * occ
			rec_total_tri += 1.0 / float(num)
			left_phone = curr_phone
			curr_phone = right_phone
			counter += 1


def missing_words(string):
	# search for unknown words
	global unknown_words

	# ignore already romanized characters and chinese (full-width) punctuation
	c = "[a-zA-Z1-9 (){},./;" + u"\uFF1A" + u"\uFF0F" + u"\uFF0C" + u"\uFF01" + u"\uFF02" + u"\uFF1B" + u"\uFF1F" + u"\uFF5B" + u"\uFF3B" + u"\uFF3D" + u"\uFF5D" + u"\uFF08" + u"\uFF09" + u"\u3002" + "]"
	string = re.sub(c, "", string)
	for char in string:
		if char not in unknown_words and not char.isspace():
			unknown_words.append(char)


def rand_repl(word):
	global char_list
	global curr_rand
	r = random.choice(char_list[word][1])
	curr_rand = char_list[word][1].index(r)
	count_p(char_list[word][0][curr_rand], len(char_list[word][0]), 1)
	count_trip(char_list[word][0][curr_rand], len(char_list[word][0]), 1)
	return r

for line in rec:

	#cpy = re.split(" ", line, 1)
	#cpy[1] = re.sub(" ", "", cpy[1])
	giant_string += line


for word in key:
	a = re.subn(word, rand_repl(word), giant_string)
	giant_string = a[0]
	w = char_list[word][0][curr_rand]
	x = len(char_list[word][0])
	# count_p(w, x, a[1])
	# count_trip(w, x, a[1])

missing_words(giant_string)
m.write(giant_string)


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


z.write("Unknown words:\n")
z.write(str(len(unknown_words))+"\n")
for word in range(0, len(unknown_words)):
	z.write(unknown_words[word] + "\n")
