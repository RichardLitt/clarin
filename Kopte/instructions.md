# Generic File Information

I include the Corpus zip-file I got from Andrea Wurm as well as the test-files I used and my perl-Script.
So far it takes in a text-file and a Stand-off XML-file with annotations that it adds to the text file - still with some small bug.
There are more than one XML-file for each text-file. So once the script is running correctly, we should increase the functionality to add all the annotations from the different XML-files.
Also, the texts from the corpus are stored in separate files, so we need to have a wrapper around to read and process them one after the other.
The file structure is as such:
The text-files are stored under "Corpus"
The Annotations under : "Analyses"
so these are the directories that are the most interesting for us.

I also include my preliminary result file so you get an idea of what the structure should look like.

# German Email

So, now I've looked at it: It looks better.

But still a few things:

Between "led" and "these projects" is the word space
annotated (missing comma). Your script is now available for the annotation
following tokens packed. You could also put the to the previous?

In "Belle Province" is "Province" part of the Negev, annotation, in
UAM is not twice "Belle" annotated, "Province", however. It
is a second problem emerged there possibility can not be
, to determine whether "Province" s to trans-| nt-e or n-gram | ng-k belongs.

In "north of the 49th" should be "the" not actually annotated
It is, however, and not recognizable, to which belongs posev it.
Or is always closed the first attribute standing in the first place?

From then on in each segment a Token is annotated too much. ... Hmm,
somehow it seems to work quite yet.

Have you any idea?

Best regards
Andrea

--------------

Also, jetzt habe ich es angeschaut: Sieht besser aus.

Aber immer noch ein paar Kleinigkeiten:

Zwischen "fuehrte" und "diese Projekte" ist der Wortzwischenraum 
annotiert (fehlendes Komma). Dein Skript hat die Annotation jetzt zum 
folgenden Token gepackt. Koennte man das auch zum vorangehenden legen?

Bei "von Belle Province" ist "Province" Teil der negev-Annotierung, in 
UAM ist zweimal "von Belle" annotiert, "Province" aber nicht. Dabei 
kommt ein zweites Problem ans Tageslicht: es laesst sich naemlich nicht 
feststellen, ob "Province" zu n-trans|nt-e oder zu n-gramm|ng-k gehoert.

Bei "noerdlich des 49." duerfte "des" eigentlich nicht annotiert sein, 
ist es aber, und wieder nicht erkennbar, zu welchem posev es gehoert. 
Oder wird immer das an erster Stelle stehende Attribut zuerst geschlossen?

Ab dann ist in jedem Segment ein Token zu viel annotiert. ... Hmm, 
irgendwie scheint es doch noch nicht ganz zu funktionieren.

Hast du eine Idee?

Viele Gruesse
Andrea
