from nltk import word_tokenize
from bs4 import BeautifulSoup
from nltk.corpus import PlaintextCorpusReader
import re
import string
import json
import itertools


def generate_token_list():

    # load reuters files with the help of NLTK's PlaintextCorpusReader
    sgm_files = PlaintextCorpusReader("reuters", '.*\.sgm')
    token_list = []
    unsorted_token_list = open("unsorted_token_list.txt", 'w')  # use for pretty print the list

    for fileid in sgm_files.fileids():
        f = open("reuters" + '/' + fileid)
        sgm_file = f.read()
        parsed_sgm = BeautifulSoup(sgm_file, 'html.parser')

        for document_text in parsed_sgm.find_all('reuters'):
            block_tokenizer(document_text, token_list, unsorted_token_list)

    with open("unsorted_token_list.json", mode="w", encoding="utf-8") as myFile:
        json.dump(token_list, myFile)


def block_tokenizer(document_text, token_list, unsorted_token_list):

    doc_id = int(document_text['newid'])
    doc_text = str(document_text.find('text'))
    raw = BeautifulSoup(doc_text, 'html.parser').get_text()
    raw = raw.replace("\u0002", '')
    raw = raw.replace("\u0003", '')
    for c in string.punctuation:
        raw = raw.replace(c, " ")
    tokens = word_tokenize(raw)
    for token in tokens:
        token_list.append((token, doc_id))
        print(json.dumps([token, doc_id]), file=unsorted_token_list)


def sort_tokens(unsorted_list):

    f = open(unsorted_list)
    file = f.read()
    res = json.loads(file)
    sorted_list = sorted(res, key=lambda x: x[0])

    with open("sorted_tokens.json", mode="w", encoding="utf-8") as myFile:
        json.dump(sorted_list, myFile)


def remove_duplicates(sorted_list):

    f = open(sorted_list)
    file = f.read()
    sorted_list_res = json.loads(file)
    unique_tokens = []
    term = sorted_list_res[0][0]
    doc_id = sorted_list_res[0][1]
    unique_tokens.append((term, doc_id))

    #print to txt to pretty print
    unique_list = open("sorted_unique_tokens.txt", 'w')
    print(json.dumps([term, doc_id]), file=unique_list)

    for token in sorted_list_res:
        if token[0] == term:
            if token[1] == doc_id:
                continue
            elif token[1] != doc_id:
                doc_id = token[1]
                unique_tokens.append((token[0], token[1]))
                print(json.dumps([token[0], token[1]]), file=unique_list)
        else:
            term = token[0]
            doc_id = token[1]
            unique_tokens.append((token[0], token[1]))
            print(json.dumps([token[0], token[1]]), file=unique_list)

    with open("sorted_unique_tokens.json", mode="w", encoding="utf-8") as myFile:
        json.dump(unique_tokens, myFile)


def generate_posting_list(sorted_list):

    f = open(sorted_list)
    file = f.read()
    res = json.loads(file)
    postings = []
    naive_indexer = []

    #print to txt to pretty print
    naive_indexer_text = open("naive_indexer.txt", 'w')
    cycle = itertools.cycle(res)
    next(cycle)

    for token in res:
        peek_token = next(cycle)
        if token[0] == peek_token[0]:
            postings.append(token[1])
        else:
            if len(postings) > 0:
                postings.append(token[1])
                naive_indexer.append([token[0], [len(postings), postings.copy()]])
                print(json.dumps([token[0], [len(postings), postings.copy()]]), file=naive_indexer_text)
                postings.clear()
            else:
                naive_indexer.append([token[0], [1, [token[1]]]])
                print(json.dumps([token[0], [1, [token[1]]]]), file=naive_indexer_text)

    with open("naive_indexer.json", mode="w", encoding="utf-8") as myFile:
        json.dump(naive_indexer, myFile)


#Use this helper function to test a small amount of data
def test_token_list():

    # load reuters files with the help of NLTK's PlaintextCorpusReader
    sgm_files = PlaintextCorpusReader("reuters", '.*\.sgm')
    sgm_fileIds = sgm_files.fileids() #TO REMOVE LATER
    token_list = []

    f = open("reuters/reut2-000.sgm")
    sgm_file = f.read()
    parsed_sgm = BeautifulSoup(sgm_file, 'html.parser')
    unsorted_token_list = open("unsorted_token_list.txt", 'w') #use for pretty print the list

    for document_text in parsed_sgm.find_all('reuters'):
        doc_id = int(document_text['newid'])
        if doc_id > 4:
            continue
        doc_text = str(document_text.find('text'))
        raw = BeautifulSoup(doc_text, 'html.parser').get_text()
        raw = raw.replace("\u0002", '')
        raw = raw.replace("\u0003", '')
        for c in string.punctuation:
            raw = raw.replace(c, " ")
        raw = re.sub(r"\d", "", raw)
        tokens = word_tokenize(raw)
        for token in tokens:
            token_list.append((token, doc_id))
            print(json.dumps([token, doc_id]), file=unsorted_token_list)

    with open("unsorted_token_list.json", mode="w", encoding="utf-8") as myFile:
        json.dump(token_list, myFile)


generate_token_list()

sort_tokens("unsorted_token_list.json")

remove_duplicates("sorted_tokens.json")

generate_posting_list("sorted_unique_tokens.json")

#test_token_list()