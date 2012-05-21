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

from __future__ import division
import subprocess, sys	
import nltk, re, pprint
nltk.download()
from nltk.corpus import wordnet as wn

# The test file should be 'curdie'

file = open(sys.argv[1])
file = file.read()

tokens = nltk.word_tokenize(file)
text = nltk.Text(tokens)

print [wn.synsets(item) for item in text[:10]]

# wordList = file.split(' ')
# print wordList

# This grabs the relevent output from the terminal-side wordnet.
# It stores it as a single string.
def wn_cmd(word):
    cmd = [ 'wn', word]
    output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
    return output

#def wndict():
    #blah blah blah
    #blah blah
    #blah

#output = output.split('\n')
#print output

#if __name__ == "__main__":
    #wn(sys.argv[1])

