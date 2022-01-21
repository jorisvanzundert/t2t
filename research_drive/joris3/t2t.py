import sys
import os
import glob
import regex
import json

from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

def get_input_folder( argv ):
    if( len( argv ) != 2 ):
        return './research_drive/joris2/inputfolder'
    else:
        return argv[0]

def get_output_folder( argv ):
    if( len( argv ) != 2 ):
        return './research_drive/joris2/outputfolder'
    else:
        return argv[1]

# Main
input_folder = get_input_folder( sys.argv )
output_folder = get_output_folder( sys.argv )

results = {}

tokenizer = AutoTokenizer.from_pretrained( 'wietsedv/bert-base-dutch-cased-finetuned-conll2002-ner' )
model = AutoModelForTokenClassification.from_pretrained( 'wietsedv/bert-base-dutch-cased-finetuned-conll2002-ner' )
# model = AutoModelForTokenClassification.from_pretrained( "GroNLP/bert-base-dutch-cased", revision="v1" )

nlp = pipeline( 'ner', model=model, tokenizer=tokenizer )
ner_results = []

file_paths = glob.glob( os.path.join( input_folder, '*' ) )
for file_path in file_paths:
    with open( file_path ) as text_file:
        text = text_file.read()
        ner_results = nlp( text )

with open( os.path.join( output_folder, 'results.txt' ), 'w' ) as results_file:
    results_file.write( json.dumps( str( ner_results ) ) )
