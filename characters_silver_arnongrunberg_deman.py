# Script to compute coincidence (F1) between PER tag attributed by
# Alpino parser and mentions of characters according to the
# manual silver standard by Roel Smeets.

import csv
import regex

# Create a dictionary of names for characters
# based on silver data from Roel Smeets.
# NOTE: The Silver data contained the entries
#
# 53,1,Sam,Samarenda,
# 53,1,Sam,Samarenda Ambani,
#
# These have been corrected to:
#
# 53,1,Sam,Samarendra,
# 53,1,Sam,Samarendra Ambani,
#
characters = {}
all_mentions = [] # For check
with open( './data_test/NAMES_ArnonGrunberg_DeMan.csv', 'r' ) as names_file:
    reader = csv.reader( names_file,delimiter=',' )
    for row in reader:
        if( row[1] not in characters.keys() ):
            characters[ row[1] ] = { 'name': '', 'mentions': [] }
        character = characters[ row[1] ]
        character[ 'name' ] = row[2]
        character[ 'mentions' ].append( row[3] )
        all_mentions += row[3].split( ' ' )


# Create a list of all positions that contain a name
novel_lines = []
with open ( './alpino_data/parsed/ArnonGrunberg_DeManZonderZiekte_partok.txt', 'r' ) as novel_file:
    novel_lines = novel_file.read().split( '\n' )

regex_space = regex.compile( r' ' )
found_characters = []
for line in novel_lines:
    for character in characters.values():
        for mention in character[ 'mentions' ]:
            for match in regex.finditer( r'{}\W'.format( mention ), line ):
                par_sen = line.split( '|' )[0]
                line_until_match = line[ 0:match.start() ].split( '|' )[1]
                tok_pos = len( regex_space.findall( line_until_match ) )
                # found_characters.append( ( par_sen, tok_pos, mention ) )
                # In cases such as "Samarendra Ambani" we want to add in
                # a mention for the second (or third name, etc.)
                # if( ' ' in mention ):
                for sub_mention in mention.split( ' ' ):
                    found_characters.append( ( par_sen, tok_pos, sub_mention ) )
                    tok_pos += 1

# We may very well end up with a lot of duplicates in the list due to e.g.
# "Samarendra" and "Samarendra Ambani" both being searched for.
# Therefore we 'set' the list.
found_characters = list( set( found_characters ) )

# Check: all mentions should be found at least once.
# This is by far a guarrantee for accuracy of the silver standard, but it's
# something..
found = [ found_character[2] for found_character in found_characters ]
found = set( found )
print( 'Not found:', set( all_mentions ) - found )
# => {'Aida Ambani', 'H`oney'}
# Checked against text: no mentions in source text.
print( 'Note: Checked against text: no mentions in source text.' )


# Okay, on to evaluation. We want to find per item in the list a PER in
# Andreas' parsing. Each item in the list looks like:
#
# => ('2-2', 7, 'Sam')
#
# Each line in Andreas' parsing:
#
# => ArnonGrunberg_DeMan	2-2	7	Sam	Sam	N(eigen,ev,basis,zijd,stan)	7	appos	PER	-	-	O	1)
#
corefs = []
with open( './alpino_data/parsed/ArnonGrunberg_DeManZonderZiekte_coref.txt', 'r' ) as coref_file:
    corefs = coref_file.read().split( '\n' )
    corefs = [ coref.split( '\t' ) for coref in corefs ]
    # Filter out empty lines and lines with non coref infos.
    corefs = [ coref for coref in corefs if len( coref ) > 1 ]
    corefs = { '{}-{}'.format( coref[1], coref[2] ): coref[3:] for coref in corefs  }

no_matching_coref = []
false_negatives = 0
true_positives = 0
character_line_refs = []
for found_character in found_characters:
    line_ref = '{}-{}'.format( found_character[0], found_character[1] )
    character_line_refs.append( line_ref )
    if( corefs[ line_ref ][5] == 'PER' ):
        true_positives += 1
    else:
        false_negatives += 1

print( 'True positives:', true_positives )
print( 'False negatives:', false_negatives )

false_positives = 0
true_negatives = 0
for line_ref, coref in corefs.items():
    if coref[5]=='PER':
        if( line_ref not in character_line_refs ):
            false_positives += 1
    else:
        if( line_ref not in character_line_refs ):
            true_negatives += 1

print( 'True negatives:', true_negatives )
print( 'False positives:', false_positives )

fscore = true_positives / ( true_positives + ( 0.5 * ( false_positives + false_negatives ) ) )

print( 'F1-Score:', fscore )
