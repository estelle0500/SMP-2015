#!/usr/bin/perl
=pod
  converts csv file into html/xml for use by prompt_generator
  usage: cat 50-sentence.csv | perl csv2html.pl > 50-sentence.xml
=cut

while (<>) {
    chomp;
    ($entry,$eng,$man,$hokkien) = split(/,/);
    $entry =~ s/\s+//;
    if ($entry ne "") {
        print "<h3>$eng<br>$man<br>$hokkien</h3>\n";
    }
}
