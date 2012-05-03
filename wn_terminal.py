'''
Wordnet XML tagger (in prep.)
Richard Littauer, CLARIN-D

This depends on: 
  - having a full wordnet installation (specifically, wn)
  - currently, using Mac OSX.

annotate corpora with information from wordnet
1 word per line (ignore xml)
look up word
annotate back into the xml

work similar to a tagger
lemma, pos
only .... in the word tag
add a new tab at the end of the line
would be a nice tool for CLARIN/weblicht
demo file

To do:
  - Make it executable outside of Mac OSX
  - Make it grab wordnet files externally
  - Use an existing XML schema instead of the provisional one provided here
  - Better XML wrapping.
  - More options

'''

# Fedex some packages in
import subprocess, sys	
import nltk, re, pprint

# The test file should be 'curdie'

file = open(sys.argv[1])
file = file.read()

# Let's tokenise the file so we can deal with each word. 
tokens = nltk.word_tokenize(file)
text = nltk.Text(tokens)

# This grabs the relevent output from the terminal-side wordnet.
# It stores it as a single string.
def wn_cmd(word):
    cmd = [ 'wn', word]
    output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
    return output

def wn_cmd_opt(word_choice, option):
    cmd = [ 'wn', word_choice, option]
    output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
    return output


# This leaves you with four main blocks for the four poss.
def pos_split(raw_word):
    raw = raw_word.split('\n\n')
    pos_list = map(lambda s: s.strip(), raw)
    return pos_list


# This keeps the parts of speech that are relevant as a dictionary
def pos_retain(pos_list):
    dictionary = {}

    # Defines the part of speech in a dictionary
    pos = {}
    for item in pos_list:
        pos_pass = item.split(' ')
        
        # Is there any information on that POS for this word?
        if pos_pass[0] == 'No':
            continue
        else:
            # Ok, if there is, put the options in a dictionary
            wn_options = {}
            item = item.split('\n')
            item = map(lambda s: s.strip(), item)
            item = map(lambda s: s.split('\t\t'), item[1:])
            for entry in item: 
                try: wn_options[entry[0]] = entry[1]
                except: 
                    entry = entry[0].split('\t')
                    entry = map(lambda s: s.split(', '), entry)
                    if len(entry[0]) == 2:
                        wn_options[entry[0][0]] = entry[1][0]
                        wn_options[entry[0][1]] = entry[1][0]
        pos[pos_pass[3]] = wn_options
    word = pos_pass[5].split('\n')[0]
    dictionary[word] = pos
    return dictionary

def lookup(word):
    for item in word: options = word[item]
    if options != {}:
        print
        print 'Choose an option for pos:'
        for pos in options: 
            print pos
            for item in options[pos]:
                print '\t%s\t%s' % (item, options[pos][item])
        print
        print word
        pos_choice = raw_input('POS: ')
        choice = raw_input('Option: ')
        for pos in options: 
            if pos_choice == pos:
                pos = pos
                break
        for item in options[pos]: 
            if choice == item:
                word_choice = word.keys()[0]
                print wn_cmd_opt(word_choice, choice)
    else: print 'There is no entry for the word %s.' % word.keys()[0]

if __name__ == "__main__":
    try:
        for item in text[:10]:
            word = pos_retain(pos_split(wn_cmd(item)))
            lookup(word)
    except: 
        print 'Wrong parameters'



