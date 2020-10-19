import json


def get_terms(preprocessing, index):
    f = open(index)
    file = f.read()
    naive_index = json.loads(file)
    terms = len(naive_index)
    print("number of distinct terms in reuters ", terms)


def get_postings(preprocessing, index):
    f = open(index)
    file = f.read()
    naive_index = json.loads(file)
    postings = 0

    for token in naive_index:
        postings += token[1][0]

    print("number of non-positional postings ", postings)


def get_tokens(preprocessing, token_list):
    f = open(token_list)
    file = f.read()
    parsed_token_list = json.loads(file)
    tokens = len(parsed_token_list)
    print("number of word tokens ", tokens)


get_terms("unfiltered", "files/naive_indexer.json")

get_postings("unfiltered", "files/naive_indexer.json")

get_tokens("unfiltered", "files/unsorted_token_list.json")

