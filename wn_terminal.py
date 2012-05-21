'''
Wordnet XML tagger (in prep.)
Richard Littauer, CLARIN-D

This depends on: 
  - having a full wordnet installation (specifically, wn)
  - currently, using Mac OSX.
  - having the stuttgard tree-tagger installed. 

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

output_file = '/Users/richardlittauer/Github/clarin/output_file'


# This gets tokenizers with the Stuttgart tree-tagger. 
def tree_tagger_text(input_file, language):
    tree_tagger = 'tree-tagger-' + language
    cmd = [ tree_tagger, sys.argv[1] ]
    output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
    return output

# This grabs the relevent output from the terminal-side wordnet.
# It stores it as a single string.
def wn_cmd(word):
    cmd = [ 'wn', word]
    output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
    return output

def wn_cmd_opt(word_choice, option):
    option = '-' + option
    cmd = [ 'wn', word_choice, option]
    output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
    return output

# The following functions assume you are not using the Stuttgart Tree Tagger
# tokeniser. 

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
                try: 
                    wn_options[entry[0]] = entry[1]
                except: 
                    entry = entry[0].split('\t')
                    entry = map(lambda s: s.split(', '), entry)
                    if len(entry[0]) == 2:
                        wn_options[entry[0][0]] = entry[1][0]
                        wn_options[entry[0][1]] = entry[1][0]
        pos[pos_pass[3]] = wn_options
    if pos_pass[0] == 'Information': 
        word = pos_pass[4].split('\n')[0]
    else:
        word = pos_pass[5].split('\n')[0]
    dictionary[word] = pos
    return dictionary

# This is a lookup function if you're not sure what POS it is.
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

# Using the Penn Treebank used in the tree tagger tokenizer. 
def penn_treebank_match(wordlist):
    raw_word , pos , lemma = wordlist[0:3]
    # This list is not complete at the moment. 
    try:
        if pos == 'NN':
            return wordlist, pos_retain(pos_split(wn_cmd(lemma)))[lemma]['noun']
        if pos == 'PP':
            return wordlist, pos_retain(pos_split(wn_cmd(lemma)))[lemma]['noun']
        if pos == 'NNS':
            return wordlist, pos_retain(pos_split(wn_cmd(lemma)))[lemma]['noun']
        if pos == 'VBD':
            return wordlist, pos_retain(pos_split(wn_cmd(lemma)))[lemma]['verb']
        if pos == 'VBN':
            return wordlist, pos_retain(pos_split(wn_cmd(lemma)))[lemma]['verb']
        if pos == 'RB':
            return wordlist, pos_retain(pos_split(wn_cmd(lemma)))[lemma]['adv']
        if pos == 'JJ':
            return wordlist, pos_retain(pos_split(wn_cmd(lemma)))[lemma]['adj']
        else: return wordlist, {}
    except: return wordlist, {}

# Gets the available options for each word. 
def tt_lookup(tokenised_string):
    optioned_text = []
    
    dictionary = tokenised_string.split('\n')
    for line in range(len(dictionary)):
        if dictionary[line][:2] == '##':
            pass
        if dictionary[line][:1] == '<':
            pass
        dictionary[line] = dictionary[line].split('\t')
    for wordlist in dictionary:
        if len(wordlist) != 1:
            optioned_text += [penn_treebank_match(wordlist)]
        else:
            optioned_text.append((wordlist, {}))
    return optioned_text


# Presenting what the choices are, in case you want to choose
def tag_options(optioned_text):
    options = {}

    # From those available in the text. 
    for item in optioned_text: 
        if len(item[0]) != 1:
            if item[0][1] == 'NN': options['noun'] = item[1]
            if item[0][1] == 'NP': options['noun'] = item[1]
            if item[0][1] == 'NNS': options['noun'] = item[1]
            if item[0][1] == 'PP': options['noun'] =  item[1]
            if item[0][1] == 'VBD': options['verb'] = item[1]
            if item[0][1] == 'VBN': options['verb'] = item[1]
            if item[0][1] == 'RB': options['adv'] = item[1]
            if item[0][1] == 'JJ': options['adj'] = item[1]

    print 
    print 'Options for which part of speech?'
    print 'noun | verb | adj | adv '
    pos = raw_input('verify: ')
    possible_choices = []
    #try:
    print
    for x in options[pos].keys():
        possible_choices += [x]
        print '\t%s\t\t%s' % (x, options[pos][x])
    print

    # This except isn't working at the moment - need to find a better way to
    # loop
    #except: 
    #    print 'Did you spell it right?'
    #    pos = raw_input('verify: ')


    option_choice = raw_input('Which options? (ex: hypen, treen) ')
    for x in option_choice: 
        if x[0] == '-': 
            option_choice[x] = x[1:]
    option_choice = option_choice.replace(' ','').split(',')
    #for x in option_choice:
    #    if x not in possible_choices: 
    #        print 'Did you spell them right?'
    #        option_choice = raw_input('Which options? ')
    #        option_choice = option_choice.replace(' ','').split(',')

    return optioned_text, pos, option_choice

def tagger(optioned_text, pos, option_choice):
    pos_converter = {}
    pos_converter['noun'] = 'NN', 'NP', 'P', 'NNS'
    pos_converter['verb'] = 'VBD', 'VBN'
    pos_converter['adv'] = 'RB'
    pos_converter['adj'] = 'JJ'

    global output_file
    # Open up the file
    f = open(output_file,'w+')

    from datetime import datetime
    f.write('## XML Tagged from the Wordnet Parser on %s.\n' % str(datetime.now()))

    print optioned_text
    for x in optioned_text:
        written = False
        results = {}
        if len(x[0]) != 1:
            for choice in option_choice:
                if x[0][1] in pos_converter[pos]:
                    #try:
                    if x[0][2] != '<unknown>':
                        # Needs to be sorted for each type of option with a
                        # specific other function.
                        results[choice] = globals()[choice](wn_cmd_opt(x[0][2], choice))
                    #except:
                    #    continue
            for key in sorted(results.iterkeys()):
                written = True
                print '<' + results[key] + '>'
                f.write('<' + results[key] + '>\n')
            if written:
                print '\t'.join(x[0]) 
                f.write('\t'.join(x[0]) + '\n')
                for key in sorted(results.iterkeys(), reverse=True):
                    print '</' + key + '>'
                    f.write('</' + key + '>\n')
            if not written:
                print '\t'.join(x[0])
                f.write('\t'.join(x[0]) + '\n')
        else:
            print x[0][0]


# For hyponyms
def hypon(rawtext):
    rawtext = rawtext.replace('\t','').replace('  ','').split('\n')
    for item in rawtext: 
        if item == '': 
            rawtext.remove(item)
    # Doesn't have the sense delineated: could do --- 
    option = 'hypon'
    rawtext = rawtext[2:]
    pattern = re.compile(" HAS INSTANCE")
    rawtext[:] = [item for item in rawtext if re.match(pattern, item) == None]
    results = '|'.join(rawtext)
    final_string = option + '="' + results + '"'
    return final_string

def hypen(rawtext):
    rawtext = rawtext.replace('\t','').replace('  ','').split('\n')
    for item in rawtext: 
        if item == '': 
            rawtext.remove(item)
    option = 'hypen'
    rawtext = rawtext[2:]
    results = '|'.join(rawtext)
    final_string = option + '="' + results + '"'
    return final_string

def partn(rawtext):
    rawtext = rawtext.replace('\t','').replace('  ','').split('\n')
    for item in rawtext: 
        if item == '': 
            rawtext.remove(item)
    print rawtext
    option = 'partn'

def coorn(rawtext):
    rawtext = rawtext.replace('\t','').replace('  ','').split('\n')
    for item in rawtext: 
        if item == '': 
            rawtext.remove(item)
    print rawtext
    option = 'coorn'

def famln(rawtext):
    rawtext = rawtext.replace('\t','').replace('  ','').split('\n')
    for item in rawtext: 
        if item == '': 
            rawtext.remove(item)
    print rawtext
    option = 'famln'

def treen(rawtext):
    rawtext = rawtext.replace('\t','').replace('  ','').split('\n')
    for item in rawtext: 
        if item == '': 
            rawtext.remove(item)
    print rawtext
    option = 'treen'

def derin(rawtext):
    rawtext = rawtext.replace('\t','').replace('  ','').split('\n')
    for item in rawtext: 
        if item == '': 
            rawtext.remove(item)
    print rawtext
    option = 'derin'

def synsn(rawtext):
    rawtext = rawtext.replace('\t','').replace('  ','').split('\n')
    for item in rawtext: 
        if item == '': 
            rawtext.remove(item)
    print rawtext
    option = 'synsn'

def meron(rawtext):
    rawtext = rawtext.replace('\t','').replace('  ','').split('\n')
    for item in rawtext: 
        if item == '': 
            rawtext.remove(item)
    print rawtext
    option = 'hypon'

def over(rawtext):
    rawtext = rawtext.replace('\t','').replace('  ','').split('\n')
    for item in rawtext: 
        if item == '': 
            rawtext.remove(item)
    print rawtext
    option = 'over'


def hmern(rawtext):
    rawtext = rawtext.replace('\t','').replace('  ','').split('\n')
    for item in rawtext: 
        if item == '': 
            rawtext.remove(item)
    print rawtext
    option = 'hmern'


if __name__ == "__main__":
    #for item in text[:10]:
        # Argument 1 must be the input file.
    if sys.argv[2] == 'tt':
        language = sys.argv[3]
        if sys.argv[1] == 'output_file':
            optioned_text, pos, choice = \
            tag_options(tt_lookup(file))
            tagger(optioned_text, pos, choice)
        else:
            optioned_text, pos, choice = \
            tag_options(tt_lookup(tree_tagger_text(file, language)))
            tagger(optioned_text, pos, choice)

        # These are simply for testing, and will not end up in this section. 
        # hypon(wn_cmd_opt('mountain', '-hypon'))
        # hypen(wn_cmd_opt('mountain', '-hypen'))
        # partn(wn_cmd_opt('mountain', '-partn'))
        # coorn(wn_cmd_opt('mountain', '-coorn'))
        # famln(wn_cmd_opt('mountain', '-famln'))
        # treen(wn_cmd_opt('mountain', '-treen'))
        # derin(wn_cmd_opt('mountain', '-derin'))
        # synsn(wn_cmd_opt('mountain', '-synsn'))
        # meron(wn_cmd_opt('mountain', '-meron'))
        # over(wn_cmd_opt('mountain', '-over'))
        # hmern(wn_cmd_opt('mountain', '-hmern'))

    if sys.argv[2] == 'nltk':
        # Let's tokenise the file so we can deal with each word. 
        tokens = nltk.word_tokenize(file)
        text = nltk.Text(tokens)
        word = pos_retain(pos_split(wn_cmd(item)))
        lookup(word)
#except: 
    #    print 'Wrong parameters'



