import config
import os
import glob
import regex
import json

from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline


def ensure_path( path ):
    if( os.path.isdir( path ) != True ):
        os.mkdir( path )

ensure_path( config.DATA_PATH )
ensure_path( config.RESULTS_PATH )


# Main
tokenizer = AutoTokenizer.from_pretrained( 'wietsedv/bert-base-dutch-cased-finetuned-conll2002-ner' )
model = AutoModelForTokenClassification.from_pretrained( 'wietsedv/bert-base-dutch-cased-finetuned-conll2002-ner' )
# model = AutoModelForTokenClassification.from_pretrained( "GroNLP/bert-base-dutch-cased", revision="v1" )

nlp = pipeline( 'ner', model=model, tokenizer=tokenizer )

file_paths = glob.glob( os.path.join( '.', config.DATA_PATH, '*.txt' ) )
for file_path in file_paths:
    with open( file_path ) as test_file:
        text = test_file.read()
        lines = text.split( )
        ner_results = nlp( text )
    result_path = file_path.split( os.path.sep )[-1].split('.')[0] + '.ner.txt'
    with open( os.path.join( '.', config.RESULTS_PATH, result_path ), 'w' ) as result_file:
        result_file.write( json.dumps( str( ner_results ) ) )
