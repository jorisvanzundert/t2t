import os
import sys
import glob
import regex
import json

def get_input_folder( argv ):
    if( len( argv ) != 2 ):
        return './research_drive/joris/inputfolder'
    else:
        return argv[0]

def get_output_folder( argv ):
    if( len( argv ) != 2 ):
        return './research_drive/joris/outputfolder'
    else:
        return argv[1]

space_regex = regex.compile( r'\s' )
def count_spaces( text ):
    return len( space_regex.findall( text ) )

# 'Main'
input_folder = get_input_folder( sys.argv )
output_folder = get_output_folder( sys.argv )

results = {}

for file_path in glob.glob( os.path.join( input_folder, '*' ) ):
    with open( file_path, 'r' ) as text_file:
        text = text_file.read()
        results[ file_path ] = { 'spaces': count_spaces( text ) }

with open( os.path.join( output_folder, 'results.txt' ), 'w' ) as results_file:
    results_file.write( json.dumps( results ) )
