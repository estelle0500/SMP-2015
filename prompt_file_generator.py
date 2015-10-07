#!/usr/bin/python
"""
  Prompt generator for sentence collection.

    usage: edit the global variables at the top, then run. 
        python prompt_file_generator.py 

# BP: This is a docstring, you can refer to it as a global variable __DOC__, it doubles up as
# documentation on how you use this program
"""

import codecs,re,sys,os

# Global settings
# BP: remove the comments with heading # BP: after you're done reading
# BP: these are added for commentary and learning
RANDOM_SENTENCES='data/500sent.csv'
COMMON_SENTENCES='data/120sent.csv'
FILTER='perl csv2html.pl'
#FILTER=None
OUTDIR="out/"

# BP: python has two styles of commenting, quotation marks actually get bound to the function and 
# BP: become part of the help system. 
def prompt(line):
    " condense prompts in different languages into one"
    # input: one string with English, Chinese and Hokkien prompts separated by tabs
    # output: one string with all the prompts
    col = re.split(u"\u0009", line)
    # assuming English, Chinese and Hokkien prompts are in column 1, 2, 3 respectively
    prompt_str = "English: " + col[1]  + " Chinese: " + col[2] + " Hokkien: " + col[3]
    return prompt_str

# BP: %03i -> zero pad integer to 3 decimal places
def get_prompt_filename(i):
    "returns the path for the i'th speaker prompts"
    return os.path.join(OUTDIR,"prompt_file%03i.utt.txt" % i)

def get_path(id,  prompt_no):
    "returns the path to the id'th speaker prompt_no'th utterance"
    return "recordings/s1%02/spkr1%02i.u%03i.wav" % (id,id,prompt_no)

def format_prompt(id, prompt, prompt_no):
    " to format prompt for XML"
    # input: ID number of speaker, string containing prompt, prompt number
    # output: string containing prompt and filepath to save recording
    xml_str = prompt + u"\u0009"  + get_path(id,prompt_no)
    return xml_str

# BP: there's something to be said about this design. On one hand it doesn't decouple cleanly because
# BP: both this function and the function outside needs to know about the whole way of generation
# BP: this function doesn't really do something coherent. One way to fix this is to get it to return
# a list of indices rather than a tuple. Of course, that is huge, which is why
# we would return an "iterator" with the fixed range.
# take a look at generators in python.
def shuffle(id):
    "gets list of prompts for a range"
    # input: ID number of speaker, list of 500 prompts
    # output: tuple containing prompt number of first and last prompt
    t = (10 * (id - 1), 10 * (id - 1) + 80)
    return t

def load_prompts(fn):
    "loads a prompt file"
    if FILTER != None:
        fin=os.popen("cat %s | %s" %(fn,FILTER));
    else:
        fin=open(fn);
    prompts=map(lambda(x): x.strip(),fin.readlines());
    fin.close();
    return prompts;
    # BP: map(function, iterable) applies the function to every item in the iterable (list or dictionary)
    # BP: lambda(x): x.strip() defines an anonymous (unnamed) function that strips x. i.e. remove
    # BP: leading and trailing spaces

    # BP: remember to close files, in this case it takes care of it for you but remember in general
    # BP: to clean up after setting up

# main program

# BP: probably better to use two separate lists for clarity
# BP: also cleaned up by sharing the common function

# read prompts 
common_prompts=load_prompts(COMMON_SENTENCES);
random_prompts=load_prompts(RANDOM_SENTENCES);

# generate file for each speaker
for i in range(1, 51):
    # BP: python has a with statement which is convenient for doing this..
    # BP: after you exit the execution context, it automatically deallocates and closes it.

    # open up a file for this speaker's prompts list
    with codecs.open(get_prompt_filename(i), "w+", "utf-8-sig") as prompt_file:

        # add fixed sentences
        for j in range(0, len(common_prompts)):
            prompt_file.write(codecs.decode(common_prompts[j],'utf-8-sig'))
            prompt_file.write('\t'+get_path(i,j)+'\n')

                # add variable sentences
        tup = shuffle(i)
        for j in range(tup[0], tup[1]):
            prompt_file.write(codecs.decode(random_prompts[j % 500],'utf-8-sig'))
            prompt_file.write('\t'+get_path(i,j%500)+'\n')
# done
