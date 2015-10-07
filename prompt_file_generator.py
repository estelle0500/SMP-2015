#!/usr/bin/python
import codecs
import re


def prompt(line):
	# condense prompts in different languages into one
	# input: one string with English, Chinese and Hokkien prompts separated by tabs
	# output: one string with all the prompts
	col = re.split(u"\u0009", line)
	# assuming English, Chinese and Hokkien prompts are in column 1, 2, 3 respectively
	prompt_str = "English: " + col[1]  + " Chinese: " + col[2] + " Hokkien: " + col[3]
	return prompt_str


def format_prompt(id, prompt, prompt_no):
	# to format prompt for XML
	# input: ID number of speaker, string containing prompt, prompt number
	# output: string containing prompt and filepath to save recording
	xml_str = prompt + u"\u0009" + str(id).zfill(2) + "_" + str(prompt_no + 1).zfill(3) + "\n"
	return xml_str


def shuffle(id):
	# input: ID number of speaker, list of 500 prompts
	# output: tuple containing prompt number of first and last prompt
	t = (10 * (id - 1), 10 * (id - 1) + 80)
	return t

# main program

# open file for 500 sentences
f500 = open("/Users/student/Downloads/500sent.txt")

# open file for 120 fixed sentences
f120 = open("/Users/student/Downloads/120sent.txt")

# list of prompts
prompt_list = []

# add prompts to list
for line in f500:
	prompt_list.append(prompt(line))

for line in f120:
	prompt_list.append(prompt(line))

# generate file for each speaker
for i in range(1, 51):
	# open up a file for this speaker's prompts list
	prompt_file = codecs.open("/Users/student/Documents/generator/prompt_file" + str(i).zfill(2), mode="w+")

	# add fixed sentences
	for j in range(500, 520):
		prompt_file.write(format_prompt(i, prompt_list[j], j))

	# add variable sentences
	tup = shuffle(i)
	for j in range(tup[0], tup[1]):
		prompt_file.write(format_prompt(i, prompt_list[j % 500], j % 500))
# done
