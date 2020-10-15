from nltk import word_tokenize
from bs4 import BeautifulSoup
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import stopwords
import nltk, re, pprint
import json
import string
import argparse
import json
import sys
from os import path


def generate_token_list():

    # load reuters files with the help of NLTK's PlaintextCorpusReader
    sgm_files = PlaintextCorpusReader("reuters", '.*\.sgm')
    sgm_fileIds = sgm_files.fileids() #TO REMOVE LATER

    # for each fileId open the file and read a raw text to return iteratively
    for fileid in sgm_files.fileids():
        f = open("reuters" + '/' + fileid)
        sgm_file = f.read()
        parsed_sgm = BeautifulSoup(sgm_file, 'html.parser')
        for document_text in parsed_sgm.find_all('reuters'):
            doc_id = int(document_text['newid'])
            doc_text = str(document_text.find('text'))
            raw = BeautifulSoup(doc_text, 'html.parser').get_text()
            raw = raw.replace("\u0002", '')
            raw = raw.replace("\u0003", '')
            #raw = raw.translate(str.maketrans('', '', string.punctuation))
            for c in string.punctuation:
                raw = raw.replace(c, " ")
            raw = re.sub(r"\d", "", raw)
            tokens = word_tokenize(raw)
            print(doc_id)
            print(raw)


generate_token_list()
