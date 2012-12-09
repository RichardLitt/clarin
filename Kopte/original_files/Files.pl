#!/usr/bin/perl -w
###################################################################
###                                                             ###
###    Author: Hannah Kermes                                    ###
###   Purpose: Operations on and in files                       ###
###   Created: Tue Jul 30 10:29:02 2002                         ###
###  Modified: Wed Jun  8 18:17:08 2011 (hannah)                ###
###                                                             ###
###################################################################
# 
# 
# 

package Files;

use lib "/usr/bin/lib/";
use FileHandle;


sub open_infile {
  my $file = shift;

  $in = new FileHandle("$file")
    or die "ERROR: cannot open $file: $!\n";

  return $in;
}

sub open_outfile {
  my $file = shift;
  
  $in = new FileHandle(">$file")
    or die "ERROR: cannot open $file: $!\n";

  return $in;
}

sub open_appendfile {
  my $file = shift;
  
  $in = new FileHandle(">>$file")
    or die "ERROR: cannot open $file: $!\n";

  return $in;
}

sub fileglob {
    my $f = shift;
    my $end = shift;

    $end = "" if (not defined $end);

    if (-d $f) {
	@files = glob "$f/*$end";
    }
    elsif (-f $f) {
	@files = ($f);
    }
    else {
	@files = glob "$f*$end";
    }
    return @files;
}

sub basedir {
    my $basedir = shift;
    if (-d $basedir) {
    }
    else {
	$basedir =~ s/[^\/]+$//;
    }
    return $basedir;
}

sub mkdir {
    my $dir = shift;

    if (not -d $dir) {
	Files::print_message("mkdir $dir");
	system "mkdir $dir";
    }
}

sub clean_dir {
  my $dir = shift;

  if (-d $dir) {
#      Files::print_message_tab("cleaning up in $dir ...");
      system "rm -f $dir/*\.*";
  }
}

sub notdir_next {
    my $dir = shift;
    if (not -d $dir) {
	Files::print_message("ERROR: $dir is not a directory");
	next;
    }
}

sub notfile_next {
    my $dir = shift;
    if (not -f $dir) {
	Files::print_message("ERROR: $dir is not a directory");
	next;
    }
}

sub notdir_exit {
    my $dir = shift;
    if (not -d $dir) {
	Files::print_message("ERROR: $dir is not a directory");
	exit;
    }
}

sub print_message {
  my $message = shift;
  print $message."\n";
}

sub print_message_time {
  my $message = shift;
  print scalar localtime;
  print "\n\t".$message."\n";
}

sub print_message_tab {
  my $message = shift;
  print "\t".$message."\n";
}



1;
