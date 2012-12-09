##################################################
# Liling's comments on the PERL code are prefaced
# with ###. Note. 
# 
# something like shift/push functions cannot be recoded easily into
# python. And i think there are more than this piece of code that is
# making your program work too.
# 
# i'm sorry but as perl fanatic as i am, i'm not good enough to recode
# some of the built in array functions easily. And i am particularly
# really bad at regex, hahahaaa... so i'm going to give you some
# walkthrough. hope you dont mind. I'll point you out to some online
# tutorials along this walkthrough.
#
# here's the second installment of the code explanation, once you've grasp the idea of that big regex loop, the rest of the code is just a lot of repeated procedures in checking different regex.
# 
##################################################

### the shebang (#!) is just the unix way to tell that system that
### this is a perl script. and the (-w) option is to toggle on the
### warnings.
### http://www.sthomas.net/roberts-perl-tutorial.htm/ch22/Shebang 
### the 1st 2 lines fail because you cannot do (#use lib) on a
### directory. Go to "/home/hannah/bin/lib/" and see what is the exact
### name of the lib file(s). Possibly, you can try 
### Without the final (/), you are using a lib file, not a directory.

#!/usr/bin/perl -w

# The following three comments out were due to failures. Still seems to work?
#use lib "/home/hannah/bin/lib/";
#use lib "/data/resources/Corpora/bin/lib/";
use Getopt::Long;
use FileHandle;
use Files;

### The (#use Files;) doesn't work because perl doesn't have an in-built library call files. They have specific File functions like (use Files::Path) or (use Files::Spec). However there is a library call FileHandle, that's why (use FileHandle;) works. See the perl documentation. http://perldoc.perl.org/index-modules-F.html . 

### GetOptions is a simple function to instantiate to the options when you run the perl script on the terminal. http://www.devshed.com/c/a/Perl/Processing-Command-Line-Options-with-PERL/3/ . This getoption is pretty unix based which python also have http://docs.python.org/library/getopt.html. 

$Opt_utf8 = 0;
$Opt_utf8out = 0;

GetOptions( 
	   "utf8"=> \$Opt_utf8,
           "utf8out" => \$Opt_utf8out,
	  );

## error message: Wrong number of arguments
die "Usage: uam2xml.perl <text-file><UAM-file>\n"
  unless @ARGV == 2;

### So this is something very uniquely "scripty", the (unless) statement. So instead of using (if...elif...else...), in script writing, it's nice to use unless. To recode something with unless to python just makes the code seriously long =)
### see "Initializing hashes of lists" section from http://wiki.python.org/moin/PerlPhrasebook . 
### The other thing is (@ARGV), its equivalence in python is raw_input. see http://docs.python.org/library/functions.html#raw_input

## command line arguments
$txtf = shift @ARGV;

###   $uamf = shift @ARGV;
###   $uamin = open_infile($uamf);
###   while (<$uamin>) {
### 1st thing is what is call the readline operator in perl, in scripting what you want is short and quick typing so in n perl, the < > operators are use http://perldoc.perl.org/functions/readline.html. Instead of the normal readline() in python http://docs.python.org/tutorial/inputoutput.html, perl uses < >. the above lines of code is equivalent to this in python:
### 
###   uamf = raw_input('please enter the path to the textfile')
###   uamin = open (umaf)
###   for line in umain:
### 
### 2nd thing to know is what is called the "default variable" (i.e. $_), in this piece of code when you do the "while (<$uamin>)" line, perl will automatically set the default variable as the current line that you are reading from the < > and the while loop. So let's say you have a text file:
### 
###   this is the 1st line.
###   this is the 2nd line.
### 
### and then you have the code below in perl
### 
###   while (<read_text_above>) {
###     print $_; # that means print the current line.
###   }
### 
### the output will be:
### 
###   this is the 1st line.
###   this is the 2nd line.
### 
### So let's say if you want to use this in the script reading $_ is a lot of trouble, so in perl, the code below will work exactly the same as the one in $_, since $_ is ommitable.
### 
###   while (<read_text_above>) {
###     print; # without explicitly saying $_, it also print the current line.
###   }
###   
### for more info, check out "Perl variable types > scalar" section from the perldoc, http://perldoc.perl.org/perlintro.html. 
### For now, you can treat it as the $_ inside the loop is the current line read by the < > and the while loop. let's go back to the big regex if clause.
### 

$uamf = shift @ARGV;

### This is ultimately perly, so shift function is sort of weird. Perl thinks of arrays like a queue/stack, it can do both.
### So let's say i have an array ['apple', 'banana', 'pear'] in python, we know that array[0] = 'apple' and i could say txtf = array[0] but in perl i simply use the shift which always let the variable (i.e. $txtf) be the first item in the array (i.e. array[0] in python). See http://perl.about.com/od/perltutorials/a/perlshift.htm

$uamin = open_infile($uamf);

### okay, now this is the very weird part that i dont get. open_infile is surely not an inbuilt function in perl. most probably whoever wrote this had already written a function to open input file. normally to open an input file i would have use instead:
###   open FH,"</path/to/input/file.txt";
###   read_line(*FH);
### For more info, and a more python like way of perl file reading, see http://perl.about.com/od/perltutorials/a/readwritefiles.htm

while (<$uamin>) {
### i assume that that (open_infile($uamf)) returns an array of text and each element in the array is one line of text from the inputfile, that's why the code can do a while loop like this.
    chomp;
### as explained previously, the chomp function removes the final newline character (ie. $/ in perl and \n in python)
    if(/<segment /){
	
### if(/<segment /){
### 	
### the above is another one of perl shortcuts, it's equivalent to this in more readable perl:
### 
### if ($_ ~= /<segment /) {
### 
### meaning it's checking whether the current line matches the "<segment " regex. So i assume that in your input files are are lines that has "<segment this is a segment or something", then the match if clause above will say it matches. I'm assuming if you have ran through some serious regex training in python, if not, i suggest that you read up on python regex or basic unix/perl regex too http://perldoc.perl.org/perlretut.html, it's sort of very helpful in scriptiing. 
### 
### Another point to note is when you want to explicitly check something is conditionally equals to something you would use ~= instead of == (like in python). see http://stackoverflow.com/questions/10405868/what-does-mean-in-perl . So in python it might look like this, i like to use the regex module (i.e. import re) in python instead of using crude equivalence:
### 
###   import re
###   pattern_tocheck_if_line_has_<segmentandspace_ = r'[<segment\s]'
### 
###   for line in umain:
###     re.matches(pattern_tocheck_if_line_has_<segmentandspace_, line) # i'm not very sure whether you should use re.matches or re.search but you're the python guy, so you should decide. hahaa...

### So for the next few lines it's trying to do some really crazy checks on the regex:
### 
### 	/start=\'([0-9]+)\'/;
### 	$start = $1;
### 	
### 	/end=\'([0-9]+)\'/;
### 	$end = $1;
### 	
### the above code is equivalent to the below in more readable perl:
### 
### 	if ($_ =~ /start=\'([0-9]+)\'/) {
###     $start = $1; }
### 	if ($_ = /end=\'([0-9]+)\'/) {
###     $end = $1; }

	# begin of segment
	/start=\'([0-9]+)\'/;
	$start = $1;
	# end of segment
	/end=\'([0-9]+)\'/;
	$end = $1;
	# feature annotation
	/features=\'([^\']+)\'/;
	$features = $1;
	# get rid of the feature "annotation"
	$features =~ s/annotation;//;
	# replace ; by |
	$features =~ s/;/|/g;

### This part is rather crazy and it's not exactly elegant but it sort of works i guess. The whole loop is doing some regex substitution. and that's where i'm the weakest. hahahaa... okay, let me check the perldoc and refresh my regex, then get back to you on this chunk of code, okay?

### 	
### But here comes another perly thing, $1, it has some special meaning in perl. It means this "so let's check whether there are any token that matches the '([0-9]+)\' regex, and then i will instantiate $start with that token that matches that regex". if my regex is not wrong '([0-9]+)\' means any continuous chain of digits, i.e. if it matches a number, make $start the same value as that number. The stackoverflow has a very nice explanation on the special $1 variable http://stackoverflow.com/questions/1036285/what-does-1-mean-in-perl or you can search the official perlvar documentations http://perldoc.perl.org/perlvar.html
### 
### 	/features=\'([^\']+)\'/;
### 	$features = $1;
### 
### Now after going through the regex to instantiate $start and $end, we know that the above code can be rewritten into:
### 
### 	if ($_ =~ /features=\'([^\']+)\'/ ) {
### $features = $1; }
### 
### So what the above is saying is if my current line contains the regex pattern "feature=...", i'll instantiate the $feature variable with the token that matches that regex.  I think, and you need to check because my regex knowledge is weak, this regex \'([^\']+)\  means that anything that doesn't contain the "\" character. 
### 
### 	$features =~ s/annotation;//;
### 	$features =~ s/;/|/g;
### 
### now this 2 lines are the magic of perl/unix based regex. the 1st line says this "so i've taken the token that matches my "feature=...." regex, so within that token, i want to replace the "annotation" with null character. so for e.g. if this is how the current line look like:
### 
### <segment 1231441 feature=this is a text ;annotation det cop det nn 123123>
### 
### $start will have the value "1231441"
### $end will have the value "123123"
### $feature will have the value "feature=this is a text; annotation det cop det nn"
### 
### then after the $features =~ s/annotation;//; code, 
### $feature will have the value "feature=this is a text; det cop det nn"
### 
### then after the $features =~ s/;/|/g; line,
### the ; character will be replaced by |
### $feature will have the value "feature=this is a text| det cop det nn"
### 
### Alright, the above description of the regex in the loop should give you a brief idea of what the script is doing, it's reading file performing some clean up using regex and then output into the "cleaned" format. 
	
#	Files::print_message($start);

	push(@{$Start{$start}},$features); 
	push(@{$End{$end}},$features); 

### There's just one thing that i dont use in perl but your script did, he used some push/pop stack/que functions that i'll need to check up the perldoc again.
### so my next (i.e. also the last installment) will just describe the last 2 lines in the loop.
### 
### push(@{$Start{$start}},$features); 
### push(@{$End{$end}},$features); 

    }
}

$uamin->close;

$pretagf = $txtf;
$pretagf =~ s/\.[a-zA-Z]+/.pretag/;

$txtin = open_infile($txtf);
$out = open_outfile($pretagf);

$charcnt = 0;
while (<$txtin>) {
    chomp;
    # split line into single characters
    @characters = split //;
#    Files::print_message(join(":",@characters));
    $btag = "";
    $etag = "";
    $token = "";
    # go through the line character by character
    foreach $char (@characters) {
	# character count
	$charcnt++;

	# CHECK for END segment first
	# we print out the segments after white space or punctuation
	# if the end segment is checked after the print-out
	# we include the next token!!!
	if (exists $End{$charcnt}) {
	    # the position may be the end of more than one segment
	    foreach $feat (@{$End{$charcnt}}) {
#		Files::print_message($feat);
		$feat =~ s/([^|]+)\|//;
		$struc = $1;
		$etag .= "</$struc>";
	    }
	}
	# white space, newline, punctuation
	# if segments
	if ($char =~ /[.:,;?!\n\s]/) {
	    if ($btag) {
		$btag =~ s/</\n</g;
		$btag =~ s/>$/>\n/;
	    }
	    if ($etag) {
		$etag =~ s/>/>\n/g;
		$etag =~ s/^</\n</;
	    }
	    print $out $btag.$token.$etag.$char;
	    $btag = "";
	    $etag = "";
	    $token = "";
	}
	else {
	    $token .= $char;
	}
	# begin of a segment
	if (exists $Start{$charcnt}) {
	    # may be a multiple start position
	    foreach $feat (@{$Start{$charcnt}}) {
#		Files::print_message($feat);
		$feat =~ s/([^|]+)\|//;
		$struc = $1;
		$btag .= "<$struc att=\"|$feat|\">";
		print "<$struc att=\"|$feat|\">";
	    }
	}
	print $char;
	print "</$struc>" if (exists $End{$charcnt});
    }
}
print $out "\n";

$txtin->close;
$out->close;


sub open_infile {
  my $file = shift;

  my $in = FileHandle->new($file,"<:encoding(UTF-8)")
      or die "ERROR: cannot open $file: $!\n" if ($Opt_utf8);

  $in = new FileHandle("$file")
      or die "ERROR: cannot open $file: $!\n" if (!$Opt_utf8);

  return $in;
}

sub open_outfile {
  my $file = shift;
  
  my $out = FileHandle->new($file, ">:encoding(UTF-8)")
    or die "ERROR: cannot open $file: $!\n";

#  $out = new FileHandle(">$file")
#      or die "ERROR: cannot open $file: $!\n";

  return $out;
}
