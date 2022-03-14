# Script to compute coincidence (F1) between PER tag attributed by
# Alpino parser + DutchCoRef + DutchCoRef neural modulesand
# and mentions of characters according to the
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
        all_mentions.append( row[3] )

# print( all_mentions )

# Create a list of all positions that contain a name
novel_tokens = []
characters_pos_silver = []
novel_conll_file_path = './alpino_data/parsed/20220216/ArnonGrunberg_DeMan_output.conll'
with open ( novel_conll_file_path, 'r' ) as novel_file:
    novel_tokens = novel_file.read().split( '\n' )
    novel_tokens = [ novel_token.split( '\t' )[1:5] for novel_token in novel_tokens if len( novel_token.split( '\t' ) ) > 4 ]

# print( novel_tokens[0:10] )
# => [['1-1', '0', 'Voor', 'voor'], … ]

regex_alpha_only = regex.compile( r'[\p{L}\p{Nl}]+' )
for idx_start, token in enumerate( novel_tokens ):
    for mention in all_mentions:
        mention_parts = mention.split( ' ' )
        match = True
        idx_end = idx_start
        for idx, part in enumerate( mention_parts ):
            idx_end += idx
            if( idx_end < len( novel_tokens ) ):
                # if( ( idx_end < len( novel_tokens ) ) and ( novel_tokens[idx_end][2].lower() != part.lower() ) ):
                alpha_start = regex_alpha_only.match( novel_tokens[idx_end][2].lower() )
                if( alpha_start != None ):
                    alpha_start = alpha_start.group(0)
                    if( alpha_start != part.lower() ):
                        match = False
                else:
                    match = False
            else:
                match = False
        if( match ):
            characters_pos_silver.append( ( idx_start, idx_end, mention ) )

print( characters_pos_silver[0:10] )
# => [(4, 4, 'Samarendra'), (4, 5, 'Samarendra Ambani'), (51, 51, 'Samarendra'), … ]

# Create the list of mentions according to ducoref

def map_mention( mention ):
    ducoref_offset = 1
    mention_parts = mention.split( '\t' )
    if( mention_parts[3]== 'name' ):
        return ( int( mention_parts[1] ) - ducoref_offset, int( mention_parts[2] ) - ducoref_offset, mention_parts[12] )
    else:
        return None

characters_pos_ducoref = []
with open ( './alpino_data/parsed/20220216/ArnonGrunberg_DeMan_output.mentions.tsv', 'r' ) as ducoref_file:
    characters_pos_ducoref = ducoref_file.read().split( '\n' )[1:-1]
    characters_pos_ducoref = [ map_mention( mention ) for mention in characters_pos_ducoref ]
    characters_pos_ducoref = [ mention for mention in characters_pos_ducoref if mention != None ]

print( characters_pos_ducoref[0:10] )
# => [(4, 5, 'Samarendra Ambani'), (20, 20, 'Samarendra’s'), (51, 51, 'Samarendra'), (55, 58, 'de m … ]

characters_pos_silver = [ ( tup[0], tup[1] ) for tup in characters_pos_silver ]
print( characters_pos_silver[0:10] )
characters_pos_ducoref = [ ( tup[0], tup[1] ) for tup in characters_pos_ducoref ]
print( characters_pos_ducoref[0:10] )

false_negatives = 0
true_positives = 0
character_line_refs = []
for tup in characters_pos_silver:
    if( tup in characters_pos_ducoref ):
        true_positives += 1
    else:
        false_negatives += 1

print( 'True positives:', true_positives )
print( 'False negatives:', false_negatives )

false_positives = 0
true_negatives = 0
for tup in characters_pos_ducoref:
    if( tup not in characters_pos_silver ):
        false_positives += 1
    else:
        true_negatives += 1

print( 'True negatives:', true_negatives )
print( 'False positives:', false_positives )

fscore = true_positives / ( true_positives + ( 0.5 * ( false_positives + false_negatives ) ) )

print( 'F1-Score:', fscore )
