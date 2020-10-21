import json
import re


def get_terms(preprocessing, index):

    f = open(index)
    file = f.read()
    index_list = json.loads(file)

    if preprocessing == "unfiltered":

        terms = len(index_list)
        print("number of distinct terms in reuters ", terms)

    elif preprocessing == "no_numbers":

        alpha_index = []
        alpha_index_text = open("files/alpha_index.txt", 'w')
        for token in index_list:
            if not (re.search(r'\d', token[0])):
                alpha_index.append(token)
                print(json.dumps(token), file=alpha_index_text)
        terms = len(alpha_index)
        print("number of distinct terms without words in reuters ", terms)
        with open("files/alpha_index.json", mode="w", encoding="utf-8") as myFile:
            json.dump(alpha_index, myFile)


def get_postings(preprocessing, index):
    f = open(index)
    file = f.read()
    naive_index = json.loads(file)
    postings = 0

    for token in naive_index:
        postings += token[1][0]

    if preprocessing == "unfiltered":
        print("number of non-positional postings ", postings)
    elif preprocessing == "no_numbers":
        print("number of non-positional postings without numbers ", postings)


get_terms("unfiltered", "files/naive_indexer.json")

get_postings("unfiltered", "files/naive_indexer.json")

get_terms("no_numbers", "files/naive_indexer.json")

get_postings("no_numbers", "files/alpha_index.json")
