# Research Log

This log traces the steps taken in various experiments using Andreas van Cranenburgh's dutchcoref system to see how well coref resolution collides with the silver standard delivered by Roel Smeets' manual tagging. We hopw to develop a character identification tool for literary texts based on the knowledge gained from this.

## Docker (pre January 2022)
Refer to /Users/joris/Workspace/alpino-docker/README.md to see how a Docker container was constructed and dutchcoref was installed.

## Parsing Arnon Grunberg's *De Man Zonder Ziekte*

* Converted .epub from Roel to .txt using Calibre 5.34.0 (Mac)

This produces a text file with paragraphs separated by blank lines.

* Used Alpino tools to produce a indexed .txt version with one tokenized sentence per line

```
cd /home/Alpino/Tokenization
./paragraph_per_line /home/dutchcoref/tmp/ArnonGrunberg_DeManZonderZiekte_fragment.txt | ./add_key | ./tokenize.sh | ./number_sents
```

At first this leads to a local error:

```
perl: warning: Setting locale failed.
perl: warning: Setting locale failed.
perl: warning: Please check that your locale settings:
	LANGUAGE = "en_US.utf8",
	LC_ALL = "en_US.utf8",
	LANG = "en_US.utf8"
    are supported and installed on your system.
```

Fixing this with: https://askubuntu.com/questions/162391/how-do-i-fix-my-locale-issue

```
apt-get clean && apt-get update && apt-get install -y locales
locale-gen "en_US.UTF-8"
```

Then it worked. We can store the output in a new .txt file:

```
./paragraph_per_line /home/dutchcoref/tmp/ArnonGrunberg_DeManZonderZiekte_fragment.txt | ./add_key | ./tokenize.sh | ./number_sents > ArnonGrunberg_DeManZonderZiekte_fragment_partok.txt
```

* Then ran Andreas' machinery:

To install follw the instruction in his repo:

```
$ git clone https://github.com/andreasvc/dutchcoref.git
$ cd dutchcoref
$ pip3 install -r requirements.txt
```

Do NOT forget to install the Dutch first names data and the CLIN26 shared task data:

Dutch first names (required)

Download Top_eerste_voornamen_NL_2010.csv from https://www.meertens.knaw.nl/nvb/ (click on "Veelgestelde vragen" and then on the bottom "Klik hier"). Unzip it and put the csv file in the data/ directory.
Number & gender data from Web text (required), CLIN26 shared task data (optional)

Clone this repository under same parent folder as this repository:

```
~/code/dutchcoref $ cd ..
~/code $ git clone https://bitbucket.org/robvanderg/groref.git
```

### After installing I did this to apply
```
cd /home/dutchcoref/tmp
cat ArnonGrunberg_DeManZonderZiekte_fragment_partok.txt | Alpino number_analyses=1 end_hook=xml -parse -flag treebank ArnonGrunberg_DeMan

python3 coref.py --fmt=booknlp tmp/ArnonGrunberg_DeMan > tmp/ArnonGrubger_DeMan/ArnonGrunberg_DeManZonderZiekte_coref.txt
```

* Repeated the proces with full text of Arnon Grunberg's novel
* Copied `De man zonder ziekte - Arnon Grunberg.txt` to `ArnonGrunberg_DeManZonderZiekte.txt`. Removed copyright notice (front matter), and the part numbers "I" an "II", as wel as the 'verantworoding' (back matter).

The result is in `t2t/alpino_data/parsed/ArnonGruberg_DeManZonderZiekte_coref.txt`

## 23 January 2022

Computed F1 for Alpino's parsing PER in comparison with Roel's silver standard. See `characters_silver_arnongrunberg_deman.py` for details. 0.81 F1.


## 16 February 2022

Andrea's sent me some friendly notes on how to engage the neural modules which should improve accuracy of person entity detection.

//----- email January 24, 2022, 12.41PM CET -------------
Hier instructies hoe je de neurale classifier aan kan zetten:
https://github.com/andreasvc/dutchcoref/#neural-modules
Dit model en de annotaties worden beschreven in dit paper: https://aclanthology.org/2021.crac-1.5/

Het corpus bevat de volgende boeken (een deel uit Riddle, een ander deel uit Project Gutenberg):

Abdolah_Koning.tsv                        Kooten_Verrekijker.tsv
Barnes_AlsofVoorbijIs.tsv                 Mansell_VersierMeDan.tsv
Bernlef_ZijnDood.tsv                      Mitchell_NietVerhoordeGebeden.tsv
Bezaz_Vinexvrouwen.tsv                    Moor_SchilderEnMeisje.tsv
Binet_Hhhh.tsv                            Multatuli_MaxHavelaar.tsv
Carre_OnsSoortVerrader.tsv                Nescio_DeUitvreter.tsv
Collins_Hongerspelen.tsv                  Nescio_Dichtertje.tsv
ConanDoyle_SherlockHolmesDeAgraSchat.tsv  Nescio_Titaantjes.tsv
Couperus_ElineVere.tsv                    Rowling_HarryPotterEn.tsv
Dewulf_KleineDagen.tsv                    Siebelink_Oscar.tsv
Eco_BegraafplaatsVanPraag.tsv             Springer_Quadriga.tsv
Eggers_WatIsWat.tsv                       Tolstoy_AnnaKarenina.tsv
Gilbert_EtenBiddenBeminnen.tsv            Vermeer_Cruise.tsv
Grunberg_HuidEnHaar.tsv                   Verne_ReisOmDeWereld.tsv
Hugo_DeEllendigen.tsv                     Voskuil_Buurman.tsv
James_VijftigTintenGrijs.tsv              Weisberger_ChanelChic.tsv
Kinsella_ShopaholicBaby.tsv               Worthy_JamesWorthy.tsv
Kluun_Haantjes.tsv                        Yalom_RaadselSpinoza.tsv
Koch_Diner.tsv

Hier de gender/animacy annotaties: https://drive.google.com/file/d/1qktH_oqpiC3LbkjJURIuMx90QyRyLx5e/view?usp=sharing
(Niet verder verspreiden svp)
Beschrijving van annotatieschema:

features: tab-separated files with entity features: gender and number.
  Each entity is identified by the indices (sentence number, begin/end token)
  of its first mention.
  Gender has values:
  - f (female)
  - m (male)
  - fm (unknown or mixed gender)
  - n (neuter, non-human)

  Any gender except n implies a human entity.

  Number:
  - sg (singular)
  - pl (plural; an entity consisting of multiple individuals/objects)

  The semantic number is annotated (e.g., "the group" is plural since it could be
  referred to by "they"), regardless of the syntactic number.

--
http://andreasvc.github.io

----- email January 24, 2022, 12.41PM CET -----//

NB The attached file is ./data_test/features.zip

//----- email February 5, 2022, 06.41PM CET -----
Andreas van Cranenburgh

Feb 5, 2022, 6:41 PM (11 days ago)

to R.J.H., Joris
Beste Joris,

Misschien had je e.e.a. al aan de praat gekeregen, maar zo niet, bij deze uitgebreidere instructies (ik heb voor de gelegenheid de README verbetert):

    Tokeniseer en parseer de tekst met correcte nummering van alinea's:
    https://github.com/andreasvc/dutchcoref#tokenization-parsing-and-coreference-of-a-text-file
    Pas de neurale modules toe (deze stap is optioneel maar geeft betere resultaten):
    https://github.com/andreasvc/dutchcoref#neural-modules
    Zet ook de optie voor extra output aan:
    https://github.com/andreasvc/dutchcoref#information-on-clusters-mentions-links-and-quotations

Uiteindelijk bevat het bestand "<prefix>clusters.tsv" dan de lijst met entitieiten (cluster=entiteit in deze context) met eigenschappen zoals gender waarop we kunnen evalueren. Voor personages wil je filteren op human=1 en je kan een drempelwaarde voor size toepassen (aantal mentions van de entiteit). Voorbeeld:

id      gender  human   number  size    firstmention    mentions        label
0       fm      1       pl      1       0       0       vrouwen
1       fm      1       pl      1       1       1       we
2       n       0       sg      1       2       2       de penarie
3       fm      1       pl      1       3       3       de dertig zakenvrouwen van het jaar in Nederland
4       n       0       sg      2       4       4,214   Nederland
[...]

Groet,
--
http://andreasvc.github.io

//----- email February 5, 2022, 06.41PM CET -----


I am now following the instructions in the second mail to apply also the neural models.

On Andreas' repo it says:

```
$ pip3 install -r requirements-neural.txt
$ wget https://github.com/andreasvc/dutchcoref/releases/download/v0.1/models.zip
$ unzip models.zip
$ python3 coref.py --neural=span,feat,pron mydocument/ >output.conll
```

However… requirements-neural.txt only differs as to installing scipy. So rather:

```
$ pip3 install scikit-learn
$ wget https://github.com/andreasvc/dutchcoref/releases/download/v0.1/models.zip
$ unzip models.zip
```

(Had to `apt install wget`.)

Andreas advised to use `--outputprefix=output` to generate information on clusters, mentions, links, and quotations. So combining it all, I now try:

```
$ python3 coref.py tmp/ArnonGrunberg_DeMan/ --fmt=booknlp --outputprefix=ArnonGrunberg_DeMan_output
```

Output transfered to `alpino_data/parsed/20220216/` (which is `/work/data/parsed/20220216/` in the Docker container).


Then

```
$ python3 coref.py --neural=span,feat,pron --fmt=booknlp --outputprefix=ArnonGrunberg_DeMan_output tmp/ArnonGrunberg_DeMan/
```

Oh blast, M1 problems:
```
The TensorFlow library was compiled to use AVX instructions, but these aren't available on your machine.
qemu: uncaught target signal 6 (Aborted) - core dumped
```

as per: https://github.com/tensorflow/tensorflow/issues/52845#issuecomment-1025015276
and as per: https://github.com/yaroslavvb/tensorflow-community-wheels/issues/206

```
$ pip install --ignore-installed --upgrade https://tf.novaal.de/barcelona/tensorflow-2.7.0-cp38-cp38-linux_x86_64.whl
```

Well, it's running, but God knows how long it will take. It's not training though, it shouldn't be agonizingly slow, right? (19.18hrs).

It was done at 08.28 the next day, so 13hrs for a mid size novel.


## 21 February 2022
Took a stab at F1 computing silver standard vs. ducoref.

True positives: 1499
False negatives: 279
True negatives: 1484
False positives: 1081
F1-Score: 0.6879302432308398

However, the evaluation is not fair. Andreas' system e.g. gives:

'''
6	21	22	noun	22	-	-	O	f	1	sg	2	Samarendra’s vriendin
7	21	21	name	21	PER	-	O	m	1	sg	7	Samarendra’s
'''

While Roel's standard leads only to one mention "Samarenda".

Therefore the goal for next meeting is figuring out what a **fair comparison is**. At least we want:

* F1 on novel level (just: are character names found, probably a perfect score?)
* Gender recognized well?
* Some heuristic F1 on mention level
* Some heuristic F1 on entity level
* Some heuristic F1 on clustering

Hypothesis: many mentions == important character
	* We can count mentions/clusters and see if they match up to the silver standard which reports the more important characters.
	* Question: is there a threshold for being a somewhat important character


## Monday 14 March 2022

Converted `characters_silver_neural_arnongrunberg_deman.py` to notebook 'Evaluating Ducoref Against a Silver Standard.ipynb`.

--
