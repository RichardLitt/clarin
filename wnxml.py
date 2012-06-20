'''
Wordnet XML & CQP tagger
Richard Littauer, CLARIN-D

This depends on: 
  - having a full wordnet installation (specifically, wn)
  - currently, using Mac OSX (possible Unix).
  - having the stuttgard tree-tagger installed.

1 word per line (ignore xml) 
# Currently, this only works on a previously parsed text
look up word
annotate back into the xml

add a new tab at the end of the line ## Why?
would be a nice tool for weblicht
demo file

To do:
  - Make it executable outside of Mac OSX
  - Make it grab wordnet files externally #Meaning? 
  - Use an existing XML schema instead of the provisional one provided here
    #Need to look for this.
      - Better XML wrapping. # See above.
  - More options #Working on it.

'''

# Fedex some packages in
import subprocess, sys	
import nltk, re
import types

# The test file should be 'curdie'

file = open(sys.argv[2])
file = file.read()

output_file = '/Users/richardlittauer/Github/clarin/output_' + sys.argv[2] + \
        '_' + sys.argv[1]


# This gets tokenizers with the Stuttgart tree-tagger. 
def tree_tagger_text(input_file, language):
    tree_tagger = 'tree-tagger-' + language
    cmd = [ tree_tagger, sys.argv[2] ]
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
    opts = ['noun', 'verb', 'adj', 'adv']
    try:
        if sys.argv[5] in opts: pos = sys.argv[5]
        print 'Option chosen: ' + pos
    except:
        pos = ''
        while pos not in opts:
            pos = raw_input('verify: ')
        print 'Option chosen: ' + pos
    possible_choices = []
    #try:
    print
    for x in options[pos].keys():
        possible_choices += [x]
        print '\t%s\t\t%s' % (x, options[pos][x])
    print

    choices = ['hypen', 'hypon', 'synsn', 'hypev', 'synsv', 'simsv']

    print 'Options available currently: '
    for choice in choices: print '\t' + choice

    print

    # Making argument input possible
    try:
        if len(sys.argv[6]) >= 2:
            option_choice = []
            for choice in sys.argv[6].split(', '):
                if choice in choices:
                    option_choice.append(choice)
                if choice not in choices:
                    while choice not in choices:
                        choice = raw_input('Which options? (ex: hypen, treen) ')
                    option_choice.append(choice)
        print 'Options chosen: '
        for item in option_choice: print '\t' + item
        print
    
    # To manually input
    except:

        option_choice = []

        choices = raw_input('Which options? (ex: hypen, treen) ')

        for choice in choices.split(', '):
            while choice not in choices:
                choice = raw_input('Which options? (ex: hypen, treen) ')
            option_choice.append(choice)

        print 'Options chosen: '
        for item in option_choice: print '\t' + item
        print

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

    for x in optioned_text:
        written = False
        results = {}
        if len(x[0]) != 1:
            for choice in option_choice:
                if x[0][1] in pos_converter[pos]:

                    if x[0][2] != '<unknown>':
                        # Needs to be sorted for each type of option with a
                        # specific other function.
                        results[choice] = globals()[choice](wn_cmd_opt(x[0][2], choice))

            for key in sorted(results.iterkeys()):
                written = True
                if isinstance(results[key], types.StringTypes): 
                    if sys.argv[1] == 'xml':
                        print '<' + results[key] + '>'
                        f.write('<' + results[key] + '>\n')
                    if sys.argv[1] == 'cqp':
                        print results[key]
                        f.write(results[key] + '\n')
                if isinstance(results[key], types.ListType):
                    if sys.argv[1] == 'xml':
                        for sense in results[key]:
                            print '<' + sense + '>'
                            f.write('<' + sense + '>\n')
                    if sys.argv[1] == 'cqp':
                        for sense in results[key]:
                            print sense
                            f.write(sense + '\n')
            if written:
                print '\t'.join(x[0]) 
                f.write('\t'.join(x[0]) + '\n')
                if sys.argv[1] == 'xml':
                    for key in sorted(results.iterkeys(), reverse=True):
                        if isinstance(results[key], types.StringTypes): 
                            print '</' + key + '>'
                            f.write('</' + key + '>\n')
                        if isinstance(results[key], types.ListType):
                            for sense in results[key]:
                                print '</' + key + '>'
                                f.write('</' + key + '>\n')

            if not written:
                print '\t'.join(x[0])
                f.write('\t'.join(x[0]) + '\n')
        else:
            print x[0][0] + '\n'
            f.write(x[0][0] + '\n')


'''
These are the explicit options for pos information in wn
'''

# For noun hyponyms
def hypon(rawtext):
    option = 'hypon'

    # Split according to senses
    rawtext = rawtext.replace('\t','').replace('  ','').replace\
            (' => ','')
    rawtext = re.split('Sense \d+',rawtext)
    final_string = []

    # For each different sense
    for block in rawtext[1:]:

        index = rawtext.index(block)

        #split into lines
        block = block.split('\n')

        for item in block: 
            # remove empty items
            if item == '': block.remove(item)
        for item in block: 
            # remove empty items if any are left
            if item == '': block.remove(item)

        # Remove instances
        pattern = re.compile("INSTANCE")
        block[:] = [item for item in block if re.search(pattern, item) == None]

        if sys.argv[1] == 'xml': 
            #mung it all together
            results = '|'.join(block)
            final_string.append(option + '="' + results + '"')

        if sys.argv[1] == 'cqp':
            for item in range(len(block)):
                block[item] = 'sense' + str(index) + ':' + option + str(item) + ':' + block[item]

            #mung it all together
            results = '|'.join(block)
            final_string.append(results)

    return final_string

# For verb hyponyms
def hypev(rawtext):
    option = 'hypev'

    # Split according to senses
    rawtext = rawtext.replace('\t','').replace('  ','').replace\
            (' => ','')
    rawtext = re.split('Sense \d+',rawtext)
    final_string = []

    # For each different sense
    for block in rawtext[1:]:

        index = rawtext.index(block)

        #split into lines
        block = block.split('\n')

        for item in block: 
            # remove empty items
            if item == '': block.remove(item)
        for item in block: 
            # remove empty items if any are left
            if item == '': block.remove(item)

        # Remove instances
        pattern = re.compile("INSTANCE")
        block[:] = [item for item in block if re.search(pattern, item) == None]

        if sys.argv[1] == 'xml': 
            #mung it all together
            results = '|'.join(block)
            final_string.append(option + '="' + results + '"')

        if sys.argv[1] == 'cqp':
            for item in range(len(block)):
                block[item] = 'sense' + str(index) + ':' + option + str(item) + ':' + block[item]

            #mung it all together
            results = '|'.join(block)
            final_string.append(results)

    return final_string

# For noun hypernyms
def hypen(rawtext):
    option = 'hypen'
    
    # split according to senses
    rawtext = rawtext.replace('\t','').replace('  ','').replace(' => ', '')
    rawtext = re.split('Sense \d+',rawtext)
    final_string = []

    # For each different sense
    for block in rawtext[1:]:

        index = rawtext.index(block)

        #split into lines
        block = block.split('\n')

        for item in block: 
            # remove empty items
            if item == '': block.remove(item)
        for item in block: 
            # remove empty items if any are left
            if item == '': block.remove(item)

        # Remove instances
        pattern = re.compile("INSTANCE")
        block[:] = [item for item in block if re.search(pattern, item) == None]

        if sys.argv[1] == 'xml': 
            #mung it all together
            results = '|'.join(block)
            final_string.append(option + '="' + results + '"')

        if sys.argv[1] == 'cqp':
            for item in range(len(block)):
                block[item] = 'sense' + str(index) + ':' + option + str(item) + ':' + block[item]
            #mung it all together
            results = '|'.join(block)
            final_string.append(results)

    return final_string

# For the hyponym tree
def treen(rawtext):
    option = 'hypon'

    # Split according to senses
    rawtext = rawtext.replace('\t','').replace('    ', '.').replace(' => ','')
    rawtext = re.split('Sense \d+',rawtext)
    final_string = []

    print rawtext

    # For each different sense
    for block in rawtext[1:]:

        index = rawtext.index(block)

        #split into lines
        block = block.split('\n')

        for item in block: 
            # remove empty items
            if item == '': block.remove(item)
        for item in block: 
            # remove empty items if any are left
            if item == '': block.remove(item)


        # Remove instances
        pattern = re.compile("INSTANCE")
        block[:] = [item for item in block if re.search(pattern, item) == None]

        for item in range(len(block)): block[item] = block[item]\
                .replace(' ','')

        previous_item = [1,1]
        # Trying to think of a good looping mechanism to get the periods ##
        ### FAILING
        for item in range(len(block)):
            sense = index
            hypon = item
            while block[item][1] == '.':
                hypon
        print block
        
        if sys.argv[1] == 'xml': 
            #mung it all together
            results = '|'.join(block)
            final_string.append(option + '="' + results + '"')

        if sys.argv[1] == 'cqp':
            for item in range(len(block)):
                block[item] = 'sense' + str(index) + ':' + option + str(item) + ':' + block[item]

            #mung it all together
            results = '|'.join(block)
            final_string.append(results)

    return final_string

# For synonyms by frequency
def synsn(rawtext):
    option = 'synsn'
    
    # split according to senses
    rawtext = rawtext.replace('\t','').replace('  ','').replace(' => ', '')
    rawtext = re.split('Sense \d+',rawtext)
    final_string = []

    # For each different sense
    for block in rawtext[1:]:

        index = rawtext.index(block)

        #split into lines
        block = block.split('\n')

        for item in block: 
            # remove empty items
            if item == '': block.remove(item)
        for item in block: 
            # remove empty items if any are left
            if item == '': block.remove(item)

        if sys.argv[1] == 'xml': 
            #mung it all together
            results = '|'.join(block)
            final_string.append(option + '="' + results + '"')

        if sys.argv[1] == 'cqp':
            for item in range(len(block)):
                block[item] = 'sense' + str(index) + ':' + option + str(item) + ':' + block[item]
            #mung it all together
            results = '|'.join(block)
            final_string.append(results)

    return final_string

# For synonyms by frequence for verbs
def synsv(rawtext):
    option = 'synsv'
    
    # split according to senses
    rawtext = rawtext.replace('\t','').replace('  ','').replace(' => ', '')
    rawtext = re.split('Sense \d+',rawtext)
    final_string = []

    # For each different sense
    for block in rawtext[1:]:

        index = rawtext.index(block)

        #split into lines
        block = block.split('\n')

        for item in block: 
            # remove empty items
            if item == '': block.remove(item)
        for item in block: 
            # remove empty items if any are left
            if item == '': block.remove(item)

        if sys.argv[1] == 'xml': 
            #mung it all together
            results = '|'.join(block)
            final_string.append(option + '="' + results + '"')

        if sys.argv[1] == 'cqp':
            for item in range(len(block)):
                block[item] = 'sense' + str(index) + ':' + option + str(item) + ':' + block[item]
            #mung it all together
            results = '|'.join(block)
            final_string.append(results)

    return final_string

# For synonyms by similarity of meaning for vebrs
def simsv(rawtext):
    option = 'simsv'
    
    # split according to senses
    rawtext = rawtext.replace('\t','').replace('  ','').replace(' => ', '')\
            .replace('--------------','')
    rawtext = re.split('Sense \d+',rawtext)
    final_string = []

    # For each different sense
    for block in rawtext[1:]:

        index = rawtext.index(block)

        #split into lines
        block = block.split('\n')

        for item in block: 
            # remove empty items
            if item == '': block.remove(item)
        for item in block: 
            # remove empty items if any are left
            if item == '': block.remove(item)

        if sys.argv[1] == 'xml': 
            #mung it all together
            results = '|'.join(block)
            final_string.append(option + '="' + results + '"')

        if sys.argv[1] == 'cqp':
            for item in range(len(block)):
                block[item] = 'sense' + str(index) + ':' + option + str(item) + ':' + block[item]
            #mung it all together
            results = '|'.join(block)
            final_string.append(results)

    return final_string


# This is where things begin to happen. 
if __name__ == "__main__":

    '''
    Example argument input:
        python wnxml.py xml curdie tt english noun 'hypen, hypon'
        "      "        format file tagger language pos wn.options
    '''

    try:

        # How do we want this to be output?
        outFormats = ['xml', 'cqp']
        while sys.argv[1] not in outFormats:
            sys.argv[1] = raw_input('Choose xml or cqp output: ')

        # What sort of tagger do yuo want to use?
        if sys.argv[3] == 'tt':
            
            # What language is the text in?
            if (sys.argv[4] == 'english'): language = 'english'
            elif (sys.argv[4] == 'german'): language = 'german'
            else:
                language = raw_input('english or deutsch? e/g ')
                if language == 'e': language = 'english'
                if language == 'g': language = 'german'

            # Are we tagging a document we've already tagged?
            if sys.argv[2] == 'output_file':
                optioned_text, pos, choice = \
                tag_options(tt_lookup(file))
                tagger(optioned_text, pos, choice)

            # Or not?
            else:
                optioned_text, pos, choice = \
                tag_options(tt_lookup(tree_tagger_text(file, language)))
                tagger(optioned_text, pos, choice)

        # Not currently functional/tested
        if sys.argv[3] == 'nltk':
            # Let's tokenise the file so we can deal with each word. 
            tokens = nltk.word_tokenize(file)
            text = nltk.Text(tokens)
            word = pos_retain(pos_split(wn_cmd(item)))
            lookup(word)

    except: 
        print 'Wrong parameters. Consult developer.'

# Work in progress. 
