#!/Library/Frameworks/Python.framework/Versions/Current/bin/python
# -*- coding: ISO-8859-1 -*-

# arg enabler
import sys
# This is the parser/scraper/XMLer
from BeautifulSoup import BeautifulSoup 
# This is for regex
import re 
# And now for some unicode
import codecs
# For converting strings to file objects later, for looping
from StringIO import StringIO


# This should get all of the information from an annotation file, 
# and put it into a dictionary. 
annotations = {}
def get_annotations(uamin, annotations):
    # Parse the annotation file, get the segments needed.
    bs = BeautifulSoup(uamin)
    segmentlist = bs.findAll('segment')
    # Make it a dictionary
    for s in segmentlist:
        # Using IDs, get all information
        # Remove extra stuff in 'features'
        annotations[s['id']] = [\
            # Int format for indexing later.
            int(s['start']),\
            int(s['end']),\
            # negev, posev, etc. 
            s['features'][11:].split(';')[0],\
            # The contents. | and | aded on the edges. 
            '|' + '|'.join(s['features'][11:].split(';')[1:]) + '|',\
            # active or not? NB that active is not currently referenced in the
            # code, and must be later for inactive tags. 
            s['state']\
            ]
        # To see how this looks
        # print annotations[s['id']] 

        # Without using lists - not as efficient.
        #sid = segment['id']
        #start = segment['start']
        #end = segment['end']
        #features = segment['feature s'][11:]
        #features = re.sub(';','|', features)
        #state = segment['state']
    return annotations

'''
# Simply put, the system of skipping to the end of a word if the end happens to
# be in the middle of it, and placing the closing tag there, does not work. I am
# not sure why, but I've spent some considerable amount of hours on it. I suspect
# that there is something amiss with the cleanIndexing. The issue may be that
# it is unclear where exactly the start is supposed to fall - before 203?
# After? In any event, the tagging scheme is quite opaque. 

# One of the clear issues is the test .pretag files - it is not clear what is
# intended. Particularly as none of the tags seem to fall where the Annotation
# file wants them to. They are either early, or late, or the codecs are messing
# something up that I can't see. 

# The perl code I could not adapt can be found, generally, in lines 215-280.
# Lines 229-241 are especially confusing - what does check the end segment
# first mean? Much of this may be inability to deal with the scriptiness of
# perl, but I don't think so. I think much of the issue lies with the
# opaqueness of the annotations, not with the code. The 'small bug' is more
# likely to be an annotator problem. I may very well be wrong, particularly as
# the bug below is due to my own problems with how I set this up. I should
# recode this half, as my idea of using a clean index where annotations are
# ignored doesn't seem to work very well. 
'''


# This should use those annotations and an input file to create an output 
# annotated file. 
def annotate(input_file, annotations):

    # Get the annotations you'll be needing. Look them up in the dictionary.
    # Putting in an index at the end of range() limits the annotator, for
    # development uses. 
    for line in range(len(annotations))[:5]:
        line = annotations[str(line+1)]
        start, end, ftag, fvalue, state = line

        # This changes for each iteration - the goal is to not mess up the
        # clean version, so that the start/end indexes aren't off. 
        output = ''
        # Keep a version without tags for referencing
        clean = ''
        # Track whether you're in a tag or not
        tag = False
        # Indexes for normal version and tagless version
        cIndex = -1
        cleanIndex = -1
        # Make a dictionary so that you can cross reference, so that previous
        # tags go into the output, as well, and not just a clean version.
        IndexBinding = {}

        # Go through character by character, updating the index
        while True:
            c = input_file.read(1)
            cIndex += 1
            # If not in a tag, update clean index and make the ref. version
            if c == '<': tag = True
            if not tag: 
                clean += c
                cleanIndex += 1
            if c == '>': 
                tag = False
                cleanIndex -= 1
            # Stop at the end
            if not c: break
            # Make the cross-reference index. 
            IndexBinding[cleanIndex] = cIndex

        input_file.seek(0)
        f = input_file.read()

        #print f

        # Add in what you've already scanned
        output += f[:IndexBinding[start]]
        # And the new tags
        if output[-2] != '>':
            output += '\n<' + ftag + ' attr="' + fvalue + '">\n'
        elif output[-2] == '>':
            output += '<' + ftag + ' attr="' + fvalue + '">\n'
        # Add in what's inside the tags, and the end, then reset
        while f[IndexBinding[end]] not in (' '):
            end += 1
        #output += f[IndexBinding[start]:IndexBinding[end]]
        output += f[IndexBinding[start]:IndexBinding[end]]
        #print output_string
        if output[-1] != '\n':
            output += '\n</' + ftag + '>\n'
        elif output[-1] == '\n':
            output += '</' + ftag + '>\n'
        # Put the rest in
        output += f[IndexBinding[end]:]

        # Print it ou in iterations to be clear what is going on each time.
        # This can and should be commented out later.
        # print output

        # This converts the output into a file object so that read() works
        # again. cStringIO is faster, but not unicode. 
        input_file = StringIO(output)

        #print output

    # Print out the final annotated results. This should eventually be written
    # to the output file - given the current bugs, not necessary. 
    #print '==================================================' 
    print input_file.read()
    
    # Print out preliminary results for now
    # Codec issues at the moment. 
    output_file = 'output.pretag'
    g = codecs.open(output_file, 'w+', encoding='utf-8')
    g.write(output)
    g.close()

# The main program
if __name__ == "__main__":
    try:
        # The annotation file
        uamin = codecs.open(sys.argv[2], 'r+', encoding='utf-8')
        # The target file to annotate
        input_file = codecs.open(sys.argv[1], 'r+', encoding='utf-8')
        # Call the functions
        annotate(input_file, get_annotations(uamin, annotations))

    # When something goes wrong. A loop will be put here for more annotation.
    except IndexError:
        print "Usage: uam2xml.py <text-file> <UAM-file>\n"
