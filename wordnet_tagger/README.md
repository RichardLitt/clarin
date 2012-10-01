WordNet CQP and XML Tagger
==============================

This was developed by Richard Littauer as part of the CLARIN-D project,
at Saarland University in Saarbrücken. 

# Requirements
--------------

This code is dependant upon:
  * Using the Mac OSX terminal (Possibly with UNIX terminal)
  * [Python 2.7](http://www.python.org/getit/releases/2.7/) (Not compatible with Python 3)
  * An installed command-line version of [WordNet](http://wordnet.princeton.edu/wordnet/download/). Running `wn tree -hypon` should be possible from the terminal.
  * The [Stuttgart Tree Tagger](http://www.ims.uni-stuttgart.de/projekte/corplex/TreeTagger/), also runnable from the command line.

Clone this repository, or simply download `wn_tagger.py` and use your
own corpora, in any format.

If you would like to use the tagger universally, set up a symbolic link:

  * `$ ln -s /your/desired/directory/path/wn_tagger.py /usr/bin/wn_tagger`
  * `$ chmod 755 a+x /your/desired/directory/path/wn_tagger.py`

In such cases, the full file path must be specified for the input file.

# How to run
------------

To a certain extent, this can be run straight from the command line.
Example inputs: 

  * `python wn_tagger.py xml curdie english noun 'hypen, hypon'`
  * `python wn_tagger.py cqp curdie`

Necessary arguments:
  * `python wn_tagger.py` - To run the file. 
  * `xml` or `cqp` - the output file format
  * `curdie` - example input file (in the same directory, or with full
    path)

Optional arguments (these will be requested if not given)
  * `english` or `german` - language for the tagger. German wordnet is
    not currently supported.
  * `noun` or `verb` - the part of speech to be tagged.
  * `hypen, hypon` - The desired wordnet extractions, comma and space delineated. For a single argument, type simply `hypen`.

Once the script has run, the ouput file should be in file
`output\_input-file-name\_format`. An example output can be seen in
the file `output\_curdie\_cqp`.

# Development
-------------

For a list of development issues and tasks, consult the issues list
(this repository). For questions, leave a comment, or write to me. 

To do:
-------
  * Make workable on a previously tagged text (ignore xml, tagging)
  * Make it executable outside of Mac OSX
  * Make it grab wordnet information externally 
  * Use an existing XML schema instead of the provisional one provided here
  * More options.


# License
-----------

This program is licensed under the [GPL-3 license](http://www.gnu.org/licenses/gpl-3.0.txt). 
