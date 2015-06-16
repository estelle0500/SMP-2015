import re
import codecs

# file containing lexicon
lex = codecs.open("/Users/student/Downloads/lexicon_v3.txt", encoding="utf-8", mode="r+")

# file containing recorded sentences
rec = codecs.open("/Users/student/Downloads/prompts.txt", encoding="utf-8", mode="r+")

# output file for phone count
f = codecs.open("/Users/student/Documents/phone_count.txt", encoding="utf-8", mode="w+")

# output file for romanized hokkien
m = codecs.open("/Users/student/Documents/hokkien_romanization.txt", encoding="utf-8", mode="w+")

# counter for number of phones
count = {'i': 0.0, 'ei': 0.0, 'uh': 0.0, 'o': 0.0, 'ai': 0.0, 'ia': 0.0, 'ioo': 0.0, 'ua': 0.0, 'ui': 0.0, 'iau': 0.0, 'u': 0.0, 'e': 0.0, 'ah': 0.0, 'oh': 0.0, 'au': 0.0, 'io': 0.0, 'iu': 0.0, 'ue': 0.0, 'uai': 0.0, 'p': 0.0, 'b': 0.0, 't': 0.0, 'k': 0.0, 'q': 0.0, 'h': 0.0, 'm': 0.0, 'ng': 0.0, 's': 0.0, 'ts': 0.0, 'dz': 0.0, 'ph': 0.0, 'th': 0.0, 'kh': 0.0, 'n': 0.0, 'tsh': 0.0, 'l': 0.0, 'g': 0.0, 'j': 0.0, 'd': 0.0, '_': 0.0}

# counter for number of triphones
count_tri = {}
for x in count.keys():
	for y in count.keys():
		for z in count.keys():
			temp = x + y + z
			count_tri[temp] = 0

# list of words in lexicon (in Chinese characters) mapped to phone
char_list = {}

# number of phones in sentences
rec_total = 0.0

# number of triphones in sentences
rec_total_tri = 0.0

for line in lex:
	col = re.split(",", line)

	# strip nonalphabetical characters and make them lower case
	col[1] = re.sub("[^a-zA-Z /]+", "", col[1])
	col[1].lower()

	# alternate pronunciations
	word = []
	c = 0
	pron = re.split("/", col[1])
	for p in pron:
		print p
		word.append([])
		x = re.split(" ", p)
		for s in x:
			if not len(s) == 0 and not s.isspace():
				word[c].append(s)
		c += 1

	# characters/phrase
	# col[2] = re.sub("[a-zA-Z1-9,./':;?]()", "", col[2])
	li = []
	li.append(word)
	li.append(col[0])
	char_list[col[2]] = li

# sort dict keys by descending length of string
key = char_list.keys()
key.sort()
key.sort(key=len, reverse=True)
for k in key:
	if k.isspace() or len(k) == 0:
		key.remove(k)

for line in rec:

	# replace known phrases
	for word in key:
		cpy = line
		line = re.sub(word, char_list[word][1] + " ", line)
		while cpy != line:

			# count phones
			# print word
			for w in char_list[word][0]:
				for phone in w:
					if phone in count.keys():
						# print phone
						# print len(char_list[word][0])
						# print 1.0 / float(len(char_list[word]))
						count[phone] += 1.0 / float(len(char_list[word][0]))
						rec_total += 1.0 / float(len(char_list[word][0]))
				# print "\n"

			# count triphones
			for w in char_list[word][0]:
				# note: '_' is used to denote null / no phone
				if len(w) != 0:
					left_phone = "_"
					curr_phone = w[0]
					right_phone = "_"

					counter = 1
					while curr_phone != "_":
						if len(w) > counter:
							right_phone = w[counter]
						else:
							right_phone = "_"

						tri = left_phone + curr_phone + right_phone
						count_tri[tri] += 1.0 / float(len(char_list[word][0]))
						rec_total_tri += 1.0 / float(len(char_list[word][0]))
						left_phone = curr_phone
						curr_phone = right_phone
						counter += 1

			cpy = line
			line = re.sub(word, char_list[word][1], line)

	m.write(line)

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
	f.write(str(li[1]))
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
	f.write(str(li[1]))
	f.write(u"\u0009")
	f.write("\n")
